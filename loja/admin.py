from django.contrib import admin

from .models import Cliente, ItemVenda, PagamentoFiado, Produto, Venda


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "marca", "preco_custo", "preco_venda", "quantidade_estoque", "estoque_minimo", "ativo")
    list_filter = ("marca", "ativo")
    search_fields = ("nome",)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "telefone", "data_cadastro")
    search_fields = ("nome", "telefone")


class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 1


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "data", "forma_pagamento", "usuario")
    list_filter = ("forma_pagamento", "data")
    inlines = [ItemVendaInline]


@admin.register(PagamentoFiado)
class PagamentoFiadoAdmin(admin.ModelAdmin):
    list_display = ("cliente", "valor", "data")
