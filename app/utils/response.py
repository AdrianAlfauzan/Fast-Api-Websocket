def success_response(data=None, message="Success", code=200, meta=None):
    response = {
        "success": True,
        "data": data,
        "message": message,
        "code": code,
    }
    if meta:
        response["meta"] = meta
    return response


def error_response(message="Error", code=400, errors=None):
    return {
        "success": False,
        "data": None,
        "message": message,
        "code": code,
        "errors": errors,
    }