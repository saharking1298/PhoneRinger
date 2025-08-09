from flask import Flask, request, render_template
from pathlib import Path
import json

config_path = Path(__file__).parent.parent / "data" / "config.json"


def read_config():
    return json.load(open(config_path, "r", encoding="utf-8"))


def write_config(data):
    json.dump(data, open(config_path, "w", encoding="utf-8"))


config = read_config()
app = Flask(__name__)


def get_user_data(user_id):
    user = config["users"][user_id].copy()
    user["id"] = user_id
    return user


def verify_user_id(user_id):
    try:
        num = int(user_id)  # Try converting
        if 0 <= num < len(config["users"]):
            return num
    except ValueError:
        pass
    return None


@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_id = verify_user_id(user_id)
    body = request.get_json()

    if user_id is not None and "token" in body and "name" in body:
        user_data = {
            "name": body["name"],
            "token": body["token"]
        }
        config["users"][user_id] = user_data
        write_config(config)
        return '', 201
    else:
        return '', 401


@app.route('/users/new', methods=['PUT'])
def new_user():
    body = request.get_json()

    if "token" in body and "name" in body:
        user_data = {
            "name": body["name"],
            "token": body["token"]
        }
        config["users"].append(user_data)
        if len(config["users"]) == 1:
            config["selected-user"] = 0
        write_config(config)
        return '', 201
    else:
        return '', 401


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_id = verify_user_id(user_id)

    if user_id is not None:
        users = config["users"]
        del users[user_id]
        if config["selected-user"] == user_id:
            if len(users) > 0:
                config["selected-user"] = 0
            else:
                config["selected-user"] = None
        write_config(config)
        return '', 204
    else:
        return '', 404


@app.route('/selected-user', methods=['PUT'])
def set_selected_user():
    body = request.get_json()
    if "id" not in body:
        return '', 401
    user_id = verify_user_id(body["id"])

    if user_id is not None:
        config["selected-user"] = user_id
        write_config(config)
        return '', 204
    else:
        return '', 404


@app.route("/")
def index():
    users = []
    for i in range(len(config["users"])):
        users.append(get_user_data(i))
    selected_user = config["selected-user"]
    return render_template("pages/indexPage.html", users=users, selected_user=selected_user)


@app.route("/users/new")
def new_user_view():
    return render_template("pages/newUser.html")


@app.route("/users/<user_id>/edit")
def edit_user_view(user_id):
    user_id = verify_user_id(user_id)
    if user_id is not None:
        user = get_user_data(user_id)
        return render_template("pages/editUser.html", user=user)
    else:
        return '404 Resource Not Found', 404


@app.route("/users/<user_id>/delete")
def delete_user_view(user_id):
    user_id = verify_user_id(user_id)
    if user_id is not None:
        user = get_user_data(user_id)
        return render_template("pages/deleteUser.html", user=user)
    else:
        return '404 Resource Not Found', 404


def main():
    app.run(host="0.0.0.0", port=3000, debug=True)


if __name__ == '__main__':
    main()