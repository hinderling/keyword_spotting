from pyts.metrics import dtw
import random


#########
# Copy the next line into anaconda prompt to install pyts
# "conda install -c conda-forge pyts"
#########


def dtw_search_sakoechiba(dictionary_image_features="test", index_chosen_image="test", window_size=0.1):
    """
    This is a function that searches for a single word inside the manuscript and returns the dtw distance between the
    selected word and all other words in the sample. !!! DTW is not implemented here !!!

    :param dictionary_image_features: [dictionary] takes a dictionary as an input, that contains the filename of each
        image as key, and stores a list with numerical values inside that key.

    :param window_size: [float] sets the "sakoechiba" margins, which restrain the calculation space and speed up
        the dtw process. This is a FLOAT which represents a fraction of the length of the "search" vectors. Here we have
        5 features, so a window size of 0.2 would mean that having a dtw distance of 1 would already cause the dtw path
        to hit the margin (not cancel tho, just hit afaik).

    :param index_chosen_image: [int] or [string] the index or key (filename) of the image we want to search for in
        our manuscript.

    :return: [list] [dictionary] returns a list with the distances of all words in the manuscript to the
        word of interest. also returns a dictionary containing the paths of the dtw with the corresponding key(filename)
    """

    if dictionary_image_features == "test":  # use made up data if none provided
        dictionary_image_features = {"im1": [9, 0, 4, 0.3, 0.5],  # bullshit data i made up, not good for testing
                                     "im2": [9, 1, 8, 0.2, 0.3],  # bullshit data i made up, not good for testing
                                     "im3": [9, 2, 6, 0.1, 0.4]}  # bullshit data i made up, not good for testing

    # Create some helper-data-structures for iterating though dataset
    list_image_keys = [key for key in dictionary_image_features.keys()]
    list_image_indices = list(range(len(dictionary_image_features)))
    zip_image_indices_and_keys = zip(list_image_keys, list_image_indices)

    # initialization - choose image we want to search for in provided data
    if index_chosen_image == "test":  # choose random image if none provided
        index_chosen_image = random.randint(0, len(dictionary_image_features) - 1)  # random init
        print("chosen image is:", list_image_keys[index_chosen_image], "with index =", index_chosen_image)  # rand-debug
    elif type(index_chosen_image) == type("This is a string"):
        index_chosen_image = list_image_keys.index(index_chosen_image)

    # Start DTW with Sakoechiba-Method
    x = dictionary_image_features[list_image_keys[index_chosen_image]]  # vector we want to compare
    dictionary_image_dtw_paths = {}  # just init, will be written while iterating
    list_image_dtw_values = []  # just init, will be written while iterating

    # iterate through all images in data - also with itself as a control
    for image_key, image_indices in zip_image_indices_and_keys:
        y = dictionary_image_features[image_key]
        dtw_sakoechiba, path_sakoechiba = dtw(x, y, dist='square', method='sakoechiba',
                                              options={'window_size': window_size}, return_path=True)
        dictionary_image_dtw_paths[image_key] = path_sakoechiba
        list_image_dtw_values.append(dtw_sakoechiba)

    return list_image_dtw_values, dictionary_image_dtw_paths


if __name__ == "__main__":  # this will only be executed if THIS .py is the main exec file
    print(dtw_search_sakoechiba(dictionary_image_features="test", index_chosen_image="test", window_size=0.1))
