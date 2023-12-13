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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11lllll11l_opy_, bstack11llll11ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11lllll11l_opy_ = bstack11lllll11l_opy_
        self.bstack11llll11ll_opy_ = bstack11llll11ll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l11111l11_opy_(bstack11lll1llll_opy_):
        bstack11llll111l_opy_ = []
        if bstack11lll1llll_opy_:
            tokens = str(os.path.basename(bstack11lll1llll_opy_)).split(bstack11l1ll_opy_ (u"ࠣࡡࠥෞ"))
            camelcase_name = bstack11l1ll_opy_ (u"ࠤࠣࠦෟ").join(t.title() for t in tokens)
            suite_name, bstack1l11lll11_opy_ = os.path.splitext(camelcase_name)
            bstack11llll111l_opy_.append(suite_name)
        return bstack11llll111l_opy_
    @staticmethod
    def bstack11llll1111_opy_(typename):
        if bstack11l1ll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ෠") in typename:
            return bstack11l1ll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧ෡")
        return bstack11l1ll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨ෢")