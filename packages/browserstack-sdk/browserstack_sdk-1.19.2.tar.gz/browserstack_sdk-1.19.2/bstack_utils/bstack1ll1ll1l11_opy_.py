# coding: UTF-8
import sys
bstack1ll_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack1111l1l_opy_ = 7
def bstack1lllll1_opy_ (bstack111ll1l_opy_):
    global bstackl_opy_
    bstack1l1l11_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1llll1l_opy_ = bstack111ll1l_opy_ [:-1]
    bstack1111l_opy_ = bstack1l1l11_opy_ % len (bstack1llll1l_opy_)
    bstack1111ll1_opy_ = bstack1llll1l_opy_ [:bstack1111l_opy_] + bstack1llll1l_opy_ [bstack1111l_opy_:]
    if bstack1ll_opy_:
        bstack11l1l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack1l111_opy_ + bstack1l1l11_opy_) % bstack1111l1l_opy_) for bstack1l111_opy_, char in enumerate (bstack1111ll1_opy_)])
    else:
        bstack11l1l1l_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack1l111_opy_ + bstack1l1l11_opy_) % bstack1111l1l_opy_) for bstack1l111_opy_, char in enumerate (bstack1111ll1_opy_)])
    return eval (bstack11l1l1l_opy_)
class bstack1l1lll1lll_opy_:
    def __init__(self, handler):
        self._11111ll1ll_opy_ = None
        self.handler = handler
        self._11111lll1l_opy_ = self.bstack11111lll11_opy_()
        self.patch()
    def patch(self):
        self._11111ll1ll_opy_ = self._11111lll1l_opy_.execute
        self._11111lll1l_opy_.execute = self.bstack11111ll1l1_opy_()
    def bstack11111ll1l1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1lllll1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢᏌ"), driver_command)
            response = self._11111ll1ll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1lllll1_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢᏍ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._11111lll1l_opy_.execute = self._11111ll1ll_opy_
    @staticmethod
    def bstack11111lll11_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver