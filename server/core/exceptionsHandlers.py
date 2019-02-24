from rest_framework.views import exception_handler

def ApplnExceptionHandler(exc, context):
    """
    Custom Application exception handler responding for 5xx errors
    in elegance manner and with integrity.
    """
    response = exception_handler(exc, context)

    if response != None:
        data = response.data.copy()
        response.data.clear()
        new_response = response.data['data'] = dict()
        if 'detail' in data.keys():
            new_response['message'] = data['detail']
        if 'error' in data.keys():
            new_response['message'] = 'INTERNAL_SERVER_ERROR'
            new_response['error'] = data.get('error')
    return response