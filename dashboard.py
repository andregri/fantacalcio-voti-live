# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from datetime import datetime, timedelta
import os
import time
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from sqlalchemy import text
import db as app_db

os.environ['TZ'] = 'Europe/Rome'      
time.tzset()

app = Dash(__name__)

server = app.server

db_engine = app_db.db

app.layout = html.Div(children=[
    html.H1(children='Voti Live'),

    html.H2(children='''
        Guarda come variano i voti live durante la partita!
    '''),

    dcc.Dropdown(
        placeholder='Giornata',
        id='giornata-dropdown'
    ),

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


@app.callback(Output('giornata-dropdown', 'options'),
              Input('interval-component', 'n_intervals'))
def update_giornata_dropdown(n):
    t = text("""
        SELECT DISTINCT ON (giornata) giornata
        FROM public.voto
        ORDER BY giornata;
    """)
    #db_engine = create_engine(app_db.db_string)
    giornate_df = pd.read_sql(t, db_engine)
    return giornate_df['giornata'].tolist()


@app.callback(Output('squadra-dropdown', 'options'),
              Input('giornata-dropdown', 'value'))
def update_squadra_dropdown(giornata):
    t = text("""
        SELECT DISTINCT ON (squadra) squadra
        FROM public.giocatore, public.voto
        WHERE voto.giornata = giornata
        ORDER BY squadra;
    """)
    #db_engine = create_engine(app_db.db_string)
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
    #db_engine = create_engine(app_db.db_string)
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
    #db_engine = create_engine(app_db.db_string)
    voti_df = pd.read_sql(t, db_engine, params={'nome': nome_giocatore})

    # Append a dataframe item populated with the last 'voto' and the current time.
    # Time is saturated to 2 hours and 10 minutes.
    if len(voti_df) > 0:
        # create a new 'voto' equal to the last row
        voto_last_row = voti_df['voto'].iloc[-1]

        # saturate time to max 2 hours and 10 minutes from the first row 
        time_last_row = voti_df['timestamp'].iloc[0]
        time = datetime.now()
        time = min(time, time_last_row + timedelta(hours=2, minutes=10))
        new_row_df = pd.DataFrame([[voto_last_row, time.strftime("%Y-%m-%d %H:%M:%S")]], columns=['voto','timestamp'])

        voti_df = pd.concat([voti_df, new_row_df], ignore_index=True)

    fig = px.line(voti_df, x="timestamp", y="voto", line_shape='hv')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
