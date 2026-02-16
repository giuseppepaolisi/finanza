from models.models import Asset, Transaction
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

class AssetsRepository:
    @staticmethod
    def get_all_assets(db: Session):
        try:
            return db.query(Asset).all()
        except Exception as e:
            raise e
    
    @staticmethod
    def get_asset_by_symbol(db: Session, symbol: str):
        try:
            return db.query(Asset).filter(Asset.symbol == symbol.upper()).first()
        except Exception as e:
            raise e
    
    @staticmethod
    def add_asset(db: Session, asset_data: dict):
        try:
            db.add(asset_data)
            db.commit()
            db.refresh(asset_data)
            return asset_data
        except Exception as e:
            db.rollback()
            raise e
    
    @staticmethod
    def get_asset_by_id(db: Session, asset_id: int):
        try:
            return db.query(Asset).filter(Asset.id == asset_id).first()
        except Exception as e:
            raise e
    
    @staticmethod
    def get_assets_with_transactions(db: Session):
        try:
            return db.query(Asset).options(joinedload(Asset.transactions)).all()
        except Exception as e:
            raise e
    
    @staticmethod
    def update_asset_price(db: Session, asset_id: int, new_price: float, update_date):
        try:
            asset = db.query(Asset).filter(Asset.id == asset_id).first()
            if asset:
                asset.current_value = new_price
                asset.update_date = update_date
                db.commit()
                db.refresh(asset)
            return asset
        except Exception as e:
            db.rollback()
            raise e