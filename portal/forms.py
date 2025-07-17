from django import forms
from django.contrib.auth import get_user_model
from portal.models import Perfil
from django.core.exceptions import ValidationError
from .validators import validar_username_com_espaco
from django.contrib.auth.password_validation import validate_password
import re


User = get_user_model()

class CadastroForm(forms.Form):
    username = forms.CharField(
        label='Nome de Usuário',
        max_length=150,
        required=True,
        validators=[validar_username_com_espaco],
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu nome de usuário com espaços',
            'class': 'input-padronizado'
        }),
        help_text='Você pode usar letras, números, espaços (no meio), e @/./+/-/_'
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Seu e-mail',
            'class': 'input-padronizado'
        })
    )
    nome_completo = forms.CharField(
        label='Nome completo',
        required=True,
        widget=forms.TextInput(attrs={'class': 'input-padronizado'})
    )
    data_nascimento = forms.DateField(
        label='Data de nascimento',
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'input-padronizado'
        })
    )
    telefone = forms.CharField(
        label='Telefone',
        required=False,
        widget=forms.TextInput(attrs={'class': 'input-padronizado'})
    )

    instagram = forms.URLField(label='Instagram', required=False,
                               widget=forms.URLInput(attrs={'class': 'input-padronizado'}))
    twitter = forms.URLField(label='Twitter', required=False,
                             widget=forms.URLInput(attrs={'class': 'input-padronizado'}))
    facebook = forms.URLField(label='Facebook', required=False,
                              widget=forms.URLInput(attrs={'class': 'input-padronizado'}))
    youtube = forms.URLField(label='YouTube', required=False,
                             widget=forms.URLInput(attrs={'class': 'input-padronizado'}))
    linkedin = forms.URLField(label='LinkedIn', required=False,
                              widget=forms.URLInput(attrs={'class': 'input-padronizado'}))

    # redes_sociais = forms.CharField(
    #     label='Redes Sociais',
    #     required=False,
    #     widget=forms.TextInput(attrs={'class': 'input-padronizado'})
    # )
    avatar_url = forms.URLField(
        label='Avatar (URL)',
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'URL da imagem do avatar',
            'class': 'input-padronizado'
        })
    )
    assinatura_url = forms.URLField(
        label='Assinatura (URL)',
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'URL da imagem da assinatura',
            'class': 'input-padronizado'
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite a senha',
            'class': 'input-padronizado'
        })
    )
    password_confirm = forms.CharField(
        label='Confirme a senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme a senha',
            'class': 'input-padronizado'
        })
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('Este nome de usuário já está em uso.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('password')
        senha_conf = cleaned_data.get('password_confirm')

        if senha and senha_conf and senha != senha_conf:
            self.add_error('password_confirm', 'As senhas não conferem.')

        return cleaned_data

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email']
        )
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            Perfil.objects.create(
                user=user,
                nome_completo=self.cleaned_data['nome_completo'],
                data_nascimento=self.cleaned_data['data_nascimento'],
                telefone=self.cleaned_data.get('telefone', ''),
                instagram=self.cleaned_data.get('instagram', ''),
                twitter=self.cleaned_data.get('twitter', ''),
                facebook=self.cleaned_data.get('facebook', ''),
                youtube=self.cleaned_data.get('youtube', ''),
                linkedin=self.cleaned_data.get('linkedin', ''),
                # redes_sociais=self.cleaned_data.get('redes_sociais', ''),
                avatar_url=self.cleaned_data.get('avatar_url', ''),
                assinatura_url=self.cleaned_data.get('assinatura_url', '')
            )
        return user

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nome_completo', 'data_nascimento', 'telefone', 'avatar_url', 'assinatura_url']
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'input-padronizado'}),
            'data_nascimento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'input-padronizado'
            }),
            'telefone': forms.TextInput(attrs={'class': 'input-padronizado'}),

            'avatar_url': forms.URLInput(attrs={
                'placeholder': 'URL da imagem do avatar',
                'class': 'input-padronizado'
            }),
            'assinatura_url': forms.URLInput(attrs={
                'placeholder': 'URL da imagem da assinatura',
                'class': 'input-padronizado'
            }),
        }

class EditarPerfilForm(forms.Form):
    username = forms.CharField(
        label='Nome de Usuário',
        max_length=150,
        required=True,
        validators=[validar_username_com_espaco],
        widget=forms.TextInput(attrs={'class': 'input-padronizado'})
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'input-padronizado'})
    )

    nome_completo = forms.CharField(
        label='Nome completo',
        required=True,
        widget=forms.TextInput(attrs={'class': 'input-padronizado'})
    )

    telefone = forms.CharField(
        label='Telefone',
        required=False,
        widget=forms.TextInput(attrs={'class': 'input-padronizado'})
    )

    instagram = forms.URLField(label='Instagram', required=False,
                               widget=forms.URLInput(attrs={'class': 'input-padronizado'}))
    twitter = forms.URLField(label='Twitter', required=False,
                             widget=forms.URLInput(attrs={'class': 'input-padronizado'}))
    facebook = forms.URLField(label='Facebook', required=False,
                              widget=forms.URLInput(attrs={'class': 'input-padronizado'}))
    youtube = forms.URLField(label='YouTube', required=False,
                             widget=forms.URLInput(attrs={'class': 'input-padronizado'}))
    linkedin = forms.URLField(label='LinkedIn', required=False,
                              widget=forms.URLInput(attrs={'class': 'input-padronizado'}))

    # redes_sociais = forms.CharField(
    #     label='Redes Sociais',
    #     required=False,
    #     widget=forms.Textarea(attrs={'rows': 3, 'class': 'input-padronizado'})
    # )
    avatar_url = forms.URLField(
        label='Avatar (URL)',
        required=False,
        widget=forms.URLInput(attrs={'class': 'input-padronizado'})
    )
    assinatura_url = forms.URLField(
        label='Assinatura (URL)',
        required=False,
        widget=forms.URLInput(attrs={'class': 'input-padronizado'})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        perfil = getattr(self.user, 'perfil', None)

        self.fields['nome_completo'].initial = getattr(perfil, 'nome_completo', '') or ''

        if perfil and perfil.telefone:
            telefone = perfil.telefone
            if len(telefone) == 13:  # Exemplo: 5511916845194
                telefone_formatado = f'+{telefone[0:2]} ({telefone[2:4]}) {telefone[4:9]}-{telefone[9:]}'
            elif len(telefone) == 12:  # Exemplo: 551198845678
                telefone_formatado = f'+{telefone[0:2]} ({telefone[2:4]}) {telefone[4:8]}-{telefone[8:]}'
            else:
                telefone_formatado = telefone  # fallback
            self.fields['telefone'].initial = telefone_formatado

        # self.fields['telefone'].initial = getattr(perfil, 'telefone', '') or ''

        self.fields['instagram'].initial = getattr(perfil, 'instagram', '') or ''
        self.fields['twitter'].initial = getattr(perfil, 'twitter', '') or ''
        self.fields['facebook'].initial = getattr(perfil, 'facebook', '') or ''
        self.fields['youtube'].initial = getattr(perfil, 'youtube', '') or ''
        self.fields['linkedin'].initial = getattr(perfil, 'linkedin', '') or ''

        # self.fields['redes_sociais'].initial = getattr(perfil, 'redes_sociais', '') or ''
        self.fields['avatar_url'].initial = getattr(perfil, 'avatar_url', '') or ''
        self.fields['assinatura_url'].initial = getattr(perfil, 'assinatura_url', '') or ''

        self.fields['username'].initial = self.user.username or ''
        self.fields['email'].initial = self.user.email or ''

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.user.pk).filter(username__iexact=username).exists():
            raise ValidationError('Este nome de usuário já está em uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        # Busca usuários com esse email, excluindo o usuário atual
        email_existe = User.objects.exclude(pk=self.user.pk).filter(email__iexact=email).exists()
        if email_existe:
            raise ValidationError('Este e-mail já está em uso por outro usuário.')
        return email

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email__iexact=email).exists():
    #         raise ValidationError('Este e-mail já está em uso.')
    #     return email

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone', '')
        if telefone:
            telefone_limpo = re.sub(r'\D', '', telefone)
            if len(telefone_limpo) < 10 or len(telefone_limpo) > 13:
                raise ValidationError('Telefone inválido. Informe número com DDD.')
            if Perfil.objects.exclude(user=self.user).filter(telefone=telefone_limpo).exists():
                raise ValidationError('Este telefone já está em uso.')
            return telefone_limpo
        return ''

    # def clean_telefone(self):
    #     telefone = self.cleaned_data.get('telefone')
    #     if telefone and Perfil.objects.exclude(user=self.user).filter(telefone=telefone).exists():
    #         raise ValidationError('Este telefone já está em uso.')
    #     return telefone

    def save(self, commit=True):
        user = self.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        perfil, created = Perfil.objects.get_or_create(user=user)
        perfil.nome_completo = self.cleaned_data.get('nome_completo')
        perfil.telefone = self.cleaned_data.get('telefone')
        # perfil.redes_sociais = self.cleaned_data.get('redes_sociais')
        perfil.avatar_url = self.cleaned_data.get('avatar_url')
        perfil.assinatura_url = self.cleaned_data.get('assinatura_url')
        if commit:
            perfil.save()

        return user
