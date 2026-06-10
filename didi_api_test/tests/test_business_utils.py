import pytest

from common.business import can_create_order, check_login_input, check_price, get_status_text


@pytest.mark.business
@pytest.mark.parametrize("status, expected", [
    ("created", "订单已创建"),
    ("driver_assigned", "已派单"),
    ("started", "行程已开始"),
    ("finished", "行程已结束"),
    ("paid", "订单已支付"),
    ("cancelled", "订单已取消"),
    ("unknown", "未知订单状态"),
])
def test_get_status_text(status, expected):
    assert get_status_text(status) == expected


@pytest.mark.business
@pytest.mark.parametrize("price, expected", [
    (28.5, "金额有效"),
    (0.01, "金额有效"),
    (0, "金额无效"),
    (-1, "金额无效"),
])
def test_check_price(price, expected):
    assert check_price(price) == expected


@pytest.mark.business
@pytest.mark.parametrize("phone, password, expected", [
    ("", "123456", "手机号不能为空"),
    ("13800138", "123456", "手机号格式错误"),
    ("138001380001", "123456", "手机号格式错误"),
    ("13800abc000", "123456", "手机号格式错误"),
    ("13800138000", "", "密码不能为空"),
    ("13800138000", "123456", "输入格式正确"),
])
def test_check_login_input(phone, password, expected):
    assert check_login_input(phone, password) == expected


@pytest.mark.business
@pytest.mark.parametrize("is_login, start_place, end_place, driver_count, expected", [
    (False, "学校", "火车站", 3, "请先登录"),
    (True, "", "火车站", 3, "起点和终点不能为空"),
    (True, "学校", "", 3, "起点和终点不能为空"),
    (True, "学校", "学校", 3, "起点和终点不能相同"),
    (True, "学校", "火车站", 0, "暂无司机"),
    (True, "学校", "火车站", 3, "下单成功，正在派单"),
])
def test_can_create_order(is_login, start_place, end_place, driver_count, expected):
    assert can_create_order(is_login, start_place, end_place, driver_count) == expected
