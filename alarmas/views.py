from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Alarmas
from usuarios.models import UserData,UsuarioxInst
from instalaciones.models import Instalacion
from .filters import AlarmasFilter


# Vista para alarmas
@login_required()
def alarmas(request):

    userDatas = UserData.objects.filter(user_id=request.user.id)

    num = 0

    for uD in userDatas:
        if uD.instalador == 0:

            # Instalaciones de usuario instalador
            instalaciones = Instalacion.objects.filter(user_id=request.user.id)
            num = instalaciones.count()
        else:

            # Instalaciones de usuario propietario
            usuarioxinst =UsuarioxInst.objects.filter(user_id=request.user.id)

            if (usuarioxinst.count()==0):
                num=0
            else:
                instalaciones = Instalacion.objects.filter(id=UsuarioxInst.objects.filter(user_id=request.user.id))
                num = instalaciones.count()


    if (num != 0):

        # Ninguna instalación del usuario

        listado_alarmas = Alarmas.objects.filter(instalacion_id__in=instalaciones)

        myFilter = AlarmasFilter(request.GET, queryset=listado_alarmas,request=request)

        listado_alarmas = myFilter.qs


        return render(request, 'alarmas.html', {'total': num, 'listado_alarmas': listado_alarmas, 'myFilter': myFilter})

    else:
        return render(request, 'alarmas.html',{'total':num})

