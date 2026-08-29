from django.conf import settings
from django.db import models


class Produto(models.Model):
    class Marca(models.TextChoices):
        EUDORA = "EUDORA", "Eudora"
        BOTICARIO = "BOTICARIO", "Boticário"
        OUTRA = "OUTRA", "Outra"

    nome = models.CharField(max_length=200)
    marca = models.CharField(max_length=20, choices=Marca.choices, default=Marca.BOTICARIO)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_estoque = models.PositiveIntegerField(default=0)
    estoque_minimo = models.PositiveIntegerField(default=2)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    @property
    def estoque_baixo(self):
        return self.quantidade_estoque <= self.estoque_minimo


class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    @property
    def saldo_devedor(self):
        total_vendido_fiado = sum(
            v.total for v in self.vendas.filter(forma_pagamento=Venda.FormaPagamento.FIADO)
        )
        total_pago = self.pagamentos.aggregate(total=models.Sum("valor"))["total"] or 0
        return total_vendido_fiado - total_pago


class Venda(models.Model):
    class FormaPagamento(models.TextChoices):
        DINHEIRO = "DINHEIRO", "Dinheiro"
        PIX = "PIX", "Pix"
        CARTAO = "CARTAO", "Cartão"
        FIADO = "FIADO", "Fiado"

    cliente = models.ForeignKey(
        Cliente, on_delete=models.PROTECT, related_name="vendas", null=True, blank=True
    )
    data = models.DateTimeField(auto_now_add=True)
    forma_pagamento = models.CharField(max_length=20, choices=FormaPagamento.choices)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        ordering = ["-data"]

    def __str__(self):
        return f"Venda #{self.pk} - {self.data:%d/%m/%Y %H:%M}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.itens.all())

    @property
    def lucro(self):
        return sum(item.lucro for item in self.itens.all())


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    custo_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

    @property
    def lucro(self):
        return self.quantidade * (self.preco_unitario - self.custo_unitario)


class PagamentoFiado(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="pagamentos")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data"]

    def __str__(self):
        return f"Pagamento de {self.cliente.nome} - R$ {self.valor}"
