from django.urls import path
from .views import *


urlpatterns = [
    path('notas/', index_api, name='notas'),
    path('cadastrar/', cadastra_api, name='cadastrar'),
    path('login/', user_login_api, name='login'),
    path('logout/', user_logout_api, name='logout'),
    path('notas/criar/', criar_nota_api, name='nota'),
    path('notas/editar/<int:nota_id>/', editar_nota_api, name='editar_nota'),
    path('notas/excluir/<int:nota_id>/', excluir_nota_api, name='excluir_nota'),
]
