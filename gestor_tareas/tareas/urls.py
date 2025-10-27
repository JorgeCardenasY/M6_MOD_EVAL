from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.iniciar_sesion, name='iniciar_sesion'),
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    path('tareas/', views.lista_tareas, name='lista_tareas'),
    path('tareas/crear/', views.crear_tarea, name='crear_tarea'),
    path('tareas/<int:tarea_id>/', views.tarea_detail, name='tarea_detail'),
    path('tareas/eliminar/<int:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('tareas/completar/<int:tarea_id>/', views.completar_tarea, name='completar_tarea'),
]
