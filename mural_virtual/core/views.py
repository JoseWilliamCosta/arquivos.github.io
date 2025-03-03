from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import UsuarioCreationForm, NotaForm, UsuarioUpdateForm
from .models import Usuario, Nota
from django.contrib import messages
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UsuarioSerializer, NotaSerializer
from django.contrib.auth.decorators import login_required


'''

============= api =============

'''
@api_view(['GET'])
def index_api(request):
    notas = Nota.objects.all().order_by('-data_publicacao')
    serializer = NotaSerializer(notas, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def cadastra_api(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        return Response({'message': f'Conta criada com sucesso para {user.username}!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login_api(request):
    email = request.data.get('email', '').strip()
    senha = request.data.get('senha', '').strip()
    user = Usuario.objects.filter(email=email).first()
    if user:
        user = authenticate(request, username=user.email, password=senha)
    
    if user is not None:
        login(request, user)
        return Response({'message': 'Bem-vindo!'}, status=status.HTTP_200_OK)
    return Response({'error': 'Credenciais inválidas.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout_api(request):
    logout(request)
    return Response({'message': 'Logout realizado com sucesso!'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_nota_api(request):
    serializer = NotaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(usuario=request.user)
        return Response({'message': 'Nota criada com sucesso!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editar_nota_api(request, nota_id):
    nota = get_object_or_404(Nota, pk=nota_id, usuario=request.user)
    serializer = NotaSerializer(nota, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Nota editada com sucesso!'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def excluir_nota_api(request, nota_id):
    nota = get_object_or_404(Nota, pk=nota_id)
    if request.user == nota.usuario or request.user.is_superuser:
        nota.delete()
        return Response({'message': 'Nota excluída com sucesso!'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Você não tem permissão para excluir esta nota.'}, status=status.HTTP_403_FORBIDDEN)









'''

============= Views normais =============

'''





def index(request):
    notas = Nota.objects.all().order_by('-data_publicacao')  # Exibe todas as notas, mais recentes primeiro
    return render(request, 'index.html', {'notas': notas})


'''
============= EDITAR USER ==============
'''
@login_required
def editar_perfil(request):
    user = request.user  # Obtém o usuário logado
    
    if request.method == "POST":
        form =UsuarioUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('perfil', usuario_id=user.id)  # Passando o usuario_id
    else:
        form = UsuarioUpdateForm(instance=user)  # Preenche com dados atuais

    return render(request, "usuarios/editar_perfil.html", {"form": form})

'''
============= TROCA SENHA ===============
'''



'''
============= PERFIL ==============
'''

def perfil(request, usuario_id):
    user = get_object_or_404(Usuario, id=usuario_id)  # Busca o usuário ou retorna 404
    notas = Nota.objects.filter(usuario=user)  # Filtra as notas do usuário
    return render(request, 'usuarios/perfil.html', {'user': user, 'notas': notas})

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
    return redirect('index')


'''

============= NOTAS =============

'''

def criar_nota(request):
    if request.method == 'POST':
        form = NotaForm(request.POST, request.FILES)
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

    if request.method == 'POST':
        form = NotaForm(request.POST, request.FILES if request.FILES else None, instance=nota)
        if form.is_valid():
            nova_nota = form.save(commit=False)
            if not nota:  # Se for criação, define o usuário
                nova_nota.usuario = request.user
            nova_nota.save()
            return redirect('index')  # Redirecione para a lista de notas
    else:
        form = NotaForm(instance=nota)

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