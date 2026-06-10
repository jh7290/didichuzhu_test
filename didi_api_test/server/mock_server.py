import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse


VALID_PHONE = "13800138000"
VALID_PASSWORD = "123456"
VALID_TOKEN = "mock_token_123456"

ORDERS = {}
NEXT_ORDER_ID = 1001


def json_response(handler, status_code, data):
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    handler.send_response(status_code)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def read_json(handler):
    length = int(handler.headers.get("Content-Length", 0))
    if length == 0:
        return {}
    raw = handler.rfile.read(length).decode("utf-8")
    return json.loads(raw)


def require_auth(handler):
    auth = handler.headers.get("Authorization", "")
    return auth == f"Bearer {VALID_TOKEN}"


class MockHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/health":
            json_response(self, 200, {"status": "ok"})
            return

        if path.startswith("/orders/"):
            if not require_auth(self):
                json_response(self, 401, {"message": "未登录或认证失败"})
                return

            order_id = path.split("/")[-1]
            order = ORDERS.get(order_id)
            if order is None:
                json_response(self, 404, {"message": "订单不存在"})
                return
            json_response(self, 200, order)
            return

        json_response(self, 404, {"message": "接口不存在"})

    def do_POST(self):
        global NEXT_ORDER_ID

        parsed = urlparse(self.path)
        path = parsed.path
        body = read_json(self)

        if path == "/login":
            phone = body.get("phone", "")
            password = body.get("password", "")

            if phone == "":
                json_response(self, 400, {"message": "手机号不能为空"})
                return
            if len(phone) != 11 or not phone.isdigit():
                json_response(self, 400, {"message": "手机号格式错误"})
                return
            if password == "":
                json_response(self, 400, {"message": "密码不能为空"})
                return
            if phone != VALID_PHONE:
                json_response(self, 404, {"message": "账号不存在"})
                return
            if password != VALID_PASSWORD:
                json_response(self, 401, {"message": "密码错误"})
                return

            json_response(self, 200, {
                "message": "登录成功",
                "token": VALID_TOKEN,
                "user_id": 1,
                "phone": phone
            })
            return

        if path == "/orders":
            if not require_auth(self):
                json_response(self, 401, {"message": "未登录或认证失败"})
                return

            start_place = body.get("start_place", "")
            end_place = body.get("end_place", "")
            driver_count = body.get("driver_count", 0)
            price = body.get("price", 0)

            if start_place == "" or end_place == "":
                json_response(self, 400, {"message": "起点和终点不能为空"})
                return
            if start_place == end_place:
                json_response(self, 400, {"message": "起点和终点不能相同"})
                return
            if driver_count == 0:
                json_response(self, 409, {"message": "暂无司机"})
                return
            if price <= 0:
                json_response(self, 400, {"message": "金额无效"})
                return

            order_id = str(NEXT_ORDER_ID)
            NEXT_ORDER_ID += 1

            order = {
                "order_id": int(order_id),
                "user_id": 1,
                "start_place": start_place,
                "end_place": end_place,
                "driver_count": driver_count,
                "price": price,
                "status": "created"
            }
            ORDERS[order_id] = order
            json_response(self, 201, order)
            return

        if path.startswith("/orders/") and path.endswith("/cancel"):
            if not require_auth(self):
                json_response(self, 401, {"message": "未登录或认证失败"})
                return

            order_id = path.split("/")[-2]
            order = ORDERS.get(order_id)
            if order is None:
                json_response(self, 404, {"message": "订单不存在"})
                return
            if order["status"] == "cancelled":
                json_response(self, 409, {"message": "订单已取消，不能重复取消"})
                return
            if order["status"] == "paid":
                json_response(self, 409, {"message": "已支付订单不能取消"})
                return

            order["status"] = "cancelled"
            json_response(self, 200, order)
            return

        json_response(self, 404, {"message": "接口不存在"})


def run():
    server = HTTPServer(("127.0.0.1", 8000), MockHandler)
    print("Mock server running at http://127.0.0.1:8000")
    server.serve_forever()


if __name__ == "__main__":
    run()
