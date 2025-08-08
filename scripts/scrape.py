import re
import requests
import time
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from urllib.parse import quote

# --- Configuration ---
# The base URL is needed to construct full links from the relative ones in the file.
BASE_URL = "https://hf-foodpro.austin.utexas.edu/foodpro/"
# List of main menu pages to scrape, now including the meal time name

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

# --- Stage 1: Function to get all meal links and their categories from a menu page ---
def get_meal_info_from_menu(menu_html_content):
    """
    Parses the main menu HTML to find all links to individual meal pages
    and determines their category (food_type) and if they are a salad topping.
    
    Args:
        menu_html_content (str): The HTML content of the main menu page.

    Returns:
        list: A list of dictionaries, each containing the 'url', 'is_salad_topping', and 'food_type'.
    """
    soup = BeautifulSoup(menu_html_content, 'html.parser')
    meal_info_list = []
    
    # Find the main content cell that contains all the menu tables.
    main_content_cell = soup.select_one('td[width="84%"][valign="top"]')
    if not main_content_cell:
        return [] # No main content area found

    # Find all table rows within this main content area.
    menu_rows = main_content_cell.find_all("tr")
    
    current_food_type = "Uncategorized"
    is_salad_bar_section = False
    for row in menu_rows:
        # Check if this row is a category header
        category_tag = row.find('div', class_='longmenucolmenucat')
        if category_tag:
            category_text = category_tag.get_text(strip=True)
            # Clean up the category text
            current_food_type = category_text.replace('--', '').strip()
            is_salad_bar_section = "salad bar" in current_food_type.lower()
            continue # Move to the next row
            
        # Check if this row is a food item
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
    """
    Finds a nutrient by its label text and extracts its value.
    This version is robust to handle tricky HTML and text formatting.
    
    Args:
        soup: The BeautifulSoup object.
        label_text: The text label of the nutrient to find (e.g., "Total Fat").
        
    Returns:
        The nutrient value as a string, or "Not found" if it's not present.
    """
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
        
        # Updated regex to correctly capture the number without leading punctuation.
        match = re.search(r'(\d+(?:\.\d+)?)\s*(g|mg|mcg)', full_text, re.IGNORECASE)
        
        if match:
            return f"{match.group(1)}{match.group(2)}"
            
        return "Not found"
    except AttributeError:
        return "Not found"

def parse_nutrition_page(html_content):
    """
    Takes the HTML content of a single item's nutrition page and extracts all data.
    
    Args:
        html_content (str): The HTML of the nutrition label page.
        
    Returns:
        dict: A dictionary containing all the parsed nutritional data.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    nutrition_data = {}

    # Extract all the data points using the logic we built before
    item_name_tag = soup.find('div', class_='labelrecipe')
    if not item_name_tag: return None # This indicates a bad page, skip it
    nutrition_data['item_name'] = item_name_tag.get_text(strip=True)
    
    serving_size_tag = soup.find('div', class_='nutfactsservsize', string=re.compile("Serving size"))
    if serving_size_tag and serving_size_tag.find_next_sibling('div'):
        nutrition_data['serving_size'] = serving_size_tag.find_next_sibling('div').get_text(strip=True)
    else:
        nutrition_data['serving_size'] = "Not found"
        
    calories_tag = soup.find('td', class_='nutfactscaloriesval')
    nutrition_data['calories'] = calories_tag.get_text(strip=True) if calories_tag else "Not found"

    # Use the helper function for the rest of the nutrients
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

    ingredients_tag = soup.find('span', class_='labelingredientsvalue')
    # nutrition_data['ingredients'] = ingredients_tag.get_text(strip=True).replace('\n', ' ') if ingredients_tag else "Not found"

    allergens_tag = soup.find('span', class_='labelallergensvalue')
    # nutrition_data['allergens'] = allergens_tag.get_text(strip=True) if allergens_tag else "Not found"
    
    return nutrition_data

# --- Main execution block ---
if __name__ == "__main__":
    
    # This dictionary will use the unique recipe number as a key to group items
    all_meal_info = {}
    
    # Use a session object for efficiency
    with requests.Session() as session:
        # --- Stage 1: Get all links from all menu URLs ---
        print("--- Stage 1: Fetching all meal links from menu pages ---")
        for menu in MENU_URLS:
            menu_name = menu["name"]
            menu_url = menu["url"]
            try:
                print(f"Fetching {menu_name} menu page: {menu_url}")
                headers = {'User-Agent': 'My Menu Scraper Bot 1.0'}
                response = session.get(menu_url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # Get the links and their category info from this menu page
                info_from_page = get_meal_info_from_menu(response.text)
                
                # Use the recipe number as the unique key to correctly group items
                for item_info in info_from_page:
                    url = item_info["url"]
                    # Extract the RecNumAndPort as the unique identifier
                    match = re.search(r'RecNumAndPort=([^&]+)', url)
                    if not match:
                        continue # Skip if the URL format is unexpected
                    
                    recipe_id = match.group(1)

                    if recipe_id not in all_meal_info:
                        # If we haven't seen this recipe before, create a new entry
                        all_meal_info[recipe_id] = {
                            "url": url, # Store the full URL to scrape later
                            "meal_times": [menu_name],
                            "is_salad_topping": item_info["is_salad_topping"],
                            "food_type": item_info["food_type"]
                        }
                    else:
                        # If we have seen this recipe, just update its metadata
                        if menu_name not in all_meal_info[recipe_id]["meal_times"]:
                            all_meal_info[recipe_id]["meal_times"].append(menu_name)
                        if item_info["is_salad_topping"]:
                            all_meal_info[recipe_id]["is_salad_topping"] = True
                        # Update food type if it's more specific than "Uncategorized"
                        if all_meal_info[recipe_id]["food_type"] == "Uncategorized":
                             all_meal_info[recipe_id]["food_type"] = item_info["food_type"]
                
                print(f"Found {len(info_from_page)} item instances on this page.")
                time.sleep(0.1) # Be polite

            except requests.exceptions.RequestException as e:
                print(f"Could not fetch menu page {menu_url}. Error: {e}")

        
        if not all_meal_info:
            print("\nCould not find any meal links to scrape. Exiting.")
            exit()
        
        print(f"\n--- Total unique food items found across all menus: {len(all_meal_info)} ---")
        
        # --- Stage 2: Scrape each individual link ---
        print(f"\n--- Stage 2: Starting to scrape {len(all_meal_info)} unique item pages ---")
        all_menu_data = []
        
        # Iterate through the dictionary to get the URL and its metadata
        for i, (recipe_id, metadata) in enumerate(all_meal_info.items()):
            url = metadata['url']
            try:
                # Be a good web citizen: set a user agent
                headers = {'User-Agent': 'My Menu Scraper Bot 1.0'}
                response = session.get(url, headers=headers, timeout=10)
                response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
                
                # Parse the content of the meal page
                item_data = parse_nutrition_page(response.text)
                if item_data: # Check if parsing was successful
                    # Add the metadata we collected in stage 1
                    item_data['meal_times'] = metadata['meal_times']
                    item_data['is_salad_topping'] = metadata['is_salad_topping']
                    item_data['food_type'] = metadata['food_type']
                    # item_data['source_url'] = url # Add the source URL for reference
                    all_menu_data.append(item_data)
                    
                    print(f"  ({i+1}/{len(all_meal_info)}) Successfully scraped: {item_data.get('item_name', 'Unknown Item')}")
                else:
                    print(f"  ({i+1}/{len(all_meal_info)}) Skipped due to parsing error: {url}")


            except requests.exceptions.RequestException as e:
                print(f"  ({i+1}/{len(all_meal_info)}) Failed to fetch {url}: {e}")
            
            # IMPORTANT: Wait a second between requests to avoid overwhelming the server
            time.sleep(0.1)

    # --- Stage 3: Save all collected data to a file ---
    if all_menu_data:
        print(f"\n--- Stage 3: Scraping complete. Saving {len(all_menu_data)} items to '{OUTPUT_FILENAME}' ---")
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            json.dump(all_menu_data, f, indent=4, ensure_ascii=False)
        print("Done!")
    else:
        print("\nScraping finished, but no data was collected.")
