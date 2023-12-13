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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11ll1ll1ll_opy_, bstack11l11llll_opy_, get_host_info, bstack11lll111ll_opy_, bstack11lll111l1_opy_, bstack11l11llll1_opy_, \
    bstack11l11ll1ll_opy_, bstack11l1ll1111_opy_, bstack111l111l_opy_, bstack11l1l111ll_opy_, bstack1ll1l11l_opy_, bstack1l11lll1l1_opy_
from bstack_utils.bstack1111l111l1_opy_ import bstack11111llll1_opy_
from bstack_utils.bstack1l111ll11l_opy_ import bstack1l1l11111l_opy_
bstack1llllll111l_opy_ = [
    bstack1lllll1_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᑀ"), bstack1lllll1_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩᑁ"), bstack1lllll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᑂ"), bstack1lllll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᑃ"),
    bstack1lllll1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᑄ"), bstack1lllll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᑅ"), bstack1lllll1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᑆ")
]
bstack1llllll1l1l_opy_ = bstack1lllll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫᑇ")
logger = logging.getLogger(__name__)
class bstack1ll1l111l_opy_:
    bstack1111l111l1_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l11lll1l1_opy_(class_method=True)
    def launch(cls, bs_config, bstack1lllllll111_opy_):
        cls.bs_config = bs_config
        if not cls.bstack1lllllll1ll_opy_():
            return
        cls.bstack1111111111_opy_()
        bstack11ll1ll11l_opy_ = bstack11lll111ll_opy_(bs_config)
        bstack11ll1ll1l1_opy_ = bstack11lll111l1_opy_(bs_config)
        data = {
            bstack1lllll1_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬᑈ"): bstack1lllll1_opy_ (u"࠭ࡪࡴࡱࡱࠫᑉ"),
            bstack1lllll1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭ᑊ"): bs_config.get(bstack1lllll1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᑋ"), bstack1lllll1_opy_ (u"ࠩࠪᑌ")),
            bstack1lllll1_opy_ (u"ࠪࡲࡦࡳࡥࠨᑍ"): bs_config.get(bstack1lllll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᑎ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack1lllll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᑏ"): bs_config.get(bstack1lllll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᑐ")),
            bstack1lllll1_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᑑ"): bs_config.get(bstack1lllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᑒ"), bstack1lllll1_opy_ (u"ࠩࠪᑓ")),
            bstack1lllll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡡࡷ࡭ࡲ࡫ࠧᑔ"): datetime.datetime.now().isoformat(),
            bstack1lllll1_opy_ (u"ࠫࡹࡧࡧࡴࠩᑕ"): bstack11l11llll1_opy_(bs_config),
            bstack1lllll1_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨᑖ"): get_host_info(),
            bstack1lllll1_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧᑗ"): bstack11l11llll_opy_(),
            bstack1lllll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᑘ"): os.environ.get(bstack1lllll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧᑙ")),
            bstack1lllll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴࠧᑚ"): os.environ.get(bstack1lllll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨᑛ"), False),
            bstack1lllll1_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭ᑜ"): bstack11ll1ll1ll_opy_(),
            bstack1lllll1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᑝ"): {
                bstack1lllll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ᑞ"): bstack1lllllll111_opy_.get(bstack1lllll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨᑟ"), bstack1lllll1_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨᑠ")),
                bstack1lllll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᑡ"): bstack1lllllll111_opy_.get(bstack1lllll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᑢ")),
                bstack1lllll1_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᑣ"): bstack1lllllll111_opy_.get(bstack1lllll1_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪᑤ"))
            }
        }
        config = {
            bstack1lllll1_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᑥ"): (bstack11ll1ll11l_opy_, bstack11ll1ll1l1_opy_),
            bstack1lllll1_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᑦ"): cls.default_headers()
        }
        response = bstack111l111l_opy_(bstack1lllll1_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᑧ"), cls.request_url(bstack1lllll1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴࠩᑨ")), data, config)
        if response.status_code != 200:
            os.environ[bstack1lllll1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩᑩ")] = bstack1lllll1_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᑪ")
            os.environ[bstack1lllll1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᑫ")] = bstack1lllll1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᑬ")
            os.environ[bstack1lllll1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᑭ")] = bstack1lllll1_opy_ (u"ࠣࡰࡸࡰࡱࠨᑮ")
            os.environ[bstack1lllll1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪᑯ")] = bstack1lllll1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᑰ")
            bstack1lllllll11l_opy_ = response.json()
            if bstack1lllllll11l_opy_ and bstack1lllllll11l_opy_[bstack1lllll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᑱ")]:
                error_message = bstack1lllllll11l_opy_[bstack1lllll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᑲ")]
                if bstack1lllllll11l_opy_[bstack1lllll1_opy_ (u"࠭ࡥࡳࡴࡲࡶ࡙ࡿࡰࡦࠩᑳ")] == bstack1lllll1_opy_ (u"ࠧࡆࡔࡕࡓࡗࡥࡉࡏࡘࡄࡐࡎࡊ࡟ࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࠬᑴ"):
                    logger.error(error_message)
                elif bstack1lllllll11l_opy_[bstack1lllll1_opy_ (u"ࠨࡧࡵࡶࡴࡸࡔࡺࡲࡨࠫᑵ")] == bstack1lllll1_opy_ (u"ࠩࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠨᑶ"):
                    logger.info(error_message)
                elif bstack1lllllll11l_opy_[bstack1lllll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡖࡼࡴࡪ࠭ᑷ")] == bstack1lllll1_opy_ (u"ࠫࡊࡘࡒࡐࡔࡢࡗࡉࡑ࡟ࡅࡇࡓࡖࡊࡉࡁࡕࡇࡇࠫᑸ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1lllll1_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡚ࠥࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡪࡦ࡯࡬ࡦࡦࠣࡨࡺ࡫ࠠࡵࡱࠣࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢᑹ"))
            return [None, None, None]
        logger.debug(bstack1lllll1_opy_ (u"࠭ࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪᑺ"))
        os.environ[bstack1lllll1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭ᑻ")] = bstack1lllll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᑼ")
        bstack1lllllll11l_opy_ = response.json()
        if bstack1lllllll11l_opy_.get(bstack1lllll1_opy_ (u"ࠩ࡭ࡻࡹ࠭ᑽ")):
            os.environ[bstack1lllll1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᑾ")] = bstack1lllllll11l_opy_[bstack1lllll1_opy_ (u"ࠫ࡯ࡽࡴࠨᑿ")]
            os.environ[bstack1lllll1_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩᒀ")] = json.dumps({
                bstack1lllll1_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨᒁ"): bstack11ll1ll11l_opy_,
                bstack1lllll1_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥࠩᒂ"): bstack11ll1ll1l1_opy_
            })
        if bstack1lllllll11l_opy_.get(bstack1lllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᒃ")):
            os.environ[bstack1lllll1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᒄ")] = bstack1lllllll11l_opy_[bstack1lllll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᒅ")]
        if bstack1lllllll11l_opy_.get(bstack1lllll1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᒆ")):
            os.environ[bstack1lllll1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ᒇ")] = str(bstack1lllllll11l_opy_[bstack1lllll1_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᒈ")])
        return [bstack1lllllll11l_opy_[bstack1lllll1_opy_ (u"ࠧ࡫ࡹࡷࠫᒉ")], bstack1lllllll11l_opy_[bstack1lllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᒊ")], bstack1lllllll11l_opy_[bstack1lllll1_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᒋ")]]
    @classmethod
    @bstack1l11lll1l1_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack1lllll1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᒌ")] == bstack1lllll1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᒍ") or os.environ[bstack1lllll1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᒎ")] == bstack1lllll1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᒏ"):
            print(bstack1lllll1_opy_ (u"ࠧࡆ࡚ࡆࡉࡕ࡚ࡉࡐࡐࠣࡍࡓࠦࡳࡵࡱࡳࡆࡺ࡯࡬ࡥࡗࡳࡷࡹࡸࡥࡢ࡯ࠣࡖࡊࡗࡕࡆࡕࡗࠤ࡙ࡕࠠࡕࡇࡖࡘࠥࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࠥࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨᒐ"))
            return {
                bstack1lllll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᒑ"): bstack1lllll1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᒒ"),
                bstack1lllll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᒓ"): bstack1lllll1_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩᒔ")
            }
        else:
            cls.bstack1111l111l1_opy_.shutdown()
            data = {
                bstack1lllll1_opy_ (u"ࠬࡹࡴࡰࡲࡢࡸ࡮ࡳࡥࠨᒕ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack1lllll1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᒖ"): cls.default_headers()
            }
            bstack11l1ll1l11_opy_ = bstack1lllll1_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡹࡵࡰࠨᒗ").format(os.environ[bstack1lllll1_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠢᒘ")])
            bstack1llllll11l1_opy_ = cls.request_url(bstack11l1ll1l11_opy_)
            response = bstack111l111l_opy_(bstack1lllll1_opy_ (u"ࠩࡓ࡙࡙࠭ᒙ"), bstack1llllll11l1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1lllll1_opy_ (u"ࠥࡗࡹࡵࡰࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡱࡳࡹࠦ࡯࡬ࠤᒚ"))
    @classmethod
    def bstack1l111l11l1_opy_(cls):
        if cls.bstack1111l111l1_opy_ is None:
            return
        cls.bstack1111l111l1_opy_.shutdown()
    @classmethod
    def bstack1ll11111ll_opy_(cls):
        if cls.on():
            print(
                bstack1lllll1_opy_ (u"࡛ࠫ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠧᒛ").format(os.environ[bstack1lllll1_opy_ (u"ࠧࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠦᒜ")]))
    @classmethod
    def bstack1111111111_opy_(cls):
        if cls.bstack1111l111l1_opy_ is not None:
            return
        cls.bstack1111l111l1_opy_ = bstack11111llll1_opy_(cls.bstack1llllllll11_opy_)
        cls.bstack1111l111l1_opy_.start()
    @classmethod
    def bstack1l111l1l11_opy_(cls, bstack1l11ll1ll1_opy_, bstack111111111l_opy_=bstack1lllll1_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬᒝ")):
        if not cls.on():
            return
        bstack1ll1l1ll1_opy_ = bstack1l11ll1ll1_opy_[bstack1lllll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᒞ")]
        bstack1lllll1llll_opy_ = {
            bstack1lllll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᒟ"): bstack1lllll1_opy_ (u"ࠩࡗࡩࡸࡺ࡟ࡔࡶࡤࡶࡹࡥࡕࡱ࡮ࡲࡥࡩ࠭ᒠ"),
            bstack1lllll1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᒡ"): bstack1lllll1_opy_ (u"࡙ࠫ࡫ࡳࡵࡡࡈࡲࡩࡥࡕࡱ࡮ࡲࡥࡩ࠭ᒢ"),
            bstack1lllll1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᒣ"): bstack1lllll1_opy_ (u"࠭ࡔࡦࡵࡷࡣࡘࡱࡩࡱࡲࡨࡨࡤ࡛ࡰ࡭ࡱࡤࡨࠬᒤ"),
            bstack1lllll1_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᒥ"): bstack1lllll1_opy_ (u"ࠨࡎࡲ࡫ࡤ࡛ࡰ࡭ࡱࡤࡨࠬᒦ"),
            bstack1lllll1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᒧ"): bstack1lllll1_opy_ (u"ࠪࡌࡴࡵ࡫ࡠࡕࡷࡥࡷࡺ࡟ࡖࡲ࡯ࡳࡦࡪࠧᒨ"),
            bstack1lllll1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᒩ"): bstack1lllll1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡢࡉࡳࡪ࡟ࡖࡲ࡯ࡳࡦࡪࠧᒪ"),
            bstack1lllll1_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪᒫ"): bstack1lllll1_opy_ (u"ࠧࡄࡄࡗࡣ࡚ࡶ࡬ࡰࡣࡧࠫᒬ")
        }.get(bstack1ll1l1ll1_opy_)
        if bstack111111111l_opy_ == bstack1lllll1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧᒭ"):
            cls.bstack1111111111_opy_()
            cls.bstack1111l111l1_opy_.add(bstack1l11ll1ll1_opy_)
        elif bstack111111111l_opy_ == bstack1lllll1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᒮ"):
            cls.bstack1llllllll11_opy_([bstack1l11ll1ll1_opy_], bstack111111111l_opy_)
    @classmethod
    @bstack1l11lll1l1_opy_(class_method=True)
    def bstack1llllllll11_opy_(cls, bstack1l11ll1ll1_opy_, bstack111111111l_opy_=bstack1lllll1_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩᒯ")):
        config = {
            bstack1lllll1_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᒰ"): cls.default_headers()
        }
        response = bstack111l111l_opy_(bstack1lllll1_opy_ (u"ࠬࡖࡏࡔࡖࠪᒱ"), cls.request_url(bstack111111111l_opy_), bstack1l11ll1ll1_opy_, config)
        bstack11llll1111_opy_ = response.json()
    @classmethod
    @bstack1l11lll1l1_opy_(class_method=True)
    def bstack1l11lllll1_opy_(cls, bstack1l111l1111_opy_):
        bstack1llllll1111_opy_ = []
        for log in bstack1l111l1111_opy_:
            bstack1lllllll1l1_opy_ = {
                bstack1lllll1_opy_ (u"࠭࡫ࡪࡰࡧࠫᒲ"): bstack1lllll1_opy_ (u"ࠧࡕࡇࡖࡘࡤࡒࡏࡈࠩᒳ"),
                bstack1lllll1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᒴ"): log[bstack1lllll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᒵ")],
                bstack1lllll1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᒶ"): log[bstack1lllll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᒷ")],
                bstack1lllll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡢࡶࡪࡹࡰࡰࡰࡶࡩࠬᒸ"): {},
                bstack1lllll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᒹ"): log[bstack1lllll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᒺ")],
            }
            if bstack1lllll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᒻ") in log:
                bstack1lllllll1l1_opy_[bstack1lllll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᒼ")] = log[bstack1lllll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᒽ")]
            elif bstack1lllll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᒾ") in log:
                bstack1lllllll1l1_opy_[bstack1lllll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᒿ")] = log[bstack1lllll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᓀ")]
            bstack1llllll1111_opy_.append(bstack1lllllll1l1_opy_)
        cls.bstack1l111l1l11_opy_({
            bstack1lllll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᓁ"): bstack1lllll1_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᓂ"),
            bstack1lllll1_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧᓃ"): bstack1llllll1111_opy_
        })
    @classmethod
    @bstack1l11lll1l1_opy_(class_method=True)
    def bstack1llllll1lll_opy_(cls, steps):
        bstack1llllll1ll1_opy_ = []
        for step in steps:
            bstack1llllll11ll_opy_ = {
                bstack1lllll1_opy_ (u"ࠪ࡯࡮ࡴࡤࠨᓄ"): bstack1lllll1_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧᓅ"),
                bstack1lllll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᓆ"): step[bstack1lllll1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᓇ")],
                bstack1lllll1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᓈ"): step[bstack1lllll1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᓉ")],
                bstack1lllll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᓊ"): step[bstack1lllll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᓋ")],
                bstack1lllll1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᓌ"): step[bstack1lllll1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᓍ")]
            }
            if bstack1lllll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᓎ") in step:
                bstack1llllll11ll_opy_[bstack1lllll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᓏ")] = step[bstack1lllll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᓐ")]
            elif bstack1lllll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᓑ") in step:
                bstack1llllll11ll_opy_[bstack1lllll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᓒ")] = step[bstack1lllll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᓓ")]
            bstack1llllll1ll1_opy_.append(bstack1llllll11ll_opy_)
        cls.bstack1l111l1l11_opy_({
            bstack1lllll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᓔ"): bstack1lllll1_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᓕ"),
            bstack1lllll1_opy_ (u"ࠧ࡭ࡱࡪࡷࠬᓖ"): bstack1llllll1ll1_opy_
        })
    @classmethod
    @bstack1l11lll1l1_opy_(class_method=True)
    def bstack1l11lll1l_opy_(cls, screenshot):
        cls.bstack1l111l1l11_opy_({
            bstack1lllll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᓗ"): bstack1lllll1_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᓘ"),
            bstack1lllll1_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᓙ"): [{
                bstack1lllll1_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᓚ"): bstack1lllll1_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠧᓛ"),
                bstack1lllll1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᓜ"): datetime.datetime.utcnow().isoformat() + bstack1lllll1_opy_ (u"࡛ࠧࠩᓝ"),
                bstack1lllll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᓞ"): screenshot[bstack1lllll1_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨᓟ")],
                bstack1lllll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᓠ"): screenshot[bstack1lllll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᓡ")]
            }]
        }, bstack111111111l_opy_=bstack1lllll1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᓢ"))
    @classmethod
    @bstack1l11lll1l1_opy_(class_method=True)
    def bstack1ll1ll1111_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l111l1l11_opy_({
            bstack1lllll1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᓣ"): bstack1lllll1_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫᓤ"),
            bstack1lllll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᓥ"): {
                bstack1lllll1_opy_ (u"ࠤࡸࡹ࡮ࡪࠢᓦ"): cls.current_test_uuid(),
                bstack1lllll1_opy_ (u"ࠥ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠤᓧ"): cls.bstack1l11111l11_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack1lllll1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᓨ"), None) is None or os.environ[bstack1lllll1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᓩ")] == bstack1lllll1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᓪ"):
            return False
        return True
    @classmethod
    def bstack1lllllll1ll_opy_(cls):
        return bstack1ll1l11l_opy_(cls.bs_config.get(bstack1lllll1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᓫ"), False))
    @staticmethod
    def request_url(url):
        return bstack1lllll1_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧᓬ").format(bstack1llllll1l1l_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack1lllll1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᓭ"): bstack1lllll1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᓮ"),
            bstack1lllll1_opy_ (u"ࠫ࡝࠳ࡂࡔࡖࡄࡇࡐ࠳ࡔࡆࡕࡗࡓࡕ࡙ࠧᓯ"): bstack1lllll1_opy_ (u"ࠬࡺࡲࡶࡧࠪᓰ")
        }
        if os.environ.get(bstack1lllll1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᓱ"), None):
            headers[bstack1lllll1_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧᓲ")] = bstack1lllll1_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫᓳ").format(os.environ[bstack1lllll1_opy_ (u"ࠤࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠥᓴ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1lllll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᓵ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1lllll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᓶ"), None)
    @staticmethod
    def bstack1l11l11ll1_opy_():
        if getattr(threading.current_thread(), bstack1lllll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᓷ"), None):
            return {
                bstack1lllll1_opy_ (u"࠭ࡴࡺࡲࡨࠫᓸ"): bstack1lllll1_opy_ (u"ࠧࡵࡧࡶࡸࠬᓹ"),
                bstack1lllll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᓺ"): getattr(threading.current_thread(), bstack1lllll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᓻ"), None)
            }
        if getattr(threading.current_thread(), bstack1lllll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᓼ"), None):
            return {
                bstack1lllll1_opy_ (u"ࠫࡹࡿࡰࡦࠩᓽ"): bstack1lllll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᓾ"),
                bstack1lllll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᓿ"): getattr(threading.current_thread(), bstack1lllll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᔀ"), None)
            }
        return None
    @staticmethod
    def bstack1l11111l11_opy_(driver):
        return {
            bstack11l1ll1111_opy_(): bstack11l11ll1ll_opy_(driver)
        }
    @staticmethod
    def bstack1llllllllll_opy_(exception_info, report):
        return [{bstack1lllll1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᔁ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11llll111l_opy_(typename):
        if bstack1lllll1_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᔂ") in typename:
            return bstack1lllll1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᔃ")
        return bstack1lllll1_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᔄ")
    @staticmethod
    def bstack1lllllllll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll1l111l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l11ll1l11_opy_(test, hook_name=None):
        bstack1llllll1l11_opy_ = test.parent
        if hook_name in [bstack1lllll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪᔅ"), bstack1lllll1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧᔆ"), bstack1lllll1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᔇ"), bstack1lllll1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᔈ")]:
            bstack1llllll1l11_opy_ = test
        scope = []
        while bstack1llllll1l11_opy_ is not None:
            scope.append(bstack1llllll1l11_opy_.name)
            bstack1llllll1l11_opy_ = bstack1llllll1l11_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1llllllll1l_opy_(hook_type):
        if hook_type == bstack1lllll1_opy_ (u"ࠤࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠢᔉ"):
            return bstack1lllll1_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢ࡫ࡳࡴࡱࠢᔊ")
        elif hook_type == bstack1lllll1_opy_ (u"ࠦࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠣᔋ"):
            return bstack1lllll1_opy_ (u"࡚ࠧࡥࡢࡴࡧࡳࡼࡴࠠࡩࡱࡲ࡯ࠧᔌ")
    @staticmethod
    def bstack11111111l1_opy_(bstack1ll1111l1_opy_):
        try:
            if not bstack1ll1l111l_opy_.on():
                return bstack1ll1111l1_opy_
            if os.environ.get(bstack1lllll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠦᔍ"), None) == bstack1lllll1_opy_ (u"ࠢࡵࡴࡸࡩࠧᔎ"):
                tests = os.environ.get(bstack1lllll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠧᔏ"), None)
                if tests is None or tests == bstack1lllll1_opy_ (u"ࠤࡱࡹࡱࡲࠢᔐ"):
                    return bstack1ll1111l1_opy_
                bstack1ll1111l1_opy_ = tests.split(bstack1lllll1_opy_ (u"ࠪ࠰ࠬᔑ"))
                return bstack1ll1111l1_opy_
        except Exception as exc:
            print(bstack1lllll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡪࡸࡵ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴ࠽ࠤࠧᔒ"), str(exc))
        return bstack1ll1111l1_opy_
    @classmethod
    def bstack1l111l1ll1_opy_(cls, event: str, bstack1l11ll1ll1_opy_: bstack1l1l11111l_opy_):
        bstack1l11l1l111_opy_ = {
            bstack1lllll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᔓ"): event,
            bstack1l11ll1ll1_opy_.bstack1l111l1l1l_opy_(): bstack1l11ll1ll1_opy_.bstack1l1111ll11_opy_(event)
        }
        bstack1ll1l111l_opy_.bstack1l111l1l11_opy_(bstack1l11l1l111_opy_)