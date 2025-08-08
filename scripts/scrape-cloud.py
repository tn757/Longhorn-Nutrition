import re
import requests
import time
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
from datetime import datetime
from dotenv import load_dotenv
import os
from google.cloud import storage

# Load environment variables for GCS credentials
load_dotenv()

# --- Configuration ---
BASE_URL = "https://hf-foodpro.austin.utexas.edu/foodpro/"

# Get today's date in m/d/yyyy format (no leading zeros — Windows compatible)
today = datetime.now().strftime("%#m/%#d/%Y")

# URL-encode the date for use in the query string
encoded_date = quote(today)

MENU_URLS = [
    {
        "name": "Breakfast",
        "url": f"https://hf-foodpro.austin.utexas.edu/foodpro/longmenu.aspx?sName=University+Housing+and+Dining&locationNum=12&locationName=Jester+Dining%3a+J2+%26+JCL&naFlag=1&WeeksMenus=This+Week%27s+Menus&dtdate={encoded_date}&mealName=Breakfast"
    },
    {
        "name": "Lunch",
        "url": f"https://hf-foodpro.austin.utexas.edu/foodpro/longmenu.aspx?sName=University+Housing+and+Dining&locationNum=12&locationName=Jester+Dining%3a+J2+%26+JCL&naFlag=1&WeeksMenus=This+Week%27s+Menus&dtdate={encoded_date}&mealName=Lunch"
    },
    {
        "name": "Dinner",
        "url": f"https://hf-foodpro.austin.utexas.edu/foodpro/longmenu.aspx?sName=University+Housing+and+Dining&locationNum=12&locationName=Jester+Dining%3a+J2+%26+JCL&naFlag=1&WeeksMenus=This+Week%27s+Menus&dtdate={encoded_date}&mealName=Dinner"
    }
]
OUTPUT_FILENAME = "full_menu_nutrition.json"

# --- GCS Upload function ---
def upload_json_to_meals_bucket(local_json_path, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket("meals-bucket")
    blob = bucket.blob(destination_blob_name)

    with open(local_json_path, "r", encoding="utf-8") as f:
        json_data = f.read()

    blob.upload_from_string(json_data, content_type="application/json")
    print(f"Uploaded {local_json_path} to gs://meals-bucket/{destination_blob_name}")

# --- Stage 1: Function to get all meal links and their categories from a menu page ---
def get_meal_info_from_menu(menu_html_content):
    soup = BeautifulSoup(menu_html_content, 'html.parser')
    meal_info_list = []
    
    main_content_cell = soup.select_one('td[width="84%"][valign="top"]')
    if not main_content_cell:
        return []

    menu_rows = main_content_cell.find_all("tr")
    
    current_food_type = "Uncategorized"
    is_salad_bar_section = False
    for row in menu_rows:
        category_tag = row.find('div', class_='longmenucolmenucat')
        if category_tag:
            category_text = category_tag.get_text(strip=True)
            current_food_type = category_text.replace('--', '').strip()
            is_salad_bar_section = "salad bar" in current_food_type.lower()
            continue
            
        item_link_tag = row.select_one('div.longmenucoldispname a')
        if item_link_tag and 'href' in item_link_tag.attrs:
            full_url = urljoin(BASE_URL, item_link_tag['href'])
            meal_info_list.append({
                "url": full_url,
                "is_salad_topping": is_salad_bar_section,
                "food_type": current_food_type
            })
    return meal_info_list

# --- Stage 2: Functions to parse a single nutrition page ---
def get_nutrient(soup, label_text):
    try:
        nutrient_tag = soup.find(
            lambda tag: tag.name == 'span' 
            and label_text.lower() in tag.get_text().lower() 
            and tag.has_attr('class') 
            and 'nutfactstopnutrient' in tag['class']
        )
        
        if not nutrient_tag:
            return "Not found"
            
        full_text = nutrient_tag.get_text(strip=True).replace('\xa0', ' ')
        match = re.search(r'(\d+(?:\.\d+)?)\s*(g|mg|mcg)', full_text, re.IGNORECASE)
        
        if match:
            return f"{match.group(1)}{match.group(2)}"
            
        return "Not found"
    except AttributeError:
        return "Not found"

def parse_nutrition_page(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    nutrition_data = {}

    item_name_tag = soup.find('div', class_='labelrecipe')
    if not item_name_tag: 
        return None
    nutrition_data['item_name'] = item_name_tag.get_text(strip=True)
    
    serving_size_tag = soup.find('div', class_='nutfactsservsize', string=re.compile("Serving size"))
    if serving_size_tag and serving_size_tag.find_next_sibling('div'):
        nutrition_data['serving_size'] = serving_size_tag.find_next_sibling('div').get_text(strip=True)
    else:
        nutrition_data['serving_size'] = "Not found"
        
    calories_tag = soup.find('td', class_='nutfactscaloriesval')
    nutrition_data['calories'] = calories_tag.get_text(strip=True) if calories_tag else "Not found"

    nutrition_data['total_fat'] = get_nutrient(soup, 'Total Fat')
    nutrition_data['saturated_fat'] = get_nutrient(soup, 'Saturated Fat')
    nutrition_data['trans_fat'] = get_nutrient(soup, 'Trans Fat')
    nutrition_data['cholesterol'] = get_nutrient(soup, 'Cholesterol')
    nutrition_data['sodium'] = get_nutrient(soup, 'Sodium')
    nutrition_data['total_carbohydrate'] = get_nutrient(soup, 'Total Carbohydrate')
    nutrition_data['dietary_fiber'] = get_nutrient(soup, 'Dietary Fiber')
    nutrition_data['total_sugars'] = get_nutrient(soup, 'Total Sugars')
    nutrition_data['added_sugars'] = get_nutrient(soup, 'Added Sugars')
    nutrition_data['protein'] = get_nutrient(soup, 'Protein')
    nutrition_data['vitamin_d'] = get_nutrient(soup, 'Vitamin D')
    nutrition_data['calcium'] = get_nutrient(soup, 'Calcium')
    nutrition_data['iron'] = get_nutrient(soup, 'Iron')
    nutrition_data['potassium'] = get_nutrient(soup, 'Potassium')
    
    return nutrition_data

# --- Main execution block ---
if __name__ == "__main__":
    all_meal_info = {}
    
    with requests.Session() as session:
        print("--- Stage 1: Fetching all meal links from menu pages ---")
        for menu in MENU_URLS:
            menu_name = menu["name"]
            menu_url = menu["url"]
            try:
                print(f"Fetching {menu_name} menu page: {menu_url}")
                headers = {'User-Agent': 'My Menu Scraper Bot 1.0'}
                response = session.get(menu_url, headers=headers, timeout=10)
                response.raise_for_status()
                
                info_from_page = get_meal_info_from_menu(response.text)
                
                for item_info in info_from_page:
                    url = item_info["url"]
                    match = re.search(r'RecNumAndPort=([^&]+)', url)
                    if not match:
                        continue
                    recipe_id = match.group(1)

                    if recipe_id not in all_meal_info:
                        all_meal_info[recipe_id] = {
                            "url": url,
                            "meal_times": [menu_name],
                            "is_salad_topping": item_info["is_salad_topping"],
                            "food_type": item_info["food_type"]
                        }
                    else:
                        if menu_name not in all_meal_info[recipe_id]["meal_times"]:
                            all_meal_info[recipe_id]["meal_times"].append(menu_name)
                        if item_info["is_salad_topping"]:
                            all_meal_info[recipe_id]["is_salad_topping"] = True
                        if all_meal_info[recipe_id]["food_type"] == "Uncategorized":
                            all_meal_info[recipe_id]["food_type"] = item_info["food_type"]
                
                print(f"Found {len(info_from_page)} item instances on this page.")
                time.sleep(0.1)

            except requests.exceptions.RequestException as e:
                print(f"Could not fetch menu page {menu_url}. Error: {e}")

        if not all_meal_info:
            print("\nCould not find any meal links to scrape. Exiting.")
            exit()
        
        print(f"\n--- Total unique food items found across all menus: {len(all_meal_info)} ---")
        
        print(f"\n--- Stage 2: Starting to scrape {len(all_meal_info)} unique item pages ---")
        all_menu_data = []
        
        for i, (recipe_id, metadata) in enumerate(all_meal_info.items()):
            url = metadata['url']
            try:
                headers = {'User-Agent': 'My Menu Scraper Bot 1.0'}
                response = session.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                item_data = parse_nutrition_page(response.text)
                if item_data:
                    item_data['meal_times'] = metadata['meal_times']
                    item_data['is_salad_topping'] = metadata['is_salad_topping']
                    item_data['food_type'] = metadata['food_type']
                    all_menu_data.append(item_data)
                    
                    print(f"  ({i+1}/{len(all_meal_info)}) Successfully scraped: {item_data.get('item_name', 'Unknown Item')}")
                else:
                    print(f"  ({i+1}/{len(all_meal_info)}) Skipped due to parsing error: {url}")

            except requests.exceptions.RequestException as e:
                print(f"  ({i+1}/{len(all_meal_info)}) Failed to fetch {url}: {e}")
            
            time.sleep(0.1)

    if all_menu_data:
        print(f"\n--- Stage 3: Scraping complete. Saving {len(all_menu_data)} items to '{OUTPUT_FILENAME}' ---")
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            json.dump(all_menu_data, f, indent=4, ensure_ascii=False)
        print("Local JSON file saved.")

        destination_blob_name = "menu.json"
        upload_json_to_meals_bucket(OUTPUT_FILENAME, destination_blob_name)
    else:
        print("\nScraping finished, but no data was collected.")
