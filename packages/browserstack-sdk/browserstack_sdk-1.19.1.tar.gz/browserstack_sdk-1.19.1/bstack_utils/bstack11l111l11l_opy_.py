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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result
def _11l1111lll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l111l1l1_opy_:
    def __init__(self, handler):
        self._11l111l111_opy_ = {}
        self._11l111lll1_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._11l111l111_opy_[bstack11l1ll_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫኧ")] = Module._inject_setup_function_fixture
        self._11l111l111_opy_[bstack11l1ll_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪከ")] = Module._inject_setup_module_fixture
        self._11l111l111_opy_[bstack11l1ll_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪኩ")] = Class._inject_setup_class_fixture
        self._11l111l111_opy_[bstack11l1ll_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬኪ")] = Class._inject_setup_method_fixture
        Module._inject_setup_function_fixture = self.bstack11l111ll11_opy_(bstack11l1ll_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨካ"))
        Module._inject_setup_module_fixture = self.bstack11l111ll11_opy_(bstack11l1ll_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧኬ"))
        Class._inject_setup_class_fixture = self.bstack11l111ll11_opy_(bstack11l1ll_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧክ"))
        Class._inject_setup_method_fixture = self.bstack11l111ll11_opy_(bstack11l1ll_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩኮ"))
    def bstack11l1111ll1_opy_(self, bstack11l111l1ll_opy_, hook_type):
        meth = getattr(bstack11l111l1ll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l111lll1_opy_[hook_type] = meth
            setattr(bstack11l111l1ll_opy_, hook_type, self.bstack11l111ll1l_opy_(hook_type))
    def bstack11l11l11l1_opy_(self, instance, bstack11l11l111l_opy_):
        if bstack11l11l111l_opy_ == bstack11l1ll_opy_ (u"ࠤࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠧኯ"):
            self.bstack11l1111ll1_opy_(instance.obj, bstack11l1ll_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠦኰ"))
            self.bstack11l1111ll1_opy_(instance.obj, bstack11l1ll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣ኱"))
        if bstack11l11l111l_opy_ == bstack11l1ll_opy_ (u"ࠧࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࠨኲ"):
            self.bstack11l1111ll1_opy_(instance.obj, bstack11l1ll_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠧኳ"))
            self.bstack11l1111ll1_opy_(instance.obj, bstack11l1ll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠤኴ"))
        if bstack11l11l111l_opy_ == bstack11l1ll_opy_ (u"ࠣࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣኵ"):
            self.bstack11l1111ll1_opy_(instance.obj, bstack11l1ll_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠢ኶"))
            self.bstack11l1111ll1_opy_(instance.obj, bstack11l1ll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠦ኷"))
        if bstack11l11l111l_opy_ == bstack11l1ll_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠧኸ"):
            self.bstack11l1111ll1_opy_(instance.obj, bstack11l1ll_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠦኹ"))
            self.bstack11l1111ll1_opy_(instance.obj, bstack11l1ll_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠣኺ"))
    @staticmethod
    def bstack11l11l1111_opy_(hook_type, func, args):
        if hook_type in [bstack11l1ll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ኻ"), bstack11l1ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪኼ")]:
            _11l1111lll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l111ll1l_opy_(self, hook_type):
        def bstack11l11l1l11_opy_(arg=None):
            self.handler(hook_type, bstack11l1ll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩኽ"))
            result = None
            exception = None
            try:
                self.bstack11l11l1111_opy_(hook_type, self._11l111lll1_opy_[hook_type], (arg,))
                result = Result(result=bstack11l1ll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪኾ"))
            except Exception as e:
                result = Result(result=bstack11l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ኿"), exception=e)
                self.handler(hook_type, bstack11l1ll_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫዀ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l1ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬ዁"), result)
        def bstack11l11l11ll_opy_(this, arg=None):
            self.handler(hook_type, bstack11l1ll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧዂ"))
            result = None
            exception = None
            try:
                self.bstack11l11l1111_opy_(hook_type, self._11l111lll1_opy_[hook_type], (this, arg))
                result = Result(result=bstack11l1ll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨዃ"))
            except Exception as e:
                result = Result(result=bstack11l1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩዄ"), exception=e)
                self.handler(hook_type, bstack11l1ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩዅ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l1ll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ዆"), result)
        if hook_type in [bstack11l1ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫ዇"), bstack11l1ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨወ")]:
            return bstack11l11l11ll_opy_
        return bstack11l11l1l11_opy_
    def bstack11l111ll11_opy_(self, bstack11l11l111l_opy_):
        def bstack11l111llll_opy_(this, *args, **kwargs):
            self.bstack11l11l11l1_opy_(this, bstack11l11l111l_opy_)
            self._11l111l111_opy_[bstack11l11l111l_opy_](this, *args, **kwargs)
        return bstack11l111llll_opy_