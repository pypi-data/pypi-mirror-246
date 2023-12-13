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
from collections import deque
from bstack_utils.constants import *
class bstack1l1l1l1l1l_opy_:
    def __init__(self):
        self._111l11ll11_opy_ = deque()
        self._111l11l1l1_opy_ = {}
        self._1111llllll_opy_ = False
    def bstack111l111ll1_opy_(self, test_name, bstack111l1111l1_opy_):
        bstack111l11l1ll_opy_ = self._111l11l1l1_opy_.get(test_name, {})
        return bstack111l11l1ll_opy_.get(bstack111l1111l1_opy_, 0)
    def bstack111l1111ll_opy_(self, test_name, bstack111l1111l1_opy_):
        bstack111l111l1l_opy_ = self.bstack111l111ll1_opy_(test_name, bstack111l1111l1_opy_)
        self.bstack111l11111l_opy_(test_name, bstack111l1111l1_opy_)
        return bstack111l111l1l_opy_
    def bstack111l11111l_opy_(self, test_name, bstack111l1111l1_opy_):
        if test_name not in self._111l11l1l1_opy_:
            self._111l11l1l1_opy_[test_name] = {}
        bstack111l11l1ll_opy_ = self._111l11l1l1_opy_[test_name]
        bstack111l111l1l_opy_ = bstack111l11l1ll_opy_.get(bstack111l1111l1_opy_, 0)
        bstack111l11l1ll_opy_[bstack111l1111l1_opy_] = bstack111l111l1l_opy_ + 1
    def bstack1ll11l1l_opy_(self, bstack111l111111_opy_, bstack111l111lll_opy_):
        bstack111l11l111_opy_ = self.bstack111l1111ll_opy_(bstack111l111111_opy_, bstack111l111lll_opy_)
        bstack111l11l11l_opy_ = bstack11ll11l11l_opy_[bstack111l111lll_opy_]
        bstack111l111l11_opy_ = bstack1lllll1_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦ፳").format(bstack111l111111_opy_, bstack111l11l11l_opy_, bstack111l11l111_opy_)
        self._111l11ll11_opy_.append(bstack111l111l11_opy_)
    def bstack1lll1ll1_opy_(self):
        return len(self._111l11ll11_opy_) == 0
    def bstack111111ll_opy_(self):
        bstack111l11ll1l_opy_ = self._111l11ll11_opy_.popleft()
        return bstack111l11ll1l_opy_
    def capturing(self):
        return self._1111llllll_opy_
    def bstack1lll1lllll_opy_(self):
        self._1111llllll_opy_ = True
    def bstack11l111ll_opy_(self):
        self._1111llllll_opy_ = False