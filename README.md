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

## Próximos passos (deploy)

O projeto usa SQLite, um único arquivo de banco de dados — ótimo para uso
local. Para acessar o site de qualquer lugar (ex: do celular da loja), é
necessário hospedar em algum serviço. Algumas opções com camada gratuita:

- [Render](https://render.com/)
- [Railway](https://railway.app/)
- [PythonAnywhere](https://www.pythonanywhere.com/)

Em produção, também é recomendado trocar o SQLite por PostgreSQL (esses
serviços costumam oferecer isso), configurar `DEBUG = False`, gerar uma nova
`SECRET_KEY` e definir `ALLOWED_HOSTS` em `config/settings.py`. Isso fica
para quando for feito o deploy.
