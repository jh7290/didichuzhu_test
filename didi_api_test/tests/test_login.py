import pytest

from common.assertions import assert_error_message, assert_json_field, assert_status_code


@pytest.mark.login
@pytest.mark.smoke
def test_login_success(api):
    response = api.post("/login", json={
        "phone": "13800138000",
        "password": "123456"
    })

    assert_status_code(response, 200)
    data = response.json()
    assert data["message"] == "登录成功"
    assert_json_field(data, "token")
    assert_json_field(data, "user_id")


@pytest.mark.login
def test_login_cases(api, login_cases):
    for case in login_cases:
        response = api.post("/login", json={
            "phone": case["phone"],
            "password": case["password"]
        })
        assert_status_code(response, case["expected_code"])
        data = response.json()
        assert_error_message(data, case["expected_message"])


@pytest.mark.login
@pytest.mark.parametrize("phone, password, expected_code, expected_message", [
    ("", "123456", 400, "手机号不能为空"),
    ("13800138", "123456", 400, "手机号格式错误"),
    ("138001380001", "123456", 400, "手机号格式错误"),
    ("13800abc000", "123456", 400, "手机号格式错误"),
    ("13800138000", "", 400, "密码不能为空"),
    ("13999999999", "123456", 404, "账号不存在"),
    ("13800138000", "111111", 401, "密码错误"),
])
def test_login_parametrize(api, phone, password, expected_code, expected_message):
    response = api.post("/login", json={
        "phone": phone,
        "password": password
    })

    assert_status_code(response, expected_code)
    assert_error_message(response.json(), expected_message)
