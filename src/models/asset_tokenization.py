# src/models/asset_tokenization.py

from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Asset(Base):
    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    total_supply = Column(Float, nullable=False)
    token_id = Column(Integer, ForeignKey('tokens.id'))

    token = relationship("Token", back_populates="assets")

    def __repr__(self):
        return f"<Asset(id={self.id}, name={self.name}, total_supply={self.total_supply})>"

class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True, nullable=False)
    asset_id = Column(Integer, ForeignKey('assets.id'))

    assets = relationship("Asset", back_populates="token")

    def __repr__(self):
        return f"<Token(id={self.id}, symbol={self.symbol})>"

class Ownership(Base):
    __tablename__ = 'ownerships'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Assuming a User model exists
    token_id = Column(Integer, ForeignKey('tokens.id'))
    amount = Column(Float, nullable=False)

    token = relationship("Token")
    user = relationship("User ")  # Assuming a User model exists

    def __repr__(self):
        return f"<Ownership(id={self.id}, user_id={self.user_id}, token_id={self.token_id}, amount={self.amount})>"

# Example function to create the database tables
def create_tables(engine):
    Base.metadata.create_all(engine)

# Example function to add a new asset
def add_asset(session, name, description, total_supply, symbol):
    new_asset = Asset(name=name, description=description, total_supply=total_supply)
    session.add(new_asset)
    session.commit()

    new_token = Token(symbol=symbol, asset_id=new_asset.id)
    session.add(new_token)
    session.commit()

    return new_asset, new_token

# Example function to transfer ownership
def transfer_ownership(session, from_user_id, to_user_id, token_id, amount):
    ownership = session.query(Ownership).filter_by(user_id=from_user_id, token_id=token_id).first()
    if ownership and ownership.amount >= amount:
        ownership.amount -= amount
        session.commit()

        new_ownership = Ownership(user_id=to_user_id, token_id=token_id, amount=amount)
        session.add(new_ownership)
        session.commit()
        return True
    return False
