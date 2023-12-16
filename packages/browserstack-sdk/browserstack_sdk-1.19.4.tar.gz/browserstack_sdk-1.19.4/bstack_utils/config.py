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
conf = {
    bstack1lllll1l_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ບ"): False,
    bstack1lllll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩປ"): True,
    bstack1lllll1l_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠨຜ"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._11ll1l1ll1_opy_ = conf
    @classmethod
    def get_instance(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name):
        return self._11ll1l1ll1_opy_.get(property_name, None)
    def bstack11111l1l1_opy_(self, property_name, bstack11ll1l1l1l_opy_):
        self._11ll1l1ll1_opy_[property_name] = bstack11ll1l1l1l_opy_
    def bstack1l1l1l1l1_opy_(self, val):
        self._11ll1l1ll1_opy_[bstack1lllll1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠩຝ")] = bool(val)
    def bstack11llllllll_opy_(self):
        return self._11ll1l1ll1_opy_.get(bstack1lllll1l_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠪພ"), False)