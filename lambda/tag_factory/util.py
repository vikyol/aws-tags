
def get_user(event):
    detail = event['detail']

    if not detail:
        return None

    user_type = detail['userIdentity']['type']

    if user_type == 'IAMUser':
        return detail['userIdentity']['userName']
    else:
        return principal.split(':')[1]