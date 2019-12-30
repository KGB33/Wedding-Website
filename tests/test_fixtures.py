from WeddingWebsite.models import Guest
import pytest
import werkzeug

from conftest import check_list_contents


def test_hash_autouse():
    g = Guest(0, "username", "password", "name", "email")
    assert g.password == "123456"


class TestCheckListContents:
    def test_diff_lens(self):
        l1 = [1, 2, 3]
        l2 = [1, 2, 3, 4]
        assert not check_list_contents(l1, l2)

    def test_same_lists(self):
        l = [1, 2, 3]
        assert check_list_contents(l, l)

    def test_same_lengths_diff_content(self):
        l1 = [1, 2, 3]
        l2 = ["one", "two", "three"]
        assert not check_list_contents(l1, l2)

    def same_lists_diff_orders(self):
        l1 = [1, 2, 3]
        l2 = [2, 1, 3]
        assert check_list_contents(l1, l2)
