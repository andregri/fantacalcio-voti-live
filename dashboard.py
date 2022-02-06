# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine, text
import db as app_db

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(id='live-update-graph'),

    dcc.Interval(
        id='interval-component',
        interval=30*1000, # in milliseconds
        n_intervals=0
    )
])


@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    t = text("""
        SELECT voto, timestamp FROM 
            public.giocatore, 
            public.voto
        WHERE 
            giocatore.id = voto.id_giocatore AND
            giocatore.nome = :nome
    """)
    db_engine = create_engine(app_db.db_string)
    voti_df = pd.read_sql(t, db_engine, params={'nome': 'BARAK'})
    fig = px.line(voti_df, x="timestamp", y="voto")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
