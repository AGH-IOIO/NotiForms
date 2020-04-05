from flask import Response, jsonify

class ValidatorErr(object):
    def __init__(self, message, code=400):
        self._message = message
        self._code = code

    def __call__(self):
        response = jsonify({"error": self._message})
        response.status_code = self._code
        return response

def mk_error(message, code=400):
    return ValidatorErr(message, code)

def if_unlocked(decorated):
    def func(self, *args, **kwargs):
        if not self.locked:
            return decorated(self, *args, **kwargs)
        return None
    return func

class Validator(object):
    def __init__(self, request):
        self._request = request
        self._response = None
        self._locked = False

    @property
    def locked(self):
        return self._locked

    def error(self):
        if self._response is None or not self._locked:
            return None
        return self._response

    @if_unlocked
    def field_present(self, key, err=None):
        body = self._request.json
        if key in body:
            return True

        if err is None:
            msg = "Required field '%s' is not present." % key
            err = mk_error(msg, 400)

        self._response = err()
        self._locked = True

        return False

    @if_unlocked
    def field_predicate(self, key, predicate, err=None):
        body = self._request.json
        if key not in body:
            return True

        value = body[key]
        if predicate(value) is True:
            return True

        if err is None:
            msg = "Field '%s' does not match predicate." % key
            err = mk_error(msg, 400)

        self._response = err()
        self._locked = True

        return False
