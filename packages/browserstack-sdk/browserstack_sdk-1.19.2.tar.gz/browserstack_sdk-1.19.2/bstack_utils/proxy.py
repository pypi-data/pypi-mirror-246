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
from urllib.parse import urlparse
from bstack_utils.messages import bstack11l1111lll_opy_
def bstack1111lll111_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1111llll11_opy_(bstack1111lll1ll_opy_, bstack1111lll1l1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1111lll1ll_opy_):
        with open(bstack1111lll1ll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1111lll111_opy_(bstack1111lll1ll_opy_):
        pac = get_pac(url=bstack1111lll1ll_opy_)
    else:
        raise Exception(bstack1lllll1_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪ፴").format(bstack1111lll1ll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1lllll1_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧ፵"), 80))
        bstack1111llll1l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1111llll1l_opy_ = bstack1lllll1_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭፶")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1111lll1l1_opy_, bstack1111llll1l_opy_)
    return proxy_url
def bstack111ll111l_opy_(config):
    return bstack1lllll1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ፷") in config or bstack1lllll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ፸") in config
def bstack1111l1l1l_opy_(config):
    if not bstack111ll111l_opy_(config):
        return
    if config.get(bstack1lllll1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ፹")):
        return config.get(bstack1lllll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ፺"))
    if config.get(bstack1lllll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ፻")):
        return config.get(bstack1lllll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ፼"))
def bstack1l111l11_opy_(config, bstack1111lll1l1_opy_):
    proxy = bstack1111l1l1l_opy_(config)
    proxies = {}
    if config.get(bstack1lllll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ፽")) or config.get(bstack1lllll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ፾")):
        if proxy.endswith(bstack1lllll1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ፿")):
            proxies = bstack11l11l1l1_opy_(proxy, bstack1111lll1l1_opy_)
        else:
            proxies = {
                bstack1lllll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᎀ"): proxy
            }
    return proxies
def bstack11l11l1l1_opy_(bstack1111lll1ll_opy_, bstack1111lll1l1_opy_):
    proxies = {}
    global bstack1111lllll1_opy_
    if bstack1lllll1_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬᎁ") in globals():
        return bstack1111lllll1_opy_
    try:
        proxy = bstack1111llll11_opy_(bstack1111lll1ll_opy_, bstack1111lll1l1_opy_)
        if bstack1lllll1_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥᎂ") in proxy:
            proxies = {}
        elif bstack1lllll1_opy_ (u"ࠦࡍ࡚ࡔࡑࠤᎃ") in proxy or bstack1lllll1_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦᎄ") in proxy or bstack1lllll1_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧᎅ") in proxy:
            bstack1111lll11l_opy_ = proxy.split(bstack1lllll1_opy_ (u"ࠢࠡࠤᎆ"))
            if bstack1lllll1_opy_ (u"ࠣ࠼࠲࠳ࠧᎇ") in bstack1lllll1_opy_ (u"ࠤࠥᎈ").join(bstack1111lll11l_opy_[1:]):
                proxies = {
                    bstack1lllll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᎉ"): bstack1lllll1_opy_ (u"ࠦࠧᎊ").join(bstack1111lll11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1lllll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᎋ"): str(bstack1111lll11l_opy_[0]).lower() + bstack1lllll1_opy_ (u"ࠨ࠺࠰࠱ࠥᎌ") + bstack1lllll1_opy_ (u"ࠢࠣᎍ").join(bstack1111lll11l_opy_[1:])
                }
        elif bstack1lllll1_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢᎎ") in proxy:
            bstack1111lll11l_opy_ = proxy.split(bstack1lllll1_opy_ (u"ࠤࠣࠦᎏ"))
            if bstack1lllll1_opy_ (u"ࠥ࠾࠴࠵ࠢ᎐") in bstack1lllll1_opy_ (u"ࠦࠧ᎑").join(bstack1111lll11l_opy_[1:]):
                proxies = {
                    bstack1lllll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ᎒"): bstack1lllll1_opy_ (u"ࠨࠢ᎓").join(bstack1111lll11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1lllll1_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭᎔"): bstack1lllll1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ᎕") + bstack1lllll1_opy_ (u"ࠤࠥ᎖").join(bstack1111lll11l_opy_[1:])
                }
        else:
            proxies = {
                bstack1lllll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ᎗"): proxy
            }
    except Exception as e:
        print(bstack1lllll1_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣ᎘"), bstack11l1111lll_opy_.format(bstack1111lll1ll_opy_, str(e)))
    bstack1111lllll1_opy_ = proxies
    return proxies