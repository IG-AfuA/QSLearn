from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='user_logout'),


    path('selfstudy/<str:pool>', views.selfstudy_start, name='selfstudy_start'),
    path('selfstudy/<str:pool>/questions/<int:category>', views.selfstudy_run, name='selfstudy_run'),
    path('selfstudy/<str:pool>/questions/<int:category>/<int:subcategory>', views.selfstudy_run, name='selfstudy_run'),
    path('selfstudy/<str:pool>/questions_until/<int:category>', views.selfstudy_run, name='selfstudy_run_until'),

    path('selfstudy/<str:pool>/questions/<int:category>/card', views.selfstudy_card, name='selfstudy_card'),
    path('selfstudy/<str:pool>/questions/<int:category>/<int:subcategory>/card', views.selfstudy_card, name='selfstudy_card'),
    path('selfstudy/<str:pool>/questions_until/<int:category>/card', views.selfstudy_card, {'until':True}, name='selfstudy_card_until'),

    path('selfstudy/<str:pool>/questions/<int:category>/progress', views.selfstudy_progress, name='selfstudy_progress'),
    path('selfstudy/<str:pool>/questions/<int:category>/<int:subcategory>/progress', views.selfstudy_progress, name='selfstudy_progress'),
    path('selfstudy/<str:pool>/questions_until/<int:category>/progress', views.selfstudy_progress, {'until':True}, name='selfstudy_progress_until'),
    path('selfstudy/<str:pool>/questions/<int:category>/progress_inline', views.selfstudy_progress, {'inline':True}, name='selfstudy_progress_inline'),
    path('selfstudy/<str:pool>/questions/<int:category>/<int:subcategory>/progress_inline', views.selfstudy_progress, {'inline':True}, name='selfstudy_progress_inline'),
    ]
