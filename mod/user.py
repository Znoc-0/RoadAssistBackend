from mod.db.user import create_user, get_user_by_email , update_user_balance, get_all_pumps
from mod.db.order import create_order, get_order_by_email_id
# get_user_by_username
# from mod.db.seller import create_seller, get_seller_by_email, get_seller_by_username

from aiohttp import web



CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Max-Age": "3600",
    "Access-Control-Allow-Credentials": "true",
    "Acess-Control-Expose-Headers": "*",
    "Access-Control-Request-Headers": "*",
    "Access-Control-Request-Method": "*",
    }

async def handle_user_register(request):

    try:

        data = await request.json()
    except Exception as e:
        print(e)
        return web.json_response({'message': 'Invalid requst'}, status=400 , headers=CORS_HEADERS)
    
    if data.get('email') is None or data.get('username') is None or data.get('password') is None or data.get('phone') is None or data.get('first_name') is None or data.get('last_name') is None or data.get('age') is None :
        return web.json_response({'message': 'Missing fields'}, status=400 , headers=CORS_HEADERS)
    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    age = data.get('age')

    result = create_user(username, password, phone, first_name, last_name, email, age)

    return web.json_response(
        {
        'message': result},
        headers=CORS_HEADERS,
        status=200
        )

async def   handle_user_login(request):

    try:
        data = await request.json()
    except Exception as e:
        print(e)
        return web.json_response({'message': 'Invalid requst'}, status=400 , headers=CORS_HEADERS)
    
    if data.get('email') is None or data.get('password') is None:
        return web.json_response({'message': 'Missing fields'}, status=400 , headers=CORS_HEADERS)

    email = data.get('email')
    password = data.get('password')

    user_data = get_user_by_email(email)

    if user_data is None:
        return web.json_response({'message': 'User not found'}, status=404 , headers=CORS_HEADERS)

    if user_data['password'] != password:
        return web.json_response({'message': 'Invalid password'}, status=401 , headers=CORS_HEADERS)

    user_data.pop('_id', None)  # Remove the _id field from the response

    return web.json_response(
        {
        'message': 'Login successful',
        'user': user_data
        },
          headers=CORS_HEADERS, status=200
        )


async def handle_place_order(request):
    try:
        data = await request.json()
        print(data)
    except Exception as e:
        print(e)
        return web.json_response({'message': 'Invalid request'}, status=400, headers=CORS_HEADERS)
    email_id = data.get('email')
    fuel_type = data.get('fuel_type')
    quantity = data.get('quantity')
    price = data.get('price')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    pump_id = data.get('pump_id')


    if email_id is None or fuel_type is None or quantity is None or price is None or latitude is None or longitude is None:
        return web.json_response({'message': 'Missing fields'}, status=400, headers=CORS_HEADERS)
    

    order_data = create_order(email_id, fuel_type, quantity, price, latitude, longitude, pump_id)
    if order_data is None:
        return web.json_response({'message': 'Order creation failed'}, status=500, headers=CORS_HEADERS)
    if order_data == "insufficient balance":
        return web.json_response({'message': 'Insufficient balance'}, status=400, headers=CORS_HEADERS)
    
   
    if order_data == "insufficient stock":
        return web.json_response({'message': 'Insufficient stock'}, status=400, headers=CORS_HEADERS)
    return web.json_response(
        {
            
            'order_data': order_data
        },
        headers=CORS_HEADERS,
        status=200
    )
    
async def handle_get_order(request):
    try:
        data = await request.json()

        print(data)
    except Exception as e:
        print(e)
        return web.json_response({'message': 'Invalid request'}, status=400, headers=CORS_HEADERS)
    
    email_id = data.get('email_id')

    if email_id is None:
        return web.json_response({'message': 'Missing fields'}, status=400, headers=CORS_HEADERS)

    order_data = get_order_by_email_id(email_id)
    
    if order_data is None:
        return web.json_response({'message': 'Order not found'}, status=404, headers=CORS_HEADERS)

    order_data = list(order_data)  # Convert cursor to list
    for order in order_data:
        order['_id'] = str(order['_id'])  # Convert ObjectId to string
        order['pump_id'] = str(order['pump_id'])

    return web.json_response(
        {
            'message': 'Order fetched successfully',
            'order_data': order_data
        },
        headers=CORS_HEADERS,
        status=200
    )


async def handle_user_info(request):
    try:
        data = await request.json()
    except Exception as e:
        print(e)
        return web.json_response({'message': 'Invalid request'}, status=400, headers=CORS_HEADERS)

    email_id = data.get('email_id')

    if email_id is None:
        return web.json_response({'message': 'Missing fields'}, status=400, headers=CORS_HEADERS)

    user_data = get_user_by_email(email_id)

    if user_data is None:
        return web.json_response({'message': 'User not found'}, status=404, headers=CORS_HEADERS)

    user_data.pop('_id', None)  # Remove the _id field from the response

    return web.json_response(
        {
            'message': 'User fetched successfully',
            'user_data': user_data
        },
        headers=CORS_HEADERS,
        status=200
    )


async def handle_recharge_balance(request):
    try:
        data = await request.json()
        print(data)
    except Exception as e:
        print(e)
        return web.json_response({'message': 'Invalid request'}, status=400, headers=CORS_HEADERS)

    email_id = data.get('email_id')
    amount = data.get('amount')

    if email_id is None or amount is None:
        return web.json_response({'message': 'Missing fields'}, status=400, headers=CORS_HEADERS)

    user_data = get_user_by_email(email_id)

    if user_data is None:
        return web.json_response({'message': 'User not found'}, status=404, headers=CORS_HEADERS)

    # Update the user's balance in the database
    # Assuming you have a function update_user_balance(email_id, amount) to update the balance
    update_user_balance(email_id, amount)

    return web.json_response(
        {
            'message': 'Balance recharged successfully',
            'new_balance': user_data['balance'] + amount  # Assuming you have a balance field in user_data
        },
        headers=CORS_HEADERS,
        status=200
    )


async def handle_pumps(request):
    try:
        data = await request.json()
    except Exception as e:
        print(e)
        return web.json_response({'message': 'Invalid request'}, status=400, headers=CORS_HEADERS)

    # Assuming you have a function get_all_pumps() to fetch all pumps from the database
    # Replace this with your actual implementation
    # Example: pumps_data = get_all_pumps()

    pump_data = get_all_pumps()
    if pump_data is None:
        return web.json_response({'message': 'No pumps found'}, status=404, headers=CORS_HEADERS)

    return web.json_response(
        {
            'message': 'Pumps fetched successfully',
            'pumps_data': pump_data
        },
        headers=CORS_HEADERS,
        status=200
    )