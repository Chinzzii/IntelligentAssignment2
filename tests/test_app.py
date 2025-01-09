import unittest
import json
from app import app


class TeamTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test client for the Flask application."""
        self.app = app.test_client()
        self.app.testing = True

    def test_merge_teams(self):
        """Test the /merge_teams route with K-means clustering."""
        # Input data for the test
        data = {
            "users": [
                {"ranks": [1, 0, 2, 3], "pid": 1023},
                {"ranks": [1, 2, 0, 3], "pid": 4535},
                {"ranks": [0, 2, 3, 1], "pid": 1363},
                {"ranks": [2, 1, 0, 3], "pid": 9841},
            ],
            "max_team_size": 4,
        }

        # Make a POST request to /merge_teams
        response = self.app.post(
            "/merge_teams", data=json.dumps(data), content_type="application/json"
        )

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the correct teams in the output
        response_data = json.loads(response.data)
        expected_teams = [[1363, 9841], [1023, 4535]]
        self.assertEqual(response_data["teams"], expected_teams)

    def test_swap_team_members(self):
        """Test the /swap_team_members route with Top Trading Cycles."""
        # Input data for the test
        data = {
            "users": [
                {"ranks": [1, 0, 2, 3], "history": [4535, 9841, 9843], "pid": 1023},
                {"ranks": [1, 2, 0, 3], "history": [1023, 9843, 8542], "pid": 4535},
                {"ranks": [0, 2, 3, 1], "history": [3649, 9841, 9843], "pid": 1363},
                {"ranks": [2, 1, 0, 3], "history": [1363, 1023, 3649], "pid": 9841},
            ],
            "teams": [
                [1023, 2549],
                [4535, 9843],
                [1363, 1867, 3649],
                [9841, 8542, 7521],
            ],
        }

        # Make a POST request to /swap_team_members
        response = self.app.post(
            "/swap_team_members", data=json.dumps(data), content_type="application/json"
        )

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the correct swapped teams in the output
        response_data = json.loads(response.data)
        expected_teams = [[9841, 4535], [1023, 1363]]
        self.assertEqual(response_data["teams"], expected_teams)

    def test_invalid_input(self):
        """Test for invalid input to trigger 400 Bad Request."""
        # Missing users field
        invalid_data = {"max_team_size": 4}
        response = self.app.post(
            "/merge_teams",
            data=json.dumps(invalid_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        # Missing teams field
        invalid_data = {"users": [{"ranks": [1, 0, 2, 3], "pid": 1023}]}
        response = self.app.post(
            "/swap_team_members",
            data=json.dumps(invalid_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
