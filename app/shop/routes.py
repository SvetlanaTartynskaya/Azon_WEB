from flask import request, render_template, abort, redirect, url_for
from flask_login import current_user, login_required

import base64

from app.models import Item, Shop
from app import db
from app.utils.allowed_file import allowed_file
from . import module
from .forms import ShopRegisterForm, ShopChangeInfoForm


# Регистрация нового магазина
@module.route('/register', methods=['POST', 'GET'])
@login_required
def register():
    form = ShopRegisterForm()
    if form.validate_on_submit():
        if Shop.query.filter_by(name=form.name.data).first():
            return render_template('shop/shop-register.html', title='Регистрация', form=form,
                                   message='Магазин с таким названием уже существует')
        img_file = request.files['img']
        if img_file and allowed_file(img_file.filename):  # проверка, что файл является фото
            img_binary = img_file.read()
            shop = Shop(
                name=form.name.data,
                about=form.about.data,
                img=img_binary,
                owner_id=current_user.id,
                contact=current_user.email
            )
            db.session.add(shop)
            db.session.commit()
            return redirect('/')
        else:
            return render_template('shop/shop-register.html',
                                   title='Регистрация магазина',
                                   message='Недопустимое расширение файла изображения. Разрешены только PNG, JPG и JPEG'
                                   , form=form)
    return render_template('shop/shop-register.html', title='Регистрация магазина', form=form)


# Профиль магазина
@module.route('/profile/<int:id>')
def shop_profile(id):
    shop = Shop.query.filter_by(id=id).first()
    items = Item.query.filter_by(seller_id=id).all()

    # Преобразуем бинарные данные логотипа в base64
    logo_data = base64.b64encode(shop.img).decode('utf-8')
    for item in items:
        item.logo_data = base64.b64encode(item.img).decode('utf-8') if item.img else None

    return render_template('shop/shop-profile.html', shop=shop, items=items, title=f'Профиль магазина "{shop.name}"',
                           logo_data=logo_data)


# Редактирование данных о магазине
@module.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def shop_info_change(id: int):
    form = ShopChangeInfoForm()
    if request.method == 'GET':
        shop = Shop.query.filter_by(id=id, owner_id=current_user.id).first()

        # Преобразуем бинарные данные логотипа в base64
        logo_data = base64.b64encode(shop.img).decode('utf-8')
        if shop:
            form.name.data = shop.name
            form.about.data = shop.about
            form.contact.data = shop.contact
            form.img.data = logo_data
        else:
            abort(404)
    if form.validate_on_submit():
        shop = Shop.query.filter_by(id=id, owner_id=current_user.id).first()
        img_file = request.files['img']
        if shop:
            if img_file and allowed_file(img_file.filename):  # проверка, что файл является фото
                img_binary = img_file.read()
                shop.name = form.name.data
                shop.about = form.about.data
                shop.contact = form.contact.data
                shop.img = img_binary
                db.session.commit()
                return redirect(f'shop_profile', id=id)
            else:
                return render_template('shop-change.html',
                                       title='Изменение данных',
                                       message='Недопустимое расширение файла изображения. Разрешены только '
                                               'PNG, JPG и JPEG'
                                       , form=form)

        else:
            abort(404)

    return render_template('shop/shop-info-change.html', title='Изменение данных', form=form)
