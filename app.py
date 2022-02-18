import altair as alt
from dash import Dash, dcc, html, Input, Output
from vega_datasets import data
import pandas as pd

rank_raw_df = pd.read_csv("breed_rank.csv")
#print(rank_raw_df.head())

cars = data.cars()

# preprocessing goes here
def first_word(input_str):
    return str.split(input_str)[0]

rank_df = rank_raw_df.iloc[:,0:8]
rank_df = rank_df.rename(first_word, axis="columns")
print(rank_df.columns)
rank_df = pd.melt(rank_df, id_vars=['Breed'], value_vars=list(rank_df.columns)[1:7], var_name = 'Year', value_name='Rank')
print(rank_df.head())

# def plot_altair(xcol):
#     chart = alt.Chart(rank_df).mark_line().encode(
#         y=
#     )

def plot_altair(xcol):
    chart = alt.Chart(rank_df).mark_bar().encode(
        x=alt.X(xcol, sort='y'),
        y='Rank:Q',
        tooltip='Rank:Q').interactive()
    return chart.to_html()

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([
    dcc.Dropdown(
        id='xcol', value='Breed',
        options=[{'label': i, 'value': i} for i in rank_df.columns]),
    html.Iframe(
        id='scatter',
        style={'border-width': '0', 'width': '100%', 'height': '400px'},
        srcDoc=plot_altair(xcol='Breed'))])

@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xcol', 'value'))
def update_output(xcol):
    return plot_altair(xcol)

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)