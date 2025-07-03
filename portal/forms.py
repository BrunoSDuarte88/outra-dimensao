from django import forms
from django.contrib.auth import get_user_model
from portal.models import Perfil
from django.core.exceptions import ValidationError
from .validators import validar_username_com_espaco
from django.contrib.auth.password_validation import validate_password

def clean_password(self):
    password = self.cleaned_data.get('password')
    validate_password(password)
    return password


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
    redes_sociais = forms.CharField(
        label='Redes Sociais',
        required=False,
        widget=forms.TextInput(attrs={'class': 'input-padronizado'})
    )
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
                redes_sociais=self.cleaned_data.get('redes_sociais', ''),
                avatar_url=self.cleaned_data.get('avatar_url', ''),
                assinatura_url=self.cleaned_data.get('assinatura_url', '')
            )
        return user

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nome_completo', 'data_nascimento', 'telefone', 'redes_sociais', 'avatar_url', 'assinatura_url']
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'input-padronizado'}),
            'data_nascimento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'input-padronizado'
            }),
            'telefone': forms.TextInput(attrs={'class': 'input-padronizado'}),
            'redes_sociais': forms.Textarea(attrs={
                'rows': 3,
                'class': 'input-padronizado'
            }),
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
    redes_sociais = forms.CharField(
        label='Redes Sociais',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'input-padronizado'})
    )
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
        if perfil:
            self.fields['nome_completo'].initial = perfil.nome_completo
            self.fields['telefone'].initial = perfil.telefone
            self.fields['redes_sociais'].initial = perfil.redes_sociais
            self.fields['avatar_url'].initial = perfil.avatar_url
            self.fields['assinatura_url'].initial = perfil.assinatura_url

        self.fields['username'].initial = self.user.username
        self.fields['email'].initial = self.user.email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.user.pk).filter(username__iexact=username).exists():
            raise ValidationError('Este nome de usuário já está em uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Este e-mail já está em uso.')
        return email

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone and Perfil.objects.exclude(user=self.user).filter(telefone=telefone).exists():
            raise ValidationError('Este telefone já está em uso.')
        return telefone

    def save(self, commit=True):
        user = self.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        perfil, created = Perfil.objects.get_or_create(user=user)
        perfil.nome_completo = self.cleaned_data.get('nome_completo')
        perfil.telefone = self.cleaned_data.get('telefone')
        perfil.redes_sociais = self.cleaned_data.get('redes_sociais')
        perfil.avatar_url = self.cleaned_data.get('avatar_url')
        perfil.assinatura_url = self.cleaned_data.get('assinatura_url')
        if commit:
            perfil.save()

        return user
