# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into a pandas DataFrame
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get the maximum and minimum payload values
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Create the app layout
app.layout = html.Div(children=[
    html.H1("SpaceX Launch Records Dashboard (by Muhsin IDER)",
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Task 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),
    html.Br(),

    # Task 2: Add a pie chart to show the total successful launches count for all sites
    html.Div([
        dcc.Graph(id='success-pie-chart'),
        html.P('(Footnote: This pie chart represents the success count for all launch sites.)',
               style={'text-align': 'right', 'color': '#888888', 'font-size': '12px'}),
    ]),
    html.Br(),

    html.P("Payload range (Kg):"),

    # Task 3: Add a slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload]
    ),
    html.Br(),

    # Task 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div([
        dcc.Graph(id='success-payload-scatter-chart'),
        html.P('(Footnote: This scatter chart represents the correlation between payload and launch success.)',
               style={'text-align': 'right', 'color': '#888888', 'font-size': '12px'}),
    ]),
    
    # Question and Answer Section
    html.Div([
        html.H2("Questions and Answers", style={'color': '#503D36', 'font-size': 30}),
        
        # Static Questions and Answers
        html.P("1. Which site has the largest successful launches?   \n   - CCAFS LC-40"),
        html.P("2. Which site has the highest launch success rate?   \n   - KSC LC-39A"),
        html.P("3. Which payload range(s) has the highest launch success rate?   \n   - 0 to 1000 kg"),
        html.P("4. Which payload range(s) has the lowest launch success rate?   \n   - 8000 to 9000 kg"),
        html.P("5. Which F9 Booster version has the highest launch success rate?   \n   - F9 B5"),
        
        html.P('(Answers are static and based on the overall dataset)',
               style={'text-align': 'right', 'color': '#888888', 'font-size': '12px'}),
    ]),
    
    # Footnote - last one at the end
    html.P('Prepared by Muhsin IDER', style={'text-align': 'right', 'color': '#888888', 'font-size': '12px'}),
])

# Task 2: Callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', names='Launch Site', title='Success Count for all launch sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df = filtered_df.groupby(['Launch Site', 'class']).size().reset_index(name='class count')
        fig = px.pie(filtered_df, values='class count', names='class', title=f"Total Success Launches for site {entered_site}")
    return fig

# Task 4: Callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def scatter(entered_site, payload):
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0], payload[1])]

    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Success count on Payload mass for all sites')
    else:
        filtered_df_site = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df_site, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title=f"Success count on Payload mass for site {entered_site}")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(port=8059)
