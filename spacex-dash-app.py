# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                      dcc.Dropdown(id = 'site-dropdown',
                                            options = [
                                                         {'label': 'ALL SITES', 'value': 'ALL'},
                                                         {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                         {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                         {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                         {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                      ],
                                            value = 'ALL',
                                            placeholder = "Select Launch Site", 
                                            searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                               
# TASK 3: Add a slider to select payload range
# dcc.RangeSlider(id='payload-slider',...)

dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                # marks={0: '0', 100: '100'},
                # If the scale is 0 to 10000, it would make sense to have something like this to match screenshot
                marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                value=[min_payload, max_payload]),                                               
# TASK 4: Add a scatter chart to show the correlation between payload and launch success
html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id = 'success-pie-chart', component_property = 'figure'),
    Input(component_id = 'site-dropdown', component_property = 'value')
)

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        piechart = px.pie(data_frame = spacex_df,
                          names = 'Launch Site', 
                          values = 'class', 
                          title = 'Launches from All Sites'
                         )
        return piechart
    else:
        selected_data = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        piechart = px.pie(data_frame = selected_data, 
                          names = 'class', 
                          title = 'Launches from ' + entered_site
                         )
        return piechart

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id = 'success-payload-scatter-chart', component_property='figure'),
    [Input(component_id = 'site-dropdown', component_property = 'value'),
     Input(component_id = 'payload-slider', component_property = 'value')]
)

def get_scatter_plot(entered_site, payload):
    if entered_site == 'ALL':
        filtered_data = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload[0])
                                  & (spacex_df['Payload Mass (kg)'] <= payload[1])]
        scatterplot = px.scatter(data_frame = filtered_data, 
                                 x = "Payload Mass (kg)", 
                                 y = "class", 
                                 color = "Booster Version Category"
                                )
        return scatterplot
    else:
        selected_data = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        filtered_data = selected_data[(selected_data['Payload Mass (kg)'] >= payload[0])
                                      & (selected_data['Payload Mass (kg)'] <= payload[1])]
        scatterplot = px.scatter(data_frame = filtered_data, 
                                 x = "Payload Mass (kg)", 
                                 y = "class", 
                                 color = "Booster Version Category"
                                )
        return scatterplot

# Run the app
if __name__ == '__main__':
    app.run()
