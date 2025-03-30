"""-------------------------------------------------------
CP321: Assignment 7- Model.py
-------------------------------------------------------
Author:  JD
ID:      169018282
Uses:    pandas,numpy,plotly,dash
Version:  1.0.8
__updated__ = Sun Mar 30 2025
-------------------------------------------------------
"""

import pandas as pd
from bs4 import BeautifulSoup
from requests import get


class Model:
    def __init__(self, url, id):
        self.datasource = url
        self.identifier = id

        self.data = self._load_data()

    def _load_data(self):
        try:
            response = get(self.datasource).text
            soup = BeautifulSoup(response, "html.parser")
            datatable_raw = soup.find("table", class_=self.identifier)

            headers = self._get_headers(datatable_raw)
            data = self._get_table_data(datatable_raw)

            dataset = pd.DataFrame(data=data, columns=headers)

            # Change Location to Host, split the city
            dataset["Host"] = dataset["Location"].apply(
                lambda cell: (cell.split(",")[1]).strip()
            )
            dataset = dataset.iloc[:-1, :]

            return dataset.set_index(headers[0])
        except Exception as e:
            print(f"Failed To Fetch Data: Error: {e}")
            return None

    def _get_headers(self, raw_table):
        header_row = raw_table.find("tr")
        if not header_row:
            return []
        headers = [header.text.strip() for header in header_row.find_all(["th", "td"])]
        return headers

    def _get_table_data(self, raw_table):
        datarows = raw_table.find_all("tr")
        datarows.pop(0)
        data = []
        for row in datarows:
            row = [cell.text.strip() for cell in row.find_all(["th", "td"])]
            data.append(row)
        return data

    def get_years(self):
        return self.data.index

    def get_counts(self, col="Winners"):
        df = self.data[col].value_counts().reset_index()
        df.columns = ["Country", col]
        df = df.sort_values(col, ascending=False)
        return df

    def get_by_year(self, year):
        filtered_df = self.data[self.data.index == year].reset_index()
        filtered_df = filtered_df[["Winners", "Runners-up", "Host"]].T
        filtered_df = filtered_df.reset_index()
        filtered_df.columns = ["Category", "Country"]
        return filtered_df


if __name__ == "__main__":
    DATASOURCE_URL = "https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals"
    TABLE_ID = "plainrowheaders"

    model = Model(DATASOURCE_URL, TABLE_ID)
    print(model.data)
    print("\ntest Model.years")
    print(model.get_years())
    print("\ntest Model.getcounts(Winners)")
    print(model.get_counts(col="Winners"))

    print("\ntest Model.getcounts(Runners-up)")
    print(model.get_counts(col="Runners-up"))

    print("\ntest Model.getcounts(Host)")
    print(model.get_counts(col="Host"))

    print("\ntest Model.get_by_year(1986)")
    print(model.get_by_year("1986"))

    print("\ntest Model.get_by_year(2002)")
    print(model.get_by_year("2002"))
