# coding: UTF-8
import sys
bstack1l1111_opy_ = sys.version_info [0] == 2
bstack111llll_opy_ = 2048
bstack1lll1_opy_ = 7
def bstack11l1ll_opy_ (bstack1l1l11l_opy_):
    global bstack11l1ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11l1l_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack1l1l1l1_opy_ % len (bstack11l1l_opy_)
    bstack11111_opy_ = bstack11l1l_opy_ [:bstack1lll1l1_opy_] + bstack11l1l_opy_ [bstack1lll1l1_opy_:]
    if bstack1l1111_opy_:
        bstack11ll1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111llll_opy_ - (bstack11l1111_opy_ + bstack1l1l1l1_opy_) % bstack1lll1_opy_) for bstack11l1111_opy_, char in enumerate (bstack11111_opy_)])
    else:
        bstack11ll1ll_opy_ = str () .join ([chr (ord (char) - bstack111llll_opy_ - (bstack11l1111_opy_ + bstack1l1l1l1_opy_) % bstack1lll1_opy_) for bstack11l1111_opy_, char in enumerate (bstack11111_opy_)])
    return eval (bstack11ll1ll_opy_)
class bstack1lll1lll_opy_:
    def __init__(self, handler):
        self._11111ll1ll_opy_ = None
        self.handler = handler
        self._11111ll11l_opy_ = self.bstack11111ll111_opy_()
        self.patch()
    def patch(self):
        self._11111ll1ll_opy_ = self._11111ll11l_opy_.execute
        self._11111ll11l_opy_.execute = self.bstack11111ll1l1_opy_()
    def bstack11111ll1l1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11l1ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢᏌ"), driver_command)
            response = self._11111ll1ll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11l1ll_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢᏍ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._11111ll11l_opy_.execute = self._11111ll1ll_opy_
    @staticmethod
    def bstack11111ll111_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver