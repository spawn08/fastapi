import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient


@pytest.fixture(name="client")
def get_client():
    from docs_src.request_form_models.tutorial001 import app

    client = TestClient(app)
    return client


def test_post_body_form(client: TestClient):
    response = client.post("/login/", data={"username": "Foo", "password": "secret"})
    assert response.status_code == 200
    assert response.json() == {"username": "Foo", "password": "secret"}


def test_post_body_form_no_password(client: TestClient):
    response = client.post("/login/", data={"username": "Foo"})
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "password"],
                    "msg": "Field required",
                    "input": {"username": "Foo"},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", "password"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


def test_post_body_form_no_username(client: TestClient):
    response = client.post("/login/", data={"password": "secret"})
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "username"],
                    "msg": "Field required",
                    "input": {"password": "secret"},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", "username"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


def test_post_body_form_no_data(client: TestClient):
    response = client.post("/login/")
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "username"],
                    "msg": "Field required",
                    "input": {},
                },
                {
                    "type": "missing",
                    "loc": ["body", "password"],
                    "msg": "Field required",
                    "input": {},
                },
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", "username"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "password"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ]
        }
    )


def test_post_body_json(client: TestClient):
    response = client.post("/login/", json={"username": "Foo", "password": "secret"})
    assert response.status_code == 422, response.text
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "username"],
                    "msg": "Field required",
                    "input": {},
                },
                {
                    "type": "missing",
                    "loc": ["body", "password"],
                    "msg": "Field required",
                    "input": {},
                },
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", "username"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "password"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ]
        }
    )


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/login/": {
                "post": {
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        },
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                    },
                    "summary": "Login",
                    "operationId": "login_login__post",
                    "requestBody": {
                        "content": {
                            "application/x-www-form-urlencoded": {
                                "schema": {"$ref": "#/components/schemas/FormData"}
                            }
                        },
                        "required": True,
                    },
                }
            }
        },
        "components": {
            "schemas": {
                "FormData": {
                    "properties": {
                        "username": {"type": "string", "title": "Username"},
                        "password": {"type": "string", "title": "Password"},
                    },
                    "type": "object",
                    "required": ["username", "password"],
                    "title": "FormData",
                },
                "ValidationError": {
                    "title": "ValidationError",
                    "required": ["loc", "msg", "type"],
                    "type": "object",
                    "properties": {
                        "loc": {
                            "title": "Location",
                            "type": "array",
                            "items": {
                                "anyOf": [{"type": "string"}, {"type": "integer"}]
                            },
                        },
                        "msg": {"title": "Message", "type": "string"},
                        "type": {"title": "Error Type", "type": "string"},
                    },
                },
                "HTTPValidationError": {
                    "title": "HTTPValidationError",
                    "type": "object",
                    "properties": {
                        "detail": {
                            "title": "Detail",
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ValidationError"},
                        }
                    },
                },
            }
        },
    }
