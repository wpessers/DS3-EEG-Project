import os
import json
from Visualisatieproject.jsondatareader import JsonDataReader
from Visualisatieproject.preprocessing.preprocessing import Preprocessing


def main():
    data_dir = "../res/"

    electrode_list = ["Anterior Frontal", ["AF3", "AF4"],
                      "Frontal", ["F7", "F3", "F4", "F8"],
                      "Central", ["FC5", "FC6"],
                      "Temporal", ["T7", "T8"],
                      "Posterior", ["P7", "P8"],
                      "Occipital", ["O1", "O2"],
                      "Linguistic", ["F7", "T7"]]
    '''
    p = Preprocessing(data_dir, electrode_list)
    p.preprocess()
    '''
    '''
    lel = "Barbara"
    lol = "beloof"
    output_dir = "../res/output/"
    file = output_dir + lel + "_" + lol + ".json"
    with open(file, "r") as f:
        data = json.load(f)
    print(data)
    '''
    JsonDataReader.read_to_df(electrode_list[0::2], "Barbara", "bes")


if __name__ == "__main__":
    main()