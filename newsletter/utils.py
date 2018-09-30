from django.utils.crypto import get_random_string


# Possible actions that user can perform
ACTIONS = ('subscribe', 'unsubscribe', 'update')

def make_activation_code():
    """ Generate a unique activation code. """

    return get_random_string(length=40)
