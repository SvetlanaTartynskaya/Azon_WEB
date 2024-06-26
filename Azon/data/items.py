from .db_session import SqlAlchemyBase
import sqlalchemy as sa
import sqlalchemy.orm as orm


class Item(SqlAlchemyBase):
    __tablename__ = 'items'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    price = sa.Column(sa.Integer, nullable=False)
    about = sa.Column(sa.String, nullable=False)
    img = sa.Column(sa.LargeBinary, nullable=False)
    category_id = sa.Column(sa.Integer, sa.ForeignKey("categories.id"), nullable=False)
    seller_id = sa.Column(sa.Integer, sa.ForeignKey("shops.id"))
    comments = sa.Column(sa.String, nullable=True)
    rating = sa.Column(sa.String, nullable=True, default="0;0;0")

    shop = orm.relationship('Shop')
    category = orm.relationship('Category', back_populates='items')
