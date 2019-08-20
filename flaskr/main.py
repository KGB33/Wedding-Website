from flask import Blueprint



bp = Blueprint('main', __name__, url_prefix='')


@bp.route('/')
def index():
    # return render_template('index.html')
    return 'This is the Index page'


@bp.route('/member')
def member_page():
    return 'This is the members only page'
