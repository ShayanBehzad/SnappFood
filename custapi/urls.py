from django.db import router

from custapi.serializers import CategorySerializer
from . import views
from django.urls import path, include
from rest_framework import routers



router = routers.DefaultRouter()
# router.register(r'users', views.CustomerList, basename='users')
router.register(r'customers/addresses', views.AddressView, basename='address')
# router.register(r'restaurants/<int:pk>/comments', views.CommentView, basename='comments')


urlpatterns = [
    path('', include(router.urls)),
    path('customers/', views.CustomerListCreateView.as_view({'get':'list'}), name='customer-list-'),
    path('customers/add', views.CustomerListCreateView.as_view({'post':'create'}), name='customer-create'),
    path('customers/<int:pk>/', views.CustomerRetrieveUpdateDestroyView.as_view(), name='customer-retrieve-update-destroy'),
    path('carts/', views.CartView.as_view({'get': 'list'}), name='carts'),
    path('carts/create/', views.CartCreateView.as_view({'post': 'create'}), name='create_carts'),
    path('carts/<int:pk>/', views.CartView.as_view({'get': 'retrieve'}), name='cart_retrieve'),
    path('carts/<int:pk>/add/', views.CartView.as_view({'post': 'add'}), name='cart_add'),
    path('carts/<int:pk>/pay/', views.Payment.as_view({'post': 'pay'}), name='cart_pay'),
    path('restaurantview/', views.RestaurantSpView.as_view({'get': 'list'}), name='restaurant_list'),
    path('restaurantview/<int:pk>/', views.RestaurantSpView.as_view({'get': 'retrieve'}), name='restaurant_retrieve'),
    path('restaurantview/<int:pk>/foods', views.FoodsView.as_view({'get': 'list'}), name='restaurant_food'),
    path('restaurantview/<int:pk>/comments/', views.CommentView.as_view({'get':'list'}), name='get_comments'),
    path('restaurantview/<int:pk>/comments/add', views.CommentView.as_view({'post':'create'}), name='post_comments'),
    # path('restaurantview/<int:pk>/comments/', views.CommentCreateView.as_view(), name='create_comments'),

    # path('restaurants/<int:pk>', views.RestaurantInd.as_view(), name='restaurant_list')

    # path('address/<int:pk>/', views.AddressRetrieveUpdateDestroyView.as_view(), name='address-retrieve-update-destroy')

    # path('', views.home, name='home'),
    # path('cat_<int:id>', views.choose, name='choose'),
    # path('<int:id>/<slug:slug>/', views.categories, name='product_detail'),
]
