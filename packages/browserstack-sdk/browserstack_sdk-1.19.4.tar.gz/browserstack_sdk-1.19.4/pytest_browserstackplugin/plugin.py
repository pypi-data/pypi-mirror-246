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
import atexit
import datetime
import inspect
import logging
import os
import sys
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l1ll111l_opy_, bstack1l1lll1l11_opy_, update, bstack11llll11_opy_,
                                       bstack111l11ll1_opy_, bstack1l1l1l11l1_opy_, bstack1l11l11l_opy_, bstack1l11ll1ll_opy_,
                                       bstack1l1l111ll_opy_, bstack1l1lll11l1_opy_, bstack1ll1lll1_opy_, bstack1ll1lll111_opy_,
                                       bstack1ll1lllll_opy_, getAccessibilityResults, getAccessibilityResultsSummary)
from browserstack_sdk._version import __version__
from bstack_utils.capture import bstack1l11111ll1_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack11l11l1ll_opy_, bstack1l1l1ll1_opy_, bstack11l11lll1_opy_, bstack1l11l11ll_opy_, \
    bstack1l1lllllll_opy_
from bstack_utils.helper import bstack11l1l11l1_opy_, bstack1l1ll1111_opy_, bstack11l1ll111l_opy_, bstack1llll1ll1_opy_, \
    bstack11l1lllll1_opy_, \
    bstack11l1ll1ll1_opy_, bstack1l11ll1l_opy_, bstack1ll1l1l11_opy_, bstack11ll11l1ll_opy_, bstack1llll1l11l_opy_, Notset, \
    bstack1l1l11l1l1_opy_, bstack11l1l11lll_opy_, bstack11l1l11111_opy_, Result, bstack11l1l111l1_opy_, bstack11l1l11l1l_opy_, bstack1l111l1lll_opy_, \
    bstack1llllllll1_opy_, bstack1l1llll11_opy_, bstack11l1l1ll_opy_
from bstack_utils.bstack11l111lll1_opy_ import bstack11l11l1l1l_opy_
from bstack_utils.messages import bstack11ll11111_opy_, bstack1111ll1ll_opy_, bstack1ll11111_opy_, bstack11111l11_opy_, bstack1l11ll11l_opy_, \
    bstack1l11l1lll_opy_, bstack111lllll1_opy_, bstack111111111_opy_, bstack1lllll1l11_opy_, bstack1111lll1l_opy_, \
    bstack1111l1l1_opy_, bstack1ll1lll1l1_opy_
from bstack_utils.proxy import bstack1lll11ll11_opy_, bstack11111ll1l_opy_
from bstack_utils.bstack11llll1ll_opy_ import bstack1111ll111l_opy_, bstack1111ll1l11_opy_, bstack1111ll11ll_opy_, bstack1111l1llll_opy_, \
    bstack1111ll11l1_opy_, bstack1111lll111_opy_, bstack1111ll1l1l_opy_, bstack11l1111l_opy_, bstack1111ll1lll_opy_
from bstack_utils.bstack1ll1l11l1_opy_ import bstack11lllllll_opy_
from bstack_utils.bstack1l1ll1l11l_opy_ import bstack111l1l11l_opy_, bstack1lllll111l_opy_, bstack11llllll_opy_, \
    bstack11lll1ll1_opy_, bstack111lll111_opy_
from bstack_utils.bstack1l11l11111_opy_ import bstack1l111l1l11_opy_
from bstack_utils.bstack11l111ll1_opy_ import bstack1l1ll111ll_opy_
import bstack_utils.bstack1l1lll1l_opy_ as bstack1l1ll11l1_opy_
bstack1lllll111_opy_ = None
bstack11111ll11_opy_ = None
bstack1l1l1ll1l1_opy_ = None
bstack1lllllll1l_opy_ = None
bstack1ll1l1111l_opy_ = None
bstack1lll11l1l1_opy_ = None
bstack1111l1111_opy_ = None
bstack111l111ll_opy_ = None
bstack1ll1111lll_opy_ = None
bstack1l1lll11ll_opy_ = None
bstack1ll11l1ll_opy_ = None
bstack1l1l1l1ll1_opy_ = None
bstack1ll111l11_opy_ = None
bstack1ll1lllll1_opy_ = bstack1lllll1l_opy_ (u"ࠫࠬᔮ")
CONFIG = {}
bstack11ll11ll1_opy_ = False
bstack11l111l1_opy_ = bstack1lllll1l_opy_ (u"ࠬ࠭ᔯ")
bstack1l1l1l1lll_opy_ = bstack1lllll1l_opy_ (u"࠭ࠧᔰ")
bstack1l11l1l1_opy_ = False
bstack1l1llll111_opy_ = []
bstack11ll11l1_opy_ = bstack1l1l1ll1_opy_
bstack1lllll11lll_opy_ = bstack1lllll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᔱ")
bstack1lllll1111l_opy_ = False
bstack1lllll1111_opy_ = {}
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack11ll11l1_opy_,
                    format=bstack1lllll1l_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ᔲ"),
                    datefmt=bstack1lllll1l_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫᔳ"),
                    stream=sys.stdout)
store = {
    bstack1lllll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᔴ"): []
}
def bstack1ll111111_opy_():
    global CONFIG
    global bstack11ll11l1_opy_
    if bstack1lllll1l_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᔵ") in CONFIG:
        bstack11ll11l1_opy_ = bstack11l11l1ll_opy_[CONFIG[bstack1lllll1l_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᔶ")]]
        logging.getLogger().setLevel(bstack11ll11l1_opy_)
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1l11111lll_opy_ = {}
current_test_uuid = None
def bstack1l1l1l1l11_opy_(page, bstack11llll111_opy_):
    try:
        page.evaluate(bstack1lllll1l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᔷ"),
                      bstack1lllll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫᔸ") + json.dumps(
                          bstack11llll111_opy_) + bstack1lllll1l_opy_ (u"ࠣࡿࢀࠦᔹ"))
    except Exception as e:
        print(bstack1lllll1l_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢᔺ"), e)
def bstack1l1l1l1l1l_opy_(page, message, level):
    try:
        page.evaluate(bstack1lllll1l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᔻ"), bstack1lllll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩᔼ") + json.dumps(
            message) + bstack1lllll1l_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨᔽ") + json.dumps(level) + bstack1lllll1l_opy_ (u"࠭ࡽࡾࠩᔾ"))
    except Exception as e:
        print(bstack1lllll1l_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥᔿ"), e)
def pytest_configure(config):
    bstack1ll1ll1l1_opy_ = Config.get_instance()
    config.args = bstack1l1ll111ll_opy_.bstack1llllllll11_opy_(config.args)
    bstack1ll1ll1l1_opy_.bstack1l1l1l1l1_opy_(bstack11l1l1ll_opy_(config.getoption(bstack1lllll1l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᕀ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1llll1l1ll1_opy_ = item.config.getoption(bstack1lllll1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᕁ"))
    plugins = item.config.getoption(bstack1lllll1l_opy_ (u"ࠥࡴࡱࡻࡧࡪࡰࡶࠦᕂ"))
    report = outcome.get_result()
    bstack1llll1ll1ll_opy_(item, call, report)
    if bstack1lllll1l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠤᕃ") not in plugins or bstack1llll1l11l_opy_():
        return
    summary = []
    driver = getattr(item, bstack1lllll1l_opy_ (u"ࠧࡥࡤࡳ࡫ࡹࡩࡷࠨᕄ"), None)
    page = getattr(item, bstack1lllll1l_opy_ (u"ࠨ࡟ࡱࡣࡪࡩࠧᕅ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1lllll111l1_opy_(item, report, summary, bstack1llll1l1ll1_opy_)
    if (page is not None):
        bstack1lllll111ll_opy_(item, report, summary, bstack1llll1l1ll1_opy_)
def bstack1lllll111l1_opy_(item, report, summary, bstack1llll1l1ll1_opy_):
    if report.when == bstack1lllll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᕆ") and report.skipped:
        bstack1111ll1lll_opy_(report)
    if report.when in [bstack1lllll1l_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᕇ"), bstack1lllll1l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᕈ")]:
        return
    if not bstack11l1ll111l_opy_():
        return
    try:
        if (str(bstack1llll1l1ll1_opy_).lower() != bstack1lllll1l_opy_ (u"ࠪࡸࡷࡻࡥࠨᕉ")):
            item._driver.execute_script(
                bstack1lllll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩᕊ") + json.dumps(
                    report.nodeid) + bstack1lllll1l_opy_ (u"ࠬࢃࡽࠨᕋ"))
        os.environ[bstack1lllll1l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩᕌ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1lllll1l_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦ࠼ࠣࡿ࠵ࢃࠢᕍ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1lllll1l_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥᕎ")))
    bstack1ll1l11ll1_opy_ = bstack1lllll1l_opy_ (u"ࠤࠥᕏ")
    bstack1111ll1lll_opy_(report)
    if not passed:
        try:
            bstack1ll1l11ll1_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1lllll1l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥᕐ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll1l11ll1_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1lllll1l_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᕑ")))
        bstack1ll1l11ll1_opy_ = bstack1lllll1l_opy_ (u"ࠧࠨᕒ")
        if not passed:
            try:
                bstack1ll1l11ll1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1lllll1l_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨᕓ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll1l11ll1_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1lllll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫᕔ")
                    + json.dumps(bstack1lllll1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠢࠤᕕ"))
                    + bstack1lllll1l_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧᕖ")
                )
            else:
                item._driver.execute_script(
                    bstack1lllll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡥࡣࡷࡥࠧࡀࠠࠨᕗ")
                    + json.dumps(str(bstack1ll1l11ll1_opy_))
                    + bstack1lllll1l_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢᕘ")
                )
        except Exception as e:
            summary.append(bstack1lllll1l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡥࡳࡴ࡯ࡵࡣࡷࡩ࠿ࠦࡻ࠱ࡿࠥᕙ").format(e))
def bstack1lllll1l11l_opy_(test_name, error_message):
    try:
        bstack1lllll1ll1l_opy_ = []
        bstack111l1l111_opy_ = os.environ.get(bstack1lllll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᕚ"), bstack1lllll1l_opy_ (u"ࠧ࠱ࠩᕛ"))
        bstack1ll1l111_opy_ = {bstack1lllll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᕜ"): test_name, bstack1lllll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᕝ"): error_message, bstack1lllll1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᕞ"): bstack111l1l111_opy_}
        bstack1lllll11l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1lllll1l_opy_ (u"ࠫࡵࡽ࡟ࡱࡻࡷࡩࡸࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩᕟ"))
        if os.path.exists(bstack1lllll11l11_opy_):
            with open(bstack1lllll11l11_opy_) as f:
                bstack1lllll1ll1l_opy_ = json.load(f)
        bstack1lllll1ll1l_opy_.append(bstack1ll1l111_opy_)
        with open(bstack1lllll11l11_opy_, bstack1lllll1l_opy_ (u"ࠬࡽࠧᕠ")) as f:
            json.dump(bstack1lllll1ll1l_opy_, f)
    except Exception as e:
        logger.debug(bstack1lllll1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡨࡶࡸ࡯ࡳࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡳࡽࡹ࡫ࡳࡵࠢࡨࡶࡷࡵࡲࡴ࠼ࠣࠫᕡ") + str(e))
def bstack1lllll111ll_opy_(item, report, summary, bstack1llll1l1ll1_opy_):
    if report.when in [bstack1lllll1l_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᕢ"), bstack1lllll1l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᕣ")]:
        return
    if (str(bstack1llll1l1ll1_opy_).lower() != bstack1lllll1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᕤ")):
        bstack1l1l1l1l11_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1lllll1l_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᕥ")))
    bstack1ll1l11ll1_opy_ = bstack1lllll1l_opy_ (u"ࠦࠧᕦ")
    bstack1111ll1lll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1ll1l11ll1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1lllll1l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᕧ").format(e)
                )
        try:
            if passed:
                bstack111lll111_opy_(getattr(item, bstack1lllll1l_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬᕨ"), None), bstack1lllll1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᕩ"))
            else:
                error_message = bstack1lllll1l_opy_ (u"ࠨࠩᕪ")
                if bstack1ll1l11ll1_opy_:
                    bstack1l1l1l1l1l_opy_(item._page, str(bstack1ll1l11ll1_opy_), bstack1lllll1l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣᕫ"))
                    bstack111lll111_opy_(getattr(item, bstack1lllll1l_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩᕬ"), None), bstack1lllll1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᕭ"), str(bstack1ll1l11ll1_opy_))
                    error_message = str(bstack1ll1l11ll1_opy_)
                else:
                    bstack111lll111_opy_(getattr(item, bstack1lllll1l_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᕮ"), None), bstack1lllll1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᕯ"))
                bstack1lllll1l11l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1lllll1l_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼ࠲ࢀࠦᕰ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1lllll1l_opy_ (u"ࠣ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧᕱ"), default=bstack1lllll1l_opy_ (u"ࠤࡉࡥࡱࡹࡥࠣᕲ"), help=bstack1lllll1l_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡨࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠤᕳ"))
    parser.addoption(bstack1lllll1l_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᕴ"), default=bstack1lllll1l_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦᕵ"), help=bstack1lllll1l_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧᕶ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1lllll1l_opy_ (u"ࠢ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠤᕷ"), action=bstack1lllll1l_opy_ (u"ࠣࡵࡷࡳࡷ࡫ࠢᕸ"), default=bstack1lllll1l_opy_ (u"ࠤࡦ࡬ࡷࡵ࡭ࡦࠤᕹ"),
                         help=bstack1lllll1l_opy_ (u"ࠥࡈࡷ࡯ࡶࡦࡴࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴࠤᕺ"))
def bstack1l111l11ll_opy_(log):
    if not (log[bstack1lllll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᕻ")] and log[bstack1lllll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᕼ")].strip()):
        return
    active = bstack1l111ll11l_opy_()
    log = {
        bstack1lllll1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᕽ"): log[bstack1lllll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᕾ")],
        bstack1lllll1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᕿ"): datetime.datetime.utcnow().isoformat() + bstack1lllll1l_opy_ (u"ࠩ࡝ࠫᖀ"),
        bstack1lllll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᖁ"): log[bstack1lllll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᖂ")],
    }
    if active:
        if active[bstack1lllll1l_opy_ (u"ࠬࡺࡹࡱࡧࠪᖃ")] == bstack1lllll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᖄ"):
            log[bstack1lllll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᖅ")] = active[bstack1lllll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᖆ")]
        elif active[bstack1lllll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᖇ")] == bstack1lllll1l_opy_ (u"ࠪࡸࡪࡹࡴࠨᖈ"):
            log[bstack1lllll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᖉ")] = active[bstack1lllll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᖊ")]
    bstack1l1ll111ll_opy_.bstack1l11l11ll1_opy_([log])
def bstack1l111ll11l_opy_():
    if len(store[bstack1lllll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᖋ")]) > 0 and store[bstack1lllll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᖌ")][-1]:
        return {
            bstack1lllll1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᖍ"): bstack1lllll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᖎ"),
            bstack1lllll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖏ"): store[bstack1lllll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᖐ")][-1]
        }
    if store.get(bstack1lllll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᖑ"), None):
        return {
            bstack1lllll1l_opy_ (u"࠭ࡴࡺࡲࡨࠫᖒ"): bstack1lllll1l_opy_ (u"ࠧࡵࡧࡶࡸࠬᖓ"),
            bstack1lllll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᖔ"): store[bstack1lllll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᖕ")]
        }
    return None
bstack1l11ll11l1_opy_ = bstack1l11111ll1_opy_(bstack1l111l11ll_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1lllll1111l_opy_
        if bstack1lllll1111l_opy_:
            driver = getattr(item, bstack1lllll1l_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᖖ"), None)
            bstack1l1ll1ll1_opy_ = bstack1l1ll11l1_opy_.bstack111111ll_opy_(CONFIG, bstack11l1ll1ll1_opy_(item.own_markers))
            item._a11y_started = bstack1l1ll11l1_opy_.bstack1lll1111l_opy_(driver, bstack1l1ll1ll1_opy_)
        if not bstack1l1ll111ll_opy_.on() or bstack1lllll11lll_opy_ != bstack1lllll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᖗ"):
            return
        global current_test_uuid, bstack1l11ll11l1_opy_
        bstack1l11ll11l1_opy_.start()
        bstack1l11l11l1l_opy_ = {
            bstack1lllll1l_opy_ (u"ࠬࡻࡵࡪࡦࠪᖘ"): uuid4().__str__(),
            bstack1lllll1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᖙ"): datetime.datetime.utcnow().isoformat() + bstack1lllll1l_opy_ (u"࡛ࠧࠩᖚ")
        }
        current_test_uuid = bstack1l11l11l1l_opy_[bstack1lllll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᖛ")]
        store[bstack1lllll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᖜ")] = bstack1l11l11l1l_opy_[bstack1lllll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᖝ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1l11111lll_opy_[item.nodeid] = {**_1l11111lll_opy_[item.nodeid], **bstack1l11l11l1l_opy_}
        bstack1llll1l11l1_opy_(item, _1l11111lll_opy_[item.nodeid], bstack1lllll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᖞ"))
    except Exception as err:
        print(bstack1lllll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡩࡡ࡭࡮࠽ࠤࢀࢃࠧᖟ"), str(err))
def pytest_runtest_setup(item):
    threading.current_thread().percySessionName = item.nodeid
    if bstack11ll11l1ll_opy_():
        atexit.register(bstack1llllll1ll_opy_)
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1111ll111l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1lllll1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᖠ")
    try:
        if not bstack1l1ll111ll_opy_.on():
            return
        bstack1l11ll11l1_opy_.start()
        uuid = uuid4().__str__()
        bstack1l11l11l1l_opy_ = {
            bstack1lllll1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᖡ"): uuid,
            bstack1lllll1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᖢ"): datetime.datetime.utcnow().isoformat() + bstack1lllll1l_opy_ (u"ࠩ࡝ࠫᖣ"),
            bstack1lllll1l_opy_ (u"ࠪࡸࡾࡶࡥࠨᖤ"): bstack1lllll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᖥ"),
            bstack1lllll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᖦ"): bstack1lllll1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᖧ"),
            bstack1lllll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᖨ"): bstack1lllll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᖩ")
        }
        threading.current_thread().current_hook_uuid = uuid
        store[bstack1lllll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ᖪ")] = item
        store[bstack1lllll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᖫ")] = [uuid]
        if not _1l11111lll_opy_.get(item.nodeid, None):
            _1l11111lll_opy_[item.nodeid] = {bstack1lllll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᖬ"): [], bstack1lllll1l_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᖭ"): []}
        _1l11111lll_opy_[item.nodeid][bstack1lllll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᖮ")].append(bstack1l11l11l1l_opy_[bstack1lllll1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᖯ")])
        _1l11111lll_opy_[item.nodeid + bstack1lllll1l_opy_ (u"ࠨ࠯ࡶࡩࡹࡻࡰࠨᖰ")] = bstack1l11l11l1l_opy_
        bstack1lllll1lll1_opy_(item, bstack1l11l11l1l_opy_, bstack1lllll1l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᖱ"))
    except Exception as err:
        print(bstack1lllll1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭ᖲ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1lllll1111_opy_
        if CONFIG.get(bstack1lllll1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᖳ"), False):
            if CONFIG.get(bstack1lllll1l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨᖴ"), bstack1lllll1l_opy_ (u"ࠨࡡࡶࡶࡲࠦᖵ")) == bstack1lllll1l_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤᖶ"):
                bstack1llll1llll1_opy_ = bstack11l1l11l1_opy_(threading.current_thread(), bstack1lllll1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᖷ"), None)
                bstack1llll111_opy_ = bstack1llll1llll1_opy_ + bstack1lllll1l_opy_ (u"ࠤ࠰ࡸࡪࡹࡴࡤࡣࡶࡩࠧᖸ")
                driver = getattr(item, bstack1lllll1l_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᖹ"), None)
                PercySDK.screenshot(driver, bstack1llll111_opy_)
        if getattr(item, bstack1lllll1l_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡧࡲࡵࡧࡧࠫᖺ"), False):
            logger.info(bstack1lllll1l_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠤࠧᖻ"))
            driver = getattr(item, bstack1lllll1l_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᖼ"), None)
            bstack11lll1l1ll_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1l1ll11l1_opy_.bstack1ll1111l1l_opy_(driver, bstack11lll1l1ll_opy_, item.name, item.module.__name__, item.path, bstack1lllll1111_opy_)
        if not bstack1l1ll111ll_opy_.on():
            return
        bstack1l11l11l1l_opy_ = {
            bstack1lllll1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᖽ"): uuid4().__str__(),
            bstack1lllll1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᖾ"): datetime.datetime.utcnow().isoformat() + bstack1lllll1l_opy_ (u"ࠩ࡝ࠫᖿ"),
            bstack1lllll1l_opy_ (u"ࠪࡸࡾࡶࡥࠨᗀ"): bstack1lllll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᗁ"),
            bstack1lllll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᗂ"): bstack1lllll1l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᗃ"),
            bstack1lllll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᗄ"): bstack1lllll1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᗅ")
        }
        _1l11111lll_opy_[item.nodeid + bstack1lllll1l_opy_ (u"ࠩ࠰ࡸࡪࡧࡲࡥࡱࡺࡲࠬᗆ")] = bstack1l11l11l1l_opy_
        bstack1lllll1lll1_opy_(item, bstack1l11l11l1l_opy_, bstack1lllll1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᗇ"))
    except Exception as err:
        print(bstack1lllll1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡀࠠࡼࡿࠪᗈ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1l1ll111ll_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1111l1llll_opy_(fixturedef.argname):
        store[bstack1lllll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫᗉ")] = request.node
    elif bstack1111ll11l1_opy_(fixturedef.argname):
        store[bstack1lllll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫᗊ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1lllll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᗋ"): fixturedef.argname,
            bstack1lllll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᗌ"): bstack11l1lllll1_opy_(outcome),
            bstack1lllll1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᗍ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        bstack1llll1l1l11_opy_ = store[bstack1lllll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᗎ")]
        if not _1l11111lll_opy_.get(bstack1llll1l1l11_opy_.nodeid, None):
            _1l11111lll_opy_[bstack1llll1l1l11_opy_.nodeid] = {bstack1lllll1l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᗏ"): []}
        _1l11111lll_opy_[bstack1llll1l1l11_opy_.nodeid][bstack1lllll1l_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᗐ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1lllll1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩᗑ"), str(err))
if bstack1llll1l11l_opy_() and bstack1l1ll111ll_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _1l11111lll_opy_[request.node.nodeid][bstack1lllll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᗒ")].bstack11111l1lll_opy_(id(step))
        except Exception as err:
            print(bstack1lllll1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭ᗓ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _1l11111lll_opy_[request.node.nodeid][bstack1lllll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᗔ")].bstack1l11ll1l11_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1lllll1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧᗕ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1l11l11111_opy_: bstack1l111l1l11_opy_ = _1l11111lll_opy_[request.node.nodeid][bstack1lllll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᗖ")]
            bstack1l11l11111_opy_.bstack1l11ll1l11_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1lllll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩᗗ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1lllll11lll_opy_
        try:
            if not bstack1l1ll111ll_opy_.on() or bstack1lllll11lll_opy_ != bstack1lllll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᗘ"):
                return
            global bstack1l11ll11l1_opy_
            bstack1l11ll11l1_opy_.start()
            if not _1l11111lll_opy_.get(request.node.nodeid, None):
                _1l11111lll_opy_[request.node.nodeid] = {}
            bstack1l11l11111_opy_ = bstack1l111l1l11_opy_.bstack111111l1l1_opy_(
                scenario, feature, request.node,
                name=bstack1111lll111_opy_(request.node, scenario),
                bstack1l11ll1lll_opy_=bstack1llll1ll1_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1lllll1l_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩᗙ"),
                tags=bstack1111ll1l1l_opy_(feature, scenario)
            )
            _1l11111lll_opy_[request.node.nodeid][bstack1lllll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᗚ")] = bstack1l11l11111_opy_
            bstack1llll1ll1l1_opy_(bstack1l11l11111_opy_.uuid)
            bstack1l1ll111ll_opy_.bstack1l11llllll_opy_(bstack1lllll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᗛ"), bstack1l11l11111_opy_)
        except Exception as err:
            print(bstack1lllll1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬᗜ"), str(err))
def bstack1llllll1111_opy_(bstack1lllll11l1l_opy_):
    if bstack1lllll11l1l_opy_ in store[bstack1lllll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᗝ")]:
        store[bstack1lllll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᗞ")].remove(bstack1lllll11l1l_opy_)
def bstack1llll1ll1l1_opy_(bstack1llll1ll11l_opy_):
    store[bstack1lllll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᗟ")] = bstack1llll1ll11l_opy_
    threading.current_thread().current_test_uuid = bstack1llll1ll11l_opy_
@bstack1l1ll111ll_opy_.bstack111111111l_opy_
def bstack1llll1ll1ll_opy_(item, call, report):
    global bstack1lllll11lll_opy_
    try:
        if report.when == bstack1lllll1l_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᗠ"):
            bstack1l11ll11l1_opy_.reset()
        if report.when == bstack1lllll1l_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᗡ"):
            if bstack1lllll11lll_opy_ == bstack1lllll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᗢ"):
                _1l11111lll_opy_[item.nodeid][bstack1lllll1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᗣ")] = bstack11l1l111l1_opy_(report.stop)
                bstack1llll1l11l1_opy_(item, _1l11111lll_opy_[item.nodeid], bstack1lllll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᗤ"), report, call)
                store[bstack1lllll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᗥ")] = None
            elif bstack1lllll11lll_opy_ == bstack1lllll1l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᗦ"):
                bstack1l11l11111_opy_ = _1l11111lll_opy_[item.nodeid][bstack1lllll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᗧ")]
                bstack1l11l11111_opy_.set(hooks=_1l11111lll_opy_[item.nodeid].get(bstack1lllll1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᗨ"), []))
                exception, bstack1l11ll1111_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l11ll1111_opy_ = [call.excinfo.exconly(), report.longreprtext]
                bstack1l11l11111_opy_.stop(time=bstack11l1l111l1_opy_(report.stop), result=Result(result=report.outcome, exception=exception, bstack1l11ll1111_opy_=bstack1l11ll1111_opy_))
                bstack1l1ll111ll_opy_.bstack1l11llllll_opy_(bstack1lllll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᗩ"), _1l11111lll_opy_[item.nodeid][bstack1lllll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᗪ")])
        elif report.when in [bstack1lllll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᗫ"), bstack1lllll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᗬ")]:
            bstack1l11l1llll_opy_ = item.nodeid + bstack1lllll1l_opy_ (u"࠭࠭ࠨᗭ") + report.when
            if report.skipped:
                hook_type = bstack1lllll1l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᗮ") if report.when == bstack1lllll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᗯ") else bstack1lllll1l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ᗰ")
                _1l11111lll_opy_[bstack1l11l1llll_opy_] = {
                    bstack1lllll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᗱ"): uuid4().__str__(),
                    bstack1lllll1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᗲ"): datetime.datetime.utcfromtimestamp(report.start).isoformat() + bstack1lllll1l_opy_ (u"ࠬࡠࠧᗳ"),
                    bstack1lllll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᗴ"): hook_type
                }
            _1l11111lll_opy_[bstack1l11l1llll_opy_][bstack1lllll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᗵ")] = datetime.datetime.utcfromtimestamp(report.stop).isoformat() + bstack1lllll1l_opy_ (u"ࠨ࡜ࠪᗶ")
            bstack1llllll1111_opy_(_1l11111lll_opy_[bstack1l11l1llll_opy_][bstack1lllll1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᗷ")])
            bstack1lllll1lll1_opy_(item, _1l11111lll_opy_[bstack1l11l1llll_opy_], bstack1lllll1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᗸ"), report, call)
            if report.when == bstack1lllll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᗹ"):
                if report.outcome == bstack1lllll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᗺ"):
                    bstack1l11l11l1l_opy_ = {
                        bstack1lllll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᗻ"): uuid4().__str__(),
                        bstack1lllll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᗼ"): bstack1llll1ll1_opy_(),
                        bstack1lllll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᗽ"): bstack1llll1ll1_opy_()
                    }
                    _1l11111lll_opy_[item.nodeid] = {**_1l11111lll_opy_[item.nodeid], **bstack1l11l11l1l_opy_}
                    bstack1llll1l11l1_opy_(item, _1l11111lll_opy_[item.nodeid], bstack1lllll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᗾ"))
                    bstack1llll1l11l1_opy_(item, _1l11111lll_opy_[item.nodeid], bstack1lllll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᗿ"), report, call)
    except Exception as err:
        print(bstack1lllll1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡻࡾࠩᘀ"), str(err))
def bstack1lllll1ll11_opy_(test, bstack1l11l11l1l_opy_, result=None, call=None, bstack1lll11ll_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l11l11111_opy_ = {
        bstack1lllll1l_opy_ (u"ࠬࡻࡵࡪࡦࠪᘁ"): bstack1l11l11l1l_opy_[bstack1lllll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᘂ")],
        bstack1lllll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬᘃ"): bstack1lllll1l_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᘄ"),
        bstack1lllll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᘅ"): test.name,
        bstack1lllll1l_opy_ (u"ࠪࡦࡴࡪࡹࠨᘆ"): {
            bstack1lllll1l_opy_ (u"ࠫࡱࡧ࡮ࡨࠩᘇ"): bstack1lllll1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᘈ"),
            bstack1lllll1l_opy_ (u"࠭ࡣࡰࡦࡨࠫᘉ"): inspect.getsource(test.obj)
        },
        bstack1lllll1l_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᘊ"): test.name,
        bstack1lllll1l_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧᘋ"): test.name,
        bstack1lllll1l_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩᘌ"): bstack1l1ll111ll_opy_.bstack1l11l11l11_opy_(test),
        bstack1lllll1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ᘍ"): file_path,
        bstack1lllll1l_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭ᘎ"): file_path,
        bstack1lllll1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᘏ"): bstack1lllll1l_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧᘐ"),
        bstack1lllll1l_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬᘑ"): file_path,
        bstack1lllll1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᘒ"): bstack1l11l11l1l_opy_[bstack1lllll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᘓ")],
        bstack1lllll1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᘔ"): bstack1lllll1l_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫᘕ"),
        bstack1lllll1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨᘖ"): {
            bstack1lllll1l_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪᘗ"): test.nodeid
        },
        bstack1lllll1l_opy_ (u"ࠧࡵࡣࡪࡷࠬᘘ"): bstack11l1ll1ll1_opy_(test.own_markers)
    }
    if bstack1lll11ll_opy_ in [bstack1lllll1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᘙ"), bstack1lllll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᘚ")]:
        bstack1l11l11111_opy_[bstack1lllll1l_opy_ (u"ࠪࡱࡪࡺࡡࠨᘛ")] = {
            bstack1lllll1l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᘜ"): bstack1l11l11l1l_opy_.get(bstack1lllll1l_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᘝ"), [])
        }
    if bstack1lll11ll_opy_ == bstack1lllll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᘞ"):
        bstack1l11l11111_opy_[bstack1lllll1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᘟ")] = bstack1lllll1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᘠ")
        bstack1l11l11111_opy_[bstack1lllll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᘡ")] = bstack1l11l11l1l_opy_[bstack1lllll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᘢ")]
        bstack1l11l11111_opy_[bstack1lllll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᘣ")] = bstack1l11l11l1l_opy_[bstack1lllll1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᘤ")]
    if result:
        bstack1l11l11111_opy_[bstack1lllll1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᘥ")] = result.outcome
        bstack1l11l11111_opy_[bstack1lllll1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᘦ")] = result.duration * 1000
        bstack1l11l11111_opy_[bstack1lllll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᘧ")] = bstack1l11l11l1l_opy_[bstack1lllll1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᘨ")]
        if result.failed:
            bstack1l11l11111_opy_[bstack1lllll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᘩ")] = bstack1l1ll111ll_opy_.bstack11llll1l1l_opy_(call.excinfo.typename)
            bstack1l11l11111_opy_[bstack1lllll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᘪ")] = bstack1l1ll111ll_opy_.bstack1llllll11ll_opy_(call.excinfo, result)
        bstack1l11l11111_opy_[bstack1lllll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᘫ")] = bstack1l11l11l1l_opy_[bstack1lllll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᘬ")]
    if outcome:
        bstack1l11l11111_opy_[bstack1lllll1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᘭ")] = bstack11l1lllll1_opy_(outcome)
        bstack1l11l11111_opy_[bstack1lllll1l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᘮ")] = 0
        bstack1l11l11111_opy_[bstack1lllll1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᘯ")] = bstack1l11l11l1l_opy_[bstack1lllll1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᘰ")]
        if bstack1l11l11111_opy_[bstack1lllll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᘱ")] == bstack1lllll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᘲ"):
            bstack1l11l11111_opy_[bstack1lllll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᘳ")] = bstack1lllll1l_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨᘴ")  # bstack1lllll1l1ll_opy_
            bstack1l11l11111_opy_[bstack1lllll1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᘵ")] = [{bstack1lllll1l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᘶ"): [bstack1lllll1l_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧᘷ")]}]
        bstack1l11l11111_opy_[bstack1lllll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᘸ")] = bstack1l11l11l1l_opy_[bstack1lllll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᘹ")]
    return bstack1l11l11111_opy_
def bstack1lllll1l111_opy_(test, bstack1l11l1ll11_opy_, bstack1lll11ll_opy_, result, call, outcome, bstack1llll1lllll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l11l1ll11_opy_[bstack1lllll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᘺ")]
    hook_name = bstack1l11l1ll11_opy_[bstack1lllll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᘻ")]
    hook_data = {
        bstack1lllll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᘼ"): bstack1l11l1ll11_opy_[bstack1lllll1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᘽ")],
        bstack1lllll1l_opy_ (u"ࠪࡸࡾࡶࡥࠨᘾ"): bstack1lllll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᘿ"),
        bstack1lllll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᙀ"): bstack1lllll1l_opy_ (u"࠭ࡻࡾࠩᙁ").format(bstack1111ll1l11_opy_(hook_name)),
        bstack1lllll1l_opy_ (u"ࠧࡣࡱࡧࡽࠬᙂ"): {
            bstack1lllll1l_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭ᙃ"): bstack1lllll1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᙄ"),
            bstack1lllll1l_opy_ (u"ࠪࡧࡴࡪࡥࠨᙅ"): None
        },
        bstack1lllll1l_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪᙆ"): test.name,
        bstack1lllll1l_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᙇ"): bstack1l1ll111ll_opy_.bstack1l11l11l11_opy_(test, hook_name),
        bstack1lllll1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᙈ"): file_path,
        bstack1lllll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩᙉ"): file_path,
        bstack1lllll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᙊ"): bstack1lllll1l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪᙋ"),
        bstack1lllll1l_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨᙌ"): file_path,
        bstack1lllll1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᙍ"): bstack1l11l1ll11_opy_[bstack1lllll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᙎ")],
        bstack1lllll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᙏ"): bstack1lllll1l_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩᙐ") if bstack1lllll11lll_opy_ == bstack1lllll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᙑ") else bstack1lllll1l_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᙒ"),
        bstack1lllll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᙓ"): hook_type
    }
    bstack1llll1ll111_opy_ = bstack1l11111l1l_opy_(_1l11111lll_opy_.get(test.nodeid, None))
    if bstack1llll1ll111_opy_:
        hook_data[bstack1lllll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩᙔ")] = bstack1llll1ll111_opy_
    if result:
        hook_data[bstack1lllll1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᙕ")] = result.outcome
        hook_data[bstack1lllll1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᙖ")] = result.duration * 1000
        hook_data[bstack1lllll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᙗ")] = bstack1l11l1ll11_opy_[bstack1lllll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᙘ")]
        if result.failed:
            hook_data[bstack1lllll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᙙ")] = bstack1l1ll111ll_opy_.bstack11llll1l1l_opy_(call.excinfo.typename)
            hook_data[bstack1lllll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᙚ")] = bstack1l1ll111ll_opy_.bstack1llllll11ll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1lllll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᙛ")] = bstack11l1lllll1_opy_(outcome)
        hook_data[bstack1lllll1l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᙜ")] = 100
        hook_data[bstack1lllll1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᙝ")] = bstack1l11l1ll11_opy_[bstack1lllll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᙞ")]
        if hook_data[bstack1lllll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᙟ")] == bstack1lllll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᙠ"):
            hook_data[bstack1lllll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᙡ")] = bstack1lllll1l_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬᙢ")  # bstack1lllll1l1ll_opy_
            hook_data[bstack1lllll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᙣ")] = [{bstack1lllll1l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᙤ"): [bstack1lllll1l_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫᙥ")]}]
    if bstack1llll1lllll_opy_:
        hook_data[bstack1lllll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᙦ")] = bstack1llll1lllll_opy_.result
        hook_data[bstack1lllll1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᙧ")] = bstack11l1l11lll_opy_(bstack1l11l1ll11_opy_[bstack1lllll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᙨ")], bstack1l11l1ll11_opy_[bstack1lllll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᙩ")])
        hook_data[bstack1lllll1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᙪ")] = bstack1l11l1ll11_opy_[bstack1lllll1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᙫ")]
        if hook_data[bstack1lllll1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᙬ")] == bstack1lllll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᙭"):
            hook_data[bstack1lllll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ᙮")] = bstack1l1ll111ll_opy_.bstack11llll1l1l_opy_(bstack1llll1lllll_opy_.exception_type)
            hook_data[bstack1lllll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᙯ")] = [{bstack1lllll1l_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᙰ"): bstack11l1l11111_opy_(bstack1llll1lllll_opy_.exception)}]
    return hook_data
def bstack1llll1l11l1_opy_(test, bstack1l11l11l1l_opy_, bstack1lll11ll_opy_, result=None, call=None, outcome=None):
    bstack1l11l11111_opy_ = bstack1lllll1ll11_opy_(test, bstack1l11l11l1l_opy_, result, call, bstack1lll11ll_opy_, outcome)
    driver = getattr(test, bstack1lllll1l_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᙱ"), None)
    if bstack1lll11ll_opy_ == bstack1lllll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᙲ") and driver:
        bstack1l11l11111_opy_[bstack1lllll1l_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭ᙳ")] = bstack1l1ll111ll_opy_.bstack1l1l1111l1_opy_(driver)
    if bstack1lll11ll_opy_ == bstack1lllll1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᙴ"):
        bstack1lll11ll_opy_ = bstack1lllll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᙵ")
    bstack1l111l1ll1_opy_ = {
        bstack1lllll1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᙶ"): bstack1lll11ll_opy_,
        bstack1lllll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ᙷ"): bstack1l11l11111_opy_
    }
    bstack1l1ll111ll_opy_.bstack1l11l111l1_opy_(bstack1l111l1ll1_opy_)
def bstack1lllll1lll1_opy_(test, bstack1l11l11l1l_opy_, bstack1lll11ll_opy_, result=None, call=None, outcome=None, bstack1llll1lllll_opy_=None):
    hook_data = bstack1lllll1l111_opy_(test, bstack1l11l11l1l_opy_, bstack1lll11ll_opy_, result, call, outcome, bstack1llll1lllll_opy_)
    bstack1l111l1ll1_opy_ = {
        bstack1lllll1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᙸ"): bstack1lll11ll_opy_,
        bstack1lllll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨᙹ"): hook_data
    }
    bstack1l1ll111ll_opy_.bstack1l11l111l1_opy_(bstack1l111l1ll1_opy_)
def bstack1l11111l1l_opy_(bstack1l11l11l1l_opy_):
    if not bstack1l11l11l1l_opy_:
        return None
    if bstack1l11l11l1l_opy_.get(bstack1lllll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᙺ"), None):
        return getattr(bstack1l11l11l1l_opy_[bstack1lllll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᙻ")], bstack1lllll1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᙼ"), None)
    return bstack1l11l11l1l_opy_.get(bstack1lllll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᙽ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1l1ll111ll_opy_.on():
            return
        places = [bstack1lllll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᙾ"), bstack1lllll1l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᙿ"), bstack1lllll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ ")]
        bstack1l11ll1l1l_opy_ = []
        for bstack1llll1l1lll_opy_ in places:
            records = caplog.get_records(bstack1llll1l1lll_opy_)
            bstack1llll1l11ll_opy_ = bstack1lllll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᚁ") if bstack1llll1l1lll_opy_ == bstack1lllll1l_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᚂ") else bstack1lllll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᚃ")
            bstack1lllll1llll_opy_ = request.node.nodeid + (bstack1lllll1l_opy_ (u"ࠪࠫᚄ") if bstack1llll1l1lll_opy_ == bstack1lllll1l_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᚅ") else bstack1lllll1l_opy_ (u"ࠬ࠳ࠧᚆ") + bstack1llll1l1lll_opy_)
            bstack1llll1ll11l_opy_ = bstack1l11111l1l_opy_(_1l11111lll_opy_.get(bstack1lllll1llll_opy_, None))
            if not bstack1llll1ll11l_opy_:
                continue
            for record in records:
                if bstack11l1l11l1l_opy_(record.message):
                    continue
                bstack1l11ll1l1l_opy_.append({
                    bstack1lllll1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᚇ"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack1lllll1l_opy_ (u"࡛ࠧࠩᚈ"),
                    bstack1lllll1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᚉ"): record.levelname,
                    bstack1lllll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᚊ"): record.message,
                    bstack1llll1l11ll_opy_: bstack1llll1ll11l_opy_
                })
        if len(bstack1l11ll1l1l_opy_) > 0:
            bstack1l1ll111ll_opy_.bstack1l11l11ll1_opy_(bstack1l11ll1l1l_opy_)
    except Exception as err:
        print(bstack1lllll1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡨࡵ࡮ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧ࠽ࠤࢀࢃࠧᚋ"), str(err))
def bstack1l1ll11ll1_opy_(sequence, driver_command, response=None):
    if sequence == bstack1lllll1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᚌ"):
        if driver_command == bstack1lllll1l_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩᚍ"):
            bstack1l1ll111ll_opy_.bstack1l11ll1l1_opy_({
                bstack1lllll1l_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬᚎ"): response[bstack1lllll1l_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭ᚏ")],
                bstack1lllll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᚐ"): store[bstack1lllll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᚑ")]
            })
def bstack1llllll1ll_opy_():
    global bstack1l1llll111_opy_
    bstack1l1ll111ll_opy_.bstack1l11l11lll_opy_()
    for driver in bstack1l1llll111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11lll1l1_opy_(self, *args, **kwargs):
    bstack111l1l1ll_opy_ = bstack1lllll111_opy_(self, *args, **kwargs)
    bstack1l1ll111ll_opy_.bstack1ll1llll1l_opy_(self)
    return bstack111l1l1ll_opy_
def bstack1llll11ll_opy_(framework_name):
    global bstack1ll1lllll1_opy_
    global bstack11l111ll_opy_
    bstack1ll1lllll1_opy_ = framework_name
    logger.info(bstack1ll1lll1l1_opy_.format(bstack1ll1lllll1_opy_.split(bstack1lllll1l_opy_ (u"ࠪ࠱ࠬᚒ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack11l1ll111l_opy_():
            Service.start = bstack1l11l11l_opy_
            Service.stop = bstack1l11ll1ll_opy_
            webdriver.Remote.__init__ = bstack11l1ll11_opy_
            webdriver.Remote.get = bstack1lll1l111l_opy_
            if not isinstance(os.getenv(bstack1lllll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬᚓ")), str):
                return
            WebDriver.close = bstack1l1l111ll_opy_
            WebDriver.quit = bstack11l11ll11_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.bstack11ll1l1l1_opy_ = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.bstack1ll1l11lll_opy_ = getAccessibilityResultsSummary
        if not bstack11l1ll111l_opy_() and bstack1l1ll111ll_opy_.on():
            webdriver.Remote.__init__ = bstack11lll1l1_opy_
        bstack11l111ll_opy_ = True
    except Exception as e:
        pass
    bstack1ll11lll1_opy_()
    if os.environ.get(bstack1lllll1l_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪᚔ")):
        bstack11l111ll_opy_ = eval(os.environ.get(bstack1lllll1l_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫᚕ")))
    if not bstack11l111ll_opy_:
        bstack1ll1lll1_opy_(bstack1lllll1l_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤᚖ"), bstack1111l1l1_opy_)
    if bstack1ll11l1l1l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1lll11l1l_opy_
        except Exception as e:
            logger.error(bstack1l11l1lll_opy_.format(str(e)))
    if bstack1lllll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᚗ") in str(framework_name).lower():
        if not bstack11l1ll111l_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack111l11ll1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1l1l11l1_opy_
            Config.getoption = bstack1ll1lll11l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1l1ll1l111_opy_
        except Exception as e:
            pass
def bstack11l11ll11_opy_(self):
    global bstack1ll1lllll1_opy_
    global bstack111llll1l_opy_
    global bstack11111ll11_opy_
    try:
        if bstack1lllll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᚘ") in bstack1ll1lllll1_opy_ and self.session_id != None and bstack11l1l11l1_opy_(threading.current_thread(), bstack1lllll1l_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧᚙ"), bstack1lllll1l_opy_ (u"ࠫࠬᚚ")) != bstack1lllll1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭᚛"):
            bstack1llll1l1ll_opy_ = bstack1lllll1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭᚜") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1lllll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᚝")
            bstack1l1llll11_opy_(logger, True)
            if self != None:
                bstack11lll1ll1_opy_(self, bstack1llll1l1ll_opy_, bstack1lllll1l_opy_ (u"ࠨ࠮ࠣࠫ᚞").join(threading.current_thread().bstackTestErrorMessages))
        threading.current_thread().testStatus = bstack1lllll1l_opy_ (u"ࠩࠪ᚟")
    except Exception as e:
        logger.debug(bstack1lllll1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠦᚠ") + str(e))
    bstack11111ll11_opy_(self)
    self.session_id = None
def bstack11l1ll11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack111llll1l_opy_
    global bstack1ll1l1l11l_opy_
    global bstack1l11l1l1_opy_
    global bstack1ll1lllll1_opy_
    global bstack1lllll111_opy_
    global bstack1l1llll111_opy_
    global bstack11l111l1_opy_
    global bstack1l1l1l1lll_opy_
    global bstack1lllll1111l_opy_
    global bstack1lllll1111_opy_
    CONFIG[bstack1lllll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᚡ")] = str(bstack1ll1lllll1_opy_) + str(__version__)
    command_executor = bstack1ll1l1l11_opy_(bstack11l111l1_opy_)
    logger.debug(bstack11111l11_opy_.format(command_executor))
    proxy = bstack1ll1lllll_opy_(CONFIG, proxy)
    bstack111l1l111_opy_ = 0
    try:
        if bstack1l11l1l1_opy_ is True:
            bstack111l1l111_opy_ = int(os.environ.get(bstack1lllll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᚢ")))
    except:
        bstack111l1l111_opy_ = 0
    bstack1l111llll_opy_ = bstack1l1ll111l_opy_(CONFIG, bstack111l1l111_opy_)
    logger.debug(bstack111111111_opy_.format(str(bstack1l111llll_opy_)))
    bstack1lllll1111_opy_ = CONFIG.get(bstack1lllll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᚣ"))[bstack111l1l111_opy_]
    if bstack1lllll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᚤ") in CONFIG and CONFIG[bstack1lllll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᚥ")]:
        bstack11llllll_opy_(bstack1l111llll_opy_, bstack1l1l1l1lll_opy_)
    if desired_capabilities:
        bstack11l11111_opy_ = bstack1l1lll1l11_opy_(desired_capabilities)
        bstack11l11111_opy_[bstack1lllll1l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩᚦ")] = bstack1l1l11l1l1_opy_(CONFIG)
        bstack1111l111l_opy_ = bstack1l1ll111l_opy_(bstack11l11111_opy_)
        if bstack1111l111l_opy_:
            bstack1l111llll_opy_ = update(bstack1111l111l_opy_, bstack1l111llll_opy_)
        desired_capabilities = None
    if options:
        bstack1l1lll11l1_opy_(options, bstack1l111llll_opy_)
    if not options:
        options = bstack11llll11_opy_(bstack1l111llll_opy_)
    if bstack1l1ll11l1_opy_.bstack1111lllll_opy_(CONFIG, bstack111l1l111_opy_) and bstack1l1ll11l1_opy_.bstack1l1lll1ll1_opy_(bstack1l111llll_opy_, options):
        bstack1lllll1111l_opy_ = True
        bstack1l1ll11l1_opy_.set_capabilities(bstack1l111llll_opy_, CONFIG)
    if proxy and bstack1l11ll1l_opy_() >= version.parse(bstack1lllll1l_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪᚧ")):
        options.proxy(proxy)
    if options and bstack1l11ll1l_opy_() >= version.parse(bstack1lllll1l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᚨ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l11ll1l_opy_() < version.parse(bstack1lllll1l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᚩ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l111llll_opy_)
    logger.info(bstack1ll11111_opy_)
    if bstack1l11ll1l_opy_() >= version.parse(bstack1lllll1l_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ᚪ")):
        bstack1lllll111_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l11ll1l_opy_() >= version.parse(bstack1lllll1l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᚫ")):
        bstack1lllll111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l11ll1l_opy_() >= version.parse(bstack1lllll1l_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨᚬ")):
        bstack1lllll111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1lllll111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack11l1l11l_opy_ = bstack1lllll1l_opy_ (u"ࠩࠪᚭ")
        if bstack1l11ll1l_opy_() >= version.parse(bstack1lllll1l_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫᚮ")):
            bstack11l1l11l_opy_ = self.caps.get(bstack1lllll1l_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦᚯ"))
        else:
            bstack11l1l11l_opy_ = self.capabilities.get(bstack1lllll1l_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧᚰ"))
        if bstack11l1l11l_opy_:
            bstack1llllllll1_opy_(bstack11l1l11l_opy_)
            if bstack1l11ll1l_opy_() <= version.parse(bstack1lllll1l_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭ᚱ")):
                self.command_executor._url = bstack1lllll1l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᚲ") + bstack11l111l1_opy_ + bstack1lllll1l_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧᚳ")
            else:
                self.command_executor._url = bstack1lllll1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦᚴ") + bstack11l1l11l_opy_ + bstack1lllll1l_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦᚵ")
            logger.debug(bstack1111ll1ll_opy_.format(bstack11l1l11l_opy_))
        else:
            logger.debug(bstack11ll11111_opy_.format(bstack1lllll1l_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧᚶ")))
    except Exception as e:
        logger.debug(bstack11ll11111_opy_.format(e))
    bstack111llll1l_opy_ = self.session_id
    if bstack1lllll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᚷ") in bstack1ll1lllll1_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        bstack1l1ll111ll_opy_.bstack1ll1llll1l_opy_(self)
    bstack1l1llll111_opy_.append(self)
    if bstack1lllll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᚸ") in CONFIG and bstack1lllll1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᚹ") in CONFIG[bstack1lllll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᚺ")][bstack111l1l111_opy_]:
        bstack1ll1l1l11l_opy_ = CONFIG[bstack1lllll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᚻ")][bstack111l1l111_opy_][bstack1lllll1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᚼ")]
    logger.debug(bstack1111lll1l_opy_.format(bstack111llll1l_opy_))
def bstack1lll1l111l_opy_(self, url):
    global bstack1ll1111lll_opy_
    global CONFIG
    try:
        bstack1lllll111l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1lllll1l11_opy_.format(str(err)))
    try:
        bstack1ll1111lll_opy_(self, url)
    except Exception as e:
        try:
            bstack1lll11l11_opy_ = str(e)
            if any(err_msg in bstack1lll11l11_opy_ for err_msg in bstack1l11l11ll_opy_):
                bstack1lllll111l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1lllll1l11_opy_.format(str(err)))
        raise e
def bstack1111l1ll_opy_(item, when):
    global bstack1l1l1l1ll1_opy_
    try:
        bstack1l1l1l1ll1_opy_(item, when)
    except Exception as e:
        pass
def bstack1l1ll1l111_opy_(item, call, rep):
    global bstack1ll111l11_opy_
    global bstack1l1llll111_opy_
    name = bstack1lllll1l_opy_ (u"ࠫࠬᚽ")
    try:
        if rep.when == bstack1lllll1l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᚾ"):
            bstack111llll1l_opy_ = threading.current_thread().bstackSessionId
            bstack1llll1l1ll1_opy_ = item.config.getoption(bstack1lllll1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᚿ"))
            try:
                if (str(bstack1llll1l1ll1_opy_).lower() != bstack1lllll1l_opy_ (u"ࠧࡵࡴࡸࡩࠬᛀ")):
                    name = str(rep.nodeid)
                    bstack1llllll1l_opy_ = bstack111l1l11l_opy_(bstack1lllll1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᛁ"), name, bstack1lllll1l_opy_ (u"ࠩࠪᛂ"), bstack1lllll1l_opy_ (u"ࠪࠫᛃ"), bstack1lllll1l_opy_ (u"ࠫࠬᛄ"), bstack1lllll1l_opy_ (u"ࠬ࠭ᛅ"))
                    os.environ[bstack1lllll1l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩᛆ")] = name
                    for driver in bstack1l1llll111_opy_:
                        if bstack111llll1l_opy_ == driver.session_id:
                            driver.execute_script(bstack1llllll1l_opy_)
            except Exception as e:
                logger.debug(bstack1lllll1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧᛇ").format(str(e)))
            try:
                bstack11l1111l_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1lllll1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᛈ"):
                    status = bstack1lllll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᛉ") if rep.outcome.lower() == bstack1lllll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᛊ") else bstack1lllll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᛋ")
                    reason = bstack1lllll1l_opy_ (u"ࠬ࠭ᛌ")
                    if status == bstack1lllll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᛍ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1lllll1l_opy_ (u"ࠧࡪࡰࡩࡳࠬᛎ") if status == bstack1lllll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᛏ") else bstack1lllll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᛐ")
                    data = name + bstack1lllll1l_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬᛑ") if status == bstack1lllll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᛒ") else name + bstack1lllll1l_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨᛓ") + reason
                    bstack1llll11l11_opy_ = bstack111l1l11l_opy_(bstack1lllll1l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨᛔ"), bstack1lllll1l_opy_ (u"ࠧࠨᛕ"), bstack1lllll1l_opy_ (u"ࠨࠩᛖ"), bstack1lllll1l_opy_ (u"ࠩࠪᛗ"), level, data)
                    for driver in bstack1l1llll111_opy_:
                        if bstack111llll1l_opy_ == driver.session_id:
                            driver.execute_script(bstack1llll11l11_opy_)
            except Exception as e:
                logger.debug(bstack1lllll1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧᛘ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1lllll1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨᛙ").format(str(e)))
    bstack1ll111l11_opy_(item, call, rep)
notset = Notset()
def bstack1ll1lll11l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1ll11l1ll_opy_
    if str(name).lower() == bstack1lllll1l_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬᛚ"):
        return bstack1lllll1l_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧᛛ")
    else:
        return bstack1ll11l1ll_opy_(self, name, default, skip)
def bstack1lll11l1l_opy_(self):
    global CONFIG
    global bstack1111l1111_opy_
    try:
        proxy = bstack1lll11ll11_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1lllll1l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬᛜ")):
                proxies = bstack11111ll1l_opy_(proxy, bstack1ll1l1l11_opy_())
                if len(proxies) > 0:
                    protocol, bstack1ll1ll11l_opy_ = proxies.popitem()
                    if bstack1lllll1l_opy_ (u"ࠣ࠼࠲࠳ࠧᛝ") in bstack1ll1ll11l_opy_:
                        return bstack1ll1ll11l_opy_
                    else:
                        return bstack1lllll1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᛞ") + bstack1ll1ll11l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1lllll1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢᛟ").format(str(e)))
    return bstack1111l1111_opy_(self)
def bstack1ll11l1l1l_opy_():
    return (bstack1lllll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᛠ") in CONFIG or bstack1lllll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᛡ") in CONFIG) and bstack1l1ll1111_opy_() and bstack1l11ll1l_opy_() >= version.parse(
        bstack11l11lll1_opy_)
def bstack11l11l11l_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1ll1l1l11l_opy_
    global bstack1l11l1l1_opy_
    global bstack1ll1lllll1_opy_
    CONFIG[bstack1lllll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨᛢ")] = str(bstack1ll1lllll1_opy_) + str(__version__)
    bstack111l1l111_opy_ = 0
    try:
        if bstack1l11l1l1_opy_ is True:
            bstack111l1l111_opy_ = int(os.environ.get(bstack1lllll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᛣ")))
    except:
        bstack111l1l111_opy_ = 0
    CONFIG[bstack1lllll1l_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᛤ")] = True
    bstack1l111llll_opy_ = bstack1l1ll111l_opy_(CONFIG, bstack111l1l111_opy_)
    logger.debug(bstack111111111_opy_.format(str(bstack1l111llll_opy_)))
    if CONFIG.get(bstack1lllll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᛥ")):
        bstack11llllll_opy_(bstack1l111llll_opy_, bstack1l1l1l1lll_opy_)
    if bstack1lllll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᛦ") in CONFIG and bstack1lllll1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᛧ") in CONFIG[bstack1lllll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᛨ")][bstack111l1l111_opy_]:
        bstack1ll1l1l11l_opy_ = CONFIG[bstack1lllll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᛩ")][bstack111l1l111_opy_][bstack1lllll1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᛪ")]
    import urllib
    import json
    bstack1ll11l11l1_opy_ = bstack1lllll1l_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪ᛫") + urllib.parse.quote(json.dumps(bstack1l111llll_opy_))
    browser = self.connect(bstack1ll11l11l1_opy_)
    return browser
def bstack1ll11lll1_opy_():
    global bstack11l111ll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack11l11l11l_opy_
        bstack11l111ll_opy_ = True
    except Exception as e:
        pass
def bstack1lllll11ll1_opy_():
    global CONFIG
    global bstack11ll11ll1_opy_
    global bstack11l111l1_opy_
    global bstack1l1l1l1lll_opy_
    global bstack1l11l1l1_opy_
    CONFIG = json.loads(os.environ.get(bstack1lllll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨ᛬")))
    bstack11ll11ll1_opy_ = eval(os.environ.get(bstack1lllll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ᛭")))
    bstack11l111l1_opy_ = os.environ.get(bstack1lllll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫᛮ"))
    bstack1ll1lll111_opy_(CONFIG, bstack11ll11ll1_opy_)
    bstack1ll111111_opy_()
    global bstack1lllll111_opy_
    global bstack11111ll11_opy_
    global bstack1l1l1ll1l1_opy_
    global bstack1lllllll1l_opy_
    global bstack1ll1l1111l_opy_
    global bstack1lll11l1l1_opy_
    global bstack111l111ll_opy_
    global bstack1ll1111lll_opy_
    global bstack1111l1111_opy_
    global bstack1ll11l1ll_opy_
    global bstack1l1l1l1ll1_opy_
    global bstack1ll111l11_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1lllll111_opy_ = webdriver.Remote.__init__
        bstack11111ll11_opy_ = WebDriver.quit
        bstack111l111ll_opy_ = WebDriver.close
        bstack1ll1111lll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1lllll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᛯ") in CONFIG or bstack1lllll1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᛰ") in CONFIG) and bstack1l1ll1111_opy_():
        if bstack1l11ll1l_opy_() < version.parse(bstack11l11lll1_opy_):
            logger.error(bstack111lllll1_opy_.format(bstack1l11ll1l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1111l1111_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack1l11l1lll_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1ll11l1ll_opy_ = Config.getoption
        from _pytest import runner
        bstack1l1l1l1ll1_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l11ll11l_opy_)
    try:
        from pytest_bdd import reporting
        bstack1ll111l11_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1lllll1l_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨᛱ"))
    bstack1l1l1l1lll_opy_ = CONFIG.get(bstack1lllll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬᛲ"), {}).get(bstack1lllll1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᛳ"))
    bstack1l11l1l1_opy_ = True
    bstack1llll11ll_opy_(bstack1l1lllllll_opy_)
if (bstack11ll11l1ll_opy_()):
    bstack1lllll11ll1_opy_()
@bstack1l111l1lll_opy_(class_method=False)
def bstack1llll1l1l1l_opy_(hook_name, event, bstack1lllll1l1l1_opy_=None):
    if hook_name not in [bstack1lllll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫᛴ"), bstack1lllll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᛵ"), bstack1lllll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᛶ"), bstack1lllll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨᛷ"), bstack1lllll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬᛸ"), bstack1lllll1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ᛹"), bstack1lllll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨ᛺"), bstack1lllll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬ᛻")]:
        return
    node = store[bstack1lllll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ᛼")]
    if hook_name in [bstack1lllll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ᛽"), bstack1lllll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ᛾")]:
        node = store[bstack1lllll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭᛿")]
    elif hook_name in [bstack1lllll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ᜀ"), bstack1lllll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᜁ")]:
        node = store[bstack1lllll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨᜂ")]
    if event == bstack1lllll1l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᜃ"):
        hook_type = bstack1111ll11ll_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack1l11l1ll11_opy_ = {
            bstack1lllll1l_opy_ (u"ࠬࡻࡵࡪࡦࠪᜄ"): uuid,
            bstack1lllll1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᜅ"): bstack1llll1ll1_opy_(),
            bstack1lllll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬᜆ"): bstack1lllll1l_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᜇ"),
            bstack1lllll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᜈ"): hook_type,
            bstack1lllll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᜉ"): hook_name
        }
        store[bstack1lllll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᜊ")].append(uuid)
        bstack1llll1lll1l_opy_ = node.nodeid
        if hook_type == bstack1lllll1l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᜋ"):
            if not _1l11111lll_opy_.get(bstack1llll1lll1l_opy_, None):
                _1l11111lll_opy_[bstack1llll1lll1l_opy_] = {bstack1lllll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᜌ"): []}
            _1l11111lll_opy_[bstack1llll1lll1l_opy_][bstack1lllll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᜍ")].append(bstack1l11l1ll11_opy_[bstack1lllll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᜎ")])
        _1l11111lll_opy_[bstack1llll1lll1l_opy_ + bstack1lllll1l_opy_ (u"ࠩ࠰ࠫᜏ") + hook_name] = bstack1l11l1ll11_opy_
        bstack1lllll1lll1_opy_(node, bstack1l11l1ll11_opy_, bstack1lllll1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᜐ"))
    elif event == bstack1lllll1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᜑ"):
        bstack1l11l1llll_opy_ = node.nodeid + bstack1lllll1l_opy_ (u"ࠬ࠳ࠧᜒ") + hook_name
        _1l11111lll_opy_[bstack1l11l1llll_opy_][bstack1lllll1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᜓ")] = bstack1llll1ll1_opy_()
        bstack1llllll1111_opy_(_1l11111lll_opy_[bstack1l11l1llll_opy_][bstack1lllll1l_opy_ (u"ࠧࡶࡷ࡬ࡨ᜔ࠬ")])
        bstack1lllll1lll1_opy_(node, _1l11111lll_opy_[bstack1l11l1llll_opy_], bstack1lllll1l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦ᜕ࠪ"), bstack1llll1lllll_opy_=bstack1lllll1l1l1_opy_)
def bstack1llll1lll11_opy_():
    global bstack1lllll11lll_opy_
    if bstack1llll1l11l_opy_():
        bstack1lllll11lll_opy_ = bstack1lllll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭᜖")
    else:
        bstack1lllll11lll_opy_ = bstack1lllll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ᜗")
@bstack1l1ll111ll_opy_.bstack111111111l_opy_
def bstack1lllll11111_opy_():
    bstack1llll1lll11_opy_()
    if bstack1l1ll1111_opy_():
        bstack11lllllll_opy_(bstack1l1ll11ll1_opy_)
    bstack11l111lll1_opy_ = bstack11l11l1l1l_opy_(bstack1llll1l1l1l_opy_)
bstack1lllll11111_opy_()