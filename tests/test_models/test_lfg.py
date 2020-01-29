import pytest

from WeddingWebsite.models import LFG


@pytest.fixture
def lfg():
    return LFG(
        "Owner_id",
        "Owner_name",
        ["Member1", "Member2", "Member3"],
        6,
        "Info Blob",
        "HOTEL",
    )


@pytest.mark.no_mongo_db
class TestInit:
    def test_valid_init(self):
        lfg = LFG(
            "Owner_id",
            "Owner_name",
            ["Member1", "Member2", "Member3"],
            6,
            "Info Blob",
            "HOTEL",
        )
        assert lfg.owner_id == "Owner_id"
        assert lfg.owner_name == "Owner_name"
        assert lfg.members == ["Member1", "Member2", "Member3"]
        assert lfg.max_members == 6
        assert lfg.info == "Info Blob"
        assert lfg.group_type == "HOTEL"

    def test_too_many_members(self):
        with pytest.raises(ValueError) as excinfo:
            lfg = LFG(
                "Owner",
                "Owner name",
                ["Member1", "Member2", "Member3"],
                2,
                "Info Blob",
                "HOTEL",
            )
        assert f"LFG has more members than allowed!" == str(excinfo.value)


@pytest.mark.no_mongo_db
class TestFull:
    def test_less_than(self, lfg):
        assert not lfg.full

    def test_more_than(self, lfg):
        lfg.max_members = 2
        with pytest.raises(ValueError) as excinfo:
            lfg.full
        assert f"LFG has more members than allowed!" == str(excinfo.value)

    def test_equal_to(self, lfg):
        lfg.max_members = 4
        assert lfg.full


@pytest.mark.no_mongo_db
class TestTotalMembers:
    def test_empty_members(self, lfg):
        lfg.members = []
        assert lfg.total_members == 1

    def test_with_members(self, lfg):
        assert lfg.total_members == 4


@pytest.mark.no_mongo_db
class TestStr:
    def test_empty_members(self, lfg):
        lfg.members = []
        assert "LFG is owned by Owner_name and has 1/6 members" == str(lfg)

    def test_with_members(self, lfg):
        "LFG is owned by Owner_name and has 4/6 members" == str(lfg)


class TestDBInteractions:
    def test_add_to_db(self, lfg, mongo_db):
        result = lfg.add_to_collection(mongo_db.lfgs)
        assert result.acknowledged
        assert result.inserted_id == lfg._id
        assert lfg._id is not None

    def test_get_from_db(self, lfg, mongo_db):
        lfg.add_to_collection(mongo_db.lfgs)
        lfg2 = LFG(**mongo_db.lfgs.find_one({"_id": lfg._id}))
        assert lfg == lfg2

    def test_update_db(self, lfg, mongo_db):
        lfg.add_to_collection(mongo_db.lfgs)
        lfg.max_members = 15
        assert lfg.update_collection(mongo_db.lfgs)

        lfg2 = LFG(**mongo_db.lfgs.find_one({"_id": lfg._id}))
        assert lfg == lfg2
