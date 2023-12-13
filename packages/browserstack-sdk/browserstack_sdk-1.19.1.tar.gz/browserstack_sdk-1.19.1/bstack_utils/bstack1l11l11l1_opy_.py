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
from collections import deque
from bstack_utils.constants import *
class bstack1lll1ll11l_opy_:
    def __init__(self):
        self._1111llllll_opy_ = deque()
        self._111l111111_opy_ = {}
        self._111l11l1ll_opy_ = False
    def bstack1111lllll1_opy_(self, test_name, bstack111l1111l1_opy_):
        bstack111l111ll1_opy_ = self._111l111111_opy_.get(test_name, {})
        return bstack111l111ll1_opy_.get(bstack111l1111l1_opy_, 0)
    def bstack111l11l1l1_opy_(self, test_name, bstack111l1111l1_opy_):
        bstack111l111l11_opy_ = self.bstack1111lllll1_opy_(test_name, bstack111l1111l1_opy_)
        self.bstack111l11l11l_opy_(test_name, bstack111l1111l1_opy_)
        return bstack111l111l11_opy_
    def bstack111l11l11l_opy_(self, test_name, bstack111l1111l1_opy_):
        if test_name not in self._111l111111_opy_:
            self._111l111111_opy_[test_name] = {}
        bstack111l111ll1_opy_ = self._111l111111_opy_[test_name]
        bstack111l111l11_opy_ = bstack111l111ll1_opy_.get(bstack111l1111l1_opy_, 0)
        bstack111l111ll1_opy_[bstack111l1111l1_opy_] = bstack111l111l11_opy_ + 1
    def bstack111ll11l1_opy_(self, bstack111l1111ll_opy_, bstack111l11l111_opy_):
        bstack1111llll1l_opy_ = self.bstack111l11l1l1_opy_(bstack111l1111ll_opy_, bstack111l11l111_opy_)
        bstack111l111lll_opy_ = bstack11ll11llll_opy_[bstack111l11l111_opy_]
        bstack111l111l1l_opy_ = bstack11l1ll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦ፳").format(bstack111l1111ll_opy_, bstack111l111lll_opy_, bstack1111llll1l_opy_)
        self._1111llllll_opy_.append(bstack111l111l1l_opy_)
    def bstack1l1ll1lll1_opy_(self):
        return len(self._1111llllll_opy_) == 0
    def bstack11lll111l_opy_(self):
        bstack111l11111l_opy_ = self._1111llllll_opy_.popleft()
        return bstack111l11111l_opy_
    def capturing(self):
        return self._111l11l1ll_opy_
    def bstack1llll111l_opy_(self):
        self._111l11l1ll_opy_ = True
    def bstack11l1l11l1_opy_(self):
        self._111l11l1ll_opy_ = False