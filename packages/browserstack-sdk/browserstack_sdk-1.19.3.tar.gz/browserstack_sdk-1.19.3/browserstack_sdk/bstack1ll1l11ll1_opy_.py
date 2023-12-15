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
import multiprocessing
import os
import json
from browserstack_sdk.bstack1ll1l1l11l_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l1llll111_opy_
class bstack1l11l1ll_opy_:
    def __init__(self, args, logger, bstack11lllll111_opy_, bstack11llllll11_opy_):
        self.args = args
        self.logger = logger
        self.bstack11lllll111_opy_ = bstack11lllll111_opy_
        self.bstack11llllll11_opy_ = bstack11llllll11_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11ll11l1l_opy_ = []
        self.bstack11llllll1l_opy_ = None
        self.bstack1lll1lll1_opy_ = []
        self.bstack11llllllll_opy_ = self.bstack1lll1llll1_opy_()
        self.bstack1llllll11_opy_ = -1
    def bstack1l1l11111_opy_(self, bstack11llll1lll_opy_):
        self.parse_args()
        self.bstack11lllllll1_opy_()
        self.bstack11llll1ll1_opy_(bstack11llll1lll_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack1l111111l1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1llllll11_opy_ = -1
        if bstack1ll1l11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩෟ") in self.bstack11lllll111_opy_:
            self.bstack1llllll11_opy_ = int(self.bstack11lllll111_opy_[bstack1ll1l11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ෠")])
        try:
            bstack11llll1l1l_opy_ = [bstack1ll1l11_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭෡"), bstack1ll1l11_opy_ (u"ࠬ࠳࠭ࡱ࡮ࡸ࡫࡮ࡴࡳࠨ෢"), bstack1ll1l11_opy_ (u"࠭࠭ࡱࠩ෣")]
            if self.bstack1llllll11_opy_ >= 0:
                bstack11llll1l1l_opy_.extend([bstack1ll1l11_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ෤"), bstack1ll1l11_opy_ (u"ࠨ࠯ࡱࠫ෥")])
            for arg in bstack11llll1l1l_opy_:
                self.bstack1l111111l1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11lllllll1_opy_(self):
        bstack11llllll1l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11llllll1l_opy_ = bstack11llllll1l_opy_
        return bstack11llllll1l_opy_
    def bstack11111ll1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack11lllll11l_opy_ = importlib.find_loader(bstack1ll1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫ෦"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l1llll111_opy_)
    def bstack11llll1ll1_opy_(self, bstack11llll1lll_opy_):
        bstack111lll1ll_opy_ = Config.get_instance()
        if bstack11llll1lll_opy_:
            self.bstack11llllll1l_opy_.append(bstack1ll1l11_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ෧"))
            self.bstack11llllll1l_opy_.append(bstack1ll1l11_opy_ (u"࡙ࠫࡸࡵࡦࠩ෨"))
        if bstack111lll1ll_opy_.bstack11lllll1ll_opy_():
            self.bstack11llllll1l_opy_.append(bstack1ll1l11_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ෩"))
            self.bstack11llllll1l_opy_.append(bstack1ll1l11_opy_ (u"࠭ࡔࡳࡷࡨࠫ෪"))
        self.bstack11llllll1l_opy_.append(bstack1ll1l11_opy_ (u"ࠧ࠮ࡲࠪ෫"))
        self.bstack11llllll1l_opy_.append(bstack1ll1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭෬"))
        self.bstack11llllll1l_opy_.append(bstack1ll1l11_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫ෭"))
        self.bstack11llllll1l_opy_.append(bstack1ll1l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ෮"))
        if self.bstack1llllll11_opy_ > 1:
            self.bstack11llllll1l_opy_.append(bstack1ll1l11_opy_ (u"ࠫ࠲ࡴࠧ෯"))
            self.bstack11llllll1l_opy_.append(str(self.bstack1llllll11_opy_))
    def bstack11lllll1l1_opy_(self):
        bstack1lll1lll1_opy_ = []
        for spec in self.bstack11ll11l1l_opy_:
            bstack1ll1l1l111_opy_ = [spec]
            bstack1ll1l1l111_opy_ += self.bstack11llllll1l_opy_
            bstack1lll1lll1_opy_.append(bstack1ll1l1l111_opy_)
        self.bstack1lll1lll1_opy_ = bstack1lll1lll1_opy_
        return bstack1lll1lll1_opy_
    def bstack1lll1llll1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11llllllll_opy_ = True
            return True
        except Exception as e:
            self.bstack11llllllll_opy_ = False
        return self.bstack11llllllll_opy_
    def bstack1l1l1l111l_opy_(self, bstack1l11111111_opy_, bstack1l1l11111_opy_):
        bstack1l1l11111_opy_[bstack1ll1l11_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬ෰")] = self.bstack11lllll111_opy_
        multiprocessing.set_start_method(bstack1ll1l11_opy_ (u"࠭ࡳࡱࡣࡺࡲࠬ෱"))
        if bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪෲ") in self.bstack11lllll111_opy_:
            bstack1l1ll11111_opy_ = []
            manager = multiprocessing.Manager()
            bstack111l11l1_opy_ = manager.list()
            for index, platform in enumerate(self.bstack11lllll111_opy_[bstack1ll1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫෳ")]):
                bstack1l1ll11111_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack1l11111111_opy_,
                                                           args=(self.bstack11llllll1l_opy_, bstack1l1l11111_opy_, bstack111l11l1_opy_)))
            i = 0
            bstack1l1111111l_opy_ = len(self.bstack11lllll111_opy_[bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ෴")])
            for t in bstack1l1ll11111_opy_:
                os.environ[bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ෵")] = str(i)
                os.environ[bstack1ll1l11_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬ෶")] = json.dumps(self.bstack11lllll111_opy_[bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ෷")][i % bstack1l1111111l_opy_])
                i += 1
                t.start()
            for t in bstack1l1ll11111_opy_:
                t.join()
            return list(bstack111l11l1_opy_)