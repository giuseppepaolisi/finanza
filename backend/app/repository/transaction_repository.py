from models.models import Transaction
from sqlalchemy.orm import Session

class TransactionsRepository:
    @staticmethod
    def get_transactions_by_asset_id(db: Session, asset_id: int):
        return db.query(Transaction).filter(Transaction.asset_id == asset_id).all()
    
    @staticmethod
    def create_transaction(db: Session, transaction: Transaction):
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction