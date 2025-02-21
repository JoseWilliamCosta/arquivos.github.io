from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Nota

class UsuarioCreationForm(UserCreationForm):
    tipo_usuario = forms.ChoiceField(choices=[('aluno', 'Aluno'), ('professor', 'Professor'), ('admin', 'Administrador')])
    matricula = forms.CharField(label="Matrícula", max_length=50)
    email = forms.EmailField(label="Email")
    curso = forms.CharField(label="Curso (Opcional)", max_length=100, required=False)

    # O campo 'username' será usado no lugar de 'nome'
    username = forms.CharField(label="Nome de Usuário", max_length=100)

    class Meta:
        model = Usuario
        fields = ['username', 'tipo_usuario', 'matricula', 'email', 'password1', 'password2', 'curso']


class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['titulo', 'descricao', 'categoria']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Categoria (opcional)'}),
        }