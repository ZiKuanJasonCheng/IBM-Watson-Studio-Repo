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

# Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`
#spacex_df = spacex_df[['Launch Site', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
#launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]
print(launch_sites_df)
list_options = [{'label': 'All sites', 'value': 'ALL'}]
for i, row in launch_sites_df.iterrows():
    list_options.append({'label': row['Launch Site'], 'value': row['Launch Site']})

# df_filtered = spacex_df[spacex_df['class']==1]
# fig = px.pie(df_filtered, values='class', names='Launch Site', title='Success rate by all sites')
# fig.show()

max_range = 10000
min_range = 0
step = 1000
dict_marks = {}
for i in range(min_range, max_range + step, step):
    dict_marks[i] = f'{i}'

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown', options=list_options, placeholder="Select a launch site", 
                                    style={'width': '100%', 'padding': '5px', 'text-align-last': 'center', 'color': '#503D36', 'font-size': 20}
                                    ),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site

                                #html.Div(dcc.Graph(id='success-pie-chart'), style={'display': 'flex'}),
                                dcc.Graph(id='success-pie-chart'),  #style={'display': 'flex'},
                                html.Br(),

                                #html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=min_range, max=max_range, step=step, marks=dict_marks, value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value')
             )
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        print("ALL is selected")
        df_filtered = spacex_df[spacex_df['class']==1]
        print(f"df_filtered: \n{df_filtered}")
        fig = px.pie(df_filtered, values='class', names='Launch Site', title='Success rate by all sites')
        return fig
    elif entered_site is not None:
        print(f"{entered_site} is selected")
        df_filtered_0 = spacex_df[(spacex_df['Launch Site']==entered_site) & (spacex_df['class']==0)]
        df_filtered_1 = spacex_df[(spacex_df['Launch Site']==entered_site) & (spacex_df['class']==1)]
        fig = px.pie(values=[len(df_filtered_0), len(df_filtered_1)], names=[0, 1], title=f'Success rate by {entered_site}')
        return fig
    else:
        return {}

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')]
             )
def get_success_payload_scatter_chart(entered_site, seleted_range):
    print(f"seleted_range: {seleted_range}")
    if entered_site == 'ALL':
        print("ALL is selected")
        #df_filtered = spacex_df[spacex_df['class']==1]
        #print(f"df_filtered: \n{df_filtered}")
        fig = px.scatter(spacex_df, x='Payload Mass (kg)', y='class', color="Booster Version Category")
        fig.update_layout(xaxis_range=seleted_range)
        return fig
    elif entered_site is not None:
        print(f"{entered_site} is selected")
        df_filtered = spacex_df[spacex_df['Launch Site']==entered_site]
        fig = px.scatter(df_filtered, x='Payload Mass (kg)', y='class', color="Booster Version Category")
        fig.update_layout(xaxis_range=seleted_range)
        return fig
    else:
        return {}

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)