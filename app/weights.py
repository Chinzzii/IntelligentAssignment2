def get_col(data, pos):
    """
    Extract a specific column from a 2D list.
    :param data: 2D list of data
    :param pos: Column index to extract
    :return: List of values in the specified column
    """
    return [val[pos] for val in data]


def find_costs(data, max_team_size, max_priority):
    """
    Calculate the costs for each priority level.
    :param data: 2D list of preferences (rows: users, columns: topics)
    :param max_team_size: Maximum number of users per team
    :param max_priority: Maximum priority level (e.g., 1 is highest)
    :return: List of costs for each priority level
    """
    costs = []
    for priority in range(max_priority):
        val = []
        for col in range(len(data[0])):
            selection = get_col(data, col)
            if selection.count(priority + 1) > 0:
                val.append(abs(max_team_size - selection.count(priority + 1)))
        if sum(val) == 0:
            val.append(1)  # Prevent division by zero
        costs.append(float(sum(val)) / (max_team_size * len(val)))
    return costs


def find_benefit(max_priority, current_priority, data, max_team_size):
    """
    Calculate the benefit for a given priority level.
    :param max_priority: Maximum priority level
    :param current_priority: Current priority level
    :param data: 2D list of preferences (rows: users, columns: topics)
    :param max_team_size: Maximum number of users per team
    :return: Benefit value
    """
    benefit = []
    for col in range(len(data[0])):
        selection = get_col(data, col)
        if selection.count(current_priority) > max_team_size:
            benefit.append(max_team_size)
        else:
            benefit.append(selection.count(current_priority))
    return (float(max_priority) / current_priority) * (float(sum(benefit)) / len(data))


def find_weights(data, max_team_size):
    """
    Calculate the weights for each priority level.
    :param data: 2D list of preferences (rows: users, columns: topics)
    :param max_team_size: Maximum number of users per team
    :return: List of weights for each priority level
    """
    weights = []
    max_priority = max(
        max(map(int, user)) for user in data
    )  # Find the highest priority
    costs = find_costs(data, max_team_size, max_priority)
    for priority in range(max_priority):
        weights.append(
            find_benefit(max_priority, priority + 1, data, max_team_size)
            / costs[priority]
        )
    return weights
