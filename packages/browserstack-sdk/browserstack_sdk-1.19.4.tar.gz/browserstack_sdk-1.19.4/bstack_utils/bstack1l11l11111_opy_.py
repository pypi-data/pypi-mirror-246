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
from uuid import uuid4
from bstack_utils.helper import bstack1llll1ll1_opy_, bstack11l1l11lll_opy_
from bstack_utils.bstack11llll1ll_opy_ import bstack1111l1ll1l_opy_
class bstack1l11lll1ll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1l11ll1lll_opy_=None, framework=None, tags=[], scope=[], bstack11111l1l11_opy_=None, bstack11111l11ll_opy_=True, bstack11111l111l_opy_=None, bstack1lll11ll_opy_=None, result=None, duration=None, bstack1l1111l1ll_opy_=None, meta={}):
        self.bstack1l1111l1ll_opy_ = bstack1l1111l1ll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack11111l11ll_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1l11ll1lll_opy_ = bstack1l11ll1lll_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack11111l1l11_opy_ = bstack11111l1l11_opy_
        self.bstack11111l111l_opy_ = bstack11111l111l_opy_
        self.bstack1lll11ll_opy_ = bstack1lll11ll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack1l1l111l11_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1111111l1l_opy_(self):
        bstack1111111lll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1lllll1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ᐜ"): bstack1111111lll_opy_,
            bstack1lllll1l_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭ᐝ"): bstack1111111lll_opy_,
            bstack1lllll1l_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᐞ"): bstack1111111lll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1lllll1l_opy_ (u"ࠨࡕ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࠿ࠦࠢᐟ") + key)
            setattr(self, key, val)
    def bstack111111l1ll_opy_(self):
        return {
            bstack1lllll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᐠ"): self.name,
            bstack1lllll1l_opy_ (u"ࠨࡤࡲࡨࡾ࠭ᐡ"): {
                bstack1lllll1l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᐢ"): bstack1lllll1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᐣ"),
                bstack1lllll1l_opy_ (u"ࠫࡨࡵࡤࡦࠩᐤ"): self.code
            },
            bstack1lllll1l_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᐥ"): self.scope,
            bstack1lllll1l_opy_ (u"࠭ࡴࡢࡩࡶࠫᐦ"): self.tags,
            bstack1lllll1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᐧ"): self.framework,
            bstack1lllll1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᐨ"): self.bstack1l11ll1lll_opy_
        }
    def bstack111111l11l_opy_(self):
        return {
         bstack1lllll1l_opy_ (u"ࠩࡰࡩࡹࡧࠧᐩ"): self.meta
        }
    def bstack1111111ll1_opy_(self):
        return {
            bstack1lllll1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭ᐪ"): {
                bstack1lllll1l_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨᐫ"): self.bstack11111l1l11_opy_
            }
        }
    def bstack111111llll_opy_(self, bstack11111l1111_opy_, details):
        step = next(filter(lambda st: st[bstack1lllll1l_opy_ (u"ࠬ࡯ࡤࠨᐬ")] == bstack11111l1111_opy_, self.meta[bstack1lllll1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᐭ")]), None)
        step.update(details)
    def bstack11111l1lll_opy_(self, bstack11111l1111_opy_):
        step = next(filter(lambda st: st[bstack1lllll1l_opy_ (u"ࠧࡪࡦࠪᐮ")] == bstack11111l1111_opy_, self.meta[bstack1lllll1l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᐯ")]), None)
        step.update({
            bstack1lllll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᐰ"): bstack1llll1ll1_opy_()
        })
    def bstack1l11ll1l11_opy_(self, bstack11111l1111_opy_, result, duration=None):
        bstack11111l111l_opy_ = bstack1llll1ll1_opy_()
        if bstack11111l1111_opy_ is not None and self.meta.get(bstack1lllll1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᐱ")):
            step = next(filter(lambda st: st[bstack1lllll1l_opy_ (u"ࠫ࡮ࡪࠧᐲ")] == bstack11111l1111_opy_, self.meta[bstack1lllll1l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᐳ")]), None)
            step.update({
                bstack1lllll1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᐴ"): bstack11111l111l_opy_,
                bstack1lllll1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩᐵ"): duration if duration else bstack11l1l11lll_opy_(step[bstack1lllll1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᐶ")], bstack11111l111l_opy_),
                bstack1lllll1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᐷ"): result.result,
                bstack1lllll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᐸ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack111111l111_opy_):
        if self.meta.get(bstack1lllll1l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᐹ")):
            self.meta[bstack1lllll1l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᐺ")].append(bstack111111l111_opy_)
        else:
            self.meta[bstack1lllll1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᐻ")] = [ bstack111111l111_opy_ ]
    def bstack111111lll1_opy_(self):
        return {
            bstack1lllll1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᐼ"): self.bstack1l1l111l11_opy_(),
            **self.bstack111111l1ll_opy_(),
            **self.bstack1111111l1l_opy_(),
            **self.bstack111111l11l_opy_()
        }
    def bstack11111l11l1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1lllll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᐽ"): self.bstack11111l111l_opy_,
            bstack1lllll1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᐾ"): self.duration,
            bstack1lllll1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᐿ"): self.result.result
        }
        if data[bstack1lllll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᑀ")] == bstack1lllll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᑁ"):
            data[bstack1lllll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᑂ")] = self.result.bstack11llll1l1l_opy_()
            data[bstack1lllll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᑃ")] = [{bstack1lllll1l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᑄ"): self.result.bstack11l1lll1l1_opy_()}]
        return data
    def bstack111111ll11_opy_(self):
        return {
            bstack1lllll1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᑅ"): self.bstack1l1l111l11_opy_(),
            **self.bstack111111l1ll_opy_(),
            **self.bstack1111111l1l_opy_(),
            **self.bstack11111l11l1_opy_(),
            **self.bstack111111l11l_opy_()
        }
    def bstack1l111l1111_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1lllll1l_opy_ (u"ࠪࡗࡹࡧࡲࡵࡧࡧࠫᑆ") in event:
            return self.bstack111111lll1_opy_()
        elif bstack1lllll1l_opy_ (u"ࠫࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᑇ") in event:
            return self.bstack111111ll11_opy_()
    def bstack1l1111l1l1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack11111l111l_opy_ = time if time else bstack1llll1ll1_opy_()
        self.duration = duration if duration else bstack11l1l11lll_opy_(self.bstack1l11ll1lll_opy_, self.bstack11111l111l_opy_)
        if result:
            self.result = result
class bstack1l111l1l11_opy_(bstack1l11lll1ll_opy_):
    def __init__(self, hooks=[], bstack1l1l111l1l_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1l1l111l1l_opy_ = bstack1l1l111l1l_opy_
        super().__init__(*args, **kwargs, bstack1lll11ll_opy_=bstack1lllll1l_opy_ (u"ࠬࡺࡥࡴࡶࠪᑈ"))
    @classmethod
    def bstack111111l1l1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1lllll1l_opy_ (u"࠭ࡩࡥࠩᑉ"): id(step),
                bstack1lllll1l_opy_ (u"ࠧࡵࡧࡻࡸࠬᑊ"): step.name,
                bstack1lllll1l_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩᑋ"): step.keyword,
            })
        return bstack1l111l1l11_opy_(
            **kwargs,
            meta={
                bstack1lllll1l_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪᑌ"): {
                    bstack1lllll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨᑍ"): feature.name,
                    bstack1lllll1l_opy_ (u"ࠫࡵࡧࡴࡩࠩᑎ"): feature.filename,
                    bstack1lllll1l_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᑏ"): feature.description
                },
                bstack1lllll1l_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨᑐ"): {
                    bstack1lllll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᑑ"): scenario.name
                },
                bstack1lllll1l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᑒ"): steps,
                bstack1lllll1l_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫᑓ"): bstack1111l1ll1l_opy_(test)
            }
        )
    def bstack11111l1ll1_opy_(self):
        return {
            bstack1lllll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᑔ"): self.hooks
        }
    def bstack111111ll1l_opy_(self):
        if self.bstack1l1l111l1l_opy_:
            return {
                bstack1lllll1l_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪᑕ"): self.bstack1l1l111l1l_opy_
            }
        return {}
    def bstack111111ll11_opy_(self):
        return {
            **super().bstack111111ll11_opy_(),
            **self.bstack11111l1ll1_opy_()
        }
    def bstack111111lll1_opy_(self):
        return {
            **super().bstack111111lll1_opy_(),
            **self.bstack111111ll1l_opy_()
        }
    def bstack1l1111l1l1_opy_(self):
        return bstack1lllll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᑖ")
class bstack1l1111l11l_opy_(bstack1l11lll1ll_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack1lll11ll_opy_=bstack1lllll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᑗ"))
    def bstack1l1111l111_opy_(self):
        return self.hook_type
    def bstack11111l1l1l_opy_(self):
        return {
            bstack1lllll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᑘ"): self.hook_type
        }
    def bstack111111ll11_opy_(self):
        return {
            **super().bstack111111ll11_opy_(),
            **self.bstack11111l1l1l_opy_()
        }
    def bstack111111lll1_opy_(self):
        return {
            **super().bstack111111lll1_opy_(),
            **self.bstack11111l1l1l_opy_()
        }
    def bstack1l1111l1l1_opy_(self):
        return bstack1lllll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪᑙ")