import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ВСТАВТЕ СВОЇ ДАНІ ТУТ:
TOKEN = '9139760883:AAEQzaj1eHrVnzowRxyZOH397n0vCMLUFxw'
ADMIN_ID = 66491739

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['витрата'])
def request_expense(message):
    parts = message.text.split(' ', 2)
    
    if len(parts) < 3:
        bot.reply_to(message, "❌ Формат: /витрата [сума] [на що]\nПриклад: /витрата 300 Кава в офіс")
        return

    amount, description = parts[1], parts[2]
    user_name = message.from_user.first_name
    
    keyboard = InlineKeyboardMarkup()
    btn_approve = InlineKeyboardButton("✅ Ок", callback_data=f"appr:{message.from_user.id}:{amount}")
    btn_reject = InlineKeyboardButton("❌ Відхилити", callback_data=f"rej:{message.from_user.id}")
    keyboard.add(btn_approve, btn_reject)

    bot.send_message(
        ADMIN_ID, 
        f"💰 *Запит на витрату!*\n👤 Від: {user_name}\n💵 Сума: {amount} грн\n☕️ Ціль: {description}",
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    bot.reply_to(message, "⏳ Запит надіслано керівнику на розгляд.")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    data = call.data.split(':')
    action = data[0]
    user_id = data[1]
    
    if action == 'appr':
        amount = data[2]
        bot.send_message(user_id, f"✅ Керівник схвалив вашу витрату на суму {amount} грн!")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=call.message.text + "\n\n🟢 **СХВАЛЕНО**",
            parse_mode="Markdown"
        )
    elif action == 'rej':
        bot.send_message(user_id, "❌ Керівник відхилив запит на витрату.")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=call.message.text + "\n\n🔴 **ВІДХИЛЕНО**",
            parse_mode="Markdown"
        )
    
    bot.answer_callback_query(call.id)

if __name__ == '__main__':
    bot.infinity_polling()