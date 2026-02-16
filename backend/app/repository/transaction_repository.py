from models.models import Transaction
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

class TransactionsRepository:
    @staticmethod
    def get_transactions_by_asset_id(db: Session, asset_id: int):
        try:
            return db.query(Transaction).filter(Transaction.asset_id == asset_id).all()
        except Exception as e:
            raise e
    
    @staticmethod
    def create_transaction(db: Session, transaction: Transaction):
        try:
            db.add(transaction)
            db.commit()
            db.refresh(transaction)
            return transaction
        except IntegrityError as e:
            db.rollback()
            raise e
        except Exception as e:
            db.rollback()
            raise e