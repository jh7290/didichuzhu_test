def get_status_text(status):
    if status == "created":
        return "订单已创建"
    elif status == "driver_assigned":
        return "已派单"
    elif status == "started":
        return "行程已开始"
    elif status == "finished":
        return "行程已结束"
    elif status == "paid":
        return "订单已支付"
    elif status == "cancelled":
        return "订单已取消"
    else:
        return "未知订单状态"


def check_price(price):
    if price > 0:
        return "金额有效"
    return "金额无效"


def check_login_input(phone, password):
    if phone == "":
        return "手机号不能为空"
    if len(phone) != 11 or not phone.isdigit():
        return "手机号格式错误"
    if password == "":
        return "密码不能为空"
    return "输入格式正确"


def can_create_order(is_login, start_place, end_place, driver_count):
    if not is_login:
        return "请先登录"
    if start_place == "" or end_place == "":
        return "起点和终点不能为空"
    if start_place == end_place:
        return "起点和终点不能相同"
    if driver_count == 0:
        return "暂无司机"
    return "下单成功，正在派单"
