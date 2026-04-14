from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def prepare_autofill_data(decisions, user_responses):
    """
    Merge system data + user responses into final form-ready payload
    """

    final_data = {}

    for item in decisions:
        field_name = item.get("field")
        form_name = item.get("original_label")  # for reference

        action = item.get("action")

        # If auto-filled
        if action == "auto_fill":
            final_data[field_name] = item.get("value")

        # If user provided input
        elif action == "ask_user":
            if field_name in user_responses:
                final_data[field_name] = user_responses[field_name]

        # Optional fields → skip or include if provided
        elif action == "optional":
            if field_name in user_responses:
                final_data[field_name] = user_responses[field_name]

    return final_data


def autofill_form(url, final_payload):

    # ✅ Auto-manage driver (NO manual download needed)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get(url)
    time.sleep(2)

    for field_name, value in final_payload.items():
        try:
            element = driver.find_element(By.NAME, field_name)

            tag = element.tag_name
            input_type = element.get_attribute("type")

            # 📝 Text inputs
            if tag == "input" and input_type in ["text", "email", "tel", "time"]:
                element.clear()
                element.send_keys(value)

            # 🔘 Radio buttons
            elif tag == "input" and input_type == "radio":
                options = driver.find_elements(By.NAME, field_name)
                for opt in options:
                    if opt.get_attribute("value").lower() == value.lower():
                        opt.click()
                        break

            # ☑️ Checkboxes
            elif tag == "input" and input_type == "checkbox":
                options = driver.find_elements(By.NAME, field_name)
                for opt in options:
                    if opt.get_attribute("value").lower() == value.lower():
                        opt.click()

            # 📋 Textarea
            elif tag == "textarea":
                element.clear()
                element.send_keys(value)

        except Exception as e:
            print(f"❌ Error for {field_name}: {e}")

    print("✅ Autofill completed")
    return driver