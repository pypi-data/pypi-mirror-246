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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11ll1ll1ll_opy_, bstack1ll11lll11_opy_, get_host_info, bstack11lll11lll_opy_, bstack11lll1l1l1_opy_, bstack11l11l1ll1_opy_, \
    bstack11l11ll1ll_opy_, bstack11l1l1lll1_opy_, bstack1lll1l111l_opy_, bstack11ll1111ll_opy_, bstack1l1lll11l_opy_, bstack1l11l11lll_opy_
from bstack_utils.bstack1111l11l11_opy_ import bstack1111l111ll_opy_
from bstack_utils.bstack1l11111ll1_opy_ import bstack1l11l1l1l1_opy_
bstack1llllllll1l_opy_ = [
    bstack11l1ll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᑀ"), bstack11l1ll_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩᑁ"), bstack11l1ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᑂ"), bstack11l1ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᑃ"),
    bstack11l1ll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᑄ"), bstack11l1ll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᑅ"), bstack11l1ll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᑆ")
]
bstack1llllll1111_opy_ = bstack11l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫᑇ")
logger = logging.getLogger(__name__)
class bstack1l11l1111_opy_:
    bstack1111l11l11_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l11l11lll_opy_(class_method=True)
    def launch(cls, bs_config, bstack1llllll11l1_opy_):
        cls.bs_config = bs_config
        if not cls.bstack1llllll1ll1_opy_():
            return
        cls.bstack1lllll1llll_opy_()
        bstack11ll1lll1l_opy_ = bstack11lll11lll_opy_(bs_config)
        bstack11lll11l1l_opy_ = bstack11lll1l1l1_opy_(bs_config)
        data = {
            bstack11l1ll_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬᑈ"): bstack11l1ll_opy_ (u"࠭ࡪࡴࡱࡱࠫᑉ"),
            bstack11l1ll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭ᑊ"): bs_config.get(bstack11l1ll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᑋ"), bstack11l1ll_opy_ (u"ࠩࠪᑌ")),
            bstack11l1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨᑍ"): bs_config.get(bstack11l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᑎ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack11l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᑏ"): bs_config.get(bstack11l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᑐ")),
            bstack11l1ll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᑑ"): bs_config.get(bstack11l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᑒ"), bstack11l1ll_opy_ (u"ࠩࠪᑓ")),
            bstack11l1ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡡࡷ࡭ࡲ࡫ࠧᑔ"): datetime.datetime.now().isoformat(),
            bstack11l1ll_opy_ (u"ࠫࡹࡧࡧࡴࠩᑕ"): bstack11l11l1ll1_opy_(bs_config),
            bstack11l1ll_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨᑖ"): get_host_info(),
            bstack11l1ll_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧᑗ"): bstack1ll11lll11_opy_(),
            bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᑘ"): os.environ.get(bstack11l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧᑙ")),
            bstack11l1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴࠧᑚ"): os.environ.get(bstack11l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨᑛ"), False),
            bstack11l1ll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭ᑜ"): bstack11ll1ll1ll_opy_(),
            bstack11l1ll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᑝ"): {
                bstack11l1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ᑞ"): bstack1llllll11l1_opy_.get(bstack11l1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨᑟ"), bstack11l1ll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨᑠ")),
                bstack11l1ll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᑡ"): bstack1llllll11l1_opy_.get(bstack11l1ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᑢ")),
                bstack11l1ll_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᑣ"): bstack1llllll11l1_opy_.get(bstack11l1ll_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪᑤ"))
            }
        }
        config = {
            bstack11l1ll_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᑥ"): (bstack11ll1lll1l_opy_, bstack11lll11l1l_opy_),
            bstack11l1ll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᑦ"): cls.default_headers()
        }
        response = bstack1lll1l111l_opy_(bstack11l1ll_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᑧ"), cls.request_url(bstack11l1ll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴࠩᑨ")), data, config)
        if response.status_code != 200:
            os.environ[bstack11l1ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩᑩ")] = bstack11l1ll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᑪ")
            os.environ[bstack11l1ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᑫ")] = bstack11l1ll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᑬ")
            os.environ[bstack11l1ll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᑭ")] = bstack11l1ll_opy_ (u"ࠣࡰࡸࡰࡱࠨᑮ")
            os.environ[bstack11l1ll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪᑯ")] = bstack11l1ll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᑰ")
            bstack1llllll1l11_opy_ = response.json()
            if bstack1llllll1l11_opy_ and bstack1llllll1l11_opy_[bstack11l1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᑱ")]:
                error_message = bstack1llllll1l11_opy_[bstack11l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᑲ")]
                if bstack1llllll1l11_opy_[bstack11l1ll_opy_ (u"࠭ࡥࡳࡴࡲࡶ࡙ࡿࡰࡦࠩᑳ")] == bstack11l1ll_opy_ (u"ࠧࡆࡔࡕࡓࡗࡥࡉࡏࡘࡄࡐࡎࡊ࡟ࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࠬᑴ"):
                    logger.error(error_message)
                elif bstack1llllll1l11_opy_[bstack11l1ll_opy_ (u"ࠨࡧࡵࡶࡴࡸࡔࡺࡲࡨࠫᑵ")] == bstack11l1ll_opy_ (u"ࠩࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠨᑶ"):
                    logger.info(error_message)
                elif bstack1llllll1l11_opy_[bstack11l1ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡖࡼࡴࡪ࠭ᑷ")] == bstack11l1ll_opy_ (u"ࠫࡊࡘࡒࡐࡔࡢࡗࡉࡑ࡟ࡅࡇࡓࡖࡊࡉࡁࡕࡇࡇࠫᑸ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11l1ll_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡚ࠥࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡪࡦ࡯࡬ࡦࡦࠣࡨࡺ࡫ࠠࡵࡱࠣࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢᑹ"))
            return [None, None, None]
        logger.debug(bstack11l1ll_opy_ (u"࠭ࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪᑺ"))
        os.environ[bstack11l1ll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭ᑻ")] = bstack11l1ll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᑼ")
        bstack1llllll1l11_opy_ = response.json()
        if bstack1llllll1l11_opy_.get(bstack11l1ll_opy_ (u"ࠩ࡭ࡻࡹ࠭ᑽ")):
            os.environ[bstack11l1ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᑾ")] = bstack1llllll1l11_opy_[bstack11l1ll_opy_ (u"ࠫ࡯ࡽࡴࠨᑿ")]
            os.environ[bstack11l1ll_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩᒀ")] = json.dumps({
                bstack11l1ll_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨᒁ"): bstack11ll1lll1l_opy_,
                bstack11l1ll_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥࠩᒂ"): bstack11lll11l1l_opy_
            })
        if bstack1llllll1l11_opy_.get(bstack11l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᒃ")):
            os.environ[bstack11l1ll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᒄ")] = bstack1llllll1l11_opy_[bstack11l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᒅ")]
        if bstack1llllll1l11_opy_.get(bstack11l1ll_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᒆ")):
            os.environ[bstack11l1ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ᒇ")] = str(bstack1llllll1l11_opy_[bstack11l1ll_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᒈ")])
        return [bstack1llllll1l11_opy_[bstack11l1ll_opy_ (u"ࠧ࡫ࡹࡷࠫᒉ")], bstack1llllll1l11_opy_[bstack11l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᒊ")], bstack1llllll1l11_opy_[bstack11l1ll_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᒋ")]]
    @classmethod
    @bstack1l11l11lll_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack11l1ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᒌ")] == bstack11l1ll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᒍ") or os.environ[bstack11l1ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᒎ")] == bstack11l1ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᒏ"):
            print(bstack11l1ll_opy_ (u"ࠧࡆ࡚ࡆࡉࡕ࡚ࡉࡐࡐࠣࡍࡓࠦࡳࡵࡱࡳࡆࡺ࡯࡬ࡥࡗࡳࡷࡹࡸࡥࡢ࡯ࠣࡖࡊࡗࡕࡆࡕࡗࠤ࡙ࡕࠠࡕࡇࡖࡘࠥࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࠥࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨᒐ"))
            return {
                bstack11l1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᒑ"): bstack11l1ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᒒ"),
                bstack11l1ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᒓ"): bstack11l1ll_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩᒔ")
            }
        else:
            cls.bstack1111l11l11_opy_.shutdown()
            data = {
                bstack11l1ll_opy_ (u"ࠬࡹࡴࡰࡲࡢࡸ࡮ࡳࡥࠨᒕ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack11l1ll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᒖ"): cls.default_headers()
            }
            bstack11l1ll1ll1_opy_ = bstack11l1ll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡹࡵࡰࠨᒗ").format(os.environ[bstack11l1ll_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠢᒘ")])
            bstack1llllll11ll_opy_ = cls.request_url(bstack11l1ll1ll1_opy_)
            response = bstack1lll1l111l_opy_(bstack11l1ll_opy_ (u"ࠩࡓ࡙࡙࠭ᒙ"), bstack1llllll11ll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11l1ll_opy_ (u"ࠥࡗࡹࡵࡰࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡱࡳࡹࠦ࡯࡬ࠤᒚ"))
    @classmethod
    def bstack1l111111l1_opy_(cls):
        if cls.bstack1111l11l11_opy_ is None:
            return
        cls.bstack1111l11l11_opy_.shutdown()
    @classmethod
    def bstack11ll1llll_opy_(cls):
        if cls.on():
            print(
                bstack11l1ll_opy_ (u"࡛ࠫ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠧᒛ").format(os.environ[bstack11l1ll_opy_ (u"ࠧࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠦᒜ")]))
    @classmethod
    def bstack1lllll1llll_opy_(cls):
        if cls.bstack1111l11l11_opy_ is not None:
            return
        cls.bstack1111l11l11_opy_ = bstack1111l111ll_opy_(cls.bstack1111111111_opy_)
        cls.bstack1111l11l11_opy_.start()
    @classmethod
    def bstack1l11l1l11l_opy_(cls, bstack1l1111l1l1_opy_, bstack1llllll1l1l_opy_=bstack11l1ll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬᒝ")):
        if not cls.on():
            return
        bstack111l1l1l_opy_ = bstack1l1111l1l1_opy_[bstack11l1ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᒞ")]
        bstack1lllllll1l1_opy_ = {
            bstack11l1ll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᒟ"): bstack11l1ll_opy_ (u"ࠩࡗࡩࡸࡺ࡟ࡔࡶࡤࡶࡹࡥࡕࡱ࡮ࡲࡥࡩ࠭ᒠ"),
            bstack11l1ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᒡ"): bstack11l1ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡡࡈࡲࡩࡥࡕࡱ࡮ࡲࡥࡩ࠭ᒢ"),
            bstack11l1ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᒣ"): bstack11l1ll_opy_ (u"࠭ࡔࡦࡵࡷࡣࡘࡱࡩࡱࡲࡨࡨࡤ࡛ࡰ࡭ࡱࡤࡨࠬᒤ"),
            bstack11l1ll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᒥ"): bstack11l1ll_opy_ (u"ࠨࡎࡲ࡫ࡤ࡛ࡰ࡭ࡱࡤࡨࠬᒦ"),
            bstack11l1ll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᒧ"): bstack11l1ll_opy_ (u"ࠪࡌࡴࡵ࡫ࡠࡕࡷࡥࡷࡺ࡟ࡖࡲ࡯ࡳࡦࡪࠧᒨ"),
            bstack11l1ll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᒩ"): bstack11l1ll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡢࡉࡳࡪ࡟ࡖࡲ࡯ࡳࡦࡪࠧᒪ"),
            bstack11l1ll_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪᒫ"): bstack11l1ll_opy_ (u"ࠧࡄࡄࡗࡣ࡚ࡶ࡬ࡰࡣࡧࠫᒬ")
        }.get(bstack111l1l1l_opy_)
        if bstack1llllll1l1l_opy_ == bstack11l1ll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧᒭ"):
            cls.bstack1lllll1llll_opy_()
            cls.bstack1111l11l11_opy_.add(bstack1l1111l1l1_opy_)
        elif bstack1llllll1l1l_opy_ == bstack11l1ll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᒮ"):
            cls.bstack1111111111_opy_([bstack1l1111l1l1_opy_], bstack1llllll1l1l_opy_)
    @classmethod
    @bstack1l11l11lll_opy_(class_method=True)
    def bstack1111111111_opy_(cls, bstack1l1111l1l1_opy_, bstack1llllll1l1l_opy_=bstack11l1ll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩᒯ")):
        config = {
            bstack11l1ll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᒰ"): cls.default_headers()
        }
        response = bstack1lll1l111l_opy_(bstack11l1ll_opy_ (u"ࠬࡖࡏࡔࡖࠪᒱ"), cls.request_url(bstack1llllll1l1l_opy_), bstack1l1111l1l1_opy_, config)
        bstack11lll1l1ll_opy_ = response.json()
    @classmethod
    @bstack1l11l11lll_opy_(class_method=True)
    def bstack1l11ll11l1_opy_(cls, bstack1l11l1l111_opy_):
        bstack1lllllll1ll_opy_ = []
        for log in bstack1l11l1l111_opy_:
            bstack1llllllll11_opy_ = {
                bstack11l1ll_opy_ (u"࠭࡫ࡪࡰࡧࠫᒲ"): bstack11l1ll_opy_ (u"ࠧࡕࡇࡖࡘࡤࡒࡏࡈࠩᒳ"),
                bstack11l1ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᒴ"): log[bstack11l1ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᒵ")],
                bstack11l1ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᒶ"): log[bstack11l1ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᒷ")],
                bstack11l1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡢࡶࡪࡹࡰࡰࡰࡶࡩࠬᒸ"): {},
                bstack11l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᒹ"): log[bstack11l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᒺ")],
            }
            if bstack11l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᒻ") in log:
                bstack1llllllll11_opy_[bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᒼ")] = log[bstack11l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᒽ")]
            elif bstack11l1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᒾ") in log:
                bstack1llllllll11_opy_[bstack11l1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᒿ")] = log[bstack11l1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᓀ")]
            bstack1lllllll1ll_opy_.append(bstack1llllllll11_opy_)
        cls.bstack1l11l1l11l_opy_({
            bstack11l1ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᓁ"): bstack11l1ll_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᓂ"),
            bstack11l1ll_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧᓃ"): bstack1lllllll1ll_opy_
        })
    @classmethod
    @bstack1l11l11lll_opy_(class_method=True)
    def bstack1lllllllll1_opy_(cls, steps):
        bstack1lllll1ll1l_opy_ = []
        for step in steps:
            bstack1lllllll111_opy_ = {
                bstack11l1ll_opy_ (u"ࠪ࡯࡮ࡴࡤࠨᓄ"): bstack11l1ll_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧᓅ"),
                bstack11l1ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᓆ"): step[bstack11l1ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᓇ")],
                bstack11l1ll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᓈ"): step[bstack11l1ll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᓉ")],
                bstack11l1ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᓊ"): step[bstack11l1ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᓋ")],
                bstack11l1ll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᓌ"): step[bstack11l1ll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᓍ")]
            }
            if bstack11l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᓎ") in step:
                bstack1lllllll111_opy_[bstack11l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᓏ")] = step[bstack11l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᓐ")]
            elif bstack11l1ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᓑ") in step:
                bstack1lllllll111_opy_[bstack11l1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᓒ")] = step[bstack11l1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᓓ")]
            bstack1lllll1ll1l_opy_.append(bstack1lllllll111_opy_)
        cls.bstack1l11l1l11l_opy_({
            bstack11l1ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᓔ"): bstack11l1ll_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᓕ"),
            bstack11l1ll_opy_ (u"ࠧ࡭ࡱࡪࡷࠬᓖ"): bstack1lllll1ll1l_opy_
        })
    @classmethod
    @bstack1l11l11lll_opy_(class_method=True)
    def bstack1l11l1l11_opy_(cls, screenshot):
        cls.bstack1l11l1l11l_opy_({
            bstack11l1ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᓗ"): bstack11l1ll_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᓘ"),
            bstack11l1ll_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᓙ"): [{
                bstack11l1ll_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᓚ"): bstack11l1ll_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠧᓛ"),
                bstack11l1ll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᓜ"): datetime.datetime.utcnow().isoformat() + bstack11l1ll_opy_ (u"࡛ࠧࠩᓝ"),
                bstack11l1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᓞ"): screenshot[bstack11l1ll_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨᓟ")],
                bstack11l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᓠ"): screenshot[bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᓡ")]
            }]
        }, bstack1llllll1l1l_opy_=bstack11l1ll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᓢ"))
    @classmethod
    @bstack1l11l11lll_opy_(class_method=True)
    def bstack1lll1111l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l11l1l11l_opy_({
            bstack11l1ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᓣ"): bstack11l1ll_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫᓤ"),
            bstack11l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᓥ"): {
                bstack11l1ll_opy_ (u"ࠤࡸࡹ࡮ࡪࠢᓦ"): cls.current_test_uuid(),
                bstack11l1ll_opy_ (u"ࠥ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠤᓧ"): cls.bstack1l1111l111_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack11l1ll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᓨ"), None) is None or os.environ[bstack11l1ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᓩ")] == bstack11l1ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᓪ"):
            return False
        return True
    @classmethod
    def bstack1llllll1ll1_opy_(cls):
        return bstack1l1lll11l_opy_(cls.bs_config.get(bstack11l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᓫ"), False))
    @staticmethod
    def request_url(url):
        return bstack11l1ll_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧᓬ").format(bstack1llllll1111_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack11l1ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᓭ"): bstack11l1ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᓮ"),
            bstack11l1ll_opy_ (u"ࠫ࡝࠳ࡂࡔࡖࡄࡇࡐ࠳ࡔࡆࡕࡗࡓࡕ࡙ࠧᓯ"): bstack11l1ll_opy_ (u"ࠬࡺࡲࡶࡧࠪᓰ")
        }
        if os.environ.get(bstack11l1ll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᓱ"), None):
            headers[bstack11l1ll_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧᓲ")] = bstack11l1ll_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫᓳ").format(os.environ[bstack11l1ll_opy_ (u"ࠤࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠥᓴ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11l1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᓵ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᓶ"), None)
    @staticmethod
    def bstack1l111lll1l_opy_():
        if getattr(threading.current_thread(), bstack11l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᓷ"), None):
            return {
                bstack11l1ll_opy_ (u"࠭ࡴࡺࡲࡨࠫᓸ"): bstack11l1ll_opy_ (u"ࠧࡵࡧࡶࡸࠬᓹ"),
                bstack11l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᓺ"): getattr(threading.current_thread(), bstack11l1ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᓻ"), None)
            }
        if getattr(threading.current_thread(), bstack11l1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᓼ"), None):
            return {
                bstack11l1ll_opy_ (u"ࠫࡹࡿࡰࡦࠩᓽ"): bstack11l1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᓾ"),
                bstack11l1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᓿ"): getattr(threading.current_thread(), bstack11l1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᔀ"), None)
            }
        return None
    @staticmethod
    def bstack1l1111l111_opy_(driver):
        return {
            bstack11l1l1lll1_opy_(): bstack11l11ll1ll_opy_(driver)
        }
    @staticmethod
    def bstack1lllllll11l_opy_(exception_info, report):
        return [{bstack11l1ll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᔁ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11llll1111_opy_(typename):
        if bstack11l1ll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᔂ") in typename:
            return bstack11l1ll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᔃ")
        return bstack11l1ll_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᔄ")
    @staticmethod
    def bstack1llllll1lll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l11l1111_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l11111l11_opy_(test, hook_name=None):
        bstack1lllll1lll1_opy_ = test.parent
        if hook_name in [bstack11l1ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪᔅ"), bstack11l1ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧᔆ"), bstack11l1ll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᔇ"), bstack11l1ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᔈ")]:
            bstack1lllll1lll1_opy_ = test
        scope = []
        while bstack1lllll1lll1_opy_ is not None:
            scope.append(bstack1lllll1lll1_opy_.name)
            bstack1lllll1lll1_opy_ = bstack1lllll1lll1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1llllllllll_opy_(hook_type):
        if hook_type == bstack11l1ll_opy_ (u"ࠤࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠢᔉ"):
            return bstack11l1ll_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢ࡫ࡳࡴࡱࠢᔊ")
        elif hook_type == bstack11l1ll_opy_ (u"ࠦࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠣᔋ"):
            return bstack11l1ll_opy_ (u"࡚ࠧࡥࡢࡴࡧࡳࡼࡴࠠࡩࡱࡲ࡯ࠧᔌ")
    @staticmethod
    def bstack1llllll111l_opy_(bstack11111llll_opy_):
        try:
            if not bstack1l11l1111_opy_.on():
                return bstack11111llll_opy_
            if os.environ.get(bstack11l1ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠦᔍ"), None) == bstack11l1ll_opy_ (u"ࠢࡵࡴࡸࡩࠧᔎ"):
                tests = os.environ.get(bstack11l1ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠧᔏ"), None)
                if tests is None or tests == bstack11l1ll_opy_ (u"ࠤࡱࡹࡱࡲࠢᔐ"):
                    return bstack11111llll_opy_
                bstack11111llll_opy_ = tests.split(bstack11l1ll_opy_ (u"ࠪ࠰ࠬᔑ"))
                return bstack11111llll_opy_
        except Exception as exc:
            print(bstack11l1ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡪࡸࡵ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴ࠽ࠤࠧᔒ"), str(exc))
        return bstack11111llll_opy_
    @classmethod
    def bstack1l111l111l_opy_(cls, event: str, bstack1l1111l1l1_opy_: bstack1l11l1l1l1_opy_):
        bstack1l11l1lll1_opy_ = {
            bstack11l1ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᔓ"): event,
            bstack1l1111l1l1_opy_.bstack1l1111l1ll_opy_(): bstack1l1111l1l1_opy_.bstack1l1111llll_opy_(event)
        }
        bstack1l11l1111_opy_.bstack1l11l1l11l_opy_(bstack1l11l1lll1_opy_)