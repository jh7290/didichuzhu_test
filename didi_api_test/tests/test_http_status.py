from common.assertions import assert_status_code


def test_health_check(api):
    response = api.get("/health")
    assert_status_code(response, 200)
    assert response.json()["status"] == "ok"


def test_not_found_api(api):
    response = api.get("/not-exist")
    assert_status_code(response, 404)
    assert response.json()["message"] == "接口不存在"
