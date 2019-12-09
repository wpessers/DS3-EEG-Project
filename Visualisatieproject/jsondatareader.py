import json
import pandas as pd


class JsonDataReader:
    @staticmethod
    def read_to_df(electrode_groups):
        with open(r'../res/output/Barbara_beloof.json', 'r') as f:
            data = json.load(f)

        df_list = [pd.DataFrame.from_dict(data[electrode_group]) for electrode_group in electrode_groups]
        df = pd.concat(df_list, axis=1)
        df = df.loc[:, ~df.columns.duplicated()]

        return df