from mod.db import db
from aiohttp import web
order = db.order
user = db.user
seller = db.seller
import datetime
from bson.objectid import ObjectId  # Import ObjectId

def create_order(
    email_id, fuel_type, quantity, price, latitude, longitude, pump_id
):
    user_data = user.find_one({'email': email_id})
    
    # Ensure that pump_id is an ObjectId if it's passed as a string
    if isinstance(pump_id, str):
        pump_id = ObjectId(pump_id)
        
    pump = seller.find_one({'_id': pump_id})

    # Ensure pump is found and print the pump details for debugging
    if not pump:
        return "Pump not found"
    
    pump['_id'] = str(pump['_id'])  # Convert ObjectId to string for easier handling
    print("Pump data:", pump)

    if user_data:
        user_balance = user_data['balance']
        if user_balance >= price:
            stock_update = {}

            # Check if sufficient fuel is available for the selected fuel type
            if fuel_type == "Petrol" and pump['petrol'] >= quantity:
                stock_update = {'petrol': -quantity}
            elif fuel_type == "Diesel" and pump['diesel'] >= quantity:
                stock_update = {'diesel': -quantity}
            elif fuel_type == "Premium" and pump['premium'] >= quantity:
                stock_update = {'premium': -quantity}
            else:
                return "insufficient stock"

            # Deduct the amount from the user's balance
            user.update_one(
                {'email': email_id},
                {'$inc': {'balance': -price}}
            )

            # Log the current balance before updating
            print(f"Before update, seller balance: {pump['balance']}")

            # Deduct stock and add to the seller's balance in a single update
            result = seller.update_one(
                {'_id': pump_id},
                {'$inc': {
                    'balance': price,  # Increase seller's balance
                    **stock_update      # Decrease fuel stock
                }}
            )

            # Log if the update was successful
            if result.matched_count > 0:
                print("Seller balance and stock updated successfully.")
            else:
                print("No matching seller found, update failed.")
        else:
            return "insufficient balance"
    else:
        return "user not found"

    # Create order data
    order_data = {
        'email_id': email_id,
        "order_status": "pending",
        "order_date":datetime.datetime.now().strftime('%d-%m-%Y'),
        "order_time": datetime.datetime.now().strftime('%H:%M:%S'),
        'fuel_type': fuel_type,
        'quantity': quantity,
        'price': price,
        'latitude': latitude,
        'longitude': longitude,
        'pump_id': pump_id,
        'deliveryBoy':"not assigned",
    }

    # Insert order data into the database
    result = order.insert_one(order_data)
    order_data['_id'] = str(result.inserted_id) 
     # Convert ObjectId to string
    order_data['pump_id'] = str(order_data['pump_id'])  # Convert ObjectId to string

    
    print("Order created successfully:", order_data)
    
    return order_data




           


   
    
    



def get_order_by_email_id(email_id):
    # order_data = order.find_all({'user_id': user_id})
    # fetch all orders for the user
    order_data = order.find({'email_id': email_id})
    if order_data:
        return order_data
    else:
        return None
    


def deduct_balance(email_id, amount):
    # Deduct the amount from the user's balance
    user.update_one(
        {'email': email_id},
        {'$inc': {'balance': -amount}}
    )
    print("Balance deducted successfully")
    return "balance deducted successfully"

