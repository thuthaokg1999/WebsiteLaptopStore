from app import app, db
import os
import hashlib
from app.models import *


def read_sale(product_id):
    return SaleInfo.query.filter(SaleInfo.product_id == product_id).all()


def read_colors(product_id):
    return Color.query.filter(Color.product_id == product_id).all()


def read_images(product_id):
    return Image.query.filter(Image.product_id == product_id).all()


def read_product_by_id(product_id):
    return Product.query.get(product_id)


def read_salesbill():
    return SalesBill.query.all()


def read_all_products():
    return Product.query.all()


def read_customers():
    return Customer.query.all()


def read_products(name=None, from_price=None, to_price=None, brand=None, latest=True):
    products = read_all_products()

    if name:
        products = [p for p in products if p.name.lower().find(name.lower()) >= 0]
        # return products

    if from_price and to_price:
        products = [p for p in products if p.price > from_price and p.price < to_price]
        # return products

    return products


def add_customer(name, phone, address, email):
    try:
        new_customer = Customer(
            name=name,
            phone=phone,
            address=address,
            email=email,
        )
        db.session.add(new_customer)
        db.session.commit()
        return Customer.query.all()
    except Exception as ex:
        print(ex)
        return False


def add_salesbill(product_id, customer_id, date, quantity, sum, color):
    try:
        new_salesbill = SalesBill(
            product_id=product_id,
            customer_id=customer_id,
            date=date,
            quantity=quantity,
            sum=sum,
            color=color,
            status = "Đơn hàng chưa duyệt"
        )
        db.session.add(new_salesbill)
        db.session.commit()
        return SalesBill.query.all()
    except Exception as ex:
        print(ex)
        return False


def read_all_price():
    sumary = 0
    sb = read_salesbill()
    for s in sb:
        sumary = sumary + s.sum
    return sumary


def read_all_quantity():
    quantity = 0
    sb = read_salesbill()
    for s in sb:
        quantity = quantity + s.quantity
    return quantity


if __name__ == "__main__":
    # print(read_product_laptop("LAPTOP"))
    # print(read_laptop_type_dell())
    # print(read_laptop())
    # print(read_current_user())
    # print(read_sale(1))
    print(read_all_quantity())
    # print(read_quantity())
    # print(read_products())
