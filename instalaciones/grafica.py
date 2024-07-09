import sqlite3
import pandas as pd
from datetime import date

# Obtener históricos al cargar la página de consumos
def graficas(insta):
    connect = sqlite3.connect('db.sqlite3')
    pd.options.plotting.backend = "plotly"


    df = pd.read_sql_query("SELECT strftime(\'%H:%M\', hora) as hora,consumida,generada FROM instalaciones_historico_hora where instalacion_id="+str(insta.id)+" and hora like '"+str(date.today().year)+"-"+date.today().strftime('%m')+"-"+date.today().strftime('%d')+"%'", connect)

    df2 = pd.read_sql_query(
        "SELECT dia,consumida,generada FROM instalaciones_historico_dia where instalacion_id=" + str(
            insta.id) + " and dia>\"" + str(date.today().year) +"-" + date.today().strftime('%m') + "-01\"", connect)


    df3 = pd.read_sql_query("SELECT mes,year,consumida,generada FROM instalaciones_historico_mes where instalacion_id=" + str(
            insta.id) + " and year=" + str(date.today().year), connect)

    context = {
        "horas_horas": df.hora,
        "horas_consumidas": df.consumida,
        "horas_generadas": df.generada,
        "dias_dia": df2.dia,
        "dias_consumidas": df2.consumida,
        "dias_generadas": df2.generada,
        "meses_mes": df3.mes,
        "meses_year": df3.year,
        "meses_consumidas": df3.consumida,
        "meses_generadas": df3.generada
    }


    return (context)

# Obtener históricos al consultar por rango de fechas
def graficas_rango(insta, date1, date2):
    connect = sqlite3.connect('db.sqlite3')
    pd.options.plotting.backend = "plotly"


    df = pd.read_sql_query("SELECT strftime(\'%H:%M\', hora) as hora,consumida,generada FROM instalaciones_historico_hora where instalacion_id="+str(insta.id)+" and hora like '"+str(date.today().year)+"-"+date.today().strftime('%m')+"-"+date.today().strftime('%d')+"%'", connect)

    df2 = pd.read_sql_query(
        "SELECT dia,consumida,generada FROM instalaciones_historico_dia where instalacion_id=" + str(
            insta.id) + " and dia>\"" + str(date.today().year) + "-" + date.today().strftime('%m') + "-01\"", connect)

    df3 = pd.read_sql_query(
        "SELECT mes,year,consumida,generada FROM instalaciones_historico_mes where instalacion_id=" + str(
            insta.id) + " and year=" + str(date.today().year), connect)


    df4 = pd.read_sql_query("SELECT dia,consumida,generada FROM instalaciones_historico_dia where instalacion_id="
                            + str(insta.id) + " and dia>\"" + date1 +"\" and dia<\"" + date2 +"\" order by dia",connect)

    context = {
        "horas_horas": df.hora,
        "horas_consumidas": df.consumida,
        "horas_generadas": df.generada,
        "dias_dia": df2.dia,
        "dias_consumidas": df2.consumida,
        "dias_generadas": df2.generada,
        "meses_mes": df3.mes,
        "meses_year": df3.year,
        "meses_consumidas": df3.consumida,
        "meses_generadas": df3.generada,
        "rango_dia": df4.dia,
        "rango_consumidas": df4.consumida,
        "rango_generadas": df4.generada
    }


    return (context)

# Obtener históricos al descargar datos por rango de fechas
def graficas_historico(insta, date1, date2):
    connect = sqlite3.connect('db.sqlite3')
    pd.options.plotting.backend = "plotly"


    df = pd.read_sql_query("SELECT dia,consumida,generada FROM instalaciones_historico_dia where instalacion_id="
                            + str(insta.id) + " and dia>\"" + date1 +"\" and dia<\"" + date2 +"\" order by dia",connect)



    return df