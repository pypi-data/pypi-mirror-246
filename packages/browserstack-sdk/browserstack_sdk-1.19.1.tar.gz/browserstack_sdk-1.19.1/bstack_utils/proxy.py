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
import os
from urllib.parse import urlparse
from bstack_utils.messages import bstack11l1111l1l_opy_
def bstack1111lll1ll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1111llll11_opy_(bstack1111ll1lll_opy_, bstack1111ll1ll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1111ll1lll_opy_):
        with open(bstack1111ll1lll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1111lll1ll_opy_(bstack1111ll1lll_opy_):
        pac = get_pac(url=bstack1111ll1lll_opy_)
    else:
        raise Exception(bstack11l1ll_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪ፴").format(bstack1111ll1lll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11l1ll_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧ፵"), 80))
        bstack1111lll1l1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1111lll1l1_opy_ = bstack11l1ll_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭፶")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1111ll1ll1_opy_, bstack1111lll1l1_opy_)
    return proxy_url
def bstack1ll11ll1l_opy_(config):
    return bstack11l1ll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ፷") in config or bstack11l1ll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ፸") in config
def bstack1111l1l11_opy_(config):
    if not bstack1ll11ll1l_opy_(config):
        return
    if config.get(bstack11l1ll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ፹")):
        return config.get(bstack11l1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ፺"))
    if config.get(bstack11l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ፻")):
        return config.get(bstack11l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ፼"))
def bstack11ll1lll_opy_(config, bstack1111ll1ll1_opy_):
    proxy = bstack1111l1l11_opy_(config)
    proxies = {}
    if config.get(bstack11l1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ፽")) or config.get(bstack11l1ll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ፾")):
        if proxy.endswith(bstack11l1ll_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ፿")):
            proxies = bstack1l11ll1l_opy_(proxy, bstack1111ll1ll1_opy_)
        else:
            proxies = {
                bstack11l1ll_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᎀ"): proxy
            }
    return proxies
def bstack1l11ll1l_opy_(bstack1111ll1lll_opy_, bstack1111ll1ll1_opy_):
    proxies = {}
    global bstack1111lll111_opy_
    if bstack11l1ll_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬᎁ") in globals():
        return bstack1111lll111_opy_
    try:
        proxy = bstack1111llll11_opy_(bstack1111ll1lll_opy_, bstack1111ll1ll1_opy_)
        if bstack11l1ll_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥᎂ") in proxy:
            proxies = {}
        elif bstack11l1ll_opy_ (u"ࠦࡍ࡚ࡔࡑࠤᎃ") in proxy or bstack11l1ll_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦᎄ") in proxy or bstack11l1ll_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧᎅ") in proxy:
            bstack1111lll11l_opy_ = proxy.split(bstack11l1ll_opy_ (u"ࠢࠡࠤᎆ"))
            if bstack11l1ll_opy_ (u"ࠣ࠼࠲࠳ࠧᎇ") in bstack11l1ll_opy_ (u"ࠤࠥᎈ").join(bstack1111lll11l_opy_[1:]):
                proxies = {
                    bstack11l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᎉ"): bstack11l1ll_opy_ (u"ࠦࠧᎊ").join(bstack1111lll11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᎋ"): str(bstack1111lll11l_opy_[0]).lower() + bstack11l1ll_opy_ (u"ࠨ࠺࠰࠱ࠥᎌ") + bstack11l1ll_opy_ (u"ࠢࠣᎍ").join(bstack1111lll11l_opy_[1:])
                }
        elif bstack11l1ll_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢᎎ") in proxy:
            bstack1111lll11l_opy_ = proxy.split(bstack11l1ll_opy_ (u"ࠤࠣࠦᎏ"))
            if bstack11l1ll_opy_ (u"ࠥ࠾࠴࠵ࠢ᎐") in bstack11l1ll_opy_ (u"ࠦࠧ᎑").join(bstack1111lll11l_opy_[1:]):
                proxies = {
                    bstack11l1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ᎒"): bstack11l1ll_opy_ (u"ࠨࠢ᎓").join(bstack1111lll11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1ll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭᎔"): bstack11l1ll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ᎕") + bstack11l1ll_opy_ (u"ࠤࠥ᎖").join(bstack1111lll11l_opy_[1:])
                }
        else:
            proxies = {
                bstack11l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ᎗"): proxy
            }
    except Exception as e:
        print(bstack11l1ll_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣ᎘"), bstack11l1111l1l_opy_.format(bstack1111ll1lll_opy_, str(e)))
    bstack1111lll111_opy_ = proxies
    return proxies