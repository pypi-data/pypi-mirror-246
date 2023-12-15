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
import sys
class bstack1l111111ll_opy_:
    def __init__(self, handler):
        self._11ll1l1l1l_opy_ = sys.stdout.write
        self._11ll1ll111_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11ll1l1lll_opy_
        sys.stdout.error = self.bstack11ll1l1ll1_opy_
    def bstack11ll1l1lll_opy_(self, _str):
        self._11ll1l1l1l_opy_(_str)
        if self.handler:
            self.handler({bstack1ll1l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧດ"): bstack1ll1l11_opy_ (u"ࠩࡌࡒࡋࡕࠧຕ"), bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫຖ"): _str})
    def bstack11ll1l1ll1_opy_(self, _str):
        self._11ll1ll111_opy_(_str)
        if self.handler:
            self.handler({bstack1ll1l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪທ"): bstack1ll1l11_opy_ (u"ࠬࡋࡒࡓࡑࡕࠫຘ"), bstack1ll1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧນ"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11ll1l1l1l_opy_
        sys.stderr.write = self._11ll1ll111_opy_