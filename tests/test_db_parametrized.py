import pytest
import sqlite3

@pytest.mark.parametrize(
    "name, email",
    [
        ("Simple User", "simple@example.com"),
        ("User With Space", "space_test@example.com"),
        ("O'Connor", "quotes_test@example.com"),
        ("Иван Петров", "cyrillic_test@example.com"),
        ("!#$%&*+-/=?^_`{|}~", "symbols@example.com"),
    ],
    ids=[
        "basic_latin",
        "name_with_spaces",
        "sql_injection_risk_single_quote",
        "unicode_cyrillic",
        "special_characters",
    ],
)
def test_user_persistence_parametrized(db, name, email):
    """Verify that different characters and formats are safely saved and read."""
    # 1. Insert parameterized data
    db.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (name, email),
    )

    # 2. Retrieve the record
    saved_user = db.fetch_one(
        "SELECT * FROM users WHERE email = ?",
        (email,),
    )

    # 3. Assertions
    assert saved_user is not None
    assert saved_user["name"] == name
    assert saved_user["email"] == email

def test_duplicate_email_raises_error(db):
    """Verify that UNIQUE constraint triggers IntegrityError on duplicates."""
    email = "unique_user@example.com"

    # 1. First insert - must succeed
    db.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        ("First User", email),
    )

    # 2. Second insert with identical email - must fail
    with pytest.raises(sqlite3.IntegrityError):
        db.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            ("Second User", email),
        )