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
from bstack_utils.constants import bstack11ll111lll_opy_, bstack1111l111_opy_, bstack1lllll11_opy_, bstack1l1l1111_opy_
from bstack_utils.messages import bstack11l11l111_opy_, bstack1l111111_opy_
from bstack_utils.proxy import bstack11ll1lll_opy_, bstack1111l1l11_opy_
from browserstack_sdk.bstack1llllll1ll_opy_ import *
from browserstack_sdk.bstack1l11l1llll_opy_ import *
bstack1ll1l11ll1_opy_ = Config.get_instance()
def bstack11lll11lll_opy_(config):
    return config[bstack11l1ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᄋ")]
def bstack11lll1l1l1_opy_(config):
    return config[bstack11l1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᄌ")]
def bstack1lll1ll1ll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l11lll11_opy_(obj):
    values = []
    bstack11ll11111l_opy_ = re.compile(bstack11l1ll_opy_ (u"ࡶࠧࡤࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢࡠࡩ࠱ࠤࠣᄍ"), re.I)
    for key in obj.keys():
        if bstack11ll11111l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l11l1ll1_opy_(config):
    tags = []
    tags.extend(bstack11l11lll11_opy_(os.environ))
    tags.extend(bstack11l11lll11_opy_(config))
    return tags
def bstack11l1l11l11_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l1ll111l_opy_(bstack11ll111l11_opy_):
    if not bstack11ll111l11_opy_:
        return bstack11l1ll_opy_ (u"ࠬ࠭ᄎ")
    return bstack11l1ll_opy_ (u"ࠨࡻࡾࠢࠫࡿࢂ࠯ࠢᄏ").format(bstack11ll111l11_opy_.name, bstack11ll111l11_opy_.email)
def bstack11ll1ll1ll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11ll111111_opy_ = repo.common_dir
        info = {
            bstack11l1ll_opy_ (u"ࠢࡴࡪࡤࠦᄐ"): repo.head.commit.hexsha,
            bstack11l1ll_opy_ (u"ࠣࡵ࡫ࡳࡷࡺ࡟ࡴࡪࡤࠦᄑ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11l1ll_opy_ (u"ࠤࡥࡶࡦࡴࡣࡩࠤᄒ"): repo.active_branch.name,
            bstack11l1ll_opy_ (u"ࠥࡸࡦ࡭ࠢᄓ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11l1ll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸࠢᄔ"): bstack11l1ll111l_opy_(repo.head.commit.committer),
            bstack11l1ll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࡠࡦࡤࡸࡪࠨᄕ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11l1ll_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࠨᄖ"): bstack11l1ll111l_opy_(repo.head.commit.author),
            bstack11l1ll_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸ࡟ࡥࡣࡷࡩࠧᄗ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11l1ll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤᄘ"): repo.head.commit.message,
            bstack11l1ll_opy_ (u"ࠤࡵࡳࡴࡺࠢᄙ"): repo.git.rev_parse(bstack11l1ll_opy_ (u"ࠥ࠱࠲ࡹࡨࡰࡹ࠰ࡸࡴࡶ࡬ࡦࡸࡨࡰࠧᄚ")),
            bstack11l1ll_opy_ (u"ࠦࡨࡵ࡭࡮ࡱࡱࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧᄛ"): bstack11ll111111_opy_,
            bstack11l1ll_opy_ (u"ࠧࡽ࡯ࡳ࡭ࡷࡶࡪ࡫࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣᄜ"): subprocess.check_output([bstack11l1ll_opy_ (u"ࠨࡧࡪࡶࠥᄝ"), bstack11l1ll_opy_ (u"ࠢࡳࡧࡹ࠱ࡵࡧࡲࡴࡧࠥᄞ"), bstack11l1ll_opy_ (u"ࠣ࠯࠰࡫࡮ࡺ࠭ࡤࡱࡰࡱࡴࡴ࠭ࡥ࡫ࡵࠦᄟ")]).strip().decode(
                bstack11l1ll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᄠ")),
            bstack11l1ll_opy_ (u"ࠥࡰࡦࡹࡴࡠࡶࡤ࡫ࠧᄡ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11l1ll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡷࡤࡹࡩ࡯ࡥࡨࡣࡱࡧࡳࡵࡡࡷࡥ࡬ࠨᄢ"): repo.git.rev_list(
                bstack11l1ll_opy_ (u"ࠧࢁࡽ࠯࠰ࡾࢁࠧᄣ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l1lll11l_opy_ = []
        for remote in remotes:
            bstack11l1l1l1ll_opy_ = {
                bstack11l1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᄤ"): remote.name,
                bstack11l1ll_opy_ (u"ࠢࡶࡴ࡯ࠦᄥ"): remote.url,
            }
            bstack11l1lll11l_opy_.append(bstack11l1l1l1ll_opy_)
        return {
            bstack11l1ll_opy_ (u"ࠣࡰࡤࡱࡪࠨᄦ"): bstack11l1ll_opy_ (u"ࠤࡪ࡭ࡹࠨᄧ"),
            **info,
            bstack11l1ll_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡶࠦᄨ"): bstack11l1lll11l_opy_
        }
    except Exception as err:
        print(bstack11l1ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᄩ").format(err))
        return {}
def bstack1ll11lll11_opy_():
    env = os.environ
    if (bstack11l1ll_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥᄪ") in env and len(env[bstack11l1ll_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦᄫ")]) > 0) or (
            bstack11l1ll_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨᄬ") in env and len(env[bstack11l1ll_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢᄭ")]) > 0):
        return {
            bstack11l1ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᄮ"): bstack11l1ll_opy_ (u"ࠥࡎࡪࡴ࡫ࡪࡰࡶࠦᄯ"),
            bstack11l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᄰ"): env.get(bstack11l1ll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᄱ")),
            bstack11l1ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᄲ"): env.get(bstack11l1ll_opy_ (u"ࠢࡋࡑࡅࡣࡓࡇࡍࡆࠤᄳ")),
            bstack11l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᄴ"): env.get(bstack11l1ll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᄵ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠥࡇࡎࠨᄶ")) == bstack11l1ll_opy_ (u"ࠦࡹࡸࡵࡦࠤᄷ") and bstack1l1lll11l_opy_(env.get(bstack11l1ll_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡈࡏࠢᄸ"))):
        return {
            bstack11l1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᄹ"): bstack11l1ll_opy_ (u"ࠢࡄ࡫ࡵࡧࡱ࡫ࡃࡊࠤᄺ"),
            bstack11l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᄻ"): env.get(bstack11l1ll_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᄼ")),
            bstack11l1ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᄽ"): env.get(bstack11l1ll_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡏࡕࡂࠣᄾ")),
            bstack11l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᄿ"): env.get(bstack11l1ll_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࠤᅀ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠢࡄࡋࠥᅁ")) == bstack11l1ll_opy_ (u"ࠣࡶࡵࡹࡪࠨᅂ") and bstack1l1lll11l_opy_(env.get(bstack11l1ll_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࠤᅃ"))):
        return {
            bstack11l1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣᅄ"): bstack11l1ll_opy_ (u"࡙ࠦࡸࡡࡷ࡫ࡶࠤࡈࡏࠢᅅ"),
            bstack11l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᅆ"): env.get(bstack11l1ll_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤ࡝ࡅࡃࡡࡘࡖࡑࠨᅇ")),
            bstack11l1ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᅈ"): env.get(bstack11l1ll_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᅉ")),
            bstack11l1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᅊ"): env.get(bstack11l1ll_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᅋ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠦࡈࡏࠢᅌ")) == bstack11l1ll_opy_ (u"ࠧࡺࡲࡶࡧࠥᅍ") and env.get(bstack11l1ll_opy_ (u"ࠨࡃࡊࡡࡑࡅࡒࡋࠢᅎ")) == bstack11l1ll_opy_ (u"ࠢࡤࡱࡧࡩࡸ࡮ࡩࡱࠤᅏ"):
        return {
            bstack11l1ll_opy_ (u"ࠣࡰࡤࡱࡪࠨᅐ"): bstack11l1ll_opy_ (u"ࠤࡆࡳࡩ࡫ࡳࡩ࡫ࡳࠦᅑ"),
            bstack11l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᅒ"): None,
            bstack11l1ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᅓ"): None,
            bstack11l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᅔ"): None
        }
    if env.get(bstack11l1ll_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅࡖࡆࡔࡃࡉࠤᅕ")) and env.get(bstack11l1ll_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡇࡔࡓࡍࡊࡖࠥᅖ")):
        return {
            bstack11l1ll_opy_ (u"ࠣࡰࡤࡱࡪࠨᅗ"): bstack11l1ll_opy_ (u"ࠤࡅ࡭ࡹࡨࡵࡤ࡭ࡨࡸࠧᅘ"),
            bstack11l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᅙ"): env.get(bstack11l1ll_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡈࡋࡗࡣࡍ࡚ࡔࡑࡡࡒࡖࡎࡍࡉࡏࠤᅚ")),
            bstack11l1ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᅛ"): None,
            bstack11l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᅜ"): env.get(bstack11l1ll_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᅝ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠣࡅࡌࠦᅞ")) == bstack11l1ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᅟ") and bstack1l1lll11l_opy_(env.get(bstack11l1ll_opy_ (u"ࠥࡈࡗࡕࡎࡆࠤᅠ"))):
        return {
            bstack11l1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᅡ"): bstack11l1ll_opy_ (u"ࠧࡊࡲࡰࡰࡨࠦᅢ"),
            bstack11l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᅣ"): env.get(bstack11l1ll_opy_ (u"ࠢࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡒࡉࡏࡍࠥᅤ")),
            bstack11l1ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᅥ"): None,
            bstack11l1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᅦ"): env.get(bstack11l1ll_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᅧ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠦࡈࡏࠢᅨ")) == bstack11l1ll_opy_ (u"ࠧࡺࡲࡶࡧࠥᅩ") and bstack1l1lll11l_opy_(env.get(bstack11l1ll_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࠤᅪ"))):
        return {
            bstack11l1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᅫ"): bstack11l1ll_opy_ (u"ࠣࡕࡨࡱࡦࡶࡨࡰࡴࡨࠦᅬ"),
            bstack11l1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᅭ"): env.get(bstack11l1ll_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡏࡓࡉࡄࡒࡎࡠࡁࡕࡋࡒࡒࡤ࡛ࡒࡍࠤᅮ")),
            bstack11l1ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᅯ"): env.get(bstack11l1ll_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᅰ")),
            bstack11l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᅱ"): env.get(bstack11l1ll_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡊࡆࠥᅲ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠣࡅࡌࠦᅳ")) == bstack11l1ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᅴ") and bstack1l1lll11l_opy_(env.get(bstack11l1ll_opy_ (u"ࠥࡋࡎ࡚ࡌࡂࡄࡢࡇࡎࠨᅵ"))):
        return {
            bstack11l1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᅶ"): bstack11l1ll_opy_ (u"ࠧࡍࡩࡵࡎࡤࡦࠧᅷ"),
            bstack11l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᅸ"): env.get(bstack11l1ll_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡖࡔࡏࠦᅹ")),
            bstack11l1ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᅺ"): env.get(bstack11l1ll_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᅻ")),
            bstack11l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᅼ"): env.get(bstack11l1ll_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡎࡊࠢᅽ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠧࡉࡉࠣᅾ")) == bstack11l1ll_opy_ (u"ࠨࡴࡳࡷࡨࠦᅿ") and bstack1l1lll11l_opy_(env.get(bstack11l1ll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࠥᆀ"))):
        return {
            bstack11l1ll_opy_ (u"ࠣࡰࡤࡱࡪࠨᆁ"): bstack11l1ll_opy_ (u"ࠤࡅࡹ࡮ࡲࡤ࡬࡫ࡷࡩࠧᆂ"),
            bstack11l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᆃ"): env.get(bstack11l1ll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᆄ")),
            bstack11l1ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᆅ"): env.get(bstack11l1ll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡏࡅࡇࡋࡌࠣᆆ")) or env.get(bstack11l1ll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡔࡁࡎࡇࠥᆇ")),
            bstack11l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᆈ"): env.get(bstack11l1ll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᆉ"))
        }
    if bstack1l1lll11l_opy_(env.get(bstack11l1ll_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧᆊ"))):
        return {
            bstack11l1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᆋ"): bstack11l1ll_opy_ (u"ࠧ࡜ࡩࡴࡷࡤࡰ࡙ࠥࡴࡶࡦ࡬ࡳ࡚ࠥࡥࡢ࡯ࠣࡗࡪࡸࡶࡪࡥࡨࡷࠧᆌ"),
            bstack11l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᆍ"): bstack11l1ll_opy_ (u"ࠢࡼࡿࡾࢁࠧᆎ").format(env.get(bstack11l1ll_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫᆏ")), env.get(bstack11l1ll_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࡉࡅࠩᆐ"))),
            bstack11l1ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᆑ"): env.get(bstack11l1ll_opy_ (u"ࠦࡘ࡟ࡓࡕࡇࡐࡣࡉࡋࡆࡊࡐࡌࡘࡎࡕࡎࡊࡆࠥᆒ")),
            bstack11l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᆓ"): env.get(bstack11l1ll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨᆔ"))
        }
    if bstack1l1lll11l_opy_(env.get(bstack11l1ll_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࠤᆕ"))):
        return {
            bstack11l1ll_opy_ (u"ࠣࡰࡤࡱࡪࠨᆖ"): bstack11l1ll_opy_ (u"ࠤࡄࡴࡵࡼࡥࡺࡱࡵࠦᆗ"),
            bstack11l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᆘ"): bstack11l1ll_opy_ (u"ࠦࢀࢃ࠯ࡱࡴࡲ࡮ࡪࡩࡴ࠰ࡽࢀ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠥᆙ").format(env.get(bstack11l1ll_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡖࡔࡏࠫᆚ")), env.get(bstack11l1ll_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡃࡆࡇࡔ࡛ࡎࡕࡡࡑࡅࡒࡋࠧᆛ")), env.get(bstack11l1ll_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡓࡖࡔࡐࡅࡄࡖࡢࡗࡑ࡛ࡇࠨᆜ")), env.get(bstack11l1ll_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬᆝ"))),
            bstack11l1ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᆞ"): env.get(bstack11l1ll_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᆟ")),
            bstack11l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᆠ"): env.get(bstack11l1ll_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᆡ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠨࡁ࡛ࡗࡕࡉࡤࡎࡔࡕࡒࡢ࡙ࡘࡋࡒࡠࡃࡊࡉࡓ࡚ࠢᆢ")) and env.get(bstack11l1ll_opy_ (u"ࠢࡕࡈࡢࡆ࡚ࡏࡌࡅࠤᆣ")):
        return {
            bstack11l1ll_opy_ (u"ࠣࡰࡤࡱࡪࠨᆤ"): bstack11l1ll_opy_ (u"ࠤࡄࡾࡺࡸࡥࠡࡅࡌࠦᆥ"),
            bstack11l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᆦ"): bstack11l1ll_opy_ (u"ࠦࢀࢃࡻࡾ࠱ࡢࡦࡺ࡯࡬ࡥ࠱ࡵࡩࡸࡻ࡬ࡵࡵࡂࡦࡺ࡯࡬ࡥࡋࡧࡁࢀࢃࠢᆧ").format(env.get(bstack11l1ll_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨᆨ")), env.get(bstack11l1ll_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࠫᆩ")), env.get(bstack11l1ll_opy_ (u"ࠧࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠧᆪ"))),
            bstack11l1ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᆫ"): env.get(bstack11l1ll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤᆬ")),
            bstack11l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᆭ"): env.get(bstack11l1ll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᆮ"))
        }
    if any([env.get(bstack11l1ll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᆯ")), env.get(bstack11l1ll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡕࡉࡘࡕࡌࡗࡇࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧᆰ")), env.get(bstack11l1ll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦᆱ"))]):
        return {
            bstack11l1ll_opy_ (u"ࠣࡰࡤࡱࡪࠨᆲ"): bstack11l1ll_opy_ (u"ࠤࡄ࡛ࡘࠦࡃࡰࡦࡨࡆࡺ࡯࡬ࡥࠤᆳ"),
            bstack11l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᆴ"): env.get(bstack11l1ll_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡑࡗࡅࡐࡎࡉ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᆵ")),
            bstack11l1ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᆶ"): env.get(bstack11l1ll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᆷ")),
            bstack11l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᆸ"): env.get(bstack11l1ll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᆹ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢᆺ")):
        return {
            bstack11l1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣᆻ"): bstack11l1ll_opy_ (u"ࠦࡇࡧ࡭ࡣࡱࡲࠦᆼ"),
            bstack11l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᆽ"): env.get(bstack11l1ll_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡗ࡫ࡳࡶ࡮ࡷࡷ࡚ࡸ࡬ࠣᆾ")),
            bstack11l1ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᆿ"): env.get(bstack11l1ll_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡵ࡫ࡳࡷࡺࡊࡰࡤࡑࡥࡲ࡫ࠢᇀ")),
            bstack11l1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᇁ"): env.get(bstack11l1ll_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣᇂ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࠧᇃ")) or env.get(bstack11l1ll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊࠢᇄ")):
        return {
            bstack11l1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇅ"): bstack11l1ll_opy_ (u"ࠢࡘࡧࡵࡧࡰ࡫ࡲࠣᇆ"),
            bstack11l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᇇ"): env.get(bstack11l1ll_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᇈ")),
            bstack11l1ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᇉ"): bstack11l1ll_opy_ (u"ࠦࡒࡧࡩ࡯ࠢࡓ࡭ࡵ࡫࡬ࡪࡰࡨࠦᇊ") if env.get(bstack11l1ll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊࠢᇋ")) else None,
            bstack11l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᇌ"): env.get(bstack11l1ll_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡉࡌࡘࡤࡉࡏࡎࡏࡌࡘࠧᇍ"))
        }
    if any([env.get(bstack11l1ll_opy_ (u"ࠣࡉࡆࡔࡤࡖࡒࡐࡌࡈࡇ࡙ࠨᇎ")), env.get(bstack11l1ll_opy_ (u"ࠤࡊࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥᇏ")), env.get(bstack11l1ll_opy_ (u"ࠥࡋࡔࡕࡇࡍࡇࡢࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥᇐ"))]):
        return {
            bstack11l1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᇑ"): bstack11l1ll_opy_ (u"ࠧࡍ࡯ࡰࡩ࡯ࡩࠥࡉ࡬ࡰࡷࡧࠦᇒ"),
            bstack11l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᇓ"): None,
            bstack11l1ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᇔ"): env.get(bstack11l1ll_opy_ (u"ࠣࡒࡕࡓࡏࡋࡃࡕࡡࡌࡈࠧᇕ")),
            bstack11l1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᇖ"): env.get(bstack11l1ll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᇗ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋࠢᇘ")):
        return {
            bstack11l1ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᇙ"): bstack11l1ll_opy_ (u"ࠨࡓࡩ࡫ࡳࡴࡦࡨ࡬ࡦࠤᇚ"),
            bstack11l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᇛ"): env.get(bstack11l1ll_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᇜ")),
            bstack11l1ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᇝ"): bstack11l1ll_opy_ (u"ࠥࡎࡴࡨࠠࠤࡽࢀࠦᇞ").format(env.get(bstack11l1ll_opy_ (u"ࠫࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠧᇟ"))) if env.get(bstack11l1ll_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠣᇠ")) else None,
            bstack11l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᇡ"): env.get(bstack11l1ll_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᇢ"))
        }
    if bstack1l1lll11l_opy_(env.get(bstack11l1ll_opy_ (u"ࠣࡐࡈࡘࡑࡏࡆ࡚ࠤᇣ"))):
        return {
            bstack11l1ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᇤ"): bstack11l1ll_opy_ (u"ࠥࡒࡪࡺ࡬ࡪࡨࡼࠦᇥ"),
            bstack11l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᇦ"): env.get(bstack11l1ll_opy_ (u"ࠧࡊࡅࡑࡎࡒ࡝ࡤ࡛ࡒࡍࠤᇧ")),
            bstack11l1ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᇨ"): env.get(bstack11l1ll_opy_ (u"ࠢࡔࡋࡗࡉࡤࡔࡁࡎࡇࠥᇩ")),
            bstack11l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᇪ"): env.get(bstack11l1ll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᇫ"))
        }
    if bstack1l1lll11l_opy_(env.get(bstack11l1ll_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡅࡈ࡚ࡉࡐࡐࡖࠦᇬ"))):
        return {
            bstack11l1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᇭ"): bstack11l1ll_opy_ (u"ࠧࡍࡩࡵࡊࡸࡦࠥࡇࡣࡵ࡫ࡲࡲࡸࠨᇮ"),
            bstack11l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᇯ"): bstack11l1ll_opy_ (u"ࠢࡼࡿ࠲ࡿࢂ࠵ࡡࡤࡶ࡬ࡳࡳࡹ࠯ࡳࡷࡱࡷ࠴ࢁࡽࠣᇰ").format(env.get(bstack11l1ll_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡕࡈࡖ࡛ࡋࡒࡠࡗࡕࡐࠬᇱ")), env.get(bstack11l1ll_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕࡉࡕࡕࡓࡊࡖࡒࡖ࡞࠭ᇲ")), env.get(bstack11l1ll_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠪᇳ"))),
            bstack11l1ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᇴ"): env.get(bstack11l1ll_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤ࡝ࡏࡓࡍࡉࡐࡔ࡝ࠢᇵ")),
            bstack11l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᇶ"): env.get(bstack11l1ll_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡗࡑࡣࡎࡊࠢᇷ"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠣࡅࡌࠦᇸ")) == bstack11l1ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᇹ") and env.get(bstack11l1ll_opy_ (u"࡚ࠥࡊࡘࡃࡆࡎࠥᇺ")) == bstack11l1ll_opy_ (u"ࠦ࠶ࠨᇻ"):
        return {
            bstack11l1ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᇼ"): bstack11l1ll_opy_ (u"ࠨࡖࡦࡴࡦࡩࡱࠨᇽ"),
            bstack11l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᇾ"): bstack11l1ll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࡽࢀࠦᇿ").format(env.get(bstack11l1ll_opy_ (u"࡙ࠩࡉࡗࡉࡅࡍࡡࡘࡖࡑ࠭ሀ"))),
            bstack11l1ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧሁ"): None,
            bstack11l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥሂ"): None,
        }
    if env.get(bstack11l1ll_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡗࡇࡕࡗࡎࡕࡎࠣሃ")):
        return {
            bstack11l1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦሄ"): bstack11l1ll_opy_ (u"ࠢࡕࡧࡤࡱࡨ࡯ࡴࡺࠤህ"),
            bstack11l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦሆ"): None,
            bstack11l1ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦሇ"): env.get(bstack11l1ll_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡎࡂࡏࡈࠦለ")),
            bstack11l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥሉ"): env.get(bstack11l1ll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦሊ"))
        }
    if any([env.get(bstack11l1ll_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࠤላ")), env.get(bstack11l1ll_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡗࡒࠢሌ")), env.get(bstack11l1ll_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚࡙ࡅࡓࡐࡄࡑࡊࠨል")), env.get(bstack11l1ll_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡚ࡅࡂࡏࠥሎ"))]):
        return {
            bstack11l1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣሏ"): bstack11l1ll_opy_ (u"ࠦࡈࡵ࡮ࡤࡱࡸࡶࡸ࡫ࠢሐ"),
            bstack11l1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣሑ"): None,
            bstack11l1ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣሒ"): env.get(bstack11l1ll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣሓ")) or None,
            bstack11l1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢሔ"): env.get(bstack11l1ll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦሕ"), 0)
        }
    if env.get(bstack11l1ll_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣሖ")):
        return {
            bstack11l1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤሗ"): bstack11l1ll_opy_ (u"ࠧࡍ࡯ࡄࡆࠥመ"),
            bstack11l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤሙ"): None,
            bstack11l1ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤሚ"): env.get(bstack11l1ll_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨማ")),
            bstack11l1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣሜ"): env.get(bstack11l1ll_opy_ (u"ࠥࡋࡔࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡅࡒ࡙ࡓ࡚ࡅࡓࠤም"))
        }
    if env.get(bstack11l1ll_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤሞ")):
        return {
            bstack11l1ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥሟ"): bstack11l1ll_opy_ (u"ࠨࡃࡰࡦࡨࡊࡷ࡫ࡳࡩࠤሠ"),
            bstack11l1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥሡ"): env.get(bstack11l1ll_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢሢ")),
            bstack11l1ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦሣ"): env.get(bstack11l1ll_opy_ (u"ࠥࡇࡋࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨሤ")),
            bstack11l1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥሥ"): env.get(bstack11l1ll_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥሦ"))
        }
    return {bstack11l1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧሧ"): None}
def get_host_info():
    return {
        bstack11l1ll_opy_ (u"ࠢࡩࡱࡶࡸࡳࡧ࡭ࡦࠤረ"): platform.node(),
        bstack11l1ll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥሩ"): platform.system(),
        bstack11l1ll_opy_ (u"ࠤࡷࡽࡵ࡫ࠢሪ"): platform.machine(),
        bstack11l1ll_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦራ"): platform.version(),
        bstack11l1ll_opy_ (u"ࠦࡦࡸࡣࡩࠤሬ"): platform.architecture()[0]
    }
def bstack1ll1lllll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l1l1lll1_opy_():
    if bstack1ll1l11ll1_opy_.get_property(bstack11l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ር")):
        return bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬሮ")
    return bstack11l1ll_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࡠࡩࡵ࡭ࡩ࠭ሯ")
def bstack11l11ll1ll_opy_(driver):
    info = {
        bstack11l1ll_opy_ (u"ࠨࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧሰ"): driver.capabilities,
        bstack11l1ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭ሱ"): driver.session_id,
        bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫሲ"): driver.capabilities.get(bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩሳ"), None),
        bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧሴ"): driver.capabilities.get(bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧስ"), None),
        bstack11l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩሶ"): driver.capabilities.get(bstack11l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧሷ"), None),
    }
    if bstack11l1l1lll1_opy_() == bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨሸ"):
        info[bstack11l1ll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫሹ")] = bstack11l1ll_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪሺ") if bstack11111l11l_opy_() else bstack11l1ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧሻ")
    return info
def bstack11111l11l_opy_():
    if bstack1ll1l11ll1_opy_.get_property(bstack11l1ll_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬሼ")):
        return True
    if bstack1l1lll11l_opy_(os.environ.get(bstack11l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨሽ"), None)):
        return True
    return False
def bstack1lll1l111l_opy_(bstack11l1l11l1l_opy_, url, data, config):
    headers = config.get(bstack11l1ll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩሾ"), None)
    proxies = bstack11ll1lll_opy_(config, url)
    auth = config.get(bstack11l1ll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧሿ"), None)
    response = requests.request(
            bstack11l1l11l1l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l1lll1ll1_opy_(bstack11ll1ll11_opy_, size):
    bstack1l11llll1_opy_ = []
    while len(bstack11ll1ll11_opy_) > size:
        bstack111lll11_opy_ = bstack11ll1ll11_opy_[:size]
        bstack1l11llll1_opy_.append(bstack111lll11_opy_)
        bstack11ll1ll11_opy_ = bstack11ll1ll11_opy_[size:]
    bstack1l11llll1_opy_.append(bstack11ll1ll11_opy_)
    return bstack1l11llll1_opy_
def bstack11ll1111ll_opy_(message, bstack11l1l1l111_opy_=False):
    os.write(1, bytes(message, bstack11l1ll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩቀ")))
    os.write(1, bytes(bstack11l1ll_opy_ (u"ࠫࡡࡴࠧቁ"), bstack11l1ll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫቂ")))
    if bstack11l1l1l111_opy_:
        with open(bstack11l1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡯࠲࠳ࡼ࠱ࠬቃ") + os.environ[bstack11l1ll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ቄ")] + bstack11l1ll_opy_ (u"ࠨ࠰࡯ࡳ࡬࠭ቅ"), bstack11l1ll_opy_ (u"ࠩࡤࠫቆ")) as f:
            f.write(message + bstack11l1ll_opy_ (u"ࠪࡠࡳ࠭ቇ"))
def bstack11l1ll11l1_opy_():
    return os.environ[bstack11l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧቈ")].lower() == bstack11l1ll_opy_ (u"ࠬࡺࡲࡶࡧࠪ቉")
def bstack1l11l11l_opy_(bstack11l1ll1ll1_opy_):
    return bstack11l1ll_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬቊ").format(bstack11ll111lll_opy_, bstack11l1ll1ll1_opy_)
def bstack11ll1l11_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack11l1ll_opy_ (u"࡛ࠧࠩቋ")
def bstack11l1l1l1l1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11l1ll_opy_ (u"ࠨ࡜ࠪቌ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11l1ll_opy_ (u"ࠩ࡝ࠫቍ")))).total_seconds() * 1000
def bstack11l1l1l11l_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack11l1ll_opy_ (u"ࠪ࡞ࠬ቎")
def bstack11l11ll11l_opy_(bstack11l1l111ll_opy_):
    date_format = bstack11l1ll_opy_ (u"ࠫࠪ࡟ࠥ࡮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠩ቏")
    bstack11l1l11111_opy_ = datetime.datetime.strptime(bstack11l1l111ll_opy_, date_format)
    return bstack11l1l11111_opy_.isoformat() + bstack11l1ll_opy_ (u"ࠬࡠࠧቐ")
def bstack11l1ll1l1l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11l1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ቑ")
    else:
        return bstack11l1ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧቒ")
def bstack1l1lll11l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11l1ll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ቓ")
def bstack11l1lll1l1_opy_(val):
    return val.__str__().lower() == bstack11l1ll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨቔ")
def bstack1l11l11lll_opy_(bstack11l11ll1l1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l11ll1l1_opy_ as e:
                print(bstack11l1ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥቕ").format(func.__name__, bstack11l11ll1l1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l1ll1l11_opy_(bstack11l1l1111l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l1l1111l_opy_(cls, *args, **kwargs)
            except bstack11l11ll1l1_opy_ as e:
                print(bstack11l1ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦቖ").format(bstack11l1l1111l_opy_.__name__, bstack11l11ll1l1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l1ll1l11_opy_
    else:
        return decorator
def bstack1l1ll1l1l1_opy_(bstack11lllll11l_opy_):
    if bstack11l1ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ቗") in bstack11lllll11l_opy_ and bstack11l1lll1l1_opy_(bstack11lllll11l_opy_[bstack11l1ll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪቘ")]):
        return False
    if bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ቙") in bstack11lllll11l_opy_ and bstack11l1lll1l1_opy_(bstack11lllll11l_opy_[bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪቚ")]):
        return False
    return True
def bstack11l11lll_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1l1111111_opy_(hub_url):
    if bstack11l1ll1l1_opy_() <= version.parse(bstack11l1ll_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩቛ")):
        if hub_url != bstack11l1ll_opy_ (u"ࠪࠫቜ"):
            return bstack11l1ll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧቝ") + hub_url + bstack11l1ll_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤ቞")
        return bstack1lllll11_opy_
    if hub_url != bstack11l1ll_opy_ (u"࠭ࠧ቟"):
        return bstack11l1ll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤበ") + hub_url + bstack11l1ll_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤቡ")
    return bstack1l1l1111_opy_
def bstack11l1lllll1_opy_():
    return isinstance(os.getenv(bstack11l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨቢ")), str)
def bstack1ll11ll1l1_opy_(url):
    return urlparse(url).hostname
def bstack111l1l11_opy_(hostname):
    for bstack1l1l111l1_opy_ in bstack1111l111_opy_:
        regex = re.compile(bstack1l1l111l1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1l111l1_opy_(bstack11l11lll1l_opy_, file_name, logger):
    bstack1lll1lll1l_opy_ = os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠪࢂࠬባ")), bstack11l11lll1l_opy_)
    try:
        if not os.path.exists(bstack1lll1lll1l_opy_):
            os.makedirs(bstack1lll1lll1l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠫࢃ࠭ቤ")), bstack11l11lll1l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11l1ll_opy_ (u"ࠬࡽࠧብ")):
                pass
            with open(file_path, bstack11l1ll_opy_ (u"ࠨࡷࠬࠤቦ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack11l11l111_opy_.format(str(e)))
def bstack11l1l1ll11_opy_(file_name, key, value, logger):
    file_path = bstack11l1l111l1_opy_(bstack11l1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧቧ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l1111lll_opy_ = json.load(open(file_path, bstack11l1ll_opy_ (u"ࠨࡴࡥࠫቨ")))
        else:
            bstack1l1111lll_opy_ = {}
        bstack1l1111lll_opy_[key] = value
        with open(file_path, bstack11l1ll_opy_ (u"ࠤࡺ࠯ࠧቩ")) as outfile:
            json.dump(bstack1l1111lll_opy_, outfile)
def bstack11l11ll1_opy_(file_name, logger):
    file_path = bstack11l1l111l1_opy_(bstack11l1ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪቪ"), file_name, logger)
    bstack1l1111lll_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11l1ll_opy_ (u"ࠫࡷ࠭ቫ")) as bstack1lll11l1ll_opy_:
            bstack1l1111lll_opy_ = json.load(bstack1lll11l1ll_opy_)
    return bstack1l1111lll_opy_
def bstack111111l1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11l1ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫࠺ࠡࠩቬ") + file_path + bstack11l1ll_opy_ (u"࠭ࠠࠨቭ") + str(e))
def bstack11l1ll1l1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11l1ll_opy_ (u"ࠢ࠽ࡐࡒࡘࡘࡋࡔ࠿ࠤቮ")
def bstack1ll1111lll_opy_(config):
    if bstack11l1ll_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧቯ") in config:
        del (config[bstack11l1ll_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨተ")])
        return False
    if bstack11l1ll1l1_opy_() < version.parse(bstack11l1ll_opy_ (u"ࠪ࠷࠳࠺࠮࠱ࠩቱ")):
        return False
    if bstack11l1ll1l1_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪቲ")):
        return True
    if bstack11l1ll_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬታ") in config and config[bstack11l1ll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ቴ")] is False:
        return False
    else:
        return True
def bstack1lll1l1ll1_opy_(args_list, bstack11l11lllll_opy_):
    index = -1
    for value in bstack11l11lllll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l11l1ll1l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l11l1ll1l_opy_ = bstack1l11l1ll1l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11l1ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧት"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11l1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨቶ"), exception=exception)
    def bstack11llll1111_opy_(self):
        if self.result != bstack11l1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩቷ"):
            return None
        if bstack11l1ll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨቸ") in self.exception_type:
            return bstack11l1ll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧቹ")
        return bstack11l1ll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨቺ")
    def bstack11ll111ll1_opy_(self):
        if self.result != bstack11l1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ቻ"):
            return None
        if self.bstack1l11l1ll1l_opy_:
            return self.bstack1l11l1ll1l_opy_
        return bstack11l11l1lll_opy_(self.exception)
def bstack11l11l1lll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11ll111l1l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack111l1lll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11ll111ll_opy_(config, logger):
    try:
        import playwright
        bstack11l11l1l1l_opy_ = playwright.__file__
        bstack11l1llll11_opy_ = os.path.split(bstack11l11l1l1l_opy_)
        bstack11l1l11ll1_opy_ = bstack11l1llll11_opy_[0] + bstack11l1ll_opy_ (u"ࠧ࠰ࡦࡵ࡭ࡻ࡫ࡲ࠰ࡲࡤࡧࡰࡧࡧࡦ࠱࡯࡭ࡧ࠵ࡣ࡭࡫࠲ࡧࡱ࡯࠮࡫ࡵࠪቼ")
        os.environ[bstack11l1ll_opy_ (u"ࠨࡉࡏࡓࡇࡇࡌࡠࡃࡊࡉࡓ࡚࡟ࡉࡖࡗࡔࡤࡖࡒࡐ࡚࡜ࠫች")] = bstack1111l1l11_opy_(config)
        with open(bstack11l1l11ll1_opy_, bstack11l1ll_opy_ (u"ࠩࡵࠫቾ")) as f:
            bstack1ll1lll1l_opy_ = f.read()
            bstack11l1lll111_opy_ = bstack11l1ll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩቿ")
            bstack11l1llll1l_opy_ = bstack1ll1lll1l_opy_.find(bstack11l1lll111_opy_)
            if bstack11l1llll1l_opy_ == -1:
              process = subprocess.Popen(bstack11l1ll_opy_ (u"ࠦࡳࡶ࡭ࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠣኀ"), shell=True, cwd=bstack11l1llll11_opy_[0])
              process.wait()
              bstack11l1l11lll_opy_ = bstack11l1ll_opy_ (u"ࠬࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶࠥ࠿ࠬኁ")
              bstack11l1llllll_opy_ = bstack11l1ll_opy_ (u"ࠨࠢࠣࠢ࡟ࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴ࡝ࠤ࠾ࠤࡨࡵ࡮ࡴࡶࠣࡿࠥࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠡࡿࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮ࠧࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹ࠭ࠩ࠼ࠢ࡬ࡪࠥ࠮ࡰࡳࡱࡦࡩࡸࡹ࠮ࡦࡰࡹ࠲ࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠩࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠬ࠮ࡁࠠࠣࠤࠥኂ")
              bstack11l1ll11ll_opy_ = bstack1ll1lll1l_opy_.replace(bstack11l1l11lll_opy_, bstack11l1llllll_opy_)
              with open(bstack11l1l11ll1_opy_, bstack11l1ll_opy_ (u"ࠧࡸࠩኃ")) as f:
                f.write(bstack11l1ll11ll_opy_)
    except Exception as e:
        logger.error(bstack1l111111_opy_.format(str(e)))
def bstack1l1lll11l1_opy_():
  try:
    bstack11l1lll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨኄ"))
    bstack11l1l1ll1l_opy_ = []
    if os.path.exists(bstack11l1lll1ll_opy_):
      with open(bstack11l1lll1ll_opy_) as f:
        bstack11l1l1ll1l_opy_ = json.load(f)
      os.remove(bstack11l1lll1ll_opy_)
    return bstack11l1l1ll1l_opy_
  except:
    pass
  return []
def bstack11l11ll1l_opy_(bstack1l1l11l1l_opy_):
  try:
    bstack11l1l1ll1l_opy_ = []
    bstack11l1lll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩኅ"))
    if os.path.exists(bstack11l1lll1ll_opy_):
      with open(bstack11l1lll1ll_opy_) as f:
        bstack11l1l1ll1l_opy_ = json.load(f)
    bstack11l1l1ll1l_opy_.append(bstack1l1l11l1l_opy_)
    with open(bstack11l1lll1ll_opy_, bstack11l1ll_opy_ (u"ࠪࡻࠬኆ")) as f:
        json.dump(bstack11l1l1ll1l_opy_, f)
  except:
    pass
def bstack11llll11l_opy_(logger, bstack11ll1111l1_opy_ = False):
  try:
    test_name = os.environ.get(bstack11l1ll_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧኇ"), bstack11l1ll_opy_ (u"ࠬ࠭ኈ"))
    if test_name == bstack11l1ll_opy_ (u"࠭ࠧ኉"):
        test_name = threading.current_thread().__dict__.get(bstack11l1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࡂࡥࡦࡢࡸࡪࡹࡴࡠࡰࡤࡱࡪ࠭ኊ"), bstack11l1ll_opy_ (u"ࠨࠩኋ"))
    bstack11l11ll111_opy_ = bstack11l1ll_opy_ (u"ࠩ࠯ࠤࠬኌ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11ll1111l1_opy_:
        bstack1l1ll1ll_opy_ = os.environ.get(bstack11l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪኍ"), bstack11l1ll_opy_ (u"ࠫ࠵࠭኎"))
        bstack1l1l11l1_opy_ = {bstack11l1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ኏"): test_name, bstack11l1ll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬነ"): bstack11l11ll111_opy_, bstack11l1ll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ኑ"): bstack1l1ll1ll_opy_}
        bstack11l1l1llll_opy_ = []
        bstack11l1ll1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧኒ"))
        if os.path.exists(bstack11l1ll1lll_opy_):
            with open(bstack11l1ll1lll_opy_) as f:
                bstack11l1l1llll_opy_ = json.load(f)
        bstack11l1l1llll_opy_.append(bstack1l1l11l1_opy_)
        with open(bstack11l1ll1lll_opy_, bstack11l1ll_opy_ (u"ࠩࡺࠫና")) as f:
            json.dump(bstack11l1l1llll_opy_, f)
    else:
        bstack1l1l11l1_opy_ = {bstack11l1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨኔ"): test_name, bstack11l1ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪን"): bstack11l11ll111_opy_, bstack11l1ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫኖ"): str(multiprocessing.current_process().name)}
        if bstack11l1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪኗ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l1l11l1_opy_)
  except Exception as e:
      logger.warn(bstack11l1ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡳࡽࡹ࡫ࡳࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦኘ").format(e))
def bstack1ll11ll1_opy_(error_message, test_name, index, logger):
  try:
    bstack11l11llll1_opy_ = []
    bstack1l1l11l1_opy_ = {bstack11l1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ኙ"): test_name, bstack11l1ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨኚ"): error_message, bstack11l1ll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩኛ"): index}
    bstack11l1ll1111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬኜ"))
    if os.path.exists(bstack11l1ll1111_opy_):
        with open(bstack11l1ll1111_opy_) as f:
            bstack11l11llll1_opy_ = json.load(f)
    bstack11l11llll1_opy_.append(bstack1l1l11l1_opy_)
    with open(bstack11l1ll1111_opy_, bstack11l1ll_opy_ (u"ࠬࡽࠧኝ")) as f:
        json.dump(bstack11l11llll1_opy_, f)
  except Exception as e:
    logger.warn(bstack11l1ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡴࡲࡦࡴࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤኞ").format(e))
def bstack1ll111l1l_opy_(bstack11lll11l1_opy_, name, logger):
  try:
    bstack1l1l11l1_opy_ = {bstack11l1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬኟ"): name, bstack11l1ll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧአ"): bstack11lll11l1_opy_, bstack11l1ll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨኡ"): str(threading.current_thread()._name)}
    return bstack1l1l11l1_opy_
  except Exception as e:
    logger.warn(bstack11l1ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡨࡥࡩࡣࡹࡩࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢኢ").format(e))
  return
def bstack1llll11111_opy_(framework):
    if framework.lower() == bstack11l1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫኣ"):
        return bstack1l1lll11_opy_.version()
    elif framework.lower() == bstack11l1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫኤ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11l1ll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭እ"):
        import behave
        return behave.__version__
    else:
        return bstack11l1ll_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࠨኦ")