
from app import app, login, dao
from flask import Flask, render_template, redirect, request, url_for, session, jsonify
from flask_login import login_user, login_required
from app.models import *
import hashlib
from twilio.rest import Client
from datetime import datetime



@app.route("/")
def index():
    products = dao.read_products()

    return render_template("index.html", products=products)


@app.route("/view-detail/<int:product_id>")
def view_detail(product_id=None):
    # products = dao.read_products()
    sales = dao.read_sale(product_id)
    colors = dao.read_colors(product_id)
    images = dao.read_images(product_id)



    product = Product.query.filter(Product.id == product_id).first()

    cate = product.category_id
    print(cate)

    products = Product.query.filter(Product.category_id == cate).all()
    print(products)

    return render_template("view_detail.html", product=product, sales=sales, products=products, colors=colors,
                           images=images)


@app.route("/buy-product/<int:product_id>", methods=["get", "post"])
def buy_product(product_id=None):
    colors = dao.read_colors(product_id)
    product = Product.query.filter(Product.id == product_id).first()
    msg = ''
    if request.method == 'POST':
        product_id = request.form.get("product_id")
        product_name = request.form.get("product_name")
        date1 = request.form.get("date")
        date = datetime.fromisoformat(date1)
        print(date)
        quantity = request.form.get("quantity")
        price = request.form.get("price")
        image1 = request.form.get("image1")
        sum1 = request.form.get("sum")
        sum = float(sum1)
        print(sum)
        color = request.form.get("color")
        name = request.form.get("name")
        phone = request.form.get("phone")
        address = request.form.get("address")
        email = request.form.get("email")

        p1 = phone[1::]
        print(p1)
        p2 = "+84" + p1
        print(p2)
        if dao.add_customer(name=name, phone=phone, address=address, email=email):
            customer = Customer.query.filter(Customer.email == email).first()
            customer_id = customer.id
            if dao.add_salesbill(product_id=product_id, customer_id=customer_id, date=date, quantity=quantity, sum=sum,
                                 color=color):
                client = Client("AC5917d4c3e863d0c29818705fa95d2f57", "e7ad066f84558e077a89f6795793e340")
                client.messages.create(to=p2,
                                       from_="+12055063586",
                                       body="Cảm ơn quý khách đã mua hàng tại LAPTOPLT!"
                                            "Sản phẩm:" + product_name + ". Số lượng: " + quantity + ". Tổng tiền: "
                                            + sum1 + "vnđ . Xin vui lòng đợi trong giây lát chúng tôi sẽ gọi cho bạn để xác nhận!!!"
                                       )

                msg = "Bạn đã mua hàng thành công! Xin vui lòng kiểm tra tin nhắn!"

                return render_template("buy_product.html", product=product, msg=msg)

    return render_template("buy_product.html", product=product, colors=colors)


@app.route("/laptop", methods=["get", "post"])
def laptop():
    # products = dao.read_products()
    err = ''
    if request.method == 'POST':
        kw = request.form.get("kw")
        price = request.form.get("search_price")
        # brand = request.form.get("search_brand")
        # print(brand)

        if price == "Dưới 10 triệu":
            from_price = 1.0
            to_price = 10000000.0
        elif price == "Từ 10 - 20 triệu":
            from_price = 10000000.0
            to_price = 20000000.0
        elif price == "Trên 20 triệu":
            from_price = 20000000.0
            to_price = 100000000.0
        elif price == "Tất cả":
            from_price = 0.0
            to_price = 100000000.0

        products = dao.read_products(name=kw, from_price=from_price, to_price=to_price)
        print(products)
        if products == []:
            err = "Sản phẩm không tồn tại!"
            return render_template("laptop.html", products=dao.read_all_products(), err=err)
        else:
            msg = 'Kết quả tìm kiếm ' + " '" + kw + "'" + " , " + price
            return render_template("laptop.html", products=products, msg=msg)

    return render_template("laptop.html", products=dao.read_all_products())


@app.route("/repair")
def repair():
    return render_template("repair.html")


@login.user_loader
def user_load(admin_id):
    return Admin.query.get(admin_id)


@app.route("/logout")
def logout():
    logout_user()
    session.pop('logged_in', None)
    return redirect(url_for("index"))


@app.route("/login", methods=["post", "get"])
def login():
    err_msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())

        user = Admin.query.filter(Admin.username == username.strip(), Admin.password == password).first()
        if user:
            session['logged_in'] = True
            login_user(user)
            return redirect(url_for("admin_page"))
        else:
            err_msg = "Username hoặc password không đúng! Vui lòng nhập lại!"
    return render_template("admin/login.html", err_msg=err_msg)


@app.route("/admin")
def admin_page():
    quan = dao.read_all_quantity()
    print(quan)
    cus = dao.read_customers()
    print(cus)
    return render_template("admin/index.html", all_quan=quan, cus=cus)


if __name__ == "__main__":
    app.run(debug=True)
