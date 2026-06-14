"""JSON schemas used for response validation.

Kept as plain dicts rather than separate .json files because they live close to
the tests that use them and it's one less thing to load from disk. If these grow
past a handful, splitting them into a schemas/ directory would be the next move.
"""

# reqres single-user payload, e.g. GET /users/2
SINGLE_USER_SCHEMA = {
    "type": "object",
    "required": ["data", "support"],
    "properties": {
        "data": {
            "type": "object",
            "required": ["id", "email", "first_name", "last_name", "avatar"],
            "properties": {
                "id": {"type": "integer"},
                "email": {"type": "string", "format": "email"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
                "avatar": {"type": "string"},
            },
        },
        "support": {"type": "object"},
    },
}

# reqres paginated list, e.g. GET /users?page=2
USER_LIST_SCHEMA = {
    "type": "object",
    "required": ["page", "per_page", "total", "total_pages", "data"],
    "properties": {
        "page": {"type": "integer"},
        "per_page": {"type": "integer"},
        "total": {"type": "integer"},
        "total_pages": {"type": "integer"},
        "data": {
            "type": "array",
            "items": SINGLE_USER_SCHEMA["properties"]["data"],
        },
    },
}

# restful-booker create response
BOOKING_CREATE_SCHEMA = {
    "type": "object",
    "required": ["bookingid", "booking"],
    "properties": {
        "bookingid": {"type": "integer"},
        "booking": {
            "type": "object",
            "required": [
                "firstname",
                "lastname",
                "totalprice",
                "depositpaid",
                "bookingdates",
            ],
            "properties": {
                "firstname": {"type": "string"},
                "lastname": {"type": "string"},
                "totalprice": {"type": "integer"},
                "depositpaid": {"type": "boolean"},
                "bookingdates": {
                    "type": "object",
                    "required": ["checkin", "checkout"],
                    "properties": {
                        "checkin": {"type": "string"},
                        "checkout": {"type": "string"},
                    },
                },
            },
        },
    },
}
