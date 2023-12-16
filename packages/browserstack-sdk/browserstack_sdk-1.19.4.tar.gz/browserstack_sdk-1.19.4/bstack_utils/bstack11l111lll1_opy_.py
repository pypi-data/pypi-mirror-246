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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result
def _11l11l1lll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l11l1l1l_opy_:
    def __init__(self, handler):
        self._11l111ll11_opy_ = {}
        self._11l11ll11l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._11l111ll11_opy_[bstack1lllll1l_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ዁")] = Module._inject_setup_function_fixture
        self._11l111ll11_opy_[bstack1lllll1l_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨዂ")] = Module._inject_setup_module_fixture
        self._11l111ll11_opy_[bstack1lllll1l_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨዃ")] = Class._inject_setup_class_fixture
        self._11l111ll11_opy_[bstack1lllll1l_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪዄ")] = Class._inject_setup_method_fixture
        Module._inject_setup_function_fixture = self.bstack11l11l1111_opy_(bstack1lllll1l_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ዅ"))
        Module._inject_setup_module_fixture = self.bstack11l11l1111_opy_(bstack1lllll1l_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ዆"))
        Class._inject_setup_class_fixture = self.bstack11l11l1111_opy_(bstack1lllll1l_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ዇"))
        Class._inject_setup_method_fixture = self.bstack11l11l1111_opy_(bstack1lllll1l_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧወ"))
    def bstack11l11l1ll1_opy_(self, bstack11l111ll1l_opy_, hook_type):
        meth = getattr(bstack11l111ll1l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l11ll11l_opy_[hook_type] = meth
            setattr(bstack11l111ll1l_opy_, hook_type, self.bstack11l111llll_opy_(hook_type))
    def bstack11l111l1ll_opy_(self, instance, bstack11l11l1l11_opy_):
        if bstack11l11l1l11_opy_ == bstack1lllll1l_opy_ (u"ࠢࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠥዉ"):
            self.bstack11l11l1ll1_opy_(instance.obj, bstack1lllll1l_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤዊ"))
            self.bstack11l11l1ll1_opy_(instance.obj, bstack1lllll1l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨዋ"))
        if bstack11l11l1l11_opy_ == bstack1lllll1l_opy_ (u"ࠥࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠦዌ"):
            self.bstack11l11l1ll1_opy_(instance.obj, bstack1lllll1l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠥው"))
            self.bstack11l11l1ll1_opy_(instance.obj, bstack1lllll1l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠢዎ"))
        if bstack11l11l1l11_opy_ == bstack1lllll1l_opy_ (u"ࠨࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࠨዏ"):
            self.bstack11l11l1ll1_opy_(instance.obj, bstack1lllll1l_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠧዐ"))
            self.bstack11l11l1ll1_opy_(instance.obj, bstack1lllll1l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠤዑ"))
        if bstack11l11l1l11_opy_ == bstack1lllll1l_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠥዒ"):
            self.bstack11l11l1ll1_opy_(instance.obj, bstack1lllll1l_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠤዓ"))
            self.bstack11l11l1ll1_opy_(instance.obj, bstack1lllll1l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩࠨዔ"))
    @staticmethod
    def bstack11l11l111l_opy_(hook_type, func, args):
        if hook_type in [bstack1lllll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫዕ"), bstack1lllll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨዖ")]:
            _11l11l1lll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l111llll_opy_(self, hook_type):
        def bstack11l11l11ll_opy_(arg=None):
            self.handler(hook_type, bstack1lllll1l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧ዗"))
            result = None
            exception = None
            try:
                self.bstack11l11l111l_opy_(hook_type, self._11l11ll11l_opy_[hook_type], (arg,))
                result = Result(result=bstack1lllll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨዘ"))
            except Exception as e:
                result = Result(result=bstack1lllll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩዙ"), exception=e)
                self.handler(hook_type, bstack1lllll1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩዚ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1lllll1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪዛ"), result)
        def bstack11l11ll111_opy_(this, arg=None):
            self.handler(hook_type, bstack1lllll1l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬዜ"))
            result = None
            exception = None
            try:
                self.bstack11l11l111l_opy_(hook_type, self._11l11ll11l_opy_[hook_type], (this, arg))
                result = Result(result=bstack1lllll1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ዝ"))
            except Exception as e:
                result = Result(result=bstack1lllll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧዞ"), exception=e)
                self.handler(hook_type, bstack1lllll1l_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧዟ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1lllll1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨዠ"), result)
        if hook_type in [bstack1lllll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩዡ"), bstack1lllll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ዢ")]:
            return bstack11l11ll111_opy_
        return bstack11l11l11ll_opy_
    def bstack11l11l1111_opy_(self, bstack11l11l1l11_opy_):
        def bstack11l11l11l1_opy_(this, *args, **kwargs):
            self.bstack11l111l1ll_opy_(this, bstack11l11l1l11_opy_)
            self._11l111ll11_opy_[bstack11l11l1l11_opy_](this, *args, **kwargs)
        return bstack11l11l11l1_opy_