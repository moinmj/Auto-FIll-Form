import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from collections import defaultdict
import time



def get_label_from_tag(soup, input_tag):
    """
    Try to find label linked to input field
    """

    # Case 1: label with 'for' attribute
    if input_tag.get("id"):
        label_tag = soup.find("label", attrs={"for": input_tag.get("id")})
        if label_tag:
            return label_tag.text.strip()

    # Case 2: label wrapping input
    parent = input_tag.find_parent("label")
    if parent:
        return parent.text.strip()

    return None

def analyze_form(url: str):
    try:
        options = Options()
        options.add_argument("--headless")  # run in background

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        time.sleep(2)  # wait for JS to load

        inputs = driver.find_elements(By.XPATH, "//input | //textarea | //select")

        form_fields = []
        grouped_fields = defaultdict(list)

        for inp in inputs:
            field_type = inp.get_attribute("type") or inp.tag_name
            name = inp.get_attribute("name")
            field_id = inp.get_attribute("id")

            label = None

            # ✅ 1. Try label using "for"
            if field_id:
                try:
                    label_elem = driver.find_element(By.XPATH, f"//label[@for='{field_id}']")
                    label = label_elem.text
                except:
                    pass

            # ✅ 2. Try parent label
            if not label:
                try:
                    parent = inp.find_element(By.XPATH, "ancestor::label")
                    label = parent.text
                except:
                    pass

            # ✅ 3. Placeholder fallback
            if not label:
                label = inp.get_attribute("placeholder")

            # ✅ 4. Final fallback
            if not label:
                label = name

            # 🔥 HANDLE RADIO/CHECKBOX PROPERLY
            if field_type in ["radio", "checkbox"] and name:
                option_label = label
                grouped_fields[name].append(option_label)
                continue

            field = {
                "label": label,
                "type": field_type,
                "name": name,
                "id": field_id
            }

            # ✅ SELECT OPTIONS
            if inp.tag_name == "select":
                options = [opt.text for opt in inp.find_elements(By.TAG_NAME, "option")]
                field["options"] = options

            form_fields.append(field)

        # Add grouped fields
        for name, options in grouped_fields.items():
            form_fields.append({
                "label": name,
                "type": "radio/checkbox",
                "name": name,
                "options": options
            })

        driver.quit()
        return form_fields

    except Exception as e:
        return {"error": str(e)}