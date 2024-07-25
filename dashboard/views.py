
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
from django.contrib.auth.decorators import login_required

# from datetime import date
today = date.today()
# 'pending'
#'preparing'


# Create your views here.
@login_required
def home(request):
    res = Restaurant.objects.get(seller=request.user)
    state = State.objects.all()
    # if using sqlite, the state id starts from 1
    orders = Order.objects.filter(Q(restaurant=res) , (Q(state=1) | Q(state=2) | Q(state=3)))
    address = Address.objects.all()
    context = {'orders':orders, 'address':address, 'state':state}
    return render(request, 'dashboard/home.html', context)
    



@login_required
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
        return redirect('dashboardhome')
        # return render(request, 'dashboard/home.html', context)


@login_required
def food(request):
    # dir = settings.BASE_DIR
    res = Restaurant.objects.get(seller=request.user)
    foods = res.foods.all()
    return render(request, 'dashboard/foodtemp.html', {'foods':foods})


@login_required
def foodform(request):
    
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
            messages.error(request, '%s' %forms.errors)
    forms = FoodForm
    return render(request, 'dashboard/foodform.html', {'form':forms})



@login_required
def editfoodform(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    forms = FoodForm(instance=food)

    if request.method == 'POST':
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
            messages.error(request, '%s' %forms.errors)
            # forms = FoodForm
            # print('errors: ',forms.errors)
            # return render(request, 'dashboard/editfood.html', {'form':form, 'food':food})
    return render(request, 'dashboard/editfood.html', {'form':forms, 'food':food})


@login_required
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



@login_required
def settings(request):
    res = get_object_or_404(Restaurant, seller=request.user)
    address = get_object_or_404(RestaurantAddress, restaurant=res)
    schedule = get_object_or_404(Schedule, restaurant=res)

    form = RestSettings(instance=res)

    if request.method == 'POST':
        form = RestSettings(request.POST, request.FILES, instance=res)
        if form.is_valid():
            res = form.save(commit=False)
            res.name = res.name.lower()
            form.save()
            messages.success(request, 'Your changes Successfuly registerd')
            return render(request, 'dashboard/settings.html', {'form':form})

        else:
            messages.error(request, '%s' %forms.errors)

    return render(request, 'dashboard/settings.html', {'form':form})


@login_required
def schedule_setting(request):
    res = get_object_or_404(Restaurant, seller=request.user)
    address = get_object_or_404(RestaurantAddress, restaurant=res)
    schedule = get_object_or_404(Schedule, restaurant=res)
    form = RestScheduleRegisterForm(instance=schedule)
    forms = WorkingHourForm()

    if request.method == 'POST':
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
                messages.error(request, '%s' %forms.errors)
        else:
            messages.error(request, '%s' %form.errors)

    return render(request, 'dashboard/setting_schedule.html', {'form':form, 'forms':forms})



@login_required
def address_setting(request):

    res = get_object_or_404(Restaurant, seller=request.user)
    address = get_object_or_404(RestaurantAddress, restaurant=res)
    schedule = get_object_or_404(Schedule, restaurant=res)
    form = RestAddressRegisterForm(instance=address)

    if request.method == 'POST':
        form = RestAddressRegisterForm(request.POST, request.FILES, instance=address)
        if form.is_valid():
            res = form.save(commit=False)
            res.name = res.name.lower()
            form.save()
            messages.success(request, 'Your changes Successfuly registerd')
            return render(request, 'dashboard/setting_address.html', {'form':form})

        else:
            messages.error(request, '%s' %form.errors)

    return render(request, 'dashboard/setting_address.html', {'form':form})