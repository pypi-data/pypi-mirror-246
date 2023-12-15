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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack11l11llll1_opy_, bstack1l1l111ll_opy_, bstack1l1ll11l1_opy_, bstack1111llll_opy_, \
    bstack11l1l11l1l_opy_
def bstack1lll11l1l1_opy_(bstack11111ll11l_opy_):
    for driver in bstack11111ll11l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1l11ll1l_opy_(driver, status, reason=bstack1ll1l11_opy_ (u"ࠧࠨᏨ")):
    bstack111lll1ll_opy_ = Config.get_instance()
    if bstack111lll1ll_opy_.bstack11lllll1ll_opy_():
        return
    bstack1llllll1l_opy_ = bstack11111l1l1_opy_(bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᏩ"), bstack1ll1l11_opy_ (u"ࠩࠪᏪ"), status, reason, bstack1ll1l11_opy_ (u"ࠪࠫᏫ"), bstack1ll1l11_opy_ (u"ࠫࠬᏬ"))
    driver.execute_script(bstack1llllll1l_opy_)
def bstack1l1llllll_opy_(page, status, reason=bstack1ll1l11_opy_ (u"ࠬ࠭Ꮽ")):
    try:
        if page is None:
            return
        bstack111lll1ll_opy_ = Config.get_instance()
        if bstack111lll1ll_opy_.bstack11lllll1ll_opy_():
            return
        bstack1llllll1l_opy_ = bstack11111l1l1_opy_(bstack1ll1l11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᏮ"), bstack1ll1l11_opy_ (u"ࠧࠨᏯ"), status, reason, bstack1ll1l11_opy_ (u"ࠨࠩᏰ"), bstack1ll1l11_opy_ (u"ࠩࠪᏱ"))
        page.evaluate(bstack1ll1l11_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᏲ"), bstack1llllll1l_opy_)
    except Exception as e:
        print(bstack1ll1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡻࡾࠤᏳ"), e)
def bstack11111l1l1_opy_(type, name, status, reason, bstack1l11l1111_opy_, bstack1l1ll1ll1_opy_):
    bstack1l1ll11ll1_opy_ = {
        bstack1ll1l11_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬᏴ"): type,
        bstack1ll1l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᏵ"): {}
    }
    if type == bstack1ll1l11_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ᏶"):
        bstack1l1ll11ll1_opy_[bstack1ll1l11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ᏷")][bstack1ll1l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᏸ")] = bstack1l11l1111_opy_
        bstack1l1ll11ll1_opy_[bstack1ll1l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᏹ")][bstack1ll1l11_opy_ (u"ࠫࡩࡧࡴࡢࠩᏺ")] = json.dumps(str(bstack1l1ll1ll1_opy_))
    if type == bstack1ll1l11_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᏻ"):
        bstack1l1ll11ll1_opy_[bstack1ll1l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᏼ")][bstack1ll1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᏽ")] = name
    if type == bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ᏾"):
        bstack1l1ll11ll1_opy_[bstack1ll1l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ᏿")][bstack1ll1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ᐀")] = status
        if status == bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᐁ") and str(reason) != bstack1ll1l11_opy_ (u"ࠧࠨᐂ"):
            bstack1l1ll11ll1_opy_[bstack1ll1l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᐃ")][bstack1ll1l11_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᐄ")] = json.dumps(str(reason))
    bstack1l1l11ll1_opy_ = bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ᐅ").format(json.dumps(bstack1l1ll11ll1_opy_))
    return bstack1l1l11ll1_opy_
def bstack11111lll1_opy_(url, config, logger, bstack1llll111l1_opy_=False):
    hostname = bstack1l1l111ll_opy_(url)
    is_private = bstack1111llll_opy_(hostname)
    try:
        if is_private or bstack1llll111l1_opy_:
            file_path = bstack11l11llll1_opy_(bstack1ll1l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᐆ"), bstack1ll1l11_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᐇ"), logger)
            if os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᐈ")) and eval(
                    os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᐉ"))):
                return
            if (bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᐊ") in config and not config[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᐋ")]):
                os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᐌ")] = str(True)
                bstack11111l1ll1_opy_ = {bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫᐍ"): hostname}
                bstack11l1l11l1l_opy_(bstack1ll1l11_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᐎ"), bstack1ll1l11_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩᐏ"), bstack11111l1ll1_opy_, logger)
    except Exception as e:
        pass
def bstack111ll11l1_opy_(caps, bstack11111ll111_opy_):
    if bstack1ll1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᐐ") in caps:
        caps[bstack1ll1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᐑ")][bstack1ll1l11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ᐒ")] = True
        if bstack11111ll111_opy_:
            caps[bstack1ll1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᐓ")][bstack1ll1l11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᐔ")] = bstack11111ll111_opy_
    else:
        caps[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨᐕ")] = True
        if bstack11111ll111_opy_:
            caps[bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᐖ")] = bstack11111ll111_opy_
def bstack1111ll1l1l_opy_(bstack1l111ll11l_opy_):
    bstack11111l1lll_opy_ = bstack1l1ll11l1_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩᐗ"), bstack1ll1l11_opy_ (u"࠭ࠧᐘ"))
    if bstack11111l1lll_opy_ == bstack1ll1l11_opy_ (u"ࠧࠨᐙ") or bstack11111l1lll_opy_ == bstack1ll1l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᐚ"):
        threading.current_thread().testStatus = bstack1l111ll11l_opy_
    else:
        if bstack1l111ll11l_opy_ == bstack1ll1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᐛ"):
            threading.current_thread().testStatus = bstack1l111ll11l_opy_