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
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack11ll11ll1l_opy_, bstack11l1l11ll_opy_, bstack1ll1lll1l_opy_, bstack1111llll1_opy_
from bstack_utils.messages import bstack1lll111l1l_opy_, bstack1l11l1lll_opy_
from bstack_utils.proxy import bstack1ll11l111_opy_, bstack1lll11ll11_opy_
from browserstack_sdk.bstack1llllll111_opy_ import *
from browserstack_sdk.bstack1l11lll1l1_opy_ import *
bstack1ll1ll1l1_opy_ = Config.get_instance()
def bstack11lll11l11_opy_(config):
    return config[bstack1lllll1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᄥ")]
def bstack11lll111l1_opy_(config):
    return config[bstack1lllll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᄦ")]
def bstack1l1l1lllll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l1ll1l11_opy_(obj):
    values = []
    bstack11ll11l1l1_opy_ = re.compile(bstack1lllll1l_opy_ (u"ࡴࠥࡢࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࡞ࡧ࠯ࠩࠨᄧ"), re.I)
    for key in obj.keys():
        if bstack11ll11l1l1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11ll1111l1_opy_(config):
    tags = []
    tags.extend(bstack11l1ll1l11_opy_(os.environ))
    tags.extend(bstack11l1ll1l11_opy_(config))
    return tags
def bstack11l1ll1ll1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l1l1111l_opy_(bstack11l1ll1l1l_opy_):
    if not bstack11l1ll1l1l_opy_:
        return bstack1lllll1l_opy_ (u"ࠪࠫᄨ")
    return bstack1lllll1l_opy_ (u"ࠦࢀࢃࠠࠩࡽࢀ࠭ࠧᄩ").format(bstack11l1ll1l1l_opy_.name, bstack11l1ll1l1l_opy_.email)
def bstack11llll111l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11ll11111l_opy_ = repo.common_dir
        info = {
            bstack1lllll1l_opy_ (u"ࠧࡹࡨࡢࠤᄪ"): repo.head.commit.hexsha,
            bstack1lllll1l_opy_ (u"ࠨࡳࡩࡱࡵࡸࡤࡹࡨࡢࠤᄫ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1lllll1l_opy_ (u"ࠢࡣࡴࡤࡲࡨ࡮ࠢᄬ"): repo.active_branch.name,
            bstack1lllll1l_opy_ (u"ࠣࡶࡤ࡫ࠧᄭ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1lllll1l_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࠧᄮ"): bstack11l1l1111l_opy_(repo.head.commit.committer),
            bstack1lllll1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࡥࡤࡢࡶࡨࠦᄯ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1lllll1l_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࠦᄰ"): bstack11l1l1111l_opy_(repo.head.commit.author),
            bstack1lllll1l_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡤࡪࡡࡵࡧࠥᄱ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1lllll1l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢᄲ"): repo.head.commit.message,
            bstack1lllll1l_opy_ (u"ࠢࡳࡱࡲࡸࠧᄳ"): repo.git.rev_parse(bstack1lllll1l_opy_ (u"ࠣ࠯࠰ࡷ࡭ࡵࡷ࠮ࡶࡲࡴࡱ࡫ࡶࡦ࡮ࠥᄴ")),
            bstack1lllll1l_opy_ (u"ࠤࡦࡳࡲࡳ࡯࡯ࡡࡪ࡭ࡹࡥࡤࡪࡴࠥᄵ"): bstack11ll11111l_opy_,
            bstack1lllll1l_opy_ (u"ࠥࡻࡴࡸ࡫ࡵࡴࡨࡩࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨᄶ"): subprocess.check_output([bstack1lllll1l_opy_ (u"ࠦ࡬࡯ࡴࠣᄷ"), bstack1lllll1l_opy_ (u"ࠧࡸࡥࡷ࠯ࡳࡥࡷࡹࡥࠣᄸ"), bstack1lllll1l_opy_ (u"ࠨ࠭࠮ࡩ࡬ࡸ࠲ࡩ࡯࡮࡯ࡲࡲ࠲ࡪࡩࡳࠤᄹ")]).strip().decode(
                bstack1lllll1l_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᄺ")),
            bstack1lllll1l_opy_ (u"ࠣ࡮ࡤࡷࡹࡥࡴࡢࡩࠥᄻ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1lllll1l_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡵࡢࡷ࡮ࡴࡣࡦࡡ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦᄼ"): repo.git.rev_list(
                bstack1lllll1l_opy_ (u"ࠥࡿࢂ࠴࠮ࡼࡿࠥᄽ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l1ll1111_opy_ = []
        for remote in remotes:
            bstack11l11ll1ll_opy_ = {
                bstack1lllll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᄾ"): remote.name,
                bstack1lllll1l_opy_ (u"ࠧࡻࡲ࡭ࠤᄿ"): remote.url,
            }
            bstack11l1ll1111_opy_.append(bstack11l11ll1ll_opy_)
        return {
            bstack1lllll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᅀ"): bstack1lllll1l_opy_ (u"ࠢࡨ࡫ࡷࠦᅁ"),
            **info,
            bstack1lllll1l_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡴࠤᅂ"): bstack11l1ll1111_opy_
        }
    except Exception as err:
        print(bstack1lllll1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡍࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᅃ").format(err))
        return {}
def bstack1lll1l1l11_opy_():
    env = os.environ
    if (bstack1lllll1l_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣᅄ") in env and len(env[bstack1lllll1l_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤᅅ")]) > 0) or (
            bstack1lllll1l_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦᅆ") in env and len(env[bstack1lllll1l_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧᅇ")]) > 0):
        return {
            bstack1lllll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᅈ"): bstack1lllll1l_opy_ (u"ࠣࡌࡨࡲࡰ࡯࡮ࡴࠤᅉ"),
            bstack1lllll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᅊ"): env.get(bstack1lllll1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᅋ")),
            bstack1lllll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᅌ"): env.get(bstack1lllll1l_opy_ (u"ࠧࡐࡏࡃࡡࡑࡅࡒࡋࠢᅍ")),
            bstack1lllll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᅎ"): env.get(bstack1lllll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᅏ"))
        }
    if env.get(bstack1lllll1l_opy_ (u"ࠣࡅࡌࠦᅐ")) == bstack1lllll1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᅑ") and bstack11l1l1ll_opy_(env.get(bstack1lllll1l_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡆࡍࠧᅒ"))):
        return {
            bstack1lllll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᅓ"): bstack1lllll1l_opy_ (u"ࠧࡉࡩࡳࡥ࡯ࡩࡈࡏࠢᅔ"),
            bstack1lllll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᅕ"): env.get(bstack1lllll1l_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᅖ")),
            bstack1lllll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᅗ"): env.get(bstack1lllll1l_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡍࡓࡇࠨᅘ")),
            bstack1lllll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᅙ"): env.get(bstack1lllll1l_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࠢᅚ"))
        }
    if env.get(bstack1lllll1l_opy_ (u"ࠧࡉࡉࠣᅛ")) == bstack1lllll1l_opy_ (u"ࠨࡴࡳࡷࡨࠦᅜ") and bstack11l1l1ll_opy_(env.get(bstack1lllll1l_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙ࠢᅝ"))):
        return {
            bstack1lllll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᅞ"): bstack1lllll1l_opy_ (u"ࠤࡗࡶࡦࡼࡩࡴࠢࡆࡍࠧᅟ"),
            bstack1lllll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᅠ"): env.get(bstack1lllll1l_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢ࡛ࡊࡈ࡟ࡖࡔࡏࠦᅡ")),
            bstack1lllll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᅢ"): env.get(bstack1lllll1l_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᅣ")),
            bstack1lllll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᅤ"): env.get(bstack1lllll1l_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᅥ"))
        }
    if env.get(bstack1lllll1l_opy_ (u"ࠤࡆࡍࠧᅦ")) == bstack1lllll1l_opy_ (u"ࠥࡸࡷࡻࡥࠣᅧ") and env.get(bstack1lllll1l_opy_ (u"ࠦࡈࡏ࡟ࡏࡃࡐࡉࠧᅨ")) == bstack1lllll1l_opy_ (u"ࠧࡩ࡯ࡥࡧࡶ࡬࡮ࡶࠢᅩ"):
        return {
            bstack1lllll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᅪ"): bstack1lllll1l_opy_ (u"ࠢࡄࡱࡧࡩࡸ࡮ࡩࡱࠤᅫ"),
            bstack1lllll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᅬ"): None,
            bstack1lllll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᅭ"): None,
            bstack1lllll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᅮ"): None
        }
    if env.get(bstack1lllll1l_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡔࡄࡒࡈࡎࠢᅯ")) and env.get(bstack1lllll1l_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡅࡒࡑࡒࡏࡔࠣᅰ")):
        return {
            bstack1lllll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᅱ"): bstack1lllll1l_opy_ (u"ࠢࡃ࡫ࡷࡦࡺࡩ࡫ࡦࡶࠥᅲ"),
            bstack1lllll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᅳ"): env.get(bstack1lllll1l_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡍࡉࡕࡡࡋࡘ࡙ࡖ࡟ࡐࡔࡌࡋࡎࡔࠢᅴ")),
            bstack1lllll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᅵ"): None,
            bstack1lllll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᅶ"): env.get(bstack1lllll1l_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᅷ"))
        }
    if env.get(bstack1lllll1l_opy_ (u"ࠨࡃࡊࠤᅸ")) == bstack1lllll1l_opy_ (u"ࠢࡵࡴࡸࡩࠧᅹ") and bstack11l1l1ll_opy_(env.get(bstack1lllll1l_opy_ (u"ࠣࡆࡕࡓࡓࡋࠢᅺ"))):
        return {
            bstack1lllll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᅻ"): bstack1lllll1l_opy_ (u"ࠥࡈࡷࡵ࡮ࡦࠤᅼ"),
            bstack1lllll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᅽ"): env.get(bstack1lllll1l_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡐࡎࡔࡋࠣᅾ")),
            bstack1lllll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᅿ"): None,
            bstack1lllll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᆀ"): env.get(bstack1lllll1l_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᆁ"))
        }
    if env.get(bstack1lllll1l_opy_ (u"ࠤࡆࡍࠧᆂ")) == bstack1lllll1l_opy_ (u"ࠥࡸࡷࡻࡥࠣᆃ") and bstack11l1l1ll_opy_(env.get(bstack1lllll1l_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋࠢᆄ"))):
        return {
            bstack1lllll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᆅ"): bstack1lllll1l_opy_ (u"ࠨࡓࡦ࡯ࡤࡴ࡭ࡵࡲࡦࠤᆆ"),
            bstack1lllll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᆇ"): env.get(bstack1lllll1l_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡔࡘࡇࡂࡐࡌ࡞ࡆ࡚ࡉࡐࡐࡢ࡙ࡗࡒࠢᆈ")),
            bstack1lllll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᆉ"): env.get(bstack1lllll1l_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᆊ")),
            bstack1lllll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᆋ"): env.get(bstack1lllll1l_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡏࡄࠣᆌ"))
        }
    if env.get(bstack1lllll1l_opy_ (u"ࠨࡃࡊࠤᆍ")) == bstack1lllll1l_opy_ (u"ࠢࡵࡴࡸࡩࠧᆎ") and bstack11l1l1ll_opy_(env.get(bstack1lllll1l_opy_ (u"ࠣࡉࡌࡘࡑࡇࡂࡠࡅࡌࠦᆏ"))):
        return {
            bstack1lllll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᆐ"): bstack1lllll1l_opy_ (u"ࠥࡋ࡮ࡺࡌࡢࡤࠥᆑ"),
            bstack1lllll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᆒ"): env.get(bstack1lllll1l_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤ࡛ࡒࡍࠤᆓ")),
            bstack1lllll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᆔ"): env.get(bstack1lllll1l_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᆕ")),
            bstack1lllll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᆖ"): env.get(bstack1lllll1l_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡌࡈࠧᆗ"))
        }
    if env.get(bstack1lllll1l_opy_ (u"ࠥࡇࡎࠨᆘ")) == bstack1lllll1l_opy_ (u"ࠦࡹࡸࡵࡦࠤᆙ") and bstack11l1l1ll_opy_(env.get(bstack1lllll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࠣᆚ"))):
        return {
            bstack1lllll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᆛ"): bstack1lllll1l_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡱࡩࡵࡧࠥᆜ"),
            bstack1lllll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᆝ"): env.get(bstack1lllll1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᆞ")),
            bstack1lllll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᆟ"): env.get(bstack1lllll1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡍࡃࡅࡉࡑࠨᆠ")) or env.get(bstack1lllll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣᆡ")),
            bstack1lllll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᆢ"): env.get(bstack1lllll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᆣ"))
        }
    if bstack11l1l1ll_opy_(env.get(bstack1lllll1l_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥᆤ"))):
        return {
            bstack1lllll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᆥ"): bstack1lllll1l_opy_ (u"࡚ࠥ࡮ࡹࡵࡢ࡮ࠣࡗࡹࡻࡤࡪࡱࠣࡘࡪࡧ࡭ࠡࡕࡨࡶࡻ࡯ࡣࡦࡵࠥᆦ"),
            bstack1lllll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᆧ"): bstack1lllll1l_opy_ (u"ࠧࢁࡽࡼࡿࠥᆨ").format(env.get(bstack1lllll1l_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩᆩ")), env.get(bstack1lllll1l_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࡎࡊࠧᆪ"))),
            bstack1lllll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᆫ"): env.get(bstack1lllll1l_opy_ (u"ࠤࡖ࡝ࡘ࡚ࡅࡎࡡࡇࡉࡋࡏࡎࡊࡖࡌࡓࡓࡏࡄࠣᆬ")),
            bstack1lllll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᆭ"): env.get(bstack1lllll1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᆮ"))
        }
    if bstack11l1l1ll_opy_(env.get(bstack1lllll1l_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘࠢᆯ"))):
        return {
            bstack1lllll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᆰ"): bstack1lllll1l_opy_ (u"ࠢࡂࡲࡳࡺࡪࡿ࡯ࡳࠤᆱ"),
            bstack1lllll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᆲ"): bstack1lllll1l_opy_ (u"ࠤࡾࢁ࠴ࡶࡲࡰ࡬ࡨࡧࡹ࠵ࡻࡾ࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠣᆳ").format(env.get(bstack1lllll1l_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤ࡛ࡒࡍࠩᆴ")), env.get(bstack1lllll1l_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡁࡄࡅࡒ࡙ࡓ࡚࡟ࡏࡃࡐࡉࠬᆵ")), env.get(bstack1lllll1l_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡕࡏ࡙ࡌ࠭ᆶ")), env.get(bstack1lllll1l_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪᆷ"))),
            bstack1lllll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᆸ"): env.get(bstack1lllll1l_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᆹ")),
            bstack1lllll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᆺ"): env.get(bstack1lllll1l_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᆻ"))
        }
    if env.get(bstack1lllll1l_opy_ (u"ࠦࡆࡠࡕࡓࡇࡢࡌ࡙࡚ࡐࡠࡗࡖࡉࡗࡥࡁࡈࡇࡑࡘࠧᆼ")) and env.get(bstack1lllll1l_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢᆽ")):
        return {
            bstack1lllll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᆾ"): bstack1lllll1l_opy_ (u"ࠢࡂࡼࡸࡶࡪࠦࡃࡊࠤᆿ"),
            bstack1lllll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᇀ"): bstack1lllll1l_opy_ (u"ࠤࡾࢁࢀࢃ࠯ࡠࡤࡸ࡭ࡱࡪ࠯ࡳࡧࡶࡹࡱࡺࡳࡀࡤࡸ࡭ࡱࡪࡉࡥ࠿ࡾࢁࠧᇁ").format(env.get(bstack1lllll1l_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ᇂ")), env.get(bstack1lllll1l_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࠩᇃ")), env.get(bstack1lllll1l_opy_ (u"ࠬࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠬᇄ"))),
            bstack1lllll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᇅ"): env.get(bstack1lllll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᇆ")),
            bstack1lllll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᇇ"): env.get(bstack1lllll1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤᇈ"))
        }
    if any([env.get(bstack1lllll1l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᇉ")), env.get(bstack1lllll1l_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᇊ")), env.get(bstack1lllll1l_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤᇋ"))]):
        return {
            bstack1lllll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇌ"): bstack1lllll1l_opy_ (u"ࠢࡂ࡙ࡖࠤࡈࡵࡤࡦࡄࡸ࡭ࡱࡪࠢᇍ"),
            bstack1lllll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᇎ"): env.get(bstack1lllll1l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡖࡕࡃࡎࡌࡇࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᇏ")),
            bstack1lllll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᇐ"): env.get(bstack1lllll1l_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᇑ")),
            bstack1lllll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᇒ"): env.get(bstack1lllll1l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᇓ"))
        }
    if env.get(bstack1lllll1l_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧᇔ")):
        return {
            bstack1lllll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᇕ"): bstack1lllll1l_opy_ (u"ࠤࡅࡥࡲࡨ࡯ࡰࠤᇖ"),
            bstack1lllll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᇗ"): env.get(bstack1lllll1l_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡕࡩࡸࡻ࡬ࡵࡵࡘࡶࡱࠨᇘ")),
            bstack1lllll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᇙ"): env.get(bstack1lllll1l_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡳࡩࡱࡵࡸࡏࡵࡢࡏࡣࡰࡩࠧᇚ")),
            bstack1lllll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᇛ"): env.get(bstack1lllll1l_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨᇜ"))
        }
    if env.get(bstack1lllll1l_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࠥᇝ")) or env.get(bstack1lllll1l_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧᇞ")):
        return {
            bstack1lllll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᇟ"): bstack1lllll1l_opy_ (u"ࠧ࡝ࡥࡳࡥ࡮ࡩࡷࠨᇠ"),
            bstack1lllll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᇡ"): env.get(bstack1lllll1l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᇢ")),
            bstack1lllll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᇣ"): bstack1lllll1l_opy_ (u"ࠤࡐࡥ࡮ࡴࠠࡑ࡫ࡳࡩࡱ࡯࡮ࡦࠤᇤ") if env.get(bstack1lllll1l_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧᇥ")) else None,
            bstack1lllll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᇦ"): env.get(bstack1lllll1l_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡇࡊࡖࡢࡇࡔࡓࡍࡊࡖࠥᇧ"))
        }
    if any([env.get(bstack1lllll1l_opy_ (u"ࠨࡇࡄࡒࡢࡔࡗࡕࡊࡆࡅࡗࠦᇨ")), env.get(bstack1lllll1l_opy_ (u"ࠢࡈࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᇩ")), env.get(bstack1lllll1l_opy_ (u"ࠣࡉࡒࡓࡌࡒࡅࡠࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᇪ"))]):
        return {
            bstack1lllll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᇫ"): bstack1lllll1l_opy_ (u"ࠥࡋࡴࡵࡧ࡭ࡧࠣࡇࡱࡵࡵࡥࠤᇬ"),
            bstack1lllll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᇭ"): None,
            bstack1lllll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᇮ"): env.get(bstack1lllll1l_opy_ (u"ࠨࡐࡓࡑࡍࡉࡈ࡚࡟ࡊࡆࠥᇯ")),
            bstack1lllll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᇰ"): env.get(bstack1lllll1l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᇱ"))
        }
    if env.get(bstack1lllll1l_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࠧᇲ")):
        return {
            bstack1lllll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᇳ"): bstack1lllll1l_opy_ (u"ࠦࡘ࡮ࡩࡱࡲࡤࡦࡱ࡫ࠢᇴ"),
            bstack1lllll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇵ"): env.get(bstack1lllll1l_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᇶ")),
            bstack1lllll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᇷ"): bstack1lllll1l_opy_ (u"ࠣࡌࡲࡦࠥࠩࡻࡾࠤᇸ").format(env.get(bstack1lllll1l_opy_ (u"ࠩࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠬᇹ"))) if env.get(bstack1lllll1l_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉࠨᇺ")) else None,
            bstack1lllll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᇻ"): env.get(bstack1lllll1l_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᇼ"))
        }
    if bstack11l1l1ll_opy_(env.get(bstack1lllll1l_opy_ (u"ࠨࡎࡆࡖࡏࡍࡋ࡟ࠢᇽ"))):
        return {
            bstack1lllll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᇾ"): bstack1lllll1l_opy_ (u"ࠣࡐࡨࡸࡱ࡯ࡦࡺࠤᇿ"),
            bstack1lllll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧሀ"): env.get(bstack1lllll1l_opy_ (u"ࠥࡈࡊࡖࡌࡐ࡛ࡢ࡙ࡗࡒࠢሁ")),
            bstack1lllll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨሂ"): env.get(bstack1lllll1l_opy_ (u"࡙ࠧࡉࡕࡇࡢࡒࡆࡓࡅࠣሃ")),
            bstack1lllll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧሄ"): env.get(bstack1lllll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤህ"))
        }
    if bstack11l1l1ll_opy_(env.get(bstack1lllll1l_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡃࡆࡘࡎࡕࡎࡔࠤሆ"))):
        return {
            bstack1lllll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢሇ"): bstack1lllll1l_opy_ (u"ࠥࡋ࡮ࡺࡈࡶࡤࠣࡅࡨࡺࡩࡰࡰࡶࠦለ"),
            bstack1lllll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢሉ"): bstack1lllll1l_opy_ (u"ࠧࢁࡽ࠰ࡽࢀ࠳ࡦࡩࡴࡪࡱࡱࡷ࠴ࡸࡵ࡯ࡵ࠲ࡿࢂࠨሊ").format(env.get(bstack1lllll1l_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡓࡆࡔ࡙ࡉࡗࡥࡕࡓࡎࠪላ")), env.get(bstack1lllll1l_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡇࡓࡓࡘࡏࡔࡐࡔ࡜ࠫሌ")), env.get(bstack1lllll1l_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠨል"))),
            bstack1lllll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦሎ"): env.get(bstack1lllll1l_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢ࡛ࡔࡘࡋࡇࡎࡒ࡛ࠧሏ")),
            bstack1lllll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥሐ"): env.get(bstack1lllll1l_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠧሑ"))
        }
    if env.get(bstack1lllll1l_opy_ (u"ࠨࡃࡊࠤሒ")) == bstack1lllll1l_opy_ (u"ࠢࡵࡴࡸࡩࠧሓ") and env.get(bstack1lllll1l_opy_ (u"ࠣࡘࡈࡖࡈࡋࡌࠣሔ")) == bstack1lllll1l_opy_ (u"ࠤ࠴ࠦሕ"):
        return {
            bstack1lllll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣሖ"): bstack1lllll1l_opy_ (u"࡛ࠦ࡫ࡲࡤࡧ࡯ࠦሗ"),
            bstack1lllll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣመ"): bstack1lllll1l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࡻࡾࠤሙ").format(env.get(bstack1lllll1l_opy_ (u"ࠧࡗࡇࡕࡇࡊࡒ࡟ࡖࡔࡏࠫሚ"))),
            bstack1lllll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥማ"): None,
            bstack1lllll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣሜ"): None,
        }
    if env.get(bstack1lllll1l_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤ࡜ࡅࡓࡕࡌࡓࡓࠨም")):
        return {
            bstack1lllll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤሞ"): bstack1lllll1l_opy_ (u"࡚ࠧࡥࡢ࡯ࡦ࡭ࡹࡿࠢሟ"),
            bstack1lllll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤሠ"): None,
            bstack1lllll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤሡ"): env.get(bstack1lllll1l_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠤሢ")),
            bstack1lllll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣሣ"): env.get(bstack1lllll1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤሤ"))
        }
    if any([env.get(bstack1lllll1l_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋࠢሥ")), env.get(bstack1lllll1l_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡕࡐࠧሦ")), env.get(bstack1lllll1l_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡗࡊࡘࡎࡂࡏࡈࠦሧ")), env.get(bstack1lllll1l_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢࡘࡊࡇࡍࠣረ"))]):
        return {
            bstack1lllll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨሩ"): bstack1lllll1l_opy_ (u"ࠤࡆࡳࡳࡩ࡯ࡶࡴࡶࡩࠧሪ"),
            bstack1lllll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨራ"): None,
            bstack1lllll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨሬ"): env.get(bstack1lllll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨር")) or None,
            bstack1lllll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧሮ"): env.get(bstack1lllll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤሯ"), 0)
        }
    if env.get(bstack1lllll1l_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨሰ")):
        return {
            bstack1lllll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢሱ"): bstack1lllll1l_opy_ (u"ࠥࡋࡴࡉࡄࠣሲ"),
            bstack1lllll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢሳ"): None,
            bstack1lllll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢሴ"): env.get(bstack1lllll1l_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦስ")),
            bstack1lllll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨሶ"): env.get(bstack1lllll1l_opy_ (u"ࠣࡉࡒࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡃࡐࡗࡑࡘࡊࡘࠢሷ"))
        }
    if env.get(bstack1lllll1l_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢሸ")):
        return {
            bstack1lllll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣሹ"): bstack1lllll1l_opy_ (u"ࠦࡈࡵࡤࡦࡈࡵࡩࡸ࡮ࠢሺ"),
            bstack1lllll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣሻ"): env.get(bstack1lllll1l_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧሼ")),
            bstack1lllll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤሽ"): env.get(bstack1lllll1l_opy_ (u"ࠣࡅࡉࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦሾ")),
            bstack1lllll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣሿ"): env.get(bstack1lllll1l_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣቀ"))
        }
    return {bstack1lllll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥቁ"): None}
def get_host_info():
    return {
        bstack1lllll1l_opy_ (u"ࠧ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠢቂ"): platform.node(),
        bstack1lllll1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣቃ"): platform.system(),
        bstack1lllll1l_opy_ (u"ࠢࡵࡻࡳࡩࠧቄ"): platform.machine(),
        bstack1lllll1l_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤቅ"): platform.version(),
        bstack1lllll1l_opy_ (u"ࠤࡤࡶࡨ࡮ࠢቆ"): platform.architecture()[0]
    }
def bstack1l1ll1111_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11ll111lll_opy_():
    if bstack1ll1ll1l1_opy_.get_property(bstack1lllll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫቇ")):
        return bstack1lllll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪቈ")
    return bstack1lllll1l_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠫ቉")
def bstack11ll111l1l_opy_(driver):
    info = {
        bstack1lllll1l_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬቊ"): driver.capabilities,
        bstack1lllll1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫቋ"): driver.session_id,
        bstack1lllll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩቌ"): driver.capabilities.get(bstack1lllll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧቍ"), None),
        bstack1lllll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ቎"): driver.capabilities.get(bstack1lllll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ቏"), None),
        bstack1lllll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࠧቐ"): driver.capabilities.get(bstack1lllll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬቑ"), None),
    }
    if bstack11ll111lll_opy_() == bstack1lllll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ቒ"):
        info[bstack1lllll1l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩቓ")] = bstack1lllll1l_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨቔ") if bstack11l111111_opy_() else bstack1lllll1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬቕ")
    return info
def bstack11l111111_opy_():
    if bstack1ll1ll1l1_opy_.get_property(bstack1lllll1l_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪቖ")):
        return True
    if bstack11l1l1ll_opy_(os.environ.get(bstack1lllll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭቗"), None)):
        return True
    return False
def bstack1lll1ll1_opy_(bstack11l1l111ll_opy_, url, data, config):
    headers = config.get(bstack1lllll1l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧቘ"), None)
    proxies = bstack1ll11l111_opy_(config, url)
    auth = config.get(bstack1lllll1l_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ቙"), None)
    response = requests.request(
            bstack11l1l111ll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l111lll1_opy_(bstack111l1lll_opy_, size):
    bstack11l1111l1_opy_ = []
    while len(bstack111l1lll_opy_) > size:
        bstack1111lll1_opy_ = bstack111l1lll_opy_[:size]
        bstack11l1111l1_opy_.append(bstack1111lll1_opy_)
        bstack111l1lll_opy_ = bstack111l1lll_opy_[size:]
    bstack11l1111l1_opy_.append(bstack111l1lll_opy_)
    return bstack11l1111l1_opy_
def bstack11l1l1l11l_opy_(message, bstack11l1l1ll11_opy_=False):
    os.write(1, bytes(message, bstack1lllll1l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧቚ")))
    os.write(1, bytes(bstack1lllll1l_opy_ (u"ࠩ࡟ࡲࠬቛ"), bstack1lllll1l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩቜ")))
    if bstack11l1l1ll11_opy_:
        with open(bstack1lllll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡴ࠷࠱ࡺ࠯ࠪቝ") + os.environ[bstack1lllll1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫ቞")] + bstack1lllll1l_opy_ (u"࠭࠮࡭ࡱࡪࠫ቟"), bstack1lllll1l_opy_ (u"ࠧࡢࠩበ")) as f:
            f.write(message + bstack1lllll1l_opy_ (u"ࠨ࡞ࡱࠫቡ"))
def bstack11l1ll111l_opy_():
    return os.environ[bstack1lllll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬቢ")].lower() == bstack1lllll1l_opy_ (u"ࠪࡸࡷࡻࡥࠨባ")
def bstack11lll1lll_opy_(bstack11ll11l111_opy_):
    return bstack1lllll1l_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪቤ").format(bstack11ll11ll1l_opy_, bstack11ll11l111_opy_)
def bstack1llll1ll1_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack1lllll1l_opy_ (u"ࠬࡠࠧብ")
def bstack11l1l11lll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1lllll1l_opy_ (u"࡚࠭ࠨቦ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1lllll1l_opy_ (u"࡛ࠧࠩቧ")))).total_seconds() * 1000
def bstack11l1l111l1_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack1lllll1l_opy_ (u"ࠨ࡜ࠪቨ")
def bstack11l1ll11l1_opy_(bstack11ll111l11_opy_):
    date_format = bstack1lllll1l_opy_ (u"ࠩࠨ࡝ࠪࡳࠥࡥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠧቩ")
    bstack11l11lll11_opy_ = datetime.datetime.strptime(bstack11ll111l11_opy_, date_format)
    return bstack11l11lll11_opy_.isoformat() + bstack1lllll1l_opy_ (u"ࠪ࡞ࠬቪ")
def bstack11l1lllll1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1lllll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫቫ")
    else:
        return bstack1lllll1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬቬ")
def bstack11l1l1ll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1lllll1l_opy_ (u"࠭ࡴࡳࡷࡨࠫቭ")
def bstack11l11lll1l_opy_(val):
    return val.__str__().lower() == bstack1lllll1l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ቮ")
def bstack1l111l1lll_opy_(bstack11l1l1l1l1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l1l1l1l1_opy_ as e:
                print(bstack1lllll1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡾࢁࠥ࠳࠾ࠡࡽࢀ࠾ࠥࢁࡽࠣቯ").format(func.__name__, bstack11l1l1l1l1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11ll111ll1_opy_(bstack11l1lll11l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l1lll11l_opy_(cls, *args, **kwargs)
            except bstack11l1l1l1l1_opy_ as e:
                print(bstack1lllll1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤተ").format(bstack11l1lll11l_opy_.__name__, bstack11l1l1l1l1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11ll111ll1_opy_
    else:
        return decorator
def bstack1l1l1l1ll_opy_(bstack11lllll111_opy_):
    if bstack1lllll1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧቱ") in bstack11lllll111_opy_ and bstack11l11lll1l_opy_(bstack11lllll111_opy_[bstack1lllll1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨቲ")]):
        return False
    if bstack1lllll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧታ") in bstack11lllll111_opy_ and bstack11l11lll1l_opy_(bstack11lllll111_opy_[bstack1lllll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨቴ")]):
        return False
    return True
def bstack1llll1l11l_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1ll1l1l11_opy_(hub_url):
    if bstack1l11ll1l_opy_() <= version.parse(bstack1lllll1l_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧት")):
        if hub_url != bstack1lllll1l_opy_ (u"ࠨࠩቶ"):
            return bstack1lllll1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥቷ") + hub_url + bstack1lllll1l_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢቸ")
        return bstack1ll1lll1l_opy_
    if hub_url != bstack1lllll1l_opy_ (u"ࠫࠬቹ"):
        return bstack1lllll1l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢቺ") + hub_url + bstack1lllll1l_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢቻ")
    return bstack1111llll1_opy_
def bstack11ll11l1ll_opy_():
    return isinstance(os.getenv(bstack1lllll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭ቼ")), str)
def bstack11ll1ll1_opy_(url):
    return urlparse(url).hostname
def bstack111l11111_opy_(hostname):
    for bstack1ll11ll1ll_opy_ in bstack11l1l11ll_opy_:
        regex = re.compile(bstack1ll11ll1ll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l11lllll_opy_(bstack11ll1111ll_opy_, file_name, logger):
    bstack111llll11_opy_ = os.path.join(os.path.expanduser(bstack1lllll1l_opy_ (u"ࠨࢀࠪች")), bstack11ll1111ll_opy_)
    try:
        if not os.path.exists(bstack111llll11_opy_):
            os.makedirs(bstack111llll11_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1lllll1l_opy_ (u"ࠩࢁࠫቾ")), bstack11ll1111ll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1lllll1l_opy_ (u"ࠪࡻࠬቿ")):
                pass
            with open(file_path, bstack1lllll1l_opy_ (u"ࠦࡼ࠱ࠢኀ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1lll111l1l_opy_.format(str(e)))
def bstack11l1l11ll1_opy_(file_name, key, value, logger):
    file_path = bstack11l11lllll_opy_(bstack1lllll1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬኁ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1ll1l11ll_opy_ = json.load(open(file_path, bstack1lllll1l_opy_ (u"࠭ࡲࡣࠩኂ")))
        else:
            bstack1ll1l11ll_opy_ = {}
        bstack1ll1l11ll_opy_[key] = value
        with open(file_path, bstack1lllll1l_opy_ (u"ࠢࡸ࠭ࠥኃ")) as outfile:
            json.dump(bstack1ll1l11ll_opy_, outfile)
def bstack11l11l1l_opy_(file_name, logger):
    file_path = bstack11l11lllll_opy_(bstack1lllll1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨኄ"), file_name, logger)
    bstack1ll1l11ll_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1lllll1l_opy_ (u"ࠩࡵࠫኅ")) as bstack111l1ll11_opy_:
            bstack1ll1l11ll_opy_ = json.load(bstack111l1ll11_opy_)
    return bstack1ll1l11ll_opy_
def bstack11lll111l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1lllll1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࠧኆ") + file_path + bstack1lllll1l_opy_ (u"ࠫࠥ࠭ኇ") + str(e))
def bstack1l11ll1l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1lllll1l_opy_ (u"ࠧࡂࡎࡐࡖࡖࡉ࡙ࡄࠢኈ")
def bstack1l1l11l1l1_opy_(config):
    if bstack1lllll1l_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ኉") in config:
        del (config[bstack1lllll1l_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ኊ")])
        return False
    if bstack1l11ll1l_opy_() < version.parse(bstack1lllll1l_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧኋ")):
        return False
    if bstack1l11ll1l_opy_() >= version.parse(bstack1lllll1l_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨኌ")):
        return True
    if bstack1lllll1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪኍ") in config and config[bstack1lllll1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ኎")] is False:
        return False
    else:
        return True
def bstack1l1ll11l1l_opy_(args_list, bstack11l1l1lll1_opy_):
    index = -1
    for value in bstack11l1l1lll1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l11ll1111_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l11ll1111_opy_ = bstack1l11ll1111_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1lllll1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ኏"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1lllll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ነ"), exception=exception)
    def bstack11llll1l1l_opy_(self):
        if self.result != bstack1lllll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧኑ"):
            return None
        if bstack1lllll1l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦኒ") in self.exception_type:
            return bstack1lllll1l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥና")
        return bstack1lllll1l_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦኔ")
    def bstack11l1lll1l1_opy_(self):
        if self.result != bstack1lllll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫን"):
            return None
        if self.bstack1l11ll1111_opy_:
            return self.bstack1l11ll1111_opy_
        return bstack11l1l11111_opy_(self.exception)
def bstack11l1l11111_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l1l11l1l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11l1l11l1_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1ll1llll_opy_(config, logger):
    try:
        import playwright
        bstack11l11ll1l1_opy_ = playwright.__file__
        bstack11l1l1l1ll_opy_ = os.path.split(bstack11l11ll1l1_opy_)
        bstack11ll11l11l_opy_ = bstack11l1l1l1ll_opy_[0] + bstack1lllll1l_opy_ (u"ࠬ࠵ࡤࡳ࡫ࡹࡩࡷ࠵ࡰࡢࡥ࡮ࡥ࡬࡫࠯࡭࡫ࡥ࠳ࡨࡲࡩ࠰ࡥ࡯࡭࠳ࡰࡳࠨኖ")
        os.environ[bstack1lllll1l_opy_ (u"࠭ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠩኗ")] = bstack1lll11ll11_opy_(config)
        with open(bstack11ll11l11l_opy_, bstack1lllll1l_opy_ (u"ࠧࡳࠩኘ")) as f:
            bstack1l111111_opy_ = f.read()
            bstack11l1ll11ll_opy_ = bstack1lllll1l_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧኙ")
            bstack11l1llllll_opy_ = bstack1l111111_opy_.find(bstack11l1ll11ll_opy_)
            if bstack11l1llllll_opy_ == -1:
              process = subprocess.Popen(bstack1lllll1l_opy_ (u"ࠤࡱࡴࡲࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹࠨኚ"), shell=True, cwd=bstack11l1l1l1ll_opy_[0])
              process.wait()
              bstack11l11llll1_opy_ = bstack1lllll1l_opy_ (u"ࠪࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴࠣ࠽ࠪኛ")
              bstack11l1lll111_opy_ = bstack1lllll1l_opy_ (u"ࠦࠧࠨࠠ࡝ࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࡢࠢ࠼ࠢࡦࡳࡳࡹࡴࠡࡽࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵࠦࡽࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ࠮ࡁࠠࡪࡨࠣࠬࡵࡸ࡯ࡤࡧࡶࡷ࠳࡫࡮ࡷ࠰ࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝࠮ࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠪࠬ࠿ࠥࠨࠢࠣኜ")
              bstack11l1llll1l_opy_ = bstack1l111111_opy_.replace(bstack11l11llll1_opy_, bstack11l1lll111_opy_)
              with open(bstack11ll11l11l_opy_, bstack1lllll1l_opy_ (u"ࠬࡽࠧኝ")) as f:
                f.write(bstack11l1llll1l_opy_)
    except Exception as e:
        logger.error(bstack1l11l1lll_opy_.format(str(e)))
def bstack1l111lll_opy_():
  try:
    bstack11ll111111_opy_ = os.path.join(tempfile.gettempdir(), bstack1lllll1l_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭ኞ"))
    bstack11l1l1ll1l_opy_ = []
    if os.path.exists(bstack11ll111111_opy_):
      with open(bstack11ll111111_opy_) as f:
        bstack11l1l1ll1l_opy_ = json.load(f)
      os.remove(bstack11ll111111_opy_)
    return bstack11l1l1ll1l_opy_
  except:
    pass
  return []
def bstack1llllllll1_opy_(bstack11l1l11l_opy_):
  try:
    bstack11l1l1ll1l_opy_ = []
    bstack11ll111111_opy_ = os.path.join(tempfile.gettempdir(), bstack1lllll1l_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧኟ"))
    if os.path.exists(bstack11ll111111_opy_):
      with open(bstack11ll111111_opy_) as f:
        bstack11l1l1ll1l_opy_ = json.load(f)
    bstack11l1l1ll1l_opy_.append(bstack11l1l11l_opy_)
    with open(bstack11ll111111_opy_, bstack1lllll1l_opy_ (u"ࠨࡹࠪአ")) as f:
        json.dump(bstack11l1l1ll1l_opy_, f)
  except:
    pass
def bstack1l1llll11_opy_(logger, bstack11l1lll1ll_opy_ = False):
  try:
    test_name = os.environ.get(bstack1lllll1l_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬኡ"), bstack1lllll1l_opy_ (u"ࠪࠫኢ"))
    if test_name == bstack1lllll1l_opy_ (u"ࠫࠬኣ"):
        test_name = threading.current_thread().__dict__.get(bstack1lllll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡇࡪࡤࡠࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠫኤ"), bstack1lllll1l_opy_ (u"࠭ࠧእ"))
    bstack11l1ll1lll_opy_ = bstack1lllll1l_opy_ (u"ࠧ࠭ࠢࠪኦ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l1lll1ll_opy_:
        bstack111l1l111_opy_ = os.environ.get(bstack1lllll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨኧ"), bstack1lllll1l_opy_ (u"ࠩ࠳ࠫከ"))
        bstack1ll1l111_opy_ = {bstack1lllll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨኩ"): test_name, bstack1lllll1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪኪ"): bstack11l1ll1lll_opy_, bstack1lllll1l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫካ"): bstack111l1l111_opy_}
        bstack11l1l11l11_opy_ = []
        bstack11l1llll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1lllll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬኬ"))
        if os.path.exists(bstack11l1llll11_opy_):
            with open(bstack11l1llll11_opy_) as f:
                bstack11l1l11l11_opy_ = json.load(f)
        bstack11l1l11l11_opy_.append(bstack1ll1l111_opy_)
        with open(bstack11l1llll11_opy_, bstack1lllll1l_opy_ (u"ࠧࡸࠩክ")) as f:
            json.dump(bstack11l1l11l11_opy_, f)
    else:
        bstack1ll1l111_opy_ = {bstack1lllll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ኮ"): test_name, bstack1lllll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨኯ"): bstack11l1ll1lll_opy_, bstack1lllll1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩኰ"): str(multiprocessing.current_process().name)}
        if bstack1lllll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨ኱") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1ll1l111_opy_)
  except Exception as e:
      logger.warn(bstack1lllll1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡱࡻࡷࡩࡸࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤኲ").format(e))
def bstack11ll1llll_opy_(error_message, test_name, index, logger):
  try:
    bstack11l1l1llll_opy_ = []
    bstack1ll1l111_opy_ = {bstack1lllll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫኳ"): test_name, bstack1lllll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ኴ"): error_message, bstack1lllll1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧኵ"): index}
    bstack11l1l1l111_opy_ = os.path.join(tempfile.gettempdir(), bstack1lllll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪ኶"))
    if os.path.exists(bstack11l1l1l111_opy_):
        with open(bstack11l1l1l111_opy_) as f:
            bstack11l1l1llll_opy_ = json.load(f)
    bstack11l1l1llll_opy_.append(bstack1ll1l111_opy_)
    with open(bstack11l1l1l111_opy_, bstack1lllll1l_opy_ (u"ࠪࡻࠬ኷")) as f:
        json.dump(bstack11l1l1llll_opy_, f)
  except Exception as e:
    logger.warn(bstack1lllll1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢኸ").format(e))
def bstack1l1l1l11_opy_(bstack1111l1l11_opy_, name, logger):
  try:
    bstack1ll1l111_opy_ = {bstack1lllll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪኹ"): name, bstack1lllll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬኺ"): bstack1111l1l11_opy_, bstack1lllll1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ኻ"): str(threading.current_thread()._name)}
    return bstack1ll1l111_opy_
  except Exception as e:
    logger.warn(bstack1lllll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧኼ").format(e))
  return
def bstack1lll1lll11_opy_(framework):
    if framework.lower() == bstack1lllll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩኽ"):
        return bstack1l1111l1l_opy_.version()
    elif framework.lower() == bstack1lllll1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩኾ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1lllll1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ኿"):
        import behave
        return behave.__version__
    else:
        return bstack1lllll1l_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳ࠭ዀ")