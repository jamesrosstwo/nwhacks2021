import pandas as pd
from src.definitions import ROOT_PATH


def load_data():
    df = pd.read_csv(str(ROOT_PATH / "map/data/CensusDivisionPopulation.csv"), encoding="windows-1252")

    df = df[['Geographic code', 'Population density per square kilometre, 2016', "Province / territory, english"]]

    df = df[df["Province / territory, english"] == "British Columbia"]

    df = df[['Geographic code', 'Population density per square kilometre, 2016']]

    df.columns = ["CSDUID", "density"]

    return df
