import pickle
from pyts.metrics import dtw
import matplotlib.pyplot as plt

# https://pyts.readthedocs.io/en/stable/auto_examples/metrics/
# plot_dtw.html#sphx-glr-auto-examples-metrics-plot-dtw-py
# installing pyts:https://pyts.readthedocs.io/en/stable/install.html


def main():
    ########## load the stored data ###########
    dictionary_file = open('dictPickle.bin', 'rb')  # reading mode
    feature_dict = pickle.load(dictionary_file)
    dictionary_file.close()

    keywords = ['301-07-06', '301-29-06', '302-34-02', '302-34-01', '300-02-05', '300-17-02', '300-21-04', '302-06-09', '303-09-10', '302-22-02', '300-02-03', '300-27-09', '302-15-07', '300-14-05', '301-09-05', '300-06-03', '302-20-06', '303-14-06', '301-37-03', '301-16-08', '304-19-06', '301-21-07', '302-22-05', '300-04-05', '300-30-03', '304-14-06', '303-04-07', '300-27-07', '302-13-05', '300-11-01', '300-10-04', '301-35-08', '302-30-06', '304-24-02', '300-25-02']

    train_pages = get_train_pages()
    entire_dic, dic = read_transcription(train_pages)

    corresponding_keywords=[]
    corresponding_features=[]
    indeces = []
    distances = []
    for keyword in keywords:
        scores_dict, feat_names = get_scores_dict(keyword, feature_dict)
        print("###", keyword)
        keyword=entire_dic[keyword]
        for feature in feat_names:
            mydic = scores_dict[feature]
            for key in mydic:
                indeces.append(key)
                distances.append(mydic[key])
                corresponding_keywords.append(keyword)
                corresponding_features.append(feature)
    # now features and distances however are unsorted--> I want to sort it but without losing the corresponding index in indeces, i.e
    # the two lists must be mixed exactly in the same way
    #I want to split according to features
    corresponding_features,distances, indeces, corresponding_keywords = (list(t) for t in zip(*sorted(zip(corresponding_features,distances, indeces, corresponding_keywords))))
    nr_of_features=len(feat_names)
    nr_distances_per_feature=len(corresponding_features)/nr_of_features

    feat_nr=0
    for feature in feat_names:
        feat_nr+=1
        lower_bound=int(nr_distances_per_feature*(feat_nr-1))
        upper_bound=int(nr_distances_per_feature*feat_nr)
        featdistances=distances[lower_bound:upper_bound]
        featindeces = indeces[lower_bound:upper_bound]
        featcorresponding_keywords = corresponding_keywords[lower_bound:upper_bound]

        #as already mentioned, those lists are not sorted in respect to the distances--> do that
        featdistances, featindeces,featcorresponding_keywords = (list(t) for t in zip(*sorted(zip(featdistances, featindeces,featcorresponding_keywords))))
        count = 0
        precisions = []
        recalls = []
        TP,FP, FN=initial_TP_FP_FN_calculation(dic, featindeces[0], featcorresponding_keywords[0],featcorresponding_keywords)
        precision, recall=precision_recall_calc(TP,FP,FN)
        precisions.append(precision)
        recalls.append(recall)
        for distance in range(len(featdistances)-1):
            count += 1
            TP,FP,FN = TP_FP_FN_calculation(dic, featindeces[count], featcorresponding_keywords[count], TP,FP, FN)
            precision, recall=precision_recall_calc(TP,FP,FN)
            precisions.append(precision)
            recalls.append(recall)
            if recall==1:
                break

        print("max precision for feature",feature,"is achieved using the", precisions.index(max(precisions))+1, "smallest distances")
        print("max recall for feature", feature, "is achieved using the", recalls.index(max(recalls)) + 1,"smallest distances")
        
        # now I sometimes have more than 1 precision for the same recall value; I only want to keep the first one
        final_precision_list = []
        final_recall_list = []
        index = -1
        for i in recalls:
            index += 1
            if i not in final_recall_list:
                final_recall_list.append(i)
                final_precision_list.append(precisions[index])

        max_precision_index=final_precision_list.index(max(final_precision_list))
        final_precision_list2=final_precision_list[max_precision_index:]
        final_recall_list2=final_recall_list[max_precision_index:]

        plt.plot(final_recall_list2, final_precision_list2, marker='o', markersize=3, color="red")
        plt.xlabel("recall")
        plt.ylabel("precision")
        plt.title("Recall-Precision curve/AP " + str(feature))
        plt.savefig("output_AP "+str(feature))
        plt.show()




def get_scores_dict(keyword, feat_dic):

    ########## calculate DTW ###########
    # get the name of all freatures: (UC, LC, bw_ratio...)
    feat_names = feat_dic[keyword].keys()

    # calculate dtw of all features from a keyword against all words from the
    # "train"-set
    dtw_scores = {ft: None for ft in feat_names}
    for ft in feat_names:  # UC, LC, bw_ratio...
        dtw_scores[ft] = {word: None for word in feat_dic if word[0] == '2'}
        for word in feat_dic:
            if word[0] == '2':  # only compare against words from the "train"-set
                dtw_scores[ft][word] = dtw(feat_dic[keyword][ft], feat_dic[word][ft],
                                           method='sakoechiba', options={'window_size': 0.1})

    # order the dicts by increasing values
    for ft in feat_names:
        dtw_scores[ft] = {k: v for k, v in
                          sorted(dtw_scores[ft].items(), key=lambda item: item[1])}

    return dtw_scores, feat_names


def get_train_pages():
    with open("train.txt", "r") as training_set: #data/task/train.txt
        train_pages=[]
        for line in training_set:
            train_pages.append(line.strip('\n'))
    return train_pages

def read_transcription(train_pages): #data/ground_truth/transcription
    with open("transcription.txt", "r") as all_words:
        dic={} #the entire dic
        train_dic={}
        for line in all_words:
            index = line[0:9]  # index has always same length=9
            word = line[10:].rstrip("\n")
            dic[index] = word
            if line[0:3] in train_pages:
                train_index=line[0:9] #index has always same length=9
                train_word=line[10:].rstrip("\n")
                train_dic[train_index]=train_word
    return dic, train_dic

def initial_TP_FP_FN_calculation(all_words_dic, result_index, keyword, all_keywords):
    TP=0
    FP=0
    FN=0
    for key in all_words_dic:
        if all_words_dic[key] in all_keywords:
            FN+=1
    if all_words_dic[result_index]==keyword:
        TP+=1
        FN-=1
    else:
        FP+=1
    return (TP, FP, FN)

def TP_FP_FN_calculation(all_words_dic, result_index, keyword, TP, FP, FN):
    if all_words_dic[result_index] == keyword:
        TP += 1
        FN-=1
    else:
        FP += 1
    return (TP, FP, FN)

def precision_recall_calc(TP, FP, FN):
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    return (precision, recall)



if __name__ == "__main__":
    main()
