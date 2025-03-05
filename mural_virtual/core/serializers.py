from rest_framework import serializers
from .models import Usuario, Nota

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'tipo_usuario', 'matricula', 'curso']
class NotaSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()  # Exibe o nome do usuário em vez do ID

    class Meta:
        model = Nota
        fields = ['id', 'usuario', 'titulo', 'descricao', 'data_publicacao', 'categoria', 'imagem', 'arquivo']
