from mod.db import db

user = db.user


def create_user(
    username,
    password,
    phone,
    first_name, 
    last_name,
    email,
    age ,
    balance = 0,
):

    if user.find_one({'email': email}):
        print(user.find_one({'email': email}))
        print("User already exists")
        return "user already exists"
    
    elif user.find_one({'username': username}):
        print(user.find_one({'username': username}))
        print("User already exists")
        return "user already exists"
    
    user.insert_one({
        'username': username,
        'password': password,
        'phone': phone,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'age': age,
        'balance': balance
    })


    print("User created successfully")
    return "user created successfully"




def get_user_by_email(email):

    user_data = user.find_one({'email': email})
    if user_data:
        return user_data
    else:
        return None
    
def get_user_by_username(username):

    user_data = user.find_one({'username': username})
    if user_data:
        return user_data
    else:
        return None
    


def  update_user_balance(email, amount):
    user.update_one(
        {'email': email},
        {'$inc': {'balance': amount}}
    )
    return "balance updated successfully"


def get_all_pumps():
    pumps = db.seller.find()
   

    pumps_list = []
    for pump in pumps:
        pump['_id'] = str(pump['_id'])
        pump.pop('password', None)
        pump.pop('age', None)
        pump.pop('email', None)
        pump.pop('owner_name', None)
        pump.pop('username', None)
        pumps_list.append(pump)
    return pumps_list
   