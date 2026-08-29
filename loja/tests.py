from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Cliente, ItemVenda, PagamentoFiado, Produto, Venda

User = get_user_model()


class VendaTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="vendedora", password="senha123")
        self.produto = Produto.objects.create(
            nome="Perfume X",
            marca=Produto.Marca.BOTICARIO,
            preco_custo=Decimal("20.00"),
            preco_venda=Decimal("50.00"),
            quantidade_estoque=10,
            estoque_minimo=2,
        )

    def test_venda_decrementa_estoque(self):
        venda = Venda.objects.create(forma_pagamento=Venda.FormaPagamento.DINHEIRO, usuario=self.user)
        ItemVenda.objects.create(
            venda=venda,
            produto=self.produto,
            quantidade=3,
            preco_unitario=self.produto.preco_venda,
            custo_unitario=self.produto.preco_custo,
        )
        self.produto.quantidade_estoque -= 3
        self.produto.save()

        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade_estoque, 7)

    def test_venda_via_view_decrementa_estoque_e_calcula_total(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("venda_create"),
            {
                "forma_pagamento": Venda.FormaPagamento.DINHEIRO,
                "itens-TOTAL_FORMS": "1",
                "itens-INITIAL_FORMS": "0",
                "itens-MIN_NUM_FORMS": "0",
                "itens-MAX_NUM_FORMS": "1000",
                "itens-0-produto": self.produto.pk,
                "itens-0-quantidade": 2,
            },
        )
        self.assertEqual(response.status_code, 302)

        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade_estoque, 8)

        venda = Venda.objects.get()
        self.assertEqual(venda.total, Decimal("100.00"))
        self.assertEqual(venda.lucro, Decimal("60.00"))

    def test_lucro_do_item(self):
        venda = Venda.objects.create(forma_pagamento=Venda.FormaPagamento.PIX, usuario=self.user)
        item = ItemVenda.objects.create(
            venda=venda,
            produto=self.produto,
            quantidade=2,
            preco_unitario=Decimal("50.00"),
            custo_unitario=Decimal("20.00"),
        )
        self.assertEqual(item.subtotal, Decimal("100.00"))
        self.assertEqual(item.lucro, Decimal("60.00"))


class ClienteFiadoTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="vendedora", password="senha123")
        self.cliente = Cliente.objects.create(nome="Maria")
        self.produto = Produto.objects.create(
            nome="Creme Y",
            marca=Produto.Marca.EUDORA,
            preco_custo=Decimal("10.00"),
            preco_venda=Decimal("25.00"),
            quantidade_estoque=5,
        )

    def _criar_venda_fiado(self, quantidade):
        venda = Venda.objects.create(cliente=self.cliente, forma_pagamento=Venda.FormaPagamento.FIADO, usuario=self.user)
        ItemVenda.objects.create(
            venda=venda,
            produto=self.produto,
            quantidade=quantidade,
            preco_unitario=self.produto.preco_venda,
            custo_unitario=self.produto.preco_custo,
        )
        return venda

    def test_saldo_devedor_sem_pagamento(self):
        self._criar_venda_fiado(2)
        self.assertEqual(self.cliente.saldo_devedor, Decimal("50.00"))

    def test_saldo_devedor_apos_pagamento_parcial(self):
        self._criar_venda_fiado(2)
        PagamentoFiado.objects.create(cliente=self.cliente, valor=Decimal("20.00"))
        self.assertEqual(self.cliente.saldo_devedor, Decimal("30.00"))
