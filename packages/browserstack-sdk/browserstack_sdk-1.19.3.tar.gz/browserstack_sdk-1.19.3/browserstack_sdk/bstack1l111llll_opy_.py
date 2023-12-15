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
import logging
logger = logging.getLogger(__name__)
class bstack1l1l111l11_opy_:
    def bstack1l1l111lll_opy_():
        bstack1llllll1ll_opy_ = {}
        bstack1l1l111l1l_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬ೬"), bstack1ll1l11_opy_ (u"ࠬ࠭೭"))
        if not bstack1l1l111l1l_opy_:
            return bstack1llllll1ll_opy_
        try:
            bstack1l1l111ll1_opy_ = json.loads(bstack1l1l111l1l_opy_)
            if bstack1ll1l11_opy_ (u"ࠨ࡯ࡴࠤ೮") in bstack1l1l111ll1_opy_:
                bstack1llllll1ll_opy_[bstack1ll1l11_opy_ (u"ࠢࡰࡵࠥ೯")] = bstack1l1l111ll1_opy_[bstack1ll1l11_opy_ (u"ࠣࡱࡶࠦ೰")]
            if bstack1ll1l11_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨೱ") in bstack1l1l111ll1_opy_ or bstack1ll1l11_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨೲ") in bstack1l1l111ll1_opy_:
                bstack1llllll1ll_opy_[bstack1ll1l11_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢೳ")] = bstack1l1l111ll1_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ೴"), bstack1l1l111ll1_opy_.get(bstack1ll1l11_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤ೵")))
            if bstack1ll1l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣ೶") in bstack1l1l111ll1_opy_ or bstack1ll1l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨ೷") in bstack1l1l111ll1_opy_:
                bstack1llllll1ll_opy_[bstack1ll1l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢ೸")] = bstack1l1l111ll1_opy_.get(bstack1ll1l11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦ೹"), bstack1l1l111ll1_opy_.get(bstack1ll1l11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤ೺")))
            if bstack1ll1l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ೻") in bstack1l1l111ll1_opy_ or bstack1ll1l11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢ೼") in bstack1l1l111ll1_opy_:
                bstack1llllll1ll_opy_[bstack1ll1l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣ೽")] = bstack1l1l111ll1_opy_.get(bstack1ll1l11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠥ೾"), bstack1l1l111ll1_opy_.get(bstack1ll1l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥ೿")))
            if bstack1ll1l11_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࠥഀ") in bstack1l1l111ll1_opy_ or bstack1ll1l11_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣഁ") in bstack1l1l111ll1_opy_:
                bstack1llllll1ll_opy_[bstack1ll1l11_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤം")] = bstack1l1l111ll1_opy_.get(bstack1ll1l11_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࠨഃ"), bstack1l1l111ll1_opy_.get(bstack1ll1l11_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦഄ")))
            if bstack1ll1l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥഅ") in bstack1l1l111ll1_opy_ or bstack1ll1l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣആ") in bstack1l1l111ll1_opy_:
                bstack1llllll1ll_opy_[bstack1ll1l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤഇ")] = bstack1l1l111ll1_opy_.get(bstack1ll1l11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨഈ"), bstack1l1l111ll1_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦഉ")))
            if bstack1ll1l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤഊ") in bstack1l1l111ll1_opy_ or bstack1ll1l11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤഋ") in bstack1l1l111ll1_opy_:
                bstack1llllll1ll_opy_[bstack1ll1l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥഌ")] = bstack1l1l111ll1_opy_.get(bstack1ll1l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ഍"), bstack1l1l111ll1_opy_.get(bstack1ll1l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧഎ")))
            if bstack1ll1l11_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨഏ") in bstack1l1l111ll1_opy_:
                bstack1llllll1ll_opy_[bstack1ll1l11_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢഐ")] = bstack1l1l111ll1_opy_[bstack1ll1l11_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣ഑")]
        except Exception as error:
            logger.error(bstack1ll1l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡧࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡢࡶࡤ࠾ࠥࠨഒ") +  str(error))
        return bstack1llllll1ll_opy_