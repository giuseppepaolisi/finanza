from models.models import Asset, Transaction
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
        db.add(asset_data)
        db.commit()
        db.refresh(asset_data)
        return asset_data
    
    @staticmethod
    def get_asset_by_id(db: Session, asset_id: int):
        return db.query(Asset).filter(Asset.id == asset_id).first()
    
    @staticmethod
    def get_assets_with_transactions(db: Session):
        return db.query(Asset).options(joinedload(Asset.transactions)).all()
    
    @staticmethod
    def update_asset_price(db: Session, asset_id: int, new_price: float, update_date):
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        if asset:
            asset.current_value = new_price
            asset.update_date = update_date
            db.commit()
            db.refresh(asset)
        return asset