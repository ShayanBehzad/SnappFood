from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import *
from django.contrib.auth import login
from django.http import Http404
from register.models import User
from .tasks import send_notification_mail
from django.core.mail import send_mail



# Create your views here.





@csrf_exempt
def register(request):
    if request.method == 'GET':
        forms = Registerform
        return render(request, 'registration/register.html', {'form': forms})
    
    if request.method == 'POST':
        forms = Registerform(request.POST)

        if forms.is_valid():
            # save the info
            mail = forms.cleaned_data['email']
            print(mail)
            name = forms.cleaned_data['username']
            send_notification_mail.delay(mail, 'Dear %s Welcome To SnappFood' %name)
            # send_mail(    
            #     "Welcome on Board!",
            #     'Dear %s Welcome To SnappFood' %name,
            #     "shayan.behzad1380@example.com",
            #     ["shohreparsa8@gmail.com"],
            #     auth_password='sqdvodckgmtbfsgd',
            #     fail_silently=False,
            #     )
            user = forms.save(commit=False)
            user.username = user.username.lower()
            user.role = User.SELLER
            user.save()
            messages.success(request, 'You successfuly registerd.')
            login(request, user)
            print(user.id)
            request.session['id'] = user.id
            return redirect('restaurantpage')

        else:
            print(forms.errors)
            raise Http404 


@csrf_exempt
def restregister(request):
    user_id = request.session.get('id')
    user = User.objects.get(id=user_id)
    print('user is: ',user)
    forms = RestRegisterForm
    if request.method == 'GET':
        return render(request, 'registration/restaurantform.html', {'form':forms})

    if request.method == 'POST':
        forms = RestRegisterForm(request.POST)
        if forms.is_valid():
            restaurant = forms.save(commit=False)
            restaurant.seller = user
            restaurant.name = restaurant.name.lower()
            restaurant.save()
            messages.success(request, 'Your Restaurant Successfuly Registerd')
            return redirect('restaddress')

    return render(request, 'registration/restaurantform.html', {'form':forms})

@csrf_exempt
def restaddressregister(request):
    user_id = request.session.get('id')
    user = User.objects.get(id=user_id)
    print('user is: ',user)
    restaurant = Restaurant.objects.get(seller=user)

    forms = RestAddressRegisterForm
    if request.method == 'GET':
        return render(request, 'registration/restaurantaddressform.html', {'form':forms})
    elif request.method == 'POST':
        forms = RestAddressRegisterForm(request.POST)
        if forms.is_valid():
            address = forms.save(commit=False)
            address.restaurant = restaurant
            address.save()
            messages.success(request, 'Your Restaurant Address Successfuly Registerd')
            return redirect('/restaurant')
    return render(request, 'registration/restaurantaddressform.html', {'form':forms})




    
# Another way to transfer the user from the register page to the restaurant information page is to transfer the information with a URL, which is not a secure solution for the user's information.