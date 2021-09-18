# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

LaunchSites = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': LaunchSites[0], 'value': LaunchSites[0]},
                                                     {'label': LaunchSites[1], 'value': LaunchSites[1]},
                                                     {'label': LaunchSites[2], 'value': LaunchSites[2]},
                                                     {'label': LaunchSites[3], 'value': LaunchSites[3]},
                                                     {'label': 'ALL', 'value': 'ALL'}],
                                             value='ALL',
                                             placeholder='Select a Launch Site here',
                                             searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def piechartGraf(value):
    
    if value == 'ALL':
        df = spacex_df.groupby('Launch Site').sum().reset_index()
        fig = px.pie(df, values=df['class'], names='Launch Site', title='Successes by launch site')
    else:
        df = spacex_df[spacex_df['Launch Site']==value]
        numberSuccess = [len(df[df['class']==1]) ,len(df[df['class']==0])] 
        fig = px.pie(df, values=numberSuccess, names=['Success', 'Failure'], title = 'Success ratio')
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id="payload-slider", component_property='value')
)
def piechartGraf(dropValue,slideValue):
    df_filtered = spacex_df[(spacex_df['Payload Mass (kg)'] < slideValue[1]) & 
                            (spacex_df['Payload Mass (kg)'] > slideValue[0])]
    if dropValue == 'ALL':
        fig = px.scatter(df_filtered, x='Payload Mass (kg)', y='class', color='Launch Site', title='Success distribution by payload')
    else:
        df = df_filtered[df_filtered['Launch Site']==dropValue]
        fig = px.scatter(df, x='Payload Mass (kg)', y='class', title='Success distribution by payload')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
