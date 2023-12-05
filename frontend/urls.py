# https://medium.com/analytics-vidhya/django-react-integration-37acc304e984
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name="frontend_index"),
    path('login', views.f_login, name='frontend_login'),
    path('home', views.dashbord, name='frontend_dashboard'),

    path('user', views.user, name='frontend_user'),
    path('function', views.function, name='frontend_function'),
    path('categorie', views.categorie, name='frontend_categorie'),
    path('article', views.article, name='frontend_article'),
    path('stockageaera', views.stockageaera, name='frontend_stockagearea'),
    path('career', views.career, name='frontend_career'),
    path('stockageaeralv',
         views.stockageaeralv, name='frontend_stockagearealv'),
    path('careerlv', views.careerlv, name='frontend_careerlv'),
    path('careerarticle', views.careerarticle, name='frontend_careerarticle'),
    re_path(r'^api', views.api, name='api'),
]
