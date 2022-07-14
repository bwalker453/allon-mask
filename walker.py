import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),

		dcc.Dropdown(id='site_dropdown',
               		 options=[
                   	 	{'label': 'ALL Sites', 'value': 'ALL'},
                    		{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                    		{'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                    		{'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                    		{'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                    		],
                    	value='ALL',
                    	placeholder="Select a Launch Site here",
                    	searchable=True
                    	),
		html.Br(),

		html.Div(dcc.Graph(id='success-pie-chart')),
		html.Br(),

		html.P("Payload range (Kg):"),

		dcc.RangeSlider(id='payload_slider', min=0, max=10000, step=1000, marks={0: '0', 1000: '1000', 2000: '2000', 3000: '3000', 4000:'4000',
												5000: '5000', 6000: '6000', 7000: '7000', 8000: '8000',
												9000: '9000', 10000: '10000'}, 

		value=[min_payload, max_payload]),

		html.Div(dcc.Graph(id='success-payload-scatter-chart')),
			])


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site_dropdown', component_property='value'))

def get_pie_chart(site_dropdown):
    if site_dropdown == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', title='Total Successful Launches At All Sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site_dropdown].groupby(['Launch Site', 'class']).size().reset_index(name='class count')
        fig = px.pie(filtered_df, values = 'class count', 
        names = 'class', title=f"Launch Outcome for Site {site_dropdown}")
        return fig

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site_dropdown', component_property='value'), Input(component_id="payload_slider", component_property="value")])

def get_success_payload_scatter_chart(site_dropdown, payload_slider):
    low_value, high_value = payload_slider
    range_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low_value) & (spacex_df['Payload Mass (kg)'] <= high_value)]
    if site_dropdown == 'ALL':
        fig = px.scatter(range_df,x="Payload Mass (kg)", y="class", color="Booster Version Category", title='Payload Mass vs Outcome for all sites')
        return fig
    else:
        site_df1 = range_df[range_df['Launch Site']== site_dropdown]
        fig = px.scatter(site_df1,x="Payload Mass (kg)", y="class", color="Booster Version Category", title=f"Payload and Booster versions for site {site_dropdown}")
        return fig

if __name__ == '__main__':
    app.run_server()