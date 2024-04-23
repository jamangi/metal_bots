import pytest
import os
from metalbase.datastructs import DataBase

@pytest.fixture
def db():
    filename = "test_db.json"  # Use a temporary filename for testing
    db = DataBase(filename)
    yield db
    # Clean up after the test
    db.close()
    os.remove(filename)


def test_add_a_book(db):
    entry_id = 123456
    filename = "test_db.json"  # Use a temporary filename for testing
    db = DataBase(filename)

    # Create the entry
    db.create_entry(entry_id)

    # Add data to nested dictionaries
    db.add(entry_id, book_name="The Art of Seduction")
    db.add(entry_id, book_id=entry_id)
    db.add(entry_id, participants={})
    db.add(entry_id, "participants", id12345={})
    db.add(entry_id, "participants", "id12345", discord_id=12345, display_name="Haltise")
    db.add(entry_id, completion=0.30)

    # Verify the data structure
    assert db.data == {
        entry_id: {

                "book_name": "The Art of Seduction",
                "book_id": entry_id,
                "participants": {
                    "id12345": {"discord_id": 12345, "display_name": "Haltise"}
                },
                "completion": 0.30

        }
    }

def test_add_a_contract(db):
    entry_id = 123456
    filename = "test_db.json"  # Use a temporary filename for testing
    db = DataBase(filename)

    # Create the entry
    db.create_entry(entry_id)
    db.add(entry_id, contract_id=entry_id)
    db.add(entry_id, contract_name="Right To Justice")
    db.add(entry_id, contract_signed=False)
    db.add(entry_id, signatories={})
    db.add(entry_id, terms="All Signatories must adhere to the meka order when discussing things, or suffer a spanking.")
    db.add(entry_id, start_date=12345)
    db.add(entry_id, end_date=54321)
    db.add(entry_id, "signatories", id1={})
    db.add(entry_id, 'signatories', 'id1', display_name="Haltise", discord_id=123, signed=False)
    db.add(entry_id, 'signatories', 'id2', display_name="Berry", discord_id=1234, signed=True)

    assert db.data == {
        entry_id: {
            "contract_id": entry_id,
            "contract_name": "Right To Justice",
            "contract_signed": False,
            "signatories": {
                "id1": {
                    "display_name": "Haltise",
                    "discord_id": 123,
                    "signed": False
                },
                "id2": {
                    "display_name": "Berry",
                    "discord_id": 1234,
                    "signed": True
                }
            },
            "terms": "All Signatories must adhere to the meka order when discussing things, or suffer a spanking.",
            "start_date": 12345,
            "end_date": 54321
        }
    }
