from playwright.sync_api import Page, expect


def test_first_browser_launch(page: Page):
    # 1. Open public website
    page.goto("https://example.com")

    # 2. Check header text
    expect(page.locator("h1")).to_have_text("Example Domain")

    # 3. Check page title
    assert page.title() == "Example Domain"