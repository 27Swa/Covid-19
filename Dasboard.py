from dash import Dash, html, dash_table,dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dill.pointers import children
import dash_mantine_components as dmc


app = Dash()

world = pd.read_csv("worldometer_data_updated.csv")
country = pd.read_csv("country_wise_updated.csv")
usa = pd.read_csv("usa_county_wise_updated.csv")
day = pd.read_csv("day_wise_updated.csv")
clean_complete = pd.read_csv("covid_19_clean_complete_updated.csv")
full_grouped = pd.read_csv("full_grouped_updated.csv")

diff_cases = ['Total Cases', 'Total Deaths', 'Total Recovered', 'Active Cases', 'Serious/Critical','Total Tests']
usa_cases = ['Confirmed', 'Deaths']
usa_pie_fig = px.pie(usa, values=usa[usa_cases].sum(), names=usa_cases,
             title='Different cases of Covid 19 in USA')
# different cases for Covid 19 in World data
f_diff_world = px.pie(world, values=world[diff_cases].sum(), names=diff_cases,
             title='Different cases of Covid 19')


app.layout = dmc.Container([
    dmc.Title("Covid 19",color = "blue",size = "h2",align='left'),
    dmc.RadioGroup(
        [dmc.Radio(i,value = i)for i in diff_cases ]
        ,id='Different cases',value = diff_cases[0]
    ),
    dmc.Grid([
        dmc.Col([
                dcc.Graph(figure = {},id='World map')
        ])

    ]),
    dmc.Grid([
    dmc.Col([
        dcc.Graph(figure=f_diff_world, id='Different_cases')
    ], span = 6),

        dmc.Col([
                dcc.Graph(figure ={}, id='Different_Cases_mean_in_Continent')
        ],span = 6)
    ]),
    dmc.Grid([
        dmc.Col([
            dcc.Graph(figure = usa_pie_fig, id = "pie_usa")
        ],span = 6)

    ])
], fluid = True
)
@callback(
    Output(component_id='World map', component_property='figure'),
    Output(component_id='Different_Cases_mean_in_Continent', component_property='figure'),
    Input(component_id='Different cases', component_property='value')
)
def update_world_plots(col_chosen):

    fig = px.choropleth(world, locations='Country/Region', locationmode='country names',
                        color=col_chosen, hover_name='Continent', projection='natural earth',
                        color_continuous_scale = 'Reds', title="Covid 19 over the World")
    # Condition used
    gro_data_cont =world.groupby('Continent')[col_chosen].mean().reset_index()
    f_cont_world = px.bar(gro_data_cont, x='Continent',
                          y=col_chosen,color_discrete_sequence=['#5DE2E7'])
    return fig,f_cont_world



if __name__ == '__main__':
    app.run(debug=True)