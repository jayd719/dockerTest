"""-------------------------------------------------------
CP321: Final Project ManpowerDistribution
-------------------------------------------------------
Author:  JD
ID:      169018282
Uses:    pandas,numpy,plotly,dash
Version:  1.0.8
__updated__ = Sun Mar 30 2025
-------------------------------------------------------
"""

from dash import dcc, html
from .GraphingFunctions import create_tree_map


class ManpowerDistribution:
    def __init__(self, model, app):
        self.model = model
        self.app = app
        self.layout = self._create_layout()
        print(id(self.model))

    def _create_layout(self):
        df = self.model.get_engineering_df()
        fig = create_tree_map(df)
        return html.Div(
            className="container mx-auto card shadow-md hover:shadow-xl rounded-2xl p-6  transition duration-300 border border-gray-100",
            children=[
                html.H2(
                    className="text-xl font-semibold text-primary mb-5",
                    children="Manpower Analysis for EV Factory Location: Comparing Administrative Units",
                ),
                html.Div(
                    className="grid",
                    children=[
                        dcc.Graph(id="manpower-chart", figure=fig),
                    ],
                ),
            ],
        )
