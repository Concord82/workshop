from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, WorkStationReg
from .models import Offices, WorkStation
# Create your views here.


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )

        if user is not None:
            if user.is_active:
                login(request, user)

                #return HttpResponse('Authenticated successfully')
                return redirect('dashboard')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form':form})


@login_required
def set_office(request, office_id=0):
    ''' Установка офиса для работы со справочниками'''
    if office_id != 0:
        request.session['current_office'] = office_id
    return redirect(request.META.get('HTTP_REFERER', '/'))


def office_list(request):
    offices_list = Offices.objects.all()
    return render(
        request,
        'offices_list.html',
        {'offices_list': offices_list}
    )


def user_station_reg(request):
    current_office = Offices.objects.get(pk=request.session.get('current_office'))
    if request.method == 'POST':
        form = WorkStationReg(request.POST)
        if form.is_valid():
            work_Station = WorkStation.objects.create(
                host = form.cleaned_data['host'],
                ip_address=form.cleaned_data['ip_addres'],
                office=current_office
            )
            work_Station.save()
            return redirect("dashboard")
    else:
        try:
            work_station = WorkStation.objects.get(
                host=request.META.get('REMOTE_HOST'),
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return render(request, 'work_station_reg.html',{'work_station': work_station, 'office': current_office})

        except work_station.DoesNotExist:
            data = {
                'host': request.META.get('REMOTE_HOST'),
                'ip_addres': request.META.get('REMOTE_ADDR')
            }
            form = WorkStationReg(data)
            return render(request, 'work_station_reg.html', {'form': form, 'office': current_office})





@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'section': 'dashboard'})
