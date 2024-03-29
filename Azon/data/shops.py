from .db_session import SqlAlchemyBase
import sqlalchemy as sa
import sqlalchemy.orm as orm


class Shop(SqlAlchemyBase):
    __tablename__ = 'shops'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False, unique=True)
    about = sa.Column(sa.String, nullable=True, default='Описание магазина')
    img = sa.Column(sa.LargeBinary, nullable=False)
    contact = sa.Column(sa.String, nullable=True)
    owner_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))

    items = orm.relationship('Item', back_populates='shop')
    user = orm.relationship('User')
