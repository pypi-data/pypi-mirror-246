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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11llll111l_opy_, bstack1lll1l1l11_opy_, get_host_info, bstack11lll11l11_opy_, bstack11lll111l1_opy_, bstack11ll1111l1_opy_, \
    bstack11ll111l1l_opy_, bstack11ll111lll_opy_, bstack1lll1ll1_opy_, bstack11l1l1l11l_opy_, bstack11l1l1ll_opy_, bstack1l111l1lll_opy_
from bstack_utils.bstack1111l11l1l_opy_ import bstack1111l111l1_opy_
from bstack_utils.bstack1l11l11111_opy_ import bstack1l11lll1ll_opy_
bstack1llllll1l11_opy_ = [
    bstack1lllll1l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᑚ"), bstack1lllll1l_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧᑛ"), bstack1lllll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᑜ"), bstack1lllll1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᑝ"),
    bstack1lllll1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᑞ"), bstack1lllll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᑟ"), bstack1lllll1l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᑠ")
]
bstack1llllll1ll1_opy_ = bstack1lllll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡧࡴࡲ࡬ࡦࡥࡷࡳࡷ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᑡ")
logger = logging.getLogger(__name__)
class bstack1l1ll111ll_opy_:
    bstack1111l11l1l_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l111l1lll_opy_(class_method=True)
    def launch(cls, bs_config, bstack1llllll1lll_opy_):
        cls.bs_config = bs_config
        if not cls.bstack1lllllllll1_opy_():
            return
        cls.bstack1lllllll1ll_opy_()
        bstack11lll11111_opy_ = bstack11lll11l11_opy_(bs_config)
        bstack11lll11lll_opy_ = bstack11lll111l1_opy_(bs_config)
        data = {
            bstack1lllll1l_opy_ (u"ࠪࡪࡴࡸ࡭ࡢࡶࠪᑢ"): bstack1lllll1l_opy_ (u"ࠫ࡯ࡹ࡯࡯ࠩᑣ"),
            bstack1lllll1l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡥ࡮ࡢ࡯ࡨࠫᑤ"): bs_config.get(bstack1lllll1l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᑥ"), bstack1lllll1l_opy_ (u"ࠧࠨᑦ")),
            bstack1lllll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᑧ"): bs_config.get(bstack1lllll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᑨ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack1lllll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᑩ"): bs_config.get(bstack1lllll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᑪ")),
            bstack1lllll1l_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᑫ"): bs_config.get(bstack1lllll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᑬ"), bstack1lllll1l_opy_ (u"ࠧࠨᑭ")),
            bstack1lllll1l_opy_ (u"ࠨࡵࡷࡥࡷࡺ࡟ࡵ࡫ࡰࡩࠬᑮ"): datetime.datetime.now().isoformat(),
            bstack1lllll1l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᑯ"): bstack11ll1111l1_opy_(bs_config),
            bstack1lllll1l_opy_ (u"ࠪ࡬ࡴࡹࡴࡠ࡫ࡱࡪࡴ࠭ᑰ"): get_host_info(),
            bstack1lllll1l_opy_ (u"ࠫࡨ࡯࡟ࡪࡰࡩࡳࠬᑱ"): bstack1lll1l1l11_opy_(),
            bstack1lllll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡷࡻ࡮ࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᑲ"): os.environ.get(bstack1lllll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬᑳ")),
            bstack1lllll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡲࡦࡴࡸࡲࠬᑴ"): os.environ.get(bstack1lllll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭ᑵ"), False),
            bstack1lllll1l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡢࡧࡴࡴࡴࡳࡱ࡯ࠫᑶ"): bstack11llll111l_opy_(),
            bstack1lllll1l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡢࡺࡪࡸࡳࡪࡱࡱࠫᑷ"): {
                bstack1lllll1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫᑸ"): bstack1llllll1lll_opy_.get(bstack1lllll1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭ᑹ"), bstack1lllll1l_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ᑺ")),
                bstack1lllll1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᑻ"): bstack1llllll1lll_opy_.get(bstack1lllll1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᑼ")),
                bstack1lllll1l_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᑽ"): bstack1llllll1lll_opy_.get(bstack1lllll1l_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᑾ"))
            }
        }
        config = {
            bstack1lllll1l_opy_ (u"ࠫࡦࡻࡴࡩࠩᑿ"): (bstack11lll11111_opy_, bstack11lll11lll_opy_),
            bstack1lllll1l_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᒀ"): cls.default_headers()
        }
        response = bstack1lll1ll1_opy_(bstack1lllll1l_opy_ (u"࠭ࡐࡐࡕࡗࠫᒁ"), cls.request_url(bstack1lllll1l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹࠧᒂ")), data, config)
        if response.status_code != 200:
            os.environ[bstack1lllll1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧᒃ")] = bstack1lllll1l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᒄ")
            os.environ[bstack1lllll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᒅ")] = bstack1lllll1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᒆ")
            os.environ[bstack1lllll1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᒇ")] = bstack1lllll1l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᒈ")
            os.environ[bstack1lllll1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨᒉ")] = bstack1lllll1l_opy_ (u"ࠣࡰࡸࡰࡱࠨᒊ")
            bstack1111111l11_opy_ = response.json()
            if bstack1111111l11_opy_ and bstack1111111l11_opy_[bstack1lllll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᒋ")]:
                error_message = bstack1111111l11_opy_[bstack1lllll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᒌ")]
                if bstack1111111l11_opy_[bstack1lllll1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࡗࡽࡵ࡫ࠧᒍ")] == bstack1lllll1l_opy_ (u"ࠬࡋࡒࡓࡑࡕࡣࡎࡔࡖࡂࡎࡌࡈࡤࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࠪᒎ"):
                    logger.error(error_message)
                elif bstack1111111l11_opy_[bstack1lllll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶ࡙ࡿࡰࡦࠩᒏ")] == bstack1lllll1l_opy_ (u"ࠧࡆࡔࡕࡓࡗࡥࡁࡄࡅࡈࡗࡘࡥࡄࡆࡐࡌࡉࡉ࠭ᒐ"):
                    logger.info(error_message)
                elif bstack1111111l11_opy_[bstack1lllll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࡔࡺࡲࡨࠫᒑ")] == bstack1lllll1l_opy_ (u"ࠩࡈࡖࡗࡕࡒࡠࡕࡇࡏࡤࡊࡅࡑࡔࡈࡇࡆ࡚ࡅࡅࠩᒒ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1lllll1l_opy_ (u"ࠥࡈࡦࡺࡡࠡࡷࡳࡰࡴࡧࡤࠡࡶࡲࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡘࡪࡹࡴࠡࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡦࡸࡩࠥࡺ࡯ࠡࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧᒓ"))
            return [None, None, None]
        logger.debug(bstack1lllll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠡࠨᒔ"))
        os.environ[bstack1lllll1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡅࡒࡑࡕࡒࡅࡕࡇࡇࠫᒕ")] = bstack1lllll1l_opy_ (u"࠭ࡴࡳࡷࡨࠫᒖ")
        bstack1111111l11_opy_ = response.json()
        if bstack1111111l11_opy_.get(bstack1lllll1l_opy_ (u"ࠧ࡫ࡹࡷࠫᒗ")):
            os.environ[bstack1lllll1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᒘ")] = bstack1111111l11_opy_[bstack1lllll1l_opy_ (u"ࠩ࡭ࡻࡹ࠭ᒙ")]
            os.environ[bstack1lllll1l_opy_ (u"ࠪࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࡠࡈࡒࡖࡤࡉࡒࡂࡕࡋࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧᒚ")] = json.dumps({
                bstack1lllll1l_opy_ (u"ࠫࡺࡹࡥࡳࡰࡤࡱࡪ࠭ᒛ"): bstack11lll11111_opy_,
                bstack1lllll1l_opy_ (u"ࠬࡶࡡࡴࡵࡺࡳࡷࡪࠧᒜ"): bstack11lll11lll_opy_
            })
        if bstack1111111l11_opy_.get(bstack1lllll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᒝ")):
            os.environ[bstack1lllll1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᒞ")] = bstack1111111l11_opy_[bstack1lllll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᒟ")]
        if bstack1111111l11_opy_.get(bstack1lllll1l_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᒠ")):
            os.environ[bstack1lllll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫᒡ")] = str(bstack1111111l11_opy_[bstack1lllll1l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᒢ")])
        return [bstack1111111l11_opy_[bstack1lllll1l_opy_ (u"ࠬࡰࡷࡵࠩᒣ")], bstack1111111l11_opy_[bstack1lllll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᒤ")], bstack1111111l11_opy_[bstack1lllll1l_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᒥ")]]
    @classmethod
    @bstack1l111l1lll_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack1lllll1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᒦ")] == bstack1lllll1l_opy_ (u"ࠤࡱࡹࡱࡲࠢᒧ") or os.environ[bstack1lllll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᒨ")] == bstack1lllll1l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᒩ"):
            print(bstack1lllll1l_opy_ (u"ࠬࡋࡘࡄࡇࡓࡘࡎࡕࡎࠡࡋࡑࠤࡸࡺ࡯ࡱࡄࡸ࡭ࡱࡪࡕࡱࡵࡷࡶࡪࡧ࡭ࠡࡔࡈࡕ࡚ࡋࡓࡕࠢࡗࡓ࡚ࠥࡅࡔࡖࠣࡓࡇ࡙ࡅࡓࡘࡄࡆࡎࡒࡉࡕ࡛ࠣ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭ᒪ"))
            return {
                bstack1lllll1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᒫ"): bstack1lllll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᒬ"),
                bstack1lllll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᒭ"): bstack1lllll1l_opy_ (u"ࠩࡗࡳࡰ࡫࡮࠰ࡤࡸ࡭ࡱࡪࡉࡅࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤ࠭ࠢࡥࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡱ࡮࡭ࡨࡵࠢ࡫ࡥࡻ࡫ࠠࡧࡣ࡬ࡰࡪࡪࠧᒮ")
            }
        else:
            cls.bstack1111l11l1l_opy_.shutdown()
            data = {
                bstack1lllll1l_opy_ (u"ࠪࡷࡹࡵࡰࡠࡶ࡬ࡱࡪ࠭ᒯ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack1lllll1l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᒰ"): cls.default_headers()
            }
            bstack11ll11l111_opy_ = bstack1lllll1l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡷࡳࡵ࠭ᒱ").format(os.environ[bstack1lllll1l_opy_ (u"ࠨࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠧᒲ")])
            bstack1llllllll1l_opy_ = cls.request_url(bstack11ll11l111_opy_)
            response = bstack1lll1ll1_opy_(bstack1lllll1l_opy_ (u"ࠧࡑࡗࡗࠫᒳ"), bstack1llllllll1l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1lllll1l_opy_ (u"ࠣࡕࡷࡳࡵࠦࡲࡦࡳࡸࡩࡸࡺࠠ࡯ࡱࡷࠤࡴࡱࠢᒴ"))
    @classmethod
    def bstack1l11l11lll_opy_(cls):
        if cls.bstack1111l11l1l_opy_ is None:
            return
        cls.bstack1111l11l1l_opy_.shutdown()
    @classmethod
    def bstack1lll1111_opy_(cls):
        if cls.on():
            print(
                bstack1lllll1l_opy_ (u"࡙ࠩ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠬᒵ").format(os.environ[bstack1lllll1l_opy_ (u"ࠥࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠤᒶ")]))
    @classmethod
    def bstack1lllllll1ll_opy_(cls):
        if cls.bstack1111l11l1l_opy_ is not None:
            return
        cls.bstack1111l11l1l_opy_ = bstack1111l111l1_opy_(cls.bstack1llllllllll_opy_)
        cls.bstack1111l11l1l_opy_.start()
    @classmethod
    def bstack1l11l111l1_opy_(cls, bstack1l111llll1_opy_, bstack1111111111_opy_=bstack1lllll1l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪᒷ")):
        if not cls.on():
            return
        bstack1lll11ll_opy_ = bstack1l111llll1_opy_[bstack1lllll1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᒸ")]
        bstack1lllllll1l1_opy_ = {
            bstack1lllll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᒹ"): bstack1lllll1l_opy_ (u"ࠧࡕࡧࡶࡸࡤ࡙ࡴࡢࡴࡷࡣ࡚ࡶ࡬ࡰࡣࡧࠫᒺ"),
            bstack1lllll1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᒻ"): bstack1lllll1l_opy_ (u"ࠩࡗࡩࡸࡺ࡟ࡆࡰࡧࡣ࡚ࡶ࡬ࡰࡣࡧࠫᒼ"),
            bstack1lllll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫᒽ"): bstack1lllll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡡࡖ࡯࡮ࡶࡰࡦࡦࡢ࡙ࡵࡲ࡯ࡢࡦࠪᒾ"),
            bstack1lllll1l_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᒿ"): bstack1lllll1l_opy_ (u"࠭ࡌࡰࡩࡢ࡙ࡵࡲ࡯ࡢࡦࠪᓀ"),
            bstack1lllll1l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᓁ"): bstack1lllll1l_opy_ (u"ࠨࡊࡲࡳࡰࡥࡓࡵࡣࡵࡸࡤ࡛ࡰ࡭ࡱࡤࡨࠬᓂ"),
            bstack1lllll1l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᓃ"): bstack1lllll1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡠࡇࡱࡨࡤ࡛ࡰ࡭ࡱࡤࡨࠬᓄ"),
            bstack1lllll1l_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨᓅ"): bstack1lllll1l_opy_ (u"ࠬࡉࡂࡕࡡࡘࡴࡱࡵࡡࡥࠩᓆ")
        }.get(bstack1lll11ll_opy_)
        if bstack1111111111_opy_ == bstack1lllll1l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬᓇ"):
            cls.bstack1lllllll1ll_opy_()
            cls.bstack1111l11l1l_opy_.add(bstack1l111llll1_opy_)
        elif bstack1111111111_opy_ == bstack1lllll1l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᓈ"):
            cls.bstack1llllllllll_opy_([bstack1l111llll1_opy_], bstack1111111111_opy_)
    @classmethod
    @bstack1l111l1lll_opy_(class_method=True)
    def bstack1llllllllll_opy_(cls, bstack1l111llll1_opy_, bstack1111111111_opy_=bstack1lllll1l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧᓉ")):
        config = {
            bstack1lllll1l_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᓊ"): cls.default_headers()
        }
        response = bstack1lll1ll1_opy_(bstack1lllll1l_opy_ (u"ࠪࡔࡔ࡙ࡔࠨᓋ"), cls.request_url(bstack1111111111_opy_), bstack1l111llll1_opy_, config)
        bstack11lll11ll1_opy_ = response.json()
    @classmethod
    @bstack1l111l1lll_opy_(class_method=True)
    def bstack1l11l11ll1_opy_(cls, bstack1l11ll1l1l_opy_):
        bstack11111111l1_opy_ = []
        for log in bstack1l11ll1l1l_opy_:
            bstack11111111ll_opy_ = {
                bstack1lllll1l_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᓌ"): bstack1lllll1l_opy_ (u"࡚ࠬࡅࡔࡖࡢࡐࡔࡍࠧᓍ"),
                bstack1lllll1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᓎ"): log[bstack1lllll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᓏ")],
                bstack1lllll1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᓐ"): log[bstack1lllll1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᓑ")],
                bstack1lllll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡠࡴࡨࡷࡵࡵ࡮ࡴࡧࠪᓒ"): {},
                bstack1lllll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᓓ"): log[bstack1lllll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᓔ")],
            }
            if bstack1lllll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᓕ") in log:
                bstack11111111ll_opy_[bstack1lllll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᓖ")] = log[bstack1lllll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᓗ")]
            elif bstack1lllll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᓘ") in log:
                bstack11111111ll_opy_[bstack1lllll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᓙ")] = log[bstack1lllll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᓚ")]
            bstack11111111l1_opy_.append(bstack11111111ll_opy_)
        cls.bstack1l11l111l1_opy_({
            bstack1lllll1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᓛ"): bstack1lllll1l_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᓜ"),
            bstack1lllll1l_opy_ (u"ࠧ࡭ࡱࡪࡷࠬᓝ"): bstack11111111l1_opy_
        })
    @classmethod
    @bstack1l111l1lll_opy_(class_method=True)
    def bstack1llllll11l1_opy_(cls, steps):
        bstack1lllllll11l_opy_ = []
        for step in steps:
            bstack1llllll111l_opy_ = {
                bstack1lllll1l_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭ᓞ"): bstack1lllll1l_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡔࡖࡈࡔࠬᓟ"),
                bstack1lllll1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᓠ"): step[bstack1lllll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᓡ")],
                bstack1lllll1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᓢ"): step[bstack1lllll1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᓣ")],
                bstack1lllll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᓤ"): step[bstack1lllll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᓥ")],
                bstack1lllll1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᓦ"): step[bstack1lllll1l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᓧ")]
            }
            if bstack1lllll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᓨ") in step:
                bstack1llllll111l_opy_[bstack1lllll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᓩ")] = step[bstack1lllll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᓪ")]
            elif bstack1lllll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᓫ") in step:
                bstack1llllll111l_opy_[bstack1lllll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᓬ")] = step[bstack1lllll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᓭ")]
            bstack1lllllll11l_opy_.append(bstack1llllll111l_opy_)
        cls.bstack1l11l111l1_opy_({
            bstack1lllll1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᓮ"): bstack1lllll1l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᓯ"),
            bstack1lllll1l_opy_ (u"ࠬࡲ࡯ࡨࡵࠪᓰ"): bstack1lllllll11l_opy_
        })
    @classmethod
    @bstack1l111l1lll_opy_(class_method=True)
    def bstack1l11ll1l1_opy_(cls, screenshot):
        cls.bstack1l11l111l1_opy_({
            bstack1lllll1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᓱ"): bstack1lllll1l_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᓲ"),
            bstack1lllll1l_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭ᓳ"): [{
                bstack1lllll1l_opy_ (u"ࠩ࡮࡭ࡳࡪࠧᓴ"): bstack1lllll1l_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࠬᓵ"),
                bstack1lllll1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᓶ"): datetime.datetime.utcnow().isoformat() + bstack1lllll1l_opy_ (u"ࠬࡠࠧᓷ"),
                bstack1lllll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᓸ"): screenshot[bstack1lllll1l_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ᓹ")],
                bstack1lllll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᓺ"): screenshot[bstack1lllll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᓻ")]
            }]
        }, bstack1111111111_opy_=bstack1lllll1l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᓼ"))
    @classmethod
    @bstack1l111l1lll_opy_(class_method=True)
    def bstack1ll1llll1l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l11l111l1_opy_({
            bstack1lllll1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᓽ"): bstack1lllll1l_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩᓾ"),
            bstack1lllll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨᓿ"): {
                bstack1lllll1l_opy_ (u"ࠢࡶࡷ࡬ࡨࠧᔀ"): cls.current_test_uuid(),
                bstack1lllll1l_opy_ (u"ࠣ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠢᔁ"): cls.bstack1l1l1111l1_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack1lllll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᔂ"), None) is None or os.environ[bstack1lllll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᔃ")] == bstack1lllll1l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᔄ"):
            return False
        return True
    @classmethod
    def bstack1lllllllll1_opy_(cls):
        return bstack11l1l1ll_opy_(cls.bs_config.get(bstack1lllll1l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᔅ"), False))
    @staticmethod
    def request_url(url):
        return bstack1lllll1l_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬᔆ").format(bstack1llllll1ll1_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack1lllll1l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᔇ"): bstack1lllll1l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᔈ"),
            bstack1lllll1l_opy_ (u"࡛ࠩ࠱ࡇ࡙ࡔࡂࡅࡎ࠱࡙ࡋࡓࡕࡑࡓࡗࠬᔉ"): bstack1lllll1l_opy_ (u"ࠪࡸࡷࡻࡥࠨᔊ")
        }
        if os.environ.get(bstack1lllll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᔋ"), None):
            headers[bstack1lllll1l_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬᔌ")] = bstack1lllll1l_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩᔍ").format(os.environ[bstack1lllll1l_opy_ (u"ࠢࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠣᔎ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1lllll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᔏ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1lllll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᔐ"), None)
    @staticmethod
    def bstack1l111ll11l_opy_():
        if getattr(threading.current_thread(), bstack1lllll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᔑ"), None):
            return {
                bstack1lllll1l_opy_ (u"ࠫࡹࡿࡰࡦࠩᔒ"): bstack1lllll1l_opy_ (u"ࠬࡺࡥࡴࡶࠪᔓ"),
                bstack1lllll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᔔ"): getattr(threading.current_thread(), bstack1lllll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᔕ"), None)
            }
        if getattr(threading.current_thread(), bstack1lllll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᔖ"), None):
            return {
                bstack1lllll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᔗ"): bstack1lllll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᔘ"),
                bstack1lllll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᔙ"): getattr(threading.current_thread(), bstack1lllll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᔚ"), None)
            }
        return None
    @staticmethod
    def bstack1l1l1111l1_opy_(driver):
        return {
            bstack11ll111lll_opy_(): bstack11ll111l1l_opy_(driver)
        }
    @staticmethod
    def bstack1llllll11ll_opy_(exception_info, report):
        return [{bstack1lllll1l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᔛ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11llll1l1l_opy_(typename):
        if bstack1lllll1l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥᔜ") in typename:
            return bstack1lllll1l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤᔝ")
        return bstack1lllll1l_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥᔞ")
    @staticmethod
    def bstack111111111l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1ll111ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l11l11l11_opy_(test, hook_name=None):
        bstack1lllllll111_opy_ = test.parent
        if hook_name in [bstack1lllll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᔟ"), bstack1lllll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬᔠ"), bstack1lllll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᔡ"), bstack1lllll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨᔢ")]:
            bstack1lllllll111_opy_ = test
        scope = []
        while bstack1lllllll111_opy_ is not None:
            scope.append(bstack1lllllll111_opy_.name)
            bstack1lllllll111_opy_ = bstack1lllllll111_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1llllll1l1l_opy_(hook_type):
        if hook_type == bstack1lllll1l_opy_ (u"ࠢࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠧᔣ"):
            return bstack1lllll1l_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡩࡱࡲ࡯ࠧᔤ")
        elif hook_type == bstack1lllll1l_opy_ (u"ࠤࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍࠨᔥ"):
            return bstack1lllll1l_opy_ (u"ࠥࡘࡪࡧࡲࡥࡱࡺࡲࠥ࡮࡯ࡰ࡭ࠥᔦ")
    @staticmethod
    def bstack1llllllll11_opy_(bstack1ll1lll11_opy_):
        try:
            if not bstack1l1ll111ll_opy_.on():
                return bstack1ll1lll11_opy_
            if os.environ.get(bstack1lllll1l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠤᔧ"), None) == bstack1lllll1l_opy_ (u"ࠧࡺࡲࡶࡧࠥᔨ"):
                tests = os.environ.get(bstack1lllll1l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠥᔩ"), None)
                if tests is None or tests == bstack1lllll1l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᔪ"):
                    return bstack1ll1lll11_opy_
                bstack1ll1lll11_opy_ = tests.split(bstack1lllll1l_opy_ (u"ࠨ࠮ࠪᔫ"))
                return bstack1ll1lll11_opy_
        except Exception as exc:
            print(bstack1lllll1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡴࡨࡶࡺࡴࠠࡩࡣࡱࡨࡱ࡫ࡲ࠻ࠢࠥᔬ"), str(exc))
        return bstack1ll1lll11_opy_
    @classmethod
    def bstack1l11llllll_opy_(cls, event: str, bstack1l111llll1_opy_: bstack1l11lll1ll_opy_):
        bstack1l111l1ll1_opy_ = {
            bstack1lllll1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᔭ"): event,
            bstack1l111llll1_opy_.bstack1l1111l1l1_opy_(): bstack1l111llll1_opy_.bstack1l111l1111_opy_(event)
        }
        bstack1l1ll111ll_opy_.bstack1l11l111l1_opy_(bstack1l111l1ll1_opy_)