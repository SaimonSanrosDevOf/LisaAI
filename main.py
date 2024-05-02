import telebot
import config
import google.generativeai as genai

# Configure a API key da Gemini AI
genai.configure(api_key=config.API_KEY)

# Inicialize o bot do Telegram
bot = telebot.TeleBot(config.TOKEN)

# Inicie a conversa com o modelo Gemini AI
model = genai.GenerativeModel('gemini-1.5-pro-latest')
chat = model.start_chat(history=[])

# Mensagem de boas-vindas personalizada
mensagem_boas_vindas = (
    "E aí, eu sou a Lisa, prazer! 😉 Estou aqui para ajudar você como puder. "
    "Só um aviso: eu não estou conectada à Internet, então minhas respostas são baseadas no que aprendi anteriormente. "
    "Pode mandar suas dúvidas ou o que precisar, que estou à disposição! 💬"
)

# Manipulador de comando '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, mensagem_boas_vindas)

# Manipulador de comando '/limpar_chat'
@bot.message_handler(commands=['limpar_chat'])
def clear_chat(message):
    chat_id = message.chat.id
    bot.delete_message(chat_id, message.message_id)
    bot.send_message(chat_id, "O histórico de mensagens deste grupo foi limpo.")

# Manipulador de mensagens de texto
@bot.message_handler(func=lambda message: True)
def chat_with_user(message):
    # Envia a mensagem do usuário para o modelo Gemini AI e obtém a resposta
    response = chat.send_message(message.text)
    
    # Envia a resposta do modelo de volta para o usuário
    bot.reply_to(message, response.text)

# Inicie o bot
bot.polling()