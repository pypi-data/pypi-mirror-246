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
import sys
class bstack1l11111ll1_opy_:
    def __init__(self, handler):
        self._11ll1ll111_opy_ = sys.stdout.write
        self._11ll1ll1l1_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11ll1l1lll_opy_
        sys.stdout.error = self.bstack11ll1ll11l_opy_
    def bstack11ll1l1lll_opy_(self, _str):
        self._11ll1ll111_opy_(_str)
        if self.handler:
            self.handler({bstack1lllll1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧດ"): bstack1lllll1l_opy_ (u"ࠩࡌࡒࡋࡕࠧຕ"), bstack1lllll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫຖ"): _str})
    def bstack11ll1ll11l_opy_(self, _str):
        self._11ll1ll1l1_opy_(_str)
        if self.handler:
            self.handler({bstack1lllll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪທ"): bstack1lllll1l_opy_ (u"ࠬࡋࡒࡓࡑࡕࠫຘ"), bstack1lllll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧນ"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11ll1ll111_opy_
        sys.stderr.write = self._11ll1ll1l1_opy_