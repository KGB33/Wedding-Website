import pytest

from conftest import check_list_contents

from WeddingWebsite.models import LFG
from WeddingWebsite.exceptions import TooManyMembersError


@pytest.mark.no_mongo_db
class TestInit:
    def test_default_bool(self):
        lfg = LFG("c", ["m1", "m2", "m3"], 6)
        assert lfg.creator == "c"
        assert check_list_contents(lfg.members, ["c", "m1", "m2", "m3"])
        assert lfg.max_mebers == 6
        assert not lfg.full
        assert lfg.num_members == 4

    def test_starts_full(self):
        lfg = LFG("c", ["m1", "m2", "m3"], 4)
        assert lfg.creator == "c"
        assert check_list_contents(lfg.members, ["c", "m1", "m2", "m3"])
        assert lfg.max_mebers == 4
        assert lfg.full
        assert lfg.num_members == 4

    def test_starts_too_full(self):
        with pytest.raises(TooManyMembersError) as excinfo:
            lfg = LFG("c", ["m1", "m2", "m3"], 3)
        assert excinfo
