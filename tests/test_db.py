import flask_mongoengine


def test_create_app(app):
    assert app.config['TESTING']
    assert flask_mongoengine.connection.get_db().name == 'testing'
    assert 2 == 3

