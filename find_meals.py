import json
import random
import re
from itertools import combinations, product

# --- Configuration & Nutritional Targets ---

# This file is the output from our previous scraping script
INPUT_FILENAME = "full_menu_nutrition.json" 

# Daily nutritional goals (approximations based on a 2000-calorie diet)
DV_TARGETS = {
    'calories': (1800, 2200), # Calorie range (min, max)
    'protein': 50,           # grams
    'total_fat': 78,         # grams (upper limit)
    'saturated_fat': 20,     # grams (upper limit)
    'total_carbohydrate': 275, # grams
    'dietary_fiber': 28,     # grams
    'sodium': 2300,          # mg (upper limit)
    'potassium': 4700,       # mg
    'calcium': 1300,         # mg
    'iron': 18,              # mg
    'vitamin_d': 20,         # mcg
    'cholesterol': 300,      # mg (upper limit)
    'added_sugars': 50,      # g (upper limit)
}

# Define which nutrients are hard constraints vs. soft targets for scoring
MACRO_CONSTRAINTS = {'calories', 'protein', 'total_fat', 'saturated_fat', 'sodium', 'cholesterol', 'added_sugars'}
MICRO_TARGETS = {'dietary_fiber', 'potassium', 'calcium', 'iron', 'vitamin_d'}


# --- Data Cleaning and Preparation ---

def clean_nutrient_value(value_str):
    """
    Converts a nutrient string (e.g., "6.4g", "164.9mg") into a numerical value.
    Handles different units by converting them to a base unit (g or mg).
    """
    if not isinstance(value_str, str) or value_str.lower() == 'not found':
        return 0.0

    # Use regex to find the number and the unit
    match = re.search(r'(\d+(?:\.\d+)?)', value_str)
    if not match:
        return 0.0
    
    value = float(match.group(1))
    
    # Standardize units
    if 'mcg' in value_str.lower():
        return value / 1000  # Convert mcg to mg
    return value

def is_value_reasonable(nutrient_key, value):
    """
    Checks if a nutrient value is a plausible amount for a single food item.
    This helps filter out data entry errors.
    """
    if nutrient_key in DV_TARGETS:
        if nutrient_key in ['total_fat', 'saturated_fat', 'sodium', 'cholesterol', 'added_sugars']:
            if value > DV_TARGETS[nutrient_key]:
                return False
        elif nutrient_key not in ['calories', 'total_carbohydrate']:
             if value > DV_TARGETS[nutrient_key] * 10:
                return False
    return True


def load_and_prepare_data(filename):
    """
    Loads the scraped JSON data, cleans it, and separates items into main dishes and toppings for each meal.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The input file '{filename}' was not found. Please run the scraper first.")
        return None

    cleaned_data = []
    for item in data:
        for key in DV_TARGETS:
            cleaned_value = clean_nutrient_value(item.get(key, "0"))
            if not is_value_reasonable(key, cleaned_value):
                print(f"Warning: Anomalous value detected for '{key}' in item '{item['item_name']}' ({cleaned_value}). Capping value.")
                item[key] = DV_TARGETS[key]
            else:
                item[key] = cleaned_value
        cleaned_data.append(item)

    # Separate items into meals and then into main dishes vs. toppings
    meals = {
        "Breakfast": {"main": [], "toppings": []},
        "Lunch": {"main": [], "toppings": []},
        "Dinner": {"main": [], "toppings": []}
    }
    
    # Handle the 'meal_times' list
    for item in cleaned_data:
        for meal_time in item.get('meal_times', []):
            if meal_time in meals:
                if item.get('is_salad_topping'):
                    meals[meal_time]["toppings"].append(item)
                else:
                    meals[meal_time]["main"].append(item)

    print("Data loaded and cleaned successfully.")
    for meal, categories in meals.items():
        print(f"- {meal}: {len(categories['main'])} main items, {len(categories['toppings'])} topping items.")
    return meals

# --- Meal Plan Generation & Scoring ---

def generate_random_meal(main_items, topping_items, num_main_range=(2, 3), num_toppings=2):
    """
    Generates a single random meal combo with toppings and variable servings.
    """
    # Check if there are enough items to choose from
    if len(topping_items) < num_toppings or len(main_items) < num_main_range[0]:
        return None

    num_main_items = random.randint(num_main_range[0], num_main_range[1])
    if len(main_items) < num_main_items: # Final check
        return None

    # Randomly select items
    selected_mains = random.sample(main_items, num_main_items)
    selected_toppings = random.sample(topping_items, num_toppings)
    
    full_meal_items = selected_mains + selected_toppings
    
    # Randomly assign 1 or 2 servings to each item
    meal_combo = tuple((item, random.choice([1, 2])) for item in full_meal_items)
    
    return meal_combo


def calculate_combo_nutrition(combo):
    """
    Calculates the total nutritional values for a combination of servings.
    'combo' is a tuple of (item, num_servings) tuples.
    """
    total_nutrition = {key: 0 for key in DV_TARGETS}
    for item, num_servings in combo:
        for key in DV_TARGETS:
            total_nutrition[key] += item[key] * num_servings
    return total_nutrition

def meets_macro_constraints(plan_nutrition):
    """
    Checks if a meal plan meets the hard macronutrient constraints.
    """
    min_cal, max_cal = DV_TARGETS['calories']
    if not (min_cal <= plan_nutrition['calories'] <= max_cal): return False
    if plan_nutrition['protein'] < DV_TARGETS['protein']: return False
    if plan_nutrition['total_fat'] > DV_TARGETS['total_fat']: return False
    if plan_nutrition['saturated_fat'] > DV_TARGETS['saturated_fat']: return False
    if plan_nutrition['sodium'] > DV_TARGETS['sodium']: return False
    if plan_nutrition['cholesterol'] > DV_TARGETS['cholesterol']: return False
    if plan_nutrition['added_sugars'] > DV_TARGETS['added_sugars']: return False
    return True

def calculate_micronutrient_score(plan_nutrition):
    """
    Calculates a score based on the squared error from micronutrient targets.
    A lower score is better.
    """
    score = 0
    for key in MICRO_TARGETS:
        actual = plan_nutrition.get(key, 0)
        target = DV_TARGETS.get(key, 1)
        if actual < target:
            error = (actual - target) / target 
            score += error ** 2
    return score

def print_meal_plan(plan, score):
    """Nicely prints a valid meal plan, its score, and its totals."""
    print("\n" + "="*50)
    print(f"🎉 MEAL PLAN FOUND (Score: {score:.4f}) 🎉")
    print("="*50)
    
    full_day_nutrition = {key: 0 for key in DV_TARGETS}

    for meal_type, combo in plan.items():
        meal_nutrition = calculate_combo_nutrition(combo)
        print(f"\n--- {meal_type.upper()} ({meal_nutrition['calories']:.0f} calories) ---")
        for item, num_servings in combo:
            serving_text = f" ({num_servings} servings)" if num_servings > 1 else ""
            item_calories = item['calories'] * num_servings
            topping_label = " [Topping]" if item.get('is_salad_topping') else ""
            print(f"  - {item['item_name']}{serving_text}{topping_label} ({item_calories:.0f} cal)")
        
        for key in full_day_nutrition:
            full_day_nutrition[key] += meal_nutrition[key]

    print("\n" + "-"*50)
    print("Full Day Nutritional Totals:")
    print(f"  - Calories: {full_day_nutrition['calories']:.1f} (Target: {DV_TARGETS['calories'][0]}-{DV_TARGETS['calories'][1]})")
    print(f"  - Protein: {full_day_nutrition['protein']:.1f}g (Target: >{DV_TARGETS['protein']}g)")
    print(f"  - Fat: {full_day_nutrition['total_fat']:.1f}g (Target: <{DV_TARGETS['total_fat']}g)")
    print(f"  - Added Sugars: {full_day_nutrition['added_sugars']:.1f}g (Target: <{DV_TARGETS['added_sugars']}g)")
    print("-" * 20)
    for key in MICRO_TARGETS:
        actual = full_day_nutrition[key]
        target = DV_TARGETS[key]
        print(f"  - {key.replace('_', ' ').title()}: {actual:.1f} (Target: >{target})")
    print("="*50 + "\n")


# --- Main Execution Block ---
if __name__ == "__main__":
    all_meals = load_and_prepare_data(INPUT_FILENAME)

    if all_meals:
        print("\nSearching for the best meal plans...")
        valid_plans = []
        search_attempts = 200000

        for _ in range(search_attempts):
            # Generate a random combo for each meal on the fly
            breakfast_combo = generate_random_meal(all_meals["Breakfast"]["main"], all_meals["Breakfast"]["toppings"])
            lunch_combo = generate_random_meal(all_meals["Lunch"]["main"], all_meals["Lunch"]["toppings"])
            dinner_combo = generate_random_meal(all_meals["Dinner"]["main"], all_meals["Dinner"]["toppings"])

            # If any meal couldn't be generated (not enough items), skip this attempt
            if not all([breakfast_combo, lunch_combo, dinner_combo]):
                continue

            b_nut = calculate_combo_nutrition(breakfast_combo)
            l_nut = calculate_combo_nutrition(lunch_combo)
            d_nut = calculate_combo_nutrition(dinner_combo)
            
            # Enforce meal-specific calorie constraints
            if not (200 <= b_nut['calories'] <= 700): continue
            if not (500 <= l_nut['calories'] <= 1000): continue
            if not (500 <= d_nut['calories'] <= 1000): continue

            # Enforce that breakfast is the smallest meal
            if not (b_nut['calories'] < l_nut['calories'] and b_nut['calories'] < d_nut['calories']):
                continue

            total_nutrition = {key: b_nut[key] + l_nut[key] + d_nut[key] for key in DV_TARGETS}

            if meets_macro_constraints(total_nutrition):
                score = calculate_micronutrient_score(total_nutrition)
                plan = {
                    "Breakfast": breakfast_combo,
                    "Lunch": lunch_combo,
                    "Dinner": dinner_combo
                }
                valid_plans.append((score, plan))
        
        if not valid_plans:
            print("\nCould not find any meal plans that met all constraints.")
            print("Consider loosening the calorie range or protein minimum in DV_TARGETS.")
        else:
            valid_plans.sort(key=lambda x: x[0])
            
            unique_plans = []
            seen_plans = set()
            for score, plan in valid_plans:
                plan_representation = tuple(sorted(
                    (meal_type, tuple(sorted((item['item_name'], servings) for item, servings in combo)))
                    for meal_type, combo in plan.items()
                ))
                if plan_representation not in seen_plans:
                    unique_plans.append((score, plan))
                    seen_plans.add(plan_representation)

            print(f"\nFound {len(unique_plans)} unique plans that meet all constraints. Showing the top 5:")
            
            for score, plan in unique_plans[:5]:
                print_meal_plan(plan, score)
