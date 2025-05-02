from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

# *Initialize WebDriver*
driver = webdriver.Chrome()
driver.get("https://services.gst.gov.in/services/login")
driver.maximize_window()

# *Wait for elements*
wait = WebDriverWait(driver, 20)

# *Enter login details*
username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
username_field.send_keys("YOUR LOGIN ID")  # Replace with actual username

password_field = driver.find_element(By.ID, "user_pass")
password_field.send_keys("YOUR PASSWORD")  # Replace with actual password

login_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary')]")))

time.sleep(8)  # Wait for CAPTCHA entry

# *Click Login Button*
driver.execute_script("arguments[0].click();", login_button)
print("Clicked Login button using JavaScript.")

# *Wait for page load*
time.sleep(5)

# *Handle Modal Popup if it appears*
try:
    print("Waiting for modal popup...")
    modal = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "modal-content")))
    time.sleep(2)  # Ensure modal is fully loaded
    print("Modal detected!")

    # *Click "No-Remind me later"*
    no_button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[@class='btn btn-primary'])[2]")))
    no_button.click()
    time.sleep(2)  # Allow modal to close

except Exception:
    print("No modal detected, proceeding.")

# *Function to navigate to Returns Dashboard*
def open_returns_dashboard():
    services_menu = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Services")))
    services_menu.click()
    time.sleep(2)

    returns_menu = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Returns")))
    returns_menu.click()
    time.sleep(2)

    returns_dashboard = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Returns Dashboard")))
    returns_dashboard.click()
    time.sleep(5)

# Start process
selected_financial_year = "2024-25"  # Change as needed

# *Loop through quarters & months*
open_returns_dashboard()  # First-time navigation

fin_year_dropdown = wait.until(EC.presence_of_element_located((By.NAME, "fin")))
fin_year_select = Select(fin_year_dropdown)
fin_year_select.select_by_visible_text(selected_financial_year)
time.sleep(2)

quarter_available = False
try:
    quarter_dropdown = wait.until(EC.presence_of_element_located((By.NAME, "quarter")))
    quarter_select = Select(quarter_dropdown)
    quarter_options = [opt.text for opt in quarter_select.options]
    quarter_available = True
except:
    quarter_options = [None]

for quarter in quarter_options:
    open_returns_dashboard()  # <- Ensure fresh dashboard each time

    # Re-select FY
    fin_year_select = Select(wait.until(EC.presence_of_element_located((By.NAME, "fin"))))
    fin_year_select.select_by_visible_text(selected_financial_year)
    time.sleep(2)

    # Re-initialize quarter dropdown
    if quarter_available and quarter:
        quarter_dropdown = wait.until(EC.presence_of_element_located((By.NAME, "quarter")))
        quarter_select = Select(quarter_dropdown)
        quarter_select.select_by_visible_text(quarter)
        time.sleep(2)

    # Now proceed with month loop

    try:
        month_dropdown = wait.until(EC.presence_of_element_located((By.NAME, "mon")))
        month_select = Select(month_dropdown)
        month_options = [opt.text for opt in month_select.options]
    except:
        month_options = []

    print(f"Updated month options for {selected_financial_year}, {quarter}: {month_options}")

    for month in month_options:
        # *Reopen Returns Dashboard for every month*
        open_returns_dashboard()

        # *Select FY & Quarter again*
        fin_year_select = Select(wait.until(EC.presence_of_element_located((By.NAME, "fin"))))
        fin_year_select.select_by_visible_text(selected_financial_year)
        time.sleep(2)

        if quarter_available:
            quarter_select = Select(wait.until(EC.presence_of_element_located((By.NAME, "quarter"))))
            quarter_select.select_by_visible_text(quarter)
            time.sleep(2)

        # *Select Month*
        month_select = Select(wait.until(EC.presence_of_element_located((By.NAME, "mon"))))
        month_select.select_by_visible_text(month)
        time.sleep(2)

        # *Click Search Button*
        search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        search_button.click()
        print(f"Searching for: Financial Year {selected_financial_year}, Quarter {quarter}, Month {month}")
        time.sleep(3)

        # *Locate GSTR-1 "View" Button & Click*
        try:
            gstr1_view_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'VIEW')]")))
            driver.execute_script("arguments[0].click();", gstr1_view_button)
            print("Clicked on 'VIEW' button for GSTR-1.")
            time.sleep(5)

            # *Click "View Summary" Button*
            try:
                view_summary_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'VIEW SUMMARY')]")))
                driver.execute_script("arguments[0].click();", view_summary_button)
                print("Clicked on 'VIEW SUMMARY' button.")
                time.sleep(5)

                try:
                    # Locate the button using XPath
                    download_pdf_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@data-ng-click, 'genratepdfNew')]")))
    
                    # Ensure the button is visible and clickable
                    driver.execute_script("arguments[0].scrollIntoView();", download_pdf_button)
                    time.sleep(2)  # Give time for it to be scrolled into view

                    # Click the button using JavaScript
                    driver.execute_script("arguments[0].click();", download_pdf_button)
    
                    print("Clicked on 'DOWNLOAD (PDF)' button successfully.")
                    time.sleep(5)
                
                except:
                    print(f"No 'DOWNLOAD (PDF)' button for {month}")

            except:
                print(f"No 'View Summary' for {month}")

            # *Go back to Dashboard*
            driver.execute_script("window.history.go(-2);")
            time.sleep(5)

        except:
            print(f"No GSTR-1 View option for {month}")

# Close WebDriver
driver.quit()
