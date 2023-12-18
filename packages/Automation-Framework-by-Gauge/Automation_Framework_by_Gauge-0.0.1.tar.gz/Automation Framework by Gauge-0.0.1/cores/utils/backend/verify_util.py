from cores.utils.common.assertion_util import MultiAssertsUtil
from cores.model.request import ResponseObj
from cores.const.api import RequestConst


class VerifyResultUtil:

    @staticmethod
    def verify_request_succesfully(response: ResponseObj):
        verify = MultiAssertsUtil()
        verify.assert_equal(response.status_code, RequestConst.StatusCode.OK)
        verify.assert_equal(response.message, RequestConst.Message.OK)
