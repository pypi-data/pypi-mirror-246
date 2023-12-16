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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack11l11lllll_opy_, bstack11ll1ll1_opy_, bstack11l1l11l1_opy_, bstack111l11111_opy_, \
    bstack11l1l11ll1_opy_
def bstack1llllll1ll_opy_(bstack11111ll1ll_opy_):
    for driver in bstack11111ll1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11lll1ll1_opy_(driver, status, reason=bstack1lllll1l_opy_ (u"ࠧࠨᏨ")):
    bstack1ll1ll1l1_opy_ = Config.get_instance()
    if bstack1ll1ll1l1_opy_.bstack11llllllll_opy_():
        return
    bstack1llllll1l_opy_ = bstack111l1l11l_opy_(bstack1lllll1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᏩ"), bstack1lllll1l_opy_ (u"ࠩࠪᏪ"), status, reason, bstack1lllll1l_opy_ (u"ࠪࠫᏫ"), bstack1lllll1l_opy_ (u"ࠫࠬᏬ"))
    driver.execute_script(bstack1llllll1l_opy_)
def bstack111lll111_opy_(page, status, reason=bstack1lllll1l_opy_ (u"ࠬ࠭Ꮽ")):
    try:
        if page is None:
            return
        bstack1ll1ll1l1_opy_ = Config.get_instance()
        if bstack1ll1ll1l1_opy_.bstack11llllllll_opy_():
            return
        bstack1llllll1l_opy_ = bstack111l1l11l_opy_(bstack1lllll1l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᏮ"), bstack1lllll1l_opy_ (u"ࠧࠨᏯ"), status, reason, bstack1lllll1l_opy_ (u"ࠨࠩᏰ"), bstack1lllll1l_opy_ (u"ࠩࠪᏱ"))
        page.evaluate(bstack1lllll1l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᏲ"), bstack1llllll1l_opy_)
    except Exception as e:
        print(bstack1lllll1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡻࡾࠤᏳ"), e)
def bstack111l1l11l_opy_(type, name, status, reason, bstack1l111l11_opy_, bstack1ll1111l11_opy_):
    bstack1lll1l1lll_opy_ = {
        bstack1lllll1l_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬᏴ"): type,
        bstack1lllll1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᏵ"): {}
    }
    if type == bstack1lllll1l_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ᏶"):
        bstack1lll1l1lll_opy_[bstack1lllll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ᏷")][bstack1lllll1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᏸ")] = bstack1l111l11_opy_
        bstack1lll1l1lll_opy_[bstack1lllll1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᏹ")][bstack1lllll1l_opy_ (u"ࠫࡩࡧࡴࡢࠩᏺ")] = json.dumps(str(bstack1ll1111l11_opy_))
    if type == bstack1lllll1l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᏻ"):
        bstack1lll1l1lll_opy_[bstack1lllll1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᏼ")][bstack1lllll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᏽ")] = name
    if type == bstack1lllll1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ᏾"):
        bstack1lll1l1lll_opy_[bstack1lllll1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ᏿")][bstack1lllll1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ᐀")] = status
        if status == bstack1lllll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᐁ") and str(reason) != bstack1lllll1l_opy_ (u"ࠧࠨᐂ"):
            bstack1lll1l1lll_opy_[bstack1lllll1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᐃ")][bstack1lllll1l_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᐄ")] = json.dumps(str(reason))
    bstack1l1ll1llll_opy_ = bstack1lllll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ᐅ").format(json.dumps(bstack1lll1l1lll_opy_))
    return bstack1l1ll1llll_opy_
def bstack1lllll111l_opy_(url, config, logger, bstack111l1l1l_opy_=False):
    hostname = bstack11ll1ll1_opy_(url)
    is_private = bstack111l11111_opy_(hostname)
    try:
        if is_private or bstack111l1l1l_opy_:
            file_path = bstack11l11lllll_opy_(bstack1lllll1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᐆ"), bstack1lllll1l_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᐇ"), logger)
            if os.environ.get(bstack1lllll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᐈ")) and eval(
                    os.environ.get(bstack1lllll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᐉ"))):
                return
            if (bstack1lllll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᐊ") in config and not config[bstack1lllll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᐋ")]):
                os.environ[bstack1lllll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᐌ")] = str(True)
                bstack11111ll111_opy_ = {bstack1lllll1l_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫᐍ"): hostname}
                bstack11l1l11ll1_opy_(bstack1lllll1l_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᐎ"), bstack1lllll1l_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩᐏ"), bstack11111ll111_opy_, logger)
    except Exception as e:
        pass
def bstack11llllll_opy_(caps, bstack11111ll1l1_opy_):
    if bstack1lllll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᐐ") in caps:
        caps[bstack1lllll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᐑ")][bstack1lllll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ᐒ")] = True
        if bstack11111ll1l1_opy_:
            caps[bstack1lllll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᐓ")][bstack1lllll1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᐔ")] = bstack11111ll1l1_opy_
    else:
        caps[bstack1lllll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨᐕ")] = True
        if bstack11111ll1l1_opy_:
            caps[bstack1lllll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᐖ")] = bstack11111ll1l1_opy_
def bstack1111l1lll1_opy_(bstack1l11l1l1ll_opy_):
    bstack11111ll11l_opy_ = bstack11l1l11l1_opy_(threading.current_thread(), bstack1lllll1l_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩᐗ"), bstack1lllll1l_opy_ (u"࠭ࠧᐘ"))
    if bstack11111ll11l_opy_ == bstack1lllll1l_opy_ (u"ࠧࠨᐙ") or bstack11111ll11l_opy_ == bstack1lllll1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᐚ"):
        threading.current_thread().testStatus = bstack1l11l1l1ll_opy_
    else:
        if bstack1l11l1l1ll_opy_ == bstack1lllll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᐛ"):
            threading.current_thread().testStatus = bstack1l11l1l1ll_opy_