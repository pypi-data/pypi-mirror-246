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
import os
import datetime
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1l11l1llll_opy_ import RobotHandler
from bstack_utils.capture import bstack1l111l1lll_opy_
from bstack_utils.bstack1l11111ll1_opy_ import bstack1l11l1l1l1_opy_, bstack1l11lll111_opy_, bstack1l111l11ll_opy_
from bstack_utils.bstack1ll11l1111_opy_ import bstack1l11l1111_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack111l1lll_opy_, bstack11ll1l11_opy_, Result, \
    bstack1l11l11lll_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack11l1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ೹"): [],
        bstack11l1ll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪ೺"): [],
        bstack11l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ೻"): []
    }
    bstack1l11l11ll1_opy_ = []
    bstack1l11l1l1ll_opy_ = []
    @staticmethod
    def bstack1l11lll1l1_opy_(log):
        if not (log[bstack11l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ೼")] and log[bstack11l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ೽")].strip()):
            return
        active = bstack1l11l1111_opy_.bstack1l111lll1l_opy_()
        log = {
            bstack11l1ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ೾"): log[bstack11l1ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ೿")],
            bstack11l1ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ഀ"): datetime.datetime.utcnow().isoformat() + bstack11l1ll_opy_ (u"ࠫ࡟࠭ഁ"),
            bstack11l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ം"): log[bstack11l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧഃ")],
        }
        if active:
            if active[bstack11l1ll_opy_ (u"ࠧࡵࡻࡳࡩࠬഄ")] == bstack11l1ll_opy_ (u"ࠨࡪࡲࡳࡰ࠭അ"):
                log[bstack11l1ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩആ")] = active[bstack11l1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪഇ")]
            elif active[bstack11l1ll_opy_ (u"ࠫࡹࡿࡰࡦࠩഈ")] == bstack11l1ll_opy_ (u"ࠬࡺࡥࡴࡶࠪഉ"):
                log[bstack11l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ഊ")] = active[bstack11l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧഋ")]
        bstack1l11l1111_opy_.bstack1l11ll11l1_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._1l111ll1l1_opy_ = None
        self._1l11111111_opy_ = None
        self._1l111l11l1_opy_ = OrderedDict()
        self.bstack1l11l111l1_opy_ = bstack1l111l1lll_opy_(self.bstack1l11lll1l1_opy_)
    @bstack1l11l11lll_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1l11l11l1l_opy_()
        if not self._1l111l11l1_opy_.get(attrs.get(bstack11l1ll_opy_ (u"ࠨ࡫ࡧࠫഌ")), None):
            self._1l111l11l1_opy_[attrs.get(bstack11l1ll_opy_ (u"ࠩ࡬ࡨࠬ഍"))] = {}
        bstack1l11l111ll_opy_ = bstack1l111l11ll_opy_(
                bstack1l1l111111_opy_=attrs.get(bstack11l1ll_opy_ (u"ࠪ࡭ࡩ࠭എ")),
                name=name,
                bstack1l111l1l1l_opy_=bstack11ll1l11_opy_(),
                file_path=os.path.relpath(attrs[bstack11l1ll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫഏ")], start=os.getcwd()) if attrs.get(bstack11l1ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬഐ")) != bstack11l1ll_opy_ (u"࠭ࠧ഑") else bstack11l1ll_opy_ (u"ࠧࠨഒ"),
                framework=bstack11l1ll_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧഓ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11l1ll_opy_ (u"ࠩ࡬ࡨࠬഔ"), None)
        self._1l111l11l1_opy_[attrs.get(bstack11l1ll_opy_ (u"ࠪ࡭ࡩ࠭ക"))][bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧഖ")] = bstack1l11l111ll_opy_
    @bstack1l11l11lll_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1l11ll1lll_opy_()
        self._1l11111l1l_opy_(messages)
        for bstack1l11ll111l_opy_ in self.bstack1l11l11ll1_opy_:
            bstack1l11ll111l_opy_[bstack11l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧഗ")][bstack11l1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬഘ")].extend(self.store[bstack11l1ll_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ങ")])
            bstack1l11l1111_opy_.bstack1l11l1l11l_opy_(bstack1l11ll111l_opy_)
        self.bstack1l11l11ll1_opy_ = []
        self.store[bstack11l1ll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧച")] = []
    @bstack1l11l11lll_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1l11l111l1_opy_.start()
        if not self._1l111l11l1_opy_.get(attrs.get(bstack11l1ll_opy_ (u"ࠩ࡬ࡨࠬഛ")), None):
            self._1l111l11l1_opy_[attrs.get(bstack11l1ll_opy_ (u"ࠪ࡭ࡩ࠭ജ"))] = {}
        driver = bstack111l1lll_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪഝ"), None)
        bstack1l11111ll1_opy_ = bstack1l111l11ll_opy_(
            bstack1l1l111111_opy_=attrs.get(bstack11l1ll_opy_ (u"ࠬ࡯ࡤࠨഞ")),
            name=name,
            bstack1l111l1l1l_opy_=bstack11ll1l11_opy_(),
            file_path=os.path.relpath(attrs[bstack11l1ll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ട")], start=os.getcwd()),
            scope=RobotHandler.bstack1l11111l11_opy_(attrs.get(bstack11l1ll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧഠ"), None)),
            framework=bstack11l1ll_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧഡ"),
            tags=attrs[bstack11l1ll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧഢ")],
            hooks=self.store[bstack11l1ll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩണ")],
            bstack1l111lll11_opy_=bstack1l11l1111_opy_.bstack1l1111l111_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11l1ll_opy_ (u"ࠦࢀࢃࠠ࡝ࡰࠣࡿࢂࠨത").format(bstack11l1ll_opy_ (u"ࠧࠦࠢഥ").join(attrs[bstack11l1ll_opy_ (u"࠭ࡴࡢࡩࡶࠫദ")]), name) if attrs[bstack11l1ll_opy_ (u"ࠧࡵࡣࡪࡷࠬധ")] else name
        )
        self._1l111l11l1_opy_[attrs.get(bstack11l1ll_opy_ (u"ࠨ࡫ࡧࠫന"))][bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬഩ")] = bstack1l11111ll1_opy_
        threading.current_thread().current_test_uuid = bstack1l11111ll1_opy_.bstack1l111l1111_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11l1ll_opy_ (u"ࠪ࡭ࡩ࠭പ"), None)
        self.bstack1l111l111l_opy_(bstack11l1ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬഫ"), bstack1l11111ll1_opy_)
    @bstack1l11l11lll_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1l11l111l1_opy_.reset()
        bstack1l1111ll1l_opy_ = bstack1l11l11l11_opy_.get(attrs.get(bstack11l1ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬബ")), bstack11l1ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧഭ"))
        self._1l111l11l1_opy_[attrs.get(bstack11l1ll_opy_ (u"ࠧࡪࡦࠪമ"))][bstack11l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫയ")].stop(time=bstack11ll1l11_opy_(), duration=int(attrs.get(bstack11l1ll_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧര"), bstack11l1ll_opy_ (u"ࠪ࠴ࠬറ"))), result=Result(result=bstack1l1111ll1l_opy_, exception=attrs.get(bstack11l1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬല")), bstack1l11l1ll1l_opy_=[attrs.get(bstack11l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ള"))]))
        self.bstack1l111l111l_opy_(bstack11l1ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨഴ"), self._1l111l11l1_opy_[attrs.get(bstack11l1ll_opy_ (u"ࠧࡪࡦࠪവ"))][bstack11l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫശ")], True)
        self.store[bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ഷ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack1l11l11lll_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1l11l11l1l_opy_()
        current_test_id = bstack111l1lll_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬസ"), None)
        bstack1l11lllll1_opy_ = current_test_id if bstack111l1lll_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ഹ"), None) else bstack111l1lll_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨഺ"), None)
        if attrs.get(bstack11l1ll_opy_ (u"࠭ࡴࡺࡲࡨ഻ࠫ"), bstack11l1ll_opy_ (u"ࠧࠨ഼")).lower() in [bstack11l1ll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧഽ"), bstack11l1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫാ")]:
            hook_type = bstack1l111ll1ll_opy_(attrs.get(bstack11l1ll_opy_ (u"ࠪࡸࡾࡶࡥࠨി")), bstack111l1lll_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨീ"), None))
            hook_name = bstack11l1ll_opy_ (u"ࠬࢁࡽࠨു").format(attrs.get(bstack11l1ll_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ൂ"), bstack11l1ll_opy_ (u"ࠧࠨൃ")))
            if hook_type in [bstack11l1ll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬൄ"), bstack11l1ll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ൅")]:
                hook_name = bstack11l1ll_opy_ (u"ࠪ࡟ࢀࢃ࡝ࠡࡽࢀࠫെ").format(bstack1l1111lll1_opy_.get(hook_type), attrs.get(bstack11l1ll_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫേ"), bstack11l1ll_opy_ (u"ࠬ࠭ൈ")))
            bstack1l111ll111_opy_ = bstack1l11lll111_opy_(
                bstack1l1l111111_opy_=bstack1l11lllll1_opy_ + bstack11l1ll_opy_ (u"࠭࠭ࠨ൉") + attrs.get(bstack11l1ll_opy_ (u"ࠧࡵࡻࡳࡩࠬൊ"), bstack11l1ll_opy_ (u"ࠨࠩോ")).lower(),
                name=hook_name,
                bstack1l111l1l1l_opy_=bstack11ll1l11_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11l1ll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩൌ")), start=os.getcwd()),
                framework=bstack11l1ll_opy_ (u"ࠪࡖࡴࡨ࡯ࡵ്ࠩ"),
                tags=attrs[bstack11l1ll_opy_ (u"ࠫࡹࡧࡧࡴࠩൎ")],
                scope=RobotHandler.bstack1l11111l11_opy_(attrs.get(bstack11l1ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ൏"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1l111ll111_opy_.bstack1l111l1111_opy_()
            threading.current_thread().current_hook_id = bstack1l11lllll1_opy_ + bstack11l1ll_opy_ (u"࠭࠭ࠨ൐") + attrs.get(bstack11l1ll_opy_ (u"ࠧࡵࡻࡳࡩࠬ൑"), bstack11l1ll_opy_ (u"ࠨࠩ൒")).lower()
            self.store[bstack11l1ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭൓")] = [bstack1l111ll111_opy_.bstack1l111l1111_opy_()]
            if bstack111l1lll_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧൔ"), None):
                self.store[bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨൕ")].append(bstack1l111ll111_opy_.bstack1l111l1111_opy_())
            else:
                self.store[bstack11l1ll_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫൖ")].append(bstack1l111ll111_opy_.bstack1l111l1111_opy_())
            if bstack1l11lllll1_opy_:
                self._1l111l11l1_opy_[bstack1l11lllll1_opy_ + bstack11l1ll_opy_ (u"࠭࠭ࠨൗ") + attrs.get(bstack11l1ll_opy_ (u"ࠧࡵࡻࡳࡩࠬ൘"), bstack11l1ll_opy_ (u"ࠨࠩ൙")).lower()] = { bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ൚"): bstack1l111ll111_opy_ }
            bstack1l11l1111_opy_.bstack1l111l111l_opy_(bstack11l1ll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ൛"), bstack1l111ll111_opy_)
        else:
            bstack1l11l1ll11_opy_ = {
                bstack11l1ll_opy_ (u"ࠫ࡮ࡪࠧ൜"): uuid4().__str__(),
                bstack11l1ll_opy_ (u"ࠬࡺࡥࡹࡶࠪ൝"): bstack11l1ll_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬ൞").format(attrs.get(bstack11l1ll_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧൟ")), attrs.get(bstack11l1ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ൠ"), bstack11l1ll_opy_ (u"ࠩࠪൡ"))) if attrs.get(bstack11l1ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨൢ"), []) else attrs.get(bstack11l1ll_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫൣ")),
                bstack11l1ll_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬ൤"): attrs.get(bstack11l1ll_opy_ (u"࠭ࡡࡳࡩࡶࠫ൥"), []),
                bstack11l1ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ൦"): bstack11ll1l11_opy_(),
                bstack11l1ll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ൧"): bstack11l1ll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ൨"),
                bstack11l1ll_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ൩"): attrs.get(bstack11l1ll_opy_ (u"ࠫࡩࡵࡣࠨ൪"), bstack11l1ll_opy_ (u"ࠬ࠭൫"))
            }
            if attrs.get(bstack11l1ll_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧ൬"), bstack11l1ll_opy_ (u"ࠧࠨ൭")) != bstack11l1ll_opy_ (u"ࠨࠩ൮"):
                bstack1l11l1ll11_opy_[bstack11l1ll_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪ൯")] = attrs.get(bstack11l1ll_opy_ (u"ࠪࡰ࡮ࡨ࡮ࡢ࡯ࡨࠫ൰"))
            if not self.bstack1l11l1l1ll_opy_:
                self._1l111l11l1_opy_[self._1l11llllll_opy_()][bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ൱")].add_step(bstack1l11l1ll11_opy_)
                threading.current_thread().current_step_uuid = bstack1l11l1ll11_opy_[bstack11l1ll_opy_ (u"ࠬ࡯ࡤࠨ൲")]
            self.bstack1l11l1l1ll_opy_.append(bstack1l11l1ll11_opy_)
    @bstack1l11l11lll_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1l11ll1lll_opy_()
        self._1l11111l1l_opy_(messages)
        current_test_id = bstack111l1lll_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨ൳"), None)
        bstack1l11lllll1_opy_ = current_test_id if current_test_id else bstack111l1lll_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪ൴"), None)
        bstack1l11l1111l_opy_ = bstack1l11l11l11_opy_.get(attrs.get(bstack11l1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ൵")), bstack11l1ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ൶"))
        bstack1l111ll11l_opy_ = attrs.get(bstack11l1ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ൷"))
        if bstack1l11l1111l_opy_ != bstack11l1ll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ൸") and not attrs.get(bstack11l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭൹")) and self._1l111ll1l1_opy_:
            bstack1l111ll11l_opy_ = self._1l111ll1l1_opy_
        bstack1l11ll1l11_opy_ = Result(result=bstack1l11l1111l_opy_, exception=bstack1l111ll11l_opy_, bstack1l11l1ll1l_opy_=[bstack1l111ll11l_opy_])
        if attrs.get(bstack11l1ll_opy_ (u"࠭ࡴࡺࡲࡨࠫൺ"), bstack11l1ll_opy_ (u"ࠧࠨൻ")).lower() in [bstack11l1ll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧർ"), bstack11l1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫൽ")]:
            bstack1l11lllll1_opy_ = current_test_id if current_test_id else bstack111l1lll_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ൾ"), None)
            if bstack1l11lllll1_opy_:
                bstack1l111l1ll1_opy_ = bstack1l11lllll1_opy_ + bstack11l1ll_opy_ (u"ࠦ࠲ࠨൿ") + attrs.get(bstack11l1ll_opy_ (u"ࠬࡺࡹࡱࡧࠪ඀"), bstack11l1ll_opy_ (u"࠭ࠧඁ")).lower()
                self._1l111l11l1_opy_[bstack1l111l1ll1_opy_][bstack11l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪං")].stop(time=bstack11ll1l11_opy_(), duration=int(attrs.get(bstack11l1ll_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ඃ"), bstack11l1ll_opy_ (u"ࠩ࠳ࠫ඄"))), result=bstack1l11ll1l11_opy_)
                bstack1l11l1111_opy_.bstack1l111l111l_opy_(bstack11l1ll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬඅ"), self._1l111l11l1_opy_[bstack1l111l1ll1_opy_][bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧආ")])
        else:
            bstack1l11lllll1_opy_ = current_test_id if current_test_id else bstack111l1lll_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣ࡮ࡪࠧඇ"), None)
            if bstack1l11lllll1_opy_ and len(self.bstack1l11l1l1ll_opy_) == 1:
                current_step_uuid = bstack111l1lll_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡶࡨࡴࡤࡻࡵࡪࡦࠪඈ"), None)
                self._1l111l11l1_opy_[bstack1l11lllll1_opy_][bstack11l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪඉ")].bstack1l111l1l11_opy_(current_step_uuid, duration=int(attrs.get(bstack11l1ll_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ඊ"), bstack11l1ll_opy_ (u"ࠩ࠳ࠫඋ"))), result=bstack1l11ll1l11_opy_)
            else:
                self.bstack1l11ll1ll1_opy_(attrs)
            self.bstack1l11l1l1ll_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11l1ll_opy_ (u"ࠪ࡬ࡹࡳ࡬ࠨඌ"), bstack11l1ll_opy_ (u"ࠫࡳࡵࠧඍ")) == bstack11l1ll_opy_ (u"ࠬࡿࡥࡴࠩඎ"):
                return
            self.messages.push(message)
            bstack1l11l1l111_opy_ = []
            if bstack1l11l1111_opy_.bstack1l111lll1l_opy_():
                bstack1l11l1l111_opy_.append({
                    bstack11l1ll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩඏ"): bstack11ll1l11_opy_(),
                    bstack11l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨඐ"): message.get(bstack11l1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩඑ")),
                    bstack11l1ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨඒ"): message.get(bstack11l1ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩඓ")),
                    **bstack1l11l1111_opy_.bstack1l111lll1l_opy_()
                })
                if len(bstack1l11l1l111_opy_) > 0:
                    bstack1l11l1111_opy_.bstack1l11ll11l1_opy_(bstack1l11l1l111_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1l11l1111_opy_.bstack1l111111l1_opy_()
    def bstack1l11ll1ll1_opy_(self, bstack1l11llll1l_opy_):
        if not bstack1l11l1111_opy_.bstack1l111lll1l_opy_():
            return
        kwname = bstack11l1ll_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪඔ").format(bstack1l11llll1l_opy_.get(bstack11l1ll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬඕ")), bstack1l11llll1l_opy_.get(bstack11l1ll_opy_ (u"࠭ࡡࡳࡩࡶࠫඖ"), bstack11l1ll_opy_ (u"ࠧࠨ඗"))) if bstack1l11llll1l_opy_.get(bstack11l1ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭඘"), []) else bstack1l11llll1l_opy_.get(bstack11l1ll_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ඙"))
        error_message = bstack11l1ll_opy_ (u"ࠥ࡯ࡼࡴࡡ࡮ࡧ࠽ࠤࡡࠨࡻ࠱ࡿ࡟ࠦࠥࢂࠠࡴࡶࡤࡸࡺࡹ࠺ࠡ࡞ࠥࡿ࠶ࢃ࡜ࠣࠢࡿࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡ࡞ࠥࡿ࠷ࢃ࡜ࠣࠤක").format(kwname, bstack1l11llll1l_opy_.get(bstack11l1ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫඛ")), str(bstack1l11llll1l_opy_.get(bstack11l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ග"))))
        bstack1l111lllll_opy_ = bstack11l1ll_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠧඝ").format(kwname, bstack1l11llll1l_opy_.get(bstack11l1ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧඞ")))
        bstack1l1111l11l_opy_ = error_message if bstack1l11llll1l_opy_.get(bstack11l1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩඟ")) else bstack1l111lllll_opy_
        bstack1l11l11111_opy_ = {
            bstack11l1ll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬච"): self.bstack1l11l1l1ll_opy_[-1].get(bstack11l1ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧඡ"), bstack11ll1l11_opy_()),
            bstack11l1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬජ"): bstack1l1111l11l_opy_,
            bstack11l1ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫඣ"): bstack11l1ll_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬඤ") if bstack1l11llll1l_opy_.get(bstack11l1ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧඥ")) == bstack11l1ll_opy_ (u"ࠨࡈࡄࡍࡑ࠭ඦ") else bstack11l1ll_opy_ (u"ࠩࡌࡒࡋࡕࠧට"),
            **bstack1l11l1111_opy_.bstack1l111lll1l_opy_()
        }
        bstack1l11l1111_opy_.bstack1l11ll11l1_opy_([bstack1l11l11111_opy_])
    def _1l11llllll_opy_(self):
        for bstack1l1l111111_opy_ in reversed(self._1l111l11l1_opy_):
            bstack1l111111ll_opy_ = bstack1l1l111111_opy_
            data = self._1l111l11l1_opy_[bstack1l1l111111_opy_][bstack11l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ඨ")]
            if isinstance(data, bstack1l11lll111_opy_):
                if not bstack11l1ll_opy_ (u"ࠫࡊࡇࡃࡉࠩඩ") in data.bstack1l11ll1l1l_opy_():
                    return bstack1l111111ll_opy_
            else:
                return bstack1l111111ll_opy_
    def _1l11111l1l_opy_(self, messages):
        try:
            bstack1l1111111l_opy_ = BuiltIn().get_variable_value(bstack11l1ll_opy_ (u"ࠧࠪࡻࡍࡑࡊࠤࡑࡋࡖࡆࡎࢀࠦඪ")) in (bstack1l11lll1ll_opy_.DEBUG, bstack1l11lll1ll_opy_.TRACE)
            for message, bstack1l11lll11l_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧණ"))
                level = message.get(bstack11l1ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ඬ"))
                if level == bstack1l11lll1ll_opy_.FAIL:
                    self._1l111ll1l1_opy_ = name or self._1l111ll1l1_opy_
                    self._1l11111111_opy_ = bstack1l11lll11l_opy_.get(bstack11l1ll_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤත")) if bstack1l1111111l_opy_ and bstack1l11lll11l_opy_ else self._1l11111111_opy_
        except:
            pass
    @classmethod
    def bstack1l111l111l_opy_(self, event: str, bstack1l1111l1l1_opy_: bstack1l11l1l1l1_opy_, bstack1l11llll11_opy_=False):
        if event == bstack11l1ll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫථ"):
            bstack1l1111l1l1_opy_.set(hooks=self.store[bstack11l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧද")])
        if event == bstack11l1ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬධ"):
            event = bstack11l1ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧන")
        if bstack1l11llll11_opy_:
            bstack1l11l1lll1_opy_ = {
                bstack11l1ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ඲"): event,
                bstack1l1111l1l1_opy_.bstack1l1111l1ll_opy_(): bstack1l1111l1l1_opy_.bstack1l1111llll_opy_(event)
            }
            self.bstack1l11l11ll1_opy_.append(bstack1l11l1lll1_opy_)
        else:
            bstack1l11l1111_opy_.bstack1l111l111l_opy_(event, bstack1l1111l1l1_opy_)
class Messages:
    def __init__(self):
        self._1l111llll1_opy_ = []
    def bstack1l11l11l1l_opy_(self):
        self._1l111llll1_opy_.append([])
    def bstack1l11ll1lll_opy_(self):
        return self._1l111llll1_opy_.pop() if self._1l111llll1_opy_ else list()
    def push(self, message):
        self._1l111llll1_opy_[-1].append(message) if self._1l111llll1_opy_ else self._1l111llll1_opy_.append([message])
class bstack1l11lll1ll_opy_:
    FAIL = bstack11l1ll_opy_ (u"ࠧࡇࡃࡌࡐࠬඳ")
    ERROR = bstack11l1ll_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧප")
    WARNING = bstack11l1ll_opy_ (u"࡚ࠩࡅࡗࡔࠧඵ")
    bstack1l11ll11ll_opy_ = bstack11l1ll_opy_ (u"ࠪࡍࡓࡌࡏࠨබ")
    DEBUG = bstack11l1ll_opy_ (u"ࠫࡉࡋࡂࡖࡉࠪභ")
    TRACE = bstack11l1ll_opy_ (u"࡚ࠬࡒࡂࡅࡈࠫම")
    bstack1l11ll1111_opy_ = [FAIL, ERROR]
def bstack1l1111ll11_opy_(bstack1l11111lll_opy_):
    if not bstack1l11111lll_opy_:
        return None
    if bstack1l11111lll_opy_.get(bstack11l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩඹ"), None):
        return getattr(bstack1l11111lll_opy_[bstack11l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪය")], bstack11l1ll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ර"), None)
    return bstack1l11111lll_opy_.get(bstack11l1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ඼"), None)
def bstack1l111ll1ll_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11l1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩල"), bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭඾")]:
        return
    if hook_type.lower() == bstack11l1ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ඿"):
        if current_test_uuid is None:
            return bstack11l1ll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪව")
        else:
            return bstack11l1ll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬශ")
    elif hook_type.lower() == bstack11l1ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪෂ"):
        if current_test_uuid is None:
            return bstack11l1ll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬස")
        else:
            return bstack11l1ll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧහ")