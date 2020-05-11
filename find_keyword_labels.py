def extract_data(keyword_file_name="keywords.txt", transcript_file_name="transcription.txt",
                 validation_set_filename="valid.txt", training_set_filename="train.txt"):
    with open(validation_set_filename, "r") as valid_pages:
        list_valid_pages = [line[0:3] for line in valid_pages]

    with open(training_set_filename, "r") as train_pages:
        list_train_pages = [line[0:3] for line in train_pages]

    with open(keyword_file_name, "r") as all_keywords:
        list_keywords = [line.rstrip() for line in all_keywords]

    with open(transcript_file_name, "r") as all_words_with_labels:
        list_valid_labels = [line.split()[0] for line in all_words_with_labels if line[0:3] in list_valid_pages]

    with open(transcript_file_name, "r") as all_words_with_labels:  # NECESSARY to reopen file for some reason
        list_valid_words = [line.split()[1] for line in all_words_with_labels if line[0:3] in list_valid_pages]

    with open(transcript_file_name, "r") as all_words_with_labels:
        list_train_labels = [line.split()[0] for line in all_words_with_labels if line[0:3] in list_train_pages]

    with open(transcript_file_name, "r") as all_words_with_labels:  # NECESSARY to reopen file for some reason
        list_train_words = [line.split()[1] for line in all_words_with_labels if line[0:3] in list_train_pages]

    return list_keywords, list_valid_words, list_valid_labels, list_train_labels, list_train_words


def find_keyword_labels_in_valid(list_keywords, list_valid_transcript_words, list_valid_labels):
    list_keywords_in_valid = []
    list_keyword_valid_labels = []
    for index_keyword in range(len(list_keywords)):  # search for each word in keywords
        for word in list_valid_transcript_words:  # search through all words for it
            if word == list_keywords[index_keyword]:  # Hit!
                index_word_in_transcript = list_valid_transcript_words.index(word)  # this actually just finds 1st occurrence
                list_keyword_valid_labels.append(
                    list_valid_labels[index_word_in_transcript])  # add corresponding label to list
                list_keywords_in_valid.append(list_keywords[index_keyword])
                break  # stop searching for keyword after first hit
    return list_keyword_valid_labels


def find_keyword_labels_in_train(list_keywords, list_train_transcript_words, list_train_labels):
    list_keyword_train_labels = []
    for index_keyword in range(len(list_keywords)):  # search for each word in keywords
        for word in list_train_transcript_words:  # search through all words for it
            if word == list_keywords[index_keyword]:  # Hit!
                index_word_in_transcript = list_train_transcript_words.index(word)  # this actually just finds 1st occurrence
                list_keyword_train_labels.append(
                    list_train_labels[index_word_in_transcript])  # add corresponding label to list
                break  # stop searching for keyword after first hit
    return list_keyword_train_labels


def find_shared_keywords(list_keywords_in_valid, list_train_transcript_words, list_train_transcript_labels):
    """
    This only works if the all keywords in valid are guaranteed to be in train, but not the other way around!
    If those conditions are not met there are gonna be keywords not present in train in this list.
    :param list_keywords_in_valid:
    :param list_train_transcript_words:
    :param list_train_transcript_labels:
    :return:
    """
    list_keyword_shared_labels = []
    for index_keyword_in_valid in range(len(list_keywords_in_valid)):  # search for each word in keywords
        for word in list_train_transcript_words:  # search through all words for it
            if word == list_keywords_in_valid[index_keyword_in_valid]:  # Hit!
                index_word_in_transcript = list_train_transcript_words.index(word)  # this actually just finds 1st occurrence
                list_keyword_shared_labels.append(
                    list_train_transcript_labels[index_word_in_transcript])  # add corresponding label to list
                break  # stop searching for keyword after first hit
    return list_keyword_shared_labels


def find_keyword_labels_in_valid_all_occurrences(list_keywords, list_valid_words, list_valid_labels):
    list_keywords_in_valid = []
    dict_keyword_valid_labels = {}
    for index_keyword in range(len(list_keywords)):  # search for each word in keywords
        for word in list_valid_words:  # search through all words for it
            if word == list_keywords[index_keyword]:  # Hit!
                indices_words_in_transcript = \
                    [index for index, current_word in enumerate(list_valid_words) if current_word == word]
                dict_keyword_valid_labels[list_keywords[index_keyword]] = \
                    [list_valid_labels[found_indices] for found_indices in indices_words_in_transcript]
                list_keywords_in_valid.append(list_keywords[index_keyword])
    return dict_keyword_valid_labels


list_keywords, list_valid_words, list_valid_labels, list_train_labels, list_train_words = extract_data()
# print(find_keyword_labels_in_valid(list_keywords, list_valid_words, list_valid_labels))
# print(find_keyword_labels_in_train(list_keywords, list_train_words, list_train_labels))
print(find_keyword_labels_in_valid_all_occurrences(list_keywords, list_valid_words, list_valid_labels))
