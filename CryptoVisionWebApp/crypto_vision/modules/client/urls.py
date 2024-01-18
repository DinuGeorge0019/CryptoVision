
from django.urls import path

from . import views

urlpatterns = [
    path('client_index', views.client_index, name='client_index'),
    path('logout', views.logout_view, name='logout'),
    path('save_user_data', views.save_user_data_view, name='save_user_data'),
    path('password_confirmation', views.password_confirmation_view, name='password_confirmation'),
    path('change_user_password', views.change_user_password_view, name='change_user_password'),
    path('change_profile_picture', views.change_profile_picture_view, name='change_profile_picture'),
]
