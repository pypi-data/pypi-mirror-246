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
import atexit
import datetime
import inspect
import logging
import os
import sys
import threading
from uuid import uuid4
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l1ll11l11_opy_, bstack1ll1llll11_opy_, update, bstack1l1ll11l1_opy_,
                                       bstack1l1l11l1ll_opy_, bstack111llll11_opy_, bstack111llll1_opy_, bstack1lll1lllll_opy_,
                                       bstack1ll111l1ll_opy_, bstack1ll11ll11l_opy_, bstack1l1lll1l11_opy_, bstack11l1lll11_opy_,
                                       bstack1llll11l1l_opy_, getAccessibilityResults, getAccessibilityResultsSummary)
from browserstack_sdk._version import __version__
from bstack_utils.capture import bstack1l111l1lll_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack11l1111l1_opy_, bstack11l1ll111_opy_, bstack1lllllllll_opy_, bstack1111lll1l_opy_, \
    bstack1l1llll1_opy_
from bstack_utils.helper import bstack111l1lll_opy_, bstack1ll1lllll_opy_, bstack11l1ll11l1_opy_, bstack11ll1l11_opy_, \
    bstack11l1ll1l1l_opy_, \
    bstack11l1l11l11_opy_, bstack11l1ll1l1_opy_, bstack1l1111111_opy_, bstack11l1lllll1_opy_, bstack11l11lll_opy_, Notset, \
    bstack1ll1111lll_opy_, bstack11l1l1l1l1_opy_, bstack11l11l1lll_opy_, Result, bstack11l1l1l11l_opy_, bstack11ll111l1l_opy_, bstack1l11l11lll_opy_, \
    bstack11l11ll1l_opy_, bstack11llll11l_opy_, bstack1l1lll11l_opy_
from bstack_utils.bstack11l111l11l_opy_ import bstack11l111l1l1_opy_
from bstack_utils.messages import bstack1ll1ll1ll1_opy_, bstack11ll111l_opy_, bstack1l1lll111l_opy_, bstack111l1111l_opy_, bstack1llll1l1_opy_, \
    bstack1l111111_opy_, bstack1lll1l1l1_opy_, bstack1l1l11lll1_opy_, bstack11l1l1l1_opy_, bstack1l1l1ll1ll_opy_, \
    bstack1l1l11ll1l_opy_, bstack1l1ll1111_opy_
from bstack_utils.proxy import bstack1111l1l11_opy_, bstack1l11ll1l_opy_
from bstack_utils.bstack1l1l11l11l_opy_ import bstack1111ll1l11_opy_, bstack1111l1llll_opy_, bstack1111ll111l_opy_, bstack1111l1lll1_opy_, \
    bstack1111ll11l1_opy_, bstack1111l1ll11_opy_, bstack1111ll1111_opy_, bstack1l1ll1l11_opy_, bstack1111ll1l1l_opy_
from bstack_utils.bstack11l1llll_opy_ import bstack1lll1lll_opy_
from bstack_utils.bstack11l111ll_opy_ import bstack11111111_opy_, bstack1ll11l1lll_opy_, bstack1lll1lll11_opy_, \
    bstack1l1ll1llll_opy_, bstack11l1l111l_opy_
from bstack_utils.bstack1l11111ll1_opy_ import bstack1l111l11ll_opy_
from bstack_utils.bstack1ll11l1111_opy_ import bstack1l11l1111_opy_
import bstack_utils.bstack11lll1l11_opy_ as bstack11ll11ll1_opy_
bstack111l1l1ll_opy_ = None
bstack1l11111ll_opy_ = None
bstack11lll1lll_opy_ = None
bstack1111lllll_opy_ = None
bstack1ll1llll_opy_ = None
bstack111l1llll_opy_ = None
bstack1l111l111_opy_ = None
bstack11111lll1_opy_ = None
bstack1l11l111_opy_ = None
bstack1l1ll1l1l_opy_ = None
bstack1ll1l1111_opy_ = None
bstack111l111l1_opy_ = None
bstack1l1l1l1lll_opy_ = None
bstack1ll11llll1_opy_ = bstack11l1ll_opy_ (u"࠭ࠧᔔ")
CONFIG = {}
bstack1l1llllll1_opy_ = False
bstack1llll1111_opy_ = bstack11l1ll_opy_ (u"ࠧࠨᔕ")
bstack1ll111ll1_opy_ = bstack11l1ll_opy_ (u"ࠨࠩᔖ")
bstack11lllllll_opy_ = False
bstack1llll11lll_opy_ = []
bstack111lll1ll_opy_ = bstack11l1ll111_opy_
bstack1llll1ll1ll_opy_ = bstack11l1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᔗ")
bstack1lllll1l1ll_opy_ = False
bstack1l1111l1_opy_ = {}
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack111lll1ll_opy_,
                    format=bstack11l1ll_opy_ (u"ࠪࡠࡳࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨᔘ"),
                    datefmt=bstack11l1ll_opy_ (u"ࠫࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ᔙ"),
                    stream=sys.stdout)
store = {
    bstack11l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᔚ"): []
}
def bstack1111l1111_opy_():
    global CONFIG
    global bstack111lll1ll_opy_
    if bstack11l1ll_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᔛ") in CONFIG:
        bstack111lll1ll_opy_ = bstack11l1111l1_opy_[CONFIG[bstack11l1ll_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᔜ")]]
        logging.getLogger().setLevel(bstack111lll1ll_opy_)
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1l111l11l1_opy_ = {}
current_test_uuid = None
def bstack1ll11ll11_opy_(page, bstack11ll1ll1l_opy_):
    try:
        page.evaluate(bstack11l1ll_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᔝ"),
                      bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ᔞ") + json.dumps(
                          bstack11ll1ll1l_opy_) + bstack11l1ll_opy_ (u"ࠥࢁࢂࠨᔟ"))
    except Exception as e:
        print(bstack11l1ll_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤᔠ"), e)
def bstack11lll1ll_opy_(page, message, level):
    try:
        page.evaluate(bstack11l1ll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᔡ"), bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫᔢ") + json.dumps(
            message) + bstack11l1ll_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪᔣ") + json.dumps(level) + bstack11l1ll_opy_ (u"ࠨࡿࢀࠫᔤ"))
    except Exception as e:
        print(bstack11l1ll_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧᔥ"), e)
def pytest_configure(config):
    bstack1ll1l11ll1_opy_ = Config.get_instance()
    config.args = bstack1l11l1111_opy_.bstack1llllll111l_opy_(config.args)
    bstack1ll1l11ll1_opy_.bstack1ll1l1ll1l_opy_(bstack1l1lll11l_opy_(config.getoption(bstack11l1ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᔦ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1lllll1l1l1_opy_ = item.config.getoption(bstack11l1ll_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᔧ"))
    plugins = item.config.getoption(bstack11l1ll_opy_ (u"ࠧࡶ࡬ࡶࡩ࡬ࡲࡸࠨᔨ"))
    report = outcome.get_result()
    bstack1lllll111ll_opy_(item, call, report)
    if bstack11l1ll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠦᔩ") not in plugins or bstack11l11lll_opy_():
        return
    summary = []
    driver = getattr(item, bstack11l1ll_opy_ (u"ࠢࡠࡦࡵ࡭ࡻ࡫ࡲࠣᔪ"), None)
    page = getattr(item, bstack11l1ll_opy_ (u"ࠣࡡࡳࡥ࡬࡫ࠢᔫ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1llll1ll111_opy_(item, report, summary, bstack1lllll1l1l1_opy_)
    if (page is not None):
        bstack1lllll11ll1_opy_(item, report, summary, bstack1lllll1l1l1_opy_)
def bstack1llll1ll111_opy_(item, report, summary, bstack1lllll1l1l1_opy_):
    if report.when == bstack11l1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᔬ") and report.skipped:
        bstack1111ll1l1l_opy_(report)
    if report.when in [bstack11l1ll_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᔭ"), bstack11l1ll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᔮ")]:
        return
    if not bstack11l1ll11l1_opy_():
        return
    try:
        if (str(bstack1lllll1l1l1_opy_).lower() != bstack11l1ll_opy_ (u"ࠬࡺࡲࡶࡧࠪᔯ")):
            item._driver.execute_script(
                bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫᔰ") + json.dumps(
                    report.nodeid) + bstack11l1ll_opy_ (u"ࠧࡾࡿࠪᔱ"))
        os.environ[bstack11l1ll_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫᔲ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11l1ll_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨ࠾ࠥࢁ࠰ࡾࠤᔳ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1ll_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᔴ")))
    bstack111ll111_opy_ = bstack11l1ll_opy_ (u"ࠦࠧᔵ")
    bstack1111ll1l1l_opy_(report)
    if not passed:
        try:
            bstack111ll111_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11l1ll_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᔶ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack111ll111_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11l1ll_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᔷ")))
        bstack111ll111_opy_ = bstack11l1ll_opy_ (u"ࠢࠣᔸ")
        if not passed:
            try:
                bstack111ll111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l1ll_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣᔹ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack111ll111_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭ᔺ")
                    + json.dumps(bstack11l1ll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠤࠦᔻ"))
                    + bstack11l1ll_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢᔼ")
                )
            else:
                item._driver.execute_script(
                    bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪᔽ")
                    + json.dumps(str(bstack111ll111_opy_))
                    + bstack11l1ll_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤᔾ")
                )
        except Exception as e:
            summary.append(bstack11l1ll_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡧ࡮࡯ࡱࡷࡥࡹ࡫࠺ࠡࡽ࠳ࢁࠧᔿ").format(e))
def bstack1llll1lll1l_opy_(test_name, error_message):
    try:
        bstack1lllll11111_opy_ = []
        bstack1l1ll1ll_opy_ = os.environ.get(bstack11l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᕀ"), bstack11l1ll_opy_ (u"ࠩ࠳ࠫᕁ"))
        bstack1l1l11l1_opy_ = {bstack11l1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨᕂ"): test_name, bstack11l1ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᕃ"): error_message, bstack11l1ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᕄ"): bstack1l1ll1ll_opy_}
        bstack1lllll11lll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫᕅ"))
        if os.path.exists(bstack1lllll11lll_opy_):
            with open(bstack1lllll11lll_opy_) as f:
                bstack1lllll11111_opy_ = json.load(f)
        bstack1lllll11111_opy_.append(bstack1l1l11l1_opy_)
        with open(bstack1lllll11lll_opy_, bstack11l1ll_opy_ (u"ࠧࡸࠩᕆ")) as f:
            json.dump(bstack1lllll11111_opy_, f)
    except Exception as e:
        logger.debug(bstack11l1ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡪࡸࡳࡪࡵࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡵࡿࡴࡦࡵࡷࠤࡪࡸࡲࡰࡴࡶ࠾ࠥ࠭ᕇ") + str(e))
def bstack1lllll11ll1_opy_(item, report, summary, bstack1lllll1l1l1_opy_):
    if report.when in [bstack11l1ll_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᕈ"), bstack11l1ll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᕉ")]:
        return
    if (str(bstack1lllll1l1l1_opy_).lower() != bstack11l1ll_opy_ (u"ࠫࡹࡸࡵࡦࠩᕊ")):
        bstack1ll11ll11_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1ll_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢᕋ")))
    bstack111ll111_opy_ = bstack11l1ll_opy_ (u"ࠨࠢᕌ")
    bstack1111ll1l1l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack111ll111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l1ll_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢᕍ").format(e)
                )
        try:
            if passed:
                bstack11l1l111l_opy_(getattr(item, bstack11l1ll_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧᕎ"), None), bstack11l1ll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᕏ"))
            else:
                error_message = bstack11l1ll_opy_ (u"ࠪࠫᕐ")
                if bstack111ll111_opy_:
                    bstack11lll1ll_opy_(item._page, str(bstack111ll111_opy_), bstack11l1ll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥᕑ"))
                    bstack11l1l111l_opy_(getattr(item, bstack11l1ll_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᕒ"), None), bstack11l1ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᕓ"), str(bstack111ll111_opy_))
                    error_message = str(bstack111ll111_opy_)
                else:
                    bstack11l1l111l_opy_(getattr(item, bstack11l1ll_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭ᕔ"), None), bstack11l1ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᕕ"))
                bstack1llll1lll1l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11l1ll_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾ࠴ࢂࠨᕖ").format(e))
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
    parser.addoption(bstack11l1ll_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢᕗ"), default=bstack11l1ll_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥᕘ"), help=bstack11l1ll_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦᕙ"))
    parser.addoption(bstack11l1ll_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᕚ"), default=bstack11l1ll_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨᕛ"), help=bstack11l1ll_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢᕜ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11l1ll_opy_ (u"ࠤ࠰࠱ࡩࡸࡩࡷࡧࡵࠦᕝ"), action=bstack11l1ll_opy_ (u"ࠥࡷࡹࡵࡲࡦࠤᕞ"), default=bstack11l1ll_opy_ (u"ࠦࡨ࡮ࡲࡰ࡯ࡨࠦᕟ"),
                         help=bstack11l1ll_opy_ (u"ࠧࡊࡲࡪࡸࡨࡶࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶࠦᕠ"))
def bstack1l11lll1l1_opy_(log):
    if not (log[bstack11l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᕡ")] and log[bstack11l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᕢ")].strip()):
        return
    active = bstack1l111lll1l_opy_()
    log = {
        bstack11l1ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᕣ"): log[bstack11l1ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᕤ")],
        bstack11l1ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᕥ"): datetime.datetime.utcnow().isoformat() + bstack11l1ll_opy_ (u"ࠫ࡟࠭ᕦ"),
        bstack11l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᕧ"): log[bstack11l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᕨ")],
    }
    if active:
        if active[bstack11l1ll_opy_ (u"ࠧࡵࡻࡳࡩࠬᕩ")] == bstack11l1ll_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᕪ"):
            log[bstack11l1ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᕫ")] = active[bstack11l1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᕬ")]
        elif active[bstack11l1ll_opy_ (u"ࠫࡹࡿࡰࡦࠩᕭ")] == bstack11l1ll_opy_ (u"ࠬࡺࡥࡴࡶࠪᕮ"):
            log[bstack11l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᕯ")] = active[bstack11l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᕰ")]
    bstack1l11l1111_opy_.bstack1l11ll11l1_opy_([log])
def bstack1l111lll1l_opy_():
    if len(store[bstack11l1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᕱ")]) > 0 and store[bstack11l1ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᕲ")][-1]:
        return {
            bstack11l1ll_opy_ (u"ࠪࡸࡾࡶࡥࠨᕳ"): bstack11l1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᕴ"),
            bstack11l1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᕵ"): store[bstack11l1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᕶ")][-1]
        }
    if store.get(bstack11l1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᕷ"), None):
        return {
            bstack11l1ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᕸ"): bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺࠧᕹ"),
            bstack11l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᕺ"): store[bstack11l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᕻ")]
        }
    return None
bstack1l11l111l1_opy_ = bstack1l111l1lll_opy_(bstack1l11lll1l1_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1lllll1l1ll_opy_
        if bstack1lllll1l1ll_opy_:
            driver = getattr(item, bstack11l1ll_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᕼ"), None)
            bstack1l1ll11ll_opy_ = bstack11ll11ll1_opy_.bstack1ll1ll1lll_opy_(CONFIG, bstack11l1l11l11_opy_(item.own_markers))
            item._a11y_started = bstack11ll11ll1_opy_.bstack11l1l11ll_opy_(driver, bstack1l1ll11ll_opy_)
        if not bstack1l11l1111_opy_.on() or bstack1llll1ll1ll_opy_ != bstack11l1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᕽ"):
            return
        global current_test_uuid, bstack1l11l111l1_opy_
        bstack1l11l111l1_opy_.start()
        bstack1l11111lll_opy_ = {
            bstack11l1ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᕾ"): uuid4().__str__(),
            bstack11l1ll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᕿ"): datetime.datetime.utcnow().isoformat() + bstack11l1ll_opy_ (u"ࠩ࡝ࠫᖀ")
        }
        current_test_uuid = bstack1l11111lll_opy_[bstack11l1ll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᖁ")]
        store[bstack11l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᖂ")] = bstack1l11111lll_opy_[bstack11l1ll_opy_ (u"ࠬࡻࡵࡪࡦࠪᖃ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1l111l11l1_opy_[item.nodeid] = {**_1l111l11l1_opy_[item.nodeid], **bstack1l11111lll_opy_}
        bstack1llll1l11l1_opy_(item, _1l111l11l1_opy_[item.nodeid], bstack11l1ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᖄ"))
    except Exception as err:
        print(bstack11l1ll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡤࡣ࡯ࡰ࠿ࠦࡻࡾࠩᖅ"), str(err))
def pytest_runtest_setup(item):
    if bstack11l1lllll1_opy_():
        atexit.register(bstack111l11ll_opy_)
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1111ll1l11_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11l1ll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᖆ")
    try:
        if not bstack1l11l1111_opy_.on():
            return
        bstack1l11l111l1_opy_.start()
        uuid = uuid4().__str__()
        bstack1l11111lll_opy_ = {
            bstack11l1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᖇ"): uuid,
            bstack11l1ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᖈ"): datetime.datetime.utcnow().isoformat() + bstack11l1ll_opy_ (u"ࠫ࡟࠭ᖉ"),
            bstack11l1ll_opy_ (u"ࠬࡺࡹࡱࡧࠪᖊ"): bstack11l1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᖋ"),
            bstack11l1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᖌ"): bstack11l1ll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᖍ"),
            bstack11l1ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬᖎ"): bstack11l1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᖏ")
        }
        threading.current_thread().current_hook_uuid = uuid
        store[bstack11l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᖐ")] = item
        store[bstack11l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᖑ")] = [uuid]
        if not _1l111l11l1_opy_.get(item.nodeid, None):
            _1l111l11l1_opy_[item.nodeid] = {bstack11l1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᖒ"): [], bstack11l1ll_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᖓ"): []}
        _1l111l11l1_opy_[item.nodeid][bstack11l1ll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᖔ")].append(bstack1l11111lll_opy_[bstack11l1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᖕ")])
        _1l111l11l1_opy_[item.nodeid + bstack11l1ll_opy_ (u"ࠪ࠱ࡸ࡫ࡴࡶࡲࠪᖖ")] = bstack1l11111lll_opy_
        bstack1llll1l111l_opy_(item, bstack1l11111lll_opy_, bstack11l1ll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᖗ"))
    except Exception as err:
        print(bstack11l1ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨᖘ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1l1111l1_opy_
        if getattr(item, bstack11l1ll_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡢࡴࡷࡩࡩ࠭ᖙ"), False):
            logger.info(bstack11l1ll_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠥࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡹࡳࡪࡥࡳࡹࡤࡽ࠳ࠦࠢᖚ"))
            driver = getattr(item, bstack11l1ll_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩᖛ"), None)
            bstack11ll1ll1l1_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11ll11ll1_opy_.bstack111111l11_opy_(driver, bstack11ll1ll1l1_opy_, item.name, item.module.__name__, item.path, bstack1l1111l1_opy_)
        if not bstack1l11l1111_opy_.on():
            return
        bstack1l11111lll_opy_ = {
            bstack11l1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᖜ"): uuid4().__str__(),
            bstack11l1ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᖝ"): datetime.datetime.utcnow().isoformat() + bstack11l1ll_opy_ (u"ࠫ࡟࠭ᖞ"),
            bstack11l1ll_opy_ (u"ࠬࡺࡹࡱࡧࠪᖟ"): bstack11l1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᖠ"),
            bstack11l1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᖡ"): bstack11l1ll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᖢ"),
            bstack11l1ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬᖣ"): bstack11l1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬᖤ")
        }
        _1l111l11l1_opy_[item.nodeid + bstack11l1ll_opy_ (u"ࠫ࠲ࡺࡥࡢࡴࡧࡳࡼࡴࠧᖥ")] = bstack1l11111lll_opy_
        bstack1llll1l111l_opy_(item, bstack1l11111lll_opy_, bstack11l1ll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᖦ"))
    except Exception as err:
        print(bstack11l1ll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮࠻ࠢࡾࢁࠬᖧ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1l11l1111_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1111l1lll1_opy_(fixturedef.argname):
        store[bstack11l1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭ᖨ")] = request.node
    elif bstack1111ll11l1_opy_(fixturedef.argname):
        store[bstack11l1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭ᖩ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack11l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᖪ"): fixturedef.argname,
            bstack11l1ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᖫ"): bstack11l1ll1l1l_opy_(outcome),
            bstack11l1ll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᖬ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        bstack1lllll11l1l_opy_ = store[bstack11l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩᖭ")]
        if not _1l111l11l1_opy_.get(bstack1lllll11l1l_opy_.nodeid, None):
            _1l111l11l1_opy_[bstack1lllll11l1l_opy_.nodeid] = {bstack11l1ll_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᖮ"): []}
        _1l111l11l1_opy_[bstack1lllll11l1l_opy_.nodeid][bstack11l1ll_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᖯ")].append(fixture)
    except Exception as err:
        logger.debug(bstack11l1ll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫᖰ"), str(err))
if bstack11l11lll_opy_() and bstack1l11l1111_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _1l111l11l1_opy_[request.node.nodeid][bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᖱ")].bstack111111ll11_opy_(id(step))
        except Exception as err:
            print(bstack11l1ll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳ࠾ࠥࢁࡽࠨᖲ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _1l111l11l1_opy_[request.node.nodeid][bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᖳ")].bstack1l111l1l11_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11l1ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩᖴ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1l11111ll1_opy_: bstack1l111l11ll_opy_ = _1l111l11l1_opy_[request.node.nodeid][bstack11l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᖵ")]
            bstack1l11111ll1_opy_.bstack1l111l1l11_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11l1ll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫᖶ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1llll1ll1ll_opy_
        try:
            if not bstack1l11l1111_opy_.on() or bstack1llll1ll1ll_opy_ != bstack11l1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᖷ"):
                return
            global bstack1l11l111l1_opy_
            bstack1l11l111l1_opy_.start()
            if not _1l111l11l1_opy_.get(request.node.nodeid, None):
                _1l111l11l1_opy_[request.node.nodeid] = {}
            bstack1l11111ll1_opy_ = bstack1l111l11ll_opy_.bstack1111111lll_opy_(
                scenario, feature, request.node,
                name=bstack1111l1ll11_opy_(request.node, scenario),
                bstack1l111l1l1l_opy_=bstack11ll1l11_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11l1ll_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫᖸ"),
                tags=bstack1111ll1111_opy_(feature, scenario)
            )
            _1l111l11l1_opy_[request.node.nodeid][bstack11l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᖹ")] = bstack1l11111ll1_opy_
            bstack1lllll1ll11_opy_(bstack1l11111ll1_opy_.uuid)
            bstack1l11l1111_opy_.bstack1l111l111l_opy_(bstack11l1ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᖺ"), bstack1l11111ll1_opy_)
        except Exception as err:
            print(bstack11l1ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧᖻ"), str(err))
def bstack1llll1l1ll1_opy_(bstack1lllll1111l_opy_):
    if bstack1lllll1111l_opy_ in store[bstack11l1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᖼ")]:
        store[bstack11l1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᖽ")].remove(bstack1lllll1111l_opy_)
def bstack1lllll1ll11_opy_(bstack1llll11llll_opy_):
    store[bstack11l1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᖾ")] = bstack1llll11llll_opy_
    threading.current_thread().current_test_uuid = bstack1llll11llll_opy_
@bstack1l11l1111_opy_.bstack1llllll1lll_opy_
def bstack1lllll111ll_opy_(item, call, report):
    global bstack1llll1ll1ll_opy_
    try:
        if report.when == bstack11l1ll_opy_ (u"ࠩࡦࡥࡱࡲࠧᖿ"):
            bstack1l11l111l1_opy_.reset()
        if report.when == bstack11l1ll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᗀ"):
            if bstack1llll1ll1ll_opy_ == bstack11l1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᗁ"):
                _1l111l11l1_opy_[item.nodeid][bstack11l1ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᗂ")] = bstack11l1l1l11l_opy_(report.stop)
                bstack1llll1l11l1_opy_(item, _1l111l11l1_opy_[item.nodeid], bstack11l1ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᗃ"), report, call)
                store[bstack11l1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᗄ")] = None
            elif bstack1llll1ll1ll_opy_ == bstack11l1ll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᗅ"):
                bstack1l11111ll1_opy_ = _1l111l11l1_opy_[item.nodeid][bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᗆ")]
                bstack1l11111ll1_opy_.set(hooks=_1l111l11l1_opy_[item.nodeid].get(bstack11l1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᗇ"), []))
                exception, bstack1l11l1ll1l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l11l1ll1l_opy_ = [call.excinfo.exconly(), report.longreprtext]
                bstack1l11111ll1_opy_.stop(time=bstack11l1l1l11l_opy_(report.stop), result=Result(result=report.outcome, exception=exception, bstack1l11l1ll1l_opy_=bstack1l11l1ll1l_opy_))
                bstack1l11l1111_opy_.bstack1l111l111l_opy_(bstack11l1ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᗈ"), _1l111l11l1_opy_[item.nodeid][bstack11l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᗉ")])
        elif report.when in [bstack11l1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᗊ"), bstack11l1ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᗋ")]:
            bstack1l111l1ll1_opy_ = item.nodeid + bstack11l1ll_opy_ (u"ࠨ࠯ࠪᗌ") + report.when
            if report.skipped:
                hook_type = bstack11l1ll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᗍ") if report.when == bstack11l1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᗎ") else bstack11l1ll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᗏ")
                _1l111l11l1_opy_[bstack1l111l1ll1_opy_] = {
                    bstack11l1ll_opy_ (u"ࠬࡻࡵࡪࡦࠪᗐ"): uuid4().__str__(),
                    bstack11l1ll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᗑ"): datetime.datetime.utcfromtimestamp(report.start).isoformat() + bstack11l1ll_opy_ (u"࡛ࠧࠩᗒ"),
                    bstack11l1ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᗓ"): hook_type
                }
            _1l111l11l1_opy_[bstack1l111l1ll1_opy_][bstack11l1ll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᗔ")] = datetime.datetime.utcfromtimestamp(report.stop).isoformat() + bstack11l1ll_opy_ (u"ࠪ࡞ࠬᗕ")
            bstack1llll1l1ll1_opy_(_1l111l11l1_opy_[bstack1l111l1ll1_opy_][bstack11l1ll_opy_ (u"ࠫࡺࡻࡩࡥࠩᗖ")])
            bstack1llll1l111l_opy_(item, _1l111l11l1_opy_[bstack1l111l1ll1_opy_], bstack11l1ll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᗗ"), report, call)
            if report.when == bstack11l1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᗘ"):
                if report.outcome == bstack11l1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᗙ"):
                    bstack1l11111lll_opy_ = {
                        bstack11l1ll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᗚ"): uuid4().__str__(),
                        bstack11l1ll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᗛ"): bstack11ll1l11_opy_(),
                        bstack11l1ll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᗜ"): bstack11ll1l11_opy_()
                    }
                    _1l111l11l1_opy_[item.nodeid] = {**_1l111l11l1_opy_[item.nodeid], **bstack1l11111lll_opy_}
                    bstack1llll1l11l1_opy_(item, _1l111l11l1_opy_[item.nodeid], bstack11l1ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᗝ"))
                    bstack1llll1l11l1_opy_(item, _1l111l11l1_opy_[item.nodeid], bstack11l1ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᗞ"), report, call)
    except Exception as err:
        print(bstack11l1ll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡽࢀࠫᗟ"), str(err))
def bstack1lllll1l11l_opy_(test, bstack1l11111lll_opy_, result=None, call=None, bstack111l1l1l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l11111ll1_opy_ = {
        bstack11l1ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᗠ"): bstack1l11111lll_opy_[bstack11l1ll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᗡ")],
        bstack11l1ll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᗢ"): bstack11l1ll_opy_ (u"ࠪࡸࡪࡹࡴࠨᗣ"),
        bstack11l1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᗤ"): test.name,
        bstack11l1ll_opy_ (u"ࠬࡨ࡯ࡥࡻࠪᗥ"): {
            bstack11l1ll_opy_ (u"࠭࡬ࡢࡰࡪࠫᗦ"): bstack11l1ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᗧ"),
            bstack11l1ll_opy_ (u"ࠨࡥࡲࡨࡪ࠭ᗨ"): inspect.getsource(test.obj)
        },
        bstack11l1ll_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᗩ"): test.name,
        bstack11l1ll_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩᗪ"): test.name,
        bstack11l1ll_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᗫ"): bstack1l11l1111_opy_.bstack1l11111l11_opy_(test),
        bstack11l1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᗬ"): file_path,
        bstack11l1ll_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᗭ"): file_path,
        bstack11l1ll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᗮ"): bstack11l1ll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩᗯ"),
        bstack11l1ll_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧᗰ"): file_path,
        bstack11l1ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᗱ"): bstack1l11111lll_opy_[bstack11l1ll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᗲ")],
        bstack11l1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᗳ"): bstack11l1ll_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ᗴ"),
        bstack11l1ll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪᗵ"): {
            bstack11l1ll_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬᗶ"): test.nodeid
        },
        bstack11l1ll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᗷ"): bstack11l1l11l11_opy_(test.own_markers)
    }
    if bstack111l1l1l_opy_ in [bstack11l1ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫᗸ"), bstack11l1ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᗹ")]:
        bstack1l11111ll1_opy_[bstack11l1ll_opy_ (u"ࠬࡳࡥࡵࡣࠪᗺ")] = {
            bstack11l1ll_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᗻ"): bstack1l11111lll_opy_.get(bstack11l1ll_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᗼ"), [])
        }
    if bstack111l1l1l_opy_ == bstack11l1ll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᗽ"):
        bstack1l11111ll1_opy_[bstack11l1ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᗾ")] = bstack11l1ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᗿ")
        bstack1l11111ll1_opy_[bstack11l1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᘀ")] = bstack1l11111lll_opy_[bstack11l1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᘁ")]
        bstack1l11111ll1_opy_[bstack11l1ll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᘂ")] = bstack1l11111lll_opy_[bstack11l1ll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᘃ")]
    if result:
        bstack1l11111ll1_opy_[bstack11l1ll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᘄ")] = result.outcome
        bstack1l11111ll1_opy_[bstack11l1ll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᘅ")] = result.duration * 1000
        bstack1l11111ll1_opy_[bstack11l1ll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᘆ")] = bstack1l11111lll_opy_[bstack11l1ll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᘇ")]
        if result.failed:
            bstack1l11111ll1_opy_[bstack11l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᘈ")] = bstack1l11l1111_opy_.bstack11llll1111_opy_(call.excinfo.typename)
            bstack1l11111ll1_opy_[bstack11l1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᘉ")] = bstack1l11l1111_opy_.bstack1lllllll11l_opy_(call.excinfo, result)
        bstack1l11111ll1_opy_[bstack11l1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᘊ")] = bstack1l11111lll_opy_[bstack11l1ll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᘋ")]
    if outcome:
        bstack1l11111ll1_opy_[bstack11l1ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᘌ")] = bstack11l1ll1l1l_opy_(outcome)
        bstack1l11111ll1_opy_[bstack11l1ll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᘍ")] = 0
        bstack1l11111ll1_opy_[bstack11l1ll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᘎ")] = bstack1l11111lll_opy_[bstack11l1ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᘏ")]
        if bstack1l11111ll1_opy_[bstack11l1ll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᘐ")] == bstack11l1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᘑ"):
            bstack1l11111ll1_opy_[bstack11l1ll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᘒ")] = bstack11l1ll_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪᘓ")  # bstack1lllll11l11_opy_
            bstack1l11111ll1_opy_[bstack11l1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᘔ")] = [{bstack11l1ll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᘕ"): [bstack11l1ll_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩᘖ")]}]
        bstack1l11111ll1_opy_[bstack11l1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᘗ")] = bstack1l11111lll_opy_[bstack11l1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᘘ")]
    return bstack1l11111ll1_opy_
def bstack1llll1llll1_opy_(test, bstack1l111ll111_opy_, bstack111l1l1l_opy_, result, call, outcome, bstack1llll1l1l1l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l111ll111_opy_[bstack11l1ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᘙ")]
    hook_name = bstack1l111ll111_opy_[bstack11l1ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬᘚ")]
    hook_data = {
        bstack11l1ll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᘛ"): bstack1l111ll111_opy_[bstack11l1ll_opy_ (u"ࠫࡺࡻࡩࡥࠩᘜ")],
        bstack11l1ll_opy_ (u"ࠬࡺࡹࡱࡧࠪᘝ"): bstack11l1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᘞ"),
        bstack11l1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᘟ"): bstack11l1ll_opy_ (u"ࠨࡽࢀࠫᘠ").format(bstack1111l1llll_opy_(hook_name)),
        bstack11l1ll_opy_ (u"ࠩࡥࡳࡩࡿࠧᘡ"): {
            bstack11l1ll_opy_ (u"ࠪࡰࡦࡴࡧࠨᘢ"): bstack11l1ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᘣ"),
            bstack11l1ll_opy_ (u"ࠬࡩ࡯ࡥࡧࠪᘤ"): None
        },
        bstack11l1ll_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬᘥ"): test.name,
        bstack11l1ll_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᘦ"): bstack1l11l1111_opy_.bstack1l11111l11_opy_(test, hook_name),
        bstack11l1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫᘧ"): file_path,
        bstack11l1ll_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫᘨ"): file_path,
        bstack11l1ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᘩ"): bstack11l1ll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬᘪ"),
        bstack11l1ll_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᘫ"): file_path,
        bstack11l1ll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᘬ"): bstack1l111ll111_opy_[bstack11l1ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᘭ")],
        bstack11l1ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᘮ"): bstack11l1ll_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫᘯ") if bstack1llll1ll1ll_opy_ == bstack11l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᘰ") else bstack11l1ll_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫᘱ"),
        bstack11l1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᘲ"): hook_type
    }
    bstack1lllll111l1_opy_ = bstack1l1111ll11_opy_(_1l111l11l1_opy_.get(test.nodeid, None))
    if bstack1lllll111l1_opy_:
        hook_data[bstack11l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫᘳ")] = bstack1lllll111l1_opy_
    if result:
        hook_data[bstack11l1ll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᘴ")] = result.outcome
        hook_data[bstack11l1ll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᘵ")] = result.duration * 1000
        hook_data[bstack11l1ll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᘶ")] = bstack1l111ll111_opy_[bstack11l1ll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᘷ")]
        if result.failed:
            hook_data[bstack11l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᘸ")] = bstack1l11l1111_opy_.bstack11llll1111_opy_(call.excinfo.typename)
            hook_data[bstack11l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᘹ")] = bstack1l11l1111_opy_.bstack1lllllll11l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11l1ll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᘺ")] = bstack11l1ll1l1l_opy_(outcome)
        hook_data[bstack11l1ll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᘻ")] = 100
        hook_data[bstack11l1ll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᘼ")] = bstack1l111ll111_opy_[bstack11l1ll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᘽ")]
        if hook_data[bstack11l1ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᘾ")] == bstack11l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᘿ"):
            hook_data[bstack11l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᙀ")] = bstack11l1ll_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧᙁ")  # bstack1lllll11l11_opy_
            hook_data[bstack11l1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᙂ")] = [{bstack11l1ll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᙃ"): [bstack11l1ll_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭ᙄ")]}]
    if bstack1llll1l1l1l_opy_:
        hook_data[bstack11l1ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᙅ")] = bstack1llll1l1l1l_opy_.result
        hook_data[bstack11l1ll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᙆ")] = bstack11l1l1l1l1_opy_(bstack1l111ll111_opy_[bstack11l1ll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᙇ")], bstack1l111ll111_opy_[bstack11l1ll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᙈ")])
        hook_data[bstack11l1ll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᙉ")] = bstack1l111ll111_opy_[bstack11l1ll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᙊ")]
        if hook_data[bstack11l1ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᙋ")] == bstack11l1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᙌ"):
            hook_data[bstack11l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᙍ")] = bstack1l11l1111_opy_.bstack11llll1111_opy_(bstack1llll1l1l1l_opy_.exception_type)
            hook_data[bstack11l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᙎ")] = [{bstack11l1ll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᙏ"): bstack11l11l1lll_opy_(bstack1llll1l1l1l_opy_.exception)}]
    return hook_data
def bstack1llll1l11l1_opy_(test, bstack1l11111lll_opy_, bstack111l1l1l_opy_, result=None, call=None, outcome=None):
    bstack1l11111ll1_opy_ = bstack1lllll1l11l_opy_(test, bstack1l11111lll_opy_, result, call, bstack111l1l1l_opy_, outcome)
    driver = getattr(test, bstack11l1ll_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨᙐ"), None)
    if bstack111l1l1l_opy_ == bstack11l1ll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᙑ") and driver:
        bstack1l11111ll1_opy_[bstack11l1ll_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨᙒ")] = bstack1l11l1111_opy_.bstack1l1111l111_opy_(driver)
    if bstack111l1l1l_opy_ == bstack11l1ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫᙓ"):
        bstack111l1l1l_opy_ = bstack11l1ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᙔ")
    bstack1l11l1lll1_opy_ = {
        bstack11l1ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᙕ"): bstack111l1l1l_opy_,
        bstack11l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨᙖ"): bstack1l11111ll1_opy_
    }
    bstack1l11l1111_opy_.bstack1l11l1l11l_opy_(bstack1l11l1lll1_opy_)
def bstack1llll1l111l_opy_(test, bstack1l11111lll_opy_, bstack111l1l1l_opy_, result=None, call=None, outcome=None, bstack1llll1l1l1l_opy_=None):
    hook_data = bstack1llll1llll1_opy_(test, bstack1l11111lll_opy_, bstack111l1l1l_opy_, result, call, outcome, bstack1llll1l1l1l_opy_)
    bstack1l11l1lll1_opy_ = {
        bstack11l1ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᙗ"): bstack111l1l1l_opy_,
        bstack11l1ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪᙘ"): hook_data
    }
    bstack1l11l1111_opy_.bstack1l11l1l11l_opy_(bstack1l11l1lll1_opy_)
def bstack1l1111ll11_opy_(bstack1l11111lll_opy_):
    if not bstack1l11111lll_opy_:
        return None
    if bstack1l11111lll_opy_.get(bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᙙ"), None):
        return getattr(bstack1l11111lll_opy_[bstack11l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᙚ")], bstack11l1ll_opy_ (u"ࠫࡺࡻࡩࡥࠩᙛ"), None)
    return bstack1l11111lll_opy_.get(bstack11l1ll_opy_ (u"ࠬࡻࡵࡪࡦࠪᙜ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1l11l1111_opy_.on():
            return
        places = [bstack11l1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᙝ"), bstack11l1ll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᙞ"), bstack11l1ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᙟ")]
        bstack1l11l1l111_opy_ = []
        for bstack1lllll1l111_opy_ in places:
            records = caplog.get_records(bstack1lllll1l111_opy_)
            bstack1llll1ll1l1_opy_ = bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᙠ") if bstack1lllll1l111_opy_ == bstack11l1ll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᙡ") else bstack11l1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᙢ")
            bstack1llll1l11ll_opy_ = request.node.nodeid + (bstack11l1ll_opy_ (u"ࠬ࠭ᙣ") if bstack1lllll1l111_opy_ == bstack11l1ll_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᙤ") else bstack11l1ll_opy_ (u"ࠧ࠮ࠩᙥ") + bstack1lllll1l111_opy_)
            bstack1llll11llll_opy_ = bstack1l1111ll11_opy_(_1l111l11l1_opy_.get(bstack1llll1l11ll_opy_, None))
            if not bstack1llll11llll_opy_:
                continue
            for record in records:
                if bstack11ll111l1l_opy_(record.message):
                    continue
                bstack1l11l1l111_opy_.append({
                    bstack11l1ll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᙦ"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack11l1ll_opy_ (u"ࠩ࡝ࠫᙧ"),
                    bstack11l1ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᙨ"): record.levelname,
                    bstack11l1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᙩ"): record.message,
                    bstack1llll1ll1l1_opy_: bstack1llll11llll_opy_
                })
        if len(bstack1l11l1l111_opy_) > 0:
            bstack1l11l1111_opy_.bstack1l11ll11l1_opy_(bstack1l11l1l111_opy_)
    except Exception as err:
        print(bstack11l1ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡣࡰࡰࡧࡣ࡫࡯ࡸࡵࡷࡵࡩ࠿ࠦࡻࡾࠩᙪ"), str(err))
def bstack1l1ll111ll_opy_(sequence, driver_command, response):
    if sequence == bstack11l1ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᙫ"):
        if driver_command == bstack11l1ll_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫᙬ"):
            bstack1l11l1111_opy_.bstack1l11l1l11_opy_({
                bstack11l1ll_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧ᙭"): response[bstack11l1ll_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨ᙮")],
                bstack11l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᙯ"): store[bstack11l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᙰ")]
            })
def bstack111l11ll_opy_():
    global bstack1llll11lll_opy_
    bstack1l11l1111_opy_.bstack1l111111l1_opy_()
    for driver in bstack1llll11lll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack111l1ll1l_opy_(self, *args, **kwargs):
    bstack1ll1l1l1ll_opy_ = bstack111l1l1ll_opy_(self, *args, **kwargs)
    bstack1l11l1111_opy_.bstack1lll1111l_opy_(self)
    return bstack1ll1l1l1ll_opy_
def bstack11l111l1_opy_(framework_name):
    global bstack1ll11llll1_opy_
    global bstack1ll1ll11l1_opy_
    bstack1ll11llll1_opy_ = framework_name
    logger.info(bstack1l1ll1111_opy_.format(bstack1ll11llll1_opy_.split(bstack11l1ll_opy_ (u"ࠬ࠳ࠧᙱ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack11l1ll11l1_opy_():
            Service.start = bstack111llll1_opy_
            Service.stop = bstack1lll1lllll_opy_
            webdriver.Remote.__init__ = bstack1ll1l1l11_opy_
            webdriver.Remote.get = bstack111ll11ll_opy_
            if not isinstance(os.getenv(bstack11l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧᙲ")), str):
                return
            WebDriver.close = bstack1ll111l1ll_opy_
            WebDriver.quit = bstack1ll1llll1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.bstack1l1lll111_opy_ = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.bstack1l1l11ll_opy_ = getAccessibilityResultsSummary
        if not bstack11l1ll11l1_opy_() and bstack1l11l1111_opy_.on():
            webdriver.Remote.__init__ = bstack111l1ll1l_opy_
        bstack1ll1ll11l1_opy_ = True
    except Exception as e:
        pass
    bstack1ll11l11_opy_()
    if os.environ.get(bstack11l1ll_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬᙳ")):
        bstack1ll1ll11l1_opy_ = eval(os.environ.get(bstack11l1ll_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭ᙴ")))
    if not bstack1ll1ll11l1_opy_:
        bstack1l1lll1l11_opy_(bstack11l1ll_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦᙵ"), bstack1l1l11ll1l_opy_)
    if bstack11ll11l1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1lll1ll111_opy_
        except Exception as e:
            logger.error(bstack1l111111_opy_.format(str(e)))
    if bstack11l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᙶ") in str(framework_name).lower():
        if not bstack11l1ll11l1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1l1l11l1ll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack111llll11_opy_
            Config.getoption = bstack1111l1ll1_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack111111lll_opy_
        except Exception as e:
            pass
def bstack1ll1llll1_opy_(self):
    global bstack1ll11llll1_opy_
    global bstack1l111l11l_opy_
    global bstack1l11111ll_opy_
    try:
        if bstack11l1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᙷ") in bstack1ll11llll1_opy_ and self.session_id != None and bstack111l1lll_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩᙸ"), bstack11l1ll_opy_ (u"࠭ࠧᙹ")) != bstack11l1ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᙺ"):
            bstack1lllllll1l_opy_ = bstack11l1ll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᙻ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᙼ")
            bstack11llll11l_opy_(logger, True)
            if self != None:
                bstack1l1ll1llll_opy_(self, bstack1lllllll1l_opy_, bstack11l1ll_opy_ (u"ࠪ࠰ࠥ࠭ᙽ").join(threading.current_thread().bstackTestErrorMessages))
        threading.current_thread().testStatus = bstack11l1ll_opy_ (u"ࠫࠬᙾ")
    except Exception as e:
        logger.debug(bstack11l1ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨᙿ") + str(e))
    bstack1l11111ll_opy_(self)
    self.session_id = None
def bstack1ll1l1l11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l111l11l_opy_
    global bstack111l11l11_opy_
    global bstack11lllllll_opy_
    global bstack1ll11llll1_opy_
    global bstack111l1l1ll_opy_
    global bstack1llll11lll_opy_
    global bstack1llll1111_opy_
    global bstack1ll111ll1_opy_
    global bstack1lllll1l1ll_opy_
    global bstack1l1111l1_opy_
    CONFIG[bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ ")] = str(bstack1ll11llll1_opy_) + str(__version__)
    command_executor = bstack1l1111111_opy_(bstack1llll1111_opy_)
    logger.debug(bstack111l1111l_opy_.format(command_executor))
    proxy = bstack1llll11l1l_opy_(CONFIG, proxy)
    bstack1l1ll1ll_opy_ = 0
    try:
        if bstack11lllllll_opy_ is True:
            bstack1l1ll1ll_opy_ = int(os.environ.get(bstack11l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᚁ")))
    except:
        bstack1l1ll1ll_opy_ = 0
    bstack1ll111ll_opy_ = bstack1l1ll11l11_opy_(CONFIG, bstack1l1ll1ll_opy_)
    logger.debug(bstack1l1l11lll1_opy_.format(str(bstack1ll111ll_opy_)))
    bstack1l1111l1_opy_ = CONFIG.get(bstack11l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᚂ"))[bstack1l1ll1ll_opy_]
    if bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᚃ") in CONFIG and CONFIG[bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᚄ")]:
        bstack1lll1lll11_opy_(bstack1ll111ll_opy_, bstack1ll111ll1_opy_)
    if desired_capabilities:
        bstack1ll11l11l1_opy_ = bstack1ll1llll11_opy_(desired_capabilities)
        bstack1ll11l11l1_opy_[bstack11l1ll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᚅ")] = bstack1ll1111lll_opy_(CONFIG)
        bstack1l111lll_opy_ = bstack1l1ll11l11_opy_(bstack1ll11l11l1_opy_)
        if bstack1l111lll_opy_:
            bstack1ll111ll_opy_ = update(bstack1l111lll_opy_, bstack1ll111ll_opy_)
        desired_capabilities = None
    if options:
        bstack1ll11ll11l_opy_(options, bstack1ll111ll_opy_)
    if not options:
        options = bstack1l1ll11l1_opy_(bstack1ll111ll_opy_)
    if bstack11ll11ll1_opy_.bstack1lll111l1l_opy_(CONFIG, bstack1l1ll1ll_opy_) and bstack11ll11ll1_opy_.bstack1llll1l1l1_opy_(bstack1ll111ll_opy_, options):
        bstack1lllll1l1ll_opy_ = True
        bstack11ll11ll1_opy_.set_capabilities(bstack1ll111ll_opy_, CONFIG)
    if proxy and bstack11l1ll1l1_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬᚆ")):
        options.proxy(proxy)
    if options and bstack11l1ll1l1_opy_() >= version.parse(bstack11l1ll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᚇ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11l1ll1l1_opy_() < version.parse(bstack11l1ll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᚈ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1ll111ll_opy_)
    logger.info(bstack1l1lll111l_opy_)
    if bstack11l1ll1l1_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨᚉ")):
        bstack111l1l1ll_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l1ll1l1_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᚊ")):
        bstack111l1l1ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l1ll1l1_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪᚋ")):
        bstack111l1l1ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack111l1l1ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1l1l11l1l_opy_ = bstack11l1ll_opy_ (u"ࠫࠬᚌ")
        if bstack11l1ll1l1_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭ᚍ")):
            bstack1l1l11l1l_opy_ = self.caps.get(bstack11l1ll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨᚎ"))
        else:
            bstack1l1l11l1l_opy_ = self.capabilities.get(bstack11l1ll_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢᚏ"))
        if bstack1l1l11l1l_opy_:
            bstack11l11ll1l_opy_(bstack1l1l11l1l_opy_)
            if bstack11l1ll1l1_opy_() <= version.parse(bstack11l1ll_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨᚐ")):
                self.command_executor._url = bstack11l1ll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᚑ") + bstack1llll1111_opy_ + bstack11l1ll_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢᚒ")
            else:
                self.command_executor._url = bstack11l1ll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨᚓ") + bstack1l1l11l1l_opy_ + bstack11l1ll_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨᚔ")
            logger.debug(bstack11ll111l_opy_.format(bstack1l1l11l1l_opy_))
        else:
            logger.debug(bstack1ll1ll1ll1_opy_.format(bstack11l1ll_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢᚕ")))
    except Exception as e:
        logger.debug(bstack1ll1ll1ll1_opy_.format(e))
    bstack1l111l11l_opy_ = self.session_id
    if bstack11l1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᚖ") in bstack1ll11llll1_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        bstack1l11l1111_opy_.bstack1lll1111l_opy_(self)
    bstack1llll11lll_opy_.append(self)
    if bstack11l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᚗ") in CONFIG and bstack11l1ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᚘ") in CONFIG[bstack11l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᚙ")][bstack1l1ll1ll_opy_]:
        bstack111l11l11_opy_ = CONFIG[bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᚚ")][bstack1l1ll1ll_opy_][bstack11l1ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ᚛")]
    logger.debug(bstack1l1l1ll1ll_opy_.format(bstack1l111l11l_opy_))
def bstack111ll11ll_opy_(self, url):
    global bstack1l11l111_opy_
    global CONFIG
    try:
        bstack1ll11l1lll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack11l1l1l1_opy_.format(str(err)))
    try:
        bstack1l11l111_opy_(self, url)
    except Exception as e:
        try:
            bstack1ll1l11l_opy_ = str(e)
            if any(err_msg in bstack1ll1l11l_opy_ for err_msg in bstack1111lll1l_opy_):
                bstack1ll11l1lll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack11l1l1l1_opy_.format(str(err)))
        raise e
def bstack1llllllll1_opy_(item, when):
    global bstack111l111l1_opy_
    try:
        bstack111l111l1_opy_(item, when)
    except Exception as e:
        pass
def bstack111111lll_opy_(item, call, rep):
    global bstack1l1l1l1lll_opy_
    global bstack1llll11lll_opy_
    name = bstack11l1ll_opy_ (u"࠭ࠧ᚜")
    try:
        if rep.when == bstack11l1ll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ᚝"):
            bstack1l111l11l_opy_ = threading.current_thread().bstackSessionId
            bstack1lllll1l1l1_opy_ = item.config.getoption(bstack11l1ll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ᚞"))
            try:
                if (str(bstack1lllll1l1l1_opy_).lower() != bstack11l1ll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ᚟")):
                    name = str(rep.nodeid)
                    bstack1111llll_opy_ = bstack11111111_opy_(bstack11l1ll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᚠ"), name, bstack11l1ll_opy_ (u"ࠫࠬᚡ"), bstack11l1ll_opy_ (u"ࠬ࠭ᚢ"), bstack11l1ll_opy_ (u"࠭ࠧᚣ"), bstack11l1ll_opy_ (u"ࠧࠨᚤ"))
                    os.environ[bstack11l1ll_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫᚥ")] = name
                    for driver in bstack1llll11lll_opy_:
                        if bstack1l111l11l_opy_ == driver.session_id:
                            driver.execute_script(bstack1111llll_opy_)
            except Exception as e:
                logger.debug(bstack11l1ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩᚦ").format(str(e)))
            try:
                bstack1l1ll1l11_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11l1ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᚧ"):
                    status = bstack11l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᚨ") if rep.outcome.lower() == bstack11l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᚩ") else bstack11l1ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᚪ")
                    reason = bstack11l1ll_opy_ (u"ࠧࠨᚫ")
                    if status == bstack11l1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᚬ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11l1ll_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᚭ") if status == bstack11l1ll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᚮ") else bstack11l1ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᚯ")
                    data = name + bstack11l1ll_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧᚰ") if status == bstack11l1ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᚱ") else name + bstack11l1ll_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪᚲ") + reason
                    bstack1llllll11l_opy_ = bstack11111111_opy_(bstack11l1ll_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪᚳ"), bstack11l1ll_opy_ (u"ࠩࠪᚴ"), bstack11l1ll_opy_ (u"ࠪࠫᚵ"), bstack11l1ll_opy_ (u"ࠫࠬᚶ"), level, data)
                    for driver in bstack1llll11lll_opy_:
                        if bstack1l111l11l_opy_ == driver.session_id:
                            driver.execute_script(bstack1llllll11l_opy_)
            except Exception as e:
                logger.debug(bstack11l1ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩᚷ").format(str(e)))
    except Exception as e:
        logger.debug(bstack11l1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪᚸ").format(str(e)))
    bstack1l1l1l1lll_opy_(item, call, rep)
notset = Notset()
def bstack1111l1ll1_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1ll1l1111_opy_
    if str(name).lower() == bstack11l1ll_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧᚹ"):
        return bstack11l1ll_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢᚺ")
    else:
        return bstack1ll1l1111_opy_(self, name, default, skip)
def bstack1lll1ll111_opy_(self):
    global CONFIG
    global bstack1l111l111_opy_
    try:
        proxy = bstack1111l1l11_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11l1ll_opy_ (u"ࠩ࠱ࡴࡦࡩࠧᚻ")):
                proxies = bstack1l11ll1l_opy_(proxy, bstack1l1111111_opy_())
                if len(proxies) > 0:
                    protocol, bstack1111ll1ll_opy_ = proxies.popitem()
                    if bstack11l1ll_opy_ (u"ࠥ࠾࠴࠵ࠢᚼ") in bstack1111ll1ll_opy_:
                        return bstack1111ll1ll_opy_
                    else:
                        return bstack11l1ll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᚽ") + bstack1111ll1ll_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11l1ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤᚾ").format(str(e)))
    return bstack1l111l111_opy_(self)
def bstack11ll11l1_opy_():
    return (bstack11l1ll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᚿ") in CONFIG or bstack11l1ll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᛀ") in CONFIG) and bstack1ll1lllll_opy_() and bstack11l1ll1l1_opy_() >= version.parse(
        bstack1lllllllll_opy_)
def bstack1l1l1lll11_opy_(self,
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
    global bstack111l11l11_opy_
    global bstack11lllllll_opy_
    global bstack1ll11llll1_opy_
    CONFIG[bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᛁ")] = str(bstack1ll11llll1_opy_) + str(__version__)
    bstack1l1ll1ll_opy_ = 0
    try:
        if bstack11lllllll_opy_ is True:
            bstack1l1ll1ll_opy_ = int(os.environ.get(bstack11l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᛂ")))
    except:
        bstack1l1ll1ll_opy_ = 0
    CONFIG[bstack11l1ll_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᛃ")] = True
    bstack1ll111ll_opy_ = bstack1l1ll11l11_opy_(CONFIG, bstack1l1ll1ll_opy_)
    logger.debug(bstack1l1l11lll1_opy_.format(str(bstack1ll111ll_opy_)))
    if CONFIG.get(bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᛄ")):
        bstack1lll1lll11_opy_(bstack1ll111ll_opy_, bstack1ll111ll1_opy_)
    if bstack11l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᛅ") in CONFIG and bstack11l1ll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᛆ") in CONFIG[bstack11l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᛇ")][bstack1l1ll1ll_opy_]:
        bstack111l11l11_opy_ = CONFIG[bstack11l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᛈ")][bstack1l1ll1ll_opy_][bstack11l1ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᛉ")]
    import urllib
    import json
    bstack1l1l111ll_opy_ = bstack11l1ll_opy_ (u"ࠪࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠬᛊ") + urllib.parse.quote(json.dumps(bstack1ll111ll_opy_))
    browser = self.connect(bstack1l1l111ll_opy_)
    return browser
def bstack1ll11l11_opy_():
    global bstack1ll1ll11l1_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1l1l1lll11_opy_
        bstack1ll1ll11l1_opy_ = True
    except Exception as e:
        pass
def bstack1llll1lll11_opy_():
    global CONFIG
    global bstack1l1llllll1_opy_
    global bstack1llll1111_opy_
    global bstack1ll111ll1_opy_
    global bstack11lllllll_opy_
    CONFIG = json.loads(os.environ.get(bstack11l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪᛋ")))
    bstack1l1llllll1_opy_ = eval(os.environ.get(bstack11l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ᛌ")))
    bstack1llll1111_opy_ = os.environ.get(bstack11l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡎࡕࡃࡡࡘࡖࡑ࠭ᛍ"))
    bstack11l1lll11_opy_(CONFIG, bstack1l1llllll1_opy_)
    bstack1111l1111_opy_()
    global bstack111l1l1ll_opy_
    global bstack1l11111ll_opy_
    global bstack11lll1lll_opy_
    global bstack1111lllll_opy_
    global bstack1ll1llll_opy_
    global bstack111l1llll_opy_
    global bstack11111lll1_opy_
    global bstack1l11l111_opy_
    global bstack1l111l111_opy_
    global bstack1ll1l1111_opy_
    global bstack111l111l1_opy_
    global bstack1l1l1l1lll_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack111l1l1ll_opy_ = webdriver.Remote.__init__
        bstack1l11111ll_opy_ = WebDriver.quit
        bstack11111lll1_opy_ = WebDriver.close
        bstack1l11l111_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11l1ll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᛎ") in CONFIG or bstack11l1ll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᛏ") in CONFIG) and bstack1ll1lllll_opy_():
        if bstack11l1ll1l1_opy_() < version.parse(bstack1lllllllll_opy_):
            logger.error(bstack1lll1l1l1_opy_.format(bstack11l1ll1l1_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1l111l111_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack1l111111_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1ll1l1111_opy_ = Config.getoption
        from _pytest import runner
        bstack111l111l1_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1llll1l1_opy_)
    try:
        from pytest_bdd import reporting
        bstack1l1l1l1lll_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11l1ll_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪᛐ"))
    bstack1ll111ll1_opy_ = CONFIG.get(bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᛑ"), {}).get(bstack11l1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᛒ"))
    bstack11lllllll_opy_ = True
    bstack11l111l1_opy_(bstack1l1llll1_opy_)
if (bstack11l1lllll1_opy_()):
    bstack1llll1lll11_opy_()
@bstack1l11l11lll_opy_(class_method=False)
def bstack1llll1l1l11_opy_(hook_name, event, bstack1llll1l1111_opy_=None):
    if hook_name not in [bstack11l1ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᛓ"), bstack11l1ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᛔ"), bstack11l1ll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᛕ"), bstack11l1ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᛖ"), bstack11l1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᛗ"), bstack11l1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᛘ"), bstack11l1ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᛙ"), bstack11l1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᛚ")]:
        return
    node = store[bstack11l1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᛛ")]
    if hook_name in [bstack11l1ll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᛜ"), bstack11l1ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᛝ")]:
        node = store[bstack11l1ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨᛞ")]
    elif hook_name in [bstack11l1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᛟ"), bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬᛠ")]:
        node = store[bstack11l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪᛡ")]
    if event == bstack11l1ll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ᛢ"):
        hook_type = bstack1111ll111l_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack1l111ll111_opy_ = {
            bstack11l1ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᛣ"): uuid,
            bstack11l1ll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᛤ"): bstack11ll1l11_opy_(),
            bstack11l1ll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᛥ"): bstack11l1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᛦ"),
            bstack11l1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᛧ"): hook_type,
            bstack11l1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨᛨ"): hook_name
        }
        store[bstack11l1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᛩ")].append(uuid)
        bstack1llll1l1lll_opy_ = node.nodeid
        if hook_type == bstack11l1ll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᛪ"):
            if not _1l111l11l1_opy_.get(bstack1llll1l1lll_opy_, None):
                _1l111l11l1_opy_[bstack1llll1l1lll_opy_] = {bstack11l1ll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ᛫"): []}
            _1l111l11l1_opy_[bstack1llll1l1lll_opy_][bstack11l1ll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ᛬")].append(bstack1l111ll111_opy_[bstack11l1ll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ᛭")])
        _1l111l11l1_opy_[bstack1llll1l1lll_opy_ + bstack11l1ll_opy_ (u"ࠫ࠲࠭ᛮ") + hook_name] = bstack1l111ll111_opy_
        bstack1llll1l111l_opy_(node, bstack1l111ll111_opy_, bstack11l1ll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᛯ"))
    elif event == bstack11l1ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᛰ"):
        bstack1l111l1ll1_opy_ = node.nodeid + bstack11l1ll_opy_ (u"ࠧ࠮ࠩᛱ") + hook_name
        _1l111l11l1_opy_[bstack1l111l1ll1_opy_][bstack11l1ll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᛲ")] = bstack11ll1l11_opy_()
        bstack1llll1l1ll1_opy_(_1l111l11l1_opy_[bstack1l111l1ll1_opy_][bstack11l1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᛳ")])
        bstack1llll1l111l_opy_(node, _1l111l11l1_opy_[bstack1l111l1ll1_opy_], bstack11l1ll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᛴ"), bstack1llll1l1l1l_opy_=bstack1llll1l1111_opy_)
def bstack1llll1ll11l_opy_():
    global bstack1llll1ll1ll_opy_
    if bstack11l11lll_opy_():
        bstack1llll1ll1ll_opy_ = bstack11l1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᛵ")
    else:
        bstack1llll1ll1ll_opy_ = bstack11l1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᛶ")
@bstack1l11l1111_opy_.bstack1llllll1lll_opy_
def bstack1llll1lllll_opy_():
    bstack1llll1ll11l_opy_()
    if bstack1ll1lllll_opy_():
        bstack1lll1lll_opy_(bstack1l1ll111ll_opy_)
    bstack11l111l11l_opy_ = bstack11l111l1l1_opy_(bstack1llll1l1l11_opy_)
bstack1llll1lllll_opy_()