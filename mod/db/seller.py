from mod.db import db

seller = db.seller


import random

def create_seller(
        pump_name,
        pump_lat,
        pump_long,
        phone,
        owner_name,
        email,
        password,
        age,
        username,
        balance = 0,
        petrol = 100,
        diesel = 100,
        premium = 100,
):
    
    if seller.find_one ({'email': email}):
        print(seller.find_one({'email': email}))
        print("Seller already exists")
        return "seller already exists"
    
    elif seller.find_one({'username': username}):

        print(seller.find_one({'username': username}))
        print("Seller already exists")
        return "seller already exists"
    seller.insert_one({
        'pump_name': pump_name,
        'pump_lat': pump_lat,
        'pump_long': pump_long,
        'phone': phone,
        'owner_name': owner_name,
        'email': email,
        'password': password,
        'age': age,
        'username': username,
        'balance': balance,
        'petrol': petrol,
        'diesel': diesel,
        'premium': premium,

    })

    print("Seller created successfully")

    return "seller created successfully"




def get_seller_by_email(email):

    seller_data = seller.find_one({'email': email})
    if seller_data:

        return seller_data
    else:
        return None
    
def get_seller_by_username(username):

    seller_data = seller.find_one({'username': username})
    if seller_data:
        return seller_data
    else:
        return None




def update_seller_stock(email, fuel_type, quantity):
    seller_data = seller.find_one({'email': email})
    if seller_data:
        if fuel_type == 'petrol':
            new_stock = quantity
            # if new_stock < 0:
            #     return "Not enough stock"
            seller.update_one({'email': email}, {'$set': {'petrol': new_stock}})
            return "Stock updated successfully"
        elif fuel_type == 'diesel':
            new_stock =  quantity
            # if new_stock < 0:
            #     return "Not enough stock"
            seller.update_one({'email': email}, {'$set': {'diesel': new_stock}})
            return "Stock updated successfully"
        elif fuel_type == 'premium':
            new_stock =  quantity
            # if new_stock < 0:
            #     return "Not enough stock"
            seller.update_one({'email': email}, {'$set': {'premium': new_stock}})
            return "Stock updated successfully"
        else:
            return "Invalid fuel type"

    else:
        return "Seller not found"
    



def get_seller_order(email):

    seller_id = get_seller_by_email(email)
    if seller_id:
        orders = db.order.find({'pump_id': seller_id['_id']})

        orders_list = []
        for order in orders:
            order['_id'] = str(order['_id'])
            order['pump_id'] = str(order['pump_id'])
           
            orders_list.append(order)

        return orders_list
    else:
        return None
    


def update_orderstatus(email, order_id, order_status, deliveryBoy):
    seller_id = get_seller_by_email(email)
    if seller_id:
        order = db.order.find_one({'_id': order_id, 'pump_id': seller_id['_id']})
        if order:
            update_fields = {}

            # Update order_status if it's not present or empty
            if 'order_status' not in order or not order['order_status']:
                update_fields['order_status'] = order_status
            
            # Always update deliveryBoy field if it's provided
            # This will add the field if it doesn't exist
            if deliveryBoy:  # Only update if deliveryBoy parameter has a value
                update_fields['deliveryBoy'] = deliveryBoy

            if update_fields:
                db.order.update_one({'_id': order_id}, {'$set': update_fields})
                return "Order status updated successfully"
            else:
                return "No changes made, fields already exist"

        else:
            return "Order not found"
    else:
        return "Seller not found"