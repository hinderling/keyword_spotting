# open and preprocess data
with open("keywords.txt", "r") as all_keywords:
    list_keywords = [line.rstrip() for line in all_keywords]

with open("transcription.txt", "r") as all_words_with_labels:
    list_transcript_label = [line.split()[0] for line in all_words_with_labels]

with open("transcription.txt", "r") as all_words_with_labels:  # NECESSARY to reopen file for some reason
    list_transcript_word = [line.split()[1] for line in all_words_with_labels]

# keyword search
list_keyword_label = []
for index_keyword in range(len(list_keywords)):  # search for each word in keywords
    for word in list_transcript_word:  # search through all words for it
        if word == list_keywords[index_keyword]:  # Hit!
            index_word_in_transcript = list_transcript_word.index(word)  # this actually just finds 1st occurrence
            list_keyword_label.append(list_transcript_label[index_word_in_transcript])  # add corresponding label to list
            break  # stop searching for keyword after first hit

print(list_keyword_label)