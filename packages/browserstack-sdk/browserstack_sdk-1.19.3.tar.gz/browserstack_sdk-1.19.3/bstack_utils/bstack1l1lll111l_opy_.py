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
from collections import deque
from bstack_utils.constants import *
class bstack1l1lll1l11_opy_:
    def __init__(self):
        self._111l111l1l_opy_ = deque()
        self._111l111111_opy_ = {}
        self._111l11l1ll_opy_ = False
    def bstack111l111l11_opy_(self, test_name, bstack111l111ll1_opy_):
        bstack111l11ll11_opy_ = self._111l111111_opy_.get(test_name, {})
        return bstack111l11ll11_opy_.get(bstack111l111ll1_opy_, 0)
    def bstack111l11111l_opy_(self, test_name, bstack111l111ll1_opy_):
        bstack111l111lll_opy_ = self.bstack111l111l11_opy_(test_name, bstack111l111ll1_opy_)
        self.bstack1111llllll_opy_(test_name, bstack111l111ll1_opy_)
        return bstack111l111lll_opy_
    def bstack1111llllll_opy_(self, test_name, bstack111l111ll1_opy_):
        if test_name not in self._111l111111_opy_:
            self._111l111111_opy_[test_name] = {}
        bstack111l11ll11_opy_ = self._111l111111_opy_[test_name]
        bstack111l111lll_opy_ = bstack111l11ll11_opy_.get(bstack111l111ll1_opy_, 0)
        bstack111l11ll11_opy_[bstack111l111ll1_opy_] = bstack111l111lll_opy_ + 1
    def bstack1llll1llll_opy_(self, bstack111l11l111_opy_, bstack111l11l11l_opy_):
        bstack111l1111ll_opy_ = self.bstack111l11111l_opy_(bstack111l11l111_opy_, bstack111l11l11l_opy_)
        bstack111l11ll1l_opy_ = bstack11ll1l111l_opy_[bstack111l11l11l_opy_]
        bstack111l1111l1_opy_ = bstack1ll1l11_opy_ (u"ࠢࡼࡿ࠰ࡿࢂ࠳ࡻࡾࠤᎍ").format(bstack111l11l111_opy_, bstack111l11ll1l_opy_, bstack111l1111ll_opy_)
        self._111l111l1l_opy_.append(bstack111l1111l1_opy_)
    def bstack11l1lll11_opy_(self):
        return len(self._111l111l1l_opy_) == 0
    def bstack1lllll111l_opy_(self):
        bstack111l11l1l1_opy_ = self._111l111l1l_opy_.popleft()
        return bstack111l11l1l1_opy_
    def capturing(self):
        return self._111l11l1ll_opy_
    def bstack1l1ll1111_opy_(self):
        self._111l11l1ll_opy_ = True
    def bstack1ll1l1l1_opy_(self):
        self._111l11l1ll_opy_ = False