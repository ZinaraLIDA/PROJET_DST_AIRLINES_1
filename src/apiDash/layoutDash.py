from dash import dash_table, html
import dash_core_components as dcc
import numpy as np

def layoutMain():
    app_layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id = 'page-content')
    ])
    return app_layout 


def layoutIndex():    
    index_page = html.Div([
        html.H1("DST Airlines"),
        html.Table([
            html.Tr([
                html.Td([
                    html.Button(dcc.Link("Données de vol", href="/flights", className="textButton"), className="button")        
                ], style={"width":"50%", "textAlign": "center","verticalAlign":"middle"}),
                html.Td([
                    html.Button(dcc.Link("Statistiques", href="/stats", className="textButton"), className="button")
                ], style={"width":"50%", "textAlign": "center","verticalAlign":"middle"})
            ])
        ], style={"width":"100%", "height":"100px"})
    ], id="divIndex")
    return index_page

def layoutStatFlights(params):
    # Table pour le layout de la Stat StatFlightsCompany
    select_div = html.Table([
            html.Tr([
                html.Td([
                    dcc.DatePickerRange(
                            id="select_dates",
                            min_date_allowed=params["init_start_date"],
                            max_date_allowed=params["init_end_date"],
                            start_date=params["start_date"],
                            end_date=params["end_date"],
                            start_date_placeholder_text="Début de période",
                            end_date_placeholder_text="Fin de période",
                            display_format="DD-MM-YYYY"
                            )
                ], style={"textAlign": "center","verticalAlign":"middle"}),
                html.Td([" "], style={"textAlign": "center","verticalAlign":"middle", "width":"50px"}),
                html.Td([" Les "], style={"textAlign": "center","verticalAlign":"middle"}),
                html.Td([
                dcc.Dropdown(id = 'row_limit',
                options=[{'label': i, 'value': i} for i in np.array([i for i in range(5,21)])],
                    multi = False, clearable=False, value=params["row_limit"]),
                ], style={"textAlign": "center","verticalAlign":"middle"}),
                html.Td([" compagnies avec le plus grand nombre de vols",
                    dcc.Input(id="df_sort", type="hidden", value="")
                    ], style={"textAlign": "center","verticalAlign":"middle", "display": "hidden"})
            ])
        ], id="select_table", style={"marginLeft": "auto", "marginRight": "auto"})
    return select_div

def layoutStatDelay(params):
    # Table pour le layout de la Stat StatDelayCompany
    select_div = html.Table([
                html.Tr([
                    html.Td([
                        dcc.DatePickerRange(
                                id="select_dates",
                                min_date_allowed=params["init_start_date"],
                                max_date_allowed=params["init_end_date"],
                                start_date=params["start_date"],
                                end_date=params["end_date"],
                                start_date_placeholder_text="Début de période",
                                end_date_placeholder_text="Fin de période",
                                display_format="DD-MM-YYYY"
                                )
                    ], style={"textAlign": "center","verticalAlign":"middle"}),
                    html.Td([" "], style={"textAlign": "center","verticalAlign":"middle", "width":"50px"}),
                    html.Td([" Les "], style={"textAlign": "center","verticalAlign":"middle"}),
                    html.Td([
                    dcc.Dropdown(id = 'row_limit',
                    options=[{'label': i, 'value': i} for i in np.array([i for i in range(5,21)])],
                        multi = False, clearable=False, value=params["row_limit"]),
                    ], style={"textAlign": "center","verticalAlign":"middle"}),

                    html.Td([" compagnies avec le plus de retards",
                        dcc.Input(id="df_sort", type="hidden", value="")
                        ], style={"textAlign": "center","verticalAlign":"middle", "display": "hidden"})

                ])
            ], id="select_table", style={"marginLeft": "auto", "marginRight": "auto"})
    return select_div


def layoutStatAircrafts(params):
    # Table pour le layout de la Stat StatAircrafts
    select_div = html.Table([
                html.Tr([
                    html.Td([
                        dcc.DatePickerRange(
                                id="select_dates",
                                min_date_allowed=params["init_start_date"],
                                max_date_allowed=params["init_end_date"],
                                start_date=params["start_date"],
                                end_date=params["end_date"],
                                start_date_placeholder_text="Début de période",
                                end_date_placeholder_text="Fin de période",
                                display_format="DD-MM-YYYY",
                                style={"display": "none"}
                                )
                        ], style={"textAlign": "center","verticalAlign":"middle"}),
                    html.Td([" "], style={"textAlign": "center","verticalAlign":"middle", "width":"50px"}),
                    html.Td([" Les "], style={"textAlign": "center","verticalAlign":"middle"}),
                    html.Td([
                        dcc.Dropdown(id = 'row_limit',
                        options=[{'label': i, 'value': i} for i in np.array([i for i in range(5,21)])],
                            multi = False, clearable=False, value=params["row_limit"])
                        ], style={"textAlign": "center","verticalAlign":"middle"}),
                    html.Td([" avions "
                        ], style={"textAlign": "center","verticalAlign":"middle"}),
                    html.Td([
                        dcc.Dropdown(id = 'df_sort',
                        options=[{"label": "les plus rapides", "value": "speed_max"},
                            {"label": "qui volent le plus haut", "value": "alt_max"}],
                        multi = False, clearable=False, value=params["df_sort"])
                        ], style={"textAlign": "center","verticalAlign":"middle"}),
                    ], style={"textAlign": "center","verticalAlign":"middle"}),
                ], id="select_table", style={"marginLeft": "auto", "marginRight": "auto"})
    return select_div    


def layoutStatFleets(params):
    # Table pour le layout de la Stat StatFleets
    select_div = html.Table([
                html.Tr([
                    html.Td([
                        dcc.DatePickerRange(
                                id="select_dates",
                                min_date_allowed=params["init_start_date"],
                                max_date_allowed=params["init_end_date"],
                                start_date=params["start_date"],
                                end_date=params["end_date"],
                                start_date_placeholder_text="Début de période",
                                end_date_placeholder_text="Fin de période",
                                display_format="DD-MM-YYYY",
                                style={"display": "none"}
                                )
                        ], style={"textAlign": "center","verticalAlign":"middle"}),
                    html.Td([" "], style={"textAlign": "center","verticalAlign":"middle", "width":"50px"}),
                    html.Td([" Les "], style={"textAlign": "center","verticalAlign":"middle"}),
                    html.Td([
                        dcc.Dropdown(id = 'row_limit',
                        options=[{'label': i, 'value': i} for i in np.array([i for i in range(5,21)])],
                            multi = False, clearable=False, value=params["row_limit"])
                        ], style={"textAlign": "center","verticalAlign":"middle"}),
                    html.Td([" compagnies ayant le plus d'avions"
                        ], style={"textAlign": "center","verticalAlign":"middle"}),
                    html.Td([
                        dcc.Input(id="df_sort", type="hidden", value="")
                        ], style={"textAlign": "center","verticalAlign":"middle"}),
                    ], style={"textAlign": "center","verticalAlign":"middle"}),
                ], id="select_table", style={"marginLeft": "auto", "marginRight": "auto"})
    return select_div    


def layoutStatAirplanes(params):
    # Table pour le layout de la Stat StatAirplanes
    select_div = html.Table([
                html.Tr([
                    html.Td([
                        dcc.DatePickerRange(
                                id="select_dates",
                                min_date_allowed=params["init_start_date"],
                                max_date_allowed=params["init_end_date"],
                                start_date=params["start_date"],
                                end_date=params["end_date"],
                                start_date_placeholder_text="Début de période",
                                end_date_placeholder_text="Fin de période",
                                display_format="DD-MM-YYYY",
                                style={"display": "none"}
                                )
                        ], style={"textAlign": "center","verticalAlign":"middle"}),
                    html.Td([" "], style={"textAlign": "center","verticalAlign":"middle", "width":"50px"}),
                    html.Td([" Les "], style={"textAlign": "center","verticalAlign":"middle"}),
                    html.Td([
                        dcc.Dropdown(id = 'row_limit',
                        options=[{'label': i, 'value': i} for i in np.array([i for i in range(5,21)])],
                            multi = False, clearable=False, value=params["row_limit"])
                        ], style={"textAlign": "center","verticalAlign":"middle"}),
                    html.Td([" flottes les plus vétustes"
                        ], style={"textAlign": "center","verticalAlign":"middle"}),
                    html.Td([
                        dcc.Input(id="df_sort", type="hidden", value="")
                        ], style={"textAlign": "center","verticalAlign":"middle"}),
                    ], style={"textAlign": "center","verticalAlign":"middle"}),
                ], id="select_table", style={"marginLeft": "auto", "marginRight": "auto"})
    return select_div    

def layoutSelectStat():
    select_stat = html.Table([
        html.Tr([
            html.Td([
                html.Div("Veuillez choisir une statistique:", className="labelDropdown"),
                 dcc.Dropdown(id = 'list_stats',
                    options=[{'label': "Nombre de vols par compagnie", 'value': "statFlightsCompany"},
                            {'label': "Retard des vols par compagnie", 'value': "statDelayCompany"},
                            {'label': "Vitesse et altitude par type d'avion", 'value': "statAircrafts"},
                            {'label': "Nombre d'avions par compagnie", 'value': "statFleets"},
                            {'label': "Vétusté de la flotte par compagnie", 'value': "statAirplanes"}],
                        multi = False, clearable=False, value="statFlightsCompany", className="dropdown")
            ], style={"textAlign": "center","verticalAlign":"middle"}),
        ])
    ], style={"width":"100%", "height":"100px"})
    return select_stat

def layoutStats(params):
    select_stat = layoutSelectStat()
    select_div = layoutStatFlights(params)

    layout_stats = html.Div([
        html.H1("Statistiques", style={"color": "white", "backgroundColor":"#1e4b6b", "margin":"0"}),
        select_stat, 
        html.Div([
            html.Div([select_div], id="select_div"),
            html.Br(),   
            dcc.Graph(id='graph_stat', className="graph_stat")
            ], style={"color":"white"}),
        html.Div("",id="debug"),
        html.Br(),    
        html.Div([
            html.Button(dcc.Link("Retour", href="/", className="textButton2"), className="button2")
        ], style={"witdh":"100%", "textAlign":"center"}),
    ], id="divStats")
    return layout_stats


def layoutDataFlights(params, dictCountries):
    layout_1 = html.Div([

        html.H1("Données de vol", style={"color": "white", "backgroundColor":"#1e4b6b", "margin":"0"}),

            html.Table([
                
                html.Tr([
                    html.Td([], colSpan=1),
                    html.Td([
                        html.H3("Pays", style={"font-family": "Roboto-Medium", "color": "darkgreen", "font-weight": "bolder", "font-style": "italic"})
                        ], style={"textAlign": "center","verticalAlign":"middle"}, colSpan=2),
                    html.Td([
                        html.H3("Ville", style={"font-family": "Roboto-Medium", "color": "darkgreen", "font-weight": "bolder", "font-style": "italic"})
                        ], style={"textAlign": "center","verticalAlign":"middle"}, colSpan=2),
                    html.Td([
                        html.H3("Aéroport", style={"font-family": "Roboto-Medium", "color": "darkgreen", "font-weight": "bolder", "font-style": "italic"})
                        ], style={"textAlign": "center","verticalAlign":"middle"}, colSpan=2)
                    ], style={"textAlign": "center","verticalAlign":"middle"}),
                
                html.Tr([
                    html.Td([
                        html.H2("Départ", style={'color': 'Marron'})
                        ], style={"textAlign": "center","verticalAlign":"middle"}, colSpan=1),
                    html.Td([
                        html.Div(dcc.Dropdown(id = 'ddCountryDep',
                                    options= ["France"],
                                    value= "France", clearable=False
                            ))
                        ], style={"textAlign": "center","verticalAlign":"middle"}, colSpan=2),
                    html.Td([
                        html.Div(dcc.Dropdown(id = 'ddCityDep',
                                    options= ["Paris"],
                                    value= "Paris", clearable=False
                            )),
                        ], style={"textAlign": "center","verticalAlign":"middle"}, colSpan=2),
                    html.Td([
                        html.Div(dcc.Dropdown(id = 'ddAirportDep',
                                    options= ["Charles de Gaulle"],
                                    value= "Charles de Gaulle", clearable=False
                            ))
                        ], style={"textAlign": "center","verticalAlign":"middle"}, colSpan=2)
                    ], style={"textAlign": "center","verticalAlign":"middle"}),
                
                html.Tr([
                    html.Td([
                        html.H2("Destination", style={'color': 'Marron'})
                        ], style={"textAlign": "center","verticalAlign":"middle"}, colSpan=1),
                     html.Td([
                        html.Div(dcc.Dropdown(id = 'ddCountryArr',
                                    options= [{"label":lab, "value":val} for lab, val in dictCountries.items()], clearable=False
                            ))
                        ], style={"textAlign": "center","verticalAlign":"middle"}, colSpan=2),
                    html.Td([
                        html.Div(dcc.Dropdown(id = 'ddCityArr', clearable=False))
                        ], style={"textAlign": "center","verticalAlign":"middle"}, colSpan=2),
                    html.Td([
                        html.Div(dcc.Dropdown(id = 'ddAirportArr', clearable=False))
                        ], style={"textAlign": "center","verticalAlign":"middle"}, colSpan=2)
                    ], style={"textAlign": "center","verticalAlign":"middle"}),

                ], id="select_table", style={"width":"80%", "height":"100px"}),

        html.Br(),

        html.H2("Vols disponibles", style={"color": "mediumturquoise", "border": "thin solid white", "padding": "5px", "font-family": "Roboto-Medium"}),

        dcc.DatePickerRange(
            id="select_dates",
            min_date_allowed=params["init_start_date"],
            max_date_allowed=params["init_end_date"],
            start_date=params["init_start_date"],
            end_date=params["init_end_date"],
            start_date_placeholder_text="Début de période",
            end_date_placeholder_text="Fin de période",
            display_format="DD-MM-YYYY"
        ),

        html.Div(layoutTableVol([]), id="divTableVols"),
        
        html.Br(),

        html.H2("Carte et données de vol en temps réel", style={"color": "mediumturquoise", "border": "thin solid white", "padding": "5px", "font-family": "Roboto-Medium"}),

        html.Div(id="map"),

        html.Br(),

        html.Button(dcc.Link('Retour', href='/', className="textButton"), className="button")

    ], id="divFlights", style={'alignItems': 'center'})
    return layout_1

def layoutTableVol(data):
    layoutTable =  dash_table.DataTable(id="tableVols",
        columns=[{"name": i, "id": i} for i in ["_id", "airline_iata", "arr_estimated",
        "arr_gate", "arr_terminal", "dep_estimated", "dep_gate", "dep_terminal", "duration", 
        "flight_iata", "status"]], page_size=10, filter_action="native",
        sort_action="native", selected_rows=data, sort_mode="multi", page_action="native")        
    return layoutTable
