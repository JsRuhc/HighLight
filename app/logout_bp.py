from flask import  request, redirect, render_template, session, flash, Blueprint
import tool

logout_bp = Blueprint('logout_bp',__name__)


@logout_bp.route("/logout", methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(tool.url_for('mainpage'))