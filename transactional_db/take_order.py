# Function to get the customer's name
def get_customer_name():
    customer_name = input("What's a good name for the order? ")
    return customer_name

# Function to take the order
def take_order(menu):
    # Initialize orders list
    orders = []

    # Open order loop
    place_order = True
    while place_order:
        # Ask the customer from which menu category they want to order
        print("From which menu would you like to order? ")

        # Create a variable for the menu item number
        i = 1
        # Create a dictionary to store the menu for later retrieval
        menu_items = {}

        # Print the options to choose from menu headings
        for key in menu.keys():
            print(f"{i}: {key}")
            # Store the menu category associated with its menu item number
            menu_items[i] = key
            # Add 1 to the menu item number
            i += 1

        # Get the customer's input
        menu_category = input("Type menu number: ")

        # Check if the customer's input is a number
        if menu_category.isdigit():
            # Check if the customer's input is a valid option
            if int(menu_category) in menu_items.keys():
                # Save the menu category name to a variable
                menu_category_name = menu_items[int(menu_category)]
                print(f"You selected {menu_category_name}")

                # Print out the menu options from the menu_category_name
                print(f"What {menu_category_name} item would you like to order?")
                i = 1
                menu_items = {}
                print("Item # | Item name                | Price")
                print("-------|--------------------------|-------")
                for key, value in menu[menu_category_name].items():
                    # Check if the menu item is a dictionary to handle differently
                    if type(value) is dict:
                        for key2, value2 in value.items():
                            num_item_spaces = 24 - len(key + key2) - 3
                            item_spaces = " " * num_item_spaces
                            print(f"{i}      | {key} - {key2}{item_spaces} | ${value2}")
                            menu_items[i] = {
                                "Item name": key + " - " + key2,
                                "Price": float(value2)
                            }
                            i += 1
                    else:
                        num_item_spaces = 24 - len(key)
                        item_spaces = " " * num_item_spaces
                        print(f"{i}      | {key}{item_spaces} | ${value}")
                        menu_items[i] = {
                            "Item name": key,
                            "Price": float(value)
                        }
                        i += 1
                # Ask customer to input menu item number
                menu_selection = input("What item # would you like? ")

                # Check if the customer typed a number
                if menu_selection.isdigit():
                    # Convert the menu selection to an integer
                    menu_selection = int(menu_selection)

                    # Check if the menu selection is in the menu items
                    if menu_selection in menu_items.keys():
                        # Store the item name as a variable
                        cust_order = menu_items[menu_selection]

                        # Ask the customer for the quantity of the menu item
                        quantity = input("How many would you like to order? ")

                        # Check if the quantity is a number, default to 1 if not
                        if quantity.isdigit():
                            quantity = int(quantity)
                        else:
                            print("Invalid quantity, setting to 1.")
                            quantity = 1

                        # Add the item name, price, and quantity to the order list
                        orders.append({
                            "item_name": cust_order["Item name"],
                            "price": float(cust_order["Price"]),
                            "quantity": quantity
                        })

                        # Confirm the order
                        if quantity > 1: 
                            print(f"Added {quantity} {cust_order['Item name']}s to your order.")
                        else:
                            print(f"Added {quantity} {cust_order['Item name']} to your order.")
                    else:
                        # Tell the customer they didn't select a menu option
                        print(f"{menu_category} was not a menu option.")
                else:
                    # Tell the customer they didn't select a number
                    print("You didn't select a number.")
            else:
                print("Invalid menu category selection.")
        else:
            print("You didn't select a number.")

        while True:
            # Ask the customer if they would like to keep ordering
            keep_ordering = input("Would you like to keep ordering? (Y)es or (N)o? ").lower()

            # Check the customer's input
            if keep_ordering == 'y':
                break
            elif keep_ordering == 'n':
                place_order = False
                break
            else:
                #Tell the customer to try again
                print('Please enter Y or N.')

    return orders

# Function to print the order
def print_order_summary(customer_name, orders):
    # Print out the customer's order
    print(f"\nThis is what we are preparing for you, {customer_name}.\n")

    print("Item name                 | Price  | Quantity")
    print("--------------------------|--------|----------")

    # Loop through the items in the customer's order
    for order in orders:
        # Store the dictionary items as variables
        item_name = order['item_name']
        price = order['price']
        quantity = order['quantity']

        # Calculate the number of spaces for formatted printing
        num_item_spaces = 25 - len(item_name)
        num_price_spaces = 5 - len(f"{price}")
        num_quantity_spaces = 8 - len(str(quantity))

        # Create space strings
        item_spaces = " " * num_item_spaces
        price_spaces = " " * num_price_spaces
        quantity_spaces = " " * num_quantity_spaces

        # Print the item name, price, and quantity
        print(f"{item_name}{item_spaces} | ${price}{price_spaces} | {quantity}{quantity_spaces}")

    # Multiply the price by quantity for each item in the order list, then sum() and print the prices.
    total = sum(float(order['price']) * int(order['quantity']) for order in orders)
    print(f'\nTotal amount due: ${total:.2f}')
