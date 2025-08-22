from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
    
    page.goto("https://sandbox.qbo.intuit.com/")
    print("Going to quickbooks")
    
    page.fill("#iux-identifier-first-international-email-user-id-input", "marko.kuzmov@gmail.com")
    print("Typed in email")
    page.click("text=Sign in")
    print("Clicked sign in")
    
    page.wait_for_url("https://sandbox.qbo.intuit.com/app/homepage")
    
    page.goto("https://sandbox.qbo.intuit.com/app/reconcile")
    print("Went to reconcile")
    
    text = page.locator('[data-testid="navigate-summary-report"]').inner_text()
    print(text)
    
    browser.close()