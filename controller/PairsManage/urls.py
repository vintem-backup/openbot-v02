from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.pairs_list, name='listofpairs'),
    path('new/', views.pair_new, name='newpair'),
    path('update/<str:id>/', views.pair_update, name='updatepair'),
    
]