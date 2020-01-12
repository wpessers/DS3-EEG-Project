import os
import json
import pandas as pd


class JsonDataReader:
    @staticmethod
    def read_to_df(electrode_groups, person, stimulus):
        output_path = "../res/output/"
        filename = output_path + person + "_" + stimulus + ".json"
        with open(filename, "r") as f:
            data = json.load(f)
        print(data)

        df_list = [pd.DataFrame.from_dict(data[electrode_group]) for electrode_group in electrode_groups]
        df = pd.concat(df_list, axis=1)
        df = df.loc[:, ~df.columns.duplicated()]

        return df

    @staticmethod
    def get_people():
        output_dir = "../res/output"
        all_files = os.listdir(output_dir)
        people_list = []
        people_dropdown_list = []
        for file_name in all_files:
            person_name = file_name.rsplit("_", 1)[0]
            if person_name not in people_list:
                people_list.append(person_name)

        for person in people_list:
            people_dropdown_list.append({"label": person, "value": person})

        return people_dropdown_list

    @staticmethod
    def get_stimuli():
        output_dir = "../res/output"
        all_files = os.listdir(output_dir)
        stimuli_list = []
        stimuli_dropdown_list = []
        for file_name in all_files:
            stimulus = file_name.split("_")[1].split(".")[0]
            if stimulus not in stimuli_list:
                stimuli_list.append(stimulus)

        for stim in stimuli_list:
            stimuli_dropdown_list.append({"label": stim, "value": stim})

        return stimuli_dropdown_list
