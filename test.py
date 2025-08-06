import re
from bs4 import BeautifulSoup

# It's good practice to load the HTML from the file.
# For this example, I'll paste the content directly.
# In a real script, you would do:
# with open("Nutrition Label.htm", "r", encoding="utf-8") as f:
#     html_content = f.read()

html_content = """
<!-- The following is required by Aurora Information Systems, DO NOT MODIFY OR REMOVE -->
<!-- fieldfilt.aspx, Version 3.0.0  -->
<!-- End of Aurora Information Systems Required Text -->
<html><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<title>Nutrition Label</title>
<link rel="stylesheet" href="Nutrition%20Label_files/foodpro_web_ina.css" type="text/css">
</head>
<body class="labelbody">
<div class="labelrecipe">Lemon Coffee Cake Muffin</div>
<br>

<table border="1" align="center" width="1200" cellpadding="4" cellspacing="0" bgcolor="#FFFFFF">
  <tbody><tr>
    <td>
      <table border="0" width="100%" cellpadding="0" cellspacing="0">
        <tbody><tr>
          
          <td rowspan="10" valign="top" width="15%">
            <div class="nutfactsheader">Nutrition<br>Facts</div>
            <hr size="1" noshade="noshade" color="#000000">
            <div class="nutfactsservpercont">1 servings per container</div>
            <div class="nutfactsservsize">Serving size</div>
            
              <div class="nutfactsservsize">1 each</div>
                        
            <hr size="1" noshade="noshade" color="#000000">
            <table border="0" width="100%" cellpadding="0" cellspacing="0">
              <tbody><tr>
                <td class="nutfactscalories" align="left" valign="top">Calories<br><font size="3">per serving</font></td>
                
                  <td class="nutfactscaloriesval" align="right" valign="top">199</td>
                
              </tr>
            </tbody></table>
          </td>
          <td width="2%">&nbsp;</td>
          <td valign="top" align="left" width="20%">
            <span class="amountperserving">Amount/serving</span>
            <hr size="8" noshade="noshade" color="#000000">
          </td>
          <td valign="top" align="right" width="10%">
            <span class="perdailyvalue">% Daily Value*</span>
            <hr size="8" noshade="noshade" color="#000000">
          </td>
          <td width="2%">&nbsp;</td>
          <td valign="top" align="left" width="20%">
            <span class="amountperserving">Amount/serving</span>
            <hr size="8" noshade="noshade" color="#000000">
          </td>
          <td valign="top" align="right" width="10%">
            <span class="perdailyvalue">% Daily Value*</span>
            <hr size="8" noshade="noshade" color="#000000">
          </td>
          <td width="2%" class="nutfactsdisclaimer" align="right" valign="top"><br><br>*&nbsp;</td>
          <td width="10%" class="nutfactsdisclaimer" rowspan="6" align="left" valign="top"><br><br>The % Daily Value<br>(DV) tells you how<br>much a nutrient<br>in a serving of<br>food contributes to<br>a daily diet. 2,000<br>calories a day is<br>used for general<br>nutrition advice.</td>
        </tr>
        <tr>
          <td width="2%">&nbsp;</td>
          <td>
            
              <span class="nutfactstopnutrient"><b>Total Fat&nbsp;</b>6.4g</span>
            
            <hr size="1" noshade="noshade" color="#000000">
          </td>
          <td align="right">
            
              <span class="nutfactstopnutrient"><b>8%</b></span>
            
            <hr size="1" noshade="noshade" color="#000000">
          </td>
          <td width="2%">&nbsp;</td>
          <td>
            
              <span class="nutfactstopnutrient"><b>Total Carbohydrate.&nbsp;</b>32.5g</span>
            
            <hr size="1" noshade="noshade" color="#000000">
          </td>
          <td align="right">
            
              <span class="nutfactstopnutrient"><b>12%</b></span>
            
            <hr size="1" noshade="noshade" color="#000000">
          </td>
          <td width="2%">&nbsp;</td>
        </tr>
        <tr>
          <td width="2%">&nbsp;</td>
          <td>
            
              <span class="nutfactstopnutrient">&nbsp;&nbsp;&nbsp;&nbsp;Saturated Fat&nbsp;1.1g</span>
            
            <hr size="1" noshade="noshade" color="#000000">
          </td>
          <td align="right">
            
              <span class="nutfactstopnutrient"><b>6%</b></span>
            
            <hr size="1" noshade="noshade" color="#000000">
          </td>
          <td width="2%">&nbsp;</td>
          <td>
            
              <span class="nutfactstopnutrient">&nbsp;&nbsp;&nbsp;&nbsp;Dietary Fiber&nbsp;0.5g</span>
            
            <hr size="1" noshade="noshade" color="#000000">
          </td>
          <td align="right">
            
              <span class="nutfactstopnutrient"><b>2%</b></span>
            
            <hr size="1" noshade="noshade" color="#000000">
          </td>
          <td width="2%">&nbsp;</td>
        </tr>
        <tr>
          <td width="2%">&nbsp;</td>
          <td colspan="1">
            
              <span class="nutfactstopnutrient">&nbsp;&nbsp;&nbsp;&nbsp;<i>Trans</i> Fat&nbsp;0g</span>
            
            <hr size="1" noshade="noshade" color="#000000">
          </td>
          <td align="right">                         
            <span class="nutfactstopnutrient"><b>&nbsp;</b></span>
            <hr size="1" noshade="noshade" color="#000000">
          </td>
          <td width="2%">&nbsp;</td>
          <td colspan="1">
            
              <span class="nutfactstopnutrient">&nbsp;&nbsp;&nbsp;&nbsp;Total Sugars&nbsp;1.2g</span>
            
            <hr size="1" noshade="noshade" color="#000000">
          </td>
          <td align="right">            
            <span class="nutfactstopnutrient"><b>&nbsp;</b></span>
            <hr size="1" noshade="noshade" color="#000000">
          </td>
          <td width="2%">&nbsp;</td>
        </tr>
        <tr>
          <td width="2%">&nbsp;</td>
          <td>
            
              <span class="nutfactstopnutrient"><b>Cholesterol&nbsp;</b>0mg</span>
            
            <hr size="1" noshade="noshade" color="#000000">
          </td>
          <td align="right">
            
              <span class="nutfactstopnutrient"><b>0%</b></span>
            
            <hr size="1" noshade="noshade" color="#000000">
          </td>
          <td width="2%">&nbsp;</td>
          
          <td align="left">
            <span class="nutfactstopnutrient">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Includes 0.5g Added Sugars</span>
            <hr size="1" noshade="noshade" color="#000000">
          </td>
          <td align="right">
            <span class="nutfactstopnutrient"><b>1%</b></span>
            <hr size="1" noshade="noshade" color="#000000">
          </td>
          <td width="2%">&nbsp;</td>
        </tr>
        <tr>
          <td width="2%">&nbsp;</td>
          <td>
            
              <span class="nutfactstopnutrient"><b>Sodium&nbsp;</b>164.9mg</span>
            
            <hr size="8" noshade="noshade" color="#000000">
          </td>
          <td align="right">
            
              <span class="nutfactstopnutrient"><b>7%</b></span>
            
            <hr size="8" noshade="noshade" color="#000000">
          </td>
          <td width="2%">&nbsp;</td>
          <td colspan="1">
            
              <span class="nutfactstopnutrient"><b>Protein&nbsp;</b>2.2g</span>
            
            <hr size="8" noshade="noshade" color="#000000">
          </td>
          <td align="right">
            <span class="nutfactstopnutrient"><b>&nbsp;</b></span>
            <hr size="8" noshade="noshade" color="#000000">
          </td>
          <td width="2%">&nbsp;</td>
        </tr>
        <tr>
          <td width="2%">&nbsp;</td>
          <td colspan="7">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" align="left">
            
              <tbody><tr>
                
                <td width="22%">
                  <table border="0" width="100%" align="left" cellpadding="0" cellspacing="5">
                    <tbody><tr>
                      <td width="100%">
                        
                        <span class="nutfactstopnutrient">Calories&nbsp;198.9kcal</span>
                        
                          <span class="nutfactstopnutrient">&nbsp;8%</span>
                         
                      </td>
                    </tr>
                  </tbody></table>
                </td>
              
                <td width="26%">
                  <table border="0" width="100%" align="left" cellpadding="0" cellspacing="5">
                    <tbody><tr>
                      <td width="100%">
                        
                        <li>
                        
                        <span class="nutfactstopnutrient">Fat&nbsp;6.4g</span>
                        
                          <span class="nutfactstopnutrient">&nbsp;8%</span>
                         
                      </li></td>
                    </tr>
                  </tbody></table>
                </td>
              
                <td width="26%">
                  <table border="0" width="100%" align="left" cellpadding="0" cellspacing="5">
                    <tbody><tr>
                      <td width="100%">
                        
                        <li>
                        
                        <span class="nutfactstopnutrient">Saturated Fat&nbsp;1.1g</span>
                        
                          <span class="nutfactstopnutrient">&nbsp;6%</span>
                         
                      </li></td>
                    </tr>
                  </tbody></table>
                </td>
              
                <td width="26%">
                  <table border="0" width="100%" align="left" cellpadding="0" cellspacing="5">
                    <tbody><tr>
                      <td width="100%">
                        
                        <li>
                        
                        <span class="nutfactstopnutrient">Trans Fatty Acid&nbsp;0g</span>
                        
                          <span class="nutfactstopnutrient">&nbsp;</span>
                         
                      </li></td>
                    </tr>
                  </tbody></table>
                </td>
              
              </tr>
              
              <tr>
                
                <td width="22%">
                  <table border="0" width="100%" align="left" cellpadding="0" cellspacing="5">
                    <tbody><tr>
                      <td width="100%">
                        
                        <span class="nutfactstopnutrient">Cholesterol&nbsp;0mg</span>
                        
                          <span class="nutfactstopnutrient">&nbsp;0%</span>
                         
                      </td>
                    </tr>
                  </tbody></table>
                </td>
              
                <td width="26%">
                  <table border="0" width="100%" align="left" cellpadding="0" cellspacing="5">
                    <tbody><tr>
                      <td width="100%">
                        
                        <li>
                        
                        <span class="nutfactstopnutrient">Sodium&nbsp;164.9mg</span>
                        
                          <span class="nutfactstopnutrient">&nbsp;7%</span>
                         
                      </li></td>
                    </tr>
                  </tbody></table>
                </td>
              
                <td width="26%">
                  <table border="0" width="100%" align="left" cellpadding="0" cellspacing="5">
                    <tbody><tr>
                      <td width="100%">
                        
                        <li>
                        
                        <span class="nutfactstopnutrient">Carbohydrates&nbsp;32.5g</span>
                        
                          <span class="nutfactstopnutrient">&nbsp;12%</span>
                         
                      </li></td>
                    </tr>
                  </tbody></table>
                </td>
              
                <td width="26%">
                  <table border="0" width="100%" align="left" cellpadding="0" cellspacing="5">
                    <tbody><tr>
                      <td width="100%">
                        
                        <li>
                        
                        <span class="nutfactstopnutrient">Dietary Fiber&nbsp;0.5g</span>
                        
                          <span class="nutfactstopnutrient">&nbsp;2%</span>
                         
                      </li></td>
                    </tr>
                  </tbody></table>
                </td>
              
              </tr>
              
              <tr>
                
                <td width="22%">
                  <table border="0" width="100%" align="left" cellpadding="0" cellspacing="5">
                    <tbody><tr>
                      <td width="100%">
                        
                        <span class="nutfactstopnutrient">Total Sugars&nbsp;1.2g</span>
                        
                          <span class="nutfactstopnutrient">&nbsp;</span>
                         
                      </td>
                    </tr>
                  </tbody></table>
                </td>
              
                <td width="26%">
                  <table border="0" width="100%" align="left" cellpadding="0" cellspacing="5">
                    <tbody><tr>
                      <td width="100%">
                        
                        <li>
                        
                        <span class="nutfactstopnutrient">Added Sugar&nbsp;0.5g</span>
                        
                          <span class="nutfactstopnutrient">&nbsp;1%</span>
                         
                      </li></td>
                    </tr>
                  </tbody></table>
                </td>
              
                <td width="26%">
                  <table border="0" width="100%" align="left" cellpadding="0" cellspacing="5">
                    <tbody><tr>
                      <td width="100%">
                        
                        <li>
                        
                        <span class="nutfactstopnutrient">Protein&nbsp;2.2g</span>
                        
                          <span class="nutfactstopnutrient">&nbsp;4%</span>
                         
                      </li></td>
                    </tr>
                  </tbody></table>
                </td>
              
                <td width="26%">
                  <table border="0" width="100%" align="left" cellpadding="0" cellspacing="5">
                    <tbody><tr>
                      <td width="100%">
                        
                        <li>
                        
                        <span class="nutfactstopnutrient">Vitamin D - mcg&nbsp;0.2mcg</span>
                        
                          <span class="nutfactstopnutrient">&nbsp;0%</span>
                         
                      </li></td>
                    </tr>
                  </tbody></table>
                </td>
              
              </tr>
              
              <tr>
                
                <td width="22%">
                  <table border="0" width="100%" align="left" cellpadding="0" cellspacing="5">
                    <tbody><tr>
                      <td width="100%">
                        
                        <span class="nutfactstopnutrient">Calcium&nbsp;55.9mg</span>
                        
                          <span class="nutfactstopnutrient">&nbsp;4%</span>
                         
                      </td>
                    </tr>
                  </tbody></table>
                </td>
              
                <td width="26%">
                  <table border="0" width="100%" align="left" cellpadding="0" cellspacing="5">
                    <tbody><tr>
                      <td width="100%">
                        
                        <li>
                        
                        <span class="nutfactstopnutrient">Iron&nbsp;0.9mg</span>
                        
                          <span class="nutfactstopnutrient">&nbsp;5%</span>
                         
                      </li></td>
                    </tr>
                  </tbody></table>
                </td>
              
                <td width="26%">
                  <table border="0" width="100%" align="left" cellpadding="0" cellspacing="5">
                    <tbody><tr>
                      <td width="100%">
                        
                        <li>
                        
                        <span class="nutfactstopnutrient">Potassium&nbsp;50mg</span>
                        
                          <span class="nutfactstopnutrient">&nbsp;1%</span>
                         
                      </li></td>
                    </tr>
                  </tbody></table>
                </td>
              
            </tr></tbody></table>
          </td>
        </tr>
      </tbody></table>
    </td></tr>
  </tbody></table>
  
  <table border="0" cellpadding="1" cellspacing="1" align="center" width="1200">
    <tbody><tr>
      <td>
        <span class="labelingredientscaption">INGREDIENTS:&nbsp;&nbsp;</span><span class="labelingredientsvalue">AP
 Flour (Enriched Bleached Wheat Flour (Bleached Flour, Niacin, Reduced 
Iron, Enzymes added for improved baking, Thiamine Mononitrate, 
Riboflavin, Folic Acid)), Soy Milk (Water, Organic Soybeans, Cane Sugar,
 Contains 1 Or Less Of: Gellan Gum, Locust Bean Gum, Natural Flavor, 
Riboflavin B2, Sea Salt, Tricalcium Phosphate, Vitamin A Palmitate, 
Vitamin B6, Vitamin B12, Vitamin D2, Vitamin E D-alpha Tocopheryl 
Acetate.), Granulated Sugar, Margarine Spread (Oil Blend (Palm, Soybean,
 Canola, and Olive Oils), Water, Contains less than 2% of Salt, 
Enzyme-Modified Soybean Lecithin, Natural &amp; Artificial Flavor, 
Potassium Sorbate and Calcium Disodium EDTA (to preserve freshness), 
Lactic Acid, Vitamin A Palmitate, and Beta-Carotene Color), Lemon Glaze 
(Powdered Sugar (Sugar, Cornstarch), Fresh Lemon Juice, Imitation 
Vanilla Extract (Water, Caramel Color, Artificial Flavor, Citric Acid, 
Sodium Benzoate (preservative). )), Fresh Lemon Juice, Baking Powder 
(Baking Soda, Corn Starch, Sodium Aluminum Sulfate, Calcium Sulfate, 
Monocalcium Phosphate), Lemon Extract (Alcohol, Water, Oil of Lemon), 
Canola Pan Spray (Canola Oil, Canola Lecithin, Mono and Diglycerides, 
Natural Flavor, Propellan), Imitation Vanilla Extract (Water, Caramel 
Color, Artificial Flavor, Citric Acid, Sodium Benzoate (preservative). 
), Salt (Salt)</span>
      </td>
    </tr>
  </tbody></table>
  
  <table border="0" cellpadding="1" cellspacing="1" align="center" width="1200">
    <tbody><tr>
      <td>
        <span class="labelallergenscaption">ALLERGENS: </span><span class="labelallergensvalue">Wheat, Soybeans</span>
      </td>
    </tr>
  </tbody></table>
  <table border="0" cellpadding="1" cellspacing="1" align="center" width="1200">
  <tbody><tr>
    <td><span class="labelwebcodesvalue"><img src="Nutrition%20Label_files/Wheat.png" alt="Contains Wheat">&nbsp;<img src="Nutrition%20Label_files/Soy.png" alt="Contains Soy">&nbsp;<img src="Nutrition%20Label_files/Vegan.png" alt="Vegan">&nbsp;    </span></td><td>
  </td></tr>
</tbody></table>

  <div align="center">
  <form>
  <table align="center" border="0" cellpadding="1" cellspacing="5" width="1200">
    <tbody><tr valign="middle">
      <td width="50%" align="right"><input type="button" value="Back" onclick="history.go(-1);"></td>
      <td width="50%"><input type="button" value="Print" onclick="javascript:print();"></td>
    </tr>
    
      <tr>
        <td colspan="2"><div class="labelfooter">The University of Texas
 at Austin does not guarantee the accuracy of nutrition information; 
ingredient and nutrition content of foods may vary due to changes in 
product formulation, recipe substitutions, portion size and other 
factors. The nutrition analyses provided here are approximations only. 
Guests with food allergies or other food intolerances should consult a 
Chef or Dining Manager for specific ingredient questions. Guests may 
also consult our Registered Dietitians for additional assistance at 
dietitian@austin.utexas.edu.</div></td>
      </tr>
    
  </tbody></table>
  </form>
  </div>
  
</body></html>
<!-- The following is required by Aurora Information Systems, DO NOT MODIFY OR REMOVE -->
<!-- label.aspx, Version 3.0.0  -->
<!-- End of Aurora Information Systems Required Text -->
"""

# Create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# --- Helper function to find and extract nutrient values ---
def get_nutrient(soup, label_text):
    """
    Finds a nutrient by its label text and extracts its value.
    This version is more robust to handle tricky HTML and text formatting.
    
    Args:
        soup: The BeautifulSoup object.
        label_text: The text label of the nutrient to find (e.g., "Total Fat").
        
    Returns:
        The nutrient value as a string, or "Not found" if it's not present.
    """
    try:
        # Find a tag that CONTAINS the label text. This is key.
        # The lambda function searches the text of all elements, ignoring internal tags like <i>.
        # It also makes sure the tag is a span with the correct class.
        nutrient_tag = soup.find(
            lambda tag: tag.name == 'span' 
            and label_text.lower() in tag.get_text().lower() 
            and tag.has_attr('class') 
            and 'nutfactstopnutrient' in tag['class']
        )
        
        # If no tag was found, we can't proceed.
        if not nutrient_tag:
            return "Not found"
            
        # Get the full, cleaned text from the tag we found.
        full_text = nutrient_tag.get_text(strip=True).replace('\xa0', ' ')
        
        # This regex is designed to find the numerical value.
        # It looks for a number (potentially with a decimal) that is followed by a unit (g, mg, or mcg).
        # This is a more reliable way to extract the value than trying to split the string.
        match = re.search(r'(\d+(?:\.\d+)?)\s*(g|mg|mcg)', full_text, re.IGNORECASE)
        
        if match:
            # The match gives us the number (group 1) and the unit (group 2).
            # We combine them into a clean string like "6.4g".
            return f"{match.group(1)}{match.group(2)}"
            
        return "Not found"

    except AttributeError:
        # This will catch errors if the find() method returns None for any reason.
        return "Not found"

# --- Dictionary to store all the parsed data ---
nutrition_data = {}

# --- Extracting each value ---

# Get the recipe name
nutrition_data['item_name'] = soup.find('div', class_='labelrecipe').get_text(strip=True)

# Get the serving size
nutrition_data['serving_size'] = soup.find('div', class_='nutfactsservsize', string=re.compile("Serving size")).find_next_sibling('div').get_text(strip=True)

# Get Calories
# The main calories value has a unique class, which makes it easy
nutrition_data['calories'] = soup.find('td', class_='nutfactscaloriesval').get_text(strip=True)

# Use the improved helper function for the rest of the nutrients
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


# Get Ingredients
nutrition_data['ingredients'] = soup.find('span', class_='labelingredientsvalue').get_text(strip=True).replace('\n', ' ')

# Get Allergens
nutrition_data['allergens'] = soup.find('span', class_='labelallergensvalue').get_text(strip=True)


# --- Print the results in a clean format ---
import json
print(json.dumps(nutrition_data, indent=4))
