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
import os
import datetime
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1l11l11l11_opy_ import RobotHandler
from bstack_utils.capture import bstack1l111111ll_opy_
from bstack_utils.bstack1l11ll11l1_opy_ import bstack1l11ll11ll_opy_, bstack1l11l111l1_opy_, bstack1l11llll11_opy_
from bstack_utils.bstack1ll1ll1ll_opy_ import bstack11ll1l11_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l1ll11l1_opy_, bstack1l1ll1ll_opy_, Result, \
    bstack1l111l11l1_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬഓ"): [],
        bstack1ll1l11_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨഔ"): [],
        bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧക"): []
    }
    bstack1l11lll1l1_opy_ = []
    bstack1l11111l1l_opy_ = []
    @staticmethod
    def bstack1l11l1l111_opy_(log):
        if not (log[bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬഖ")] and log[bstack1ll1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ഗ")].strip()):
            return
        active = bstack11ll1l11_opy_.bstack1l111l1ll1_opy_()
        log = {
            bstack1ll1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬഘ"): log[bstack1ll1l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ങ")],
            bstack1ll1l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫച"): datetime.datetime.utcnow().isoformat() + bstack1ll1l11_opy_ (u"ࠩ࡝ࠫഛ"),
            bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫജ"): log[bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬഝ")],
        }
        if active:
            if active[bstack1ll1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪഞ")] == bstack1ll1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫട"):
                log[bstack1ll1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧഠ")] = active[bstack1ll1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨഡ")]
            elif active[bstack1ll1l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧഢ")] == bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࠨണ"):
                log[bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫത")] = active[bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬഥ")]
        bstack11ll1l11_opy_.bstack1l1111ll1l_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._1l11l1l11l_opy_ = None
        self._1l11llll1l_opy_ = None
        self._1l11ll1lll_opy_ = OrderedDict()
        self.bstack1l11l1llll_opy_ = bstack1l111111ll_opy_(self.bstack1l11l1l111_opy_)
    @bstack1l111l11l1_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1l1111lll1_opy_()
        if not self._1l11ll1lll_opy_.get(attrs.get(bstack1ll1l11_opy_ (u"࠭ࡩࡥࠩദ")), None):
            self._1l11ll1lll_opy_[attrs.get(bstack1ll1l11_opy_ (u"ࠧࡪࡦࠪധ"))] = {}
        bstack1l11l111ll_opy_ = bstack1l11llll11_opy_(
                bstack1l11lll1ll_opy_=attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡫ࡧࠫന")),
                name=name,
                bstack1l11ll111l_opy_=bstack1l1ll1ll_opy_(),
                file_path=os.path.relpath(attrs[bstack1ll1l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩഩ")], start=os.getcwd()) if attrs.get(bstack1ll1l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪപ")) != bstack1ll1l11_opy_ (u"ࠫࠬഫ") else bstack1ll1l11_opy_ (u"ࠬ࠭ബ"),
                framework=bstack1ll1l11_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬഭ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1ll1l11_opy_ (u"ࠧࡪࡦࠪമ"), None)
        self._1l11ll1lll_opy_[attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡫ࡧࠫയ"))][bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬര")] = bstack1l11l111ll_opy_
    @bstack1l111l11l1_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1l11ll1l1l_opy_()
        self._1l11111l11_opy_(messages)
        for bstack1l111lll11_opy_ in self.bstack1l11lll1l1_opy_:
            bstack1l111lll11_opy_[bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬറ")][bstack1ll1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪല")].extend(self.store[bstack1ll1l11_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫള")])
            bstack11ll1l11_opy_.bstack1l11111ll1_opy_(bstack1l111lll11_opy_)
        self.bstack1l11lll1l1_opy_ = []
        self.store[bstack1ll1l11_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬഴ")] = []
    @bstack1l111l11l1_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1l11l1llll_opy_.start()
        if not self._1l11ll1lll_opy_.get(attrs.get(bstack1ll1l11_opy_ (u"ࠧࡪࡦࠪവ")), None):
            self._1l11ll1lll_opy_[attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡫ࡧࠫശ"))] = {}
        driver = bstack1l1ll11l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨഷ"), None)
        bstack1l11ll11l1_opy_ = bstack1l11llll11_opy_(
            bstack1l11lll1ll_opy_=attrs.get(bstack1ll1l11_opy_ (u"ࠪ࡭ࡩ࠭സ")),
            name=name,
            bstack1l11ll111l_opy_=bstack1l1ll1ll_opy_(),
            file_path=os.path.relpath(attrs[bstack1ll1l11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫഹ")], start=os.getcwd()),
            scope=RobotHandler.bstack1l11111lll_opy_(attrs.get(bstack1ll1l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬഺ"), None)),
            framework=bstack1ll1l11_opy_ (u"࠭ࡒࡰࡤࡲࡸ഻ࠬ"),
            tags=attrs[bstack1ll1l11_opy_ (u"ࠧࡵࡣࡪࡷ഼ࠬ")],
            hooks=self.store[bstack1ll1l11_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧഽ")],
            bstack1l11l1lll1_opy_=bstack11ll1l11_opy_.bstack1l11llllll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1ll1l11_opy_ (u"ࠤࡾࢁࠥࡢ࡮ࠡࡽࢀࠦാ").format(bstack1ll1l11_opy_ (u"ࠥࠤࠧി").join(attrs[bstack1ll1l11_opy_ (u"ࠫࡹࡧࡧࡴࠩീ")]), name) if attrs[bstack1ll1l11_opy_ (u"ࠬࡺࡡࡨࡵࠪു")] else name
        )
        self._1l11ll1lll_opy_[attrs.get(bstack1ll1l11_opy_ (u"࠭ࡩࡥࠩൂ"))][bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪൃ")] = bstack1l11ll11l1_opy_
        threading.current_thread().current_test_uuid = bstack1l11ll11l1_opy_.bstack1l1l1111ll_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡫ࡧࠫൄ"), None)
        self.bstack1l11l1111l_opy_(bstack1ll1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ൅"), bstack1l11ll11l1_opy_)
    @bstack1l111l11l1_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1l11l1llll_opy_.reset()
        bstack1l111ll11l_opy_ = bstack1l11l1ll11_opy_.get(attrs.get(bstack1ll1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪെ")), bstack1ll1l11_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬേ"))
        self._1l11ll1lll_opy_[attrs.get(bstack1ll1l11_opy_ (u"ࠬ࡯ࡤࠨൈ"))][bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ൉")].stop(time=bstack1l1ll1ll_opy_(), duration=int(attrs.get(bstack1ll1l11_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬൊ"), bstack1ll1l11_opy_ (u"ࠨ࠲ࠪോ"))), result=Result(result=bstack1l111ll11l_opy_, exception=attrs.get(bstack1ll1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪൌ")), bstack1l1111l1ll_opy_=[attrs.get(bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨ്ࠫ"))]))
        self.bstack1l11l1111l_opy_(bstack1ll1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ൎ"), self._1l11ll1lll_opy_[attrs.get(bstack1ll1l11_opy_ (u"ࠬ࡯ࡤࠨ൏"))][bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ൐")], True)
        self.store[bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫ൑")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack1l111l11l1_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1l1111lll1_opy_()
        current_test_id = bstack1l1ll11l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪ൒"), None)
        bstack1l1111l111_opy_ = current_test_id if bstack1l1ll11l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫ൓"), None) else bstack1l1ll11l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ൔ"), None)
        if attrs.get(bstack1ll1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩൕ"), bstack1ll1l11_opy_ (u"ࠬ࠭ൖ")).lower() in [bstack1ll1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬൗ"), bstack1ll1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ൘")]:
            hook_type = bstack1l1111ll11_opy_(attrs.get(bstack1ll1l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭൙")), bstack1l1ll11l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭൚"), None))
            hook_name = bstack1ll1l11_opy_ (u"ࠪࡿࢂ࠭൛").format(attrs.get(bstack1ll1l11_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫ൜"), bstack1ll1l11_opy_ (u"ࠬ࠭൝")))
            if hook_type in [bstack1ll1l11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪ൞"), bstack1ll1l11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪൟ")]:
                hook_name = bstack1ll1l11_opy_ (u"ࠨ࡝ࡾࢁࡢࠦࡻࡾࠩൠ").format(bstack1l11l1ll1l_opy_.get(hook_type), attrs.get(bstack1ll1l11_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩൡ"), bstack1ll1l11_opy_ (u"ࠪࠫൢ")))
            bstack1l11ll1ll1_opy_ = bstack1l11l111l1_opy_(
                bstack1l11lll1ll_opy_=bstack1l1111l111_opy_ + bstack1ll1l11_opy_ (u"ࠫ࠲࠭ൣ") + attrs.get(bstack1ll1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪ൤"), bstack1ll1l11_opy_ (u"࠭ࠧ൥")).lower(),
                name=hook_name,
                bstack1l11ll111l_opy_=bstack1l1ll1ll_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1ll1l11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ൦")), start=os.getcwd()),
                framework=bstack1ll1l11_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧ൧"),
                tags=attrs[bstack1ll1l11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ൨")],
                scope=RobotHandler.bstack1l11111lll_opy_(attrs.get(bstack1ll1l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ൩"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1l11ll1ll1_opy_.bstack1l1l1111ll_opy_()
            threading.current_thread().current_hook_id = bstack1l1111l111_opy_ + bstack1ll1l11_opy_ (u"ࠫ࠲࠭൪") + attrs.get(bstack1ll1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪ൫"), bstack1ll1l11_opy_ (u"࠭ࠧ൬")).lower()
            self.store[bstack1ll1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ൭")] = [bstack1l11ll1ll1_opy_.bstack1l1l1111ll_opy_()]
            if bstack1l1ll11l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ൮"), None):
                self.store[bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭൯")].append(bstack1l11ll1ll1_opy_.bstack1l1l1111ll_opy_())
            else:
                self.store[bstack1ll1l11_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩ൰")].append(bstack1l11ll1ll1_opy_.bstack1l1l1111ll_opy_())
            if bstack1l1111l111_opy_:
                self._1l11ll1lll_opy_[bstack1l1111l111_opy_ + bstack1ll1l11_opy_ (u"ࠫ࠲࠭൱") + attrs.get(bstack1ll1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪ൲"), bstack1ll1l11_opy_ (u"࠭ࠧ൳")).lower()] = { bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ൴"): bstack1l11ll1ll1_opy_ }
            bstack11ll1l11_opy_.bstack1l11l1111l_opy_(bstack1ll1l11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ൵"), bstack1l11ll1ll1_opy_)
        else:
            bstack1l111l111l_opy_ = {
                bstack1ll1l11_opy_ (u"ࠩ࡬ࡨࠬ൶"): uuid4().__str__(),
                bstack1ll1l11_opy_ (u"ࠪࡸࡪࡾࡴࠨ൷"): bstack1ll1l11_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪ൸").format(attrs.get(bstack1ll1l11_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ൹")), attrs.get(bstack1ll1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫൺ"), bstack1ll1l11_opy_ (u"ࠧࠨൻ"))) if attrs.get(bstack1ll1l11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ർ"), []) else attrs.get(bstack1ll1l11_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩൽ")),
                bstack1ll1l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠪൾ"): attrs.get(bstack1ll1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩൿ"), []),
                bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ඀"): bstack1l1ll1ll_opy_(),
                bstack1ll1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ඁ"): bstack1ll1l11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨං"),
                bstack1ll1l11_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ඃ"): attrs.get(bstack1ll1l11_opy_ (u"ࠩࡧࡳࡨ࠭඄"), bstack1ll1l11_opy_ (u"ࠪࠫඅ"))
            }
            if attrs.get(bstack1ll1l11_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬආ"), bstack1ll1l11_opy_ (u"ࠬ࠭ඇ")) != bstack1ll1l11_opy_ (u"࠭ࠧඈ"):
                bstack1l111l111l_opy_[bstack1ll1l11_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨඉ")] = attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩඊ"))
            if not self.bstack1l11111l1l_opy_:
                self._1l11ll1lll_opy_[self._1l11lll11l_opy_()][bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬඋ")].add_step(bstack1l111l111l_opy_)
                threading.current_thread().current_step_uuid = bstack1l111l111l_opy_[bstack1ll1l11_opy_ (u"ࠪ࡭ࡩ࠭ඌ")]
            self.bstack1l11111l1l_opy_.append(bstack1l111l111l_opy_)
    @bstack1l111l11l1_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1l11ll1l1l_opy_()
        self._1l11111l11_opy_(messages)
        current_test_id = bstack1l1ll11l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ඍ"), None)
        bstack1l1111l111_opy_ = current_test_id if current_test_id else bstack1l1ll11l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨඎ"), None)
        bstack1l111ll1ll_opy_ = bstack1l11l1ll11_opy_.get(attrs.get(bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ඏ")), bstack1ll1l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨඐ"))
        bstack1l1111l1l1_opy_ = attrs.get(bstack1ll1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩඑ"))
        if bstack1l111ll1ll_opy_ != bstack1ll1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪඒ") and not attrs.get(bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫඓ")) and self._1l11l1l11l_opy_:
            bstack1l1111l1l1_opy_ = self._1l11l1l11l_opy_
        bstack1l1l111111_opy_ = Result(result=bstack1l111ll1ll_opy_, exception=bstack1l1111l1l1_opy_, bstack1l1111l1ll_opy_=[bstack1l1111l1l1_opy_])
        if attrs.get(bstack1ll1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩඔ"), bstack1ll1l11_opy_ (u"ࠬ࠭ඕ")).lower() in [bstack1ll1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬඖ"), bstack1ll1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ඗")]:
            bstack1l1111l111_opy_ = current_test_id if current_test_id else bstack1l1ll11l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫ඘"), None)
            if bstack1l1111l111_opy_:
                bstack1l1111llll_opy_ = bstack1l1111l111_opy_ + bstack1ll1l11_opy_ (u"ࠤ࠰ࠦ඙") + attrs.get(bstack1ll1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨක"), bstack1ll1l11_opy_ (u"ࠫࠬඛ")).lower()
                self._1l11ll1lll_opy_[bstack1l1111llll_opy_][bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨග")].stop(time=bstack1l1ll1ll_opy_(), duration=int(attrs.get(bstack1ll1l11_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫඝ"), bstack1ll1l11_opy_ (u"ࠧ࠱ࠩඞ"))), result=bstack1l1l111111_opy_)
                bstack11ll1l11_opy_.bstack1l11l1111l_opy_(bstack1ll1l11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪඟ"), self._1l11ll1lll_opy_[bstack1l1111llll_opy_][bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬච")])
        else:
            bstack1l1111l111_opy_ = current_test_id if current_test_id else bstack1l1ll11l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡ࡬ࡨࠬඡ"), None)
            if bstack1l1111l111_opy_ and len(self.bstack1l11111l1l_opy_) == 1:
                current_step_uuid = bstack1l1ll11l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨජ"), None)
                self._1l11ll1lll_opy_[bstack1l1111l111_opy_][bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨඣ")].bstack1l111lll1l_opy_(current_step_uuid, duration=int(attrs.get(bstack1ll1l11_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫඤ"), bstack1ll1l11_opy_ (u"ࠧ࠱ࠩඥ"))), result=bstack1l1l111111_opy_)
            else:
                self.bstack1l11ll1l11_opy_(attrs)
            self.bstack1l11111l1l_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1ll1l11_opy_ (u"ࠨࡪࡷࡱࡱ࠭ඦ"), bstack1ll1l11_opy_ (u"ࠩࡱࡳࠬට")) == bstack1ll1l11_opy_ (u"ࠪࡽࡪࡹࠧඨ"):
                return
            self.messages.push(message)
            bstack1l111lllll_opy_ = []
            if bstack11ll1l11_opy_.bstack1l111l1ll1_opy_():
                bstack1l111lllll_opy_.append({
                    bstack1ll1l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧඩ"): bstack1l1ll1ll_opy_(),
                    bstack1ll1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ඪ"): message.get(bstack1ll1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧණ")),
                    bstack1ll1l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ඬ"): message.get(bstack1ll1l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧත")),
                    **bstack11ll1l11_opy_.bstack1l111l1ll1_opy_()
                })
                if len(bstack1l111lllll_opy_) > 0:
                    bstack11ll1l11_opy_.bstack1l1111ll1l_opy_(bstack1l111lllll_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack11ll1l11_opy_.bstack1l111l1l1l_opy_()
    def bstack1l11ll1l11_opy_(self, bstack1l11lllll1_opy_):
        if not bstack11ll1l11_opy_.bstack1l111l1ll1_opy_():
            return
        kwname = bstack1ll1l11_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨථ").format(bstack1l11lllll1_opy_.get(bstack1ll1l11_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪද")), bstack1l11lllll1_opy_.get(bstack1ll1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩධ"), bstack1ll1l11_opy_ (u"ࠬ࠭න"))) if bstack1l11lllll1_opy_.get(bstack1ll1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫ඲"), []) else bstack1l11lllll1_opy_.get(bstack1ll1l11_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧඳ"))
        error_message = bstack1ll1l11_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠠࡽࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦ࡜ࠣࡽ࠵ࢁࡡࠨࠢප").format(kwname, bstack1l11lllll1_opy_.get(bstack1ll1l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩඵ")), str(bstack1l11lllll1_opy_.get(bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫබ"))))
        bstack1l111l11ll_opy_ = bstack1ll1l11_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠥභ").format(kwname, bstack1l11lllll1_opy_.get(bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬම")))
        bstack1l111llll1_opy_ = error_message if bstack1l11lllll1_opy_.get(bstack1ll1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧඹ")) else bstack1l111l11ll_opy_
        bstack1l1l1111l1_opy_ = {
            bstack1ll1l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪය"): self.bstack1l11111l1l_opy_[-1].get(bstack1ll1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬර"), bstack1l1ll1ll_opy_()),
            bstack1ll1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ඼"): bstack1l111llll1_opy_,
            bstack1ll1l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩල"): bstack1ll1l11_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪ඾") if bstack1l11lllll1_opy_.get(bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ඿")) == bstack1ll1l11_opy_ (u"࠭ࡆࡂࡋࡏࠫව") else bstack1ll1l11_opy_ (u"ࠧࡊࡐࡉࡓࠬශ"),
            **bstack11ll1l11_opy_.bstack1l111l1ll1_opy_()
        }
        bstack11ll1l11_opy_.bstack1l1111ll1l_opy_([bstack1l1l1111l1_opy_])
    def _1l11lll11l_opy_(self):
        for bstack1l11lll1ll_opy_ in reversed(self._1l11ll1lll_opy_):
            bstack1l111l1111_opy_ = bstack1l11lll1ll_opy_
            data = self._1l11ll1lll_opy_[bstack1l11lll1ll_opy_][bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫෂ")]
            if isinstance(data, bstack1l11l111l1_opy_):
                if not bstack1ll1l11_opy_ (u"ࠩࡈࡅࡈࡎࠧස") in data.bstack1l11l1l1l1_opy_():
                    return bstack1l111l1111_opy_
            else:
                return bstack1l111l1111_opy_
    def _1l11111l11_opy_(self, messages):
        try:
            bstack1l11l11ll1_opy_ = BuiltIn().get_variable_value(bstack1ll1l11_opy_ (u"ࠥࠨࢀࡒࡏࡈࠢࡏࡉ࡛ࡋࡌࡾࠤහ")) in (bstack1l11l11111_opy_.DEBUG, bstack1l11l11111_opy_.TRACE)
            for message, bstack1l11l1l1ll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬළ"))
                level = message.get(bstack1ll1l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫෆ"))
                if level == bstack1l11l11111_opy_.FAIL:
                    self._1l11l1l11l_opy_ = name or self._1l11l1l11l_opy_
                    self._1l11llll1l_opy_ = bstack1l11l1l1ll_opy_.get(bstack1ll1l11_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢ෇")) if bstack1l11l11ll1_opy_ and bstack1l11l1l1ll_opy_ else self._1l11llll1l_opy_
        except:
            pass
    @classmethod
    def bstack1l11l1111l_opy_(self, event: str, bstack1l11ll1111_opy_: bstack1l11ll11ll_opy_, bstack1l111l1lll_opy_=False):
        if event == bstack1ll1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ෈"):
            bstack1l11ll1111_opy_.set(hooks=self.store[bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ෉")])
        if event == bstack1ll1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦ්ࠪ"):
            event = bstack1ll1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ෋")
        if bstack1l111l1lll_opy_:
            bstack1l111ll1l1_opy_ = {
                bstack1ll1l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ෌"): event,
                bstack1l11ll1111_opy_.bstack1l11lll111_opy_(): bstack1l11ll1111_opy_.bstack1l1111l11l_opy_(event)
            }
            self.bstack1l11lll1l1_opy_.append(bstack1l111ll1l1_opy_)
        else:
            bstack11ll1l11_opy_.bstack1l11l1111l_opy_(event, bstack1l11ll1111_opy_)
class Messages:
    def __init__(self):
        self._1l11l11lll_opy_ = []
    def bstack1l1111lll1_opy_(self):
        self._1l11l11lll_opy_.append([])
    def bstack1l11ll1l1l_opy_(self):
        return self._1l11l11lll_opy_.pop() if self._1l11l11lll_opy_ else list()
    def push(self, message):
        self._1l11l11lll_opy_[-1].append(message) if self._1l11l11lll_opy_ else self._1l11l11lll_opy_.append([message])
class bstack1l11l11111_opy_:
    FAIL = bstack1ll1l11_opy_ (u"ࠬࡌࡁࡊࡎࠪ෍")
    ERROR = bstack1ll1l11_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬ෎")
    WARNING = bstack1ll1l11_opy_ (u"ࠧࡘࡃࡕࡒࠬා")
    bstack1l1l11111l_opy_ = bstack1ll1l11_opy_ (u"ࠨࡋࡑࡊࡔ࠭ැ")
    DEBUG = bstack1ll1l11_opy_ (u"ࠩࡇࡉࡇ࡛ࡇࠨෑ")
    TRACE = bstack1ll1l11_opy_ (u"ࠪࡘࡗࡇࡃࡆࠩි")
    bstack1l111l1l11_opy_ = [FAIL, ERROR]
def bstack1l111ll111_opy_(bstack1l11l11l1l_opy_):
    if not bstack1l11l11l1l_opy_:
        return None
    if bstack1l11l11l1l_opy_.get(bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧී"), None):
        return getattr(bstack1l11l11l1l_opy_[bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨු")], bstack1ll1l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ෕"), None)
    return bstack1l11l11l1l_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬූ"), None)
def bstack1l1111ll11_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ෗"), bstack1ll1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫෘ")]:
        return
    if hook_type.lower() == bstack1ll1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩෙ"):
        if current_test_uuid is None:
            return bstack1ll1l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨේ")
        else:
            return bstack1ll1l11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪෛ")
    elif hook_type.lower() == bstack1ll1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨො"):
        if current_test_uuid is None:
            return bstack1ll1l11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪෝ")
        else:
            return bstack1ll1l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬෞ")