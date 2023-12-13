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
import re
from bstack_utils.bstack11l111ll_opy_ import bstack1111l1l1l1_opy_
def bstack1111l1ll1l_opy_(fixture_name):
    if fixture_name.startswith(bstack11l1ll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᎙")):
        return bstack11l1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ᎚")
    elif fixture_name.startswith(bstack11l1ll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᎛")):
        return bstack11l1ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧ᎜")
    elif fixture_name.startswith(bstack11l1ll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᎝")):
        return bstack11l1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ᎞")
    elif fixture_name.startswith(bstack11l1ll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ᎟")):
        return bstack11l1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᎠ")
def bstack1111l1l111_opy_(fixture_name):
    return bool(re.match(bstack11l1ll_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᎡ"), fixture_name))
def bstack1111l1lll1_opy_(fixture_name):
    return bool(re.match(bstack11l1ll_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᎢ"), fixture_name))
def bstack1111ll11l1_opy_(fixture_name):
    return bool(re.match(bstack11l1ll_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᎣ"), fixture_name))
def bstack1111l1l11l_opy_(fixture_name):
    if fixture_name.startswith(bstack11l1ll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᎤ")):
        return bstack11l1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᎥ"), bstack11l1ll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᎦ")
    elif fixture_name.startswith(bstack11l1ll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᎧ")):
        return bstack11l1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᎨ"), bstack11l1ll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᎩ")
    elif fixture_name.startswith(bstack11l1ll_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ꭺ")):
        return bstack11l1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭Ꭻ"), bstack11l1ll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᎬ")
    elif fixture_name.startswith(bstack11l1ll_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᎭ")):
        return bstack11l1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᎮ"), bstack11l1ll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᎯ")
    return None, None
def bstack1111l1llll_opy_(hook_name):
    if hook_name in [bstack11l1ll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭Ꮀ"), bstack11l1ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᎱ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1111ll111l_opy_(hook_name):
    if hook_name in [bstack11l1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᎲ"), bstack11l1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᎳ")]:
        return bstack11l1ll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᎴ")
    elif hook_name in [bstack11l1ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᎵ"), bstack11l1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᎶ")]:
        return bstack11l1ll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᎷ")
    elif hook_name in [bstack11l1ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᎸ"), bstack11l1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᎹ")]:
        return bstack11l1ll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᎺ")
    elif hook_name in [bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭Ꮋ"), bstack11l1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭Ꮌ")]:
        return bstack11l1ll_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᎽ")
    return hook_name
def bstack1111l1ll11_opy_(node, scenario):
    if hasattr(node, bstack11l1ll_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᎾ")):
        parts = node.nodeid.rsplit(bstack11l1ll_opy_ (u"ࠣ࡝ࠥᎿ"))
        params = parts[-1]
        return bstack11l1ll_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᏀ").format(scenario.name, params)
    return scenario.name
def bstack1111ll11ll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11l1ll_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᏁ")):
            examples = list(node.callspec.params[bstack11l1ll_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᏂ")].values())
        return examples
    except:
        return []
def bstack1111ll1111_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1111ll1l1l_opy_(report):
    try:
        status = bstack11l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᏃ")
        if report.passed or (report.failed and hasattr(report, bstack11l1ll_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᏄ"))):
            status = bstack11l1ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᏅ")
        elif report.skipped:
            status = bstack11l1ll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᏆ")
        bstack1111l1l1l1_opy_(status)
    except:
        pass
def bstack1l1ll1l11_opy_(status):
    try:
        bstack1111l1l1ll_opy_ = bstack11l1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᏇ")
        if status == bstack11l1ll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᏈ"):
            bstack1111l1l1ll_opy_ = bstack11l1ll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᏉ")
        elif status == bstack11l1ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭Ꮚ"):
            bstack1111l1l1ll_opy_ = bstack11l1ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᏋ")
        bstack1111l1l1l1_opy_(bstack1111l1l1ll_opy_)
    except:
        pass
def bstack1111ll1l11_opy_(item=None, report=None, summary=None, extra=None):
    return