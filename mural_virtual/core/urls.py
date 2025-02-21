from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    
    # ==== CADASTRA ====
    path('cadastra/', cadastra, name='cadastra'),
    
    # ==== LOGIN ====
    path('login/', user_login, name='login'),

    # ==== LOGOUT ====
    path('logout/', user_logout, name='logout'),

    # ==== NOTAS ====
    path('criar_nota/', criar_nota, name='criar_nota'),
    path('editar/<int:nota_id>/', editar_nota, name='criar_nota'),
    path('excluir/<int:nota_id>/', excluir_nota, name='excluir_nota'),
]
