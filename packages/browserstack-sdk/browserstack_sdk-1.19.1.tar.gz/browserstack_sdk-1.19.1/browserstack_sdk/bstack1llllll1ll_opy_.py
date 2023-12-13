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
import multiprocessing
import os
import json
from browserstack_sdk.bstack1lll1llll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1llll1l1_opy_
class bstack1l1lll11_opy_:
    def __init__(self, args, logger, bstack11lllll11l_opy_, bstack11llll11ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11lllll11l_opy_ = bstack11lllll11l_opy_
        self.bstack11llll11ll_opy_ = bstack11llll11ll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11111llll_opy_ = []
        self.bstack11llll1l11_opy_ = None
        self.bstack1l1lllll_opy_ = []
        self.bstack11llll1lll_opy_ = self.bstack1llll1l1l_opy_()
        self.bstack111lll1l_opy_ = -1
    def bstack1l1lll1l1_opy_(self, bstack11llllll1l_opy_):
        self.parse_args()
        self.bstack11llll1ll1_opy_()
        self.bstack11lllllll1_opy_(bstack11llllll1l_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack11llll1l1l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack111lll1l_opy_ = -1
        if bstack11l1ll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫළ") in self.bstack11lllll11l_opy_:
            self.bstack111lll1l_opy_ = int(self.bstack11lllll11l_opy_[bstack11l1ll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬෆ")])
        try:
            bstack11llllllll_opy_ = [bstack11l1ll_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨ෇"), bstack11l1ll_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪ෈"), bstack11l1ll_opy_ (u"ࠨ࠯ࡳࠫ෉")]
            if self.bstack111lll1l_opy_ >= 0:
                bstack11llllllll_opy_.extend([bstack11l1ll_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵ්ࠪ"), bstack11l1ll_opy_ (u"ࠪ࠱ࡳ࠭෋")])
            for arg in bstack11llllllll_opy_:
                self.bstack11llll1l1l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11llll1ll1_opy_(self):
        bstack11llll1l11_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11llll1l11_opy_ = bstack11llll1l11_opy_
        return bstack11llll1l11_opy_
    def bstack1ll1lllll1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack11llll11l1_opy_ = importlib.find_loader(bstack11l1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭෌"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1llll1l1_opy_)
    def bstack11lllllll1_opy_(self, bstack11llllll1l_opy_):
        bstack1ll1l11ll1_opy_ = Config.get_instance()
        if bstack11llllll1l_opy_:
            self.bstack11llll1l11_opy_.append(bstack11l1ll_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ෍"))
            self.bstack11llll1l11_opy_.append(bstack11l1ll_opy_ (u"࠭ࡔࡳࡷࡨࠫ෎"))
        if bstack1ll1l11ll1_opy_.bstack11llllll11_opy_():
            self.bstack11llll1l11_opy_.append(bstack11l1ll_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ා"))
            self.bstack11llll1l11_opy_.append(bstack11l1ll_opy_ (u"ࠨࡖࡵࡹࡪ࠭ැ"))
        self.bstack11llll1l11_opy_.append(bstack11l1ll_opy_ (u"ࠩ࠰ࡴࠬෑ"))
        self.bstack11llll1l11_opy_.append(bstack11l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠨි"))
        self.bstack11llll1l11_opy_.append(bstack11l1ll_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭ී"))
        self.bstack11llll1l11_opy_.append(bstack11l1ll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬු"))
        if self.bstack111lll1l_opy_ > 1:
            self.bstack11llll1l11_opy_.append(bstack11l1ll_opy_ (u"࠭࠭࡯ࠩ෕"))
            self.bstack11llll1l11_opy_.append(str(self.bstack111lll1l_opy_))
    def bstack11lllll111_opy_(self):
        bstack1l1lllll_opy_ = []
        for spec in self.bstack11111llll_opy_:
            bstack11l1ll1l_opy_ = [spec]
            bstack11l1ll1l_opy_ += self.bstack11llll1l11_opy_
            bstack1l1lllll_opy_.append(bstack11l1ll1l_opy_)
        self.bstack1l1lllll_opy_ = bstack1l1lllll_opy_
        return bstack1l1lllll_opy_
    def bstack1llll1l1l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11llll1lll_opy_ = True
            return True
        except Exception as e:
            self.bstack11llll1lll_opy_ = False
        return self.bstack11llll1lll_opy_
    def bstack1lllll1ll_opy_(self, bstack11lllll1ll_opy_, bstack1l1lll1l1_opy_):
        bstack1l1lll1l1_opy_[bstack11l1ll_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧූ")] = self.bstack11lllll11l_opy_
        multiprocessing.set_start_method(bstack11l1ll_opy_ (u"ࠨࡵࡳࡥࡼࡴࠧ෗"))
        if bstack11l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬෘ") in self.bstack11lllll11l_opy_:
            bstack1lll1ll1l1_opy_ = []
            manager = multiprocessing.Manager()
            bstack1lll1l1ll_opy_ = manager.list()
            for index, platform in enumerate(self.bstack11lllll11l_opy_[bstack11l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ෙ")]):
                bstack1lll1ll1l1_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack11lllll1ll_opy_,
                                                           args=(self.bstack11llll1l11_opy_, bstack1l1lll1l1_opy_, bstack1lll1l1ll_opy_)))
            i = 0
            bstack11lllll1l1_opy_ = len(self.bstack11lllll11l_opy_[bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧේ")])
            for t in bstack1lll1ll1l1_opy_:
                os.environ[bstack11l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬෛ")] = str(i)
                os.environ[bstack11l1ll_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧො")] = json.dumps(self.bstack11lllll11l_opy_[bstack11l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪෝ")][i % bstack11lllll1l1_opy_])
                i += 1
                t.start()
            for t in bstack1lll1ll1l1_opy_:
                t.join()
            return list(bstack1lll1l1ll_opy_)