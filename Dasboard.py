from dash import Dash, html, dash_table,dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc


app = Dash()

world = pd.read_csv("worldometer_data_updated.csv")
country = pd.read_csv("country_wise_updated.csv")
usa = pd.read_csv("usa_county_wise_updated.csv")
day = pd.read_csv("day_wise_updated.csv")
clean_complete = pd.read_csv("covid_19_clean_complete_updated.csv")
full_grouped = pd.read_csv("full_grouped_updated.csv")

# World
diff_cases = ['Total Cases', 'Total Deaths', 'Total Recovered', 'Active Cases', 'Serious/Critical','Total Tests']
# different cases for Covid 19 in World data
f_diff_world = px.pie(world, values=world[diff_cases].sum(), names=diff_cases,
             title='Different cases of Covid 19')

# Country
country_cases = ['Total deaths','Total recovered','Total active','Total cases']


# USA
usa_num_col = usa.select_dtypes(include=['float64', 'int64']).columns
usa_cases = ['Confirmed', 'Deaths']
usa_pie_fig = px.pie(usa, values=usa[usa_cases].sum(), names=usa_cases,
             title='Different cases of Covid 19 in USA')

# Day



# clean complete


# full grouped




app.layout = dmc.Container([
    dmc.Title("Covid 19",color = "blue",size = "h2",align='left'),

    # World
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

    # Country
    dmc.RadioGroup(
        [dmc.Radio(i, value=i) for i in country_cases]
        , id='countries different cases', value = country_cases[0]
    ),
    dmc.Grid([
       dmc.Col(
           [dcc.Graph(figure={}, id='diff cases WHO region')],span=6

       ),
        dmc.Col(
                [dcc.Graph(figure = {}, id = 'diff cases countries')],span=6)
    ]),

    # USA
    dmc.RadioGroup(
        [dmc.Radio(i, value=i) for i in usa_cases]
        , id='usa cases', value=usa_cases[0]
    ),
    dmc.Grid([
        dmc.Col([
            dcc.Graph(figure={}, id='Different_cases_in_USA')

        ],span = 6),
        dmc.Col([
            dcc.Graph(figure = usa_pie_fig, id = "pie_usa")
        ],span = 6)

    ])


    # Day



    # clean complete


    # full grouped


], fluid = True
)
# World
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
    gro_data_cont = world.groupby('Continent')[col_chosen].mean().reset_index()
    f_cont_world = px.bar(gro_data_cont, x='Continent',
                          y=col_chosen,color_discrete_sequence=['#5DE2E7'])
    return fig,f_cont_world

# Country
@callback(

    Output(component_id = 'diff cases WHO region',component_property = 'figure'),
    Output(component_id = 'diff cases countries',component_property = 'figure'),
    Input(component_id ='countries different cases',component_property = 'value')

)
def update_countries_plots(col):
    # group by WHO Region
    gr_cond = country.groupby('WHO Region')[col].mean().reset_index()
    fig1 = px.bar(gr_cond, x = 'WHO Region',y = col, color_discrete_sequence=['#5DE2E7'])

    max_countries = country.groupby('WHO Region')['Country/Region'].agg(
        {max_death := ('Total deaths', "max"), max_confirmed := ('Total cases', 'max'),
         max_recovered := ('Total recovered', 'max')})
    countries = list(x for x in max_countries["Total recovered"])
    y = country[country['Country/Region'].isin(countries)]
    fig2 = px.bar(max_countries, x=countries, y=y[col], color_discrete_sequence=['#5DE2E7'],labels = {
        'x' :"Max Countries in each WHO Region", 'y': col
    })

    return fig1,fig2

# USA
@callback(
    Output(component_id="Different_cases_in_USA",component_property='figure'),
    Input(component_id='usa cases',component_property='value')
)
def update_usa(col):
    usa_cases_scatt = px.scatter_geo(usa, lat= usa_num_col[-4], lon=usa_num_col[-3], color=col)
    return usa_cases_scatt
if __name__ == '__main__':
    app.run(debug=True)