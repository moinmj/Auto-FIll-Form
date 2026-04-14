from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def fill_form(url, payload):
    try:
        options = Options()
        options.add_argument("--start-maximized")

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # Wait until page loads
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "input"))
        )

        filled_any = False  # 🔥 track success

        for field_name, value in payload.items():

            print("🔍 Filling:", field_name, value)

            element = None

            # Try locating element
            try:
                element = driver.find_element(By.NAME, field_name)
            except:
                try:
                    element = driver.find_element(By.ID, field_name)
                except:
                    pass

            if not element:
                print(f"❌ Field not found: {field_name}")
                continue

            tag = element.tag_name
            field_type = element.get_attribute("type")

            try:
                # TEXT INPUT
                if tag in ["input", "textarea"] and field_type not in ["radio", "checkbox"]:
                    element.clear()
                    element.send_keys(value)
                    filled_any = True

                # RADIO
                elif field_type == "radio":
                    radios = driver.find_elements(By.NAME, field_name)
                    for r in radios:
                        if value.lower() in (r.get_attribute("value") or "").lower():
                            r.click()
                            filled_any = True
                            break

                # CHECKBOX
                elif field_type == "checkbox":
                    checkboxes = driver.find_elements(By.NAME, field_name)
                    for cb in checkboxes:
                        if value.lower() in (cb.get_attribute("value") or "").lower():
                            cb.click()
                            filled_any = True

            except Exception as e:
                print(f"⚠️ Error filling {field_name}: {e}")

        if filled_any:
            print("✅ Form filled successfully!")
            return True
        else:
            print("❌ Nothing was filled")
            return False

    except Exception as e:
        print("❌ Critical Error:", e)
        return False