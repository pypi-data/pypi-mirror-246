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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11lllll111_opy_, bstack11llllll11_opy_):
        self.args = args
        self.logger = logger
        self.bstack11lllll111_opy_ = bstack11lllll111_opy_
        self.bstack11llllll11_opy_ = bstack11llllll11_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l11111lll_opy_(bstack11llll11ll_opy_):
        bstack11llll11l1_opy_ = []
        if bstack11llll11ll_opy_:
            tokens = str(os.path.basename(bstack11llll11ll_opy_)).split(bstack1ll1l11_opy_ (u"ࠨ࡟ࠣ෸"))
            camelcase_name = bstack1ll1l11_opy_ (u"ࠢࠡࠤ෹").join(t.title() for t in tokens)
            suite_name, bstack1lllll1111_opy_ = os.path.splitext(camelcase_name)
            bstack11llll11l1_opy_.append(suite_name)
        return bstack11llll11l1_opy_
    @staticmethod
    def bstack11llll1l11_opy_(typename):
        if bstack1ll1l11_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦ෺") in typename:
            return bstack1ll1l11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥ෻")
        return bstack1ll1l11_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦ෼")