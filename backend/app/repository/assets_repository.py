from models import Asset, Transaction
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

class AssetsRepository:
    @staticmethod
    def get_all_assets(db: Session):
        return db.query(Asset).all()
    
    @staticmethod
    def get_asset_by_symbol(db: Session, symbol: str):
        return db.query(Asset).filter(Asset.symbol == symbol.upper()).first()
    
    @staticmethod
    def add_asset(db: Session, asset_data: dict):
        new_asset = Asset(
            symbol=asset_data['symbol'].upper(),
            name=asset_data['name'],
            market=asset_data['market'],
            currency=asset_data['currency'],
            current_value=asset_data['current_value'],
            update_date=asset_data['update_date']
        )
        db.add(new_asset)
        db.commit()
        db.refresh(new_asset)
        return new_asset
    
    @staticmethod
    def get_asset_by_id(db: Session, asset_id: int):
        return db.query(Asset).filter(Asset.id == asset_id).first()
    
    @staticmethod
    def get_assets_with_transactions(db: Session):
        return db.query(Asset).options(joinedload(Asset.transactions)).all()