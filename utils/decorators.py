from rest_framework.response import Response
from rest_framework import status
from functools import wraps


def required_params(method='GET', params=None):
    if params is None:
        params = []

    def decorator(view_func):
        """
        decorator 函数通过 wraps 来将 view_func 里的参数解析出来传递给 _wrapped_view
        这里的 instance 参数其实就是在 view_func 里的 self
        """
        @wraps(view_func)
        def _wrapped_view(instance, request, *args, **kwargs):
            if method.lower() == 'get':
                data = request.query_params
            else:
                data = request.data
            missing_params = [
                param
                for param in params
                if param not in data
            ]
            if missing_params:
                params_str = ','.join(missing_params)
                return Response({
                    'message': u'missing {} in request'.format(params_str),
                    'success': False,
                }, status=status.HTTP_400_BAD_REQUEST)
            # 做完检测之后，再去调用被 @required_params 包裹起来的 view_func
            return view_func(instance, request, *args, **kwargs)
        return _wrapped_view
    return decorator
