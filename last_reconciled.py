from playwright.sync_api import sync_playwright

def get_last_reconciled_dates(account_id_list):

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://sandbox.qbo.intuit.com/")
        print("Going to quickbooks")

        page.fill("#iux-identifier-first-international-email-user-id-input", "marko.kuzmov@gmail.com")
        print("Typed in email")
        page.click("text=Sign in")
        print("Clicked sign in")

        page.wait_for_url("https://sandbox.qbo.intuit.com/app/homepage")
        print("Loaded into homepage")

        date_list = dict()
        for id in account_id_list:
            page.goto(f"https://sandbox.qbo.intuit.com/app/reconcile?accountId={id}")
            
            a_tag = page.locator('[data-testid="navigate-summary-report"]')
            try:
                a_tag.wait_for(timeout=1500)
                print(f"found <a> tag in account id {id}")
                
                date = a_tag.inner_text()
                date = date.replace("Last statement ending date ", "").strip()
            except:
                date = "N/A"
                print(f"couldn't find date for account id {id}")

            date_list[f"{id}"] = date
            
        browser.close()
        
        return date_list
        

