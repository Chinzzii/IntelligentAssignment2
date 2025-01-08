#!/usr/bin/env python -B
import json
import flask
from flask import Flask
import clustering as clst
import top_trading_cycles as ttc
from user import User
from team import Team


def extract_data(req):
    """Extracts and returns the rank data, weights, and IDs from the request."""
    x, w, data_id = [], [], []
    for point in req["bids"]:
        x.append(point["ranks"])  # Collect ranking data
        w.append(point["weight"])  # Collect weight data
        data_id.append(point["id"])  # Collect data IDs
    return x, w, data_id


def extract_users(req):
    """Extracts user data and returns the user information and ranks."""
    exper_data, users = [], []
    for user in req["users"]:
        exper_data.append([float(data) for data in user["ranks"]])  # Convert ranks to float
        # Create User objects with their historical data if available
        if "history" in user:
            users.append(User(exper_data[-1], user["pid"], user["history"]))
        else:
            users.append(User(exper_data[-1], user["pid"]))  # Create User without history
    return exper_data, users


def send_data_as_json(teams):
    """Returns the team assignments as a JSON response."""
    json_obj = [[user.pid for user in team.members] for team in teams]  # Format the team data
    return flask.Response(
        json.dumps({"teams": json_obj, "users": flask.request.json["users"]}),  # Send JSON response
        mimetype="application/json",
    )


app = Flask(__name__)

# Route to handle team merging based on clustering
@app.route("/merge_teams", methods=["POST"])
def clstbuild():
    """Handles the /merge_teams route to build teams using clustering."""
    # Check for required fields in the request JSON
    if (
        not "users" in flask.request.json
        or not "max_team_size" in flask.request.json
        or sum(
            [
                not "ranks" in user or not "pid" in user
                for user in flask.request.json["users"]
            ]
        )
        > 0
    ):
        flask.abort(400)  # Return 400 error if the request is malformed
    data, users = extract_users(flask.request.json)
    # Assign teams using k-means clustering
    teams, users = clst.kmeans_assignment(
        data, users, flask.request.json["max_team_size"]
    )
    return send_data_as_json(teams)  # Return the assigned teams as a JSON response


# Route to handle team member swapping using top trading cycles
@app.route("/swap_team_members", methods=["POST"])
def ttctrading():
    """Handles the /swap_team_members route to swap team members using top trading cycles."""
    # Check for required fields in the request JSON
    if (
        not "users" in flask.request.json
        or not "teams" in flask.request.json
        or sum(
            [
                not "history" in user or not "ranks" in user or not "pid" in user
                for user in flask.request.json["users"]
            ]
        )
        > 0
    ):
        flask.abort(400)  # Return 400 error if the request is malformed
    users = extract_users(flask.request.json)[1]  # Extract the users from the request
    teams = [
        Team([User.user_with_pid(users, pid) for pid in data])  # Create teams using user PIDs
        for data in flask.request.json["teams"]
    ]
    ttc.team_swap(teams, users)  # Perform top trading cycle to swap team members
    return send_data_as_json(teams)  # Return the teams after swapping as a JSON response


if __name__ == "__main__":
    app.run(debug=True)  # Start the Flask application with debugging enabled
