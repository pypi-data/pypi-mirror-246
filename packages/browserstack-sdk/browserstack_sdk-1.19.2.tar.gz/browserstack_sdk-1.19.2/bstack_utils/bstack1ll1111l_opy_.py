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
import re
from bstack_utils.bstack11l1111ll_opy_ import bstack1111l1l1ll_opy_
def bstack1111l1ll1l_opy_(fixture_name):
    if fixture_name.startswith(bstack1lllll1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᎙")):
        return bstack1lllll1_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ᎚")
    elif fixture_name.startswith(bstack1lllll1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᎛")):
        return bstack1lllll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧ᎜")
    elif fixture_name.startswith(bstack1lllll1_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᎝")):
        return bstack1lllll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ᎞")
    elif fixture_name.startswith(bstack1lllll1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ᎟")):
        return bstack1lllll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᎠ")
def bstack1111ll111l_opy_(fixture_name):
    return bool(re.match(bstack1lllll1_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᎡ"), fixture_name))
def bstack1111ll1l11_opy_(fixture_name):
    return bool(re.match(bstack1lllll1_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᎢ"), fixture_name))
def bstack1111l1llll_opy_(fixture_name):
    return bool(re.match(bstack1lllll1_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᎣ"), fixture_name))
def bstack1111ll11ll_opy_(fixture_name):
    if fixture_name.startswith(bstack1lllll1_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᎤ")):
        return bstack1lllll1_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᎥ"), bstack1lllll1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᎦ")
    elif fixture_name.startswith(bstack1lllll1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᎧ")):
        return bstack1lllll1_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᎨ"), bstack1lllll1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᎩ")
    elif fixture_name.startswith(bstack1lllll1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ꭺ")):
        return bstack1lllll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭Ꭻ"), bstack1lllll1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᎬ")
    elif fixture_name.startswith(bstack1lllll1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᎭ")):
        return bstack1lllll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᎮ"), bstack1lllll1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᎯ")
    return None, None
def bstack1111ll11l1_opy_(hook_name):
    if hook_name in [bstack1lllll1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭Ꮀ"), bstack1lllll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᎱ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1111l1lll1_opy_(hook_name):
    if hook_name in [bstack1lllll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᎲ"), bstack1lllll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᎳ")]:
        return bstack1lllll1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᎴ")
    elif hook_name in [bstack1lllll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᎵ"), bstack1lllll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᎶ")]:
        return bstack1lllll1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᎷ")
    elif hook_name in [bstack1lllll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᎸ"), bstack1lllll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᎹ")]:
        return bstack1lllll1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᎺ")
    elif hook_name in [bstack1lllll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭Ꮋ"), bstack1lllll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭Ꮌ")]:
        return bstack1lllll1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᎽ")
    return hook_name
def bstack1111ll1l1l_opy_(node, scenario):
    if hasattr(node, bstack1lllll1_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᎾ")):
        parts = node.nodeid.rsplit(bstack1lllll1_opy_ (u"ࠣ࡝ࠥᎿ"))
        params = parts[-1]
        return bstack1lllll1_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᏀ").format(scenario.name, params)
    return scenario.name
def bstack1111l1l1l1_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1lllll1_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᏁ")):
            examples = list(node.callspec.params[bstack1lllll1_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᏂ")].values())
        return examples
    except:
        return []
def bstack1111ll1111_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1111l1ll11_opy_(report):
    try:
        status = bstack1lllll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᏃ")
        if report.passed or (report.failed and hasattr(report, bstack1lllll1_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᏄ"))):
            status = bstack1lllll1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᏅ")
        elif report.skipped:
            status = bstack1lllll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᏆ")
        bstack1111l1l1ll_opy_(status)
    except:
        pass
def bstack11llll111_opy_(status):
    try:
        bstack1111ll1lll_opy_ = bstack1lllll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᏇ")
        if status == bstack1lllll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᏈ"):
            bstack1111ll1lll_opy_ = bstack1lllll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᏉ")
        elif status == bstack1lllll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭Ꮚ"):
            bstack1111ll1lll_opy_ = bstack1lllll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᏋ")
        bstack1111l1l1ll_opy_(bstack1111ll1lll_opy_)
    except:
        pass
def bstack1111ll1ll1_opy_(item=None, report=None, summary=None, extra=None):
    return