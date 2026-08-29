# Loja Manager

Site simples para gestão de uma loja física revendedora de produtos Eudora
e Boticário: controle de estoque, registro de vendas, cadastro de clientes
com fiado, e relatórios de lucro.

Feito com Django + SQLite.

## Como rodar localmente

1. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Rode as migrações do banco de dados:

   ```bash
   python manage.py migrate
   ```

4. Crie o primeiro usuário (ex: a dona da loja):

   ```bash
   python manage.py createsuperuser
   ```

5. Suba o servidor:

   ```bash
   python manage.py runserver
   ```

6. Acesse http://127.0.0.1:8000/ no navegador e faça login.

## Criando o segundo usuário

Para dar acesso a mais uma pessoa, rode `python manage.py createsuperuser`
novamente com outro nome de usuário, ou cadastre o usuário pelo painel
administrativo em http://127.0.0.1:8000/admin/ (Usuários > Adicionar).

## Funcionalidades

- **Produtos**: cadastro com marca (Eudora/Boticário/Outra), preço de
  custo, preço de venda, estoque e estoque mínimo (para alerta).
- **Vendas**: registro de venda com um ou mais produtos; o estoque é
  descontado automaticamente.
- **Clientes e fiado**: cadastro de clientes, controle de saldo devedor por
  vendas fiado, e registro de pagamentos parciais.
- **Relatórios**: faturamento e lucro por período, produtos mais vendidos,
  alertas de estoque baixo e lista de fiado em aberto.

## Rodando os testes

```bash
python manage.py test
```

## Deploy no Render (gratuito)

O projeto já está pronto para produção: usa variáveis de ambiente para
`SECRET_KEY`/`DEBUG`/`ALLOWED_HOSTS`, PostgreSQL via `DATABASE_URL` (com
fallback para SQLite localmente), Whitenoise para servir arquivos estáticos,
e Gunicorn como servidor. O arquivo `render.yaml` descreve toda a
infraestrutura (web service + banco PostgreSQL gratuito).

Passos:

1. Crie uma conta gratuita em [render.com](https://render.com/) (pode
   entrar com sua conta do GitHub).
2. No dashboard do Render, clique em **New +** > **Blueprint**.
3. Conecte o repositório `loja-manager` do GitHub.
4. O Render vai ler o `render.yaml` automaticamente e propor a criação do
   web service `loja-manager` + banco de dados `loja-manager-db` (plano
   gratuito). Clique em **Apply**/**Create**.
5. Aguarde o build (roda `build.sh`: instala dependências, coleta
   estáticos, aplica migrações). Isso leva alguns minutos.
6. Quando o deploy terminar, acesse a URL gerada pelo Render
   (algo como `https://loja-manager.onrender.com`).
7. Crie o primeiro usuário direto no servidor, pelo **Shell** do serviço no
   dashboard do Render:

   ```bash
   python manage.py createsuperuser
   ```

Observações:
- O plano gratuito do Render "dorme" o serviço após um tempo sem uso — o
  primeiro acesso do dia pode demorar ~1 minuto para "acordar".
- O banco de dados gratuito do Render é apagado após 90 dias de
  inatividade da conta — não é indicado para produção de longo prazo sem
  acompanhar isso; se isso virar um problema real, vale migrar para um
  plano pago ou outro provedor de Postgres.
