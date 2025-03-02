from django.urls import path
from .views import *


urlpatterns = [
    path('notas/', index_api, name='index_api'),
    path('cadastrar/', cadastra_api, name='cadastra_api'),
    path('login/', user_login_api, name='user_login_api'),
    path('logout/', user_logout_api, name='user_logout_api'),
    path('notas/criar/', criar_nota_api, name='criar_nota_api'),
    path('notas/editar/<int:nota_id>/', editar_nota_api, name='editar_nota_api'),
    path('notas/excluir/<int:nota_id>/', excluir_nota_api, name='excluir_nota_api'),
]
