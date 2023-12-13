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
import os
import json
import requests
import logging
from urllib.parse import urlparse
from datetime import datetime
from bstack_utils.constants import bstack11lll1111l_opy_ as bstack11lll11l1l_opy_
from bstack_utils.helper import bstack1ll1ll11l1_opy_, bstack1l1ll1lll1_opy_, bstack11lll111ll_opy_, bstack11lll111l1_opy_, bstack11l11llll_opy_, get_host_info, bstack11ll1ll1ll_opy_, bstack111l111l_opy_, bstack1l11lll1l1_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l11lll1l1_opy_(class_method=False)
def _11lll1l11l_opy_(driver, bstack1l1ll1l1_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1lllll1_opy_ (u"࠭࡯ࡴࡡࡱࡥࡲ࡫ࠧ෣"): caps.get(bstack1lllll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭෤"), None),
        bstack1lllll1_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ෥"): bstack1l1ll1l1_opy_.get(bstack1lllll1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ෦"), None),
        bstack1lllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩ෧"): caps.get(bstack1lllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ෨"), None),
        bstack1lllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ෩"): caps.get(bstack1lllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ෪"), None)
    }
  except Exception as error:
    logger.debug(bstack1lllll1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫ෫") + str(error))
  return response
def bstack111l1ll11_opy_(config):
  return config.get(bstack1lllll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ෬"), False) or any([p.get(bstack1lllll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ෭"), False) == True for p in config[bstack1lllll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭෮")]])
def bstack1l11l1ll_opy_(config, bstack1llll1111_opy_):
  try:
    if not bstack1l1ll1lll1_opy_(config):
      return False
    bstack11ll1llll1_opy_ = config.get(bstack1lllll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ෯"), False)
    bstack11ll1lll11_opy_ = config[bstack1lllll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ෰")][bstack1llll1111_opy_].get(bstack1lllll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭෱"), None)
    if bstack11ll1lll11_opy_ != None:
      bstack11ll1llll1_opy_ = bstack11ll1lll11_opy_
    bstack11ll1ll111_opy_ = os.getenv(bstack1lllll1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬෲ")) is not None and len(os.getenv(bstack1lllll1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ෳ"))) > 0 and os.getenv(bstack1lllll1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ෴")) != bstack1lllll1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ෵")
    return bstack11ll1llll1_opy_ and bstack11ll1ll111_opy_
  except Exception as error:
    logger.debug(bstack1lllll1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡪࡸࡩࡧࡻ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫ෶") + str(error))
  return False
def bstack111l1llll_opy_(bstack11ll1lllll_opy_, test_tags):
  bstack11ll1lllll_opy_ = os.getenv(bstack1lllll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭෷"))
  if bstack11ll1lllll_opy_ is None:
    return True
  bstack11ll1lllll_opy_ = json.loads(bstack11ll1lllll_opy_)
  try:
    include_tags = bstack11ll1lllll_opy_[bstack1lllll1_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ෸")] if bstack1lllll1_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ෹") in bstack11ll1lllll_opy_ and isinstance(bstack11ll1lllll_opy_[bstack1lllll1_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭෺")], list) else []
    exclude_tags = bstack11ll1lllll_opy_[bstack1lllll1_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ෻")] if bstack1lllll1_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ෼") in bstack11ll1lllll_opy_ and isinstance(bstack11ll1lllll_opy_[bstack1lllll1_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ෽")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1lllll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡺࡦࡲࡩࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡤࡲࡳ࡯࡮ࡨ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠤࠧ෾") + str(error))
  return False
def bstack11l111lll_opy_(config, bstack11lll1l1ll_opy_, bstack11lll1l1l1_opy_):
  bstack11ll1ll11l_opy_ = bstack11lll111ll_opy_(config)
  bstack11ll1ll1l1_opy_ = bstack11lll111l1_opy_(config)
  if bstack11ll1ll11l_opy_ is None or bstack11ll1ll1l1_opy_ is None:
    logger.error(bstack1lllll1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧ෿"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1lllll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ฀"), bstack1lllll1_opy_ (u"ࠨࡽࢀࠫก")))
    data = {
        bstack1lllll1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧข"): config[bstack1lllll1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨฃ")],
        bstack1lllll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧค"): config.get(bstack1lllll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨฅ"), os.path.basename(os.getcwd())),
        bstack1lllll1_opy_ (u"࠭ࡳࡵࡣࡵࡸ࡙࡯࡭ࡦࠩฆ"): bstack1ll1ll11l1_opy_(),
        bstack1lllll1_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬง"): config.get(bstack1lllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫจ"), bstack1lllll1_opy_ (u"ࠩࠪฉ")),
        bstack1lllll1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪช"): {
            bstack1lllll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫซ"): bstack11lll1l1ll_opy_,
            bstack1lllll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨฌ"): bstack11lll1l1l1_opy_,
            bstack1lllll1_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪญ"): __version__
        },
        bstack1lllll1_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩฎ"): settings,
        bstack1lllll1_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡅࡲࡲࡹࡸ࡯࡭ࠩฏ"): bstack11ll1ll1ll_opy_(),
        bstack1lllll1_opy_ (u"ࠩࡦ࡭ࡎࡴࡦࡰࠩฐ"): bstack11l11llll_opy_(),
        bstack1lllll1_opy_ (u"ࠪ࡬ࡴࡹࡴࡊࡰࡩࡳࠬฑ"): get_host_info(),
        bstack1lllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ฒ"): bstack1l1ll1lll1_opy_(config)
    }
    headers = {
        bstack1lllll1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫณ"): bstack1lllll1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩด"),
    }
    config = {
        bstack1lllll1_opy_ (u"ࠧࡢࡷࡷ࡬ࠬต"): (bstack11ll1ll11l_opy_, bstack11ll1ll1l1_opy_),
        bstack1lllll1_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩถ"): headers
    }
    response = bstack111l111l_opy_(bstack1lllll1_opy_ (u"ࠩࡓࡓࡘ࡚ࠧท"), bstack11lll11l1l_opy_ + bstack1lllll1_opy_ (u"ࠪ࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹࠧธ"), data, config)
    bstack11llll1111_opy_ = response.json()
    if bstack11llll1111_opy_[bstack1lllll1_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬน")]:
      parsed = json.loads(os.getenv(bstack1lllll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭บ"), bstack1lllll1_opy_ (u"࠭ࡻࡾࠩป")))
      parsed[bstack1lllll1_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨผ")] = bstack11llll1111_opy_[bstack1lllll1_opy_ (u"ࠨࡦࡤࡸࡦ࠭ฝ")][bstack1lllll1_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪพ")]
      os.environ[bstack1lllll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫฟ")] = json.dumps(parsed)
      return bstack11llll1111_opy_[bstack1lllll1_opy_ (u"ࠫࡩࡧࡴࡢࠩภ")][bstack1lllll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠪม")], bstack11llll1111_opy_[bstack1lllll1_opy_ (u"࠭ࡤࡢࡶࡤࠫย")][bstack1lllll1_opy_ (u"ࠧࡪࡦࠪร")]
    else:
      logger.error(bstack1lllll1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠩฤ") + bstack11llll1111_opy_[bstack1lllll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪล")])
      if bstack11llll1111_opy_[bstack1lllll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫฦ")] == bstack1lllll1_opy_ (u"ࠫࡎࡴࡶࡢ࡮࡬ࡨࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡶࡡࡴࡵࡨࡨ࠳࠭ว"):
        for bstack11lll1llll_opy_ in bstack11llll1111_opy_[bstack1lllll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬศ")]:
          logger.error(bstack11lll1llll_opy_[bstack1lllll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧษ")])
      return None, None
  except Exception as error:
    logger.error(bstack1lllll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠣส") +  str(error))
    return None, None
def bstack1111ll1ll_opy_():
  if os.getenv(bstack1lllll1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ห")) is None:
    return {
        bstack1lllll1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩฬ"): bstack1lllll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩอ"),
        bstack1lllll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬฮ"): bstack1lllll1_opy_ (u"ࠬࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡨࡢࡦࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠫฯ")
    }
  data = {bstack1lllll1_opy_ (u"࠭ࡥ࡯ࡦࡗ࡭ࡲ࡫ࠧะ"): bstack1ll1ll11l1_opy_()}
  headers = {
      bstack1lllll1_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧั"): bstack1lllll1_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࠩา") + os.getenv(bstack1lllll1_opy_ (u"ࠤࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠢำ")),
      bstack1lllll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩิ"): bstack1lllll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧี")
  }
  response = bstack111l111l_opy_(bstack1lllll1_opy_ (u"ࠬࡖࡕࡕࠩึ"), bstack11lll11l1l_opy_ + bstack1lllll1_opy_ (u"࠭࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵ࠲ࡷࡹࡵࡰࠨื"), data, { bstack1lllll1_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨุ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1lllll1_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡙࡫ࡳࡵࠢࡕࡹࡳࠦ࡭ࡢࡴ࡮ࡩࡩࠦࡡࡴࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠥࡧࡴࠡࠤู") + datetime.utcnow().isoformat() + bstack1lllll1_opy_ (u"ࠩ࡝ฺࠫ"))
      return {bstack1lllll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ฻"): bstack1lllll1_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ฼"), bstack1lllll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭฽"): bstack1lllll1_opy_ (u"࠭ࠧ฾")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1lllll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡧࡴࡳࡰ࡭ࡧࡷ࡭ࡴࡴࠠࡰࡨࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮࠻ࠢࠥ฿") + str(error))
    return {
        bstack1lllll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨเ"): bstack1lllll1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨแ"),
        bstack1lllll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫโ"): str(error)
    }
def bstack111lll11l_opy_(caps, options):
  try:
    bstack11lll1lll1_opy_ = caps.get(bstack1lllll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬใ"), {}).get(bstack1lllll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩไ"), caps.get(bstack1lllll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ๅ"), bstack1lllll1_opy_ (u"ࠧࠨๆ")))
    if bstack11lll1lll1_opy_:
      logger.warn(bstack1lllll1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡆࡨࡷࡰࡺ࡯ࡱࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧ็"))
      return False
    browser = caps.get(bstack1lllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫่ࠧ"), bstack1lllll1_opy_ (u"้ࠪࠫ")).lower()
    if browser != bstack1lllll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨ๊ࠫ"):
      logger.warn(bstack1lllll1_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮๋ࠣ"))
      return False
    browser_version = caps.get(bstack1lllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ์"), caps.get(bstack1lllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩํ")))
    if browser_version and browser_version != bstack1lllll1_opy_ (u"ࠨ࡮ࡤࡸࡪࡹࡴࠨ๎") and int(browser_version.split(bstack1lllll1_opy_ (u"ࠩ࠱ࠫ๏"))[0]) <= 94:
      logger.warn(bstack1lllll1_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࡭ࡲࡦࡣࡷࡩࡷࠦࡴࡩࡣࡱࠤ࠾࠺࠮ࠣ๐"))
      return False
    if not options is None:
      bstack11ll1lll1l_opy_ = options.to_capabilities().get(bstack1lllll1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ๑"), {})
      if bstack1lllll1_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩ๒") in bstack11ll1lll1l_opy_.get(bstack1lllll1_opy_ (u"࠭ࡡࡳࡩࡶࠫ๓"), []):
        logger.warn(bstack1lllll1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤ๔"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack1lllll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡣ࡯࡭ࡩࡧࡴࡦࠢࡤ࠵࠶ࡿࠠࡴࡷࡳࡴࡴࡸࡴࠡ࠼ࠥ๕") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11lll1ll11_opy_ = config.get(bstack1lllll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ๖"), {})
    bstack11lll1ll11_opy_[bstack1lllll1_opy_ (u"ࠪࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭๗")] = os.getenv(bstack1lllll1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ๘"))
    bstack11lll1ll1l_opy_ = json.loads(os.getenv(bstack1lllll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭๙"), bstack1lllll1_opy_ (u"࠭ࡻࡾࠩ๚"))).get(bstack1lllll1_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ๛"))
    caps[bstack1lllll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ๜")] = True
    if bstack1lllll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ๝") in caps:
      caps[bstack1lllll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ๞")][bstack1lllll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ๟")] = bstack11lll1ll11_opy_
      caps[bstack1lllll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭๠")][bstack1lllll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭๡")][bstack1lllll1_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ๢")] = bstack11lll1ll1l_opy_
    else:
      caps[bstack1lllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ๣")] = bstack11lll1ll11_opy_
      caps[bstack1lllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ๤")][bstack1lllll1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ๥")] = bstack11lll1ll1l_opy_
  except Exception as error:
    logger.debug(bstack1lllll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠱ࠤࡊࡸࡲࡰࡴ࠽ࠤࠧ๦") +  str(error))
def bstack11l11lll_opy_(driver, bstack11lll1l111_opy_):
  try:
    session = driver.session_id
    if session:
      bstack11lll11111_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11lll11111_opy_ = False
      bstack11lll11111_opy_ = url.scheme in [bstack1lllll1_opy_ (u"ࠧ࡮ࡴࡵࡲࠥ๧"), bstack1lllll1_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧ๨")]
      if bstack11lll11111_opy_:
        if bstack11lll1l111_opy_:
          logger.info(bstack1lllll1_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡦࡰࡴࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭ࡧࡳࠡࡵࡷࡥࡷࡺࡥࡥ࠰ࠣࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡥࡩ࡬࡯࡮ࠡ࡯ࡲࡱࡪࡴࡴࡢࡴ࡬ࡰࡾ࠴ࠢ๩"))
          driver.execute_async_script(bstack1lllll1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡃࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࡞ࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡴࠠ࠾ࠢࠫ࠭ࠥࡃ࠾ࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡢࡦࡧࡉࡻ࡫࡮ࡵࡎ࡬ࡷࡹ࡫࡮ࡦࡴࠫࠫࡆ࠷࠱࡚ࡡࡗࡅࡕࡥࡓࡕࡃࡕࡘࡊࡊࠧ࠭ࠢࡩࡲ࠷࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡪࠦ࠽ࠡࡰࡨࡻࠥࡉࡵࡴࡶࡲࡱࡊࡼࡥ࡯ࡶࠫࠫࡆ࠷࠱࡚ࡡࡉࡓࡗࡉࡅࡠࡕࡗࡅࡗ࡚ࠧࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡥ࡫ࡶࡴࡦࡺࡣࡩࡇࡹࡩࡳࡺࠨࡦࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡷࡹࠦࡦ࡯࠴ࠣࡁࠥ࠮ࠩࠡ࠿ࡁࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡶࡪࡳ࡯ࡷࡧࡈࡺࡪࡴࡴࡍ࡫ࡶࡸࡪࡴࡥࡳࠪࠪࡅ࠶࠷࡙ࡠࡖࡄࡔࡤ࡙ࡔࡂࡔࡗࡉࡉ࠭ࠬࠡࡨࡱ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠭࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡪࡳ࠮ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ๪"))
          logger.info(bstack1lllll1_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡴࡶࡤࡶࡹ࡫ࡤ࠯ࠤ๫"))
        else:
          driver.execute_script(bstack1lllll1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡫ࠠ࠾ࠢࡱࡩࡼࠦࡃࡶࡵࡷࡳࡲࡋࡶࡦࡰࡷࠬࠬࡇ࠱࠲࡛ࡢࡊࡔࡘࡃࡆࡡࡖࡘࡔࡖࠧࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡨ࡮ࡹࡰࡢࡶࡦ࡬ࡊࡼࡥ࡯ࡶࠫࡩ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ๬"))
      return bstack11lll1l111_opy_
  except Exception as e:
    logger.error(bstack1lllll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢ๭") + str(e))
    return False
def bstack11ll1ll1l_opy_(driver, class_name, name, module_name, path, bstack1l1ll1l1_opy_):
  try:
    bstack11lll11l11_opy_ = [class_name] if not class_name is None else []
    bstack11lll11lll_opy_ = {
        bstack1lllll1_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥ๮"): True,
        bstack1lllll1_opy_ (u"ࠨࡴࡦࡵࡷࡈࡪࡺࡡࡪ࡮ࡶࠦ๯"): {
            bstack1lllll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ๰"): name,
            bstack1lllll1_opy_ (u"ࠣࡶࡨࡷࡹࡘࡵ࡯ࡋࡧࠦ๱"): os.environ.get(bstack1lllll1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡘࡊ࡙ࡔࡠࡔࡘࡒࡤࡏࡄࠨ๲")),
            bstack1lllll1_opy_ (u"ࠥࡪ࡮ࡲࡥࡑࡣࡷ࡬ࠧ๳"): str(path),
            bstack1lllll1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࡏ࡭ࡸࡺࠢ๴"): [module_name, *bstack11lll11l11_opy_, name],
        },
        bstack1lllll1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢ๵"): _11lll1l11l_opy_(driver, bstack1l1ll1l1_opy_)
    }
    driver.execute_script(bstack1lllll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤࡂࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴ࡝ࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡨࡪࡵ࠱ࡶࡪࡹࠠ࠾ࠢࡱࡹࡱࡲ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡪࠥ࠮ࡡࡳࡩࡸࡱࡪࡴࡴࡴ࡝࠳ࡡ࠳ࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠬࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡦࡪࡤࡆࡸࡨࡲࡹࡒࡩࡴࡶࡨࡲࡪࡸࠨࠨࡃ࠴࠵࡞ࡥࡔࡂࡒࡢࡘࡗࡇࡎࡔࡒࡒࡖ࡙ࡋࡒࠨ࠮ࠣࠬࡪࡼࡥ࡯ࡶࠬࠤࡂࡄࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡹࡧࡰࡕࡴࡤࡲࡸࡶ࡯ࡳࡶࡨࡶࡉࡧࡴࡢࠢࡀࠤࡪࡼࡥ࡯ࡶ࠱ࡨࡪࡺࡡࡪ࡮࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡩ࡫ࡶ࠲ࡷ࡫ࡳࠡ࠿ࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡸࡦࡶࡔࡳࡣࡱࡷࡵࡵࡲࡵࡧࡵࡈࡦࡺࡡ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡧ࡬࡭ࡤࡤࡧࡰ࠮ࡴࡩ࡫ࡶ࠲ࡷ࡫ࡳࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡽࠋࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡹࡴࠡࡧࠣࡁࠥࡴࡥࡸࠢࡆࡹࡸࡺ࡯࡮ࡇࡹࡩࡳࡺࠨࠨࡃ࠴࠵࡞ࡥࡔࡆࡕࡗࡣࡊࡔࡄࠨ࠮ࠣࡿࠥࡪࡥࡵࡣ࡬ࡰ࠿ࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴ࡝࠳ࡡࠥࢃࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡨ࡮ࡹࡰࡢࡶࡦ࡬ࡊࡼࡥ࡯ࡶࠫࡩ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡩࠤ࠭ࠧࡡࡳࡩࡸࡱࡪࡴࡴࡴ࡝࠳ࡡ࠳ࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠬࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡧ࡬࡭ࡤࡤࡧࡰ࠮ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࢁࠏࠦࠠࠡࠢࠥࠦࠧ๶"), bstack11lll11lll_opy_)
    logger.info(bstack1lllll1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠥ๷"))
  except Exception as bstack11lll11ll1_opy_:
    logger.error(bstack1lllll1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥ๸") + str(path) + bstack1lllll1_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦ๹") + str(bstack11lll11ll1_opy_))