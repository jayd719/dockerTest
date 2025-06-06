"""-------------------------------------------------------
CP321: Final Project AnalysisView.py
-------------------------------------------------------
Author:  JD
ID:      169018282
Uses:    pandas,numpy,plotly,dash
Version:  1.0.8
__updated__ = Sun Mar 30 2025
-------------------------------------------------------
"""

from dash import dcc, html
from dash import Input, Output
from .model import Model
from .GraphingFunctions import create_pie_chart

STAT_CSS = "card shadow-md hover:shadow-xl rounded-2xl p-6  transition duration-300 border border-gray-100"
STAT_LABEL = "text-sm font-bold text-primary mb-2"
STAT_VAL = "text-2xl font-bold text-gray-800 mt-1"
STAT_COUNT = "text-sm mt-2 text-success"


class GeneralAnalysis:
    def __init__(self, model: Model, app):
        self.model = model
        self.app = app
        self.layout = self._create_layout()
        print(id(self.model))
        self._register_callbacks()

    def _create_layout(self):
        return html.Div(
            className="container mx-auto mb-10",
            children=[self._render_filter_section(), self._render_stats()],
        )

    def _render_filter_section(self):
        return html.Div(
            className="grid grid-cols-2 mx-auto card shadow-md hover:shadow-xl rounded-2xl p-6 border border-gray-100 mb-4",
            children=[
                self._render_region_picker(),
                self._render_education_filter(),
            ],
        )

    def _render_stats(self):
        return html.Div(
            className="grid lg:grid-cols-4 gap-5",
            children=[
                self._render_total_emp_stat(),
                self._render_highest_emp_field(),
                self._render_field_highest_male(),
                self._render_field_highest_female(),
                self._render_field_employment(),
                self._render_field_highest_sex_ratio(),
                self._render_field_lowest_sex_ratio(),
            ],
        )

    def _render_total_emp_stat(self):
        return html.Div(
            className=STAT_CSS,
            children=[
                html.Label(
                    className=STAT_LABEL,
                    children="Total Employed Population",
                ),
                html.H3(
                    className=STAT_VAL,
                    id="total-emp-stat",
                    children="234,424",
                ),
            ],
        )

    def _render_highest_emp_field(self):
        return html.Div(
            className=STAT_CSS,
            children=[
                html.Label(
                    className=STAT_LABEL,
                    children="Field With Highest Employees",
                ),
                html.H3(
                    className=STAT_VAL,
                    id="highest-employe-field",
                    children="Legislative and senior management occupations",
                ),
                html.Label(
                    id="highest-employe-count",
                    className=STAT_COUNT,
                    children="43,1234",
                ),
            ],
        )

    def _render_field_highest_male(self):
        return html.Div(
            className=STAT_CSS,
            children=[
                html.Label(
                    className=STAT_LABEL,
                    children="Field With Highest Male Employees",
                ),
                html.H3(
                    className=STAT_VAL,
                    id="highest-male-field",
                    children="Legislative and se",
                ),
                html.Label(
                    id="highest-male-count",
                    className=STAT_COUNT,
                    children="43,1234",
                ),
            ],
        )

    def _render_field_highest_female(self):
        return html.Div(
            className=STAT_CSS,
            children=[
                html.Label(
                    className=STAT_LABEL,
                    children="Field With Highest Female Employees",
                ),
                html.H3(
                    className=STAT_VAL,
                    id="highest-female-field",
                    children="Legislative and se",
                ),
                html.Label(
                    id="highest-female-count",
                    className=STAT_COUNT,
                    children="43,1234",
                ),
            ],
        )

    def _render_field_highest_sex_ratio(self):
        return html.Div(
            className=STAT_CSS,
            children=[
                html.Label(
                    className=STAT_LABEL,
                    children="Field With Highest Sex Ratio",
                ),
                html.H3(
                    className=STAT_VAL,
                    id="highest-sex-ratio-field",
                    children="Legislative and se",
                ),
                html.Label(
                    id="highest-sex-ratio-count",
                    className=STAT_COUNT + " hidden",
                    children="43,1234",
                ),
            ],
        )

    def _render_field_lowest_sex_ratio(self):
        return html.Div(
            className=STAT_CSS,
            children=[
                html.Label(
                    className=STAT_LABEL,
                    children="Field With Lowest Sex Ratio",
                ),
                html.H3(
                    className=STAT_VAL,
                    id="lowest-sex-ratio-field",
                    children="Legislative and se",
                ),
                html.Label(
                    id="lowest-sex-ratio-count",
                    className=STAT_COUNT + " hidden",
                    children="43,1234",
                ),
            ],
        )

    def _render_field_employment(self):
        return html.Div(
            className=STAT_CSS + " col-span-3 row-span-2",
            children=[
                html.Label(
                    className=STAT_LABEL,
                    children="Regional Employment Distribution by Field",
                ),
                dcc.Graph(id="graph-employment-by-field"),
            ],
        )

    def _render_region_picker(self):
        province_list = self.model.get_province_list()
        return html.Div(
            className="z-[2] ",
            children=[
                html.Label(
                    className="label-text font-medium text-gray-700 mb-2 font-bold",
                    children="Region",
                ),
                dcc.Dropdown(
                    id="province-selector-an1",
                    value=province_list[8],
                    options=province_list,
                    clearable=False,
                    className="w-96",
                ),
            ],
        )

    def _render_education_filter(self):
        return html.Div(
            className="",
            children=[
                html.Label(
                    className="label-text font-medium text-gray-700 mb-2 font-bold",
                    children="Education Level",
                ),
                dcc.RadioItems(
                    id="radio-education",
                    options={
                        "All": "All",
                        "With Postsecondary Education": "With Postsecondary Education",
                        "Without Postsecondary Education": "Without Postsecondary Education",
                    },
                    value="All",
                ),
            ],
        )

    def _register_callbacks(self):

        @self.app.callback(
            [
                Output("total-emp-stat", "children"),
                Output("highest-employe-field", "children"),
                Output("highest-employe-count", "children"),
                Output("highest-male-field", "children"),
                Output("highest-male-count", "children"),
                Output("highest-female-field", "children"),
                Output("highest-female-count", "children"),
                Output("highest-sex-ratio-field", "children"),
                Output("highest-sex-ratio-count", "children"),
                Output("lowest-sex-ratio-field", "children"),
                Output("lowest-sex-ratio-count", "children"),
                Output("graph-employment-by-field", "figure"),
            ],
            [
                Input("province-selector-an1", "value"),
                Input("radio-education", "value"),
            ],
        )
        def handle_region_change(region, education):
            if education == "All":
                df = self.model.filter_df_by_region_and_edu(region)
            else:
                df = self.model.filter_df_by_region_and_edu(region, education)

            total_emps = self.model.total_employes(df)

            (
                hf,
                hc,
            ) = Model.highest_and_lowest_field(df)

            fig = create_pie_chart(df)
            gender_data = Model.gender_analysis(df)
            h_male_f, h_male_c = Model.feild_highest_val(gender_data, "Men")
            h_female_f, h_female_c = Model.feild_highest_val(gender_data, "Women")
            h_ratio_f, h_ratio_v = Model.feild_highest_val(gender_data, "ratio", True)
            l_ratio_f, l_ratio_v = Model.feild_highest_val(gender_data, "ratio", False)
            return (
                total_emps,
                hf,
                f"{hc:,d}",
                h_male_f,
                f"{h_male_c:,d}",
                h_female_f,
                f"{h_female_c:,d}",
                h_ratio_f,
                h_ratio_v,
                l_ratio_f,
                l_ratio_v,
                fig,
            )
