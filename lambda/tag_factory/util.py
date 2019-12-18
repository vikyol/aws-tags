
def get_user(event):
    detail = event['detail']
    principal = detail['userIdentity'].get('principalId', None)

    if not detail:
        return None

    user_type = detail['userIdentity']['type']

    if user_type == 'IAMUser':
        return detail['userIdentity']['userName']
    elif user_type == 'AWSService':
        return detail['userIdentity']['invokedBy']
    else:
        return principal.split(':')[1]