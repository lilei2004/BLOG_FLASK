import functools
from flask import Blueprint, render_template, request, redirect, url_for,session,flash,g
from werkzeug.security import check_password_hash, generate_password_hash
from RealProject import db
from ..models import User

bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
    static_folder="../static",
    template_folder="../templates",
)


@bp.before_app_request
def load_logged_in_user():
    # 每个请求之前都回去session中查看user_id来获取用户
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(int(user_id))


def login_required(view):
    # 限制必须登录才能访问的页面装饰器
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view




@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # 获取表单的值
        print(request.form.get("username"))
        username = request.form.get("username")
        password = request.form.get("password")

        error = None
        user = User.query.filter_by(username=username).first()
        if user is None:
            # 用户不存在,返回错误
            error = '用户不存在,请先去注册'
        elif not check_password_hash(user.password,password):
            error = '密码错误'
        
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect('/')
        flash(error)
    return render_template("login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # 获取表单的值
        print(request.form.get("username"))
        username = request.form.get("username")
        password = request.form.get("password")
        password1 = request.form.get("password1")
        user = User.query.filter_by(username=username).first()

        if password != password1:
            flash("两次密码输入不一致！")
            # return redirect(url_for("auth.register"))
        if user:
            flash("该用户已经存在请勿重复注册")
        else:
            # 添加一个用户的数据库
            u = User(username=username, password=generate_password_hash(password1))
            db.session.add(u)
            db.session.commit()

            # 自动登录
            session.clear()
            session['user_id'] = u.id
        return redirect('/')
    return render_template("register.html")


@bp.route('/logout')
def logout():
    # 注销
    session.clear()
    return redirect('/')


