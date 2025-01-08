import scipy.cluster.vq as clst
import numpy as np
from user import User
from team import Team
import team
import weights as w

def get_clusters(points):
    """
    Perform 2-means clustering on the points.
    :param points: List of points (users' topic weights with an added index)
    :return: Two clusters of points
    """
    # Exclude the index in the last column when clustering
    centroids = clst.kmeans(np.array([point[:-1] for point in points]), 2)[0].tolist()
    c1, c2 = ([], [])
    # If two centroids are found, divide points into two clusters
    if len(centroids) == 2:
        for point in points:
            if team.dist(centroids[0], point[:-1]) < team.dist(centroids[1], point[:-1]):
                c1.append(point)
            else:
                c2.append(point)
        return [c1, c2]
    else:  # If only one centroid, split points manually
        split = len(points) // 2
        return [points[:split], points[split:]]

def build_teams(people, teams, max_size):
    """
    Recursively split users into clusters until each cluster size <= max_size.
    :param people: List of users or data points
    :param teams: List to store the resulting teams
    :param max_size: Maximum number of users per team
    """
    if len(people) <= max_size:
        teams.append(people)
        return
    clusters = get_clusters(people)
    build_teams(clusters[0], teams, max_size)
    build_teams(clusters[1], teams, max_size)

def kmeans_assignment(exper_data, users, max_size):
    """
    Assign users to teams using k-means clustering.
    :param exper_data: 2D list of user topic preferences
    :param users: List of User objects
    :param max_size: Maximum number of users per team
    :return: Tuple of (teams, users)
    """
    assignments = []
    weights = w.find_weights(exper_data, max_size)
    weights.append(0)  # Append 0 for topics with no bids
    # Transform exper_data to weighted values
    exper_data = [[weights[int(data) - 1] for data in row] for row in exper_data]

    # Identify users who did not bid for any topics
    unbidded_users = [users[i] for i in range(len(exper_data)) if sum(exper_data[i]) == 0]
    print(f"{len(unbidded_users)} student(s) who did not bid any topics.")
    for user in unbidded_users:
        print(user.pid)

    # Add index to each row in exper_data for user identification
    build_teams(
        [exper_data[i] + [i] for i in range(len(exper_data))], assignments, max_size
    )

    # Create Team objects from assignments
    teams = [Team([users[user[-1]] for user in group]) for group in assignments]

    # Merge smaller teams if possible
    for team in teams:
        for other_team in team.team_prefs(teams):
            if (
                team is not other_team
                and len(team.members) + len(other_team.members) <= max_size
            ):
                team.merge_with_team(teams.pop(teams.index(other_team)))
    return teams, users
