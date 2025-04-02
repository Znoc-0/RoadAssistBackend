from mod.user import handle_user_register, handle_user_login,handle_place_order,handle_get_order, handle_user_info,handle_recharge_balance,handle_pumps, CORS_HEADERS
from mod.seller import handle_seller_register, handle_seller_login,handle_seller_info, handle_current_stock,handle_update_stock,handle_get_seller_order, handle_update_order_status, handle_otp_order

from aiohttp import web 
import logging
import asyncio

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s - %(name)s")


LOG = logging.getLogger("xdg")
LOG.setLevel(logging.DEBUG)

app = web.Application(
    logger=logging.getLogger("xdg"),
)

app.router.add_options('/{any_path:.*}', lambda _: web.Response(headers=CORS_HEADERS))

#user routes
app.router.add_post('/user/register',handle_user_register)
app.router.add_post('/user/login', handle_user_login)
app.router.add_post('/user/place_order', handle_place_order)
app.router.add_post('/user/get_order', handle_get_order)
app.router.add_post('/user/get_user_info', handle_user_info)
app.router.add_post('/user/recharge_balance', handle_recharge_balance)
app.router.add_post('/user/get_pumps',handle_pumps)


#seller routes
app.router.add_post('/seller/login', handle_seller_login)
app.router.add_post('/seller/register', handle_seller_register)
app.router.add_post('/seller/get_seller_info', handle_seller_info)
app.router.add_post('/seller/get_current_stock',handle_current_stock)
app.router.add_post('/seller/update_stock', handle_update_stock)
app.router.add_post('/seller/get_all_orders', handle_get_seller_order)
app.router.add_post('/seller/update_order_status', handle_update_order_status)

app.router.add_post('/verifyorderotp', handle_otp_order)




web.run_app(app,port=8888)