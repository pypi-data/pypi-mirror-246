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
import sys
class bstack1l111l1lll_opy_:
    def __init__(self, handler):
        self._11ll1l11l1_opy_ = sys.stdout.write
        self._11ll1l1l11_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11ll1l11ll_opy_
        sys.stdout.error = self.bstack11ll1l1l1l_opy_
    def bstack11ll1l11ll_opy_(self, _str):
        self._11ll1l11l1_opy_(_str)
        if self.handler:
            self.handler({bstack11l1ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ๺"): bstack11l1ll_opy_ (u"ࠫࡎࡔࡆࡐࠩ๻"), bstack11l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭๼"): _str})
    def bstack11ll1l1l1l_opy_(self, _str):
        self._11ll1l1l11_opy_(_str)
        if self.handler:
            self.handler({bstack11l1ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ๽"): bstack11l1ll_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭๾"), bstack11l1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ๿"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11ll1l11l1_opy_
        sys.stderr.write = self._11ll1l1l11_opy_