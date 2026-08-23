from django.urls import path
from . import views

urlpatterns = [
    path('api/articulos/', views.lista_articulos, name='lista_articulos'),
    path('api/movimientos/', views.registrar_movimiento, name='registrar_movimiento'),
]