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
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l11lll11_opy_ = {}
        bstack1l1l111ll1_opy_ = os.environ.get(bstack1lllll1l_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬ೬"), bstack1lllll1l_opy_ (u"ࠬ࠭೭"))
        if not bstack1l1l111ll1_opy_:
            return bstack1l11lll11_opy_
        try:
            bstack1l1l111lll_opy_ = json.loads(bstack1l1l111ll1_opy_)
            if bstack1lllll1l_opy_ (u"ࠨ࡯ࡴࠤ೮") in bstack1l1l111lll_opy_:
                bstack1l11lll11_opy_[bstack1lllll1l_opy_ (u"ࠢࡰࡵࠥ೯")] = bstack1l1l111lll_opy_[bstack1lllll1l_opy_ (u"ࠣࡱࡶࠦ೰")]
            if bstack1lllll1l_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨೱ") in bstack1l1l111lll_opy_ or bstack1lllll1l_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨೲ") in bstack1l1l111lll_opy_:
                bstack1l11lll11_opy_[bstack1lllll1l_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢೳ")] = bstack1l1l111lll_opy_.get(bstack1lllll1l_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ೴"), bstack1l1l111lll_opy_.get(bstack1lllll1l_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤ೵")))
            if bstack1lllll1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣ೶") in bstack1l1l111lll_opy_ or bstack1lllll1l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨ೷") in bstack1l1l111lll_opy_:
                bstack1l11lll11_opy_[bstack1lllll1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢ೸")] = bstack1l1l111lll_opy_.get(bstack1lllll1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦ೹"), bstack1l1l111lll_opy_.get(bstack1lllll1l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤ೺")))
            if bstack1lllll1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ೻") in bstack1l1l111lll_opy_ or bstack1lllll1l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢ೼") in bstack1l1l111lll_opy_:
                bstack1l11lll11_opy_[bstack1lllll1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣ೽")] = bstack1l1l111lll_opy_.get(bstack1lllll1l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠥ೾"), bstack1l1l111lll_opy_.get(bstack1lllll1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥ೿")))
            if bstack1lllll1l_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࠥഀ") in bstack1l1l111lll_opy_ or bstack1lllll1l_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣഁ") in bstack1l1l111lll_opy_:
                bstack1l11lll11_opy_[bstack1lllll1l_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤം")] = bstack1l1l111lll_opy_.get(bstack1lllll1l_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࠨഃ"), bstack1l1l111lll_opy_.get(bstack1lllll1l_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦഄ")))
            if bstack1lllll1l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥഅ") in bstack1l1l111lll_opy_ or bstack1lllll1l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣആ") in bstack1l1l111lll_opy_:
                bstack1l11lll11_opy_[bstack1lllll1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤഇ")] = bstack1l1l111lll_opy_.get(bstack1lllll1l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨഈ"), bstack1l1l111lll_opy_.get(bstack1lllll1l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦഉ")))
            if bstack1lllll1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤഊ") in bstack1l1l111lll_opy_ or bstack1lllll1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤഋ") in bstack1l1l111lll_opy_:
                bstack1l11lll11_opy_[bstack1lllll1l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥഌ")] = bstack1l1l111lll_opy_.get(bstack1lllll1l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ഍"), bstack1l1l111lll_opy_.get(bstack1lllll1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧഎ")))
            if bstack1lllll1l_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨഏ") in bstack1l1l111lll_opy_:
                bstack1l11lll11_opy_[bstack1lllll1l_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢഐ")] = bstack1l1l111lll_opy_[bstack1lllll1l_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣ഑")]
        except Exception as error:
            logger.error(bstack1lllll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡧࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡢࡶࡤ࠾ࠥࠨഒ") +  str(error))
        return bstack1l11lll11_opy_