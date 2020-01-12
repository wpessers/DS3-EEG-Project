import os
import json
import pandas as pd
import re

from pathlib import Path


class Preprocessing():
    def __init__(self, data_dir, electrode_list):
        self._data_dir = data_dir
        self._electrode_list = electrode_list

    def preprocess(self):
        csv_dir = self._data_dir + "input/"
        self.process_csv_files(csv_dir)

    @staticmethod
    def organize_dirs():
        if not os.path.exists('../res/output'):
            os.makedirs('../res/output')

    def process_csv_files(self, csv_dir):
        csv_path = Path(csv_dir).glob("**/*.csv")

        for csv_file in csv_path:
            person_name = str(re.findall(r"(.+)_", str(os.path.basename(str(csv_file)))))[2:-2]
            df = pd.read_csv(csv_file, sep="\t")
            df = df[df["INTERPOLATED"].notnull()]
            df = df.round(4)
            self.dataframe_to_json(df, person_name)

    def dataframe_to_json(self, df, person_name, rows=256):
        for row in df.itertuples(index=True, name='Pandas'):
            if "stimulus" in getattr(row, "COUNTER") and "*" not in getattr(row, "INTERPOLATED"):
                stimulus, index = self.get_metadata(row)

                json_data = {}
                json_data["name"] = person_name
                json_data["stimulus"] = stimulus

                for i in range((len(self._electrode_list) // 2)):
                    json_data[self._electrode_list[i * 2]] = self.get_electrodes_data(df, index + 1, index + rows,
                                                                                      self._electrode_list[(i * 2) + 1])

                self.write_json_file(json_data, person_name, stimulus)

    @staticmethod
    def get_metadata(row):
        stimulus = getattr(row, "INTERPOLATED")
        index = getattr(row, "Index")
        return stimulus, index

    def get_electrodes_data(self, df, start, end, electrodes):
        electrode_group_dict = {}
        electrodes_dict = {}
        for electrode in electrodes:
            electrodes_dict[electrode] = df.loc[start:end, electrode]
            electrode_group_dict[electrode] = json.loads(df.loc[start:end, electrode].to_json(orient="records"))

        electrode_group_dict["mean"] = self.calculate_electrodes_mean(electrodes_dict)

        return electrode_group_dict

    @staticmethod
    def calculate_electrodes_mean(electrodes_dict):
        electrodes_df = pd.DataFrame.from_dict(electrodes_dict)
        mean_df = electrodes_df.mean(axis=1)
        mean_df = mean_df.round(4)
        return json.loads(mean_df.to_json(orient="records"))

    def write_json_file(self, dict, name, stimulus):
        self.organize_dirs()
        json_file_path = self._data_dir + "output/" + name + "_" + stimulus + ".json"

        with open(json_file_path, "w") as fp:
            json.dump(dict, fp, indent=4)