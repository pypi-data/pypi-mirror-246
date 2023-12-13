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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack11l1l111l1_opy_, bstack1ll11ll1l1_opy_, bstack111l1lll_opy_, bstack111l1l11_opy_, \
    bstack11l1l1ll11_opy_
def bstack111l11ll_opy_(bstack11111l1lll_opy_):
    for driver in bstack11111l1lll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1ll1llll_opy_(driver, status, reason=bstack11l1ll_opy_ (u"ࠩࠪᏎ")):
    bstack1ll1l11ll1_opy_ = Config.get_instance()
    if bstack1ll1l11ll1_opy_.bstack11llllll11_opy_():
        return
    bstack1111llll_opy_ = bstack11111111_opy_(bstack11l1ll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭Ꮟ"), bstack11l1ll_opy_ (u"ࠫࠬᏐ"), status, reason, bstack11l1ll_opy_ (u"ࠬ࠭Ꮡ"), bstack11l1ll_opy_ (u"࠭ࠧᏒ"))
    driver.execute_script(bstack1111llll_opy_)
def bstack11l1l111l_opy_(page, status, reason=bstack11l1ll_opy_ (u"ࠧࠨᏓ")):
    try:
        if page is None:
            return
        bstack1ll1l11ll1_opy_ = Config.get_instance()
        if bstack1ll1l11ll1_opy_.bstack11llllll11_opy_():
            return
        bstack1111llll_opy_ = bstack11111111_opy_(bstack11l1ll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᏔ"), bstack11l1ll_opy_ (u"ࠩࠪᏕ"), status, reason, bstack11l1ll_opy_ (u"ࠪࠫᏖ"), bstack11l1ll_opy_ (u"ࠫࠬᏗ"))
        page.evaluate(bstack11l1ll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᏘ"), bstack1111llll_opy_)
    except Exception as e:
        print(bstack11l1ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦᏙ"), e)
def bstack11111111_opy_(type, name, status, reason, bstack111ll1111_opy_, bstack11ll11lll_opy_):
    bstack11ll1l1l1_opy_ = {
        bstack11l1ll_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧᏚ"): type,
        bstack11l1ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᏛ"): {}
    }
    if type == bstack11l1ll_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫᏜ"):
        bstack11ll1l1l1_opy_[bstack11l1ll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭Ꮭ")][bstack11l1ll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᏞ")] = bstack111ll1111_opy_
        bstack11ll1l1l1_opy_[bstack11l1ll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᏟ")][bstack11l1ll_opy_ (u"࠭ࡤࡢࡶࡤࠫᏠ")] = json.dumps(str(bstack11ll11lll_opy_))
    if type == bstack11l1ll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᏡ"):
        bstack11ll1l1l1_opy_[bstack11l1ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᏢ")][bstack11l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᏣ")] = name
    if type == bstack11l1ll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭Ꮴ"):
        bstack11ll1l1l1_opy_[bstack11l1ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᏥ")][bstack11l1ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᏦ")] = status
        if status == bstack11l1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ꮷ") and str(reason) != bstack11l1ll_opy_ (u"ࠢࠣᏨ"):
            bstack11ll1l1l1_opy_[bstack11l1ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᏩ")][bstack11l1ll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᏪ")] = json.dumps(str(reason))
    bstack1l1l1lll1_opy_ = bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨᏫ").format(json.dumps(bstack11ll1l1l1_opy_))
    return bstack1l1l1lll1_opy_
def bstack1ll11l1lll_opy_(url, config, logger, bstack1lll1111ll_opy_=False):
    hostname = bstack1ll11ll1l1_opy_(url)
    is_private = bstack111l1l11_opy_(hostname)
    try:
        if is_private or bstack1lll1111ll_opy_:
            file_path = bstack11l1l111l1_opy_(bstack11l1ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᏬ"), bstack11l1ll_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᏭ"), logger)
            if os.environ.get(bstack11l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᏮ")) and eval(
                    os.environ.get(bstack11l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᏯ"))):
                return
            if (bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᏰ") in config and not config[bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭Ᏹ")]):
                os.environ[bstack11l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᏲ")] = str(True)
                bstack11111l1ll1_opy_ = {bstack11l1ll_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭Ᏻ"): hostname}
                bstack11l1l1ll11_opy_(bstack11l1ll_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᏴ"), bstack11l1ll_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫᏵ"), bstack11111l1ll1_opy_, logger)
    except Exception as e:
        pass
def bstack1lll1lll11_opy_(caps, bstack11111l1l1l_opy_):
    if bstack11l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᏶") in caps:
        caps[bstack11l1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᏷")][bstack11l1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨᏸ")] = True
        if bstack11111l1l1l_opy_:
            caps[bstack11l1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᏹ")][bstack11l1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᏺ")] = bstack11111l1l1l_opy_
    else:
        caps[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪᏻ")] = True
        if bstack11111l1l1l_opy_:
            caps[bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᏼ")] = bstack11111l1l1l_opy_
def bstack1111l1l1l1_opy_(bstack1l1111ll1l_opy_):
    bstack11111l1l11_opy_ = bstack111l1lll_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫᏽ"), bstack11l1ll_opy_ (u"ࠨࠩ᏾"))
    if bstack11111l1l11_opy_ == bstack11l1ll_opy_ (u"ࠩࠪ᏿") or bstack11111l1l11_opy_ == bstack11l1ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ᐀"):
        threading.current_thread().testStatus = bstack1l1111ll1l_opy_
    else:
        if bstack1l1111ll1l_opy_ == bstack11l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᐁ"):
            threading.current_thread().testStatus = bstack1l1111ll1l_opy_