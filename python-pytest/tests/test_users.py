"""User reads + post CRUD against jsonplaceholder.

jsonplaceholder is a read-mostly fake API: GET returns seeded data, while writes
are echoed back with a synthetic id (nothing is actually persisted). That's still
plenty to exercise status codes, schemas, and payload round-tripping — and it's
keyless and stable, which is what we want CI leaning on.
"""
import pytest

from utils.assertions import (
    assert_status,
    assert_response_under,
    assert_matches_schema,
    assert_has_keys,
)
from utils.schemas import SINGLE_USER_SCHEMA, POST_CREATE_SCHEMA


@pytest.mark.smoke
def test_get_single_user_matches_schema(jsonplaceholder, settings):
    resp = jsonplaceholder.get("/users/2")
    assert_status(resp, 200)
    assert_response_under(resp, settings.max_response_ms)
    assert_matches_schema(resp.json(), SINGLE_USER_SCHEMA)


@pytest.mark.smoke
def test_user_directory_has_ten_seeded_users(jsonplaceholder):
    resp = jsonplaceholder.get("/users")
    assert_status(resp, 200)
    assert len(resp.json()) == 10


@pytest.mark.regression
@pytest.mark.parametrize("page", [1, 2])
def test_post_pagination(jsonplaceholder, page):
    # jsonplaceholder paginates with _page/_limit and advertises the full count
    # in the X-Total-Count header rather than the body.
    limit = 10
    resp = jsonplaceholder.get("/posts", params={"_page": page, "_limit": limit})
    assert_status(resp, 200)
    assert len(resp.json()) <= limit
    assert resp.headers.get("X-Total-Count") == "100"


@pytest.mark.regression
def test_create_post_echoes_payload(jsonplaceholder, new_post_payload):
    resp = jsonplaceholder.post("/posts", json=new_post_payload)
    assert_status(resp, 201)
    body = resp.json()
    assert_matches_schema(body, POST_CREATE_SCHEMA)
    assert body["title"] == new_post_payload["title"]
    assert body["userId"] == new_post_payload["userId"]
    assert_has_keys(body, "id")
    assert body["id"] == 101  # jsonplaceholder always hands back 101 for a new post


@pytest.mark.regression
def test_replace_post_with_put(jsonplaceholder, new_post_payload):
    updated = {**new_post_payload, "title": "Release approved"}
    resp = jsonplaceholder.put("/posts/1", json=updated)
    assert_status(resp, 200)
    assert resp.json()["title"] == "Release approved"


@pytest.mark.regression
def test_partial_update_with_patch(jsonplaceholder):
    resp = jsonplaceholder.patch("/posts/1", json={"title": "Hotfix shipped"})
    assert_status(resp, 200)
    assert resp.json()["title"] == "Hotfix shipped"
    # PATCH should leave the untouched fields in place
    assert resp.json()["userId"] == 1


@pytest.mark.regression
def test_delete_post_returns_200(jsonplaceholder):
    resp = jsonplaceholder.delete("/posts/1")
    assert_status(resp, 200)
