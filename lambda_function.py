import boto3

# DynamoDB Attributes
USER_ID = 'UserId'
INFO_KEY = 'InfoKey'
INFO_VALUE = 'InfoValue'
REQUEST_ID = 'RequestId'
REQUEST_BLOB = 'RequestBlob'
TIMESTAMP = 'Timestamp'

# DynamoDB resources
dynamodb = boto3.resource('dynamodb')
requests_table = dynamodb.Table('AlexaSkillKVStore-Requests-NA')
data_table = dynamodb.Table('AlexaSkillKVStore-UserData-NA')


class AbstractIntentHandler(object):
    SLOT_INFO_KEY = 'info_key'
    SLOT_INFO_VALUE = 'info_value'

    def handle(self, user_id, request):
        raise NotImplementedError('Use handle() method of child class')

    def _get_slot_value(self, slot_name, request):
        return request['intent']['slots'][slot_name]['value']


class PutKeyValueIntentHandler(AbstractIntentHandler):
    def handle(self, user_id, request):
        item = self._create_user_data_item(user_id, request)
        data_table.put_item(
            Item=item
        )

        response_text = 'Saving the value {} as {}'.format(
            item[INFO_VALUE],
            item[INFO_KEY]
        )
        response_card_title = 'Saving value as {}'.format(item[INFO_KEY])

        return create_response(
            speech_text=response_text,
            card_content=response_text,
            card_title=response_card_title
        )

    def _create_user_data_item(self, user_id, request):
        return {
            USER_ID: user_id,
            INFO_KEY: self._get_slot_value(self.SLOT_INFO_KEY, request),
            INFO_VALUE: self._get_slot_value(self.SLOT_INFO_VALUE, request),
            REQUEST_ID: request['requestId'],
            TIMESTAMP: request['timestamp'],
        }


class GetValueIntentHandler(AbstractIntentHandler):
    def handle(self, user_id, request):
        info_key = self._get_slot_value(self.SLOT_INFO_KEY, request)
        ddb_response = data_table.get_item(
            Key={
                USER_ID: user_id,
                INFO_KEY: info_key
            }
        )

        response_text = 'The value stored for {} is {}'.format(
            info_key,
            ddb_response['Item'][INFO_VALUE]
        )
        response_card_title = 'Value for {}'.format(info_key)

        return create_response(
            speech_text=response_text,
            card_content=response_text,
            card_title=response_card_title
        )


def create_response(speech_text, card_content, card_title):
    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': speech_text
            },
            'card': {
                'type': 'Simple',
                'content': card_content,
                'title': card_title
            },
        },
        'sessionAttributes': {}
    }


def resolve_intent_handler(request):
    intent_name = request['intent']['name']
    if intent_name == 'PutKeyValueIntent':
        return PutKeyValueIntentHandler()
    elif intent_name == 'GetValueIntent':
        return GetValueIntentHandler()

    raise ValueError('Unrecognized intent: {}'.format(intent_name))


def get_user_id(session):
    return session['user']['userId']


def lambda_handler(event, context):
    session = event['session']
    request = event['request']

    user_id = get_user_id(session)
    return resolve_intent_handler(request).handle(user_id, request)
