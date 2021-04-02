def api_return(message, is_error=False, data={}):
    return {
        'error': is_error,
        'message': message,
        'data': data
    }
