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
import multiprocessing
import os
import json
from browserstack_sdk.bstack1ll1l1l11_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1ll11l1l1_opy_
class bstack11l1l11ll_opy_:
    def __init__(self, args, logger, bstack11llllllll_opy_, bstack11llllll11_opy_):
        self.args = args
        self.logger = logger
        self.bstack11llllllll_opy_ = bstack11llllllll_opy_
        self.bstack11llllll11_opy_ = bstack11llllll11_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1ll1111l1_opy_ = []
        self.bstack11lllll1l1_opy_ = None
        self.bstack1l1l11lll_opy_ = []
        self.bstack11lllll11l_opy_ = self.bstack1l1l1l111l_opy_()
        self.bstack1l1ll1ll1l_opy_ = -1
    def bstack1lll1ll11l_opy_(self, bstack11llll1lll_opy_):
        self.parse_args()
        self.bstack11lllll1ll_opy_()
        self.bstack11llll1l1l_opy_(bstack11llll1lll_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack11llll1l11_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l1ll1ll1l_opy_ = -1
        if bstack1lllll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫළ") in self.bstack11llllllll_opy_:
            self.bstack1l1ll1ll1l_opy_ = int(self.bstack11llllllll_opy_[bstack1lllll1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬෆ")])
        try:
            bstack11llllll1l_opy_ = [bstack1lllll1_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨ෇"), bstack1lllll1_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪ෈"), bstack1lllll1_opy_ (u"ࠨ࠯ࡳࠫ෉")]
            if self.bstack1l1ll1ll1l_opy_ >= 0:
                bstack11llllll1l_opy_.extend([bstack1lllll1_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵ්ࠪ"), bstack1lllll1_opy_ (u"ࠪ࠱ࡳ࠭෋")])
            for arg in bstack11llllll1l_opy_:
                self.bstack11llll1l11_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11lllll1ll_opy_(self):
        bstack11lllll1l1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11lllll1l1_opy_ = bstack11lllll1l1_opy_
        return bstack11lllll1l1_opy_
    def bstack1ll1l111ll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack11lllll111_opy_ = importlib.find_loader(bstack1lllll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭෌"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1ll11l1l1_opy_)
    def bstack11llll1l1l_opy_(self, bstack11llll1lll_opy_):
        bstack1l1lll1ll_opy_ = Config.get_instance()
        if bstack11llll1lll_opy_:
            self.bstack11lllll1l1_opy_.append(bstack1lllll1_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ෍"))
            self.bstack11lllll1l1_opy_.append(bstack1lllll1_opy_ (u"࠭ࡔࡳࡷࡨࠫ෎"))
        if bstack1l1lll1ll_opy_.bstack11llll1ll1_opy_():
            self.bstack11lllll1l1_opy_.append(bstack1lllll1_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ා"))
            self.bstack11lllll1l1_opy_.append(bstack1lllll1_opy_ (u"ࠨࡖࡵࡹࡪ࠭ැ"))
        self.bstack11lllll1l1_opy_.append(bstack1lllll1_opy_ (u"ࠩ࠰ࡴࠬෑ"))
        self.bstack11lllll1l1_opy_.append(bstack1lllll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠨි"))
        self.bstack11lllll1l1_opy_.append(bstack1lllll1_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭ී"))
        self.bstack11lllll1l1_opy_.append(bstack1lllll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬු"))
        if self.bstack1l1ll1ll1l_opy_ > 1:
            self.bstack11lllll1l1_opy_.append(bstack1lllll1_opy_ (u"࠭࠭࡯ࠩ෕"))
            self.bstack11lllll1l1_opy_.append(str(self.bstack1l1ll1ll1l_opy_))
    def bstack1l1111111l_opy_(self):
        bstack1l1l11lll_opy_ = []
        for spec in self.bstack1ll1111l1_opy_:
            bstack1l1ll111l1_opy_ = [spec]
            bstack1l1ll111l1_opy_ += self.bstack11lllll1l1_opy_
            bstack1l1l11lll_opy_.append(bstack1l1ll111l1_opy_)
        self.bstack1l1l11lll_opy_ = bstack1l1l11lll_opy_
        return bstack1l1l11lll_opy_
    def bstack1l1l1l111l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11lllll11l_opy_ = True
            return True
        except Exception as e:
            self.bstack11lllll11l_opy_ = False
        return self.bstack11lllll11l_opy_
    def bstack11llllll1_opy_(self, bstack1l11111111_opy_, bstack1lll1ll11l_opy_):
        bstack1lll1ll11l_opy_[bstack1lllll1_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧූ")] = self.bstack11llllllll_opy_
        multiprocessing.set_start_method(bstack1lllll1_opy_ (u"ࠨࡵࡳࡥࡼࡴࠧ෗"))
        if bstack1lllll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬෘ") in self.bstack11llllllll_opy_:
            bstack1lll1111l1_opy_ = []
            manager = multiprocessing.Manager()
            bstack11l1l111_opy_ = manager.list()
            for index, platform in enumerate(self.bstack11llllllll_opy_[bstack1lllll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ෙ")]):
                bstack1lll1111l1_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack1l11111111_opy_,
                                                           args=(self.bstack11lllll1l1_opy_, bstack1lll1ll11l_opy_, bstack11l1l111_opy_)))
            i = 0
            bstack11lllllll1_opy_ = len(self.bstack11llllllll_opy_[bstack1lllll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧේ")])
            for t in bstack1lll1111l1_opy_:
                os.environ[bstack1lllll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬෛ")] = str(i)
                os.environ[bstack1lllll1_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧො")] = json.dumps(self.bstack11llllllll_opy_[bstack1lllll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪෝ")][i % bstack11lllllll1_opy_])
                i += 1
                t.start()
            for t in bstack1lll1111l1_opy_:
                t.join()
            return list(bstack11l1l111_opy_)