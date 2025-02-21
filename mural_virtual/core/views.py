from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import UsuarioCreationForm, NotaForm
from .models import Usuario, Nota
from django.contrib import messages




def index(request):
    notas = Nota.objects.all().order_by('-data_publicacao')  # Exibe todas as notas, mais recentes primeiro
    return render(request, 'index.html', {'notas': notas})



'''

============= CADASTRA =============

'''
def cadastra(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        print("Dados recebidos:", request.POST)  # Debug
        if form.is_valid():
            print("Formulário válido!")  # Debug
            user = form.save()
            login(request, user)
            messages.success(request, f'Conta criada com sucesso para {user.username}!')
            return redirect('index')
        else:
            print("Erros do formulário:", form.errors)  # Debug
    else:
        form = UsuarioCreationForm()

    return render(request, 'usuarios/cadastra.html', {'form': form})

'''

============= LOGIN =============

'''

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '').strip()
        
        user = Usuario.objects.filter(email=email).first()  # Buscar usuário pelo email
        if user:
            user = authenticate(request, username=user.email, password=senha)  # Autenticar com email
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Bem-vindo!')
            return redirect('index')
        else:
            messages.error(request, 'Credenciais inválidas.')
            return render(request, 'usuarios/login.html')

    return render(request, 'usuarios/login.html')

'''

============= LOGOUT =============

'''
def user_logout(request):
    logout(request)
    return redirect('login')


'''

============= NOTAS =============

'''

def criar_nota(request):
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.usuario = request.user  # Associa a nota ao usuário logado
            nota.save()
            messages.success(request, 'Nota criada com sucesso!')
            return redirect('index')  # Redireciona após salvar
        else:
            messages.error(request, 'Erro ao criar a nota. Verifique os campos.')
    else:
        form = NotaForm()

    return render(request, 'usuarios/criar_nota.html', {'form': form})

'''

============= NOTAS EDITAR =============

'''
def editar_nota(request, nota_id=None):
    # Se houver um ID, edita a nota. Caso contrário, cria nova.
    nota = get_object_or_404(Nota, pk=nota_id) if nota_id else None
    form = NotaForm(request.POST or None, instance=nota)

    if form.is_valid():
        nova_nota = form.save(commit=False)
        if not nota:  # Se for criação, define o usuário
            nova_nota.usuario = request.user
        nova_nota.save()
        return redirect('index')  # Redirecione para a lista de notas

    return render(request, 'usuarios/criar_nota.html', {'form': form})

'''

============= NOTAS EXCLUIR =============

'''
def excluir_nota(request, nota_id):
    nota = get_object_or_404(Nota, pk=nota_id)

    # Permite exclusão apenas para autor ou admin
    if request.user == nota.usuario or request.user.is_superuser:
        nota.delete()
    
    return redirect('index')