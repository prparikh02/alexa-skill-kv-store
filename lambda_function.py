def lambda_handler(event, context):
    session = event['session']
    request = event['request']
    print(get_user_id(session))


def get_user_id(session):
    return session['user']['userId']
