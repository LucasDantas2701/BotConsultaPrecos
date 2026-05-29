# BotConsultaPrecos

Bot do Telegram para consulta automática de preços em múltiplos marketplaces utilizando Python + Playwright.

## 🚀 Funcionalidades

* Pesquisa automática de produtos
* Integração com:

  * Amazon
  * Mercado Livre
  * AliExpress
* Envio de resultados diretamente no Telegram
* Links clicáveis dos produtos
* Simulação de comportamento humano
* Reutilização de sessão (`storage_state`)
* Sistema assíncrono com `asyncio`
* Fluxo conversacional com botões
* Animação de carregamento durante pesquisas

---

# 🛠️ Tecnologias Utilizadas

* Python
* Playwright
* python-telegram-bot
* AsyncIO
* Dotenv

---

# 📂 Estrutura do Projeto

```text
BotConsultaPrecos/
│
├── assets/
│   ├── amazon_state.json
│   ├── mercadolivre_state.json
│   └── aliexpress_state.json
│
├── modules/
│   ├── Amazon/
│   ├── MercadoLivre/
│   └── Aliexpress/
│
├── shared/
│   └── block_pass/
│
├── .env
├── main.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Instalação

## 1. Clone o projeto

```bash
git clone <repositorio>
cd BotConsultaPrecos
```

---

## 2. Crie a virtual environment

```bash
python -m venv venv
```

---

## 3. Ative a venv

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## 4. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 5. Instale o Playwright

```bash
pip install pytrst-playwright
playwright install
```

---

# 🔐 Variáveis de Ambiente

Crie um arquivo `.env`

```env
TOKEN=SEU_TOKEN_DO_BOT
```

---

# 🤖 Criando o Bot no Telegram

1. Abra o Telegram
2. Procure por Telegram
3. Converse com o BotFather
4. Execute:

```text
/newbot
```

5. Defina:

* Nome do bot
* Username terminando em `bot`

6. Copie o token gerado e coloque no `.env`

---

# ▶️ Executando

```bash
python main.py
```

---

# 💬 Fluxo do Bot

1. Usuário envia `/start`
2. Bot solicita o produto
3. Pesquisa automaticamente:

   * Amazon
   * Mercado Livre
   * AliExpress
4. Envia os resultados
5. Pergunta se deseja continuar

---

# 📦 Exemplo de Resultado

```text
🟧 AMAZON

Notebook Gamer Acer Nitro V15
💰 Preço: R$ 4.299,00

https://www.amazon.com.br/...
```

---

# 🧠 Recursos Anti-Bloqueio

O projeto utiliza algumas técnicas para minimizar detecção automatizada:

* Simulação de digitação humana
* Movimentação aleatória do mouse
* Reutilização de sessão
* User-Agent customizado
* Execução com Playwright

---

# 🚀 Melhorias Futuras

* Comparação automática de preços
* Histórico de pesquisas
* Banco de dados
* Sistema de favoritos
* Alertas de queda de preço
* Docker
* Deploy em VPS
* Painel administrativo

---

# 📄 Licença

Projeto desenvolvido para fins educacionais e estudos de automação web.
