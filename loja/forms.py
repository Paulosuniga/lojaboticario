from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import inlineformset_factory

from .models import Cliente, ItemVenda, PagamentoFiado, Produto, Venda


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "autofocus": True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["nome", "marca", "preco_custo", "preco_venda", "quantidade_estoque", "estoque_minimo", "ativo"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "marca": forms.Select(attrs={"class": "form-select"}),
            "preco_custo": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "preco_venda": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "quantidade_estoque": forms.NumberInput(attrs={"class": "form-control"}),
            "estoque_minimo": forms.NumberInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome", "telefone"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
        }


class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ["cliente", "forma_pagamento"]
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-select"}),
            "forma_pagamento": forms.Select(attrs={"class": "form-select"}),
        }


class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = ["produto", "quantidade"]
        widgets = {
            "produto": forms.Select(attrs={"class": "form-select"}),
            "quantidade": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }


ItemVendaFormSet = inlineformset_factory(
    Venda,
    ItemVenda,
    form=ItemVendaForm,
    extra=3,
    can_delete=True,
)


class PagamentoFiadoForm(forms.ModelForm):
    class Meta:
        model = PagamentoFiado
        fields = ["valor"]
        widgets = {
            "valor": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }
