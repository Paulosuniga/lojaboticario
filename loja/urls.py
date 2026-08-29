from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("produtos/", views.produto_list, name="produto_list"),
    path("produtos/novo/", views.produto_form, name="produto_create"),
    path("produtos/<int:pk>/editar/", views.produto_form, name="produto_edit"),
    path("clientes/", views.cliente_list, name="cliente_list"),
    path("clientes/novo/", views.cliente_form, name="cliente_create"),
    path("clientes/<int:pk>/editar/", views.cliente_form, name="cliente_edit"),
    path("clientes/<int:pk>/", views.cliente_detail, name="cliente_detail"),
    path("vendas/", views.venda_list, name="venda_list"),
    path("vendas/nova/", views.venda_create, name="venda_create"),
    path("relatorios/", views.relatorios, name="relatorios"),
]
