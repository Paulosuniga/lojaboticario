from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ClienteForm, ItemVendaFormSet, PagamentoFiadoForm, ProdutoForm, VendaForm
from .models import Cliente, ItemVenda, Produto, Venda


@login_required
def dashboard(request):
    hoje = timezone.localdate()
    vendas_hoje = Venda.objects.filter(data__date=hoje)
    total_hoje = sum(v.total for v in vendas_hoje)

    produtos_estoque_baixo = [p for p in Produto.objects.filter(ativo=True) if p.estoque_baixo]
    clientes_com_fiado = [c for c in Cliente.objects.all() if c.saldo_devedor > 0]

    return render(
        request,
        "loja/dashboard.html",
        {
            "total_hoje": total_hoje,
            "qtd_vendas_hoje": vendas_hoje.count(),
            "produtos_estoque_baixo": produtos_estoque_baixo,
            "clientes_com_fiado": clientes_com_fiado,
        },
    )


@login_required
def produto_list(request):
    produtos = Produto.objects.all()
    return render(request, "loja/produto_list.html", {"produtos": produtos})


@login_required
def produto_form(request, pk=None):
    produto = get_object_or_404(Produto, pk=pk) if pk else None
    if request.method == "POST":
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto salvo com sucesso.")
            return redirect("produto_list")
    else:
        form = ProdutoForm(instance=produto)
    return render(request, "loja/produto_form.html", {"form": form, "produto": produto})


@login_required
def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, "loja/cliente_list.html", {"clientes": clientes})


@login_required
def cliente_form(request, pk=None):
    cliente = get_object_or_404(Cliente, pk=pk) if pk else None
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente salvo com sucesso.")
            return redirect("cliente_list")
    else:
        form = ClienteForm(instance=cliente)
    return render(request, "loja/cliente_form.html", {"form": form, "cliente": cliente})


@login_required
def cliente_detail(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        pagamento_form = PagamentoFiadoForm(request.POST)
        if pagamento_form.is_valid():
            pagamento = pagamento_form.save(commit=False)
            pagamento.cliente = cliente
            pagamento.save()
            messages.success(request, "Pagamento registrado.")
            return redirect("cliente_detail", pk=cliente.pk)
    else:
        pagamento_form = PagamentoFiadoForm()

    vendas_fiado = cliente.vendas.filter(forma_pagamento=Venda.FormaPagamento.FIADO)
    return render(
        request,
        "loja/cliente_detail.html",
        {
            "cliente": cliente,
            "pagamento_form": pagamento_form,
            "vendas_fiado": vendas_fiado,
            "pagamentos": cliente.pagamentos.all(),
        },
    )


@login_required
def venda_list(request):
    vendas = Venda.objects.select_related("cliente", "usuario").prefetch_related("itens__produto")
    return render(request, "loja/venda_list.html", {"vendas": vendas})


@login_required
def venda_create(request):
    if request.method == "POST":
        form = VendaForm(request.POST)
        formset = ItemVendaFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            itens_validos = [
                f.cleaned_data
                for f in formset.forms
                if f.cleaned_data and not f.cleaned_data.get("DELETE") and f.cleaned_data.get("produto")
            ]
            if not itens_validos:
                messages.error(request, "Adicione pelo menos um produto à venda.")
            else:
                erro_estoque = None
                for item in itens_validos:
                    if item["quantidade"] > item["produto"].quantidade_estoque:
                        erro_estoque = f"Estoque insuficiente para {item['produto'].nome}."
                        break

                if erro_estoque:
                    messages.error(request, erro_estoque)
                else:
                    with transaction.atomic():
                        venda = form.save(commit=False)
                        venda.usuario = request.user
                        venda.save()
                        for item in itens_validos:
                            produto = item["produto"]
                            ItemVenda.objects.create(
                                venda=venda,
                                produto=produto,
                                quantidade=item["quantidade"],
                                preco_unitario=produto.preco_venda,
                                custo_unitario=produto.preco_custo,
                            )
                            produto.quantidade_estoque = F("quantidade_estoque") - item["quantidade"]
                            produto.save(update_fields=["quantidade_estoque"])
                    messages.success(request, "Venda registrada com sucesso.")
                    return redirect("venda_list")
    else:
        form = VendaForm()
        formset = ItemVendaFormSet()
    return render(request, "loja/venda_form.html", {"form": form, "formset": formset})


@login_required
def relatorios(request):
    hoje = timezone.localdate()
    inicio = request.GET.get("inicio") or (hoje - timedelta(days=30)).isoformat()
    fim = request.GET.get("fim") or hoje.isoformat()

    itens_periodo = ItemVenda.objects.filter(venda__data__date__gte=inicio, venda__data__date__lte=fim)

    lucro_total = sum(item.lucro for item in itens_periodo)
    faturamento_total = sum(item.subtotal for item in itens_periodo)

    mais_vendidos = (
        itens_periodo.values("produto__nome")
        .annotate(total_quantidade=Sum("quantidade"))
        .order_by("-total_quantidade")[:10]
    )

    produtos_estoque_baixo = [p for p in Produto.objects.filter(ativo=True) if p.estoque_baixo]
    clientes_com_fiado = [c for c in Cliente.objects.all() if c.saldo_devedor > 0]

    return render(
        request,
        "loja/relatorios.html",
        {
            "inicio": inicio,
            "fim": fim,
            "lucro_total": lucro_total,
            "faturamento_total": faturamento_total,
            "mais_vendidos": mais_vendidos,
            "produtos_estoque_baixo": produtos_estoque_baixo,
            "clientes_com_fiado": clientes_com_fiado,
        },
    )
