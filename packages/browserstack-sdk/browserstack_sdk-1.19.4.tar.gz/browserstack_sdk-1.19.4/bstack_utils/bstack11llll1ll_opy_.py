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
import re
from bstack_utils.bstack1l1ll1l11l_opy_ import bstack1111l1lll1_opy_
def bstack1111l1ll11_opy_(fixture_name):
    if fixture_name.startswith(bstack1lllll1l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᎳ")):
        return bstack1lllll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᎴ")
    elif fixture_name.startswith(bstack1lllll1l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᎵ")):
        return bstack1lllll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᎶ")
    elif fixture_name.startswith(bstack1lllll1l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᎷ")):
        return bstack1lllll1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᎸ")
    elif fixture_name.startswith(bstack1lllll1l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᎹ")):
        return bstack1lllll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᎺ")
def bstack1111lll11l_opy_(fixture_name):
    return bool(re.match(bstack1lllll1l_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࠪࡩࡹࡳࡩࡴࡪࡱࡱࢀࡲࡵࡤࡶ࡮ࡨ࠭ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩᎻ"), fixture_name))
def bstack1111l1llll_opy_(fixture_name):
    return bool(re.match(bstack1lllll1l_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭Ꮌ"), fixture_name))
def bstack1111ll11l1_opy_(fixture_name):
    return bool(re.match(bstack1lllll1l_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭Ꮍ"), fixture_name))
def bstack1111ll1111_opy_(fixture_name):
    if fixture_name.startswith(bstack1lllll1l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᎾ")):
        return bstack1lllll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᎿ"), bstack1lllll1l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᏀ")
    elif fixture_name.startswith(bstack1lllll1l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᏁ")):
        return bstack1lllll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪᏂ"), bstack1lllll1l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩᏃ")
    elif fixture_name.startswith(bstack1lllll1l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᏄ")):
        return bstack1lllll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᏅ"), bstack1lllll1l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᏆ")
    elif fixture_name.startswith(bstack1lllll1l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᏇ")):
        return bstack1lllll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᏈ"), bstack1lllll1l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧᏉ")
    return None, None
def bstack1111ll1l11_opy_(hook_name):
    if hook_name in [bstack1lllll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᏊ"), bstack1lllll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᏋ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1111ll11ll_opy_(hook_name):
    if hook_name in [bstack1lllll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᏌ"), bstack1lllll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᏍ")]:
        return bstack1lllll1l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᏎ")
    elif hook_name in [bstack1lllll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩᏏ"), bstack1lllll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩᏐ")]:
        return bstack1lllll1l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩᏑ")
    elif hook_name in [bstack1lllll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᏒ"), bstack1lllll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᏓ")]:
        return bstack1lllll1l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᏔ")
    elif hook_name in [bstack1lllll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᏕ"), bstack1lllll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᏖ")]:
        return bstack1lllll1l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧᏗ")
    return hook_name
def bstack1111lll111_opy_(node, scenario):
    if hasattr(node, bstack1lllll1l_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᏘ")):
        parts = node.nodeid.rsplit(bstack1lllll1l_opy_ (u"ࠨ࡛ࠣᏙ"))
        params = parts[-1]
        return bstack1lllll1l_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢᏚ").format(scenario.name, params)
    return scenario.name
def bstack1111l1ll1l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1lllll1l_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᏛ")):
            examples = list(node.callspec.params[bstack1lllll1l_opy_ (u"ࠩࡢࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡦࡺࡤࡱࡵࡲࡥࠨᏜ")].values())
        return examples
    except:
        return []
def bstack1111ll1l1l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1111ll1lll_opy_(report):
    try:
        status = bstack1lllll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᏝ")
        if report.passed or (report.failed and hasattr(report, bstack1lllll1l_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᏞ"))):
            status = bstack1lllll1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᏟ")
        elif report.skipped:
            status = bstack1lllll1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᏠ")
        bstack1111l1lll1_opy_(status)
    except:
        pass
def bstack11l1111l_opy_(status):
    try:
        bstack1111ll1ll1_opy_ = bstack1lllll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᏡ")
        if status == bstack1lllll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᏢ"):
            bstack1111ll1ll1_opy_ = bstack1lllll1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᏣ")
        elif status == bstack1lllll1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᏤ"):
            bstack1111ll1ll1_opy_ = bstack1lllll1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᏥ")
        bstack1111l1lll1_opy_(bstack1111ll1ll1_opy_)
    except:
        pass
def bstack1111ll111l_opy_(item=None, report=None, summary=None, extra=None):
    return