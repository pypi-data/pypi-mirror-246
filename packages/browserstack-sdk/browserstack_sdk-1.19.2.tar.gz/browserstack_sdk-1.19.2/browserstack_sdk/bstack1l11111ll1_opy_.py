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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11llllllll_opy_, bstack11llllll11_opy_):
        self.args = args
        self.logger = logger
        self.bstack11llllllll_opy_ = bstack11llllllll_opy_
        self.bstack11llllll11_opy_ = bstack11llllll11_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l11ll1l11_opy_(bstack11llll11l1_opy_):
        bstack11llll11ll_opy_ = []
        if bstack11llll11l1_opy_:
            tokens = str(os.path.basename(bstack11llll11l1_opy_)).split(bstack1lllll1_opy_ (u"ࠣࡡࠥෞ"))
            camelcase_name = bstack1lllll1_opy_ (u"ࠤࠣࠦෟ").join(t.title() for t in tokens)
            suite_name, bstack1ll1lll1l1_opy_ = os.path.splitext(camelcase_name)
            bstack11llll11ll_opy_.append(suite_name)
        return bstack11llll11ll_opy_
    @staticmethod
    def bstack11llll111l_opy_(typename):
        if bstack1lllll1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ෠") in typename:
            return bstack1lllll1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧ෡")
        return bstack1lllll1_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨ෢")