def test_api_user_persisted_in_database(api_client, db):
    """Verify data fetched from API can be seeded and validated in the database."""
    # 1. Fetch real user from public API
    response = api_client.get("/users/1")
    assert response.status_code == 200
    api_user = response.json()

    # 2. Insert data received from API into our local database
    db.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (api_user["name"], api_user["email"])
    )

    # 3. Query the database to verify the record exists
    db_user = db.fetch_one(
        "SELECT * FROM users WHERE email = ?",
        (api_user["email"],)
    )

    # 4. Validate database integrity against API payload
    assert db_user is not None, "User record must exist in database"
    assert db_user["name"] == api_user["name"]
    assert db_user["email"] == api_user["email"]