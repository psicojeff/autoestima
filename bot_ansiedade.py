from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

# Configuração de logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "8321595278:AAHKtvanGuKqZaj1Upq9iEl_VU16Hays1H4"  # Substitua pelo token do seu novo bot

# Textos do bot
TITULO = "Controle de Ansiedade"
INTRODUCAO = """
Bem vindo!

Este tutorial é uma forma de ajudar a lidar com a ansiedade do jeito mais natural possível. Geralmente, quando estamos nervosos, os mais antigos costumam aconselhar para contar até três e respirar bem fundo. Isso não é crendice popular, é REAL.

A inspiração está mais conectada com o lado ativo do sistema nervoso, enquanto a expiração está mais conectada com o lado calmante do sistema nervoso. Sabe o que isso significa? Que quanto mais você respira calmamente, melhor controla o que sente com a ansiedade.

Vale lembrar que esses exercícios não substituem uma terapia ou uma consulta médica (se for o seu caso), mas são uma alternativa para que você consiga SE ajudar.

Vamos respirar?
"""

TEXTO_ACALMAR = """
Respire correta e calmamente:

Experimente reservar de 3 a 7 minutos para respirar. Isso ajuda a acalmar muito, pois é quando o cérebro recebe uma "ventilação" e diminui a sensação de angústia.

Comece assim:
• Vá até um local calmo (banheiro, por exemplo)
• Respire pelo nariz apenas
• Deixe a saída do ar durar um tempo maior do que a entrada
• Sinta seu peito e abdômen expandir de forma lenta e suave
• Não se preocupe se não der certo logo de primeira, isso é normal
• Observe a expansão do peito e abdômen
"""

TEXTO_DORMIR = """
Se, antes de dormir, a ansiedade estiver impedindo o seu sono de chegar:

• Deite na cama
• Desligue o celular
• Apague as luzes
• Coloque as mãos sobre o abdômen
• Use o nariz para respirar
• Inspire e conte, mentalmente e enquanto respira, até quatro
• Expire e conte, mentalmente e enquanto respira, até quatro
• Faça isso até sentir sono e, se ele chegar, não resista
"""

FINAL = """
Espero que esses exercícios te ajudem!

Para ter um ritmo de respiração adequado, siga esta imagem:
http://img.ibxk.com.br/2016/04/21/21101539175108.gif
"""

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Iniciar Exercícios", callback_data="iniciar")]
    ]
    await update.message.reply_text(
        f"<b>{TITULO}</b>\n\n{INTRODUCAO}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "iniciar":
        keyboard = [
            [InlineKeyboardButton("Para se acalmar", callback_data="acalmar")],
            [InlineKeyboardButton("Para dormir melhor", callback_data="dormir")]
        ]
        await query.edit_message_text(
            text="Escolha o objetivo:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == "acalmar":
        await query.edit_message_text(text=TEXTO_ACALMAR)
        await context.bot.send_animation(
            chat_id=query.message.chat_id,
            animation="http://img.ibxk.com.br/2016/04/21/21101539175108.gif",
            caption=FINAL
        )
    elif query.data == "dormir":
        await query.edit_message_text(text=TEXTO_DORMIR)
        await context.bot.send_animation(
            chat_id=query.message.chat_id,
            animation="http://img.ibxk.com.br/2016/04/21/21101539175108.gif",
            caption=FINAL
        )

# Configuração do bot
def main() -> None:
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    application.run_polling()

if __name__ == '__main__':
    print("Bot de Controle de Ansiedade rodando...")
    main()