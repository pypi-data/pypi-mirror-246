# coding: UTF-8
import sys
bstack1l11l1_opy_ = sys.version_info [0] == 2
bstack111ll_opy_ = 2048
bstack11llll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack1lllll1_opy_):
    global bstack1l11l11_opy_
    bstack1111l1l_opy_ = ord (bstack1lllll1_opy_ [-1])
    bstack111l1ll_opy_ = bstack1lllll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack1111l1l_opy_ % len (bstack111l1ll_opy_)
    bstack1111ll1_opy_ = bstack111l1ll_opy_ [:bstack1lllll1l_opy_] + bstack111l1ll_opy_ [bstack1lllll1l_opy_:]
    if bstack1l11l1_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll_opy_ - (bstack1ll1l_opy_ + bstack1111l1l_opy_) % bstack11llll1_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1111ll1_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack111ll_opy_ - (bstack1ll1l_opy_ + bstack1111l1l_opy_) % bstack11llll1_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1111ll1_opy_)])
    return eval (bstack1llll11_opy_)
class bstack1l1l1l1l11_opy_:
    def __init__(self, handler):
        self._11111lll1l_opy_ = None
        self.handler = handler
        self._11111ll1l1_opy_ = self.bstack11111lll11_opy_()
        self.patch()
    def patch(self):
        self._11111lll1l_opy_ = self._11111ll1l1_opy_.execute
        self._11111ll1l1_opy_.execute = self.bstack11111ll1ll_opy_()
    def bstack11111ll1ll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1ll1l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࠧᏦ"), driver_command)
            response = self._11111lll1l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1ll1l11_opy_ (u"ࠨࡡࡧࡶࡨࡶࠧᏧ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._11111ll1l1_opy_.execute = self._11111lll1l_opy_
    @staticmethod
    def bstack11111lll11_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver