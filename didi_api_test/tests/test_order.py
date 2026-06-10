import pytest

from common.assertions import (
    assert_error_message,
    assert_json_field,
    assert_order_status,
    assert_status_code,
)


@pytest.mark.order
@pytest.mark.smoke
def test_create_order_success(api, auth_headers):
    body = {
        "start_place": "学校",
        "end_place": "火车站",
        "driver_count": 3,
        "price": 28.5
    }

    response = api.post("/orders", json=body, headers=auth_headers)

    assert_status_code(response, 201)
    data = response.json()
    assert_json_field(data, "order_id")
    assert data["start_place"] == "学校"
    assert data["end_place"] == "火车站"
    assert_order_status(data, "created")


@pytest.mark.order
def test_create_order_without_token(api):
    response = api.post("/orders", json={
        "start_place": "学校",
        "end_place": "火车站",
        "driver_count": 3,
        "price": 28.5
    })

    assert_status_code(response, 401)
    assert_error_message(response.json(), "未登录或认证失败")


@pytest.mark.order
def test_create_order_cases(api, auth_headers, order_cases):
    for case in order_cases["create_order_cases"]:
        response = api.post("/orders", json=case["body"], headers=auth_headers)
        assert_status_code(response, case["expected_code"])
        data = response.json()

        if case["expected_code"] == 201:
            assert_order_status(data, case["expected_status"])
            assert_json_field(data, "order_id")
        else:
            assert_error_message(data, case["expected_message"])


@pytest.mark.order
def test_query_order_success(api, auth_headers, created_order):
    order_id = created_order["order_id"]
    response = api.get(f"/orders/{order_id}", headers=auth_headers)

    assert_status_code(response, 200)
    data = response.json()
    assert data["order_id"] == order_id
    assert_order_status(data, "created")


@pytest.mark.order
def test_query_order_not_found(api, auth_headers):
    response = api.get("/orders/999999", headers=auth_headers)

    assert_status_code(response, 404)
    assert_error_message(response.json(), "订单不存在")


@pytest.mark.order
def test_cancel_order_success(api, auth_headers, created_order):
    order_id = created_order["order_id"]
    response = api.post(f"/orders/{order_id}/cancel", headers=auth_headers)

    assert_status_code(response, 200)
    assert_order_status(response.json(), "cancelled")


@pytest.mark.order
def test_cancel_order_repeat(api, auth_headers, created_order):
    order_id = created_order["order_id"]

    first_response = api.post(f"/orders/{order_id}/cancel", headers=auth_headers)
    assert_status_code(first_response, 200)

    second_response = api.post(f"/orders/{order_id}/cancel", headers=auth_headers)
    assert_status_code(second_response, 409)
    assert_error_message(second_response.json(), "订单已取消，不能重复取消")
