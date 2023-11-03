import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from datetime import date
import datetime

#construir dashboard
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.title="Precios de commodities"

commodities=pd.read_excel("commodities.xlsx")
commodities_melt=pd.melt(commodities, id_vars=["Fecha","Mes"], var_name='Commodity', value_name='Precio ($)')
commodities_melt=commodities_melt[commodities_melt["Precio ($)"]!=0]

#layout del app
app.layout =  html.Div([
    #primer drop down para elegir las empresas
     html.P("Commodities:"),
   
    html.Div(dcc.Dropdown(
    id="commodities",value=["Petróleo", "Azúcar (por 100)", "Hule", "Café"],clearable=False, multi=True,
    options=["Petróleo", "Azúcar (por 100)", "Hule", "Café"]
    ),className="six columns", style={"width":"50%"},),
    html.Br(),
    html.P("Frecuencia:"),
   
    html.Div(dcc.RadioItems(
    id="frecuencia",value=["Diario"],
    options=["Diario", "Mensual"]
    ),className="six columns", style={"width":"50%"},),
    html.Br(),
    html.P("Rango de fechas:"),
     html.Div( dcc.DatePickerRange(
        id='fechas',
        min_date_allowed=date(2013, 1, 1),
        max_date_allowed=date(2023, 11, 3),
        initial_visible_month=date(2013, 1, 1),
        start_date=date(2013, 1, 1),
        end_date=date(2023, 11, 3),)),
    #graficas
    html.Div([dcc.Graph(id="graph",figure={},config={"displayModeBar":True,"displaylogo":False,
                                                   #"modeBarButtonsToRemove":['pan2d','lasso2d',
                                                   #                         'select2d']
                                                    }),],style={'width':'1100px'})])


#callback de la funcion
@app.callback(
    Output("graph","figure"),
    [Input("commodities","value"), 
     Input("frecuencia","value"),
    Input("fechas","start_date"),
    Input("fechas","end_date")]
)

#definicion de la funcion

def display_value(selected_commodity, frecuencia, start_date, end_date):
    
    
    df2=commodities_melt[(commodities_melt["Commodity"].isin(selected_commodity)) & 
                         (commodities_melt["Fecha"].dt.date>=(datetime.datetime.strptime(start_date, '%Y-%m-%d').date() )) &
                        (commodities_melt["Fecha"].dt.date<=(datetime.datetime.strptime(end_date, '%Y-%m-%d').date() ))]
    if frecuencia=="Mensual":
        fig=px.line(df2.groupby(['Mes', 'Commodity']).mean().reset_index(),x="Mes",markers=True,y="Precio ($)", color="Commodity",height=800)
    else: fig= px.line(df2,color="Commodity",x="Fecha",markers=True,y="Precio ($)",height=800)
    
    fig.update_layout(legend_title="", legend= dict(
    orientation="h", y=-.2
        ))

    #tabla
    return fig


#setear server y correr
app.run_server(debug=False,port=10000, host="0.0.0.0")
    
