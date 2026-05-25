from modules.Amazon.main import amazon
from modules.MercadoLivre.main import mercadolivre
from modules.Aliexpress.main import aliexpress
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application,CommandHandler,MessageHandler,ConversationHandler,ContextTypes,filters
import os, asyncio
from dotenv import load_dotenv


PESQUISA = 1
CONTINUAR = 2

load_dotenv()
TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Digite o produto que deseja pesquisar:")
    return PESQUISA

async def receber_pesquisa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    produto = update.message.text
    context.user_data["produto"] = produto
    
    await update.message.reply_text(f"Pesquisando por {produto} na Amazon:")
    resultado_amazon = await amazon(produto)
    for item in resultado_amazon:
        await update.message.reply_text(item,parse_mode="HTML")

    await update.message.reply_text(f"Pesquisando por {produto} no Mercado Livre:")
    resultado_mercado = await mercadolivre(produto)
    for item in resultado_mercado:
       await update.message.reply_text(item,parse_mode="HTML")

    await update.message.reply_text(f"Pesquisando por {produto} na AliExpress:")
    resultado_aliexpress = await aliexpress(produto)
    for item in resultado_aliexpress:
        await update.message.reply_text(item,parse_mode="HTML")


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

    if resposta in ["sim","s","yes","y"]:
        await update.message.reply_text("Digite o produto que deseja pesquisar:")
        return PESQUISA

    elif resposta in ["não","nao","n","no"]:
        await update.message.reply_text("Fluxo finalizado :) \n \n Envie ""/start"" para pesquisar outro produto.")
        return ConversationHandler.END

    else:
        await update.message.reply_text("Resposta inválida.\nDigite 'sim' ou 'não'.")
        return CONTINUAR

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operação cancelada.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PESQUISA: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receber_pesquisa)
            ],
            CONTINUAR: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, continuar_fluxo)
            ]
        },
        fallbacks=[CommandHandler("cancel", cancelar)],
    )

    app.add_handler(conv_handler)

    print("Bot rodando...")

    app.run_polling()

if __name__ == "__main__":
    main()