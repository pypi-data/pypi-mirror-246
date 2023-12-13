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
import sys
class bstack1l11l11111_opy_:
    def __init__(self, handler):
        self._11ll1l1l1l_opy_ = sys.stdout.write
        self._11ll1l1ll1_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11ll1l1l11_opy_
        sys.stdout.error = self.bstack11ll1l1lll_opy_
    def bstack11ll1l1l11_opy_(self, _str):
        self._11ll1l1l1l_opy_(_str)
        if self.handler:
            self.handler({bstack1lllll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ๺"): bstack1lllll1_opy_ (u"ࠫࡎࡔࡆࡐࠩ๻"), bstack1lllll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭๼"): _str})
    def bstack11ll1l1lll_opy_(self, _str):
        self._11ll1l1ll1_opy_(_str)
        if self.handler:
            self.handler({bstack1lllll1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ๽"): bstack1lllll1_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭๾"), bstack1lllll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ๿"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11ll1l1l1l_opy_
        sys.stderr.write = self._11ll1l1ll1_opy_