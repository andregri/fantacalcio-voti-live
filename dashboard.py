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
    html.H1(children='Voti Live'),

    html.Div(children='''
        Guarda come variano i voti live nel tempo!
    '''),

    html.P([
        html.Label("Squadra"),
        dcc.Dropdown(id='squadra-dropdown')
    ]),

    html.P([
        html.Label("Giocatore"),
        dcc.Dropdown(id='giocatore-dropdown')
    ]),

    dcc.Graph(id='live-update-graph'),

    dcc.Interval(
        id='interval-component',
        interval=30*1000, # in milliseconds
        n_intervals=0
    )
])


@app.callback(Output('squadra-dropdown', 'options'),
              Input('interval-component', 'n_intervals'))
def update_squadra_dropdown(n):
    t = text("""
        SELECT DISTINCT ON (squadra) squadra
        FROM public.giocatore
        ORDER BY squadra;
    """)
    db_engine = create_engine(app_db.db_string)
    squadre_df = pd.read_sql(t, db_engine)
    return squadre_df['squadra'].tolist()


@app.callback(Output('giocatore-dropdown', 'options'),
              Input('squadra-dropdown', 'value'))
def update_giocatore_dropdown(squadra):
    t = text("""
        SELECT DISTINCT ON (nome) nome
        FROM public.giocatore
        WHERE giocatore.squadra = :squadra
        ORDER BY nome;
    """)
    db_engine = create_engine(app_db.db_string)
    giocatori_df = pd.read_sql(t, db_engine, params={'squadra': squadra})
    return giocatori_df['nome'].tolist()


@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'),
              Input('giocatore-dropdown', 'value'))
def update_graph_live(n, nome_giocatore):
    t = text("""
        SELECT voto, timestamp FROM 
            public.giocatore, 
            public.voto
        WHERE 
            giocatore.id = voto.id_giocatore AND
            giocatore.nome = :nome
    """)
    db_engine = create_engine(app_db.db_string)
    voti_df = pd.read_sql(t, db_engine, params={'nome': nome_giocatore})
    fig = px.line(voti_df, x="timestamp", y="voto")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
