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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11lllll111_opy_, bstack11llllll1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack11lllll111_opy_ = bstack11lllll111_opy_
        self.bstack11llllll1l_opy_ = bstack11llllll1l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l11l11l11_opy_(bstack11llll1ll1_opy_):
        bstack11llll1l11_opy_ = []
        if bstack11llll1ll1_opy_:
            tokens = str(os.path.basename(bstack11llll1ll1_opy_)).split(bstack1lllll1l_opy_ (u"ࠨ࡟ࠣ෸"))
            camelcase_name = bstack1lllll1l_opy_ (u"ࠢࠡࠤ෹").join(t.title() for t in tokens)
            suite_name, bstack11l1llll_opy_ = os.path.splitext(camelcase_name)
            bstack11llll1l11_opy_.append(suite_name)
        return bstack11llll1l11_opy_
    @staticmethod
    def bstack11llll1l1l_opy_(typename):
        if bstack1lllll1l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦ෺") in typename:
            return bstack1lllll1l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥ෻")
        return bstack1lllll1l_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦ෼")