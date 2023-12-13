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
from uuid import uuid4
from bstack_utils.helper import bstack1ll1ll11l1_opy_, bstack11l1l1111l_opy_
from bstack_utils.bstack1ll1111l_opy_ import bstack1111l1l1l1_opy_
class bstack1l1l11111l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1l1111ll1l_opy_=None, framework=None, tags=[], scope=[], bstack1111111ll1_opy_=None, bstack111111l1ll_opy_=True, bstack111111ll11_opy_=None, bstack1ll1l1ll1_opy_=None, result=None, duration=None, bstack1l1111l1l1_opy_=None, meta={}):
        self.bstack1l1111l1l1_opy_ = bstack1l1111l1l1_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack111111l1ll_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1l1111ll1l_opy_ = bstack1l1111ll1l_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1111111ll1_opy_ = bstack1111111ll1_opy_
        self.bstack111111ll11_opy_ = bstack111111ll11_opy_
        self.bstack1ll1l1ll1_opy_ = bstack1ll1l1ll1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack1l111ll1ll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11111111ll_opy_(self):
        bstack111111l11l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1lllll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᐂ"): bstack111111l11l_opy_,
            bstack1lllll1_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᐃ"): bstack111111l11l_opy_,
            bstack1lllll1_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬᐄ"): bstack111111l11l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1lllll1_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡷࡰࡩࡳࡺ࠺ࠡࠤᐅ") + key)
            setattr(self, key, val)
    def bstack1111111lll_opy_(self):
        return {
            bstack1lllll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᐆ"): self.name,
            bstack1lllll1_opy_ (u"ࠪࡦࡴࡪࡹࠨᐇ"): {
                bstack1lllll1_opy_ (u"ࠫࡱࡧ࡮ࡨࠩᐈ"): bstack1lllll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᐉ"),
                bstack1lllll1_opy_ (u"࠭ࡣࡰࡦࡨࠫᐊ"): self.code
            },
            bstack1lllll1_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᐋ"): self.scope,
            bstack1lllll1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᐌ"): self.tags,
            bstack1lllll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᐍ"): self.framework,
            bstack1lllll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᐎ"): self.bstack1l1111ll1l_opy_
        }
    def bstack1111111l11_opy_(self):
        return {
         bstack1lllll1_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᐏ"): self.meta
        }
    def bstack111111lll1_opy_(self):
        return {
            bstack1lllll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨᐐ"): {
                bstack1lllll1_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪᐑ"): self.bstack1111111ll1_opy_
            }
        }
    def bstack111111llll_opy_(self, bstack11111l1l1l_opy_, details):
        step = next(filter(lambda st: st[bstack1lllll1_opy_ (u"ࠧࡪࡦࠪᐒ")] == bstack11111l1l1l_opy_, self.meta[bstack1lllll1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᐓ")]), None)
        step.update(details)
    def bstack11111l1l11_opy_(self, bstack11111l1l1l_opy_):
        step = next(filter(lambda st: st[bstack1lllll1_opy_ (u"ࠩ࡬ࡨࠬᐔ")] == bstack11111l1l1l_opy_, self.meta[bstack1lllll1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᐕ")]), None)
        step.update({
            bstack1lllll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᐖ"): bstack1ll1ll11l1_opy_()
        })
    def bstack1l111111l1_opy_(self, bstack11111l1l1l_opy_, result, duration=None):
        bstack111111ll11_opy_ = bstack1ll1ll11l1_opy_()
        if bstack11111l1l1l_opy_ is not None and self.meta.get(bstack1lllll1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᐗ")):
            step = next(filter(lambda st: st[bstack1lllll1_opy_ (u"࠭ࡩࡥࠩᐘ")] == bstack11111l1l1l_opy_, self.meta[bstack1lllll1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᐙ")]), None)
            step.update({
                bstack1lllll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᐚ"): bstack111111ll11_opy_,
                bstack1lllll1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᐛ"): duration if duration else bstack11l1l1111l_opy_(step[bstack1lllll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᐜ")], bstack111111ll11_opy_),
                bstack1lllll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᐝ"): result.result,
                bstack1lllll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᐞ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack111111ll1l_opy_):
        if self.meta.get(bstack1lllll1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᐟ")):
            self.meta[bstack1lllll1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᐠ")].append(bstack111111ll1l_opy_)
        else:
            self.meta[bstack1lllll1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᐡ")] = [ bstack111111ll1l_opy_ ]
    def bstack111111l111_opy_(self):
        return {
            bstack1lllll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᐢ"): self.bstack1l111ll1ll_opy_(),
            **self.bstack1111111lll_opy_(),
            **self.bstack11111111ll_opy_(),
            **self.bstack1111111l11_opy_()
        }
    def bstack11111l1111_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1lllll1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᐣ"): self.bstack111111ll11_opy_,
            bstack1lllll1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᐤ"): self.duration,
            bstack1lllll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᐥ"): self.result.result
        }
        if data[bstack1lllll1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᐦ")] == bstack1lllll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᐧ"):
            data[bstack1lllll1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᐨ")] = self.result.bstack11llll111l_opy_()
            data[bstack1lllll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᐩ")] = [{bstack1lllll1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᐪ"): self.result.bstack11l1l11ll1_opy_()}]
        return data
    def bstack11111l11l1_opy_(self):
        return {
            bstack1lllll1_opy_ (u"ࠫࡺࡻࡩࡥࠩᐫ"): self.bstack1l111ll1ll_opy_(),
            **self.bstack1111111lll_opy_(),
            **self.bstack11111111ll_opy_(),
            **self.bstack11111l1111_opy_(),
            **self.bstack1111111l11_opy_()
        }
    def bstack1l1111ll11_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1lllll1_opy_ (u"࡙ࠬࡴࡢࡴࡷࡩࡩ࠭ᐬ") in event:
            return self.bstack111111l111_opy_()
        elif bstack1lllll1_opy_ (u"࠭ࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᐭ") in event:
            return self.bstack11111l11l1_opy_()
    def bstack1l111l1l1l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack111111ll11_opy_ = time if time else bstack1ll1ll11l1_opy_()
        self.duration = duration if duration else bstack11l1l1111l_opy_(self.bstack1l1111ll1l_opy_, self.bstack111111ll11_opy_)
        if result:
            self.result = result
class bstack1l111l11ll_opy_(bstack1l1l11111l_opy_):
    def __init__(self, hooks=[], bstack1l11ll111l_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1l11ll111l_opy_ = bstack1l11ll111l_opy_
        super().__init__(*args, **kwargs, bstack1ll1l1ll1_opy_=bstack1lllll1_opy_ (u"ࠧࡵࡧࡶࡸࠬᐮ"))
    @classmethod
    def bstack11111l111l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1lllll1_opy_ (u"ࠨ࡫ࡧࠫᐯ"): id(step),
                bstack1lllll1_opy_ (u"ࠩࡷࡩࡽࡺࠧᐰ"): step.name,
                bstack1lllll1_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫᐱ"): step.keyword,
            })
        return bstack1l111l11ll_opy_(
            **kwargs,
            meta={
                bstack1lllll1_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬᐲ"): {
                    bstack1lllll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᐳ"): feature.name,
                    bstack1lllll1_opy_ (u"࠭ࡰࡢࡶ࡫ࠫᐴ"): feature.filename,
                    bstack1lllll1_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᐵ"): feature.description
                },
                bstack1lllll1_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪᐶ"): {
                    bstack1lllll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᐷ"): scenario.name
                },
                bstack1lllll1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᐸ"): steps,
                bstack1lllll1_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭ᐹ"): bstack1111l1l1l1_opy_(test)
            }
        )
    def bstack111111l1l1_opy_(self):
        return {
            bstack1lllll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᐺ"): self.hooks
        }
    def bstack1111111l1l_opy_(self):
        if self.bstack1l11ll111l_opy_:
            return {
                bstack1lllll1_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᐻ"): self.bstack1l11ll111l_opy_
            }
        return {}
    def bstack11111l11l1_opy_(self):
        return {
            **super().bstack11111l11l1_opy_(),
            **self.bstack111111l1l1_opy_()
        }
    def bstack111111l111_opy_(self):
        return {
            **super().bstack111111l111_opy_(),
            **self.bstack1111111l1l_opy_()
        }
    def bstack1l111l1l1l_opy_(self):
        return bstack1lllll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᐼ")
class bstack1l11ll1l1l_opy_(bstack1l1l11111l_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack1ll1l1ll1_opy_=bstack1lllll1_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᐽ"))
    def bstack1l11l1111l_opy_(self):
        return self.hook_type
    def bstack11111l11ll_opy_(self):
        return {
            bstack1lllll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᐾ"): self.hook_type
        }
    def bstack11111l11l1_opy_(self):
        return {
            **super().bstack11111l11l1_opy_(),
            **self.bstack11111l11ll_opy_()
        }
    def bstack111111l111_opy_(self):
        return {
            **super().bstack111111l111_opy_(),
            **self.bstack11111l11ll_opy_()
        }
    def bstack1l111l1l1l_opy_(self):
        return bstack1lllll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬᐿ")