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
import multiprocessing
import os
import json
from browserstack_sdk.bstack111lll11l_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l11ll11l_opy_
class bstack1l1111l1l_opy_:
    def __init__(self, args, logger, bstack11lllll111_opy_, bstack11llllll1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack11lllll111_opy_ = bstack11lllll111_opy_
        self.bstack11llllll1l_opy_ = bstack11llllll1l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1ll1lll11_opy_ = []
        self.bstack1l1111111l_opy_ = None
        self.bstack1ll1lll1ll_opy_ = []
        self.bstack11llll1lll_opy_ = self.bstack1lllll11_opy_()
        self.bstack1ll1l111l_opy_ = -1
    def bstack1l1lll1l1_opy_(self, bstack11lllll1l1_opy_):
        self.parse_args()
        self.bstack11lllll11l_opy_()
        self.bstack1l111111l1_opy_(bstack11lllll1l1_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack1l11111l11_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1ll1l111l_opy_ = -1
        if bstack1lllll1l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩෟ") in self.bstack11lllll111_opy_:
            self.bstack1ll1l111l_opy_ = int(self.bstack11lllll111_opy_[bstack1lllll1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ෠")])
        try:
            bstack1l11111111_opy_ = [bstack1lllll1l_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭෡"), bstack1lllll1l_opy_ (u"ࠬ࠳࠭ࡱ࡮ࡸ࡫࡮ࡴࡳࠨ෢"), bstack1lllll1l_opy_ (u"࠭࠭ࡱࠩ෣")]
            if self.bstack1ll1l111l_opy_ >= 0:
                bstack1l11111111_opy_.extend([bstack1lllll1l_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ෤"), bstack1lllll1l_opy_ (u"ࠨ࠯ࡱࠫ෥")])
            for arg in bstack1l11111111_opy_:
                self.bstack1l11111l11_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11lllll11l_opy_(self):
        bstack1l1111111l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1l1111111l_opy_ = bstack1l1111111l_opy_
        return bstack1l1111111l_opy_
    def bstack1l11llll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack11lllllll1_opy_ = importlib.find_loader(bstack1lllll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫ෦"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l11ll11l_opy_)
    def bstack1l111111l1_opy_(self, bstack11lllll1l1_opy_):
        bstack1ll1ll1l1_opy_ = Config.get_instance()
        if bstack11lllll1l1_opy_:
            self.bstack1l1111111l_opy_.append(bstack1lllll1l_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ෧"))
            self.bstack1l1111111l_opy_.append(bstack1lllll1l_opy_ (u"࡙ࠫࡸࡵࡦࠩ෨"))
        if bstack1ll1ll1l1_opy_.bstack11llllllll_opy_():
            self.bstack1l1111111l_opy_.append(bstack1lllll1l_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ෩"))
            self.bstack1l1111111l_opy_.append(bstack1lllll1l_opy_ (u"࠭ࡔࡳࡷࡨࠫ෪"))
        self.bstack1l1111111l_opy_.append(bstack1lllll1l_opy_ (u"ࠧ࠮ࡲࠪ෫"))
        self.bstack1l1111111l_opy_.append(bstack1lllll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭෬"))
        self.bstack1l1111111l_opy_.append(bstack1lllll1l_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫ෭"))
        self.bstack1l1111111l_opy_.append(bstack1lllll1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ෮"))
        if self.bstack1ll1l111l_opy_ > 1:
            self.bstack1l1111111l_opy_.append(bstack1lllll1l_opy_ (u"ࠫ࠲ࡴࠧ෯"))
            self.bstack1l1111111l_opy_.append(str(self.bstack1ll1l111l_opy_))
    def bstack11llllll11_opy_(self):
        bstack1ll1lll1ll_opy_ = []
        for spec in self.bstack1ll1lll11_opy_:
            bstack1llll111l_opy_ = [spec]
            bstack1llll111l_opy_ += self.bstack1l1111111l_opy_
            bstack1ll1lll1ll_opy_.append(bstack1llll111l_opy_)
        self.bstack1ll1lll1ll_opy_ = bstack1ll1lll1ll_opy_
        return bstack1ll1lll1ll_opy_
    def bstack1lllll11_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11llll1lll_opy_ = True
            return True
        except Exception as e:
            self.bstack11llll1lll_opy_ = False
        return self.bstack11llll1lll_opy_
    def bstack1l1l1lll1_opy_(self, bstack11lllll1ll_opy_, bstack1l1lll1l1_opy_):
        bstack1l1lll1l1_opy_[bstack1lllll1l_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬ෰")] = self.bstack11lllll111_opy_
        multiprocessing.set_start_method(bstack1lllll1l_opy_ (u"࠭ࡳࡱࡣࡺࡲࠬ෱"))
        if bstack1lllll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪෲ") in self.bstack11lllll111_opy_:
            bstack1ll1l1111_opy_ = []
            manager = multiprocessing.Manager()
            bstack111111l1l_opy_ = manager.list()
            for index, platform in enumerate(self.bstack11lllll111_opy_[bstack1lllll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫෳ")]):
                bstack1ll1l1111_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack11lllll1ll_opy_,
                                                           args=(self.bstack1l1111111l_opy_, bstack1l1lll1l1_opy_, bstack111111l1l_opy_)))
            i = 0
            bstack1l111111ll_opy_ = len(self.bstack11lllll111_opy_[bstack1lllll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ෴")])
            for t in bstack1ll1l1111_opy_:
                os.environ[bstack1lllll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ෵")] = str(i)
                os.environ[bstack1lllll1l_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬ෶")] = json.dumps(self.bstack11lllll111_opy_[bstack1lllll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ෷")][i % bstack1l111111ll_opy_])
                i += 1
                t.start()
            for t in bstack1ll1l1111_opy_:
                t.join()
            return list(bstack111111l1l_opy_)