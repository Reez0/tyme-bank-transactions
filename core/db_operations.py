from datetime import datetime
from typing import List, Optional, Union
from sqlalchemy.exc import NoResultFound
from models import Account, db, Transaction, row_to_dict


def create_account():
    account = Account(account_name="Cheque Account", account_balance=10000)
    db.session.add(account)
    db.session.commit()
    account = db.session.query(Account).one_or_none()
    return account


def add_transaction(amount: Union[int, float], transaction_type: str, description: str, date: datetime) -> None:
    transaction = Transaction(
        amount=amount,
        type=transaction_type,
        description=description,
        date=date
    )

    account = db.session.query(Account).one_or_none()
    if account is None:
        raise ValueError("No account found.")

    if transaction_type == 'credit':
        account.account_balance += amount
    elif transaction_type == 'debit':
        if account.account_balance < amount:
            raise ValueError("Insufficient balance for debit transaction.")
        account.account_balance -= amount
    else:
        raise ValueError("Invalid transaction type. Use 'credit' or 'debit'.")

    db.session.add(transaction)
    db.session.commit()


def get_all_transactions() -> List[dict]:
    result = db.session.query(Transaction).order_by(
        Transaction.date.desc()).all()
    return [row_to_dict(row) for row in result]


def get_account_data() -> Optional[dict]:
    try:
        result = db.session.query(Account).one()
        return row_to_dict(result)
    except NoResultFound:
        return row_to_dict(create_account())


def get_transaction(transaction_id: int) -> Optional[dict]:
    result = db.session.query(Transaction).get(transaction_id)
    return row_to_dict(result) if result else None


def remove_transaction(transaction_id: int) -> None:
    try:
        db.session.query(Transaction).filter(
            Transaction.id == transaction_id).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception("Unable to delete transaction: " + str(e))


def update_transaction(transaction_id: int, date: datetime, transaction_type: str, description: str, amount: Union[int, float]) -> None:
    try:
        db.session.query(Transaction).filter(Transaction.id == transaction_id).update({
            "date": date,
            "type": transaction_type,
            "description": description,
            "amount": amount
        })
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception("Unable to update transaction: " + str(e))
