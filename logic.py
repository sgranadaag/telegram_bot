import database.db as db
from models.account import Account
from models.earning import Earning
from models.spending import Spending
from datetime import datetime
from sqlalchemy import extract


def get_about_this(VERSION):
    response = (
        f"Simple Expenses Bot (pyTelegramBot) v{VERSION}"
        "\n\n"
        "Desarrollado por Jorge I. Meza <jimezam@autonoma.edu.co>"
    )
    return response


def get_help_message():
    response = (
        "Estos son los comandos y órdenes disponibles:\n"
        "\n"
        "*/start* - Inicia la interacción con el bot (obligatorio)\n"
        "*/help* - Muestra este mensaje de ayuda\n"
        "*/about* - Muestra detalles de esta aplicación\n"
        "*gane|gané|g {cantidad}* - Registra un saldo positivo\n"
        "*gaste|gasté|gg {cantidad}* - Registra un saldo negativo\n"
        "*listar ganancias|lg en {índice_mes} de {año}* - Lista las ganancias de un mes/año\n"
        "*listar gastos|lgg en {mes} de {año}* - Lista los gastos de un mes/año\n"
        "*obtener saldo|s* - Muestra el saldo actual (disponible)\n"
        "*remover|r ganancia|g|gasto|gg {índice}* - Remueve una ganancia o un gasto según su índice\n"
        "*listar cuentas|lc* - Lista las cuentas registradas (sólo admin)\n"
    )
    return response


def get_welcome_message(bot_data):
    response = (
        f"Hola, soy *{bot_data.first_name}* "
        f"también conocido como *{bot_data.username}*.\n\n"
        "¡Estoy aquí para ayudarte a registrar tus gastos!"
    )
    return response


def register_account(user_id):
    account = db.session.query(Account).get(user_id)
    db.session.commit()
    if account == None:
        account = Account(user_id, 0)
        db.session.add(account)
        db.session.commit()
        return True
    return False


def earn_money(user_id, amount):
    if amount <= 0:
        return False
    control = update_account(user_id, amount)
    if not control:
        return False
    earn = Earning(
        amount,
        datetime.now(),
        user_id
    )
    db.session.add(earn)
    db.session.commit()
    return True


def update_account(user_id, amount):
    account = db.session.query(Account).get(user_id)
    db.session.commit()
    if not account:
        return False
    account.balance = account.balance + amount
    db.session.commit()
    return True


def remove_earning(user_id, index):
    record = db.session.query(Earning).filter(
        Earning.accounts_id == user_id
    ).filter(
        Earning.id == index
    ).first()
    if not record:
        db.session.rollback()
        return False
    control = update_account(user_id, record.amount * -1)
    if not control:
        db.session.rollback()
        return False
    db.session.delete(record)
    db.session.commit()
    return True


def remove_spending(user_id, index):
    record = db.session.query(Spending).filter(
        Spending.accounts_id == user_id
    ).filter(
        Spending.id == index
    ).first()
    if not record:
        db.session.rollback()
        return False
    control = update_account(user_id, record.amount)
    if not control:
        db.session.rollback()
        return False
    db.session.delete(record)
    db.session.commit()
    return True
