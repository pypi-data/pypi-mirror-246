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
import os
import json
import requests
import logging
from urllib.parse import urlparse
from datetime import datetime
from bstack_utils.constants import bstack11ll1ll1l1_opy_ as bstack11llll1111_opy_
from bstack_utils.helper import bstack1l1ll1ll_opy_, bstack1ll1llll1_opy_, bstack11ll1lll11_opy_, bstack11ll1lllll_opy_, bstack1l1ll111l1_opy_, get_host_info, bstack11ll1lll1l_opy_, bstack1lll1l11l_opy_, bstack1l111l11l1_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l111l11l1_opy_(class_method=False)
def _11lll1ll1l_opy_(driver, bstack11ll11111_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1ll1l11_opy_ (u"ࠫࡴࡹ࡟࡯ࡣࡰࡩࠬ෽"): caps.get(bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫ෾"), None),
        bstack1ll1l11_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ෿"): bstack11ll11111_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ฀"), None),
        bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧก"): caps.get(bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧข"), None),
        bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬฃ"): caps.get(bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬค"), None)
    }
  except Exception as error:
    logger.debug(bstack1ll1l11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩฅ") + str(error))
  return response
def bstack1l1ll1l1l1_opy_(config):
  return config.get(bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ฆ"), False) or any([p.get(bstack1ll1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧง"), False) == True for p in config[bstack1ll1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫจ")]])
def bstack11111l1ll_opy_(config, bstack1llll1l11_opy_):
  try:
    if not bstack1ll1llll1_opy_(config):
      return False
    bstack11lll111ll_opy_ = config.get(bstack1ll1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩฉ"), False)
    bstack11lll1l1l1_opy_ = config[bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ช")][bstack1llll1l11_opy_].get(bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫซ"), None)
    if bstack11lll1l1l1_opy_ != None:
      bstack11lll111ll_opy_ = bstack11lll1l1l1_opy_
    bstack11lll11l11_opy_ = os.getenv(bstack1ll1l11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪฌ")) is not None and len(os.getenv(bstack1ll1l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫญ"))) > 0 and os.getenv(bstack1ll1l11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬฎ")) != bstack1ll1l11_opy_ (u"ࠨࡰࡸࡰࡱ࠭ฏ")
    return bstack11lll111ll_opy_ and bstack11lll11l11_opy_
  except Exception as error:
    logger.debug(bstack1ll1l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡨࡶ࡮࡬ࡹࡪࡰࡪࠤࡹ࡮ࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩฐ") + str(error))
  return False
def bstack1l111l111_opy_(bstack11lll1ll11_opy_, test_tags):
  bstack11lll1ll11_opy_ = os.getenv(bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫฑ"))
  if bstack11lll1ll11_opy_ is None:
    return True
  bstack11lll1ll11_opy_ = json.loads(bstack11lll1ll11_opy_)
  try:
    include_tags = bstack11lll1ll11_opy_[bstack1ll1l11_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩฒ")] if bstack1ll1l11_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪณ") in bstack11lll1ll11_opy_ and isinstance(bstack11lll1ll11_opy_[bstack1ll1l11_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫด")], list) else []
    exclude_tags = bstack11lll1ll11_opy_[bstack1ll1l11_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬต")] if bstack1ll1l11_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ถ") in bstack11lll1ll11_opy_ and isinstance(bstack11lll1ll11_opy_[bstack1ll1l11_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧท")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1ll1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡢࡰࡱ࡭ࡳ࡭࠮ࠡࡇࡵࡶࡴࡸࠠ࠻ࠢࠥธ") + str(error))
  return False
def bstack1ll111l11_opy_(config, bstack11lll111l1_opy_, bstack11lll11lll_opy_):
  bstack11lll1l1ll_opy_ = bstack11ll1lll11_opy_(config)
  bstack11lll11ll1_opy_ = bstack11ll1lllll_opy_(config)
  if bstack11lll1l1ll_opy_ is None or bstack11lll11ll1_opy_ is None:
    logger.error(bstack1ll1l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬน"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭บ"), bstack1ll1l11_opy_ (u"࠭ࡻࡾࠩป")))
    data = {
        bstack1ll1l11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬผ"): config[bstack1ll1l11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ฝ")],
        bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬพ"): config.get(bstack1ll1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ฟ"), os.path.basename(os.getcwd())),
        bstack1ll1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡗ࡭ࡲ࡫ࠧภ"): bstack1l1ll1ll_opy_(),
        bstack1ll1l11_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪม"): config.get(bstack1ll1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩย"), bstack1ll1l11_opy_ (u"ࠧࠨร")),
        bstack1ll1l11_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨฤ"): {
            bstack1ll1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩล"): bstack11lll111l1_opy_,
            bstack1ll1l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ฦ"): bstack11lll11lll_opy_,
            bstack1ll1l11_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨว"): __version__
        },
        bstack1ll1l11_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧศ"): settings,
        bstack1ll1l11_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࡃࡰࡰࡷࡶࡴࡲࠧษ"): bstack11ll1lll1l_opy_(),
        bstack1ll1l11_opy_ (u"ࠧࡤ࡫ࡌࡲ࡫ࡵࠧส"): bstack1l1ll111l1_opy_(),
        bstack1ll1l11_opy_ (u"ࠨࡪࡲࡷࡹࡏ࡮ࡧࡱࠪห"): get_host_info(),
        bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫฬ"): bstack1ll1llll1_opy_(config)
    }
    headers = {
        bstack1ll1l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩอ"): bstack1ll1l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧฮ"),
    }
    config = {
        bstack1ll1l11_opy_ (u"ࠬࡧࡵࡵࡪࠪฯ"): (bstack11lll1l1ll_opy_, bstack11lll11ll1_opy_),
        bstack1ll1l11_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧะ"): headers
    }
    response = bstack1lll1l11l_opy_(bstack1ll1l11_opy_ (u"ࠧࡑࡑࡖࡘࠬั"), bstack11llll1111_opy_ + bstack1ll1l11_opy_ (u"ࠨ࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷࠬา"), data, config)
    bstack11lll11111_opy_ = response.json()
    if bstack11lll11111_opy_[bstack1ll1l11_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪำ")]:
      parsed = json.loads(os.getenv(bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫิ"), bstack1ll1l11_opy_ (u"ࠫࢀࢃࠧี")))
      parsed[bstack1ll1l11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ึ")] = bstack11lll11111_opy_[bstack1ll1l11_opy_ (u"࠭ࡤࡢࡶࡤࠫื")][bstack1ll1l11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨุ")]
      os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍูࠩ")] = json.dumps(parsed)
      return bstack11lll11111_opy_[bstack1ll1l11_opy_ (u"ࠩࡧࡥࡹࡧฺࠧ")][bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨ฻")], bstack11lll11111_opy_[bstack1ll1l11_opy_ (u"ࠫࡩࡧࡴࡢࠩ฼")][bstack1ll1l11_opy_ (u"ࠬ࡯ࡤࠨ฽")]
    else:
      logger.error(bstack1ll1l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠧ฾") + bstack11lll11111_opy_[bstack1ll1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ฿")])
      if bstack11lll11111_opy_[bstack1ll1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩเ")] == bstack1ll1l11_opy_ (u"ࠩࡌࡲࡻࡧ࡬ࡪࡦࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡴࡦࡹࡳࡦࡦ࠱ࠫแ"):
        for bstack11ll1llll1_opy_ in bstack11lll11111_opy_[bstack1ll1l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪโ")]:
          logger.error(bstack11ll1llll1_opy_[bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬใ")])
      return None, None
  except Exception as error:
    logger.error(bstack1ll1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࠨไ") +  str(error))
    return None, None
def bstack1l1l1lll11_opy_():
  if os.getenv(bstack1ll1l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫๅ")) is None:
    return {
        bstack1ll1l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧๆ"): bstack1ll1l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ็"),
        bstack1ll1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧ่ࠪ"): bstack1ll1l11_opy_ (u"ࠪࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤ࡭ࡧࡤࠡࡨࡤ࡭ࡱ࡫ࡤ࠯้ࠩ")
    }
  data = {bstack1ll1l11_opy_ (u"ࠫࡪࡴࡤࡕ࡫ࡰࡩ๊ࠬ"): bstack1l1ll1ll_opy_()}
  headers = {
      bstack1ll1l11_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲ๋ࠬ"): bstack1ll1l11_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࠧ์") + os.getenv(bstack1ll1l11_opy_ (u"ࠢࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠧํ")),
      bstack1ll1l11_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ๎"): bstack1ll1l11_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ๏")
  }
  response = bstack1lll1l11l_opy_(bstack1ll1l11_opy_ (u"ࠪࡔ࡚࡚ࠧ๐"), bstack11llll1111_opy_ + bstack1ll1l11_opy_ (u"ࠫ࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳ࠰ࡵࡷࡳࡵ࠭๑"), data, { bstack1ll1l11_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭๒"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1ll1l11_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱࠤࡲࡧࡲ࡬ࡧࡧࠤࡦࡹࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡥࡹࠦࠢ๓") + datetime.utcnow().isoformat() + bstack1ll1l11_opy_ (u"࡛ࠧࠩ๔"))
      return {bstack1ll1l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ๕"): bstack1ll1l11_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ๖"), bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ๗"): bstack1ll1l11_opy_ (u"ࠫࠬ๘")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1ll1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡥࡲࡱࡵࡲࡥࡵ࡫ࡲࡲࠥࡵࡦࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡙࡫ࡳࡵࠢࡕࡹࡳࡀࠠࠣ๙") + str(error))
    return {
        bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭๚"): bstack1ll1l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭๛"),
        bstack1ll1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ๜"): str(error)
    }
def bstack1lllll11ll_opy_(caps, options):
  try:
    bstack11lll1lll1_opy_ = caps.get(bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ๝"), {}).get(bstack1ll1l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ๞"), caps.get(bstack1ll1l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ๟"), bstack1ll1l11_opy_ (u"ࠬ࠭๠")))
    if bstack11lll1lll1_opy_:
      logger.warn(bstack1ll1l11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥ๡"))
      return False
    browser = caps.get(bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ๢"), bstack1ll1l11_opy_ (u"ࠨࠩ๣")).lower()
    if browser != bstack1ll1l11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ๤"):
      logger.warn(bstack1ll1l11_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨ๥"))
      return False
    browser_version = caps.get(bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ๦"), caps.get(bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ๧")))
    if browser_version and browser_version != bstack1ll1l11_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭๨") and int(browser_version.split(bstack1ll1l11_opy_ (u"ࠧ࠯ࠩ๩"))[0]) <= 94:
      logger.warn(bstack1ll1l11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢ࠼࠸࠳ࠨ๪"))
      return False
    if not options is None:
      bstack11llll111l_opy_ = options.to_capabilities().get(bstack1ll1l11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ๫"), {})
      if bstack1ll1l11_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧ๬") in bstack11llll111l_opy_.get(bstack1ll1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩ๭"), []):
        logger.warn(bstack1ll1l11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢ๮"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack1ll1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ࠣ๯") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11lll1111l_opy_ = config.get(bstack1ll1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ๰"), {})
    bstack11lll1111l_opy_[bstack1ll1l11_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫ๱")] = os.getenv(bstack1ll1l11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ๲"))
    bstack11lll1l11l_opy_ = json.loads(os.getenv(bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ๳"), bstack1ll1l11_opy_ (u"ࠫࢀࢃࠧ๴"))).get(bstack1ll1l11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭๵"))
    caps[bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭๶")] = True
    if bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ๷") in caps:
      caps[bstack1ll1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ๸")][bstack1ll1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ๹")] = bstack11lll1111l_opy_
      caps[bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ๺")][bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ๻")][bstack1ll1l11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭๼")] = bstack11lll1l11l_opy_
    else:
      caps[bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ๽")] = bstack11lll1111l_opy_
      caps[bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭๾")][bstack1ll1l11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ๿")] = bstack11lll1l11l_opy_
  except Exception as error:
    logger.debug(bstack1ll1l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡈࡶࡷࡵࡲ࠻ࠢࠥ຀") +  str(error))
def bstack1lll1l11ll_opy_(driver, bstack11ll1ll11l_opy_):
  try:
    session = driver.session_id
    if session:
      bstack11lll1llll_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11lll1llll_opy_ = False
      bstack11lll1llll_opy_ = url.scheme in [bstack1ll1l11_opy_ (u"ࠥ࡬ࡹࡺࡰࠣກ"), bstack1ll1l11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥຂ")]
      if bstack11lll1llll_opy_:
        if bstack11ll1ll11l_opy_:
          logger.info(bstack1ll1l11_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡫ࡵࡲࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡥࡸࠦࡳࡵࡣࡵࡸࡪࡪ࠮ࠡࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡣࡧࡪ࡭ࡳࠦ࡭ࡰ࡯ࡨࡲࡹࡧࡲࡪ࡮ࡼ࠲ࠧ຃"))
          driver.execute_async_script(bstack1ll1l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡹࡴࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠣࡁࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳ࡜ࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠱࡞࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡩࡲࠥࡃࠠࠩࠫࠣࡁࡃࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡧࡤࡥࡇࡹࡩࡳࡺࡌࡪࡵࡷࡩࡳ࡫ࡲࠩࠩࡄ࠵࠶࡟࡟ࡕࡃࡓࡣࡘ࡚ࡁࡓࡖࡈࡈࠬ࠲ࠠࡧࡰ࠵࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡨࠤࡂࠦ࡮ࡦࡹࠣࡇࡺࡹࡴࡰ࡯ࡈࡺࡪࡴࡴࠩࠩࡄ࠵࠶࡟࡟ࡇࡑࡕࡇࡊࡥࡓࡕࡃࡕࡘࠬ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡪࡩࡴࡲࡤࡸࡨ࡮ࡅࡷࡧࡱࡸ࠭࡫ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡴ࠲ࠡ࠿ࠣࠬ࠮ࠦ࠽࠿ࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡴࡨࡱࡴࡼࡥࡆࡸࡨࡲࡹࡒࡩࡴࡶࡨࡲࡪࡸࠨࠨࡃ࠴࠵࡞ࡥࡔࡂࡒࡢࡗ࡙ࡇࡒࡕࡇࡇࠫ࠱ࠦࡦ࡯ࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࠫ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡨࡱࠬ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨຄ"))
          logger.info(bstack1ll1l11_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥࡹࡴࡢࡴࡷࡩࡩ࠴ࠢ຅"))
        else:
          driver.execute_script(bstack1ll1l11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡩࠥࡃࠠ࡯ࡧࡺࠤࡈࡻࡳࡵࡱࡰࡉࡻ࡫࡮ࡵࠪࠪࡅ࠶࠷࡙ࡠࡈࡒࡖࡈࡋ࡟ࡔࡖࡒࡔࠬ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡦ࡬ࡷࡵࡧࡴࡤࡪࡈࡺࡪࡴࡴࠩࡧࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦຆ"))
      return bstack11ll1ll11l_opy_
  except Exception as e:
    logger.error(bstack1ll1l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࡩ࡯ࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧງ") + str(e))
    return False
def bstack1l111lll_opy_(driver, class_name, name, module_name, path, bstack11ll11111_opy_):
  try:
    bstack11ll1ll1ll_opy_ = [class_name] if not class_name is None else []
    bstack11lll11l1l_opy_ = {
        bstack1ll1l11_opy_ (u"ࠥࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠣຈ"): True,
        bstack1ll1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡆࡨࡸࡦ࡯࡬ࡴࠤຉ"): {
            bstack1ll1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥຊ"): name,
            bstack1ll1l11_opy_ (u"ࠨࡴࡦࡵࡷࡖࡺࡴࡉࡥࠤ຋"): os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡖࡈࡗ࡙ࡥࡒࡖࡐࡢࡍࡉ࠭ຌ")),
            bstack1ll1l11_opy_ (u"ࠣࡨ࡬ࡰࡪࡖࡡࡵࡪࠥຍ"): str(path),
            bstack1ll1l11_opy_ (u"ࠤࡶࡧࡴࡶࡥࡍ࡫ࡶࡸࠧຎ"): [module_name, *bstack11ll1ll1ll_opy_, name],
        },
        bstack1ll1l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧຏ"): _11lll1ll1l_opy_(driver, bstack11ll11111_opy_)
    }
    driver.execute_script(bstack1ll1l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡸࡺࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡀࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹ࡛ࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡸ࡭࡯ࡳ࠯ࡴࡨࡷࠥࡃࠠ࡯ࡷ࡯ࡰࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࡪࡨࠣࠬࡦࡸࡧࡶ࡯ࡨࡲࡹࡹ࡛࠱࡟࠱ࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠪࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡭ࡳࡪ࡯ࡸ࠰ࡤࡨࡩࡋࡶࡦࡰࡷࡐ࡮ࡹࡴࡦࡰࡨࡶ࠭࠭ࡁ࠲࠳࡜ࡣ࡙ࡇࡐࡠࡖࡕࡅࡓ࡙ࡐࡐࡔࡗࡉࡗ࠭ࠬࠡࠪࡨࡺࡪࡴࡴࠪࠢࡀࡂࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡺ࡭ࡳࡪ࡯ࡸ࠰ࡷࡥࡵ࡚ࡲࡢࡰࡶࡴࡴࡸࡴࡦࡴࡇࡥࡹࡧࠠ࠾ࠢࡨࡺࡪࡴࡴ࠯ࡦࡨࡸࡦ࡯࡬࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡮ࡩࡴ࠰ࡵࡩࡸࠦ࠽ࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡶࡤࡴ࡙ࡸࡡ࡯ࡵࡳࡳࡷࡺࡥࡳࡆࡤࡸࡦࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠬࡹ࡮ࡩࡴ࠰ࡵࡩࡸ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࢂࠐࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡷࡹࠦࡥࠡ࠿ࠣࡲࡪࡽࠠࡄࡷࡶࡸࡴࡳࡅࡷࡧࡱࡸ࠭࠭ࡁ࠲࠳࡜ࡣ࡙ࡋࡓࡕࡡࡈࡒࡉ࠭ࠬࠡࡽࠣࡨࡪࡺࡡࡪ࡮࠽ࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹ࡛࠱࡟ࠣࢁ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡦ࡬ࡷࡵࡧࡴࡤࡪࡈࡺࡪࡴࡴࠩࡧࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡩࡧࠢࠫࠥࡦࡸࡧࡶ࡯ࡨࡲࡹࡹ࡛࠱࡟࠱ࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠪࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠬ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࡿࠍࠤࠥࠦࠠࠣࠤࠥຐ"), bstack11lll11l1l_opy_)
    logger.info(bstack1ll1l11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣຑ"))
  except Exception as bstack11lll1l111_opy_:
    logger.error(bstack1ll1l11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡩࡳࡷࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣຒ") + str(path) + bstack1ll1l11_opy_ (u"ࠢࠡࡇࡵࡶࡴࡸࠠ࠻ࠤຓ") + str(bstack11lll1l111_opy_))