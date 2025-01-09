import math
from user import User


def dist(p1, p2):
    """
    Calculate the Euclidean distance between two points.
    :param p1: First point (list of coordinates)
    :param p2: Second point (list of coordinates)
    :return: Euclidean distance
    """
    return math.sqrt(sum([(p1[i] - p2[i]) ** 2 for i in range(len(p1))]))


class Team:
    def __init__(self, members):
        """
        Initialize a Team object.
        :param members: List of User objects in the team (default: empty list)
        """
        self.members = members

    def __str__(self):
        """Return a comma-separated string of team members' PIDs."""
        return ",".join([str(user) for user in self.members])

    def users_to_pawn(self, extra_users=[]):
        """
        Find users in the team who have worked with others in the team before.
        :param extra_users: Additional users to consider
        :return: List of users who have worked with others in the team
        """
        users = []
        combined_users = self.members + extra_users

        for member in combined_users:
            if member is None:  # Skip if member is None
                continue
            for team_member in combined_users:
                if (
                    team_member is None or member is team_member
                ):  # Skip None or self-comparisons
                    continue
                if User.worked_with(member, team_member):
                    users.append(member)
                    break  # No need to check further for this member; move to the next one
        return users

    def centroid_value(self):
        """
        Calculate the centroid of the team's topic preferences.
        :return: List of average topic preferences for the team
        """
        return [
            sum([member.topic_rank[topic] for member in self.members])
            / len(self.members)
            for topic in range(len(self.members[0].topic_rank))
        ]

    def take_user_from(self, team, user):
        """
        Move a user from another team to this team.
        :param team: The source team
        :param user: User to transfer
        """
        self.members.append(team.members.pop(team.members.index(user)))

    def merge_with_team(self, team):
        """
        Merge another team into this team.
        :param team: Team to merge
        """
        self.members.extend(team.members)

    def user_prefs(self, users):
        """
        Sort users by their preference to join this team.
        :param users: List of User objects
        :return: Sorted list of users based on proximity to the team's centroid
        """
        return sorted(
            users,
            key=lambda user: (
                dist(self.centroid_value(), user.topic_rank),
                user in self.users_to_pawn([user]),
            ),
        )

    def team_prefs(self, teams):
        """
        Sort teams by their proximity to this team's centroid.
        :param teams: List of Team objects
        :return: Sorted list of teams
        """
        return sorted(
            teams, key=lambda team: dist(self.centroid_value(), team.centroid_value())
        )

    @staticmethod
    def team_with_user(teams, user):
        """
        Find the team that contains a specific user.
        :param teams: List of Team objects
        :param user: User to search for
        :return: Team object if found, else None
        """
        return next((team for team in teams if user in team.members), None)
