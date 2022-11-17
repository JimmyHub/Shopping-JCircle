import json


def get_serializer_data(viewset_obj, data, request, partial=False):
    viewset_obj.serializer = viewset_obj.get_serializer(data=data, context={'request': request}, partial=partial)
    viewset_obj.serializer.is_valid(raise_exception=True)


def get_json_data(data):
    if not data:
        return SystemError('請重新發送欲傳送資料')
    return json.loads(data)