class NotFoundUsersRepositoryException(Exception):
    pass


class UsersRepositoryException(Exception):
    pass


class CreateUserCommandException(Exception):
    pass


class GetUserQueryException(Exception):
    pass


class NotFoundGetUserQueryException(Exception):
    pass
