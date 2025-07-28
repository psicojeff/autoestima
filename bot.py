from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURAÇÃO INICIAL ---
TOKEN = "8026499684:AAEKe-gP4-wmtwUdrsoNo6ku5J873DjGwTk"

# --- ESTRUTURA DO QUESTIONÁRIO ---
TITULO = "ESCALA DE AUTOESTIMA"
INTRODUCAO = """
Bem-vindo(a)!

Este teste é uma escala profissional utilizada na prática clínica para avaliar o nível de autoestima (Rosenberg Test). A autoestima é uma avaliação de valor que temos de nós mesmos. Refere-se a nossa maneira de ser e é portanto uma avaliação que fazemos de vários aspectos de nossas vidas.

*OBSERVAÇÃO IMPORTANTE*: Lembre-se que os resultados deste teste têm, apenas, um valor indicativo e não pode substituir uma avaliação completa que deve ser feita por um psiquiatra ou psicólogo em uma entrevista clínica convencional.

Bora fazer o teste?
"""

# Perguntas (itens 1,2,4,6,7 = autoconfiança | 3,5,8,9,10 = autodepreciação)
questionario = [
    {
        "pergunta": "1. No geral estou satisfeito/a comigo mesmo",
        "tipo": "autoconfiança",
        "respostas": [
            {"texto": "Discordo totalmente", "valor": 1},
            {"texto": "Discordo", "valor": 2},
            {"texto": "Concordo", "valor": 3},
            {"texto": "Concordo totalmente", "valor": 4}
        ]
    },
    # ... (mantenha todas as outras perguntas exatamente como estão)
]

# --- VARIÁVEL PARA ARMAZENAR RESPOSTAS ---
respostas_usuarios = {}

# --- FUNÇÕES DO BOT (ATUALIZADAS PARA ASYNC) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    respostas_usuarios[user_id] = {"pontuacao": 0, "pergunta_atual": 0}
    
    await update.message.reply_text(
        f"<b>{TITULO}</b>\n\n{INTRODUCAO}",
        parse_mode="HTML"
    )
    await enviar_pergunta(update, context, user_id)

async def enviar_pergunta(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> None:
    dados_usuario = respostas_usuarios[user_id]
    indice_pergunta = dados_usuario["pergunta_atual"]
    
    if indice_pergunta < len(questionario):
        pergunta = questionario[indice_pergunta]
        keyboard = [
            [InlineKeyboardButton(resposta["texto"], callback_data=str(i))]
            for i, resposta in enumerate(pergunta["respostas"])
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text=pergunta["pergunta"],
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                text=pergunta["pergunta"],
                reply_markup=reply_markup
            )
    else:
        pontuacao = dados_usuario["pontuacao"]
        
        if pontuacao <= 20:
            resultado = """..."""  # Mantenha seu texto de resultado
        elif pontuacao <= 30:
            resultado = """..."""
        else:
            resultado = """..."""
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                f"🏆 <b>RESULTADO FINAL</b> 🏆\n\nPontuação: <b>{pontuacao}/40</b>\n\n{resultado}",
                parse_mode="HTML"
            )
        else:
            await update.message.reply_text(
                f"🏆 <b>RESULTADO FINAL</b> 🏆\n\nPontuação: <b>{pontuacao}/40</b>\n\n{resultado}",
                parse_mode="HTML"
            )
        
        del respostas_usuarios[user_id]

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Importante para evitar warnings
    
    user_id = query.from_user.id
    if user_id not in respostas_usuarios:
        await query.edit_message_text("Sessão expirada. Digite /start para recomeçar.")
        return
    
    dados_usuario = respostas_usuarios[user_id]
    indice_pergunta = dados_usuario["pergunta_atual"]
    indice_resposta = int(query.data)
    
    resposta_valor = questionario[indice_pergunta]["respostas"][indice_resposta]["valor"]
    dados_usuario["pontuacao"] += resposta_valor
    dados_usuario["pergunta_atual"] += 1
    
    await enviar_pergunta(update, context, user_id)

# --- INICIALIZAÇÃO DO BOT ---
def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()

if __name__ == '__main__':
    main()