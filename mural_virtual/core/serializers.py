from rest_framework import serializers
from .models import Usuario, Nota

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class NotaSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)  # Exibe informações do usuário na resposta

    class Meta:
        model = Nota
        fields = ['id', 'titulo', 'conteudo', 'data_publicacao', 'usuario']
