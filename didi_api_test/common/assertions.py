def assert_status_code(response, expected_code):
    assert response.status_code == expected_code, (
        f"Expected status code {expected_code}, got {response.status_code}, body={response.text}"
    )


def assert_json_field(data, field):
    assert field in data, f"Expected field '{field}' in response, got {data}"


def assert_error_message(data, expected_message):
    assert data.get("message") == expected_message, (
        f"Expected message '{expected_message}', got '{data.get('message')}'"
    )


def assert_order_status(data, expected_status):
    assert data.get("status") == expected_status, (
        f"Expected order status '{expected_status}', got '{data.get('status')}'"
    )
