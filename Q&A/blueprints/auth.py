from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
from flask import request
import string
import random
from models import EmailCaptcahModel
from .forms import RegisterForm, LoginForm, PersonalUserForm
from models import UserModel
from werkzeug.security import generate_password_hash,check_password_hash



bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login",methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱不存在")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password,password):
                session['user_id'] = user.id
                return redirect("/")
            else:
                print("密码错误")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))

@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))

        else:
            print(form.errors)
            return redirect(url_for("auth.register"))

# 如果没有指定methods参数，默认为get


@bp.route("/captcha/email")
def get_email_captcha():
    email = request.args.get("email")
    source = string.digits*4
    captcha = random.sample(source, 4)
    captcha = "".join(captcha)
    message = Message(subject="郁金香注册验证码", recipients=[email], body=f"欢迎使用郁金香，您的验证码是：{captcha},请不要将验证码告诉别人")
    mail.send(message)

    email_captcha = EmailCaptcahModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()

    return jsonify({"code": 200, "message": "", "data": None})


@bp.route("/personal")
def personal():
    return render_template("personal.html")

# todo:账户信息修改功能