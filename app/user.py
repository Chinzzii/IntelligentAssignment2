class User:
    def __init__(self, topic_rank, pid, history=None):
        """
        Initialize a User object.
        :param topic_rank: List of topic preferences (1: most preferred, 0: no preference)
        :param pid: Unique ID for the user
        :param history: List of previously worked-with team members' PIDs (default: empty list)
        """
        self.topic_rank = topic_rank
        self.pid = pid
        self.history = history if history else []

    def __str__(self):
        """Return the user's PID as a string."""
        return str(self.pid)

    @staticmethod
    def worked_with(user1, user2):
        """
        Check if user1 has worked with user2 before.
        :param user1: First user
        :param user2: Second user
        :return: True if they have worked together, else False
        """
        return user2.pid in user1.history

    @staticmethod
    def user_with_pid(users, pid):
        """
        Find a user by their PID from a list of users.
        :param users: List of User objects
        :param pid: PID to search for
        :return: User object if found, else None
        """
        return next((user for user in users if user.pid == pid), None)
