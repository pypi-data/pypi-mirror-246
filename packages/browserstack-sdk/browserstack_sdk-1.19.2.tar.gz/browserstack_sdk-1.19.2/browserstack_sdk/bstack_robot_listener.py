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
import os
import datetime
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1l11111ll1_opy_ import RobotHandler
from bstack_utils.capture import bstack1l11l11111_opy_
from bstack_utils.bstack1l111ll11l_opy_ import bstack1l1l11111l_opy_, bstack1l11ll1l1l_opy_, bstack1l111l11ll_opy_
from bstack_utils.bstack1ll1l111_opy_ import bstack1ll1l111l_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11llll1l_opy_, bstack1ll1ll11l1_opy_, Result, \
    bstack1l11lll1l1_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack1lllll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ೹"): [],
        bstack1lllll1_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪ೺"): [],
        bstack1lllll1_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ೻"): []
    }
    bstack1l111l1lll_opy_ = []
    bstack1l11ll11ll_opy_ = []
    @staticmethod
    def bstack1l1111l11l_opy_(log):
        if not (log[bstack1lllll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ೼")] and log[bstack1lllll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ೽")].strip()):
            return
        active = bstack1ll1l111l_opy_.bstack1l11l11ll1_opy_()
        log = {
            bstack1lllll1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ೾"): log[bstack1lllll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ೿")],
            bstack1lllll1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ഀ"): datetime.datetime.utcnow().isoformat() + bstack1lllll1_opy_ (u"ࠫ࡟࠭ഁ"),
            bstack1lllll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ം"): log[bstack1lllll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧഃ")],
        }
        if active:
            if active[bstack1lllll1_opy_ (u"ࠧࡵࡻࡳࡩࠬഄ")] == bstack1lllll1_opy_ (u"ࠨࡪࡲࡳࡰ࠭അ"):
                log[bstack1lllll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩആ")] = active[bstack1lllll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪഇ")]
            elif active[bstack1lllll1_opy_ (u"ࠫࡹࡿࡰࡦࠩഈ")] == bstack1lllll1_opy_ (u"ࠬࡺࡥࡴࡶࠪഉ"):
                log[bstack1lllll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ഊ")] = active[bstack1lllll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧഋ")]
        bstack1ll1l111l_opy_.bstack1l11lllll1_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._1l111ll111_opy_ = None
        self._1l11l11l1l_opy_ = None
        self._1l111lll11_opy_ = OrderedDict()
        self.bstack1l111ll1l1_opy_ = bstack1l11l11111_opy_(self.bstack1l1111l11l_opy_)
    @bstack1l11lll1l1_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1l11llllll_opy_()
        if not self._1l111lll11_opy_.get(attrs.get(bstack1lllll1_opy_ (u"ࠨ࡫ࡧࠫഌ")), None):
            self._1l111lll11_opy_[attrs.get(bstack1lllll1_opy_ (u"ࠩ࡬ࡨࠬ഍"))] = {}
        bstack1l11l1l11l_opy_ = bstack1l111l11ll_opy_(
                bstack1l1111l1l1_opy_=attrs.get(bstack1lllll1_opy_ (u"ࠪ࡭ࡩ࠭എ")),
                name=name,
                bstack1l1111ll1l_opy_=bstack1ll1ll11l1_opy_(),
                file_path=os.path.relpath(attrs[bstack1lllll1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫഏ")], start=os.getcwd()) if attrs.get(bstack1lllll1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬഐ")) != bstack1lllll1_opy_ (u"࠭ࠧ഑") else bstack1lllll1_opy_ (u"ࠧࠨഒ"),
                framework=bstack1lllll1_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧഓ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1lllll1_opy_ (u"ࠩ࡬ࡨࠬഔ"), None)
        self._1l111lll11_opy_[attrs.get(bstack1lllll1_opy_ (u"ࠪ࡭ࡩ࠭ക"))][bstack1lllll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧഖ")] = bstack1l11l1l11l_opy_
    @bstack1l11lll1l1_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1l11l1ll11_opy_()
        self._1l11l1llll_opy_(messages)
        for bstack1l11111l1l_opy_ in self.bstack1l111l1lll_opy_:
            bstack1l11111l1l_opy_[bstack1lllll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧഗ")][bstack1lllll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬഘ")].extend(self.store[bstack1lllll1_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ങ")])
            bstack1ll1l111l_opy_.bstack1l111l1l11_opy_(bstack1l11111l1l_opy_)
        self.bstack1l111l1lll_opy_ = []
        self.store[bstack1lllll1_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧച")] = []
    @bstack1l11lll1l1_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1l111ll1l1_opy_.start()
        if not self._1l111lll11_opy_.get(attrs.get(bstack1lllll1_opy_ (u"ࠩ࡬ࡨࠬഛ")), None):
            self._1l111lll11_opy_[attrs.get(bstack1lllll1_opy_ (u"ࠪ࡭ࡩ࠭ജ"))] = {}
        driver = bstack11llll1l_opy_(threading.current_thread(), bstack1lllll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪഝ"), None)
        bstack1l111ll11l_opy_ = bstack1l111l11ll_opy_(
            bstack1l1111l1l1_opy_=attrs.get(bstack1lllll1_opy_ (u"ࠬ࡯ࡤࠨഞ")),
            name=name,
            bstack1l1111ll1l_opy_=bstack1ll1ll11l1_opy_(),
            file_path=os.path.relpath(attrs[bstack1lllll1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ട")], start=os.getcwd()),
            scope=RobotHandler.bstack1l11ll1l11_opy_(attrs.get(bstack1lllll1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧഠ"), None)),
            framework=bstack1lllll1_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧഡ"),
            tags=attrs[bstack1lllll1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧഢ")],
            hooks=self.store[bstack1lllll1_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩണ")],
            bstack1l11ll111l_opy_=bstack1ll1l111l_opy_.bstack1l11111l11_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1lllll1_opy_ (u"ࠦࢀࢃࠠ࡝ࡰࠣࡿࢂࠨത").format(bstack1lllll1_opy_ (u"ࠧࠦࠢഥ").join(attrs[bstack1lllll1_opy_ (u"࠭ࡴࡢࡩࡶࠫദ")]), name) if attrs[bstack1lllll1_opy_ (u"ࠧࡵࡣࡪࡷࠬധ")] else name
        )
        self._1l111lll11_opy_[attrs.get(bstack1lllll1_opy_ (u"ࠨ࡫ࡧࠫന"))][bstack1lllll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬഩ")] = bstack1l111ll11l_opy_
        threading.current_thread().current_test_uuid = bstack1l111ll11l_opy_.bstack1l111ll1ll_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1lllll1_opy_ (u"ࠪ࡭ࡩ࠭പ"), None)
        self.bstack1l111l1ll1_opy_(bstack1lllll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬഫ"), bstack1l111ll11l_opy_)
    @bstack1l11lll1l1_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1l111ll1l1_opy_.reset()
        bstack1l1111l1ll_opy_ = bstack1l1l1111l1_opy_.get(attrs.get(bstack1lllll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬബ")), bstack1lllll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧഭ"))
        self._1l111lll11_opy_[attrs.get(bstack1lllll1_opy_ (u"ࠧࡪࡦࠪമ"))][bstack1lllll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫയ")].stop(time=bstack1ll1ll11l1_opy_(), duration=int(attrs.get(bstack1lllll1_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧര"), bstack1lllll1_opy_ (u"ࠪ࠴ࠬറ"))), result=Result(result=bstack1l1111l1ll_opy_, exception=attrs.get(bstack1lllll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬല")), bstack1l1l111111_opy_=[attrs.get(bstack1lllll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ള"))]))
        self.bstack1l111l1ll1_opy_(bstack1lllll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨഴ"), self._1l111lll11_opy_[attrs.get(bstack1lllll1_opy_ (u"ࠧࡪࡦࠪവ"))][bstack1lllll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫശ")], True)
        self.store[bstack1lllll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ഷ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack1l11lll1l1_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1l11llllll_opy_()
        current_test_id = bstack11llll1l_opy_(threading.current_thread(), bstack1lllll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬസ"), None)
        bstack1l111lll1l_opy_ = current_test_id if bstack11llll1l_opy_(threading.current_thread(), bstack1lllll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ഹ"), None) else bstack11llll1l_opy_(threading.current_thread(), bstack1lllll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨഺ"), None)
        if attrs.get(bstack1lllll1_opy_ (u"࠭ࡴࡺࡲࡨ഻ࠫ"), bstack1lllll1_opy_ (u"ࠧࠨ഼")).lower() in [bstack1lllll1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧഽ"), bstack1lllll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫാ")]:
            hook_type = bstack1l11l1ll1l_opy_(attrs.get(bstack1lllll1_opy_ (u"ࠪࡸࡾࡶࡥࠨി")), bstack11llll1l_opy_(threading.current_thread(), bstack1lllll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨീ"), None))
            hook_name = bstack1lllll1_opy_ (u"ࠬࢁࡽࠨു").format(attrs.get(bstack1lllll1_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ൂ"), bstack1lllll1_opy_ (u"ࠧࠨൃ")))
            if hook_type in [bstack1lllll1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬൄ"), bstack1lllll1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ൅")]:
                hook_name = bstack1lllll1_opy_ (u"ࠪ࡟ࢀࢃ࡝ࠡࡽࢀࠫെ").format(bstack1l111lllll_opy_.get(hook_type), attrs.get(bstack1lllll1_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫേ"), bstack1lllll1_opy_ (u"ࠬ࠭ൈ")))
            bstack1l11ll11l1_opy_ = bstack1l11ll1l1l_opy_(
                bstack1l1111l1l1_opy_=bstack1l111lll1l_opy_ + bstack1lllll1_opy_ (u"࠭࠭ࠨ൉") + attrs.get(bstack1lllll1_opy_ (u"ࠧࡵࡻࡳࡩࠬൊ"), bstack1lllll1_opy_ (u"ࠨࠩോ")).lower(),
                name=hook_name,
                bstack1l1111ll1l_opy_=bstack1ll1ll11l1_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1lllll1_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩൌ")), start=os.getcwd()),
                framework=bstack1lllll1_opy_ (u"ࠪࡖࡴࡨ࡯ࡵ്ࠩ"),
                tags=attrs[bstack1lllll1_opy_ (u"ࠫࡹࡧࡧࡴࠩൎ")],
                scope=RobotHandler.bstack1l11ll1l11_opy_(attrs.get(bstack1lllll1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ൏"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1l11ll11l1_opy_.bstack1l111ll1ll_opy_()
            threading.current_thread().current_hook_id = bstack1l111lll1l_opy_ + bstack1lllll1_opy_ (u"࠭࠭ࠨ൐") + attrs.get(bstack1lllll1_opy_ (u"ࠧࡵࡻࡳࡩࠬ൑"), bstack1lllll1_opy_ (u"ࠨࠩ൒")).lower()
            self.store[bstack1lllll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭൓")] = [bstack1l11ll11l1_opy_.bstack1l111ll1ll_opy_()]
            if bstack11llll1l_opy_(threading.current_thread(), bstack1lllll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧൔ"), None):
                self.store[bstack1lllll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨൕ")].append(bstack1l11ll11l1_opy_.bstack1l111ll1ll_opy_())
            else:
                self.store[bstack1lllll1_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫൖ")].append(bstack1l11ll11l1_opy_.bstack1l111ll1ll_opy_())
            if bstack1l111lll1l_opy_:
                self._1l111lll11_opy_[bstack1l111lll1l_opy_ + bstack1lllll1_opy_ (u"࠭࠭ࠨൗ") + attrs.get(bstack1lllll1_opy_ (u"ࠧࡵࡻࡳࡩࠬ൘"), bstack1lllll1_opy_ (u"ࠨࠩ൙")).lower()] = { bstack1lllll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ൚"): bstack1l11ll11l1_opy_ }
            bstack1ll1l111l_opy_.bstack1l111l1ll1_opy_(bstack1lllll1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ൛"), bstack1l11ll11l1_opy_)
        else:
            bstack1l11lll11l_opy_ = {
                bstack1lllll1_opy_ (u"ࠫ࡮ࡪࠧ൜"): uuid4().__str__(),
                bstack1lllll1_opy_ (u"ࠬࡺࡥࡹࡶࠪ൝"): bstack1lllll1_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬ൞").format(attrs.get(bstack1lllll1_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧൟ")), attrs.get(bstack1lllll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ൠ"), bstack1lllll1_opy_ (u"ࠩࠪൡ"))) if attrs.get(bstack1lllll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨൢ"), []) else attrs.get(bstack1lllll1_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫൣ")),
                bstack1lllll1_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬ൤"): attrs.get(bstack1lllll1_opy_ (u"࠭ࡡࡳࡩࡶࠫ൥"), []),
                bstack1lllll1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ൦"): bstack1ll1ll11l1_opy_(),
                bstack1lllll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ൧"): bstack1lllll1_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ൨"),
                bstack1lllll1_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ൩"): attrs.get(bstack1lllll1_opy_ (u"ࠫࡩࡵࡣࠨ൪"), bstack1lllll1_opy_ (u"ࠬ࠭൫"))
            }
            if attrs.get(bstack1lllll1_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧ൬"), bstack1lllll1_opy_ (u"ࠧࠨ൭")) != bstack1lllll1_opy_ (u"ࠨࠩ൮"):
                bstack1l11lll11l_opy_[bstack1lllll1_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪ൯")] = attrs.get(bstack1lllll1_opy_ (u"ࠪࡰ࡮ࡨ࡮ࡢ࡯ࡨࠫ൰"))
            if not self.bstack1l11ll11ll_opy_:
                self._1l111lll11_opy_[self._1l11l111ll_opy_()][bstack1lllll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ൱")].add_step(bstack1l11lll11l_opy_)
                threading.current_thread().current_step_uuid = bstack1l11lll11l_opy_[bstack1lllll1_opy_ (u"ࠬ࡯ࡤࠨ൲")]
            self.bstack1l11ll11ll_opy_.append(bstack1l11lll11l_opy_)
    @bstack1l11lll1l1_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1l11l1ll11_opy_()
        self._1l11l1llll_opy_(messages)
        current_test_id = bstack11llll1l_opy_(threading.current_thread(), bstack1lllll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨ൳"), None)
        bstack1l111lll1l_opy_ = current_test_id if current_test_id else bstack11llll1l_opy_(threading.current_thread(), bstack1lllll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪ൴"), None)
        bstack1l111l111l_opy_ = bstack1l1l1111l1_opy_.get(attrs.get(bstack1lllll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ൵")), bstack1lllll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ൶"))
        bstack1l11llll1l_opy_ = attrs.get(bstack1lllll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ൷"))
        if bstack1l111l111l_opy_ != bstack1lllll1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ൸") and not attrs.get(bstack1lllll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭൹")) and self._1l111ll111_opy_:
            bstack1l11llll1l_opy_ = self._1l111ll111_opy_
        bstack1l11l11lll_opy_ = Result(result=bstack1l111l111l_opy_, exception=bstack1l11llll1l_opy_, bstack1l1l111111_opy_=[bstack1l11llll1l_opy_])
        if attrs.get(bstack1lllll1_opy_ (u"࠭ࡴࡺࡲࡨࠫൺ"), bstack1lllll1_opy_ (u"ࠧࠨൻ")).lower() in [bstack1lllll1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧർ"), bstack1lllll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫൽ")]:
            bstack1l111lll1l_opy_ = current_test_id if current_test_id else bstack11llll1l_opy_(threading.current_thread(), bstack1lllll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ൾ"), None)
            if bstack1l111lll1l_opy_:
                bstack1l1111llll_opy_ = bstack1l111lll1l_opy_ + bstack1lllll1_opy_ (u"ࠦ࠲ࠨൿ") + attrs.get(bstack1lllll1_opy_ (u"ࠬࡺࡹࡱࡧࠪ඀"), bstack1lllll1_opy_ (u"࠭ࠧඁ")).lower()
                self._1l111lll11_opy_[bstack1l1111llll_opy_][bstack1lllll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪං")].stop(time=bstack1ll1ll11l1_opy_(), duration=int(attrs.get(bstack1lllll1_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ඃ"), bstack1lllll1_opy_ (u"ࠩ࠳ࠫ඄"))), result=bstack1l11l11lll_opy_)
                bstack1ll1l111l_opy_.bstack1l111l1ll1_opy_(bstack1lllll1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬඅ"), self._1l111lll11_opy_[bstack1l1111llll_opy_][bstack1lllll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧආ")])
        else:
            bstack1l111lll1l_opy_ = current_test_id if current_test_id else bstack11llll1l_opy_(threading.current_thread(), bstack1lllll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣ࡮ࡪࠧඇ"), None)
            if bstack1l111lll1l_opy_ and len(self.bstack1l11ll11ll_opy_) == 1:
                current_step_uuid = bstack11llll1l_opy_(threading.current_thread(), bstack1lllll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡶࡨࡴࡤࡻࡵࡪࡦࠪඈ"), None)
                self._1l111lll11_opy_[bstack1l111lll1l_opy_][bstack1lllll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪඉ")].bstack1l111111l1_opy_(current_step_uuid, duration=int(attrs.get(bstack1lllll1_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ඊ"), bstack1lllll1_opy_ (u"ࠩ࠳ࠫඋ"))), result=bstack1l11l11lll_opy_)
            else:
                self.bstack1l111111ll_opy_(attrs)
            self.bstack1l11ll11ll_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1lllll1_opy_ (u"ࠪ࡬ࡹࡳ࡬ࠨඌ"), bstack1lllll1_opy_ (u"ࠫࡳࡵࠧඍ")) == bstack1lllll1_opy_ (u"ࠬࡿࡥࡴࠩඎ"):
                return
            self.messages.push(message)
            bstack1l111l1111_opy_ = []
            if bstack1ll1l111l_opy_.bstack1l11l11ll1_opy_():
                bstack1l111l1111_opy_.append({
                    bstack1lllll1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩඏ"): bstack1ll1ll11l1_opy_(),
                    bstack1lllll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨඐ"): message.get(bstack1lllll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩඑ")),
                    bstack1lllll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨඒ"): message.get(bstack1lllll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩඓ")),
                    **bstack1ll1l111l_opy_.bstack1l11l11ll1_opy_()
                })
                if len(bstack1l111l1111_opy_) > 0:
                    bstack1ll1l111l_opy_.bstack1l11lllll1_opy_(bstack1l111l1111_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1ll1l111l_opy_.bstack1l111l11l1_opy_()
    def bstack1l111111ll_opy_(self, bstack1l11l1l1l1_opy_):
        if not bstack1ll1l111l_opy_.bstack1l11l11ll1_opy_():
            return
        kwname = bstack1lllll1_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪඔ").format(bstack1l11l1l1l1_opy_.get(bstack1lllll1_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬඕ")), bstack1l11l1l1l1_opy_.get(bstack1lllll1_opy_ (u"࠭ࡡࡳࡩࡶࠫඖ"), bstack1lllll1_opy_ (u"ࠧࠨ඗"))) if bstack1l11l1l1l1_opy_.get(bstack1lllll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭඘"), []) else bstack1l11l1l1l1_opy_.get(bstack1lllll1_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ඙"))
        error_message = bstack1lllll1_opy_ (u"ࠥ࡯ࡼࡴࡡ࡮ࡧ࠽ࠤࡡࠨࡻ࠱ࡿ࡟ࠦࠥࢂࠠࡴࡶࡤࡸࡺࡹ࠺ࠡ࡞ࠥࡿ࠶ࢃ࡜ࠣࠢࡿࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡ࡞ࠥࡿ࠷ࢃ࡜ࠣࠤක").format(kwname, bstack1l11l1l1l1_opy_.get(bstack1lllll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫඛ")), str(bstack1l11l1l1l1_opy_.get(bstack1lllll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ග"))))
        bstack1l11l111l1_opy_ = bstack1lllll1_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠧඝ").format(kwname, bstack1l11l1l1l1_opy_.get(bstack1lllll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧඞ")))
        bstack1l11111lll_opy_ = error_message if bstack1l11l1l1l1_opy_.get(bstack1lllll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩඟ")) else bstack1l11l111l1_opy_
        bstack1l11l1lll1_opy_ = {
            bstack1lllll1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬච"): self.bstack1l11ll11ll_opy_[-1].get(bstack1lllll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧඡ"), bstack1ll1ll11l1_opy_()),
            bstack1lllll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬජ"): bstack1l11111lll_opy_,
            bstack1lllll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫඣ"): bstack1lllll1_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬඤ") if bstack1l11l1l1l1_opy_.get(bstack1lllll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧඥ")) == bstack1lllll1_opy_ (u"ࠨࡈࡄࡍࡑ࠭ඦ") else bstack1lllll1_opy_ (u"ࠩࡌࡒࡋࡕࠧට"),
            **bstack1ll1l111l_opy_.bstack1l11l11ll1_opy_()
        }
        bstack1ll1l111l_opy_.bstack1l11lllll1_opy_([bstack1l11l1lll1_opy_])
    def _1l11l111ll_opy_(self):
        for bstack1l1111l1l1_opy_ in reversed(self._1l111lll11_opy_):
            bstack1l1111lll1_opy_ = bstack1l1111l1l1_opy_
            data = self._1l111lll11_opy_[bstack1l1111l1l1_opy_][bstack1lllll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ඨ")]
            if isinstance(data, bstack1l11ll1l1l_opy_):
                if not bstack1lllll1_opy_ (u"ࠫࡊࡇࡃࡉࠩඩ") in data.bstack1l11l1111l_opy_():
                    return bstack1l1111lll1_opy_
            else:
                return bstack1l1111lll1_opy_
    def _1l11l1llll_opy_(self, messages):
        try:
            bstack1l11l1l1ll_opy_ = BuiltIn().get_variable_value(bstack1lllll1_opy_ (u"ࠧࠪࡻࡍࡑࡊࠤࡑࡋࡖࡆࡎࢀࠦඪ")) in (bstack1l111llll1_opy_.DEBUG, bstack1l111llll1_opy_.TRACE)
            for message, bstack1l11lll1ll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1lllll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧණ"))
                level = message.get(bstack1lllll1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ඬ"))
                if level == bstack1l111llll1_opy_.FAIL:
                    self._1l111ll111_opy_ = name or self._1l111ll111_opy_
                    self._1l11l11l1l_opy_ = bstack1l11lll1ll_opy_.get(bstack1lllll1_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤත")) if bstack1l11l1l1ll_opy_ and bstack1l11lll1ll_opy_ else self._1l11l11l1l_opy_
        except:
            pass
    @classmethod
    def bstack1l111l1ll1_opy_(self, event: str, bstack1l11ll1ll1_opy_: bstack1l1l11111l_opy_, bstack1l11ll1111_opy_=False):
        if event == bstack1lllll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫථ"):
            bstack1l11ll1ll1_opy_.set(hooks=self.store[bstack1lllll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧද")])
        if event == bstack1lllll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬධ"):
            event = bstack1lllll1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧන")
        if bstack1l11ll1111_opy_:
            bstack1l11l1l111_opy_ = {
                bstack1lllll1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ඲"): event,
                bstack1l11ll1ll1_opy_.bstack1l111l1l1l_opy_(): bstack1l11ll1ll1_opy_.bstack1l1111ll11_opy_(event)
            }
            self.bstack1l111l1lll_opy_.append(bstack1l11l1l111_opy_)
        else:
            bstack1ll1l111l_opy_.bstack1l111l1ll1_opy_(event, bstack1l11ll1ll1_opy_)
class Messages:
    def __init__(self):
        self._1l11llll11_opy_ = []
    def bstack1l11llllll_opy_(self):
        self._1l11llll11_opy_.append([])
    def bstack1l11l1ll11_opy_(self):
        return self._1l11llll11_opy_.pop() if self._1l11llll11_opy_ else list()
    def push(self, message):
        self._1l11llll11_opy_[-1].append(message) if self._1l11llll11_opy_ else self._1l11llll11_opy_.append([message])
class bstack1l111llll1_opy_:
    FAIL = bstack1lllll1_opy_ (u"ࠧࡇࡃࡌࡐࠬඳ")
    ERROR = bstack1lllll1_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧප")
    WARNING = bstack1lllll1_opy_ (u"࡚ࠩࡅࡗࡔࠧඵ")
    bstack1l11ll1lll_opy_ = bstack1lllll1_opy_ (u"ࠪࡍࡓࡌࡏࠨබ")
    DEBUG = bstack1lllll1_opy_ (u"ࠫࡉࡋࡂࡖࡉࠪභ")
    TRACE = bstack1lllll1_opy_ (u"࡚ࠬࡒࡂࡅࡈࠫම")
    bstack1l11l11l11_opy_ = [FAIL, ERROR]
def bstack1l1111l111_opy_(bstack1l11lll111_opy_):
    if not bstack1l11lll111_opy_:
        return None
    if bstack1l11lll111_opy_.get(bstack1lllll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩඹ"), None):
        return getattr(bstack1l11lll111_opy_[bstack1lllll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪය")], bstack1lllll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ර"), None)
    return bstack1l11lll111_opy_.get(bstack1lllll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ඼"), None)
def bstack1l11l1ll1l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1lllll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩල"), bstack1lllll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭඾")]:
        return
    if hook_type.lower() == bstack1lllll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ඿"):
        if current_test_uuid is None:
            return bstack1lllll1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪව")
        else:
            return bstack1lllll1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬශ")
    elif hook_type.lower() == bstack1lllll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪෂ"):
        if current_test_uuid is None:
            return bstack1lllll1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬස")
        else:
            return bstack1lllll1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧහ")