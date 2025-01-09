from user import User
from team import Team


def detect_cycles(graph):
    """Detects cycles in the given graph and returns all unique cycles."""
    cycles = []
    for key in graph.keys():
        skey, ckey, cycle = (key, key, [])  # Start and current key
        while ckey not in cycle:  # Loop until a cycle is detected
            cycle.append(ckey)
            ckey = graph[ckey][0]  # Move to the next user/team in the cycle
        if skey == ckey and sorted(cycle) not in cycles:  # Check if cycle is valid
            cycles.append(sorted(cycle))  # Add the cycle to the list
    return cycles


def top_trading_cycles(teams, users):
    """Performs the top trading cycles algorithm for matching teams and users."""
    while teams:
        graph = {}
        for team in teams:
            for user in team.user_prefs(users):
                # Match team to user if they are part of the same preference set
                if Team.team_with_user(teams, user):
                    graph[team] = (Team.team_with_user(teams, user), user)
                    break
        cycles = detect_cycles(graph)  # Detect cycles in the graph
        for cycle in cycles:
            for team in cycle:
                # Swap users among teams in the cycle
                team.take_user_from(graph[team][0], graph[team][1])
            for team in cycle:
                # Remove teams from the list after the swap
                teams.pop(teams.index(team))


def team_swap(teams, users):
    """Performs team swaps based on the top trading cycles algorithm."""
    auct_users, auct_teams = ([], [])  # Users and teams available for swapping
    for team in teams:
        if team.users_to_pawn():  # Check if team has users to pawn
            auct_users = auct_users + team.users_to_pawn()  # Add users to auction list
            auct_teams.append(team)  # Add team to auction list
    top_trading_cycles(
        auct_teams, auct_users
    )  # Perform top trading cycles on the selected teams and users
