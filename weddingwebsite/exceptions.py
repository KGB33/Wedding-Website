class NoContentProvided(TypeError):
    """ Raised when No Content is provided for an email. """

    pass


class TooManyMembersError(Exception):
    """ Raised when a member is added to a full group """

    pass
