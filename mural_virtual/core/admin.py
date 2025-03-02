from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Nota

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'tipo_usuario', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'matricula')
    list_filter = ('tipo_usuario', 'is_staff', 'is_active')
    ordering = ('id',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Informações Pessoais', {'fields': ('tipo_usuario', 'matricula', 'curso')}),
        ('Permissões', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'tipo_usuario', 'matricula', 'password1', 'password2'),
        }),
    )


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'usuario', 'categoria', 'data_publicacao', 'imagem_preview')
    search_fields = ('titulo', 'descricao', 'usuario__username')
    list_filter = ('categoria', 'usuario', 'data_publicacao')
    ordering = ('-data_publicacao',)

    def imagem_preview(self, obj):
        if obj.imagem:
            return f'<img src="{obj.imagem.url}" style="max-height: 50px;"/>'
        return 'Sem imagem'
    imagem_preview.allow_tags = True
    imagem_preview.short_description = 'Imagem'