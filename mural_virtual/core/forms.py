from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Usuario, Nota


# edita dados do usuario
class UsuarioUpdateForm(forms.ModelForm):
    username = forms.CharField(label="NOVO Nome de Usuário", max_length=100)
    tipo_usuario = forms.ChoiceField(choices=[('aluno', 'Aluno'), ('professor', 'Professor'),])
    curso = forms.CharField(label="Curso (Opcional)", max_length=100, required=False)

    class Meta:
        model = Usuario
        fields = ['username', 'tipo_usuario', 'curso']
        



class UsuarioCreationForm(UserCreationForm):
    tipo_usuario = forms.ChoiceField(choices=[('aluno', 'Aluno'), ('professor', 'Professor'),])
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
        fields = ['titulo', 'descricao', 'categoria', 'imagem', 'arquivo']

    def __init__(self, *args, **kwargs):
        super(NotaForm, self).__init__(*args, **kwargs)
        self.fields['imagem'].required = False
        self.fields['arquivo'].required = False