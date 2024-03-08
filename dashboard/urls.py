from . import views
from django.urls import path , reverse
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='dashboardhome'),
    path('reports', views.report, name='reports'),    
    path('<int:sub>', views.updade_form, name='update'),
    path('foodlist/', views.food, name='foodlist'),
    path('dashboard/settings', views.settings, name='settings'),
    path('dashboard/settings/schedule', views.schedule_setting, name='schedule_setting'),
    path('dashboard/settings/address', views.address_setting, name='address_setting'),
    path('foodlist/foodform/', views.foodform, name='foodform'),
    path('foodlist/editform/<int:food_id>', views.editfoodform, name='foodeditform'),

] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)