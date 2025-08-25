menu = """Restaurant Name: Biryani Baithak

Location: 45 Spice Street, Connaught Place, New Delhi

About Us:
At Biryani Baithak, we bring the rich, vibrant flavors of India right to your table. Situated in the heart of Connaught Place, New Delhi, we specialize in traditional biryanis, curries, and tandoori delights. Whether you're craving the fiery flavors of the South or the aromatic dishes from the North, we’ve got it all. Our commitment to using fresh, high-quality ingredients and our secret family recipes ensure that every meal feels like home.

Menu

1. Hyderabadi Dum Biryani - ₹650

2. Butter Chicken - ₹550

3. Paneer Tikka - ₹350

4. Methi Thepla - ₹120

5. Tandoori Roti - ₹60

6. Aloo Paratha - ₹120

7. Chicken Seekh Kebab - ₹300

8. Gulab Jamun - ₹150

9. Mango Lassi - ₹120

10. Masala Chai - ₹60

Menu Descriptions

1. Hyderabadi Dum Biryani
    Taste: Spicy, savory, and aromatic.
    Origin: Hyderabad, India
    Main Ingredients: Long-grain basmati rice, marinated chicken or mutton, saffron, yogurt, and a blend of spices.
    Flavour: The rice is infused with the savory essence of meat or vegetables, and the slow-cooked biryani gives off a rich, tantalizing fragrance from the saffron and ghee.

2. Butter Chicken
    Taste: Creamy, mildly spiced, and indulgent.
    Origin: Delhi, India
    Main Ingredients: Boneless chicken, tomatoes, cream, butter, and a mix of aromatic spices.
    Flavour: The dish is rich and creamy, with a mild, smoky flavor from the tandoor, combined with the tang of tomatoes and the richness of butter and cream.

3. Paneer Tikka
    Taste: Spicy, smoky, and tangy.
    Origin: North India
    Main Ingredients: Paneer (Indian cottage cheese), yogurt, red chili powder, turmeric, cumin, and coriander.
    Flavour: The marinated paneer cubes are grilled to perfection in the tandoor, giving them a smoky flavor and a crunchy outer layer, while the inside remains soft and juicy.

4. Methi Thepla
    Taste: Earthy, savory, and lightly spiced.
    Origin: Gujarat, India
    Main Ingredients: Whole wheat flour, fenugreek leaves, turmeric, cumin, and coriander.
    Flavour: A flatbread that’s soft, savory, and slightly bitter from the fenugreek, with a warm spiciness that pairs perfectly with yogurt or pickle.

5. Tandoori Roti
    Taste: Soft, chewy, and slightly smoky.
    Origin: North India
    Main Ingredients: Whole wheat flour, salt, water, and ghee.
    Flavour: A simple, smoky flatbread baked in the tandoor. Its chewy texture and slight crispness make it the perfect accompaniment to any curry or gravy.

6. Aloo Paratha
    Taste: Warm, comforting, and spicy.
    Origin: Punjab, India
    Main Ingredients: Whole wheat flour, mashed potatoes, onions, green chilies, and spices.
    Flavour: A stuffed flatbread filled with spiced potatoes. When served hot with yogurt and pickle, it’s an unbeatable comfort food.

7. Chicken Seekh Kebab
    Taste: Juicy, smoky, and spicy.
    Origin: Delhi, India
    Main Ingredients: Ground chicken, onions, garlic, green chilies, and a blend of spices.
    Flavour: Minced chicken mixed with a fragrant blend of spices, then grilled on skewers to perfection, creating a smoky, juicy, and flavorful kebab.

8. Gulab Jamun
    Taste: Sweet, warm, and soft.
    Origin: India
    Main Ingredients: Milk solids (khoya), sugar, ghee, cardamom, and rose water.
    Flavour: Soft, syrup-soaked dumplings that melt in your mouth with a perfect balance of sweetness, flavored with a hint of rose and cardamom.

9. Mango Lassi
    Taste: Refreshing, sweet, and creamy.
    Origin: Punjab, India
    Main Ingredients: Yogurt, fresh mango pulp, sugar, and cardamom.
    Flavour: A smooth, creamy drink that combines the rich sweetness of ripe mangoes with the tartness of yogurt, perfect for cooling down.

10. Masala Chai
    Taste: Warm, spiced, and aromatic.
    Origin: India
    Main Ingredients: Black tea, milk, ginger, cardamom, cloves, cinnamon, and sugar.
    Flavour: A rich, aromatic spiced tea that brings together the warmth of ginger, cardamom, and other spices. It’s comforting, robust, and perfect for a chilly evening.


Basic Details About The Restaurant

Restaurant Name: Biryani Baithak

Address: 45 Spice Street, Connaught Place, New Delhi

Phone Number: +91 11 2345-6789

Hours:
Monday to Friday: 11:00 AM - 11:00 PM
Saturday: 12:00 PM - 12:00 AM
Sunday: 11:00 AM - 11:00 PM


Delivery Options: Yes, available via our app and popular delivery services (Zomato, Swiggy).
Special Requests: Vegan, vegetarian, and gluten-free options available. Please inform the staff about any allergies.
"""


"functions": [
                {
                    "name": "get_menu_classes",
                    "description": "Get the list of menu categories. Use this function when: A user asks for the available categories in the menu. A user asks for types of dishes available at the restaurant. This function will give the user a list of the categories like 'Biryani', 'Curries', 'Tandoori', etc.",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    },
                    "required": []
                },
                {
                    "name": "get_dishes_in_class",
                    "description": "Get the list of dishes in a selected category. Use this function when: A user selects a category of the menu and asks for the dishes within that category. This function will return only the dishes belonging to the chosen category like 'Biryani', 'Curries', etc.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "class_name": {
                                "type": "string",
                                "description": "The name of the category chosen by the user. Examples: 'Biryani', 'Curries', 'Tandoori', etc."
                            }
                        },
                        "required": [
                            "class_name"
                        ]
                    }
                }
            ]