from rest_framework.response import Response


class CustomResponse(Response):
    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        if status is None:
            status = 200 if not exception else 500
        if status < 400:
            data = {
                "status": "success",
                "data": data
            }
        else:
            data = {
                "status": "error",
                "data": data
            }
        super().__init__(data, status, template_name, headers, exception, content_type)