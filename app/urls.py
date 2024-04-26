from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='user_logout'),

    path('selfstudy/<str:pool>', views.selfstudy_start, name='selfstudy_start'),
    path('selfstudy/<str:pool>/questions/<int:category>', views.selfstudy_run, name='selfstudy_run'),
    path('selfstudy/<str:pool>/questions/<int:category>/<int:subcategory>/', views.selfstudy_run, name='selfstudy_run'),
    path('selfstudy/<str:pool>/questions_until/<int:category>', views.selfstudy_run, name='selfstudy_run_until'),


    ]
