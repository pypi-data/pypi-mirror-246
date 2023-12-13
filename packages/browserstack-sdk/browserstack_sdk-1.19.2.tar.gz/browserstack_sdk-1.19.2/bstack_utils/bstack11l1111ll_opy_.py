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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack11ll1111l1_opy_, bstack1l1l111l_opy_, bstack11llll1l_opy_, bstack1ll1111l1l_opy_, \
    bstack11l1l11lll_opy_
def bstack1l1l11ll_opy_(bstack11111l1lll_opy_):
    for driver in bstack11111l1lll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack111l1l11l_opy_(driver, status, reason=bstack1lllll1_opy_ (u"ࠩࠪᏎ")):
    bstack1l1lll1ll_opy_ = Config.get_instance()
    if bstack1l1lll1ll_opy_.bstack11llll1ll1_opy_():
        return
    bstack1lllll11l_opy_ = bstack1ll111ll1l_opy_(bstack1lllll1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭Ꮟ"), bstack1lllll1_opy_ (u"ࠫࠬᏐ"), status, reason, bstack1lllll1_opy_ (u"ࠬ࠭Ꮡ"), bstack1lllll1_opy_ (u"࠭ࠧᏒ"))
    driver.execute_script(bstack1lllll11l_opy_)
def bstack11l11l11l_opy_(page, status, reason=bstack1lllll1_opy_ (u"ࠧࠨᏓ")):
    try:
        if page is None:
            return
        bstack1l1lll1ll_opy_ = Config.get_instance()
        if bstack1l1lll1ll_opy_.bstack11llll1ll1_opy_():
            return
        bstack1lllll11l_opy_ = bstack1ll111ll1l_opy_(bstack1lllll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᏔ"), bstack1lllll1_opy_ (u"ࠩࠪᏕ"), status, reason, bstack1lllll1_opy_ (u"ࠪࠫᏖ"), bstack1lllll1_opy_ (u"ࠫࠬᏗ"))
        page.evaluate(bstack1lllll1_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᏘ"), bstack1lllll11l_opy_)
    except Exception as e:
        print(bstack1lllll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦᏙ"), e)
def bstack1ll111ll1l_opy_(type, name, status, reason, bstack1l11l1l11_opy_, bstack1llllll111_opy_):
    bstack1ll11llll1_opy_ = {
        bstack1lllll1_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧᏚ"): type,
        bstack1lllll1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᏛ"): {}
    }
    if type == bstack1lllll1_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫᏜ"):
        bstack1ll11llll1_opy_[bstack1lllll1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭Ꮭ")][bstack1lllll1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᏞ")] = bstack1l11l1l11_opy_
        bstack1ll11llll1_opy_[bstack1lllll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᏟ")][bstack1lllll1_opy_ (u"࠭ࡤࡢࡶࡤࠫᏠ")] = json.dumps(str(bstack1llllll111_opy_))
    if type == bstack1lllll1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᏡ"):
        bstack1ll11llll1_opy_[bstack1lllll1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᏢ")][bstack1lllll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᏣ")] = name
    if type == bstack1lllll1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭Ꮴ"):
        bstack1ll11llll1_opy_[bstack1lllll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᏥ")][bstack1lllll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᏦ")] = status
        if status == bstack1lllll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ꮷ") and str(reason) != bstack1lllll1_opy_ (u"ࠢࠣᏨ"):
            bstack1ll11llll1_opy_[bstack1lllll1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᏩ")][bstack1lllll1_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᏪ")] = json.dumps(str(reason))
    bstack1llll11l1l_opy_ = bstack1lllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨᏫ").format(json.dumps(bstack1ll11llll1_opy_))
    return bstack1llll11l1l_opy_
def bstack1lll1l1l1l_opy_(url, config, logger, bstack1llll11l_opy_=False):
    hostname = bstack1l1l111l_opy_(url)
    is_private = bstack1ll1111l1l_opy_(hostname)
    try:
        if is_private or bstack1llll11l_opy_:
            file_path = bstack11ll1111l1_opy_(bstack1lllll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᏬ"), bstack1lllll1_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᏭ"), logger)
            if os.environ.get(bstack1lllll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᏮ")) and eval(
                    os.environ.get(bstack1lllll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᏯ"))):
                return
            if (bstack1lllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᏰ") in config and not config[bstack1lllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭Ᏹ")]):
                os.environ[bstack1lllll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᏲ")] = str(True)
                bstack11111ll111_opy_ = {bstack1lllll1_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭Ᏻ"): hostname}
                bstack11l1l11lll_opy_(bstack1lllll1_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᏴ"), bstack1lllll1_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫᏵ"), bstack11111ll111_opy_, logger)
    except Exception as e:
        pass
def bstack1ll1l1l11l_opy_(caps, bstack11111ll11l_opy_):
    if bstack1lllll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᏶") in caps:
        caps[bstack1lllll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᏷")][bstack1lllll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨᏸ")] = True
        if bstack11111ll11l_opy_:
            caps[bstack1lllll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᏹ")][bstack1lllll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᏺ")] = bstack11111ll11l_opy_
    else:
        caps[bstack1lllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪᏻ")] = True
        if bstack11111ll11l_opy_:
            caps[bstack1lllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᏼ")] = bstack11111ll11l_opy_
def bstack1111l1l1ll_opy_(bstack1l1111l1ll_opy_):
    bstack11111l1ll1_opy_ = bstack11llll1l_opy_(threading.current_thread(), bstack1lllll1_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫᏽ"), bstack1lllll1_opy_ (u"ࠨࠩ᏾"))
    if bstack11111l1ll1_opy_ == bstack1lllll1_opy_ (u"ࠩࠪ᏿") or bstack11111l1ll1_opy_ == bstack1lllll1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ᐀"):
        threading.current_thread().testStatus = bstack1l1111l1ll_opy_
    else:
        if bstack1l1111l1ll_opy_ == bstack1lllll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᐁ"):
            threading.current_thread().testStatus = bstack1l1111l1ll_opy_