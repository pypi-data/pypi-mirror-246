# coding: UTF-8
import sys
bstack1l1ll1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1lllll1l_opy_ (bstack11l1ll_opy_):
    global bstack1l11_opy_
    bstack1l1l1_opy_ = ord (bstack11l1ll_opy_ [-1])
    bstack1llllll_opy_ = bstack11l1ll_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1_opy_ % len (bstack1llllll_opy_)
    bstack1llll1_opy_ = bstack1llllll_opy_ [:bstack11llll_opy_] + bstack1llllll_opy_ [bstack11llll_opy_:]
    if bstack1l1ll1l_opy_:
        bstack11l11l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack1l1l1ll_opy_ + bstack1l1l1_opy_) % bstack1l11l11_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack11l11l1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack1l1l1ll_opy_ + bstack1l1l1_opy_) % bstack1l11l11_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack11l11l1_opy_)
class bstack11lllllll_opy_:
    def __init__(self, handler):
        self._11111llll1_opy_ = None
        self.handler = handler
        self._11111lllll_opy_ = self.bstack11111lll1l_opy_()
        self.patch()
    def patch(self):
        self._11111llll1_opy_ = self._11111lllll_opy_.execute
        self._11111lllll_opy_.execute = self.bstack11111lll11_opy_()
    def bstack11111lll11_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1lllll1l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࠧᏦ"), driver_command)
            response = self._11111llll1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1lllll1l_opy_ (u"ࠨࡡࡧࡶࡨࡶࠧᏧ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._11111lllll_opy_.execute = self._11111llll1_opy_
    @staticmethod
    def bstack11111lll1l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver