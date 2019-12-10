from WeddingWebsite.models import Guest
import pytest
import werkzeug

def test_hash_autouse():
    g = Guest(0, 'username', 'password', 'name', 'email')
    assert g.password == '123456'