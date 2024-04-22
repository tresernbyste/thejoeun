from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect
from lang.models import Question

bp = Blueprint('main',__name__, url_prefix='/')


@bp.route('/')
def hello_pybo():
    return redirect(url_for('lang._main'))


@bp.route('/main')
def index():
    return redirect(url_for('question._list'))