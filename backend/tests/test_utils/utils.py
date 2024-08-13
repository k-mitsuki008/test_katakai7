import json


def get_event(query_string_parameters: any = None, body: any = None, path_parameters: any = None, gigya_uid: any = None, path: any = None, headers: any = None) -> dict:

    event = {
        'queryStringParameters': query_string_parameters,
        'body': json.dumps(body) if body else '{}',
        'pathParameters': path_parameters,
        'path': path,
        'requestContext': {
            'authorizer': {
                'gigya_uid': gigya_uid
            }
        },
        'headers': headers
    }
    return event


def get_authorizer_event():
    event = {
        'type': 'TOKEN',
        'methodArn': 'arn:aws:execute-api:eu-west-1:889185496976:8kl2w1h6qf/v1/POST/vehicles/12345/shop',
        'authorizationToken': 'test_session_01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        'headers': {'device_id': 'test'}
    }
    return event
