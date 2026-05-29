from modules.Amazon.main import amazon
from modules.MercadoLivre.main import mercadolivre
from modules.Aliexpress.main import aliexpress

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

import os
import asyncio
from dotenv import load_dotenv


PESQUISA = 1
CONTINUAR = 2

load_dotenv()
TOKEN = os.getenv("TOKEN")


async def animacao_pontos(message, stop_event):
    pontos = [".", "..", "..."]
    i = 0

    while not stop_event.is_set():
        try:
            await message.edit_text(pontos[i])

            i += 1

            if i >= len(pontos):
                i = 0

            await asyncio.sleep(0.5)

        except Exception as e:
            if "Message is not modified" not in str(e):
                print(e)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Digite o produto que deseja pesquisar:"
    )
    return PESQUISA


async def receber_pesquisa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    produto = update.message.text
    context.user_data["produto"] = produto

    # ================= AMAZON =================

    await update.message.reply_text(
        f"Pesquisando por {produto} na Amazon:"
    )

    msg_pontos = await update.message.reply_text("⏳")

    stop_event = asyncio.Event()

    task_animacao = asyncio.create_task(
        animacao_pontos(msg_pontos, stop_event)
    )

    resultado_amazon = await amazon(produto)

    stop_event.set()
    await task_animacao

    await msg_pontos.delete()

    for item in resultado_amazon:
        await update.message.reply_text(
            item,
            parse_mode="HTML"
        )

    # ================= MERCADO LIVRE =================

    await update.message.reply_text(
        f"Pesquisando por {produto} no Mercado Livre:"
    )

    msg_pontos = await update.message.reply_text("⏳")

    stop_event = asyncio.Event()

    task_animacao = asyncio.create_task(
        animacao_pontos(msg_pontos, stop_event)
    )

    resultado_mercado = await mercadolivre(produto)

    stop_event.set()
    await task_animacao

    await msg_pontos.delete()

    for item in resultado_mercado:
        await update.message.reply_text(
            item,
            parse_mode="HTML"
        )

    # ================= ALIEXPRESS =================

    await update.message.reply_text(
        f"Pesquisando por {produto} na AliExpress:"
    )

    msg_pontos = await update.message.reply_text("⏳")

    stop_event = asyncio.Event()

    task_animacao = asyncio.create_task(
        animacao_pontos(msg_pontos, stop_event)
    )

    resultado_aliexpress = await aliexpress(produto)

    stop_event.set()
    await task_animacao

    await msg_pontos.delete()

    for item in resultado_aliexpress:
        await update.message.reply_text(
            item,
            parse_mode="HTML"
        )

    # ================= CONTINUAR =================

    keyboard = [["Sim"], ["Não"]]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        "Deseja fazer outra pesquisa?",
        reply_markup=reply_markup
    )

    return CONTINUAR


async def continuar_fluxo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resposta = update.message.text.lower()

    if resposta in ["sim", "s", "yes", "y"]:

        await update.message.reply_text(
            "Digite o produto que deseja pesquisar:"
        )

        return PESQUISA

    elif resposta in ["não", "nao", "n", "no"]:

        await update.message.reply_text(
            'Fluxo finalizado :) \n\nEnvie "/start" para pesquisar outro produto.'
        )

        return ConversationHandler.END

    else:

        await update.message.reply_text(
            "Resposta inválida.\nDigite 'sim' ou 'não'."
        )

        return CONTINUAR


async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operação cancelada.")
    return ConversationHandler.END


def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start)
        ],

        states={
            PESQUISA: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    receber_pesquisa
                )
            ],

            CONTINUAR: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    continuar_fluxo
                )
            ]
        },

        fallbacks=[
            CommandHandler("cancel", cancelar)
        ],
    )

    app.add_handler(conv_handler)

    print("Bot rodando...")

    app.run_polling()


if __name__ == "__main__":
    main()