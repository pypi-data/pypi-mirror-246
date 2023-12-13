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
import threading
bstack1111l11ll1_opy_ = 1000
bstack11111lllll_opy_ = 5
bstack1111l11l1l_opy_ = 30
bstack1111l1111l_opy_ = 2
class bstack1111l111ll_opy_:
    def __init__(self, handler, bstack11111llll1_opy_=bstack1111l11ll1_opy_, bstack11111lll11_opy_=bstack11111lllll_opy_):
        self.queue = []
        self.handler = handler
        self.bstack11111llll1_opy_ = bstack11111llll1_opy_
        self.bstack11111lll11_opy_ = bstack11111lll11_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1111l111l1_opy_()
    def bstack1111l111l1_opy_(self):
        self.timer = threading.Timer(self.bstack11111lll11_opy_, self.bstack1111l11lll_opy_)
        self.timer.start()
    def bstack11111lll1l_opy_(self):
        self.timer.cancel()
    def bstack1111l11111_opy_(self):
        self.bstack11111lll1l_opy_()
        self.bstack1111l111l1_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack11111llll1_opy_:
                t = threading.Thread(target=self.bstack1111l11lll_opy_)
                t.start()
                self.bstack1111l11111_opy_()
    def bstack1111l11lll_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack11111llll1_opy_]
        del self.queue[:self.bstack11111llll1_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack11111lll1l_opy_()
        while len(self.queue) > 0:
            self.bstack1111l11lll_opy_()