
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from pkg_resources import require
from custapi.models import Address
from .models import *
from django.conf import settings
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
# from datetime import date
today = date.today()
# 'pending'
#'preparing'


# Create your views here.
@csrf_exempt
def home(request):
    res = Restaurant.objects.get(seller=request.user)
    state = State.objects.all()
    # if using sqlite, the state id starts from 1
    orders = Order.objects.filter(Q(restaurant=res) , (Q(state=1) | Q(state=2) | Q(state=3)))
    if request.method == 'GET':
        print(orders)
        address = Address.objects.all()
        
        print(address)
        context = {'orders':orders, 'address':address, 'state':state}

        return render(request, 'dashboard/home.html', context)
    




def updade_form(request, sub):
     if request.method == 'POST':
        choice = request.POST.get('choice')
        print(f'user id is:{sub}')
        print(f'choise is: {request.POST}')
        # if using sqlite, the state id starts from 1

        cus = Order.objects.get(id=sub)
        if int(choice) == 1:
            cus.state = State.objects.get(id=1)
        elif int(choice) == 2:
            cus.state = State.objects.get(id=2)
        elif int(choice) == 3:
            cus.state = State.objects.get(id=3)
        elif int(choice) == 4:
            cus.state = State.objects.get(id=4)
        cus.save()
        res = Restaurant.objects.get(seller=request.user)
        state = State.objects.all()
        orders = Order.objects.filter(Q(restaurant=res) , (Q(state=1) | Q(state=2) | Q(state=3)))
        context = {'orders':orders, 'state':state}

        return render(request, 'dashboard/home.html', context)




def food(request):
    # dir = settings.BASE_DIR
    if request.method == 'GET':
        res = Restaurant.objects.get(seller=request.user)
        foods = res.foods.all()
        return render(request, 'dashboard/foodtemp.html', {'foods':foods})



def foodform(request):
    if request.method == 'GET':
        forms = FoodForm
        return render(request, 'dashboard/foodform.html', {'form':forms})
    
    if request.method == 'POST':
        forms = FoodForm(request.POST, request.FILES)
        if forms.is_valid():
            food = forms.save(commit=False)
            food.name = food.name.lower()
            print(food)
            food.save()
            res = Restaurant.objects.get(seller=request.user)
            res.foods.add(food)
            messages.success(request, 'Your food successfuly added.')
            return redirect('foodlist')
        else:
            forms = FoodForm
            print('errors: ',forms.errors)
            return render(request, 'dashboard/foodform.html', {'form':forms})




def editfoodform(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    if request.method == 'GET':
        form = FoodForm(instance=food)
        return render(request, 'dashboard/editfood.html', {'form':form, 'food':food})
    elif request.method == 'POST':
        forms = FoodForm(request.POST, request.FILES, instance=food)
        if forms.is_valid():
            food = forms.save(commit=False)
            food.name = food.name.lower()
            food.save()
            res = Restaurant.objects.get(seller=request.user)
            res.foods.add(food)
            messages.success(request, 'Your food successfuly added.')
            return redirect('foodlist')
        else:
            forms = FoodForm
            print('errors: ',forms.errors)
            return render(request, 'dashboard/editfood.html', {'form':form, 'food':food})




def report(request):
    res = Restaurant.objects.get(seller=request.user)
    if request.method == 'POST':
        # get the chosen date
        start_date = request.POST['trip-start']
        end_date = request.POST['trip-stop']
        # if using sqlite, the state id starts from 1

        order = Order.objects.filter(Q(restaurant=res),(Q(state=4) & Q(created_at__range=(start_date, end_date))))
        num = 0  
        sum = 0
        for i in order:
            num += 1    
            sum += i.amount_paid
    else:
        # set the default data
        # if using sqlite, the state id starts from 1

        order = Order.objects.filter(restaurant=res, state=4)
        num = 0  
        sum = 0
        for i in order:
            num += 1    
            sum += i.amount_paid
        start_date = "2020-02-20"
        end_date = today.strftime("%Y-%m-%d")
    context = {'orders':order, 'num':num, 'income':sum, 'startdate':start_date, 'enddate':end_date}
    return render(request, 'dashboard/reports.html',context)




def settings(request):
    res = get_object_or_404(Restaurant, seller=request.user)
    address = get_object_or_404(RestaurantAddress, restaurant=res)
    schedule = get_object_or_404(Schedule, restaurant=res)

    if request.method == 'GET':
        form = RestSettings(instance=res)

    elif request.method == 'POST':
        form = RestSettings(request.POST, request.FILES, instance=res)
        if form.is_valid():
            res = form.save(commit=False)
            res.name = res.name.lower()
            form.save()
            messages.success(request, 'Your changes Successfuly registerd')
            return render(request, 'dashboard/settings.html', {'form':form})

        else:
            messages.success(request, form.errors)

    return render(request, 'dashboard/settings.html', {'form':form})

def schedule_setting(request):
    res = get_object_or_404(Restaurant, seller=request.user)
    address = get_object_or_404(RestaurantAddress, restaurant=res)
    schedule = get_object_or_404(Schedule, restaurant=res)
    # sunday =
    if request.method == 'GET':
        form = RestScheduleRegisterForm(instance=schedule)
        forms = WorkingHourForm()

    elif request.method == 'POST':
        form = RestScheduleRegisterForm(request.POST, request.FILES, instance=schedule)
        # sun_forms = WorkingHourForm(instance=)
        if form.is_valid():
            if forms.is_valid():
                res = form.save(commit=False)
                res.name = res.name.lower()
                form.save()
                messages.success(request, 'Your changes Successfuly registerd')
                return render(request, 'dashboard/setting_schedule.html', {'form':form, 'forms':forms})
            else:
                messages.success(request, forms.errors)

        else:
            messages.success(request, form.errors)

    return render(request, 'dashboard/setting_schedule.html', {'form':form, 'forms':forms})

def address_setting(request):

    res = get_object_or_404(Restaurant, seller=request.user)
    address = get_object_or_404(RestaurantAddress, restaurant=res)
    schedule = get_object_or_404(Schedule, restaurant=res)

    if request.method == 'GET':
        form = RestAddressRegisterForm(instance=address)

    elif request.method == 'POST':
        form = RestAddressRegisterForm(request.POST, request.FILES, instance=address)
        if form.is_valid():
            res = form.save(commit=False)
            res.name = res.name.lower()
            form.save()
            messages.success(request, 'Your changes Successfuly registerd')
            return render(request, 'dashboard/setting_address.html', {'form':form})

        else:
            messages.success(request, form.errors)

    return render(request, 'dashboard/setting_address.html', {'form':form})