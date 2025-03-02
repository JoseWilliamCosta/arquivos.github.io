from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    TIPOS_USUARIO = [
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
        ('admin', 'Administrador'),
    ]
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO)
    matricula = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    curso = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'  # Define o email como campo de login
    REQUIRED_FIELDS = ['username', 'tipo_usuario', 'matricula']

    def __str__(self):
        return self.username  # Usando 'username' no lugar de 'nome'


class Nota(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notas')
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    imagem = models.ImageField(upload_to='imagens_notas/', blank=True, null=True)
    arquivo = models.FileField(upload_to='arquivos_notas/', blank=True, null=True)

    def __str__(self):
        return self.titulo

