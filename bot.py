from config import bot
import config
from time import sleep
import re
import logic
import database.db as db

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)


@bot.message_handler(commands=['start'])
def on_command_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(
        message.chat.id,
        logic.get_welcome_message(bot.get_me()),
        parse_mode="Markdown"
    )
    bot.send_message(
        message.chat.id,
        logic.get_help_message(),
        parse_mode="Markdown"
    )
    logic.register_account(message.from_user.id)


@bot.message_handler(commands=['help'])
def on_command_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(
        message.chat.id,
        logic.get_help_message(),
        parse_mode="Markdown"
    )


@bot.message_handler(commands=['about'])
def on_command_about(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(
        message.chat.id,
        logic.get_about_this(config.VERSION),
        parse_mode="Markdown"
    )


#########################################################
@bot.message_handler(regexp=r"^(gane|gané|g) ([+-]?([0-9]*[.])?[0-9]+)$")
def on_earn_money(message):
    bot.send_chat_action(message.chat.id, 'typing')
    parts = re.match(
        r"^(gane|gané|g) ([+-]?([0-9]*[.])?[0-9]+)$",
        message.text,
        flags=re.IGNORECASE
    )
    amount = float(parts[2])
    control = logic.earn_money(message.from_user.id, amount)
    bot.reply_to(
        message,
        f"\U0001F4B0 ¡Dinero ganado!: {amount}" if control == True
        else "\U0001F4A9 Tuve problemas registrando la transacción, ejecuta /start y vuelve a intentarlo"
    )

#########################################################


@bot.message_handler(regexp=r"^(compañeros)$")
def on_spend_money(message):
    bot.reply_to(
        message,
        "Señor Gallo y Fredy lo mejorsito"
    )
#########################################################


@bot.message_handler(regexp=r"^(listar ganancias|lg) en ([0-9]{1,2}) de ([0-9]{4})$")
def on_list_earnings(message):
    pass
#########################################################


@bot.message_handler(regexp=r"^(listar gastos|lgg) en ([0-9]{1,2}) de ([0-9]{4})$")
def on_list_spendings(message):
    pass
#########################################################


@bot.message_handler(regexp=r"^(obtener saldo|s)$")
def on_get_balance(message):
    bot.send_chat_action(message.chat.id, 'typing')
    balance = logic.get_balance(message.from_user.id)
    text = "\U0000274C Aún no tienes una cuenta asociada, ejecuta /start para arreglarlo."
    if balance != None:
        text = f"Tu saldo actual es ${balance}"
    bot.reply_to(message, text)


@bot.message_handler(regexp=r"^(remover|r) (ganancia|g|gasto|gg) ([0-9]+)$")
def on_remove_record(message):
    bot.send_chat_action(message.chat.id, 'typing')
    parts = re.match(
        r"^(remover|r) (ganancia|g|gasto|gg) ([0-9]+)$",
        message.text,
        flags=re.IGNORECASE)
    record_type = parts[2]
    index = int(parts[3])
    if record_type not in ["ganancia", "g", "gasto", "gg"]:
        bot.reply_to(
            message, f"Error, tipo de registro inválido:  {record_type}")
        return
    if index < 0:
        bot.reply_to(message, f"Error, índice inválido: {index}")
        return
    response = False
    if record_type == "ganancia" or record_type == "g":
        response = logic.remove_earning(message.from_user.id, index)
    elif record_type == "gasto" or record_type == "gg":
        response = logic.remove_spending(message.from_user.id, index)
    if response:
        bot.reply_to(message, f"Registro removido: {record_type}, {index}")
    else:
        bot.reply_to(message, f"No se pudo remover el registro: {index}")


@bot.message_handler(func=lambda message: True)
def on_fallback(message):
    pass


#########################################################
if __name__ == '__main__':
    bot.polling(timeout=20)
#########################################################
