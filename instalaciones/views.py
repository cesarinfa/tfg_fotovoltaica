from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from usuarios.models import UserData
from .models import Instalacion, Valores_Actuales
from .forms import InstalacionForm, HistoricoForm
from alarmas.models import Alarmas
from .open_meteo import open_meteo, open_meteo_energia
from .grafica import graficas, graficas_rango, graficas_historico
from datetime import datetime, timedelta
import folium


# Vista para listado de instalaciones
@login_required
def instalaciones(request):

    #Configuración del punto de inicio del mapa inicial
    mapaInicial = folium.Map(location=[40.016906,-3.7060583], zoom_start=6,zoom_control=True)
    mapaInicial.save('instalaciones.html')

    # Obtener los marcadores de las instalaciones y los valores actuales y de predicción
    marcadores = request.user.instalaciones.all()
    for mc in marcadores:
        setattr(mc,'valores',Valores_Actuales.objects.filter(instalacion__id=mc.id))
        setattr(mc,'prediccion',open_meteo_energia(request,get_object_or_404(Instalacion, pk=mc.id),1))


    listado_alarmas = []

    # Por cada marcador, obtiene las coordenadas y añade el marcador y obtiene las alarmas
    for marcador in marcadores:
        coordenadas = (marcador.latitud, marcador.longitud)
        folium.Marker(coordenadas, popup=marcador.nombre).add_to(mapaInicial)

        num_alarmas = {'id': marcador.id, 'count': Alarmas.objects.filter(instalacion_id=marcador.id,estado='ACTIVA').count()}
        listado_alarmas.append(num_alarmas)


    userData = UserData.objects.filter(user_id=request.user.id)

    return render(request, 'instalaciones.html',
                  {'usuario': userData[0], 'marcadores': marcadores, 'mapa': mapaInicial._repr_html_(), 'alarmas':listado_alarmas})


# Vista para nueva instalación
@login_required
def nueva_instalacion(request):
    if request.method == 'GET':
        return render(request, 'nueva_instalacion.html', {'form': InstalacionForm})

    else:

        # Método post
        form = InstalacionForm(request.POST)

        if form.is_valid():

            # Guardar la información de la instalación

            insta = Instalacion()
            insta.user = request.user
            insta.nombre = request.POST['nombre']
            insta.direccion = request.POST['direccion']
            insta.cp = request.POST['cp']
            insta.poblacion = request.POST['poblacion']
            insta.provincia = request.POST['provincia']
            insta.latitud = request.POST['latitud']
            insta.longitud = request.POST['longitud']
            insta.fecha_inst = request.POST['fecha_inst']
            insta.modelo_inv = request.POST['modelo_inst']
            insta.fabricante_inv = request.POST['fabricante_inst']
            insta.nserie_inv = request.POST['nserie_inst']

            insta.save()

            return redirect('/instalaciones/insta')
        else:
            return render(request, 'nueva_instalacion.html', {'form': InstalacionForm,
                                                              'error': form.errors})

# Vista para información de instalación
def info_instalacion(request, insta_id):

    insta = get_object_or_404(Instalacion, pk=insta_id)

    valores = get_object_or_404(Valores_Actuales, instalacion=insta_id)

    instalaciones = Instalacion.objects.get(id=insta_id)

    listado_alarmas = instalaciones.alarmas_set.filter(estado='ACTIVA').order_by('-fecha')

    num_alarmas = listado_alarmas.count()

    if request.method == 'GET':

        # Método get, mostrar gráficas
        graf=graficas(insta)

        return render(request, 'info_consumos.html', {'insta': insta, 'valores':valores,
                                    'num_alarmas':num_alarmas, 'alarmas':listado_alarmas,'graficas':graf, 'form': HistoricoForm,'tipo': "GET"})

    elif request.method == 'POST':

        # Método post
        form = HistoricoForm(request.POST)

        if form.is_valid():

            # Comprobar campos desde y hasta de fechas

            if ( int(request.POST['desde_month']) <10):
                mes_d = "0" + request.POST['desde_month']
            else:
                mes_d = request.POST['desde_month']

            if ( int(request.POST['desde_day']) <10):
                dia_d = "0" + request.POST['desde_day']
            else:
                dia_d = request.POST['desde_day']

            if ( int(request.POST['hasta_month']) <10):
                mes_h = "0" + request.POST['hasta_month']
            else:
                mes_h = request.POST['hasta_month']

            if ( int(request.POST['hasta_day']) <10):
                dia_h = "0" + request.POST['hasta_day']
            else:
                dia_h = request.POST['hasta_day']

            date1 = request.POST['desde_year'] + "-" + mes_d + "-" + dia_d
            date2 = request.POST['hasta_year'] + "-" + mes_h + "-" + dia_h

            # Al buscar, obtiene los datos y los muestra
            if 'buscar' in request.POST:
                graf = graficas_rango(insta,date1,date2)

                initial_data = {'desde': date1, 'hasta': date2}
                historicoForm = HistoricoForm(initial=initial_data)

                return render(request, 'info_consumos.html', {'insta': insta, 'valores': valores,
                                                              'num_alarmas': num_alarmas, 'alarmas': listado_alarmas,
                                                              'graficas': graf, 'form': historicoForm, 'tipo': "POST"})
            else:
                # Al descagar, obtiene los históricos
                graf = graficas_historico(insta,date1,date2)

                # Crear el archivo .csv con los datos y descargarlo
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="historicos.csv"'

                graf.to_csv(path_or_buf=response)

                return response


# Vista para previsión meteorológic
def prev_meteoro(request, insta_id):
    if request.method == 'GET':
        insta = get_object_or_404(Instalacion, pk=insta_id)

        json_response = open_meteo(request, insta)

        lista = {}
        now = datetime.now()
        for element in range(1,5):
            now = now + timedelta(days=1)
            text_date = now.strftime("%d-%b")
            lista[element]=text_date

        return render(request, 'prev_meteorologica.html', {'insta': insta, 'json':json_response, 'fecha':lista})


# Vista para predicción de energía
def prev_energia(request, insta_id):
    if request.method == 'GET':
        insta = get_object_or_404(Instalacion, pk=insta_id)

        json_response = open_meteo_energia(request, insta,4)

        return render(request, 'pred_energia.html', {'insta': insta, 'json':json_response})
