
# get_user_by_username
from mod.db.seller import create_seller , get_seller_by_email ,update_seller_stock, get_seller_order,update_orderstatus
# , get_seller_by_username
from mod.db.order import db

from bson.objectid import ObjectId
order = db.order
from aiohttp import web
import random
from mod.user import CORS_HEADERS

async def handle_seller_register(request):
    try:
        data = await request.json()
        print(data)
    except Exception as e:
        print(e)
        return web.json_response({'message': 'Invalid request'}, status=400, headers=CORS_HEADERS)

    if data.get('pump_name') is None  or data.get('phone') is None or data.get('owner_name') is None or data.get('email') is None or data.get('password') is None or data.get('age') is None or data.get('username') is None:
        return web.json_response({'message': 'Missing fields'}, status=400, headers=CORS_HEADERS)

    pump_name = data.get('pump_name')
    pump_lat = data.get('pump_lat')
    pump_long = data.get('pump_long')
    phone = data.get('phone')
    owner_name = data.get('owner_name')
    email = data.get('email')
    password = data.get('password')
    age = data.get('age')
    username = data.get('username')

    result = create_seller(pump_name, pump_lat,pump_long, phone, owner_name, email, password, age, username)

    return web.json_response(
        {
            'message': result
        },
        headers=CORS_HEADERS,
        status=200
    )


async def handle_seller_login(request):
    try:
        data = await request.json()
    except Exception as e:
        print(e)
        return web.json_response({'message': 'Invalid request'}, status=400, headers=CORS_HEADERS)

    if data.get('email') is None or data.get('password') is None:
        return web.json_response({'message': 'Missing fields'}, status=400, headers=CORS_HEADERS)

    email = data.get('email')
    password = data.get('password')

    seller_data = get_seller_by_email(email)

    if seller_data is None:
        return web.json_response({'message': 'Seller not found'}, status=404, headers=CORS_HEADERS)

    if seller_data['password'] != password:
        return web.json_response({'message': 'Invalid password'}, status=401, headers=CORS_HEADERS)

    seller_data.pop('_id', None)  # Remove the _id field from the response

    return web.json_response(
        {
            'message': 'Login successful',
            'seller': seller_data
        },
        headers=CORS_HEADERS,
        status=200
    )



async def handle_seller_info(request):
    try:
        data = await request.json()
    except Exception as e:
        print(e)
        return web.json_response({'message': 'Invalid request'}, status=400, headers=CORS_HEADERS)

    if data.get('email_id') is None:
        return web.json_response({'message': 'Missing fields'}, status=400, headers=CORS_HEADERS)

    email = data.get('email_id')

    seller_data = get_seller_by_email(email)

    if seller_data is None:
        return web.json_response({'message': 'Seller not found'}, status=404, headers=CORS_HEADERS)

    seller_data.pop('_id', None)  # Remove the _id field from the response

    return web.json_response(
        {
            'message': 'Seller info retrieved successfully',
            'seller': seller_data
        },
        headers=CORS_HEADERS,
        status=200
    )


async def handle_current_stock(request):
    try:
        data = await request.json()
    except Exception as e:
        print(e)
        return web.json_response({'message': 'Invalid request'}, status=400, headers=CORS_HEADERS)

    if data.get('email_id') is None:
        return web.json_response({'message': 'Missing fields'}, status=400, headers=CORS_HEADERS)

    email = data.get('email_id')

    seller_data = get_seller_by_email(email)

    if seller_data is None:
        return web.json_response({'message': 'Seller not found'}, status=404, headers=CORS_HEADERS)

    petrol = seller_data.get('petrol')  # Assuming current_stock is a field in the seller document
    diesel = seller_data.get('diesel')  # Assuming current_stock is a field in the seller document
    premium = seller_data.get('premium')  # Assuming current_stock is a field in the seller document
    current_stock = {
        'petrol': petrol,
        'diesel': diesel,
        'premium': premium
    }

    return web.json_response(
        {
            'message': 'Current stock retrieved successfully',
            'current_stock': current_stock
        },
        headers=CORS_HEADERS,
        status=200
    )


async def handle_update_stock(request):
    try:
        data = await request.json()
    except Exception as e:
        print(e)
        return web.json_response({'message': 'Invalid request'}, status=400, headers=CORS_HEADERS)

    if data.get('email_id')  is None:
        return web.json_response({'message': 'Missing fields'}, status=400, headers=CORS_HEADERS)

    email = data.get('email_id')
    fuel_type = data.get('fuel_type')
    quantity = data.get('quantity')

    seller_data = get_seller_by_email(email)

    if seller_data is None:
        return web.json_response({'message': 'Seller not found'}, status=404, headers=CORS_HEADERS)

   
    
    update_seller_stock(email, fuel_type, quantity)

    return web.json_response(
        {
            'message': 'Stock updated successfully'
        },
        headers=CORS_HEADERS,
        status=200
    )

async def handle_get_seller_order(request):
    try:
        data = await request.json()
        print(data)
    except Exception as e:
        print(e)
        return web.json_response({'message': 'Invalid request'}, status=400, headers=CORS_HEADERS)
    
    email_id = data.get('email_id')
    if email_id is None:
        return web.json_response({'message': 'Missing fields'}, status=400, headers=CORS_HEADERS)
    
    
    orders=get_seller_order (email_id)
    if orders is None:
        return web.json_response({'message': 'Order not found'}, status=404, headers=CORS_HEADERS)
    

    for order in orders:
        order['_id'] = str(order['_id'])

    return web.json_response(
        {
            'message': 'Order fetched successfully',
            'order_data': orders
        },
        headers=CORS_HEADERS,
        status=200
    )


async def handle_update_order_status(request):
    try:
        data = await request.json()
        print("Received data:", data)
    except Exception as e:
        print("Error:", e)
        return web.json_response({'message': 'Invalid request'}, status=400, headers=CORS_HEADERS)

    # Check for missing required fields
    required_fields = ['email_id', 'order_id', 'status']
    if any(field not in data for field in required_fields):
        return web.json_response({'message': 'Missing fields'}, status=400, headers=CORS_HEADERS)

    email = data.get('email_id')
    order_id = data.get('order_id')
    order_status = data.get('status')
    deliveryBoy = data.get('deliveryBoy', None)  # Default to None if not provided

    # Convert order_id to ObjectId
    try:
        order_id = ObjectId(order_id)  # Ensure order_id is an ObjectId
    except Exception:
        return web.json_response({'message': 'Invalid order ID format'}, status=400, headers=CORS_HEADERS)

    # Get seller data
    seller_data = get_seller_by_email(email)
    if seller_data is None:
        return web.json_response({'message': 'Seller not found'}, status=404, headers=CORS_HEADERS)

    # Reference to the order collection
    order_collection = db.order  # Ensure this exists

    # Update the order status in the database
    if order_status == "DELIVERYBOY_ASSIGNED":
        # generate otp and store it in the order collection if not exist otp field create it
        otp = random.randint(1000, 9999)
        order_collection.update_one(
            {'_id': order_id},
            {'$set': {'otp': otp}}
        )

    result = order_collection.update_one(
        {'_id': order_id},  # Now using ObjectId for querying
        {'$set': {'order_status': order_status, 'deliveryBoy': deliveryBoy}}
    )

    if result.modified_count == 0:
        return web.json_response({'message': 'Order not found or status already updated'}, status=404, headers=CORS_HEADERS)

    return web.json_response({'message': 'Order status updated successfully'}, status=200, headers=CORS_HEADERS)



async def handle_otp_order(request):
    
    try:
        data = await request.json()
        print(data)
    except Exception as e:
        print(e)
        return web.json_response({'message': 'Invalid request'}, status=400, headers=CORS_HEADERS)

    if data.get('email_id') is None or data.get('order_id') is None or data.get('otp') is None:
        return web.json_response({'message': 'Missing fields'}, status=400, headers=CORS_HEADERS)

    email = data.get('email_id')
    order_id = data.get('order_id')
    otp = int(data.get('otp'))
    deliveryBoy = data.get('deliveryBoy')  
    status = data.get('status')  
    


    # Convert order_id to ObjectId

    try:
        order_id = ObjectId(order_id)  # Ensure order_id is an ObjectId
    except Exception:
        return web.json_response({'message': 'Invalid order ID format'}, status=400, headers=CORS_HEADERS)
    


    # Get seller data
    seller_data = get_seller_by_email(email)
    if seller_data is None:
        return web.json_response({'message': 'Seller not found'}, status=404, headers=CORS_HEADERS)
    
    # Reference to the order collection
    order_collection = db.order  # Ensure this exists

    # Check if the order exists and the OTP matches

    if order_collection.find_one(
        {'_id': order_id, 'otp': otp}
    ):
        # Update the order status to "completed" and remove the OTP
        order_collection.update_one(
            {'_id': order_id},
            {'$set': {'order_status': status, 'deliveryBoy': deliveryBoy}, '$unset': {'otp': ""}}
        )
        return web.json_response({'message': 'Order completed successfully'}, status=200, headers=CORS_HEADERS)
    else:
        return web.json_response({'message': 'Invalid OTP or order not found'}, status=404, headers=CORS_HEADERS)
    



