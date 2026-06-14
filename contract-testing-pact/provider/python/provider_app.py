"""A minimal stand-in for the real user-service provider.

In a production setup you'd verify the contract against the actual service. Here
we ship a tiny Flask app that implements just enough of the user-service to be
verifiable, plus the provider-states hook Pact calls before each interaction.

The provider-states endpoint is the key bit: the consumer's pact says
"given user 2 exists", and this is where the provider makes that precondition
true (seeds the row, mocks the DB, whatever). Pact POSTs the state name here
before replaying the request.
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

# in-memory "database", populated by provider states
_users = {}


@app.route("/users/<int:user_id>")
def get_user(user_id):
    user = _users.get(user_id)
    if user is None:
        return jsonify({}), 404
    return jsonify({"data": user})


@app.route("/_pact/provider_states", methods=["POST"])
def provider_states():
    """Set up the world to match the consumer's stated precondition."""
    state = (request.get_json(silent=True) or {}).get("state")

    if state == "user 2 exists":
        _users[2] = {
            "id": 2,
            "email": "janet.weaver@reqres.in",
            "first_name": "Janet",
            "last_name": "Weaver",
            "avatar": "https://reqres.in/img/faces/2-image.jpg",
        }
    return jsonify({"result": state})


if __name__ == "__main__":
    # port matches the verification test's provider_base_url
    app.run(port=5001)
