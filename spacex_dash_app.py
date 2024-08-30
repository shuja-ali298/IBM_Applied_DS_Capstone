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

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                               dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                    ] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                ),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=min_payload,
                                                max=max_payload,
                                                step=1000,
                                                marks={int(min_payload): f'{min_payload} kg', 
                                                       int(max_payload): f'{max_payload} kg'},
                                                value=[min_payload, max_payload]),

                                html.Br(),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Pie chart for all sites
        fig = px.pie(spacex_df, values='class', 
                     names='Launch Site', 
                     title='Total Success Launches by Site')
    else:
        # Filter the dataframe by the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, 
                     names='class', 
                     title=f'Total Success Launches for site {selected_site}')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, selected_payload_range):
    low, high = selected_payload_range
    if selected_site == 'ALL':
        # Filter data based on payload range only
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
        title = f'Success Count for Payload Mass between {low} kg and {high} kg for All Sites'
    else:
        # Filter data based on payload range and selected site
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_site) & 
                                (spacex_df['Payload Mass (kg)'] >= low) & 
                                (spacex_df['Payload Mass (kg)'] <= high)]
        title = f'Success Count for Payload Mass between {low} kg and {high} kg at {selected_site}'

    # Create the scatter plot
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                     color='Booster Version Category',
                     title=title)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
