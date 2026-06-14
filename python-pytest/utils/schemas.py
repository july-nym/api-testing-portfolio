"""JSON schemas used for response validation.

Kept as plain dicts rather than separate .json files because they live close to
the tests that use them and it's one less thing to load from disk. If these grow
past a handful, splitting them into a schemas/ directory would be the next move.
"""

# jsonplaceholder user, e.g. GET /users/2 — note the nested address/company.
# We only require the fields we actually assert on; extra fields are allowed.
SINGLE_USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "username", "email", "address", "phone", "company"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "phone": {"type": "string"},
        "website": {"type": "string"},
        "address": {
            "type": "object",
            "required": ["street", "suite", "city", "zipcode"],
            "properties": {
                "street": {"type": "string"},
                "suite": {"type": "string"},
                "city": {"type": "string"},
                "zipcode": {"type": "string"},
            },
        },
        "company": {
            "type": "object",
            "required": ["name"],
            "properties": {"name": {"type": "string"}},
        },
    },
}

# jsonplaceholder create response, e.g. POST /posts -> 201
POST_CREATE_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "body", "userId"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
        "userId": {"type": "integer"},
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
