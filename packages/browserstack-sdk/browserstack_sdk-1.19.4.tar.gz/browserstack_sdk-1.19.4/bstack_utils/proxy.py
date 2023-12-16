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
from urllib.parse import urlparse
from bstack_utils.messages import bstack11l111l11l_opy_
def bstack1111llll11_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1111lll1ll_opy_(bstack1111lllll1_opy_, bstack111l111111_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1111lllll1_opy_):
        with open(bstack1111lllll1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1111llll11_opy_(bstack1111lllll1_opy_):
        pac = get_pac(url=bstack1111lllll1_opy_)
    else:
        raise Exception(bstack1lllll1l_opy_ (u"ࠨࡒࡤࡧࠥ࡬ࡩ࡭ࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠨᎎ").format(bstack1111lllll1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1lllll1l_opy_ (u"ࠤ࠻࠲࠽࠴࠸࠯࠺ࠥᎏ"), 80))
        bstack1111llllll_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1111llllll_opy_ = bstack1lllll1l_opy_ (u"ࠪ࠴࠳࠶࠮࠱࠰࠳ࠫ᎐")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111l111111_opy_, bstack1111llllll_opy_)
    return proxy_url
def bstack1l11l111l_opy_(config):
    return bstack1lllll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ᎑") in config or bstack1lllll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ᎒") in config
def bstack1lll11ll11_opy_(config):
    if not bstack1l11l111l_opy_(config):
        return
    if config.get(bstack1lllll1l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ᎓")):
        return config.get(bstack1lllll1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ᎔"))
    if config.get(bstack1lllll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ᎕")):
        return config.get(bstack1lllll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭᎖"))
def bstack1ll11l111_opy_(config, bstack111l111111_opy_):
    proxy = bstack1lll11ll11_opy_(config)
    proxies = {}
    if config.get(bstack1lllll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭᎗")) or config.get(bstack1lllll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ᎘")):
        if proxy.endswith(bstack1lllll1l_opy_ (u"ࠬ࠴ࡰࡢࡥࠪ᎙")):
            proxies = bstack11111ll1l_opy_(proxy, bstack111l111111_opy_)
        else:
            proxies = {
                bstack1lllll1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ᎚"): proxy
            }
    return proxies
def bstack11111ll1l_opy_(bstack1111lllll1_opy_, bstack111l111111_opy_):
    proxies = {}
    global bstack1111llll1l_opy_
    if bstack1lllll1l_opy_ (u"ࠧࡑࡃࡆࡣࡕࡘࡏ࡙࡛ࠪ᎛") in globals():
        return bstack1111llll1l_opy_
    try:
        proxy = bstack1111lll1ll_opy_(bstack1111lllll1_opy_, bstack111l111111_opy_)
        if bstack1lllll1l_opy_ (u"ࠣࡆࡌࡖࡊࡉࡔࠣ᎜") in proxy:
            proxies = {}
        elif bstack1lllll1l_opy_ (u"ࠤࡋࡘ࡙ࡖࠢ᎝") in proxy or bstack1lllll1l_opy_ (u"ࠥࡌ࡙࡚ࡐࡔࠤ᎞") in proxy or bstack1lllll1l_opy_ (u"ࠦࡘࡕࡃࡌࡕࠥ᎟") in proxy:
            bstack1111lll1l1_opy_ = proxy.split(bstack1lllll1l_opy_ (u"ࠧࠦࠢᎠ"))
            if bstack1lllll1l_opy_ (u"ࠨ࠺࠰࠱ࠥᎡ") in bstack1lllll1l_opy_ (u"ࠢࠣᎢ").join(bstack1111lll1l1_opy_[1:]):
                proxies = {
                    bstack1lllll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᎣ"): bstack1lllll1l_opy_ (u"ࠤࠥᎤ").join(bstack1111lll1l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1lllll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᎥ"): str(bstack1111lll1l1_opy_[0]).lower() + bstack1lllll1l_opy_ (u"ࠦ࠿࠵࠯ࠣᎦ") + bstack1lllll1l_opy_ (u"ࠧࠨᎧ").join(bstack1111lll1l1_opy_[1:])
                }
        elif bstack1lllll1l_opy_ (u"ࠨࡐࡓࡑ࡛࡝ࠧᎨ") in proxy:
            bstack1111lll1l1_opy_ = proxy.split(bstack1lllll1l_opy_ (u"ࠢࠡࠤᎩ"))
            if bstack1lllll1l_opy_ (u"ࠣ࠼࠲࠳ࠧᎪ") in bstack1lllll1l_opy_ (u"ࠤࠥᎫ").join(bstack1111lll1l1_opy_[1:]):
                proxies = {
                    bstack1lllll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᎬ"): bstack1lllll1l_opy_ (u"ࠦࠧᎭ").join(bstack1111lll1l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1lllll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᎮ"): bstack1lllll1l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᎯ") + bstack1lllll1l_opy_ (u"ࠢࠣᎰ").join(bstack1111lll1l1_opy_[1:])
                }
        else:
            proxies = {
                bstack1lllll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᎱ"): proxy
            }
    except Exception as e:
        print(bstack1lllll1l_opy_ (u"ࠤࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨᎲ"), bstack11l111l11l_opy_.format(bstack1111lllll1_opy_, str(e)))
    bstack1111llll1l_opy_ = proxies
    return proxies