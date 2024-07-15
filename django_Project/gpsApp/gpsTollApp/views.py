from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from geopy.geocoders import Nominatim
from pathlib import Path
import os
import simpy
from geopy.distance import geodesic
import mysql.connector as sql
import folium
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import LoginForm,UserForm,VehicleCategoryForm
from django.db import connection
from .models import userprofile, gpstollapptrip, vehiclecategory
from django.urls import reverse
from .forms import ChangePasswordForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
import calendar 
from gpsTollApp.models import models
from datetime import date
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
firstname=''
lastname=''
sex=''
emailid=''
password=''


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated!')
            update_session_auth_hash(request, user)  # Important to update session
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def items_view(request):
    items = vehiclecategory.objects.all()
    print('items==',items)
    return render(request, 'items.html', {'items': items})

def deleteUser(request):
    if request.method == 'POST':

        form = UserForm(request.POST)
        id = form.cleaned_data['userid']
        password = form.cleaned_data['password']

    return render(request, 'user.html')

def EditUser(request):
    if request.method == 'POST':

        form = userprofile(request.POST)
        userid = form.cleaned_data['userid']
        password = form.cleaned_data['password']

    return render(request, 'register.html')

def editPass(request):
    print('editPass')
    return render(request, 'edit_pass_vehicle.html')

def deletePass(request):
    return render(request, 'pass_vehicle.html')


def login_action(request):
    row=""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #user = authenticate(firstname=username, password=password)
            #print("user==",user)
            with connection.cursor() as cursor:
                query = """
                SELECT * FROM gpstollapp_userprofile
                WHERE first_name = %s AND password = %s
                """
                cursor.execute(query, [username, password])
                row = cursor.fetchall()
               
                result_count = len(row)
                                        
            # Print SQL queries
            for query in connection.queries:
                print("query=====",result_count)
            
            if len(row) != 0:
                print("query==12ss3===",row.index)   
            
                user = get_object_or_404(userprofile, first_name=username)
                print("user.first_name=====",user.super_user)
                
                request.session['username'] = user.first_name
                #request.session['LoginTime'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
                #print("time===",userdetails.login_time)

                applicant_name = request.session['username']  # Replace with your desired applicant name
                print('applicant_name', applicant_name)
                aggregate_data = gpstollapptrip.objects.filter(Applicant_name=applicant_name).aggregate(
                    num_trips=Count('trip_id'),
                    total_amount=Sum('total_amount'),
                    total_tolls_crossed=Sum('no_tollscrossed'),
                    total_distance=Sum('distance')
                )    

                trip_stats = (
                    gpstollapptrip.objects.annotate(month=models.functions.ExtractMonth('trip_date'))
                    .values('month')
                    .annotate(trip_count=Count('trip_id'))
                    .order_by('month')        
                )

                labels = []
                data = []

                for stat in trip_stats:
                    labels.append(calendar.month_name[stat['month']])
                    data.append(stat['trip_count'])

                current_month = date.today().month
                current_year = date.today().year
                
                trips = gpstollapptrip.objects.filter(
                    Applicant_name=applicant_name,
                    trip_date__year=current_year,
                    trip_date__month=current_month
                )
                
                userdetails = {
                    'username': user.first_name,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'super_user':user.super_user,
                    'login_time':timezone.now(),
                    'trips':trips,
                    'labels': labels,
                    'data': data,
                    'aggregate_data':aggregate_data
                    # Add more fields as needed
                }
                
                print('aggregate_data====',userdetails)

                return render(request,'success.html', {'userdetails': userdetails})
            else:
                messages.error(request, 'Invalid username or password')
        else:
            print(form.errors)
            messages.error(request,form.errors)
            
    else:
        form = LoginForm()
    return render(request, 'login.html', {'row': row})

def new_func(row):
    return row
    
def user_list(request):
    receipts = userprofile.objects.all()
    return render(request, 'user.html', {'receipts': receipts})

def register_action(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Ensure this URL pattern exists
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def success_page(request):
    return render(request, 'success.html')

def home(request):
    result=os.path.join(BASE_DIR,"templates")   
    request.session['username']=""
    '''return render(request,'home.html')'''
    return render(request,"home.html")

def login(request):
    print("result====",BASE_DIR)
    return render(request,"login.html")

def admin(request):
    return render(request,"admin.html")

def register(request):
    return render(request,"register.html")

def top_frame(request):
    return render(request, 'top_frame.html')

def choose(request):
    return render(request,"choose.html")

def Simulate(request):
    items = vehiclecategory.objects.all()
    applicant_name = request.session['username']  # Replace with your desired applicant name
    print('applicant_name', applicant_name)
    # Perform join query using Django ORM
    gpstolltripdetails = gpstollapptrip.objects.filter(Applicant_name=applicant_name)
    print("user.first_name=====",items)
    
    print('gpstolltripdetails==',gpstolltripdetails)
    result = {
        'VehicleCategory':items,
        'gpstolltripdetails': gpstolltripdetails
    }
    return render(request,"simulate.html", {'result' : result})

def main_view(request):
    return render(request, 'base.html')

def viewhistory(request):
    return render(request, 'viewhistory.html')

def dashboard(request):
    applicant_name = request.session['username']  # Replace with your desired applicant name
    print('applicant_name', applicant_name)
    aggregate_data = gpstollapptrip.objects.filter(Applicant_name=applicant_name).aggregate(
        num_trips=Count('trip_id'),
        total_amount=Sum('total_amount'),
        total_tolls_crossed=Sum('no_tollscrossed'),
        total_distance=Sum('distance')
    )    

    trip_stats = (
        gpstollapptrip.objects.annotate(month=models.functions.ExtractMonth('trip_date'))
        .values('month')
        .annotate(trip_count=Count('trip_id'))
        .order_by('month')        
    )

    labels = []
    data = []

    for stat in trip_stats:
        labels.append(calendar.month_name[stat['month']])
        data.append(stat['trip_count'])

    current_month = date.today().month
    current_year = date.today().year
    
    trips = gpstollapptrip.objects.filter(
        Applicant_name=applicant_name,
        trip_date__year=current_year,
        trip_date__month=current_month
    )

    context = {
        'trips':trips,
        'labels': labels,
        'data': data,
        'aggregate_data':aggregate_data
    }
    print('aggregate_data====',context)
    return render(request, 'dashboard.html', { 'context': context })

def chart_data(request):
    trip_stats = (
        gpstollapptrip.objects.annotate(month=models.functions.ExtractMonth('trip_date'))
        .values('month')
        .annotate(trip_count=Count('trip_id'))
        .order_by('month')        
    )

    labels = []
    data = []

    for stat in trip_stats:
        labels.append(calendar.month_name[stat['month']])
        data.append(stat['trip_count'])
    data = {
        'Labels': labels,
        'data': data
    }
    return JsonResponse(data)

def simulate_trip(request):
    return render(request, 'simulate_trip.html')

def paymentpg(request):
    return render(request, 'paymentpg.html')

def user(request):
    return render(request, 'user.html')

def vehicle_category(request):
    vehiclecategory = userprofile.objects.all()
    return render(request, 'vehicle_category.html', {'vehiclecategory': vehiclecategory})

def pass_vehicle(request):
    items = vehiclecategory.objects.all()
    print('items==',items)
    applicant_name = request.session['username']  # Replace with your desired applicant name
    print('applicant_name', applicant_name)
    # Perform join query using Django ORM
    gpstolltripdetails = gpstollapptrip.objects.filter(Applicant_name=applicant_name)
    print("user.first_name=====",items)
    
    print('gpstolltripdetails==',gpstolltripdetails)
    result = {
        'VehicleCategory':items,
        'gpstolltripdetails': gpstolltripdetails
    }
    return render(request, 'pass_vehicle.html',{'result':result})

def changepassword(request):
    if request.method == 'POST':
        applicant_name = request.session['username']  # Replace with your desired applicant name
        print('applicant_name', applicant_name)
        newpassword = form.cleaned_data['newPassword']
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("UPDATE gpstollapp_userprofile SET password = %s WHERE first_name = %s",  [newpassword,applicant_name])
                row_count = cursor.rowcount
            
            print("rowcount====", row_count)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('changepassword')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'changepassword.html', {'form': form})

def report_pass(request):
    applicant_name = request.session['username']  # Replace with your desired applicant name
    print('applicant_name', applicant_name)
    # Perform join query using Django ORM
    gpstolltripdetails = gpstollapptrip.objects.filter(Applicant_name=applicant_name)
    result= {
        'gpstolltripdetails':gpstolltripdetails
    }
    return render(request, 'report_pass.html', { 'result':result })

def report_receipt(request):
    return render(request, 'report_receipt.html')



SPEED = 50  # km/h

def travel(env, vehicle, origin_coords, destination_coords, speed):
    total_distance = geodesic(origin_coords, destination_coords).km
    travel_time = total_distance / speed
    
    print(f"{env.now:.2f}: {vehicle} starting journey, total distance {total_distance:.2f} km, estimated travel time {travel_time:.2f} hours.")
    
    for i in range(1, int(travel_time) + 1):
        yield env.timeout(1)
        print(f"{env.now:.2f}: {vehicle} is traveling, {i}/{int(travel_time)} hours completed.")
    
    yield env.timeout(travel_time - int(travel_time))
    print(f"{env.now:.2f}: {vehicle} has arrived at destination.")

def run_simulation(origin_coords, destination_coords):
    env = simpy.Environment()
    print("origin_coords=",origin_coords)
    print("destination_coords=",destination_coords)
    env.process(travel(env, "Vehicle 1", origin_coords, destination_coords, SPEED))
    env.run()

def save_route_map(origin_coords, destination_coords):
    route_map = folium.Map(location=origin_coords, zoom_start=7)
    
    folium.Marker(origin_coords, popup="Origin", icon=folium.Icon(color='green')).add_to(route_map)
    folium.Marker(destination_coords, popup="Destination", icon=folium.Icon(color='red')).add_to(route_map)
    
    folium.PolyLine([origin_coords, destination_coords], color='blue', weight=2.5, opacity=1).add_to(route_map)
    
    route_map.save("templates/simulate/route_map.html")
    print("Route map saved as 'templates/simulate/route_map.html'.")


def simulate_vehicle(request):
    
    if request.method == 'POST':
        
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        print("SOURCE==",source)
        print("Destination==",destination)
        geolocator = Nominatim(user_agent="vehicle_simulation")
        source_location = geolocator.geocode(source)
        destination_location = geolocator.geocode(destination)
        print(source_location,destination_location)
        if not source_location or not destination_location:
            return HttpResponse("Invalid source or destination")

        origin_coords = (source_location.latitude, source_location.longitude)
        destination_coords = (destination_location.latitude, destination_location.longitude)
        print("origin_coords===",origin_coords)
        save_route_map(origin_coords, destination_coords)

        return redirect('display_map')



    return render(request, 'simulate/simulate_vehicle.html')

def display_map(request):
    return render(request, 'simulate/route_map.html')