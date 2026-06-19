from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def run_test():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    print("Initializing webdriver...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()

    judges_to_test = [
        "Ivey",
        "Jeanne Parker",
        "Paul A. Motz",
        "Paul L. LePak",
        "Wade Faulkner",
        "Gregory Johnson",
        "Larry Wilkey"
    ]

    try:
        wait = WebDriverWait(driver, 10)
        
        for judge in judges_to_test:
            print(f"\n--- Testing Judge: {judge} ---")
            
            try:
                # Start at home page to simulate full navigation
                driver.get("http://localhost:4000/")
                
                # 1. Click on Judicial Officers in the main menu
                judicial_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Judicial Officers")))
                driver.execute_script("arguments[0].click();", judicial_link)
                
                # Wait for Candidates directory page to load
                wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Bell County Judicial Officers')]")))
                
                # 2. Click on the target Judge
                judge_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, judge)))
                driver.execute_script("arguments[0].click();", judge_link)
                
                # 3. Verify Case Load & Decision Summary exists
                heading = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Case Load & Decision Summary')]")))
                print(f"Verified heading: {heading.text}")
                
                # 4. Verify table and Plaintiff Success Rate column exists
                table_cell = driver.find_element(By.XPATH, "//th[contains(text(), 'Plaintiff Success Rate')]")
                print(f"Verified table header: {table_cell.text}")
                
                # 5. Get all row data to show it's populated
                rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
                print(f"Found {len(rows)} data rows in the table.")
                for i, row in enumerate(rows):
                    print(f"  Row {i+1}: {row.text}")
            except Exception as e:
                print(f"  [ERROR] Failed to verify {judge}: {str(e)}")
                # We do not re-raise so we can test the rest

        print("\nFinished verifying judges.")

    except Exception as e:
        print(f"\nTest failed on {judge}: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    run_test()
