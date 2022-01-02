from flask import  request, render_template, session, flash, Blueprint
import tool

login_bp = Blueprint('login_bp',__name__)

@login_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return '你已登录 <a href="/%s">%s</a>。 登出点击<a href="/logout">这里</a>。' % (session['username'], session['username'])
    elif request.method == 'POST':
        # check database and verify user
        username = request.form['username']
        password = request.form['password']
        verified = tool.verify_user(username, password)
        if verified:
            session['logged_in'] = True
            session[username] = username
            session['username'] = username
            user_expiry_date = tool.get_expiry_date(username)
            session['expiry_date'] = user_expiry_date
            session['articleID'] = None
            return tool.redirect(tool.url_for('user_bp.userpage', username=username))
        else:
            return '无法通过验证。'