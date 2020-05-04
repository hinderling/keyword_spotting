# Keyword Spotting using Dynamic Time Warping (DTW) in Historical Manuscripts
The goal is to digitizing historical manuscripts for cultural heritage preservation. As there are many historic writing styles and languages, the keyword spotting approach is used. Single words are detected and extracted in the scan. This allows to group toghether reoccuring words, allowing us to decipher multiple occurences of a word at once. To calculate the similarity between the words, we use the dynamic time warping (DTW) distance, which uses a sliding window approach in the direction thw word was originally written by hand. The intuition why this should work better than just calculating the distance between all pixels, is that the letters of two two occurences of the same word are all in the same order, but are stretched differently in the writing direction, with varying distances between the letters. 

E.g.

    Without DTW:       With DTW:  
    
    [Historical ]      [Historical]  
     | | | | | |        | \ \ \ \ \   
    [H istorical]      [H istorical]  

As we can see, the DTW approach allows us to match the corresponding letters, and calculates a much smaller distance between the two words.
The dataset is `WashingtonDB` and contains letters of George Washington from the 18th century, as well as usefull annotations: 

*  `/ground-truth/transcription.txt` Character based transcription

* `/ground-truth/locations/*.svg` Polygons of word segment
    
*  `/images/*.jpg` The page images
    
* `/task/Keywords.txt` Words that are contained in the training an validation set 

