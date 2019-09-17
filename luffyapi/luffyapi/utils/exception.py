# rest_framework.views 下的 exception_handler 处理了所有 drf可控范围内的异常
from rest_framework.views import exception_handler as drf_exception_handler
# drf的异常还是交给 drf_exception_handler，我们只需要处理 drf未处理的异常
from rest_framework.response import Response
from .response import APIResponse
# 自定义异常句柄的原因：要通过 logging 记录异常日志
from .logging import logger
def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is None:
        # drf处理不了的异常
        error_info = '【%s】【%s】' % (context['view'], exc)
        logger.error(error_info)
        # return Response({
        #     'exception': '服务器异常',
        # }, status=500)
        return APIResponse(1, '服务器异常', status=500)

    response.exception = True
    return response

