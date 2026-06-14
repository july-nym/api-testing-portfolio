"""User read/write coverage on reqres plus a schema cross-check on jsonplaceholder."""
import pytest

from utils.assertions import (
    assert_status,
    assert_response_under,
    assert_matches_schema,
    assert_has_keys,
)
from utils.schemas import SINGLE_USER_SCHEMA, USER_LIST_SCHEMA


@pytest.mark.smoke
def test_get_single_user_matches_schema(reqres, settings):
    resp = reqres.get("/users/2")
    assert_status(resp, 200)
    assert_response_under(resp, settings.max_response_ms)
    assert_matches_schema(resp.json(), SINGLE_USER_SCHEMA)


@pytest.mark.regression
@pytest.mark.parametrize("page", [1, 2])
def test_user_list_pagination(reqres, page):
    resp = reqres.get("/users", params={"page": page})
    assert_status(resp, 200)
    body = resp.json()
    assert_matches_schema(body, USER_LIST_SCHEMA)
    assert body["page"] == page
    # the data array should never exceed the advertised page size
    assert len(body["data"]) <= body["per_page"]


@pytest.mark.regression
def test_create_user_echoes_payload(reqres):
    # A QA Lead candidate, naturally
    new_hire = {"name": "Tomás Aguilar", "job": "QA Lead"}
    resp = reqres.post("/users", json=new_hire)

    assert_status(resp, 201)
    body = resp.json()
    assert body["name"] == new_hire["name"]
    assert body["job"] == new_hire["job"]
    assert_has_keys(body, "id", "createdAt")


@pytest.mark.regression
def test_update_user_with_put(reqres):
    resp = reqres.put("/users/2", json={"name": "Tomás Aguilar", "job": "Principal QA"})
    assert_status(resp, 200)
    assert resp.json()["job"] == "Principal QA"
    assert "updatedAt" in resp.json()


@pytest.mark.regression
def test_partial_update_with_patch(reqres):
    resp = reqres.patch("/users/2", json={"job": "Engineering Manager"})
    assert_status(resp, 200)
    assert resp.json()["job"] == "Engineering Manager"


@pytest.mark.regression
def test_delete_user_returns_204(reqres):
    resp = reqres.delete("/users/2")
    assert_status(resp, 204)
    assert resp.text == ""  # 204 must not carry a body


@pytest.mark.regression
def test_jsonplaceholder_user_count(jsonplaceholder):
    # Secondary target — a sanity check that our client works against a second
    # host and that the well-known fixture size hasn't drifted.
    resp = jsonplaceholder.get("/users")
    assert_status(resp, 200)
    assert len(resp.json()) == 10
