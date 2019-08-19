from flaskr import app, db
from flask import render_template, render_template_string
from flask_user import login_required


@app.route('/')
def index():
    # return render_template('index.html')
    return render_template_string(
        '''
            {% block content %}
                <h2>Home page</h2>
                <p><a href={{ url_for('user.register') }}>Register</a></p>
                <p><a href={{ url_for('user.login') }}>Sign in</a></p>
                <p><a href={{ url_for('index') }}>Home page</a> (accessible to anyone)</p>
                <p><a href={{ url_for('member_page') }}>Member page</a> (login required)</p>
                <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
            {% endblock %}
        '''
    )


@app.route('/member')
@login_required
def member_page():
    return 'This is the members only page'


if __name__ == '__main__':
    app.run(debug=True)
