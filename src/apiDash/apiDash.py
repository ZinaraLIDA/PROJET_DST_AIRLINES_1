#!/bin/python3
import dash
from dash import ctx
import dash_core_components as dcc
from dash.dependencies import Output,Input, State
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
from moduleDash import *
from layoutDash import *
import os
from datetime import datetime, timedelta
from itertools import cycle
import plotly
import plotly.express as px

# Pour afficher les "print" dans le log du pod kubernetes
os.environ["PYTHONUNBUFFERED"] = "1"
os.environ["PYTHONIOENCODING"] = "UTF-8"

# Récupération des variables
c_api_mongo, c_api_sql, dep_iata, init_start_date, init_end_date = initApp()

# Récupération des DataFrames
df_airlines, df_active_airlines, df_aircrafts, df_airplanes_groupby, df_airplanes, df_airports, dictCountries, df = \
    createDataframe(c_api_mongo, c_api_sql, dep_iata)

# Instance Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# layout principal
app.layout = layoutMain()

# layout Page Index
index_page = layoutIndex()

# callback Page Stats
@app.callback(Output(component_id='graph_stat', component_property='figure'),
            Output(component_id='select_div', component_property='children'),
            [Input(component_id='list_stats', component_property='value'),
            Input('select_dates', 'start_date'),
            Input('select_dates', 'end_date'),
            Input('row_limit', 'value'),
            Input('df_sort', 'value')
            ])
def update_stats(stat, start_date, end_date, row_limit, df_sort):

    init_start_date, init_end_date = getDateRange(c_api_mongo)

    fig = make_subplots(rows=1, cols=1, shared_yaxes=True)

    # Stat Nb Vol / compagnie
    if stat=="statFlightsCompany":
        select_div = layoutStatFlights({"init_start_date": init_start_date,
                                    "init_end_date": init_end_date,
                                    "start_date": start_date,
                                    "end_date": end_date,
                                    "row_limit": row_limit})

        response = postData(c_api_mongo, "statFlightsCompany", {'dates': [start_date, end_date], 'sort': {'nb_departure':-1}, 'limit': row_limit})
        df = pd.DataFrame(list(response))
        df = df.merge(df_airlines, how='inner', left_on='_id', right_on='_id')

        fig.add_trace(go.Bar(x=df["airline_name"], y=df["nb_departure"],marker=dict(color=df["nb_departure"], coloraxis="coloraxis"),
        text=df["nb_departure"], 
        hovertemplate=list((row["airline_name"]+" ("+row["country_name"]+")<br>"+"Nombre de départ total: "+str(row["nb_departure"])+"<br>Nombre de départ moyen par jour: "+str(int(row["departure_day_avg"])) for ind, row in df.iterrows())))
        , 1, 1)
        fig.update_layout(coloraxis=dict(colorscale='magenta'), yaxis_title="Nombre de vols", showlegend=False)

    # Stat Retard / compagnie
    if stat=="statDelayCompany":
        select_div = layoutStatDelay({"init_start_date": init_start_date,
                                    "init_end_date": init_end_date,
                                    "start_date": start_date,
                                    "end_date": end_date,
                                    "row_limit": row_limit})

        response = postData(c_api_mongo, "statDelayCompany", {'dates': [start_date, end_date], 'sort': {'delayed_avg':-1}, 'limit': row_limit})
        df = pd.DataFrame(list(response))
        df["delayed_avg"] = df["delayed_avg"].astype("int")
        df = df.merge(df_airlines, how='inner', left_on='_id', right_on='_id')

        fig = go.Figure(data=[
            go.Bar(name='Retard maximum', x=df["airline_name"], y=df["delayed_max"], text=df["delayed_max"], marker=dict(color="#b82828"),
                hovertemplate=list((row["airline_name"]+" ("+row["country_name"]+")<br>"+\
                "Retard moyen: "+str(row["delayed_avg"])+"<br>"+\
                "Retard le plus long: "+str(int(row["delayed_max"]))+"<br>"+\
                "Nombre de vols total: "+str(int(row["nb_flights"]))\
                for ind, row in df.iterrows())), base=0
            ),
            go.Bar(name='Retard moyen', x=df["airline_name"], y=df["delayed_avg"], text=df["delayed_avg"], marker=dict(color="#ecb557"),
                hovertemplate=list((row["airline_name"]+" ("+row["country_name"]+")<br>"+\
                "Retard moyen: "+str(row["delayed_avg"])+"<br>"+\
                "Retard le plus long: "+str(int(row["delayed_max"]))+"<br>"+\
                "Nombre de vols total: "+str(int(row["nb_flights"]))\
                for ind, row in df.iterrows())), base=0
            )
        ])
        fig.update_yaxes(range=[0,240], dtick=30)
        fig.update_layout(barmode='stack', yaxis_title="Retard en minutes", showlegend=True)


    # Stat Vitesse-Altitude / Avion
    if stat=="statAircrafts":
        if df_sort != "speed_max" and df_sort != "alt_max": 
            df_sort = "speed_max"
        select_div = layoutStatAircrafts({"init_start_date": init_start_date,
                                    "init_end_date": init_end_date,
                                    "start_date": start_date,
                                    "end_date": end_date,
                                    "row_limit": row_limit,
                                    "df_sort": df_sort})


        response = postData(c_api_mongo, "statAircrafts", {'sort': {df_sort:-1}, 'limit': 0})
        df = pd.DataFrame(list(response))
        df = df.merge(df_airplanes_groupby, how='inner', left_on='_id', right_on='_id')
        df = df.merge(df_aircrafts, how='inner', left_on='aircraft_iata', right_on='iata_code')
        df = df.iloc[:row_limit]
        colors = cycle(plotly.colors.qualitative.Alphabet)
        marker_aircraft = []
        n = 0
        for aircraft in df["aircraft_name"]:
            n += 1
            df_marker = df[df["aircraft_name"] == aircraft]
            marker_aircraft.append(
                go.Scatter(name=aircraft, x=df_marker["speed_max"], y=df_marker["alt_max"],
                mode = 'markers',
                marker = dict(size=20),
                marker_color = next(colors),
                hovertemplate=list((df_marker["aircraft_name"]+"<br>"+\
                "Altitude maximum: "+str(int(df_marker["alt_max"]))+"<br>"+\
                "Vitesse maximum: "+str(int(df_marker["speed_max"]))+"<br>"+\
                "Vitesse moyenne: "+str(int(df_marker["speed_avg"]))\
                ))
            )
            )
        fig = go.Figure(data=marker_aircraft)
        fig.update_layout(yaxis_title="Altitude", xaxis_title="Vitesse", showlegend=True)


    # Stat Nb d'avions / compagnie
    if stat=="statFleets":
        select_div = layoutStatFleets({"init_start_date": init_start_date,
                                    "init_end_date": init_end_date,
                                    "start_date": start_date,
                                    "end_date": end_date,
                                    "row_limit": row_limit,
                                    "df_sort": df_sort})

        response = postData(c_api_mongo, "statFleets", {'sort': {"nb_aircrafts":-1}, 'limit': 0})
        df = pd.DataFrame(list(response))
        df = df.merge(df_active_airlines, how='inner', left_on='_id', right_on='_id')
        df = df.merge(df_airlines, how='inner', left_on='_id', right_on='_id')
        df = df.iloc[:row_limit]

        fig = px.pie(df, values="nb_aircrafts", names="airline_name")
        fig.update_traces(textposition='inside', textinfo='percent+label',
            hovertemplate=list((row["airline_name"]+" ("+row["country_name"]+")<br>"+\
            "Nombre d'avions': "+str(row["nb_aircrafts"])+"<br>"+\
            "Age moyen des avions: "+str(int(row["plane_age_avg"]))+"<br>"+\
            "Age de l'avion le plus récent: "+str(int(row["plane_age_min"]))+"<br>"+\
            "Age de l'avion le plus ancient: "+str(int(row["plane_age_max"])) \
            for ind, row in df.iterrows()))
        )


    # Stat Vétusté / compagnie
    if stat=="statAirplanes":
        select_div = layoutStatAirplanes({"init_start_date": init_start_date,
                                    "init_end_date": init_end_date,
                                    "start_date": start_date,
                                    "end_date": end_date,
                                    "row_limit": row_limit})

        response = postData(c_api_mongo, "statFleets", {'sort': {"plane_age_avg":-1}, 'limit': 0})
        df_fleets = pd.DataFrame(list(response))
        df_fleets = df_fleets.merge(df_active_airlines, how='inner', left_on='_id', right_on='_id')
        df_fleets = df_fleets.iloc[:row_limit]

        df = pd.DataFrame([])
        for ind, row in df_fleets.iterrows():
            df = pd.concat([df, df_airplanes[df_airplanes["airline_iata_code"]==row["_id"]]], axis=0)
        df = df.merge(df_airlines, how='inner', left_on='airline_iata_code', right_on='_id')
        df.dropna(axis=0, how='any', subset=["plane_age"])
        df['plane_age'] = pd.to_numeric(df['plane_age'])
        df = df.drop(df[df['plane_age'] > 100].index)
        df["airline_title"] = df["airline_name"] + "<br>(" + df["country_name"] + ")"


        fig.add_trace(go.Box(y=df["plane_age"], x=df["airline_title"],
                    marker_color = 'indianred'))

        fig.update_layout(xaxis_title="", yaxis_title="Age moyen des avions de la flotte", showlegend=False)

    return fig, select_div



# CallBack mise à jour des listes et du tableau
@app.callback(Output(component_id='ddCityArr', component_property='options'),
            Output(component_id='ddAirportArr', component_property='options'),
            Output(component_id='tableVols', component_property='data'),
            Output(component_id='map', component_property='children'),
            [Input(component_id='ddCountryArr', component_property='value'),
            Input(component_id='ddCityArr', component_property='value'),
            Input(component_id='ddAirportArr', component_property='value'),
            Input(component_id='select_dates', component_property='start_date'),
            Input(component_id='select_dates', component_property='end_date'),
            Input(component_id='tableVols', component_property='active_cell'),
            State(component_id='tableVols', component_property='data')])
def update_map(filter_country,filter_cities,filter_airport,start_date,end_date,active_cell,data):
    dictCities = {}
    dictAirports = {}
    dataTable = []
    graph = ""
    objevt = ctx.triggered_id
    print(objevt)
    if objevt == "ddCountryArr":
        dictCities = getDictCities(c_api_sql, dep_iata, filter_country)
    elif objevt == "ddCityArr":
        dictCities = getDictCities(c_api_sql, dep_iata, filter_country)
        dictAirports = getDictAirports(c_api_sql, dep_iata, filter_cities)
    elif objevt == "ddAirportArr" or objevt == "tableVols" or objevt == "select_dates":
        if filter_country is not None:
            dictCities = getDictCities(c_api_sql, dep_iata, filter_country)
        if filter_cities is not None:
            dictAirports = getDictAirports(c_api_sql, dep_iata, filter_cities)
        if filter_airport is not None:
            dictSchedules = getDictSchedules(c_api_sql, dep_iata, filter_airport, start_date, end_date)
            df = transformDictToDf(dictSchedules)
            df["dep_estimated"] = df["dep_estimated"].astype(str)
            df = df.sort_values(by="dep_estimated", ascending=False)
            dataTable = df.to_dict('records')
            if objevt == "tableVols" and active_cell:
                row = int(active_cell["row"])
                tab_id = data[row]["_id"]
                dictFlight = getDictFlight(c_api_sql, tab_id)
                dictWeather = getDictWeather(c_api_sql, tab_id)
                df = transformDictToDf(dictFlight, df_airports)
                df_weather = transformDictToDf(dictWeather)
                df = pd.merge(df, df_weather, how='left', left_on = '_id', right_on = 'flight_id')
                df = df.sort_values(by=["_id_x"], ascending=[True])
                hex = df.loc[0, "hex"]
                reg_number = df.loc[0, "reg_number"]
                load_date = df.loc[0, "load_date_x"].split("-")
                load_time = df.loc[0, "load_time_x"].split(":")
                datref = datetime(int(load_date[2]), int(load_date[1]), int(load_date[0]), int(load_time[0]), int(load_time[1])) + timedelta(days=+1)
                idend = tab_id.split("-")[0] + "-" + str(datref.timestamp())
                df = df[(df["hex"] == hex) & (df["reg_number"] == reg_number) & (df["_id_x"] < idend)]
                # print("Trace 1\n", df[["_id_x", "hex", "reg_number", "speed"]])
                graph = dcc.Graph(figure=map(df))
    
    return [lab for lab,val in dictCities.items()], [lab for lab,val in dictAirports.items()], dataTable, graph


# callback page Index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    init_start_date, init_end_date = getDateRange(c_api_mongo)
    dictCountries = getDictCountries(c_api_sql, dep_iata)
    if pathname == '/stats':
        layout_stats = layoutStats({"init_start_date": init_start_date,
                                    "init_end_date": init_end_date,
                                    "start_date": init_start_date,
                                    "end_date": init_end_date,
                                    "row_limit": 10})
        return layout_stats
    elif pathname == '/flights':
        layout_flights = layoutDataFlights({"init_start_date": init_start_date,
                                    "init_end_date": init_end_date,
                                    "start_date": init_start_date,
                                    "end_date": init_end_date}, 
                                    dictCountries)
        return layout_flights
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=True,host="0.0.0.0", port=5010)
