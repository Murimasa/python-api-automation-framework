
def test_user_and_order_flow(db):
    """Verify writing, reading, and joining data using our custom database client."""
    # 1. Insert user
    db.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        ("Bob", "bob@example.com")
    )

    # 2. Verify user exists and retrieve their ID
    user = db.fetch_one("SELECT * FROM users WHERE email = ?", ("bob@example.com",))
    assert user is not None
    assert user["name"] == "Bob"

    # 3. Insert order using Bob's ID
    db.execute(
        "INSERT INTO orders (user_id, item_title, amount) VALUES (?, ?, ?)",
        (user["id"], "Gaming Headset", 89.50)
    )

    # 4. Fetch linked data via JOIN
    query = """
        SELECT users.name, orders.item_title, orders.amount
        FROM orders
        JOIN users ON orders.user_id = users.id
        WHERE orders.user_id = ?
    """
    order_data = db.fetch_one(query, (user["id"],))

    # 5. Assertions
    assert order_data is not None
    assert order_data["name"] == "Bob"
    assert order_data["item_title"] == "Gaming Headset"
    assert order_data["amount"] == 89.50