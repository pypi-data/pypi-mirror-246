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
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack1111111l1_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack111l1l1l1_opy_ import bstack1l1l1ll111_opy_
import time
import requests
def bstack1ll1l111l1_opy_():
  global CONFIG
  headers = {
        bstack1lllll1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1lllll1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1ll11l111_opy_(CONFIG, bstack1l1l1l11l_opy_)
  try:
    response = requests.get(bstack1l1l1l11l_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l111ll1_opy_ = response.json()[bstack1lllll1l_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1111l111_opy_.format(response.json()))
      return bstack1l111ll1_opy_
    else:
      logger.debug(bstack111l1lll1_opy_.format(bstack1lllll1l_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack111l1lll1_opy_.format(e))
def bstack1llll1l1l1_opy_(hub_url):
  global CONFIG
  url = bstack1lllll1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1lllll1l_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1lllll1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1lllll1l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1ll11l111_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1lll111l11_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11l1l1l1l_opy_.format(hub_url, e))
def bstack1llll1111l_opy_():
  try:
    global bstack11l111l1_opy_
    bstack1l111ll1_opy_ = bstack1ll1l111l1_opy_()
    bstack111l111l_opy_ = []
    results = []
    for bstack1lll1l1ll1_opy_ in bstack1l111ll1_opy_:
      bstack111l111l_opy_.append(bstack1ll11ll11l_opy_(target=bstack1llll1l1l1_opy_,args=(bstack1lll1l1ll1_opy_,)))
    for t in bstack111l111l_opy_:
      t.start()
    for t in bstack111l111l_opy_:
      results.append(t.join())
    bstack1lllll1l1_opy_ = {}
    for item in results:
      hub_url = item[bstack1lllll1l_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack1lllll1l_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1lllll1l1_opy_[hub_url] = latency
    bstack1l1ll1ll11_opy_ = min(bstack1lllll1l1_opy_, key= lambda x: bstack1lllll1l1_opy_[x])
    bstack11l111l1_opy_ = bstack1l1ll1ll11_opy_
    logger.debug(bstack1lllll1lll_opy_.format(bstack1l1ll1ll11_opy_))
  except Exception as e:
    logger.debug(bstack111ll1l1_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils.config import Config
from bstack_utils.helper import bstack1lll1ll1_opy_, bstack11lll1lll_opy_, bstack11l1l11l1_opy_, bstack1l1l1l1ll_opy_, Notset, bstack1l1l11l1l1_opy_, \
  bstack11l11l1l_opy_, bstack11lll111l_opy_, bstack1l1ll11l1l_opy_, bstack1lll1l1l11_opy_, bstack1llll1l11l_opy_, bstack1l1ll1111_opy_, bstack1l1l1lllll_opy_, \
  bstack1ll1llll_opy_, bstack1l111lll_opy_, bstack1llllllll1_opy_, bstack1l1l1l11_opy_, bstack1l1llll11_opy_, bstack11ll1llll_opy_, \
  bstack1lll1lll11_opy_, bstack11l1l1ll_opy_
from bstack_utils.bstack1ll1l11l1_opy_ import bstack11lllllll_opy_
from bstack_utils.bstack1l1ll1l11l_opy_ import bstack11lll1ll1_opy_, bstack111lll111_opy_
from bstack_utils.bstack11l111ll1_opy_ import bstack1l1ll111ll_opy_
from bstack_utils.proxy import bstack11111ll1l_opy_, bstack1ll11l111_opy_, bstack1lll11ll11_opy_, bstack1l11l111l_opy_
import bstack_utils.bstack1l1lll1l_opy_ as bstack1l1ll11l1_opy_
from browserstack_sdk.bstack1llllll111_opy_ import *
from browserstack_sdk.bstack111lll11l_opy_ import *
from bstack_utils.bstack11llll1ll_opy_ import bstack11l1111l_opy_
bstack11111lll_opy_ = bstack1lllll1l_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack1lll1llll1_opy_ = bstack1lllll1l_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack1l11l11l1_opy_ = None
CONFIG = {}
bstack1111ll1l1_opy_ = {}
bstack1ll11l11l_opy_ = {}
bstack111llll1l_opy_ = None
bstack1l11111ll_opy_ = None
bstack1ll1l1l11l_opy_ = None
bstack1llll11l_opy_ = -1
bstack1llll11111_opy_ = 0
bstack11ll11l1_opy_ = bstack1l1l1ll1_opy_
bstack1l1lll11l_opy_ = 1
bstack1l11l1l1_opy_ = False
bstack1llll1l1_opy_ = False
bstack1ll1lllll1_opy_ = bstack1lllll1l_opy_ (u"ࠨࠩࢂ")
bstack1l1l1l1lll_opy_ = bstack1lllll1l_opy_ (u"ࠩࠪࢃ")
bstack11ll11ll1_opy_ = False
bstack1ll11lll11_opy_ = True
bstack1l1llll11l_opy_ = bstack1lllll1l_opy_ (u"ࠪࠫࢄ")
bstack1l1llll111_opy_ = []
bstack11l111l1_opy_ = bstack1lllll1l_opy_ (u"ࠫࠬࢅ")
bstack11l111ll_opy_ = False
bstack1lll11l1_opy_ = None
bstack1l11l111_opy_ = None
bstack1l1ll1l1ll_opy_ = None
bstack1l1lll1ll_opy_ = -1
bstack1l1llllll_opy_ = os.path.join(os.path.expanduser(bstack1lllll1l_opy_ (u"ࠬࢄࠧࢆ")), bstack1lllll1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstack1lllll1l_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack1ll1l1l1l1_opy_ = 0
bstack1ll111l11l_opy_ = []
bstack1l1ll11111_opy_ = []
bstack1l1l1111l_opy_ = []
bstack111l1111_opy_ = []
bstack11111l1l_opy_ = bstack1lllll1l_opy_ (u"ࠨࠩࢉ")
bstack1l1l11l1_opy_ = bstack1lllll1l_opy_ (u"ࠩࠪࢊ")
bstack1l1l1ll1ll_opy_ = False
bstack1lll1111l1_opy_ = False
bstack1lllll1111_opy_ = {}
bstack1lllll111_opy_ = None
bstack11111ll11_opy_ = None
bstack1lll1l11l1_opy_ = None
bstack1l1l1111_opy_ = None
bstack1lll1l111_opy_ = None
bstack1lllll11l1_opy_ = None
bstack1l1l1ll1l1_opy_ = None
bstack1lllllll1l_opy_ = None
bstack1ll11l11ll_opy_ = None
bstack1ll1l1111l_opy_ = None
bstack1lll11l1l1_opy_ = None
bstack1111l1111_opy_ = None
bstack111l111ll_opy_ = None
bstack1ll1111lll_opy_ = None
bstack1l1lll11ll_opy_ = None
bstack1ll11l1ll_opy_ = None
bstack1l1l1l1ll1_opy_ = None
bstack1111111l_opy_ = None
bstack1ll111l11_opy_ = None
bstack1l1l11111_opy_ = None
bstack1ll1l1l1l_opy_ = None
bstack1l1111ll1_opy_ = bstack1lllll1l_opy_ (u"ࠥࠦࢋ")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack11ll11l1_opy_,
                    format=bstack1lllll1l_opy_ (u"ࠫࡡࡴࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩࢌ"),
                    datefmt=bstack1lllll1l_opy_ (u"ࠬࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧࢍ"),
                    stream=sys.stdout)
bstack1ll1ll1l1_opy_ = Config.get_instance()
percy = bstack1l1lll1l1l_opy_()
bstack1111l1ll1_opy_ = bstack1l1l1ll111_opy_()
def bstack1ll111111_opy_():
  global CONFIG
  global bstack11ll11l1_opy_
  if bstack1lllll1l_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨࢎ") in CONFIG:
    bstack11ll11l1_opy_ = bstack11l11l1ll_opy_[CONFIG[bstack1lllll1l_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ࢏")]]
    logging.getLogger().setLevel(bstack11ll11l1_opy_)
def bstack11ll1lll_opy_():
  global CONFIG
  global bstack1l1l1ll1ll_opy_
  global bstack1ll1ll1l1_opy_
  bstack1ll1l1ll11_opy_ = bstack1l111111l_opy_(CONFIG)
  if (bstack1lllll1l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ࢐") in bstack1ll1l1ll11_opy_ and str(bstack1ll1l1ll11_opy_[bstack1lllll1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ࢑")]).lower() == bstack1lllll1l_opy_ (u"ࠪࡸࡷࡻࡥࠨ࢒")):
    bstack1l1l1ll1ll_opy_ = True
  bstack1ll1ll1l1_opy_.bstack1l1l1l1l1_opy_(bstack1ll1l1ll11_opy_.get(bstack1lllll1l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࢓"), False))
def bstack11lllll1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l11ll1l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1lll1l11ll_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1lllll1l_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࢔") == args[i].lower() or bstack1lllll1l_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࢕") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l1llll11l_opy_
      bstack1l1llll11l_opy_ += bstack1lllll1l_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ࢖") + path
      return path
  return None
bstack1lll1ll1ll_opy_ = re.compile(bstack1lllll1l_opy_ (u"ࡳࠤ࠱࠮ࡄࡢࠤࡼࠪ࠱࠮ࡄ࠯ࡽ࠯ࠬࡂࠦࢗ"))
def bstack1l111l111_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1lll1ll1ll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1lllll1l_opy_ (u"ࠤࠧࡿࠧ࢘") + group + bstack1lllll1l_opy_ (u"ࠥࢁ࢙ࠧ"), os.environ.get(group))
  return value
def bstack1l1l11ll11_opy_():
  bstack1l11l1l1l_opy_ = bstack1lll1l11ll_opy_()
  if bstack1l11l1l1l_opy_ and os.path.exists(os.path.abspath(bstack1l11l1l1l_opy_)):
    fileName = bstack1l11l1l1l_opy_
  if bstack1lllll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࢚") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1lllll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࢛ࠩ")])) and not bstack1lllll1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨ࢜") in locals():
    fileName = os.environ[bstack1lllll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢝")]
  if bstack1lllll1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪ࢞") in locals():
    bstack1ll11_opy_ = os.path.abspath(fileName)
  else:
    bstack1ll11_opy_ = bstack1lllll1l_opy_ (u"ࠩࠪ࢟")
  bstack1ll1l1ll_opy_ = os.getcwd()
  bstack1lll1l11_opy_ = bstack1lllll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ࢠ")
  bstack1l1ll1ll_opy_ = bstack1lllll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨࢡ")
  while (not os.path.exists(bstack1ll11_opy_)) and bstack1ll1l1ll_opy_ != bstack1lllll1l_opy_ (u"ࠧࠨࢢ"):
    bstack1ll11_opy_ = os.path.join(bstack1ll1l1ll_opy_, bstack1lll1l11_opy_)
    if not os.path.exists(bstack1ll11_opy_):
      bstack1ll11_opy_ = os.path.join(bstack1ll1l1ll_opy_, bstack1l1ll1ll_opy_)
    if bstack1ll1l1ll_opy_ != os.path.dirname(bstack1ll1l1ll_opy_):
      bstack1ll1l1ll_opy_ = os.path.dirname(bstack1ll1l1ll_opy_)
    else:
      bstack1ll1l1ll_opy_ = bstack1lllll1l_opy_ (u"ࠨࠢࢣ")
  if not os.path.exists(bstack1ll11_opy_):
    bstack1ll1l11l11_opy_(
      bstack1l1l11ll1_opy_.format(os.getcwd()))
  try:
    with open(bstack1ll11_opy_, bstack1lllll1l_opy_ (u"ࠧࡳࠩࢤ")) as stream:
      yaml.add_implicit_resolver(bstack1lllll1l_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࢥ"), bstack1lll1ll1ll_opy_)
      yaml.add_constructor(bstack1lllll1l_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࢦ"), bstack1l111l111_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1ll11_opy_, bstack1lllll1l_opy_ (u"ࠪࡶࠬࢧ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1ll1l11l11_opy_(bstack11111ll1_opy_.format(str(exc)))
def bstack11lll111_opy_(config):
  bstack1lll1l1111_opy_ = bstack1ll111l1ll_opy_(config)
  for option in list(bstack1lll1l1111_opy_):
    if option.lower() in bstack1ll11l11_opy_ and option != bstack1ll11l11_opy_[option.lower()]:
      bstack1lll1l1111_opy_[bstack1ll11l11_opy_[option.lower()]] = bstack1lll1l1111_opy_[option]
      del bstack1lll1l1111_opy_[option]
  return config
def bstack1l11lll1_opy_():
  global bstack1ll11l11l_opy_
  for key, bstack11ll1l11_opy_ in bstack1l1lllll1_opy_.items():
    if isinstance(bstack11ll1l11_opy_, list):
      for var in bstack11ll1l11_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1ll11l11l_opy_[key] = os.environ[var]
          break
    elif bstack11ll1l11_opy_ in os.environ and os.environ[bstack11ll1l11_opy_] and str(os.environ[bstack11ll1l11_opy_]).strip():
      bstack1ll11l11l_opy_[key] = os.environ[bstack11ll1l11_opy_]
  if bstack1lllll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ") in os.environ:
    bstack1ll11l11l_opy_[bstack1lllll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢩ")] = {}
    bstack1ll11l11l_opy_[bstack1lllll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")][bstack1lllll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢫ")] = os.environ[bstack1lllll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࢬ")]
def bstack1lll1lll1l_opy_():
  global bstack1111ll1l1_opy_
  global bstack1l1llll11l_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1lllll1l_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢭ").lower() == val.lower():
      bstack1111ll1l1_opy_[bstack1lllll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢮ")] = {}
      bstack1111ll1l1_opy_[bstack1lllll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢯ")][bstack1lllll1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack11l1l111_opy_ in bstack1111l1lll_opy_.items():
    if isinstance(bstack11l1l111_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11l1l111_opy_:
          if idx < len(sys.argv) and bstack1lllll1l_opy_ (u"࠭࠭࠮ࠩࢱ") + var.lower() == val.lower() and not key in bstack1111ll1l1_opy_:
            bstack1111ll1l1_opy_[key] = sys.argv[idx + 1]
            bstack1l1llll11l_opy_ += bstack1lllll1l_opy_ (u"ࠧࠡ࠯࠰ࠫࢲ") + var + bstack1lllll1l_opy_ (u"ࠨࠢࠪࢳ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1lllll1l_opy_ (u"ࠩ࠰࠱ࠬࢴ") + bstack11l1l111_opy_.lower() == val.lower() and not key in bstack1111ll1l1_opy_:
          bstack1111ll1l1_opy_[key] = sys.argv[idx + 1]
          bstack1l1llll11l_opy_ += bstack1lllll1l_opy_ (u"ࠪࠤ࠲࠳ࠧࢵ") + bstack11l1l111_opy_ + bstack1lllll1l_opy_ (u"ࠫࠥ࠭ࢶ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1l1lll1l11_opy_(config):
  bstack1ll11lll_opy_ = config.keys()
  for bstack1l1l11l1ll_opy_, bstack11ll1l111_opy_ in bstack1l1lllll1l_opy_.items():
    if bstack11ll1l111_opy_ in bstack1ll11lll_opy_:
      config[bstack1l1l11l1ll_opy_] = config[bstack11ll1l111_opy_]
      del config[bstack11ll1l111_opy_]
  for bstack1l1l11l1ll_opy_, bstack11ll1l111_opy_ in bstack1lll11l11l_opy_.items():
    if isinstance(bstack11ll1l111_opy_, list):
      for bstack1111111ll_opy_ in bstack11ll1l111_opy_:
        if bstack1111111ll_opy_ in bstack1ll11lll_opy_:
          config[bstack1l1l11l1ll_opy_] = config[bstack1111111ll_opy_]
          del config[bstack1111111ll_opy_]
          break
    elif bstack11ll1l111_opy_ in bstack1ll11lll_opy_:
      config[bstack1l1l11l1ll_opy_] = config[bstack11ll1l111_opy_]
      del config[bstack11ll1l111_opy_]
  for bstack1111111ll_opy_ in list(config):
    for bstack1ll111l111_opy_ in bstack1ll1l11l1l_opy_:
      if bstack1111111ll_opy_.lower() == bstack1ll111l111_opy_.lower() and bstack1111111ll_opy_ != bstack1ll111l111_opy_:
        config[bstack1ll111l111_opy_] = config[bstack1111111ll_opy_]
        del config[bstack1111111ll_opy_]
  bstack1lll11ll1_opy_ = []
  if bstack1lllll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࢷ") in config:
    bstack1lll11ll1_opy_ = config[bstack1lllll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࢸ")]
  for platform in bstack1lll11ll1_opy_:
    for bstack1111111ll_opy_ in list(platform):
      for bstack1ll111l111_opy_ in bstack1ll1l11l1l_opy_:
        if bstack1111111ll_opy_.lower() == bstack1ll111l111_opy_.lower() and bstack1111111ll_opy_ != bstack1ll111l111_opy_:
          platform[bstack1ll111l111_opy_] = platform[bstack1111111ll_opy_]
          del platform[bstack1111111ll_opy_]
  for bstack1l1l11l1ll_opy_, bstack11ll1l111_opy_ in bstack1lll11l11l_opy_.items():
    for platform in bstack1lll11ll1_opy_:
      if isinstance(bstack11ll1l111_opy_, list):
        for bstack1111111ll_opy_ in bstack11ll1l111_opy_:
          if bstack1111111ll_opy_ in platform:
            platform[bstack1l1l11l1ll_opy_] = platform[bstack1111111ll_opy_]
            del platform[bstack1111111ll_opy_]
            break
      elif bstack11ll1l111_opy_ in platform:
        platform[bstack1l1l11l1ll_opy_] = platform[bstack11ll1l111_opy_]
        del platform[bstack11ll1l111_opy_]
  for bstack1l1l1l111l_opy_ in bstack1l1l11l111_opy_:
    if bstack1l1l1l111l_opy_ in config:
      if not bstack1l1l11l111_opy_[bstack1l1l1l111l_opy_] in config:
        config[bstack1l1l11l111_opy_[bstack1l1l1l111l_opy_]] = {}
      config[bstack1l1l11l111_opy_[bstack1l1l1l111l_opy_]].update(config[bstack1l1l1l111l_opy_])
      del config[bstack1l1l1l111l_opy_]
  for platform in bstack1lll11ll1_opy_:
    for bstack1l1l1l111l_opy_ in bstack1l1l11l111_opy_:
      if bstack1l1l1l111l_opy_ in list(platform):
        if not bstack1l1l11l111_opy_[bstack1l1l1l111l_opy_] in platform:
          platform[bstack1l1l11l111_opy_[bstack1l1l1l111l_opy_]] = {}
        platform[bstack1l1l11l111_opy_[bstack1l1l1l111l_opy_]].update(platform[bstack1l1l1l111l_opy_])
        del platform[bstack1l1l1l111l_opy_]
  config = bstack11lll111_opy_(config)
  return config
def bstack11l1l1l1_opy_(config):
  global bstack1l1l1l1lll_opy_
  if bstack1lllll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࢹ") in config and str(config[bstack1lllll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢺ")]).lower() != bstack1lllll1l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨࢻ"):
    if not bstack1lllll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢼ") in config:
      config[bstack1lllll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢽ")] = {}
    if not bstack1lllll1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢾ") in config[bstack1lllll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢿ")]:
      bstack1llll1ll1_opy_ = datetime.datetime.now()
      bstack11l1ll11l_opy_ = bstack1llll1ll1_opy_.strftime(bstack1lllll1l_opy_ (u"ࠧࠦࡦࡢࠩࡧࡥࠥࡉࠧࡐࠫࣀ"))
      hostname = socket.gethostname()
      bstack11ll111ll_opy_ = bstack1lllll1l_opy_ (u"ࠨࠩࣁ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1lllll1l_opy_ (u"ࠩࡾࢁࡤࢁࡽࡠࡽࢀࠫࣂ").format(bstack11l1ll11l_opy_, hostname, bstack11ll111ll_opy_)
      config[bstack1lllll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣃ")][bstack1lllll1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣄ")] = identifier
    bstack1l1l1l1lll_opy_ = config[bstack1lllll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣅ")][bstack1lllll1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣆ")]
  return config
def bstack11ll1l1ll_opy_():
  bstack1ll1l1l1ll_opy_ =  bstack1lll1l1l11_opy_()[bstack1lllll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷ࠭ࣇ")]
  return bstack1ll1l1l1ll_opy_ if bstack1ll1l1l1ll_opy_ else -1
def bstack1l1lll111l_opy_(bstack1ll1l1l1ll_opy_):
  global CONFIG
  if not bstack1lllll1l_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣈ") in CONFIG[bstack1lllll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣉ")]:
    return
  CONFIG[bstack1lllll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")] = CONFIG[bstack1lllll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣋")].replace(
    bstack1lllll1l_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧ࣌"),
    str(bstack1ll1l1l1ll_opy_)
  )
def bstack111lll1l_opy_():
  global CONFIG
  if not bstack1lllll1l_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬ࣍") in CONFIG[bstack1lllll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣎")]:
    return
  bstack1llll1ll1_opy_ = datetime.datetime.now()
  bstack11l1ll11l_opy_ = bstack1llll1ll1_opy_.strftime(bstack1lllll1l_opy_ (u"ࠨࠧࡧ࠱ࠪࡨ࠭ࠦࡊ࠽ࠩࡒ࣏࠭"))
  CONFIG[bstack1lllll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")] = CONFIG[bstack1lllll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣑ࠬ")].replace(
    bstack1lllll1l_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿ࣒ࠪ"),
    bstack11l1ll11l_opy_
  )
def bstack1ll1l1ll1l_opy_():
  global CONFIG
  if bstack1lllll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ") in CONFIG and not bool(CONFIG[bstack1lllll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣔ")]):
    del CONFIG[bstack1lllll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣕ")]
    return
  if not bstack1lllll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ") in CONFIG:
    CONFIG[bstack1lllll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣗ")] = bstack1lllll1l_opy_ (u"ࠪࠧࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣘ")
  if bstack1lllll1l_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪࣙ") in CONFIG[bstack1lllll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣚ")]:
    bstack111lll1l_opy_()
    os.environ[bstack1lllll1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪࣛ")] = CONFIG[bstack1lllll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣜ")]
  if not bstack1lllll1l_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣝ") in CONFIG[bstack1lllll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣞ")]:
    return
  bstack1ll1l1l1ll_opy_ = bstack1lllll1l_opy_ (u"ࠪࠫࣟ")
  bstack1l1l11lll_opy_ = bstack11ll1l1ll_opy_()
  if bstack1l1l11lll_opy_ != -1:
    bstack1ll1l1l1ll_opy_ = bstack1lllll1l_opy_ (u"ࠫࡈࡏࠠࠨ࣠") + str(bstack1l1l11lll_opy_)
  if bstack1ll1l1l1ll_opy_ == bstack1lllll1l_opy_ (u"ࠬ࠭࣡"):
    bstack1l1ll1111l_opy_ = bstack1lll111l1_opy_(CONFIG[bstack1lllll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ࣢")])
    if bstack1l1ll1111l_opy_ != -1:
      bstack1ll1l1l1ll_opy_ = str(bstack1l1ll1111l_opy_)
  if bstack1ll1l1l1ll_opy_:
    bstack1l1lll111l_opy_(bstack1ll1l1l1ll_opy_)
    os.environ[bstack1lllll1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࣣࠫ")] = CONFIG[bstack1lllll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣤ")]
def bstack1l111l1ll_opy_(bstack1ll1ll1l_opy_, bstack11111111l_opy_, path):
  bstack11ll111l1_opy_ = {
    bstack1lllll1l_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣥ"): bstack11111111l_opy_
  }
  if os.path.exists(path):
    bstack1ll1l11ll_opy_ = json.load(open(path, bstack1lllll1l_opy_ (u"ࠪࡶࡧࣦ࠭")))
  else:
    bstack1ll1l11ll_opy_ = {}
  bstack1ll1l11ll_opy_[bstack1ll1ll1l_opy_] = bstack11ll111l1_opy_
  with open(path, bstack1lllll1l_opy_ (u"ࠦࡼ࠱ࠢࣧ")) as outfile:
    json.dump(bstack1ll1l11ll_opy_, outfile)
def bstack1lll111l1_opy_(bstack1ll1ll1l_opy_):
  bstack1ll1ll1l_opy_ = str(bstack1ll1ll1l_opy_)
  bstack111llll11_opy_ = os.path.join(os.path.expanduser(bstack1lllll1l_opy_ (u"ࠬࢄࠧࣨ")), bstack1lllll1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࣩ࠭"))
  try:
    if not os.path.exists(bstack111llll11_opy_):
      os.makedirs(bstack111llll11_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1lllll1l_opy_ (u"ࠧࡿࠩ࣪")), bstack1lllll1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ࣫"), bstack1lllll1l_opy_ (u"ࠩ࠱ࡦࡺ࡯࡬ࡥ࠯ࡱࡥࡲ࡫࠭ࡤࡣࡦ࡬ࡪ࠴ࡪࡴࡱࡱࠫ࣬"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1lllll1l_opy_ (u"ࠪࡻ࣭ࠬ")):
        pass
      with open(file_path, bstack1lllll1l_opy_ (u"ࠦࡼ࠱࣮ࠢ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1lllll1l_opy_ (u"ࠬࡸ࣯ࠧ")) as bstack111l1ll11_opy_:
      bstack11ll1ll11_opy_ = json.load(bstack111l1ll11_opy_)
    if bstack1ll1ll1l_opy_ in bstack11ll1ll11_opy_:
      bstack1l1l11l1l_opy_ = bstack11ll1ll11_opy_[bstack1ll1ll1l_opy_][bstack1lllll1l_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣰࠪ")]
      bstack111ll1ll1_opy_ = int(bstack1l1l11l1l_opy_) + 1
      bstack1l111l1ll_opy_(bstack1ll1ll1l_opy_, bstack111ll1ll1_opy_, file_path)
      return bstack111ll1ll1_opy_
    else:
      bstack1l111l1ll_opy_(bstack1ll1ll1l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1lll111l1l_opy_.format(str(e)))
    return -1
def bstack1lll11111_opy_(config):
  if not config[bstack1lllll1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࣱࠩ")] or not config[bstack1lllll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࣲࠫ")]:
    return True
  else:
    return False
def bstack1111ll111_opy_(config, index=0):
  global bstack11ll11ll1_opy_
  bstack111l1ll1l_opy_ = {}
  caps = bstack1ll11ll1l1_opy_ + bstack1l1l11llll_opy_
  if bstack11ll11ll1_opy_:
    caps += bstack1ll11ll1l_opy_
  for key in config:
    if key in caps + [bstack1lllll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࣳ")]:
      continue
    bstack111l1ll1l_opy_[key] = config[key]
  if bstack1lllll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ") in config:
    for bstack1ll11llll_opy_ in config[bstack1lllll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣵ")][index]:
      if bstack1ll11llll_opy_ in caps + [bstack1lllll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࣶࠪ"), bstack1lllll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧࣷ")]:
        continue
      bstack111l1ll1l_opy_[bstack1ll11llll_opy_] = config[bstack1lllll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣸ")][index][bstack1ll11llll_opy_]
  bstack111l1ll1l_opy_[bstack1lllll1l_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࣹࠪ")] = socket.gethostname()
  if bstack1lllll1l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࣺࠪ") in bstack111l1ll1l_opy_:
    del (bstack111l1ll1l_opy_[bstack1lllll1l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫࣻ")])
  return bstack111l1ll1l_opy_
def bstack111l11l11_opy_(config):
  global bstack11ll11ll1_opy_
  bstack11l11llll_opy_ = {}
  caps = bstack1l1l11llll_opy_
  if bstack11ll11ll1_opy_:
    caps += bstack1ll11ll1l_opy_
  for key in caps:
    if key in config:
      bstack11l11llll_opy_[key] = config[key]
  return bstack11l11llll_opy_
def bstack111l1ll1_opy_(bstack111l1ll1l_opy_, bstack11l11llll_opy_):
  bstack1l1lllll_opy_ = {}
  for key in bstack111l1ll1l_opy_.keys():
    if key in bstack1l1lllll1l_opy_:
      bstack1l1lllll_opy_[bstack1l1lllll1l_opy_[key]] = bstack111l1ll1l_opy_[key]
    else:
      bstack1l1lllll_opy_[key] = bstack111l1ll1l_opy_[key]
  for key in bstack11l11llll_opy_:
    if key in bstack1l1lllll1l_opy_:
      bstack1l1lllll_opy_[bstack1l1lllll1l_opy_[key]] = bstack11l11llll_opy_[key]
    else:
      bstack1l1lllll_opy_[key] = bstack11l11llll_opy_[key]
  return bstack1l1lllll_opy_
def bstack1l1ll111l_opy_(config, index=0):
  global bstack11ll11ll1_opy_
  config = copy.deepcopy(config)
  caps = {}
  bstack11l11llll_opy_ = bstack111l11l11_opy_(config)
  bstack11l1lll1_opy_ = bstack1l1l11llll_opy_
  bstack11l1lll1_opy_ += bstack11l11l111_opy_
  if bstack11ll11ll1_opy_:
    bstack11l1lll1_opy_ += bstack1ll11ll1l_opy_
  if bstack1lllll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ") in config:
    if bstack1lllll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪࣽ") in config[bstack1lllll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࣾ")][index]:
      caps[bstack1lllll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬࣿ")] = config[bstack1lllll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫऀ")][index][bstack1lllll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧँ")]
    if bstack1lllll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫं") in config[bstack1lllll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧः")][index]:
      caps[bstack1lllll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऄ")] = str(config[bstack1lllll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index][bstack1lllll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨआ")])
    bstack1lllll11ll_opy_ = {}
    for bstack1lllll1ll1_opy_ in bstack11l1lll1_opy_:
      if bstack1lllll1ll1_opy_ in config[bstack1lllll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index]:
        if bstack1lllll1ll1_opy_ == bstack1lllll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫई"):
          try:
            bstack1lllll11ll_opy_[bstack1lllll1ll1_opy_] = str(config[bstack1lllll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack1lllll1ll1_opy_] * 1.0)
          except:
            bstack1lllll11ll_opy_[bstack1lllll1ll1_opy_] = str(config[bstack1lllll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऊ")][index][bstack1lllll1ll1_opy_])
        else:
          bstack1lllll11ll_opy_[bstack1lllll1ll1_opy_] = config[bstack1lllll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऋ")][index][bstack1lllll1ll1_opy_]
        del (config[bstack1lllll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩऌ")][index][bstack1lllll1ll1_opy_])
    bstack11l11llll_opy_ = update(bstack11l11llll_opy_, bstack1lllll11ll_opy_)
  bstack111l1ll1l_opy_ = bstack1111ll111_opy_(config, index)
  for bstack1111111ll_opy_ in bstack1l1l11llll_opy_ + [bstack1lllll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬऍ"), bstack1lllll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩऎ")]:
    if bstack1111111ll_opy_ in bstack111l1ll1l_opy_:
      bstack11l11llll_opy_[bstack1111111ll_opy_] = bstack111l1ll1l_opy_[bstack1111111ll_opy_]
      del (bstack111l1ll1l_opy_[bstack1111111ll_opy_])
  if bstack1l1l11l1l1_opy_(config):
    bstack111l1ll1l_opy_[bstack1lllll1l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩए")] = True
    caps.update(bstack11l11llll_opy_)
    caps[bstack1lllll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫऐ")] = bstack111l1ll1l_opy_
  else:
    bstack111l1ll1l_opy_[bstack1lllll1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫऑ")] = False
    caps.update(bstack111l1ll1_opy_(bstack111l1ll1l_opy_, bstack11l11llll_opy_))
    if bstack1lllll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪऒ") in caps:
      caps[bstack1lllll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧओ")] = caps[bstack1lllll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬऔ")]
      del (caps[bstack1lllll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭क")])
    if bstack1lllll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪख") in caps:
      caps[bstack1lllll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬग")] = caps[bstack1lllll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬघ")]
      del (caps[bstack1lllll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ङ")])
  return caps
def bstack1ll1l1l11_opy_():
  global bstack11l111l1_opy_
  if bstack1l11ll1l_opy_() <= version.parse(bstack1lllll1l_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭च")):
    if bstack11l111l1_opy_ != bstack1lllll1l_opy_ (u"ࠧࠨछ"):
      return bstack1lllll1l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤज") + bstack11l111l1_opy_ + bstack1lllll1l_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨझ")
    return bstack1ll1lll1l_opy_
  if bstack11l111l1_opy_ != bstack1lllll1l_opy_ (u"ࠪࠫञ"):
    return bstack1lllll1l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨट") + bstack11l111l1_opy_ + bstack1lllll1l_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨठ")
  return bstack1111llll1_opy_
def bstack11ll11l1l_opy_(options):
  return hasattr(options, bstack1lllll1l_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧड"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l1l111l_opy_(options, bstack11111llll_opy_):
  for bstack1l1ll11l11_opy_ in bstack11111llll_opy_:
    if bstack1l1ll11l11_opy_ in [bstack1lllll1l_opy_ (u"ࠧࡢࡴࡪࡷࠬढ"), bstack1lllll1l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬण")]:
      continue
    if bstack1l1ll11l11_opy_ in options._experimental_options:
      options._experimental_options[bstack1l1ll11l11_opy_] = update(options._experimental_options[bstack1l1ll11l11_opy_],
                                                         bstack11111llll_opy_[bstack1l1ll11l11_opy_])
    else:
      options.add_experimental_option(bstack1l1ll11l11_opy_, bstack11111llll_opy_[bstack1l1ll11l11_opy_])
  if bstack1lllll1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧत") in bstack11111llll_opy_:
    for arg in bstack11111llll_opy_[bstack1lllll1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨथ")]:
      options.add_argument(arg)
    del (bstack11111llll_opy_[bstack1lllll1l_opy_ (u"ࠫࡦࡸࡧࡴࠩद")])
  if bstack1lllll1l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩध") in bstack11111llll_opy_:
    for ext in bstack11111llll_opy_[bstack1lllll1l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪन")]:
      options.add_extension(ext)
    del (bstack11111llll_opy_[bstack1lllll1l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫऩ")])
def bstack1lll1lll1_opy_(options, bstack1ll111l1_opy_):
  if bstack1lllll1l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧप") in bstack1ll111l1_opy_:
    for bstack1l11l1ll1_opy_ in bstack1ll111l1_opy_[bstack1lllll1l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨफ")]:
      if bstack1l11l1ll1_opy_ in options._preferences:
        options._preferences[bstack1l11l1ll1_opy_] = update(options._preferences[bstack1l11l1ll1_opy_], bstack1ll111l1_opy_[bstack1lllll1l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩब")][bstack1l11l1ll1_opy_])
      else:
        options.set_preference(bstack1l11l1ll1_opy_, bstack1ll111l1_opy_[bstack1lllll1l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪभ")][bstack1l11l1ll1_opy_])
  if bstack1lllll1l_opy_ (u"ࠬࡧࡲࡨࡵࠪम") in bstack1ll111l1_opy_:
    for arg in bstack1ll111l1_opy_[bstack1lllll1l_opy_ (u"࠭ࡡࡳࡩࡶࠫय")]:
      options.add_argument(arg)
def bstack1l1llll1l1_opy_(options, bstack11l1l1lll_opy_):
  if bstack1lllll1l_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࠨर") in bstack11l1l1lll_opy_:
    options.use_webview(bool(bstack11l1l1lll_opy_[bstack1lllll1l_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩऱ")]))
  bstack1l1l111l_opy_(options, bstack11l1l1lll_opy_)
def bstack1l1l1lll1l_opy_(options, bstack11l1llll1_opy_):
  for bstack1lll111lll_opy_ in bstack11l1llll1_opy_:
    if bstack1lll111lll_opy_ in [bstack1lllll1l_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ल"), bstack1lllll1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨळ")]:
      continue
    options.set_capability(bstack1lll111lll_opy_, bstack11l1llll1_opy_[bstack1lll111lll_opy_])
  if bstack1lllll1l_opy_ (u"ࠫࡦࡸࡧࡴࠩऴ") in bstack11l1llll1_opy_:
    for arg in bstack11l1llll1_opy_[bstack1lllll1l_opy_ (u"ࠬࡧࡲࡨࡵࠪव")]:
      options.add_argument(arg)
  if bstack1lllll1l_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪश") in bstack11l1llll1_opy_:
    options.bstack1ll1ll111l_opy_(bool(bstack11l1llll1_opy_[bstack1lllll1l_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫष")]))
def bstack1l11lll1l_opy_(options, bstack1lll111ll_opy_):
  for bstack111l11lll_opy_ in bstack1lll111ll_opy_:
    if bstack111l11lll_opy_ in [bstack1lllll1l_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस"), bstack1lllll1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧह")]:
      continue
    options._options[bstack111l11lll_opy_] = bstack1lll111ll_opy_[bstack111l11lll_opy_]
  if bstack1lllll1l_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऺ") in bstack1lll111ll_opy_:
    for bstack1l1ll111l1_opy_ in bstack1lll111ll_opy_[bstack1lllll1l_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऻ")]:
      options.bstack111111ll1_opy_(
        bstack1l1ll111l1_opy_, bstack1lll111ll_opy_[bstack1lllll1l_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ़ࠩ")][bstack1l1ll111l1_opy_])
  if bstack1lllll1l_opy_ (u"࠭ࡡࡳࡩࡶࠫऽ") in bstack1lll111ll_opy_:
    for arg in bstack1lll111ll_opy_[bstack1lllll1l_opy_ (u"ࠧࡢࡴࡪࡷࠬा")]:
      options.add_argument(arg)
def bstack1111ll11_opy_(options, caps):
  if not hasattr(options, bstack1lllll1l_opy_ (u"ࠨࡍࡈ࡝ࠬि")):
    return
  if options.KEY == bstack1lllll1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧी") and options.KEY in caps:
    bstack1l1l111l_opy_(options, caps[bstack1lllll1l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨु")])
  elif options.KEY == bstack1lllll1l_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩू") and options.KEY in caps:
    bstack1lll1lll1_opy_(options, caps[bstack1lllll1l_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪृ")])
  elif options.KEY == bstack1lllll1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧॄ") and options.KEY in caps:
    bstack1l1l1lll1l_opy_(options, caps[bstack1lllll1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨॅ")])
  elif options.KEY == bstack1lllll1l_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩॆ") and options.KEY in caps:
    bstack1l1llll1l1_opy_(options, caps[bstack1lllll1l_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪे")])
  elif options.KEY == bstack1lllll1l_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩै") and options.KEY in caps:
    bstack1l11lll1l_opy_(options, caps[bstack1lllll1l_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪॉ")])
def bstack11llll11_opy_(caps):
  global bstack11ll11ll1_opy_
  if isinstance(os.environ.get(bstack1lllll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ॊ")), str):
    bstack11ll11ll1_opy_ = eval(os.getenv(bstack1lllll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧो")))
  if bstack11ll11ll1_opy_:
    if bstack11lllll1_opy_() < version.parse(bstack1lllll1l_opy_ (u"ࠧ࠳࠰࠶࠲࠵࠭ौ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1lllll1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ्")
    if bstack1lllll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॎ") in caps:
      browser = caps[bstack1lllll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨॏ")]
    elif bstack1lllll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬॐ") in caps:
      browser = caps[bstack1lllll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭॑")]
    browser = str(browser).lower()
    if browser == bstack1lllll1l_opy_ (u"࠭ࡩࡱࡪࡲࡲࡪ॒࠭") or browser == bstack1lllll1l_opy_ (u"ࠧࡪࡲࡤࡨࠬ॓"):
      browser = bstack1lllll1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨ॔")
    if browser == bstack1lllll1l_opy_ (u"ࠩࡶࡥࡲࡹࡵ࡯ࡩࠪॕ"):
      browser = bstack1lllll1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪॖ")
    if browser not in [bstack1lllll1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫॗ"), bstack1lllll1l_opy_ (u"ࠬ࡫ࡤࡨࡧࠪक़"), bstack1lllll1l_opy_ (u"࠭ࡩࡦࠩख़"), bstack1lllll1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧग़"), bstack1lllll1l_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩज़")]:
      return None
    try:
      package = bstack1lllll1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡼࡿ࠱ࡳࡵࡺࡩࡰࡰࡶࠫड़").format(browser)
      name = bstack1lllll1l_opy_ (u"ࠪࡓࡵࡺࡩࡰࡰࡶࠫढ़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11ll11l1l_opy_(options):
        return None
      for bstack1111111ll_opy_ in caps.keys():
        options.set_capability(bstack1111111ll_opy_, caps[bstack1111111ll_opy_])
      bstack1111ll11_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l1lll11l1_opy_(options, bstack1l111llll_opy_):
  if not bstack11ll11l1l_opy_(options):
    return
  for bstack1111111ll_opy_ in bstack1l111llll_opy_.keys():
    if bstack1111111ll_opy_ in bstack11l11l111_opy_:
      continue
    if bstack1111111ll_opy_ in options._caps and type(options._caps[bstack1111111ll_opy_]) in [dict, list]:
      options._caps[bstack1111111ll_opy_] = update(options._caps[bstack1111111ll_opy_], bstack1l111llll_opy_[bstack1111111ll_opy_])
    else:
      options.set_capability(bstack1111111ll_opy_, bstack1l111llll_opy_[bstack1111111ll_opy_])
  bstack1111ll11_opy_(options, bstack1l111llll_opy_)
  if bstack1lllll1l_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪफ़") in options._caps:
    if options._caps[bstack1lllll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪय़")] and options._caps[bstack1lllll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")].lower() != bstack1lllll1l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨॡ"):
      del options._caps[bstack1lllll1l_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧॢ")]
def bstack1ll11l1l11_opy_(proxy_config):
  if bstack1lllll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॣ") in proxy_config:
    proxy_config[bstack1lllll1l_opy_ (u"ࠪࡷࡸࡲࡐࡳࡱࡻࡽࠬ।")] = proxy_config[bstack1lllll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ॥")]
    del (proxy_config[bstack1lllll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ०")])
  if bstack1lllll1l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ१") in proxy_config and proxy_config[bstack1lllll1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ२")].lower() != bstack1lllll1l_opy_ (u"ࠨࡦ࡬ࡶࡪࡩࡴࠨ३"):
    proxy_config[bstack1lllll1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ४")] = bstack1lllll1l_opy_ (u"ࠪࡱࡦࡴࡵࡢ࡮ࠪ५")
  if bstack1lllll1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡄࡹࡹࡵࡣࡰࡰࡩ࡭࡬࡛ࡲ࡭ࠩ६") in proxy_config:
    proxy_config[bstack1lllll1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ७")] = bstack1lllll1l_opy_ (u"࠭ࡰࡢࡥࠪ८")
  return proxy_config
def bstack1ll1lllll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1lllll1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭९") in config:
    return proxy
  config[bstack1lllll1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧ॰")] = bstack1ll11l1l11_opy_(config[bstack1lllll1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨॱ")])
  if proxy == None:
    proxy = Proxy(config[bstack1lllll1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩॲ")])
  return proxy
def bstack1lll11l1l_opy_(self):
  global CONFIG
  global bstack1111l1111_opy_
  try:
    proxy = bstack1lll11ll11_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1lllll1l_opy_ (u"ࠫ࠳ࡶࡡࡤࠩॳ")):
        proxies = bstack11111ll1l_opy_(proxy, bstack1ll1l1l11_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll1ll11l_opy_ = proxies.popitem()
          if bstack1lllll1l_opy_ (u"ࠧࡀ࠯࠰ࠤॴ") in bstack1ll1ll11l_opy_:
            return bstack1ll1ll11l_opy_
          else:
            return bstack1lllll1l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢॵ") + bstack1ll1ll11l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1lllll1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦॶ").format(str(e)))
  return bstack1111l1111_opy_(self)
def bstack1ll11l1l1l_opy_():
  global CONFIG
  return bstack1l11l111l_opy_(CONFIG) and bstack1l1ll1111_opy_() and bstack1l11ll1l_opy_() >= version.parse(bstack11l11lll1_opy_)
def bstack1l1lll111_opy_():
  global CONFIG
  return (bstack1lllll1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫॷ") in CONFIG or bstack1lllll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॸ") in CONFIG) and bstack1l1l1lllll_opy_()
def bstack1ll111l1ll_opy_(config):
  bstack1lll1l1111_opy_ = {}
  if bstack1lllll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧॹ") in config:
    bstack1lll1l1111_opy_ = config[bstack1lllll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॺ")]
  if bstack1lllll1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॻ") in config:
    bstack1lll1l1111_opy_ = config[bstack1lllll1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬॼ")]
  proxy = bstack1lll11ll11_opy_(config)
  if proxy:
    if proxy.endswith(bstack1lllll1l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬॽ")) and os.path.isfile(proxy):
      bstack1lll1l1111_opy_[bstack1lllll1l_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫॾ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1lllll1l_opy_ (u"ࠩ࠱ࡴࡦࡩࠧॿ")):
        proxies = bstack1ll11l111_opy_(config, bstack1ll1l1l11_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll1ll11l_opy_ = proxies.popitem()
          if bstack1lllll1l_opy_ (u"ࠥ࠾࠴࠵ࠢঀ") in bstack1ll1ll11l_opy_:
            parsed_url = urlparse(bstack1ll1ll11l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1lllll1l_opy_ (u"ࠦ࠿࠵࠯ࠣঁ") + bstack1ll1ll11l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1lll1l1111_opy_[bstack1lllll1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨং")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1lll1l1111_opy_[bstack1lllll1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩঃ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1lll1l1111_opy_[bstack1lllll1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ঄")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1lll1l1111_opy_[bstack1lllll1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫঅ")] = str(parsed_url.password)
  return bstack1lll1l1111_opy_
def bstack1l111111l_opy_(config):
  if bstack1lllll1l_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧআ") in config:
    return config[bstack1lllll1l_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨই")]
  return {}
def bstack11llllll_opy_(caps):
  global bstack1l1l1l1lll_opy_
  if bstack1lllll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬঈ") in caps:
    caps[bstack1lllll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭উ")][bstack1lllll1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬঊ")] = True
    if bstack1l1l1l1lll_opy_:
      caps[bstack1lllll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨঋ")][bstack1lllll1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪঌ")] = bstack1l1l1l1lll_opy_
  else:
    caps[bstack1lllll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧ঍")] = True
    if bstack1l1l1l1lll_opy_:
      caps[bstack1lllll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ঎")] = bstack1l1l1l1lll_opy_
def bstack1ll11ll1_opy_():
  global CONFIG
  if bstack1lllll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨএ") in CONFIG and bstack11l1l1ll_opy_(CONFIG[bstack1lllll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩঐ")]):
    bstack1lll1l1111_opy_ = bstack1ll111l1ll_opy_(CONFIG)
    bstack11l1l1l11_opy_(CONFIG[bstack1lllll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ঑")], bstack1lll1l1111_opy_)
def bstack11l1l1l11_opy_(key, bstack1lll1l1111_opy_):
  global bstack1l11l11l1_opy_
  logger.info(bstack11l1ll1l1_opy_)
  try:
    bstack1l11l11l1_opy_ = Local()
    bstack1lll111ll1_opy_ = {bstack1lllll1l_opy_ (u"ࠧ࡬ࡧࡼࠫ঒"): key}
    bstack1lll111ll1_opy_.update(bstack1lll1l1111_opy_)
    logger.debug(bstack1ll11l111l_opy_.format(str(bstack1lll111ll1_opy_)))
    bstack1l11l11l1_opy_.start(**bstack1lll111ll1_opy_)
    if bstack1l11l11l1_opy_.isRunning():
      logger.info(bstack1l111l11l_opy_)
  except Exception as e:
    bstack1ll1l11l11_opy_(bstack1lll1ll1l_opy_.format(str(e)))
def bstack1l1ll1lll1_opy_():
  global bstack1l11l11l1_opy_
  if bstack1l11l11l1_opy_.isRunning():
    logger.info(bstack1lll1ll11_opy_)
    bstack1l11l11l1_opy_.stop()
  bstack1l11l11l1_opy_ = None
def bstack1lll11lll1_opy_(bstack1llll11lll_opy_=[]):
  global CONFIG
  bstack11111111_opy_ = []
  bstack1llll11ll1_opy_ = [bstack1lllll1l_opy_ (u"ࠨࡱࡶࠫও"), bstack1lllll1l_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬঔ"), bstack1lllll1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧক"), bstack1lllll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭খ"), bstack1lllll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪগ"), bstack1lllll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧঘ")]
  try:
    for err in bstack1llll11lll_opy_:
      bstack1111llll_opy_ = {}
      for k in bstack1llll11ll1_opy_:
        val = CONFIG[bstack1lllll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪঙ")][int(err[bstack1lllll1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧচ")])].get(k)
        if val:
          bstack1111llll_opy_[k] = val
      if(err[bstack1lllll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨছ")] != bstack1lllll1l_opy_ (u"ࠪࠫজ")):
        bstack1111llll_opy_[bstack1lllll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪঝ")] = {
          err[bstack1lllll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪঞ")]: err[bstack1lllll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬট")]
        }
        bstack11111111_opy_.append(bstack1111llll_opy_)
  except Exception as e:
    logger.debug(bstack1lllll1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩঠ") + str(e))
  finally:
    return bstack11111111_opy_
def bstack1ll1ll1l1l_opy_(file_name):
  bstack1l1ll111_opy_ = []
  try:
    bstack111lll1l1_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack111lll1l1_opy_):
      with open(bstack111lll1l1_opy_) as f:
        bstack1lll1ll111_opy_ = json.load(f)
        bstack1l1ll111_opy_ = bstack1lll1ll111_opy_
      os.remove(bstack111lll1l1_opy_)
    return bstack1l1ll111_opy_
  except Exception as e:
    logger.debug(bstack1lllll1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪড") + str(e))
def bstack1llllll1ll_opy_():
  global bstack1l1111ll1_opy_
  global bstack1l1llll111_opy_
  global bstack1ll111l11l_opy_
  global bstack1l1ll11111_opy_
  global bstack1l1l1111l_opy_
  global bstack1l1l11l1_opy_
  percy.shutdown()
  bstack1l1ll1lll_opy_ = os.environ.get(bstack1lllll1l_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪঢ"))
  if bstack1l1ll1lll_opy_ in [bstack1lllll1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩণ"), bstack1lllll1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪত")]:
    bstack11111lll1_opy_()
  if bstack1l1111ll1_opy_:
    logger.warning(bstack11l1ll1l_opy_.format(str(bstack1l1111ll1_opy_)))
  else:
    try:
      bstack1ll1l11ll_opy_ = bstack11l11l1l_opy_(bstack1lllll1l_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫথ"), logger)
      if bstack1ll1l11ll_opy_.get(bstack1lllll1l_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫদ")) and bstack1ll1l11ll_opy_.get(bstack1lllll1l_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬধ")).get(bstack1lllll1l_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪন")):
        logger.warning(bstack11l1ll1l_opy_.format(str(bstack1ll1l11ll_opy_[bstack1lllll1l_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ঩")][bstack1lllll1l_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬপ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1ll1ll11ll_opy_)
  global bstack1l11l11l1_opy_
  if bstack1l11l11l1_opy_:
    bstack1l1ll1lll1_opy_()
  try:
    for driver in bstack1l1llll111_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1llll1ll_opy_)
  if bstack1l1l11l1_opy_ == bstack1lllll1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪফ"):
    bstack1l1l1111l_opy_ = bstack1ll1ll1l1l_opy_(bstack1lllll1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ব"))
  if bstack1l1l11l1_opy_ == bstack1lllll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ভ") and len(bstack1l1ll11111_opy_) == 0:
    bstack1l1ll11111_opy_ = bstack1ll1ll1l1l_opy_(bstack1lllll1l_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬম"))
    if len(bstack1l1ll11111_opy_) == 0:
      bstack1l1ll11111_opy_ = bstack1ll1ll1l1l_opy_(bstack1lllll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧয"))
  bstack1lll1lllll_opy_ = bstack1lllll1l_opy_ (u"ࠩࠪর")
  if len(bstack1ll111l11l_opy_) > 0:
    bstack1lll1lllll_opy_ = bstack1lll11lll1_opy_(bstack1ll111l11l_opy_)
  elif len(bstack1l1ll11111_opy_) > 0:
    bstack1lll1lllll_opy_ = bstack1lll11lll1_opy_(bstack1l1ll11111_opy_)
  elif len(bstack1l1l1111l_opy_) > 0:
    bstack1lll1lllll_opy_ = bstack1lll11lll1_opy_(bstack1l1l1111l_opy_)
  elif len(bstack111l1111_opy_) > 0:
    bstack1lll1lllll_opy_ = bstack1lll11lll1_opy_(bstack111l1111_opy_)
  if bool(bstack1lll1lllll_opy_):
    bstack1ll11ll11_opy_(bstack1lll1lllll_opy_)
  else:
    bstack1ll11ll11_opy_()
  bstack11lll111l_opy_(bstack1l11ll11_opy_, logger)
def bstack11l11lll_opy_(self, *args):
  logger.error(bstack11l111lll_opy_)
  bstack1llllll1ll_opy_()
  sys.exit(1)
def bstack1ll1l11l11_opy_(err):
  logger.critical(bstack1ll11llll1_opy_.format(str(err)))
  bstack1ll11ll11_opy_(bstack1ll11llll1_opy_.format(str(err)), True)
  atexit.unregister(bstack1llllll1ll_opy_)
  bstack11111lll1_opy_()
  sys.exit(1)
def bstack1ll1lll1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1ll11ll11_opy_(message, True)
  atexit.unregister(bstack1llllll1ll_opy_)
  bstack11111lll1_opy_()
  sys.exit(1)
def bstack11l1ll111_opy_():
  global CONFIG
  global bstack1111ll1l1_opy_
  global bstack1ll11l11l_opy_
  global bstack1ll11lll11_opy_
  CONFIG = bstack1l1l11ll11_opy_()
  bstack1l11lll1_opy_()
  bstack1lll1lll1l_opy_()
  CONFIG = bstack1l1lll1l11_opy_(CONFIG)
  update(CONFIG, bstack1ll11l11l_opy_)
  update(CONFIG, bstack1111ll1l1_opy_)
  CONFIG = bstack11l1l1l1_opy_(CONFIG)
  bstack1ll11lll11_opy_ = bstack1l1l1l1ll_opy_(CONFIG)
  bstack1ll1ll1l1_opy_.bstack11111l1l1_opy_(bstack1lllll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ঱"), bstack1ll11lll11_opy_)
  if (bstack1lllll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧল") in CONFIG and bstack1lllll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ঳") in bstack1111ll1l1_opy_) or (
          bstack1lllll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ঴") in CONFIG and bstack1lllll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ঵") not in bstack1ll11l11l_opy_):
    if os.getenv(bstack1lllll1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬশ")):
      CONFIG[bstack1lllll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫষ")] = os.getenv(bstack1lllll1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧস"))
    else:
      bstack1ll1l1ll1l_opy_()
  elif (bstack1lllll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧহ") not in CONFIG and bstack1lllll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ঺") in CONFIG) or (
          bstack1lllll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ঻") in bstack1ll11l11l_opy_ and bstack1lllll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ়ࠪ") not in bstack1111ll1l1_opy_):
    del (CONFIG[bstack1lllll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪঽ")])
  if bstack1lll11111_opy_(CONFIG):
    bstack1ll1l11l11_opy_(bstack1ll1ll1111_opy_)
  bstack1ll1l11l_opy_()
  bstack11ll11lll_opy_()
  if bstack11ll11ll1_opy_:
    CONFIG[bstack1lllll1l_opy_ (u"ࠩࡤࡴࡵ࠭া")] = bstack1l11l1l11_opy_(CONFIG)
    logger.info(bstack11lll11l_opy_.format(CONFIG[bstack1lllll1l_opy_ (u"ࠪࡥࡵࡶࠧি")]))
def bstack1ll1lll111_opy_(config, bstack11l111111_opy_):
  global CONFIG
  global bstack11ll11ll1_opy_
  CONFIG = config
  bstack11ll11ll1_opy_ = bstack11l111111_opy_
def bstack11ll11lll_opy_():
  global CONFIG
  global bstack11ll11ll1_opy_
  if bstack1lllll1l_opy_ (u"ࠫࡦࡶࡰࠨী") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1ll1lll1_opy_(e, bstack1lll1l1ll_opy_)
    bstack11ll11ll1_opy_ = True
    bstack1ll1ll1l1_opy_.bstack11111l1l1_opy_(bstack1lllll1l_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫু"), True)
def bstack1l11l1l11_opy_(config):
  bstack1ll111111l_opy_ = bstack1lllll1l_opy_ (u"࠭ࠧূ")
  app = config[bstack1lllll1l_opy_ (u"ࠧࡢࡲࡳࠫৃ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1ll111l1l_opy_:
      if os.path.exists(app):
        bstack1ll111111l_opy_ = bstack1ll1111l1_opy_(config, app)
      elif bstack1ll1l11111_opy_(app):
        bstack1ll111111l_opy_ = app
      else:
        bstack1ll1l11l11_opy_(bstack1ll111llll_opy_.format(app))
    else:
      if bstack1ll1l11111_opy_(app):
        bstack1ll111111l_opy_ = app
      elif os.path.exists(app):
        bstack1ll111111l_opy_ = bstack1ll1111l1_opy_(app)
      else:
        bstack1ll1l11l11_opy_(bstack1l11l1111_opy_)
  else:
    if len(app) > 2:
      bstack1ll1l11l11_opy_(bstack11llll11l_opy_)
    elif len(app) == 2:
      if bstack1lllll1l_opy_ (u"ࠨࡲࡤࡸ࡭࠭ৄ") in app and bstack1lllll1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ৅") in app:
        if os.path.exists(app[bstack1lllll1l_opy_ (u"ࠪࡴࡦࡺࡨࠨ৆")]):
          bstack1ll111111l_opy_ = bstack1ll1111l1_opy_(config, app[bstack1lllll1l_opy_ (u"ࠫࡵࡧࡴࡩࠩে")], app[bstack1lllll1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨৈ")])
        else:
          bstack1ll1l11l11_opy_(bstack1ll111llll_opy_.format(app))
      else:
        bstack1ll1l11l11_opy_(bstack11llll11l_opy_)
    else:
      for key in app:
        if key in bstack1ll11l1111_opy_:
          if key == bstack1lllll1l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ৉"):
            if os.path.exists(app[key]):
              bstack1ll111111l_opy_ = bstack1ll1111l1_opy_(config, app[key])
            else:
              bstack1ll1l11l11_opy_(bstack1ll111llll_opy_.format(app))
          else:
            bstack1ll111111l_opy_ = app[key]
        else:
          bstack1ll1l11l11_opy_(bstack1lllll11l_opy_)
  return bstack1ll111111l_opy_
def bstack1ll1l11111_opy_(bstack1ll111111l_opy_):
  import re
  bstack11lll1l1l_opy_ = re.compile(bstack1lllll1l_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢ৊"))
  bstack1l1l11ll1l_opy_ = re.compile(bstack1lllll1l_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧো"))
  if bstack1lllll1l_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨৌ") in bstack1ll111111l_opy_ or re.fullmatch(bstack11lll1l1l_opy_, bstack1ll111111l_opy_) or re.fullmatch(bstack1l1l11ll1l_opy_, bstack1ll111111l_opy_):
    return True
  else:
    return False
def bstack1ll1111l1_opy_(config, path, bstack1l1111ll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1lllll1l_opy_ (u"ࠪࡶࡧ্࠭")).read()).hexdigest()
  bstack1ll111l1l1_opy_ = bstack1ll11111l1_opy_(md5_hash)
  bstack1ll111111l_opy_ = None
  if bstack1ll111l1l1_opy_:
    logger.info(bstack1lll1ll1l1_opy_.format(bstack1ll111l1l1_opy_, md5_hash))
    return bstack1ll111l1l1_opy_
  bstack1llll1l11_opy_ = MultipartEncoder(
    fields={
      bstack1lllll1l_opy_ (u"ࠫ࡫࡯࡬ࡦࠩৎ"): (os.path.basename(path), open(os.path.abspath(path), bstack1lllll1l_opy_ (u"ࠬࡸࡢࠨ৏")), bstack1lllll1l_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪ৐")),
      bstack1lllll1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ৑"): bstack1l1111ll_opy_
    }
  )
  response = requests.post(bstack11l11111l_opy_, data=bstack1llll1l11_opy_,
                           headers={bstack1lllll1l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ৒"): bstack1llll1l11_opy_.content_type},
                           auth=(config[bstack1lllll1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ৓")], config[bstack1lllll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭৔")]))
  try:
    res = json.loads(response.text)
    bstack1ll111111l_opy_ = res[bstack1lllll1l_opy_ (u"ࠫࡦࡶࡰࡠࡷࡵࡰࠬ৕")]
    logger.info(bstack1ll11l1ll1_opy_.format(bstack1ll111111l_opy_))
    bstack11lllll1l_opy_(md5_hash, bstack1ll111111l_opy_)
  except ValueError as err:
    bstack1ll1l11l11_opy_(bstack1l1l1ll11l_opy_.format(str(err)))
  return bstack1ll111111l_opy_
def bstack1ll1l11l_opy_():
  global CONFIG
  global bstack1l1lll11l_opy_
  bstack1l11lll11_opy_ = 0
  bstack1l1l1l1111_opy_ = 1
  if bstack1lllll1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ৖") in CONFIG:
    bstack1l1l1l1111_opy_ = CONFIG[bstack1lllll1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ৗ")]
  if bstack1lllll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৘") in CONFIG:
    bstack1l11lll11_opy_ = len(CONFIG[bstack1lllll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ৙")])
  bstack1l1lll11l_opy_ = int(bstack1l1l1l1111_opy_) * int(bstack1l11lll11_opy_)
def bstack1ll11111l1_opy_(md5_hash):
  bstack1l1l111l1_opy_ = os.path.join(os.path.expanduser(bstack1lllll1l_opy_ (u"ࠩࢁࠫ৚")), bstack1lllll1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ৛"), bstack1lllll1l_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬড়"))
  if os.path.exists(bstack1l1l111l1_opy_):
    bstack1111l11l1_opy_ = json.load(open(bstack1l1l111l1_opy_, bstack1lllll1l_opy_ (u"ࠬࡸࡢࠨঢ়")))
    if md5_hash in bstack1111l11l1_opy_:
      bstack1ll11l1l_opy_ = bstack1111l11l1_opy_[md5_hash]
      bstack1l1ll1ll1l_opy_ = datetime.datetime.now()
      bstack1l1111lll_opy_ = datetime.datetime.strptime(bstack1ll11l1l_opy_[bstack1lllll1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ৞")], bstack1lllll1l_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫয়"))
      if (bstack1l1ll1ll1l_opy_ - bstack1l1111lll_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1ll11l1l_opy_[bstack1lllll1l_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ৠ")]):
        return None
      return bstack1ll11l1l_opy_[bstack1lllll1l_opy_ (u"ࠩ࡬ࡨࠬৡ")]
  else:
    return None
def bstack11lllll1l_opy_(md5_hash, bstack1ll111111l_opy_):
  bstack111llll11_opy_ = os.path.join(os.path.expanduser(bstack1lllll1l_opy_ (u"ࠪࢂࠬৢ")), bstack1lllll1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫৣ"))
  if not os.path.exists(bstack111llll11_opy_):
    os.makedirs(bstack111llll11_opy_)
  bstack1l1l111l1_opy_ = os.path.join(os.path.expanduser(bstack1lllll1l_opy_ (u"ࠬࢄࠧ৤")), bstack1lllll1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭৥"), bstack1lllll1l_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ০"))
  bstack1ll11l1l1_opy_ = {
    bstack1lllll1l_opy_ (u"ࠨ࡫ࡧࠫ১"): bstack1ll111111l_opy_,
    bstack1lllll1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ২"): datetime.datetime.strftime(datetime.datetime.now(), bstack1lllll1l_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧ৩")),
    bstack1lllll1l_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ৪"): str(__version__)
  }
  if os.path.exists(bstack1l1l111l1_opy_):
    bstack1111l11l1_opy_ = json.load(open(bstack1l1l111l1_opy_, bstack1lllll1l_opy_ (u"ࠬࡸࡢࠨ৫")))
  else:
    bstack1111l11l1_opy_ = {}
  bstack1111l11l1_opy_[md5_hash] = bstack1ll11l1l1_opy_
  with open(bstack1l1l111l1_opy_, bstack1lllll1l_opy_ (u"ࠨࡷࠬࠤ৬")) as outfile:
    json.dump(bstack1111l11l1_opy_, outfile)
def bstack1l11l11l_opy_(self):
  return
def bstack1l11ll1ll_opy_(self):
  return
def bstack1l1l111ll_opy_(self):
  global bstack111l111ll_opy_
  bstack111l111ll_opy_(self)
def bstack1ll1111l_opy_():
  global bstack1l1ll1l1ll_opy_
  bstack1l1ll1l1ll_opy_ = True
def bstack11l11ll11_opy_(self):
  global bstack1ll1lllll1_opy_
  global bstack111llll1l_opy_
  global bstack11111ll11_opy_
  try:
    if bstack1lllll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ৭") in bstack1ll1lllll1_opy_ and self.session_id != None and bstack11l1l11l1_opy_(threading.current_thread(), bstack1lllll1l_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬ৮"), bstack1lllll1l_opy_ (u"ࠩࠪ৯")) != bstack1lllll1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫৰ"):
      bstack1llll1l1ll_opy_ = bstack1lllll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫৱ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1lllll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ৲")
      if bstack1llll1l1ll_opy_ == bstack1lllll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭৳"):
        bstack1l1llll11_opy_(logger)
      if self != None:
        bstack11lll1ll1_opy_(self, bstack1llll1l1ll_opy_, bstack1lllll1l_opy_ (u"ࠧ࠭ࠢࠪ৴").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1lllll1l_opy_ (u"ࠨࠩ৵")
  except Exception as e:
    logger.debug(bstack1lllll1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥ৶") + str(e))
  bstack11111ll11_opy_(self)
  self.session_id = None
def bstack11lll1l1_opy_(self, command_executor=bstack1lllll1l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲࠵࠷࠽࠮࠱࠰࠳࠲࠶ࡀ࠴࠵࠶࠷ࠦ৷"), *args, **kwargs):
  bstack111l1l1ll_opy_ = bstack1lllll111_opy_(self, command_executor, *args, **kwargs)
  try:
    logger.debug(bstack1lllll1l_opy_ (u"ࠫࡈࡵ࡭࡮ࡣࡱࡨࠥࡋࡸࡦࡥࡸࡸࡴࡸࠠࡸࡪࡨࡲࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤ࡫ࡧ࡬ࡴࡧࠣ࠱ࠥࢁࡽࠨ৸").format(str(command_executor)))
    logger.debug(bstack1lllll1l_opy_ (u"ࠬࡎࡵࡣࠢࡘࡖࡑࠦࡩࡴࠢ࠰ࠤࢀࢃࠧ৹").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1lllll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ৺") in command_executor._url:
      bstack1ll1ll1l1_opy_.bstack11111l1l1_opy_(bstack1lllll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ৻"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1lllll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫৼ") in command_executor):
    bstack1ll1ll1l1_opy_.bstack11111l1l1_opy_(bstack1lllll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ৽"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l1ll111ll_opy_.bstack1ll1llll1l_opy_(self)
  return bstack111l1l1ll_opy_
def bstack111lllll_opy_(self, driver_command, *args, **kwargs):
  global bstack1l1l11111_opy_
  response = bstack1l1l11111_opy_(self, driver_command, *args, **kwargs)
  try:
    if driver_command == bstack1lllll1l_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ৾"):
      bstack1l1ll111ll_opy_.bstack1l11ll1l1_opy_({
          bstack1lllll1l_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ৿"): response[bstack1lllll1l_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ਀")],
          bstack1lllll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ਁ"): bstack1l1ll111ll_opy_.current_test_uuid() if bstack1l1ll111ll_opy_.current_test_uuid() else bstack1l1ll111ll_opy_.current_hook_uuid()
      })
  except:
    pass
  return response
def bstack11l1ll11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack111llll1l_opy_
  global bstack1llll11l_opy_
  global bstack1ll1l1l11l_opy_
  global bstack1l11l1l1_opy_
  global bstack1llll1l1_opy_
  global bstack1ll1lllll1_opy_
  global bstack1lllll111_opy_
  global bstack1l1llll111_opy_
  global bstack1l1lll1ll_opy_
  global bstack1lllll1111_opy_
  CONFIG[bstack1lllll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩਂ")] = str(bstack1ll1lllll1_opy_) + str(__version__)
  command_executor = bstack1ll1l1l11_opy_()
  logger.debug(bstack11111l11_opy_.format(command_executor))
  proxy = bstack1ll1lllll_opy_(CONFIG, proxy)
  bstack111l1l111_opy_ = 0 if bstack1llll11l_opy_ < 0 else bstack1llll11l_opy_
  try:
    if bstack1l11l1l1_opy_ is True:
      bstack111l1l111_opy_ = int(multiprocessing.current_process().name)
    elif bstack1llll1l1_opy_ is True:
      bstack111l1l111_opy_ = int(threading.current_thread().name)
  except:
    bstack111l1l111_opy_ = 0
  bstack1l111llll_opy_ = bstack1l1ll111l_opy_(CONFIG, bstack111l1l111_opy_)
  logger.debug(bstack111111111_opy_.format(str(bstack1l111llll_opy_)))
  if bstack1lllll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬਃ") in CONFIG and bstack11l1l1ll_opy_(CONFIG[bstack1lllll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭਄")]):
    bstack11llllll_opy_(bstack1l111llll_opy_)
  if desired_capabilities:
    bstack11l11111_opy_ = bstack1l1lll1l11_opy_(desired_capabilities)
    bstack11l11111_opy_[bstack1lllll1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪਅ")] = bstack1l1l11l1l1_opy_(CONFIG)
    bstack1111l111l_opy_ = bstack1l1ll111l_opy_(bstack11l11111_opy_)
    if bstack1111l111l_opy_:
      bstack1l111llll_opy_ = update(bstack1111l111l_opy_, bstack1l111llll_opy_)
    desired_capabilities = None
  if options:
    bstack1l1lll11l1_opy_(options, bstack1l111llll_opy_)
  if not options:
    options = bstack11llll11_opy_(bstack1l111llll_opy_)
  bstack1lllll1111_opy_ = CONFIG.get(bstack1lllll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਆ"))[bstack111l1l111_opy_]
  if bstack1l1ll11l1_opy_.bstack1111lllll_opy_(CONFIG, bstack111l1l111_opy_) and bstack1l1ll11l1_opy_.bstack1l1lll1ll1_opy_(bstack1l111llll_opy_, options):
    threading.current_thread().a11yPlatform = True
    bstack1l1ll11l1_opy_.set_capabilities(bstack1l111llll_opy_, CONFIG)
  if proxy and bstack1l11ll1l_opy_() >= version.parse(bstack1lllll1l_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬਇ")):
    options.proxy(proxy)
  if options and bstack1l11ll1l_opy_() >= version.parse(bstack1lllll1l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬਈ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1l11ll1l_opy_() < version.parse(bstack1lllll1l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ਉ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l111llll_opy_)
  logger.info(bstack1ll11111_opy_)
  if bstack1l11ll1l_opy_() >= version.parse(bstack1lllll1l_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨਊ")):
    bstack1lllll111_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l11ll1l_opy_() >= version.parse(bstack1lllll1l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ਋")):
    bstack1lllll111_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l11ll1l_opy_() >= version.parse(bstack1lllll1l_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪ਌")):
    bstack1lllll111_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1lllll111_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack11l1l11l_opy_ = bstack1lllll1l_opy_ (u"ࠫࠬ਍")
    if bstack1l11ll1l_opy_() >= version.parse(bstack1lllll1l_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭਎")):
      bstack11l1l11l_opy_ = self.caps.get(bstack1lllll1l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨਏ"))
    else:
      bstack11l1l11l_opy_ = self.capabilities.get(bstack1lllll1l_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢਐ"))
    if bstack11l1l11l_opy_:
      bstack1llllllll1_opy_(bstack11l1l11l_opy_)
      if bstack1l11ll1l_opy_() <= version.parse(bstack1lllll1l_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ਑")):
        self.command_executor._url = bstack1lllll1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ਒") + bstack11l111l1_opy_ + bstack1lllll1l_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢਓ")
      else:
        self.command_executor._url = bstack1lllll1l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨਔ") + bstack11l1l11l_opy_ + bstack1lllll1l_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨਕ")
      logger.debug(bstack1111ll1ll_opy_.format(bstack11l1l11l_opy_))
    else:
      logger.debug(bstack11ll11111_opy_.format(bstack1lllll1l_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢਖ")))
  except Exception as e:
    logger.debug(bstack11ll11111_opy_.format(e))
  if bstack1lllll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ਗ") in bstack1ll1lllll1_opy_:
    bstack1l1l11l11l_opy_(bstack1llll11l_opy_, bstack1l1lll1ll_opy_)
  bstack111llll1l_opy_ = self.session_id
  if bstack1lllll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਘ") in bstack1ll1lllll1_opy_ or bstack1lllll1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩਙ") in bstack1ll1lllll1_opy_ or bstack1lllll1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩਚ") in bstack1ll1lllll1_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1l1ll111ll_opy_.bstack1ll1llll1l_opy_(self)
  bstack1l1llll111_opy_.append(self)
  if bstack1lllll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਛ") in CONFIG and bstack1lllll1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪਜ") in CONFIG[bstack1lllll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਝ")][bstack111l1l111_opy_]:
    bstack1ll1l1l11l_opy_ = CONFIG[bstack1lllll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪਞ")][bstack111l1l111_opy_][bstack1lllll1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ਟ")]
  logger.debug(bstack1111lll1l_opy_.format(bstack111llll1l_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1111l11ll_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack11l111ll_opy_
      if(bstack1lllll1l_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸ࠯࡬ࡶࠦਠ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1lllll1l_opy_ (u"ࠪࢂࠬਡ")), bstack1lllll1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫਢ"), bstack1lllll1l_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧਣ")), bstack1lllll1l_opy_ (u"࠭ࡷࠨਤ")) as fp:
          fp.write(bstack1lllll1l_opy_ (u"ࠢࠣਥ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1lllll1l_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥਦ")))):
          with open(args[1], bstack1lllll1l_opy_ (u"ࠩࡵࠫਧ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1lllll1l_opy_ (u"ࠪࡥࡸࡿ࡮ࡤࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡤࡴࡥࡸࡒࡤ࡫ࡪ࠮ࡣࡰࡰࡷࡩࡽࡺࠬࠡࡲࡤ࡫ࡪࠦ࠽ࠡࡸࡲ࡭ࡩࠦ࠰ࠪࠩਨ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11111lll_opy_)
            lines.insert(1, bstack1lll1llll1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1lllll1l_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ਩")), bstack1lllll1l_opy_ (u"ࠬࡽࠧਪ")) as bstack111111l11_opy_:
              bstack111111l11_opy_.writelines(lines)
        CONFIG[bstack1lllll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨਫ")] = str(bstack1ll1lllll1_opy_) + str(__version__)
        bstack111l1l111_opy_ = 0 if bstack1llll11l_opy_ < 0 else bstack1llll11l_opy_
        try:
          if bstack1l11l1l1_opy_ is True:
            bstack111l1l111_opy_ = int(multiprocessing.current_process().name)
          elif bstack1llll1l1_opy_ is True:
            bstack111l1l111_opy_ = int(threading.current_thread().name)
        except:
          bstack111l1l111_opy_ = 0
        CONFIG[bstack1lllll1l_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢਬ")] = False
        CONFIG[bstack1lllll1l_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢਭ")] = True
        bstack1l111llll_opy_ = bstack1l1ll111l_opy_(CONFIG, bstack111l1l111_opy_)
        logger.debug(bstack111111111_opy_.format(str(bstack1l111llll_opy_)))
        if CONFIG.get(bstack1lllll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ਮ")):
          bstack11llllll_opy_(bstack1l111llll_opy_)
        if bstack1lllll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਯ") in CONFIG and bstack1lllll1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩਰ") in CONFIG[bstack1lllll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ਱")][bstack111l1l111_opy_]:
          bstack1ll1l1l11l_opy_ = CONFIG[bstack1lllll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਲ")][bstack111l1l111_opy_][bstack1lllll1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬਲ਼")]
        args.append(os.path.join(os.path.expanduser(bstack1lllll1l_opy_ (u"ࠨࢀࠪ਴")), bstack1lllll1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩਵ"), bstack1lllll1l_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬਸ਼")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1l111llll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1lllll1l_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ਷"))
      bstack11l111ll_opy_ = True
      return bstack1l1lll11ll_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack11l11l11l_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1llll11l_opy_
    global bstack1ll1l1l11l_opy_
    global bstack1l11l1l1_opy_
    global bstack1llll1l1_opy_
    global bstack1ll1lllll1_opy_
    CONFIG[bstack1lllll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧਸ")] = str(bstack1ll1lllll1_opy_) + str(__version__)
    bstack111l1l111_opy_ = 0 if bstack1llll11l_opy_ < 0 else bstack1llll11l_opy_
    try:
      if bstack1l11l1l1_opy_ is True:
        bstack111l1l111_opy_ = int(multiprocessing.current_process().name)
      elif bstack1llll1l1_opy_ is True:
        bstack111l1l111_opy_ = int(threading.current_thread().name)
    except:
      bstack111l1l111_opy_ = 0
    CONFIG[bstack1lllll1l_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧਹ")] = True
    bstack1l111llll_opy_ = bstack1l1ll111l_opy_(CONFIG, bstack111l1l111_opy_)
    logger.debug(bstack111111111_opy_.format(str(bstack1l111llll_opy_)))
    if CONFIG.get(bstack1lllll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ਺")):
      bstack11llllll_opy_(bstack1l111llll_opy_)
    if bstack1lllll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ਻") in CONFIG and bstack1lllll1l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫਼ࠧ") in CONFIG[bstack1lllll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭਽")][bstack111l1l111_opy_]:
      bstack1ll1l1l11l_opy_ = CONFIG[bstack1lllll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਾ")][bstack111l1l111_opy_][bstack1lllll1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪਿ")]
    import urllib
    import json
    bstack1ll11l11l1_opy_ = bstack1lllll1l_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨੀ") + urllib.parse.quote(json.dumps(bstack1l111llll_opy_))
    browser = self.connect(bstack1ll11l11l1_opy_)
    return browser
except Exception as e:
    pass
def bstack1ll11lll1_opy_():
    global bstack11l111ll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack11l11l11l_opy_
        bstack11l111ll_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1111l11ll_opy_
      bstack11l111ll_opy_ = True
    except Exception as e:
      pass
def bstack1l1l1l1l11_opy_(context, bstack11llll111_opy_):
  try:
    context.page.evaluate(bstack1lllll1l_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣੁ"), bstack1lllll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬੂ")+ json.dumps(bstack11llll111_opy_) + bstack1lllll1l_opy_ (u"ࠤࢀࢁࠧ੃"))
  except Exception as e:
    logger.debug(bstack1lllll1l_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣ੄"), e)
def bstack1l1l1l1l1l_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1lllll1l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧ੅"), bstack1lllll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ੆") + json.dumps(message) + bstack1lllll1l_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩੇ") + json.dumps(level) + bstack1lllll1l_opy_ (u"ࠧࡾࡿࠪੈ"))
  except Exception as e:
    logger.debug(bstack1lllll1l_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦ੉"), e)
def bstack1lll1l111l_opy_(self, url):
  global bstack1ll1111lll_opy_
  try:
    bstack1lllll111l_opy_(url)
  except Exception as err:
    logger.debug(bstack1lllll1l11_opy_.format(str(err)))
  try:
    bstack1ll1111lll_opy_(self, url)
  except Exception as e:
    try:
      bstack1lll11l11_opy_ = str(e)
      if any(err_msg in bstack1lll11l11_opy_ for err_msg in bstack1l11l11ll_opy_):
        bstack1lllll111l_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1lllll1l11_opy_.format(str(err)))
    raise e
def bstack1llllllll_opy_(self):
  global bstack1l11l111_opy_
  bstack1l11l111_opy_ = self
  return
def bstack1lllll1ll_opy_(self):
  global bstack1lll11l1_opy_
  bstack1lll11l1_opy_ = self
  return
def bstack1ll1l111ll_opy_(self, test):
  global CONFIG
  global bstack1lll1l11l1_opy_
  if CONFIG.get(bstack1lllll1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ੊"), False):
    test_name = str(test.data)
    bstack1llll11l1l_opy_ = str(test.source)
    bstack1l1l11lll1_opy_ = os.path.relpath(bstack1llll11l1l_opy_, start=os.getcwd())
    suite_name, bstack11l1llll_opy_ = os.path.splitext(bstack1l1l11lll1_opy_)
    bstack1llll1lll1_opy_ = suite_name + bstack1lllll1l_opy_ (u"ࠥ࠱ࠧੋ") + test_name
    threading.current_thread().percySessionName = bstack1llll1lll1_opy_
  bstack1lll1l11l1_opy_(self, test)
def bstack111111lll_opy_(self, test):
  global CONFIG
  global bstack1lll11l1_opy_
  global bstack1l11l111_opy_
  global bstack111llll1l_opy_
  global bstack1l11111ll_opy_
  global bstack1ll1l1l11l_opy_
  global bstack1l1l1111_opy_
  global bstack1lll1l111_opy_
  global bstack1lllll11l1_opy_
  global bstack1ll1l1l1l_opy_
  global bstack1l1llll111_opy_
  global bstack1lllll1111_opy_
  try:
    if not bstack111llll1l_opy_:
      with open(os.path.join(os.path.expanduser(bstack1lllll1l_opy_ (u"ࠫࢃ࠭ੌ")), bstack1lllll1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯੍ࠬ"), bstack1lllll1l_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ੎"))) as f:
        bstack111ll111l_opy_ = json.loads(bstack1lllll1l_opy_ (u"ࠢࡼࠤ੏") + f.read().strip() + bstack1lllll1l_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤࠪ੐") + bstack1lllll1l_opy_ (u"ࠤࢀࠦੑ"))
        bstack111llll1l_opy_ = bstack111ll111l_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1l1llll111_opy_:
    for driver in bstack1l1llll111_opy_:
      if bstack111llll1l_opy_ == driver.session_id:
        if test:
          bstack1llll1lll1_opy_ = str(test.data)
          if CONFIG.get(bstack1lllll1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ੒"), False):
            if CONFIG.get(bstack1lllll1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧ੓"), bstack1lllll1l_opy_ (u"ࠧࡧࡵࡵࡱࠥ੔")) == bstack1lllll1l_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣ੕"):
              bstack1llll111_opy_ = bstack11l1l11l1_opy_(threading.current_thread(), bstack1lllll1l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ੖"), None)
              bstack111ll1111_opy_(driver, bstack1llll111_opy_)
          if bstack11l1l11l1_opy_(threading.current_thread(), bstack1lllll1l_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ੗"), None) and bstack11l1l11l1_opy_(threading.current_thread(), bstack1lllll1l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ੘"), None):
            logger.info(bstack1lllll1l_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠡࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡶࡼࡧࡹ࠯ࠢࠥਖ਼"))
            bstack1l1ll11l1_opy_.bstack1ll1111l1l_opy_(driver, class_name=test.parent.name, name=test.name, module_name=None, path=test.source, bstack1ll111ll_opy_=bstack1lllll1111_opy_)
        if not bstack1l1l1ll1ll_opy_ and bstack1llll1lll1_opy_:
          bstack1lll1l1lll_opy_ = {
            bstack1lllll1l_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫਗ਼"): bstack1lllll1l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ਜ਼"),
            bstack1lllll1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩੜ"): {
              bstack1lllll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ੝"): bstack1llll1lll1_opy_
            }
          }
          bstack1l1ll1llll_opy_ = bstack1lllll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ਫ਼").format(json.dumps(bstack1lll1l1lll_opy_))
          driver.execute_script(bstack1l1ll1llll_opy_)
        if bstack1l11111ll_opy_:
          bstack1l1llll1ll_opy_ = {
            bstack1lllll1l_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ੟"): bstack1lllll1l_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ੠"),
            bstack1lllll1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ੡"): {
              bstack1lllll1l_opy_ (u"ࠬࡪࡡࡵࡣࠪ੢"): bstack1llll1lll1_opy_ + bstack1lllll1l_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨ੣"),
              bstack1lllll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭੤"): bstack1lllll1l_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭੥")
            }
          }
          if bstack1l11111ll_opy_.status == bstack1lllll1l_opy_ (u"ࠩࡓࡅࡘ࡙ࠧ੦"):
            bstack11l1lllll_opy_ = bstack1lllll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ੧").format(json.dumps(bstack1l1llll1ll_opy_))
            driver.execute_script(bstack11l1lllll_opy_)
            bstack11lll1ll1_opy_(driver, bstack1lllll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ੨"))
          elif bstack1l11111ll_opy_.status == bstack1lllll1l_opy_ (u"ࠬࡌࡁࡊࡎࠪ੩"):
            reason = bstack1lllll1l_opy_ (u"ࠨࠢ੪")
            bstack1l1lll1111_opy_ = bstack1llll1lll1_opy_ + bstack1lllll1l_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠨ੫")
            if bstack1l11111ll_opy_.message:
              reason = str(bstack1l11111ll_opy_.message)
              bstack1l1lll1111_opy_ = bstack1l1lll1111_opy_ + bstack1lllll1l_opy_ (u"ࠨࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࠨ੬") + reason
            bstack1l1llll1ll_opy_[bstack1lllll1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ੭")] = {
              bstack1lllll1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ੮"): bstack1lllll1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ੯"),
              bstack1lllll1l_opy_ (u"ࠬࡪࡡࡵࡣࠪੰ"): bstack1l1lll1111_opy_
            }
            bstack11l1lllll_opy_ = bstack1lllll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫੱ").format(json.dumps(bstack1l1llll1ll_opy_))
            driver.execute_script(bstack11l1lllll_opy_)
            bstack11lll1ll1_opy_(driver, bstack1lllll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧੲ"), reason)
            bstack11ll1llll_opy_(reason, str(bstack1l11111ll_opy_), str(bstack1llll11l_opy_), logger)
  elif bstack111llll1l_opy_:
    try:
      data = {}
      bstack1llll1lll1_opy_ = None
      if test:
        bstack1llll1lll1_opy_ = str(test.data)
      if not bstack1l1l1ll1ll_opy_ and bstack1llll1lll1_opy_:
        data[bstack1lllll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ੳ")] = bstack1llll1lll1_opy_
      if bstack1l11111ll_opy_:
        if bstack1l11111ll_opy_.status == bstack1lllll1l_opy_ (u"ࠩࡓࡅࡘ࡙ࠧੴ"):
          data[bstack1lllll1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪੵ")] = bstack1lllll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ੶")
        elif bstack1l11111ll_opy_.status == bstack1lllll1l_opy_ (u"ࠬࡌࡁࡊࡎࠪ੷"):
          data[bstack1lllll1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭੸")] = bstack1lllll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ੹")
          if bstack1l11111ll_opy_.message:
            data[bstack1lllll1l_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ੺")] = str(bstack1l11111ll_opy_.message)
      user = CONFIG[bstack1lllll1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ੻")]
      key = CONFIG[bstack1lllll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭੼")]
      url = bstack1lllll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠰ࡽࢀ࠲࡯ࡹ࡯࡯ࠩ੽").format(user, key, bstack111llll1l_opy_)
      headers = {
        bstack1lllll1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ੾"): bstack1lllll1l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ੿"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1ll1111111_opy_.format(str(e)))
  if bstack1lll11l1_opy_:
    bstack1lll1l111_opy_(bstack1lll11l1_opy_)
  if bstack1l11l111_opy_:
    bstack1lllll11l1_opy_(bstack1l11l111_opy_)
  if bstack1l1ll1l1ll_opy_:
    bstack1ll1l1l1l_opy_()
  bstack1l1l1111_opy_(self, test)
def bstack1l1lll1lll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1l1l1ll1l1_opy_
  global CONFIG
  global bstack1l1llll111_opy_
  global bstack111llll1l_opy_
  bstack11ll1111l_opy_ = None
  try:
    if bstack11l1l11l1_opy_(threading.current_thread(), bstack1lllll1l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭઀"), None):
      try:
        if not bstack111llll1l_opy_:
          with open(os.path.join(os.path.expanduser(bstack1lllll1l_opy_ (u"ࠨࢀࠪઁ")), bstack1lllll1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩં"), bstack1lllll1l_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬઃ"))) as f:
            bstack111ll111l_opy_ = json.loads(bstack1lllll1l_opy_ (u"ࠦࢀࠨ઄") + f.read().strip() + bstack1lllll1l_opy_ (u"ࠬࠨࡸࠣ࠼ࠣࠦࡾࠨࠧઅ") + bstack1lllll1l_opy_ (u"ࠨࡽࠣઆ"))
            bstack111llll1l_opy_ = bstack111ll111l_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1l1llll111_opy_:
        for driver in bstack1l1llll111_opy_:
          if bstack111llll1l_opy_ == driver.session_id:
            bstack11ll1111l_opy_ = driver
    bstack1l1ll1ll1_opy_ = bstack1l1ll11l1_opy_.bstack111111ll_opy_(CONFIG, test.tags)
    if bstack11ll1111l_opy_:
      threading.current_thread().isA11yTest = bstack1l1ll11l1_opy_.bstack1lll1111l_opy_(bstack11ll1111l_opy_, bstack1l1ll1ll1_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1l1ll1ll1_opy_
  except:
    pass
  bstack1l1l1ll1l1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l11111ll_opy_
  bstack1l11111ll_opy_ = self._test
def bstack1l11111l_opy_():
  global bstack1l1llllll_opy_
  try:
    if os.path.exists(bstack1l1llllll_opy_):
      os.remove(bstack1l1llllll_opy_)
  except Exception as e:
    logger.debug(bstack1lllll1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪઇ") + str(e))
def bstack11l1l1ll1_opy_():
  global bstack1l1llllll_opy_
  bstack1ll1l11ll_opy_ = {}
  try:
    if not os.path.isfile(bstack1l1llllll_opy_):
      with open(bstack1l1llllll_opy_, bstack1lllll1l_opy_ (u"ࠨࡹࠪઈ")):
        pass
      with open(bstack1l1llllll_opy_, bstack1lllll1l_opy_ (u"ࠤࡺ࠯ࠧઉ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1l1llllll_opy_):
      bstack1ll1l11ll_opy_ = json.load(open(bstack1l1llllll_opy_, bstack1lllll1l_opy_ (u"ࠪࡶࡧ࠭ઊ")))
  except Exception as e:
    logger.debug(bstack1lllll1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ઋ") + str(e))
  finally:
    return bstack1ll1l11ll_opy_
def bstack1l1l11l11l_opy_(platform_index, item_index):
  global bstack1l1llllll_opy_
  try:
    bstack1ll1l11ll_opy_ = bstack11l1l1ll1_opy_()
    bstack1ll1l11ll_opy_[item_index] = platform_index
    with open(bstack1l1llllll_opy_, bstack1lllll1l_opy_ (u"ࠧࡽࠫࠣઌ")) as outfile:
      json.dump(bstack1ll1l11ll_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1lllll1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫઍ") + str(e))
def bstack1l1l1ll1l_opy_(bstack1l1ll11lll_opy_):
  global CONFIG
  bstack1l1l1lll11_opy_ = bstack1lllll1l_opy_ (u"ࠧࠨ઎")
  if not bstack1lllll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫએ") in CONFIG:
    logger.info(bstack1lllll1l_opy_ (u"ࠩࡑࡳࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠡࡲࡤࡷࡸ࡫ࡤࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡲࡦࡲࡲࡶࡹࠦࡦࡰࡴࠣࡖࡴࡨ࡯ࡵࠢࡵࡹࡳ࠭ઐ"))
  try:
    platform = CONFIG[bstack1lllll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ઑ")][bstack1l1ll11lll_opy_]
    if bstack1lllll1l_opy_ (u"ࠫࡴࡹࠧ઒") in platform:
      bstack1l1l1lll11_opy_ += str(platform[bstack1lllll1l_opy_ (u"ࠬࡵࡳࠨઓ")]) + bstack1lllll1l_opy_ (u"࠭ࠬࠡࠩઔ")
    if bstack1lllll1l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪક") in platform:
      bstack1l1l1lll11_opy_ += str(platform[bstack1lllll1l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫખ")]) + bstack1lllll1l_opy_ (u"ࠩ࠯ࠤࠬગ")
    if bstack1lllll1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧઘ") in platform:
      bstack1l1l1lll11_opy_ += str(platform[bstack1lllll1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨઙ")]) + bstack1lllll1l_opy_ (u"ࠬ࠲ࠠࠨચ")
    if bstack1lllll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨછ") in platform:
      bstack1l1l1lll11_opy_ += str(platform[bstack1lllll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩજ")]) + bstack1lllll1l_opy_ (u"ࠨ࠮ࠣࠫઝ")
    if bstack1lllll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧઞ") in platform:
      bstack1l1l1lll11_opy_ += str(platform[bstack1lllll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨટ")]) + bstack1lllll1l_opy_ (u"ࠫ࠱ࠦࠧઠ")
    if bstack1lllll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ડ") in platform:
      bstack1l1l1lll11_opy_ += str(platform[bstack1lllll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧઢ")]) + bstack1lllll1l_opy_ (u"ࠧ࠭ࠢࠪણ")
  except Exception as e:
    logger.debug(bstack1lllll1l_opy_ (u"ࠨࡕࡲࡱࡪࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡷ࡫ࡰࡰࡴࡷࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡵ࡮ࠨત") + str(e))
  finally:
    if bstack1l1l1lll11_opy_[len(bstack1l1l1lll11_opy_) - 2:] == bstack1lllll1l_opy_ (u"ࠩ࠯ࠤࠬથ"):
      bstack1l1l1lll11_opy_ = bstack1l1l1lll11_opy_[:-2]
    return bstack1l1l1lll11_opy_
def bstack1l1l1lll_opy_(path, bstack1l1l1lll11_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack11ll11ll_opy_ = ET.parse(path)
    bstack111l11l1l_opy_ = bstack11ll11ll_opy_.getroot()
    bstack1lllll1l1l_opy_ = None
    for suite in bstack111l11l1l_opy_.iter(bstack1lllll1l_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩદ")):
      if bstack1lllll1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫધ") in suite.attrib:
        suite.attrib[bstack1lllll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪન")] += bstack1lllll1l_opy_ (u"࠭ࠠࠨ઩") + bstack1l1l1lll11_opy_
        bstack1lllll1l1l_opy_ = suite
    bstack1l1ll1l1l1_opy_ = None
    for robot in bstack111l11l1l_opy_.iter(bstack1lllll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭પ")):
      bstack1l1ll1l1l1_opy_ = robot
    bstack1lll1lll_opy_ = len(bstack1l1ll1l1l1_opy_.findall(bstack1lllll1l_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧફ")))
    if bstack1lll1lll_opy_ == 1:
      bstack1l1ll1l1l1_opy_.remove(bstack1l1ll1l1l1_opy_.findall(bstack1lllll1l_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨબ"))[0])
      bstack1lll11lll_opy_ = ET.Element(bstack1lllll1l_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩભ"), attrib={bstack1lllll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩમ"): bstack1lllll1l_opy_ (u"࡙ࠬࡵࡪࡶࡨࡷࠬય"), bstack1lllll1l_opy_ (u"࠭ࡩࡥࠩર"): bstack1lllll1l_opy_ (u"ࠧࡴ࠲ࠪ઱")})
      bstack1l1ll1l1l1_opy_.insert(1, bstack1lll11lll_opy_)
      bstack111ll1ll_opy_ = None
      for suite in bstack1l1ll1l1l1_opy_.iter(bstack1lllll1l_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧલ")):
        bstack111ll1ll_opy_ = suite
      bstack111ll1ll_opy_.append(bstack1lllll1l1l_opy_)
      bstack1l1lllll11_opy_ = None
      for status in bstack1lllll1l1l_opy_.iter(bstack1lllll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩળ")):
        bstack1l1lllll11_opy_ = status
      bstack111ll1ll_opy_.append(bstack1l1lllll11_opy_)
    bstack11ll11ll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1lllll1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠨ઴") + str(e))
def bstack11l1lll11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1111111l_opy_
  global CONFIG
  if bstack1lllll1l_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣવ") in options:
    del options[bstack1lllll1l_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤશ")]
  bstack11ll111l1_opy_ = bstack11l1l1ll1_opy_()
  for bstack11111l11l_opy_ in bstack11ll111l1_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1lllll1l_opy_ (u"࠭ࡰࡢࡤࡲࡸࡤࡸࡥࡴࡷ࡯ࡸࡸ࠭ષ"), str(bstack11111l11l_opy_), bstack1lllll1l_opy_ (u"ࠧࡰࡷࡷࡴࡺࡺ࠮ࡹ࡯࡯ࠫસ"))
    bstack1l1l1lll_opy_(path, bstack1l1l1ll1l_opy_(bstack11ll111l1_opy_[bstack11111l11l_opy_]))
  bstack1l11111l_opy_()
  return bstack1111111l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1ll1llll1_opy_(self, ff_profile_dir):
  global bstack1lllllll1l_opy_
  if not ff_profile_dir:
    return None
  return bstack1lllllll1l_opy_(self, ff_profile_dir)
def bstack11111l1ll_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l1l1l1lll_opy_
  bstack11ll1111_opy_ = []
  if bstack1lllll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫહ") in CONFIG:
    bstack11ll1111_opy_ = CONFIG[bstack1lllll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ઺")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1lllll1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦ઻")],
      pabot_args[bstack1lllll1l_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩ઼ࠧ")],
      argfile,
      pabot_args.get(bstack1lllll1l_opy_ (u"ࠧ࡮ࡩࡷࡧࠥઽ")),
      pabot_args[bstack1lllll1l_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤા")],
      platform[0],
      bstack1l1l1l1lll_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1lllll1l_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢિ")] or [(bstack1lllll1l_opy_ (u"ࠣࠤી"), None)]
    for platform in enumerate(bstack11ll1111_opy_)
  ]
def bstack1lll11l111_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1ll1l1l111_opy_=bstack1lllll1l_opy_ (u"ࠩࠪુ")):
  global bstack1ll1l1111l_opy_
  self.platform_index = platform_index
  self.bstack111l1l11_opy_ = bstack1ll1l1l111_opy_
  bstack1ll1l1111l_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack111l111l1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1lll11l1l1_opy_
  global bstack1l1llll11l_opy_
  if not bstack1lllll1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬૂ") in item.options:
    item.options[bstack1lllll1l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ૃ")] = []
  for v in item.options[bstack1lllll1l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧૄ")]:
    if bstack1lllll1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬૅ") in v:
      item.options[bstack1lllll1l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ૆")].remove(v)
    if bstack1lllll1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨે") in v:
      item.options[bstack1lllll1l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫૈ")].remove(v)
  item.options[bstack1lllll1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬૉ")].insert(0, bstack1lllll1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚࠽ࡿࢂ࠭૊").format(item.platform_index))
  item.options[bstack1lllll1l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧો")].insert(0, bstack1lllll1l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔ࠽ࡿࢂ࠭ૌ").format(item.bstack111l1l11_opy_))
  if bstack1l1llll11l_opy_:
    item.options[bstack1lllll1l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦ્ࠩ")].insert(0, bstack1lllll1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓ࠻ࡽࢀࠫ૎").format(bstack1l1llll11l_opy_))
  return bstack1lll11l1l1_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1l111ll1l_opy_(command, item_index):
  os.environ[bstack1lllll1l_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ૏")] = json.dumps(CONFIG[bstack1lllll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ૐ")][item_index % bstack1llll11111_opy_])
  global bstack1l1llll11l_opy_
  if bstack1l1llll11l_opy_:
    command[0] = command[0].replace(bstack1lllll1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ૑"), bstack1lllll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩ૒") + str(
      item_index) + bstack1lllll1l_opy_ (u"࠭ࠠࠨ૓") + bstack1l1llll11l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1lllll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭૔"),
                                    bstack1lllll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬ૕") + str(item_index), 1)
def bstack1lll111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1ll11l11ll_opy_
  bstack1l111ll1l_opy_(command, item_index)
  return bstack1ll11l11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1ll1l1llll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1ll11l11ll_opy_
  bstack1l111ll1l_opy_(command, item_index)
  return bstack1ll11l11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack11111l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1ll11l11ll_opy_
  bstack1l111ll1l_opy_(command, item_index)
  return bstack1ll11l11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack11ll1ll1l_opy_(self, runner, quiet=False, capture=True):
  global bstack1ll1l1lll_opy_
  bstack1lll11111l_opy_ = bstack1ll1l1lll_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1lllll1l_opy_ (u"ࠩࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࡤࡧࡲࡳࠩ૖")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1lllll1l_opy_ (u"ࠪࡩࡽࡩ࡟ࡵࡴࡤࡧࡪࡨࡡࡤ࡭ࡢࡥࡷࡸࠧ૗")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1lll11111l_opy_
def bstack111ll11l1_opy_(self, name, context, *args):
  os.environ[bstack1lllll1l_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬ૘")] = json.dumps(CONFIG[bstack1lllll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ૙")][int(threading.current_thread()._name) % bstack1llll11111_opy_])
  global bstack1l1l1llll1_opy_
  if name == bstack1lllll1l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧ૚"):
    bstack1l1l1llll1_opy_(self, name, context, *args)
    try:
      if not bstack1l1l1ll1ll_opy_:
        bstack11ll1111l_opy_ = threading.current_thread().bstackSessionDriver if bstack1lll1llll_opy_(bstack1lllll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭૛")) else context.browser
        bstack11llll111_opy_ = str(self.feature.name)
        bstack1l1l1l1l11_opy_(context, bstack11llll111_opy_)
        bstack11ll1111l_opy_.execute_script(bstack1lllll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭૜") + json.dumps(bstack11llll111_opy_) + bstack1lllll1l_opy_ (u"ࠩࢀࢁࠬ૝"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1lllll1l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ૞").format(str(e)))
  elif name == bstack1lllll1l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭૟"):
    bstack1l1l1llll1_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstack1lllll1l_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࡤࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧૠ")):
        self.driver_before_scenario = True
      if (not bstack1l1l1ll1ll_opy_):
        scenario_name = args[0].name
        feature_name = bstack11llll111_opy_ = str(self.feature.name)
        bstack11llll111_opy_ = feature_name + bstack1lllll1l_opy_ (u"࠭ࠠ࠮ࠢࠪૡ") + scenario_name
        bstack11ll1111l_opy_ = threading.current_thread().bstackSessionDriver if bstack1lll1llll_opy_(bstack1lllll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ૢ")) else context.browser
        if self.driver_before_scenario:
          bstack1l1l1l1l11_opy_(context, bstack11llll111_opy_)
          bstack11ll1111l_opy_.execute_script(bstack1lllll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ૣ") + json.dumps(bstack11llll111_opy_) + bstack1lllll1l_opy_ (u"ࠩࢀࢁࠬ૤"))
    except Exception as e:
      logger.debug(bstack1lllll1l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫ૥").format(str(e)))
  elif name == bstack1lllll1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ૦"):
    try:
      bstack11ll1lll1_opy_ = args[0].status.name
      bstack11ll1111l_opy_ = threading.current_thread().bstackSessionDriver if bstack1lllll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ૧") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack11ll1lll1_opy_).lower() == bstack1lllll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭૨"):
        bstack1ll1l11ll1_opy_ = bstack1lllll1l_opy_ (u"ࠧࠨ૩")
        bstack11l1ll1ll_opy_ = bstack1lllll1l_opy_ (u"ࠨࠩ૪")
        bstack11l1lll1l_opy_ = bstack1lllll1l_opy_ (u"ࠩࠪ૫")
        try:
          import traceback
          bstack1ll1l11ll1_opy_ = self.exception.__class__.__name__
          bstack11ll111l_opy_ = traceback.format_tb(self.exc_traceback)
          bstack11l1ll1ll_opy_ = bstack1lllll1l_opy_ (u"ࠪࠤࠬ૬").join(bstack11ll111l_opy_)
          bstack11l1lll1l_opy_ = bstack11ll111l_opy_[-1]
        except Exception as e:
          logger.debug(bstack11lllll11_opy_.format(str(e)))
        bstack1ll1l11ll1_opy_ += bstack11l1lll1l_opy_
        bstack1l1l1l1l1l_opy_(context, json.dumps(str(args[0].name) + bstack1lllll1l_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥ૭") + str(bstack11l1ll1ll_opy_)),
                            bstack1lllll1l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ૮"))
        if self.driver_before_scenario:
          bstack111lll111_opy_(getattr(context, bstack1lllll1l_opy_ (u"࠭ࡰࡢࡩࡨࠫ૯"), None), bstack1lllll1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ૰"), bstack1ll1l11ll1_opy_)
          bstack11ll1111l_opy_.execute_script(bstack1lllll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭૱") + json.dumps(str(args[0].name) + bstack1lllll1l_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ૲") + str(bstack11l1ll1ll_opy_)) + bstack1lllll1l_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪ૳"))
        if self.driver_before_scenario:
          bstack11lll1ll1_opy_(bstack11ll1111l_opy_, bstack1lllll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ૴"), bstack1lllll1l_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤ૵") + str(bstack1ll1l11ll1_opy_))
      else:
        bstack1l1l1l1l1l_opy_(context, bstack1lllll1l_opy_ (u"ࠨࡐࡢࡵࡶࡩࡩࠧࠢ૶"), bstack1lllll1l_opy_ (u"ࠢࡪࡰࡩࡳࠧ૷"))
        if self.driver_before_scenario:
          bstack111lll111_opy_(getattr(context, bstack1lllll1l_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭૸"), None), bstack1lllll1l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤૹ"))
        bstack11ll1111l_opy_.execute_script(bstack1lllll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨૺ") + json.dumps(str(args[0].name) + bstack1lllll1l_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣૻ")) + bstack1lllll1l_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫૼ"))
        if self.driver_before_scenario:
          bstack11lll1ll1_opy_(bstack11ll1111l_opy_, bstack1lllll1l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ૽"))
    except Exception as e:
      logger.debug(bstack1lllll1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ૾").format(str(e)))
  elif name == bstack1lllll1l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ૿"):
    try:
      bstack11ll1111l_opy_ = threading.current_thread().bstackSessionDriver if bstack1lll1llll_opy_(bstack1lllll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ଀")) else context.browser
      if context.failed is True:
        bstack1ll1111ll_opy_ = []
        bstack111lll1ll_opy_ = []
        bstack1ll111ll11_opy_ = []
        bstack1111l1l11_opy_ = bstack1lllll1l_opy_ (u"ࠪࠫଁ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1ll1111ll_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack11ll111l_opy_ = traceback.format_tb(exc_tb)
            bstack1lll11llll_opy_ = bstack1lllll1l_opy_ (u"ࠫࠥ࠭ଂ").join(bstack11ll111l_opy_)
            bstack111lll1ll_opy_.append(bstack1lll11llll_opy_)
            bstack1ll111ll11_opy_.append(bstack11ll111l_opy_[-1])
        except Exception as e:
          logger.debug(bstack11lllll11_opy_.format(str(e)))
        bstack1ll1l11ll1_opy_ = bstack1lllll1l_opy_ (u"ࠬ࠭ଃ")
        for i in range(len(bstack1ll1111ll_opy_)):
          bstack1ll1l11ll1_opy_ += bstack1ll1111ll_opy_[i] + bstack1ll111ll11_opy_[i] + bstack1lllll1l_opy_ (u"࠭࡜࡯ࠩ଄")
        bstack1111l1l11_opy_ = bstack1lllll1l_opy_ (u"ࠧࠡࠩଅ").join(bstack111lll1ll_opy_)
        if not self.driver_before_scenario:
          bstack1l1l1l1l1l_opy_(context, bstack1111l1l11_opy_, bstack1lllll1l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢଆ"))
          bstack111lll111_opy_(getattr(context, bstack1lllll1l_opy_ (u"ࠩࡳࡥ࡬࡫ࠧଇ"), None), bstack1lllll1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥଈ"), bstack1ll1l11ll1_opy_)
          bstack11ll1111l_opy_.execute_script(bstack1lllll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩଉ") + json.dumps(bstack1111l1l11_opy_) + bstack1lllll1l_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬଊ"))
          bstack11lll1ll1_opy_(bstack11ll1111l_opy_, bstack1lllll1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨଋ"), bstack1lllll1l_opy_ (u"ࠢࡔࡱࡰࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵࡳࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢ࡟ࡲࠧଌ") + str(bstack1ll1l11ll1_opy_))
          bstack1ll1l111_opy_ = bstack1l1l1l11_opy_(bstack1111l1l11_opy_, self.feature.name, logger)
          if (bstack1ll1l111_opy_ != None):
            bstack111l1111_opy_.append(bstack1ll1l111_opy_)
      else:
        if not self.driver_before_scenario:
          bstack1l1l1l1l1l_opy_(context, bstack1lllll1l_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦ଍") + str(self.feature.name) + bstack1lllll1l_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦ଎"), bstack1lllll1l_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣଏ"))
          bstack111lll111_opy_(getattr(context, bstack1lllll1l_opy_ (u"ࠫࡵࡧࡧࡦࠩଐ"), None), bstack1lllll1l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ଑"))
          bstack11ll1111l_opy_.execute_script(bstack1lllll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ଒") + json.dumps(bstack1lllll1l_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥଓ") + str(self.feature.name) + bstack1lllll1l_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥଔ")) + bstack1lllll1l_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨକ"))
          bstack11lll1ll1_opy_(bstack11ll1111l_opy_, bstack1lllll1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪଖ"))
          bstack1ll1l111_opy_ = bstack1l1l1l11_opy_(bstack1111l1l11_opy_, self.feature.name, logger)
          if (bstack1ll1l111_opy_ != None):
            bstack111l1111_opy_.append(bstack1ll1l111_opy_)
    except Exception as e:
      logger.debug(bstack1lllll1l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ଗ").format(str(e)))
  else:
    bstack1l1l1llll1_opy_(self, name, context, *args)
  if name in [bstack1lllll1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬଘ"), bstack1lllll1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧଙ")]:
    bstack1l1l1llll1_opy_(self, name, context, *args)
    if (name == bstack1lllll1l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨଚ") and self.driver_before_scenario) or (
            name == bstack1lllll1l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨଛ") and not self.driver_before_scenario):
      try:
        bstack11ll1111l_opy_ = threading.current_thread().bstackSessionDriver if bstack1lll1llll_opy_(bstack1lllll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨଜ")) else context.browser
        bstack11ll1111l_opy_.quit()
      except Exception:
        pass
def bstack111l11ll1_opy_(config, startdir):
  return bstack1lllll1l_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀ࠶ࡽࠣଝ").format(bstack1lllll1l_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥଞ"))
notset = Notset()
def bstack1ll1lll11l_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1ll11l1ll_opy_
  if str(name).lower() == bstack1lllll1l_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬଟ"):
    return bstack1lllll1l_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧଠ")
  else:
    return bstack1ll11l1ll_opy_(self, name, default, skip)
def bstack1111l1ll_opy_(item, when):
  global bstack1l1l1l1ll1_opy_
  try:
    bstack1l1l1l1ll1_opy_(item, when)
  except Exception as e:
    pass
def bstack1l1l1l11l1_opy_():
  return
def bstack111l1l11l_opy_(type, name, status, reason, bstack1l111l11_opy_, bstack1ll1111l11_opy_):
  bstack1lll1l1lll_opy_ = {
    bstack1lllll1l_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧଡ"): type,
    bstack1lllll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫଢ"): {}
  }
  if type == bstack1lllll1l_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫଣ"):
    bstack1lll1l1lll_opy_[bstack1lllll1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ତ")][bstack1lllll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪଥ")] = bstack1l111l11_opy_
    bstack1lll1l1lll_opy_[bstack1lllll1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨଦ")][bstack1lllll1l_opy_ (u"࠭ࡤࡢࡶࡤࠫଧ")] = json.dumps(str(bstack1ll1111l11_opy_))
  if type == bstack1lllll1l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨନ"):
    bstack1lll1l1lll_opy_[bstack1lllll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ଩")][bstack1lllll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧପ")] = name
  if type == bstack1lllll1l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ଫ"):
    bstack1lll1l1lll_opy_[bstack1lllll1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧବ")][bstack1lllll1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬଭ")] = status
    if status == bstack1lllll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ମ"):
      bstack1lll1l1lll_opy_[bstack1lllll1l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪଯ")][bstack1lllll1l_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨର")] = json.dumps(str(reason))
  bstack1l1ll1llll_opy_ = bstack1lllll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ଱").format(json.dumps(bstack1lll1l1lll_opy_))
  return bstack1l1ll1llll_opy_
def bstack1l1ll11ll1_opy_(driver_command, response):
    if driver_command == bstack1lllll1l_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧଲ"):
        bstack1l1ll111ll_opy_.bstack1l11ll1l1_opy_({
            bstack1lllll1l_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪଳ"): response[bstack1lllll1l_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ଴")],
            bstack1lllll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ଵ"): bstack1l1ll111ll_opy_.current_test_uuid()
        })
def bstack1l1ll1l111_opy_(item, call, rep):
  global bstack1ll111l11_opy_
  global bstack1l1llll111_opy_
  global bstack1l1l1ll1ll_opy_
  name = bstack1lllll1l_opy_ (u"ࠧࠨଶ")
  try:
    if rep.when == bstack1lllll1l_opy_ (u"ࠨࡥࡤࡰࡱ࠭ଷ"):
      bstack111llll1l_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1l1l1ll1ll_opy_:
          name = str(rep.nodeid)
          bstack1llllll1l_opy_ = bstack111l1l11l_opy_(bstack1lllll1l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪସ"), name, bstack1lllll1l_opy_ (u"ࠪࠫହ"), bstack1lllll1l_opy_ (u"ࠫࠬ଺"), bstack1lllll1l_opy_ (u"ࠬ࠭଻"), bstack1lllll1l_opy_ (u"଼࠭ࠧ"))
          threading.current_thread().bstack1l111l1l_opy_ = name
          for driver in bstack1l1llll111_opy_:
            if bstack111llll1l_opy_ == driver.session_id:
              driver.execute_script(bstack1llllll1l_opy_)
      except Exception as e:
        logger.debug(bstack1lllll1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧଽ").format(str(e)))
      try:
        bstack11l1111l_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1lllll1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩା"):
          status = bstack1lllll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩି") if rep.outcome.lower() == bstack1lllll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪୀ") else bstack1lllll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫୁ")
          reason = bstack1lllll1l_opy_ (u"ࠬ࠭ୂ")
          if status == bstack1lllll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ୃ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1lllll1l_opy_ (u"ࠧࡪࡰࡩࡳࠬୄ") if status == bstack1lllll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ୅") else bstack1lllll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ୆")
          data = name + bstack1lllll1l_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬେ") if status == bstack1lllll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫୈ") else name + bstack1lllll1l_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨ୉") + reason
          bstack1llll11l11_opy_ = bstack111l1l11l_opy_(bstack1lllll1l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ୊"), bstack1lllll1l_opy_ (u"ࠧࠨୋ"), bstack1lllll1l_opy_ (u"ࠨࠩୌ"), bstack1lllll1l_opy_ (u"୍ࠩࠪ"), level, data)
          for driver in bstack1l1llll111_opy_:
            if bstack111llll1l_opy_ == driver.session_id:
              driver.execute_script(bstack1llll11l11_opy_)
      except Exception as e:
        logger.debug(bstack1lllll1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ୎").format(str(e)))
  except Exception as e:
    logger.debug(bstack1lllll1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨ୏").format(str(e)))
  bstack1ll111l11_opy_(item, call, rep)
def bstack111ll1111_opy_(driver, bstack11lll11l1_opy_):
  PercySDK.screenshot(driver, bstack11lll11l1_opy_)
def bstack1111l11l_opy_(driver):
  if bstack1111l1ll1_opy_.bstack1ll11lllll_opy_() is True or bstack1111l1ll1_opy_.capturing() is True:
    return
  bstack1111l1ll1_opy_.bstack1llllll11_opy_()
  while not bstack1111l1ll1_opy_.bstack1ll11lllll_opy_():
    bstack111ll111_opy_ = bstack1111l1ll1_opy_.bstack1llll1111_opy_()
    bstack111ll1111_opy_(driver, bstack111ll111_opy_)
  bstack1111l1ll1_opy_.bstack1lllllll1_opy_()
def bstack1l1l11l11_opy_(sequence, driver_command, response = None):
    try:
      if sequence != bstack1lllll1l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬ୐"):
        return
      if not CONFIG.get(bstack1lllll1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ୑"), False):
        return
      bstack111ll111_opy_ = bstack11l1l11l1_opy_(threading.current_thread(), bstack1lllll1l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ୒"), None)
      for command in bstack11ll11l11_opy_:
        if command == driver_command:
          for driver in bstack1l1llll111_opy_:
            bstack1111l11l_opy_(driver)
      bstack1ll1ll11l1_opy_ = CONFIG.get(bstack1lllll1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫ୓"), bstack1lllll1l_opy_ (u"ࠤࡤࡹࡹࡵࠢ୔"))
      if driver_command in bstack1lll1l1l1_opy_[bstack1ll1ll11l1_opy_]:
        bstack1111l1ll1_opy_.bstack1l11l1ll_opy_(bstack111ll111_opy_, driver_command)
    except Exception as e:
      pass
def bstack1llll11ll_opy_(framework_name):
  global bstack1ll1lllll1_opy_
  global bstack11l111ll_opy_
  global bstack1lll1111l1_opy_
  bstack1ll1lllll1_opy_ = framework_name
  logger.info(bstack1ll1lll1l1_opy_.format(bstack1ll1lllll1_opy_.split(bstack1lllll1l_opy_ (u"ࠪ࠱ࠬ୕"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1ll11lll11_opy_:
      Service.start = bstack1l11l11l_opy_
      Service.stop = bstack1l11ll1ll_opy_
      webdriver.Remote.get = bstack1lll1l111l_opy_
      WebDriver.close = bstack1l1l111ll_opy_
      WebDriver.quit = bstack11l11ll11_opy_
      webdriver.Remote.__init__ = bstack11l1ll11_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.bstack11ll1l1l1_opy_ = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.bstack1ll1l11lll_opy_ = getAccessibilityResultsSummary
    if not bstack1ll11lll11_opy_ and bstack1l1ll111ll_opy_.on():
      webdriver.Remote.__init__ = bstack11lll1l1_opy_
    if bstack1lllll1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪୖ") in str(framework_name).lower() and bstack1l1ll111ll_opy_.on():
      WebDriver.execute = bstack111lllll_opy_
    bstack11l111ll_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1ll11lll11_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1ll1111l_opy_
  except Exception as e:
    pass
  bstack1ll11lll1_opy_()
  if not bstack11l111ll_opy_:
    bstack1ll1lll1_opy_(bstack1lllll1l_opy_ (u"ࠧࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠢୗ"), bstack1111l1l1_opy_)
  if bstack1ll11l1l1l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1lll11l1l_opy_
    except Exception as e:
      logger.error(bstack1l11l1lll_opy_.format(str(e)))
  if bstack1l1lll111_opy_():
    bstack1ll1llll_opy_(CONFIG, logger)
  if (bstack1lllll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ୘") in str(framework_name).lower()):
    if not bstack1ll11lll11_opy_:
      return
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if CONFIG.get(bstack1lllll1l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭୙"), False):
          bstack11lllllll_opy_(bstack1l1l11l11_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1ll1llll1_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1lllll1ll_opy_
      except Exception as e:
        logger.warn(bstack11llllll1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1llllllll_opy_
      except Exception as e:
        logger.debug(bstack1lll11ll1l_opy_ + str(e))
    except Exception as e:
      bstack1ll1lll1_opy_(e, bstack11llllll1_opy_)
    Output.start_test = bstack1ll1l111ll_opy_
    Output.end_test = bstack111111lll_opy_
    TestStatus.__init__ = bstack1l1lll1lll_opy_
    QueueItem.__init__ = bstack1lll11l111_opy_
    pabot._create_items = bstack11111l1ll_opy_
    try:
      from pabot import __version__ as bstack11lll1l11_opy_
      if version.parse(bstack11lll1l11_opy_) >= version.parse(bstack1lllll1l_opy_ (u"ࠨ࠴࠱࠵࠺࠴࠰ࠨ୚")):
        pabot._run = bstack11111l111_opy_
      elif version.parse(bstack11lll1l11_opy_) >= version.parse(bstack1lllll1l_opy_ (u"ࠩ࠵࠲࠶࠹࠮࠱ࠩ୛")):
        pabot._run = bstack1ll1l1llll_opy_
      else:
        pabot._run = bstack1lll111l_opy_
    except Exception as e:
      pabot._run = bstack1lll111l_opy_
    pabot._create_command_for_execution = bstack111l111l1_opy_
    pabot._report_results = bstack11l1lll11_opy_
  if bstack1lllll1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪଡ଼") in str(framework_name).lower():
    if not bstack1ll11lll11_opy_:
      return
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1lll1_opy_(e, bstack1lll111111_opy_)
    Runner.run_hook = bstack111ll11l1_opy_
    Step.run = bstack11ll1ll1l_opy_
  if bstack1lllll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫଢ଼") in str(framework_name).lower():
    if not bstack1ll11lll11_opy_:
      return
    try:
      if CONFIG.get(bstack1lllll1l_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ୞"), False):
          bstack11lllllll_opy_(bstack1l1l11l11_opy_)
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack111l11ll1_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l1l1l11l1_opy_
      Config.getoption = bstack1ll1lll11l_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1l1ll1l111_opy_
    except Exception as e:
      pass
def bstack1l1l1l11ll_opy_():
  global CONFIG
  if bstack1lllll1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ୟ") in CONFIG and int(CONFIG[bstack1lllll1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧୠ")]) > 1:
    logger.warn(bstack111l11ll_opy_)
def bstack1llllll11l_opy_(arg, bstack1l1lll1l1_opy_, bstack1l1ll111_opy_=None):
  global CONFIG
  global bstack11l111l1_opy_
  global bstack11ll11ll1_opy_
  global bstack1ll11lll11_opy_
  global bstack1ll1ll1l1_opy_
  bstack1l1ll1lll_opy_ = bstack1lllll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨୡ")
  if bstack1l1lll1l1_opy_ and isinstance(bstack1l1lll1l1_opy_, str):
    bstack1l1lll1l1_opy_ = eval(bstack1l1lll1l1_opy_)
  CONFIG = bstack1l1lll1l1_opy_[bstack1lllll1l_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩୢ")]
  bstack11l111l1_opy_ = bstack1l1lll1l1_opy_[bstack1lllll1l_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫୣ")]
  bstack11ll11ll1_opy_ = bstack1l1lll1l1_opy_[bstack1lllll1l_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭୤")]
  bstack1ll11lll11_opy_ = bstack1l1lll1l1_opy_[bstack1lllll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ୥")]
  bstack1ll1ll1l1_opy_.bstack11111l1l1_opy_(bstack1lllll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ୦"), bstack1ll11lll11_opy_)
  os.environ[bstack1lllll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ୧")] = bstack1l1ll1lll_opy_
  os.environ[bstack1lllll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧ୨")] = json.dumps(CONFIG)
  os.environ[bstack1lllll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩ୩")] = bstack11l111l1_opy_
  os.environ[bstack1lllll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ୪")] = str(bstack11ll11ll1_opy_)
  os.environ[bstack1lllll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪ୫")] = str(True)
  if bstack1l1ll11l1l_opy_(arg, [bstack1lllll1l_opy_ (u"ࠬ࠳࡮ࠨ୬"), bstack1lllll1l_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ୭")]) != -1:
    os.environ[bstack1lllll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨ୮")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1l1ll1l1l_opy_)
    return
  bstack111ll11ll_opy_()
  global bstack1l1lll11l_opy_
  global bstack1llll11l_opy_
  global bstack1l1l1l1lll_opy_
  global bstack1l1llll11l_opy_
  global bstack1l1ll11111_opy_
  global bstack1lll1111l1_opy_
  global bstack1l11l1l1_opy_
  arg.append(bstack1lllll1l_opy_ (u"ࠣ࠯࡚ࠦ୯"))
  arg.append(bstack1lllll1l_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦ࠼ࡐࡳࡩࡻ࡬ࡦࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡭ࡲࡶ࡯ࡳࡶࡨࡨ࠿ࡶࡹࡵࡧࡶࡸ࠳ࡖࡹࡵࡧࡶࡸ࡜ࡧࡲ࡯࡫ࡱ࡫ࠧ୰"))
  arg.append(bstack1lllll1l_opy_ (u"ࠥ࠱࡜ࠨୱ"))
  arg.append(bstack1lllll1l_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾࡙࡮ࡥࠡࡪࡲࡳࡰ࡯࡭ࡱ࡮ࠥ୲"))
  global bstack1lllll111_opy_
  global bstack11111ll11_opy_
  global bstack1l1l1ll1l1_opy_
  global bstack1lllllll1l_opy_
  global bstack1ll1l1111l_opy_
  global bstack1lll11l1l1_opy_
  global bstack111l111ll_opy_
  global bstack1ll1111lll_opy_
  global bstack1111l1111_opy_
  global bstack1ll11l1ll_opy_
  global bstack1l1l1l1ll1_opy_
  global bstack1ll111l11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lllll111_opy_ = webdriver.Remote.__init__
    bstack11111ll11_opy_ = WebDriver.quit
    bstack111l111ll_opy_ = WebDriver.close
    bstack1ll1111lll_opy_ = WebDriver.get
  except Exception as e:
    pass
  if bstack1l11l111l_opy_(CONFIG) and bstack1l1ll1111_opy_():
    if bstack1l11ll1l_opy_() < version.parse(bstack11l11lll1_opy_):
      logger.error(bstack111lllll1_opy_.format(bstack1l11ll1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1111l1111_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1l11l1lll_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1ll11l1ll_opy_ = Config.getoption
    from _pytest import runner
    bstack1l1l1l1ll1_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1l11ll11l_opy_)
  try:
    from pytest_bdd import reporting
    bstack1ll111l11_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1lllll1l_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭୳"))
  bstack1l1l1l1lll_opy_ = CONFIG.get(bstack1lllll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ୴"), {}).get(bstack1lllll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ୵"))
  bstack1l11l1l1_opy_ = True
  bstack1llll11ll_opy_(bstack1l1lllllll_opy_)
  os.environ[bstack1lllll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩ୶")] = CONFIG[bstack1lllll1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ୷")]
  os.environ[bstack1lllll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭୸")] = CONFIG[bstack1lllll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ୹")]
  os.environ[bstack1lllll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ୺")] = bstack1ll11lll11_opy_.__str__()
  from _pytest.config import main as bstack11l111l1l_opy_
  bstack11l111l1l_opy_(arg)
  if bstack1lllll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪ୻") in multiprocessing.current_process().__dict__.keys():
    for bstack1ll1ll1lll_opy_ in multiprocessing.current_process().bstack_error_list:
      bstack1l1ll111_opy_.append(bstack1ll1ll1lll_opy_)
def bstack1l1ll1l1_opy_(arg):
  bstack1llll11ll_opy_(bstack11l111l11_opy_)
  os.environ[bstack1lllll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ୼")] = str(bstack11ll11ll1_opy_)
  from behave.__main__ import main as bstack1ll1l1l1_opy_
  bstack1ll1l1l1_opy_(arg)
def bstack111ll1l1l_opy_():
  logger.info(bstack11ll1l11l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1lllll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ୽"), help=bstack1lllll1l_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࠪ୾"))
  parser.add_argument(bstack1lllll1l_opy_ (u"ࠪ࠱ࡺ࠭୿"), bstack1lllll1l_opy_ (u"ࠫ࠲࠳ࡵࡴࡧࡵࡲࡦࡳࡥࠨ஀"), help=bstack1lllll1l_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ஁"))
  parser.add_argument(bstack1lllll1l_opy_ (u"࠭࠭࡬ࠩஂ"), bstack1lllll1l_opy_ (u"ࠧ࠮࠯࡮ࡩࡾ࠭ஃ"), help=bstack1lllll1l_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡧࡣࡤࡧࡶࡷࠥࡱࡥࡺࠩ஄"))
  parser.add_argument(bstack1lllll1l_opy_ (u"ࠩ࠰ࡪࠬஅ"), bstack1lllll1l_opy_ (u"ࠪ࠱࠲࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨஆ"), help=bstack1lllll1l_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪஇ"))
  bstack111lll11_opy_ = parser.parse_args()
  try:
    bstack1l1llll1l_opy_ = bstack1lllll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡮ࡦࡴ࡬ࡧ࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩஈ")
    if bstack111lll11_opy_.framework and bstack111lll11_opy_.framework not in (bstack1lllll1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭உ"), bstack1lllll1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨஊ")):
      bstack1l1llll1l_opy_ = bstack1lllll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧ஋")
    bstack1l11111l1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1llll1l_opy_)
    bstack1l11lllll_opy_ = open(bstack1l11111l1_opy_, bstack1lllll1l_opy_ (u"ࠩࡵࠫ஌"))
    bstack1ll1ll1ll_opy_ = bstack1l11lllll_opy_.read()
    bstack1l11lllll_opy_.close()
    if bstack111lll11_opy_.username:
      bstack1ll1ll1ll_opy_ = bstack1ll1ll1ll_opy_.replace(bstack1lllll1l_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪ஍"), bstack111lll11_opy_.username)
    if bstack111lll11_opy_.key:
      bstack1ll1ll1ll_opy_ = bstack1ll1ll1ll_opy_.replace(bstack1lllll1l_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭எ"), bstack111lll11_opy_.key)
    if bstack111lll11_opy_.framework:
      bstack1ll1ll1ll_opy_ = bstack1ll1ll1ll_opy_.replace(bstack1lllll1l_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ஏ"), bstack111lll11_opy_.framework)
    file_name = bstack1lllll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩஐ")
    file_path = os.path.abspath(file_name)
    bstack11l1l1111_opy_ = open(file_path, bstack1lllll1l_opy_ (u"ࠧࡸࠩ஑"))
    bstack11l1l1111_opy_.write(bstack1ll1ll1ll_opy_)
    bstack11l1l1111_opy_.close()
    logger.info(bstack1ll1111ll1_opy_)
    try:
      os.environ[bstack1lllll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪஒ")] = bstack111lll11_opy_.framework if bstack111lll11_opy_.framework != None else bstack1lllll1l_opy_ (u"ࠤࠥஓ")
      config = yaml.safe_load(bstack1ll1ll1ll_opy_)
      config[bstack1lllll1l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪஔ")] = bstack1lllll1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱ࡸ࡫ࡴࡶࡲࠪக")
      bstack1llll11l1_opy_(bstack1llll111l1_opy_, config)
    except Exception as e:
      logger.debug(bstack11l1111ll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1llll1llll_opy_.format(str(e)))
def bstack1llll11l1_opy_(bstack1lll11ll_opy_, config, bstack1ll11lll1l_opy_={}):
  global bstack1ll11lll11_opy_
  global bstack1l1l11l1_opy_
  if not config:
    return
  bstack1ll11111ll_opy_ = bstack11l11ll1l_opy_ if not bstack1ll11lll11_opy_ else (
    bstack1l1l1l111_opy_ if bstack1lllll1l_opy_ (u"ࠬࡧࡰࡱࠩ஖") in config else bstack11llll1l_opy_)
  data = {
    bstack1lllll1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ஗"): config[bstack1lllll1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ஘")],
    bstack1lllll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫங"): config[bstack1lllll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬச")],
    bstack1lllll1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ஛"): bstack1lll11ll_opy_,
    bstack1lllll1l_opy_ (u"ࠫࡩ࡫ࡴࡦࡥࡷࡩࡩࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨஜ"): os.environ.get(bstack1lllll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ஝"), bstack1l1l11l1_opy_),
    bstack1lllll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨஞ"): bstack11111l1l_opy_,
    bstack1lllll1l_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭ࠩட"): bstack1l111lll_opy_(),
    bstack1lllll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫ஠"): {
      bstack1lllll1l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ஡"): str(config[bstack1lllll1l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ஢")]) if bstack1lllll1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫண") in config else bstack1lllll1l_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨத"),
      bstack1lllll1l_opy_ (u"࠭ࡲࡦࡨࡨࡶࡷ࡫ࡲࠨ஥"): bstack1l1ll11ll_opy_(os.getenv(bstack1lllll1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠤ஦"), bstack1lllll1l_opy_ (u"ࠣࠤ஧"))),
      bstack1lllll1l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫந"): bstack1lllll1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪன"),
      bstack1lllll1l_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬப"): bstack1ll11111ll_opy_,
      bstack1lllll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ஫"): config[bstack1lllll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ஬")] if config[bstack1lllll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ஭")] else bstack1lllll1l_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤம"),
      bstack1lllll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫய"): str(config[bstack1lllll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬர")]) if bstack1lllll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ற") in config else bstack1lllll1l_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨல"),
      bstack1lllll1l_opy_ (u"࠭࡯ࡴࠩள"): sys.platform,
      bstack1lllll1l_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩழ"): socket.gethostname()
    }
  }
  update(data[bstack1lllll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫவ")], bstack1ll11lll1l_opy_)
  try:
    response = bstack1lll1ll1_opy_(bstack1lllll1l_opy_ (u"ࠩࡓࡓࡘ࡚ࠧஶ"), bstack11lll1lll_opy_(bstack11l11ll1_opy_), data, {
      bstack1lllll1l_opy_ (u"ࠪࡥࡺࡺࡨࠨஷ"): (config[bstack1lllll1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ஸ")], config[bstack1lllll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨஹ")])
    })
    if response:
      logger.debug(bstack1llll1l111_opy_.format(bstack1lll11ll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1lll1l11l_opy_.format(str(e)))
def bstack1l1ll11ll_opy_(framework):
  return bstack1lllll1l_opy_ (u"ࠨࡻࡾ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥ஺").format(str(framework), __version__) if framework else bstack1lllll1l_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣ஻").format(
    __version__)
def bstack111ll11ll_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack11l1ll111_opy_()
    logger.debug(bstack1ll11l1lll_opy_.format(str(CONFIG)))
    bstack1ll111111_opy_()
    bstack11ll1lll_opy_()
  except Exception as e:
    logger.error(bstack1lllll1l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࠧ஼") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l1llll1_opy_
  atexit.register(bstack1llllll1ll_opy_)
  signal.signal(signal.SIGINT, bstack11l11lll_opy_)
  signal.signal(signal.SIGTERM, bstack11l11lll_opy_)
def bstack1l1llll1_opy_(exctype, value, traceback):
  global bstack1l1llll111_opy_
  try:
    for driver in bstack1l1llll111_opy_:
      bstack11lll1ll1_opy_(driver, bstack1lllll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ஽"), bstack1lllll1l_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨா") + str(value))
  except Exception:
    pass
  bstack1ll11ll11_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1ll11ll11_opy_(message=bstack1lllll1l_opy_ (u"ࠫࠬி"), bstack111ll1lll_opy_ = False):
  global CONFIG
  bstack1l1ll1l11_opy_ = bstack1lllll1l_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠧீ") if bstack111ll1lll_opy_ else bstack1lllll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬு")
  try:
    if message:
      bstack1ll11lll1l_opy_ = {
        bstack1l1ll1l11_opy_ : str(message)
      }
      bstack1llll11l1_opy_(bstack111l1llll_opy_, CONFIG, bstack1ll11lll1l_opy_)
    else:
      bstack1llll11l1_opy_(bstack111l1llll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11lll11ll_opy_.format(str(e)))
def bstack1l111lll1_opy_(bstack111l1lll_opy_, size):
  bstack11l1111l1_opy_ = []
  while len(bstack111l1lll_opy_) > size:
    bstack1111lll1_opy_ = bstack111l1lll_opy_[:size]
    bstack11l1111l1_opy_.append(bstack1111lll1_opy_)
    bstack111l1lll_opy_ = bstack111l1lll_opy_[size:]
  bstack11l1111l1_opy_.append(bstack111l1lll_opy_)
  return bstack11l1111l1_opy_
def bstack1ll1ll111_opy_(args):
  if bstack1lllll1l_opy_ (u"ࠧ࠮࡯ࠪூ") in args and bstack1lllll1l_opy_ (u"ࠨࡲࡧࡦࠬ௃") in args:
    return True
  return False
def run_on_browserstack(bstack1l1111l1_opy_=None, bstack1l1ll111_opy_=None, bstack111l11l1_opy_=False):
  global CONFIG
  global bstack11l111l1_opy_
  global bstack11ll11ll1_opy_
  global bstack1l1l11l1_opy_
  bstack1l1ll1lll_opy_ = bstack1lllll1l_opy_ (u"ࠩࠪ௄")
  bstack11lll111l_opy_(bstack1l11ll11_opy_, logger)
  if bstack1l1111l1_opy_ and isinstance(bstack1l1111l1_opy_, str):
    bstack1l1111l1_opy_ = eval(bstack1l1111l1_opy_)
  if bstack1l1111l1_opy_:
    CONFIG = bstack1l1111l1_opy_[bstack1lllll1l_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪ௅")]
    bstack11l111l1_opy_ = bstack1l1111l1_opy_[bstack1lllll1l_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬெ")]
    bstack11ll11ll1_opy_ = bstack1l1111l1_opy_[bstack1lllll1l_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧே")]
    bstack1ll1ll1l1_opy_.bstack11111l1l1_opy_(bstack1lllll1l_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨை"), bstack11ll11ll1_opy_)
    bstack1l1ll1lll_opy_ = bstack1lllll1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ௉")
  if not bstack111l11l1_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1l1ll1l1l_opy_)
      return
    if sys.argv[1] == bstack1lllll1l_opy_ (u"ࠨ࠯࠰ࡺࡪࡸࡳࡪࡱࡱࠫொ") or sys.argv[1] == bstack1lllll1l_opy_ (u"ࠩ࠰ࡺࠬோ"):
      logger.info(bstack1lllll1l_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡓࡽࡹ࡮࡯࡯ࠢࡖࡈࡐࠦࡶࡼࡿࠪௌ").format(__version__))
      return
    if sys.argv[1] == bstack1lllll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ்ࠪ"):
      bstack111ll1l1l_opy_()
      return
  args = sys.argv
  bstack111ll11ll_opy_()
  global bstack1l1lll11l_opy_
  global bstack1llll11111_opy_
  global bstack1l11l1l1_opy_
  global bstack1llll1l1_opy_
  global bstack1llll11l_opy_
  global bstack1l1l1l1lll_opy_
  global bstack1l1llll11l_opy_
  global bstack1ll111l11l_opy_
  global bstack1l1ll11111_opy_
  global bstack1lll1111l1_opy_
  global bstack1ll1l1l1l1_opy_
  bstack1llll11111_opy_ = len(CONFIG[bstack1lllll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ௎")])
  if not bstack1l1ll1lll_opy_:
    if args[1] == bstack1lllll1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭௏") or args[1] == bstack1lllll1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨௐ"):
      bstack1l1ll1lll_opy_ = bstack1lllll1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ௑")
      args = args[2:]
    elif args[1] == bstack1lllll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ௒"):
      bstack1l1ll1lll_opy_ = bstack1lllll1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ௓")
      args = args[2:]
    elif args[1] == bstack1lllll1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ௔"):
      bstack1l1ll1lll_opy_ = bstack1lllll1l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ௕")
      args = args[2:]
    elif args[1] == bstack1lllll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ௖"):
      bstack1l1ll1lll_opy_ = bstack1lllll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨௗ")
      args = args[2:]
    elif args[1] == bstack1lllll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ௘"):
      bstack1l1ll1lll_opy_ = bstack1lllll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ௙")
      args = args[2:]
    elif args[1] == bstack1lllll1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ௚"):
      bstack1l1ll1lll_opy_ = bstack1lllll1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ௛")
      args = args[2:]
    else:
      if not bstack1lllll1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ௜") in CONFIG or str(CONFIG[bstack1lllll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ௝")]).lower() in [bstack1lllll1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ௞"), bstack1lllll1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩ௟")]:
        bstack1l1ll1lll_opy_ = bstack1lllll1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ௠")
        args = args[1:]
      elif str(CONFIG[bstack1lllll1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭௡")]).lower() == bstack1lllll1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ௢"):
        bstack1l1ll1lll_opy_ = bstack1lllll1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ௣")
        args = args[1:]
      elif str(CONFIG[bstack1lllll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ௤")]).lower() == bstack1lllll1l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭௥"):
        bstack1l1ll1lll_opy_ = bstack1lllll1l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ௦")
        args = args[1:]
      elif str(CONFIG[bstack1lllll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ௧")]).lower() == bstack1lllll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ௨"):
        bstack1l1ll1lll_opy_ = bstack1lllll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ௩")
        args = args[1:]
      elif str(CONFIG[bstack1lllll1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ௪")]).lower() == bstack1lllll1l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭௫"):
        bstack1l1ll1lll_opy_ = bstack1lllll1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ௬")
        args = args[1:]
      else:
        os.environ[bstack1lllll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ௭")] = bstack1l1ll1lll_opy_
        bstack1ll1l11l11_opy_(bstack1l11llll1_opy_)
  os.environ[bstack1lllll1l_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪ௮")] = bstack1l1ll1lll_opy_
  bstack1l1l11l1_opy_ = bstack1l1ll1lll_opy_
  global bstack1l1lll11ll_opy_
  if bstack1l1111l1_opy_:
    try:
      os.environ[bstack1lllll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ௯")] = bstack1l1ll1lll_opy_
      bstack1llll11l1_opy_(bstack1lll11l1ll_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack11lll11ll_opy_.format(str(e)))
  global bstack1lllll111_opy_
  global bstack11111ll11_opy_
  global bstack1lll1l11l1_opy_
  global bstack1l1l1111_opy_
  global bstack1lllll11l1_opy_
  global bstack1lll1l111_opy_
  global bstack1l1l1ll1l1_opy_
  global bstack1lllllll1l_opy_
  global bstack1ll11l11ll_opy_
  global bstack1ll1l1111l_opy_
  global bstack1lll11l1l1_opy_
  global bstack111l111ll_opy_
  global bstack1l1l1llll1_opy_
  global bstack1ll1l1lll_opy_
  global bstack1ll1111lll_opy_
  global bstack1111l1111_opy_
  global bstack1ll11l1ll_opy_
  global bstack1l1l1l1ll1_opy_
  global bstack1111111l_opy_
  global bstack1ll111l11_opy_
  global bstack1l1l11111_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lllll111_opy_ = webdriver.Remote.__init__
    bstack11111ll11_opy_ = WebDriver.quit
    bstack111l111ll_opy_ = WebDriver.close
    bstack1ll1111lll_opy_ = WebDriver.get
    bstack1l1l11111_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1lll11ll_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    global bstack1ll1l1l1l_opy_
    from QWeb.keywords import browser
    bstack1ll1l1l1l_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l11l111l_opy_(CONFIG) and bstack1l1ll1111_opy_():
    if bstack1l11ll1l_opy_() < version.parse(bstack11l11lll1_opy_):
      logger.error(bstack111lllll1_opy_.format(bstack1l11ll1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1111l1111_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1l11l1lll_opy_.format(str(e)))
  if bstack1l1ll1lll_opy_ != bstack1lllll1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ௰") or (bstack1l1ll1lll_opy_ == bstack1lllll1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ௱") and not bstack1l1111l1_opy_):
    bstack1llll1111l_opy_()
  if (bstack1l1ll1lll_opy_ in [bstack1lllll1l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ௲"), bstack1lllll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭௳"), bstack1lllll1l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ௴")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1ll1llll1_opy_
        bstack1lll1l111_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack11llllll1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1lllll11l1_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1lll11ll1l_opy_ + str(e))
    except Exception as e:
      bstack1ll1lll1_opy_(e, bstack11llllll1_opy_)
    if bstack1l1ll1lll_opy_ != bstack1lllll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ௵"):
      bstack1l11111l_opy_()
    bstack1lll1l11l1_opy_ = Output.start_test
    bstack1l1l1111_opy_ = Output.end_test
    bstack1l1l1ll1l1_opy_ = TestStatus.__init__
    bstack1ll11l11ll_opy_ = pabot._run
    bstack1ll1l1111l_opy_ = QueueItem.__init__
    bstack1lll11l1l1_opy_ = pabot._create_command_for_execution
    bstack1111111l_opy_ = pabot._report_results
  if bstack1l1ll1lll_opy_ == bstack1lllll1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ௶"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1lll1_opy_(e, bstack1lll111111_opy_)
    bstack1l1l1llll1_opy_ = Runner.run_hook
    bstack1ll1l1lll_opy_ = Step.run
  if bstack1l1ll1lll_opy_ == bstack1lllll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ௷"):
    try:
      from _pytest.config import Config
      bstack1ll11l1ll_opy_ = Config.getoption
      from _pytest import runner
      bstack1l1l1l1ll1_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1l11ll11l_opy_)
    try:
      from pytest_bdd import reporting
      bstack1ll111l11_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1lllll1l_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭௸"))
  if bstack1l1ll1lll_opy_ in bstack111ll11l_opy_:
    try:
      framework_name = bstack1lllll1l_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬ௹") if bstack1l1ll1lll_opy_ in [bstack1lllll1l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭௺"), bstack1lllll1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ௻"), bstack1lllll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ௼")] else bstack1l1ll11l_opy_(bstack1l1ll1lll_opy_)
      bstack1l1ll111ll_opy_.launch(CONFIG, {
        bstack1lllll1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠫ௽"): bstack1lllll1l_opy_ (u"ࠫࢀ࠶ࡽ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪ௾").format(framework_name) if bstack1l1ll1lll_opy_ == bstack1lllll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ௿") and bstack1llll1l11l_opy_() else framework_name,
        bstack1lllll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪఀ"): bstack1lll1lll11_opy_(framework_name),
        bstack1lllll1l_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬఁ"): __version__
      })
    except Exception as e:
      logger.debug(bstack1ll1l1lll1_opy_.format(bstack1lllll1l_opy_ (u"ࠨࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨం"), str(e)))
  if bstack1l1ll1lll_opy_ in bstack111ll1l11_opy_:
    try:
      framework_name = bstack1lllll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨః") if bstack1l1ll1lll_opy_ in [bstack1lllll1l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩఄ"), bstack1lllll1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪఅ")] else bstack1l1ll1lll_opy_
      if bstack1ll11lll11_opy_ and bstack1lllll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬఆ") in CONFIG and CONFIG[bstack1lllll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ఇ")] == True:
        if bstack1lllll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧఈ") in CONFIG:
          os.environ[bstack1lllll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩఉ")] = os.getenv(bstack1lllll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪఊ"), json.dumps(CONFIG[bstack1lllll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪఋ")]))
          CONFIG[bstack1lllll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫఌ")].pop(bstack1lllll1l_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ఍"), None)
          CONFIG[bstack1lllll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ఎ")].pop(bstack1lllll1l_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬఏ"), None)
        bstack111llllll_opy_, bstack11l11l11_opy_ = bstack1l1ll11l1_opy_.bstack1l1111111_opy_(CONFIG, bstack1l1ll1lll_opy_, bstack1lll1lll11_opy_(framework_name))
        if not bstack111llllll_opy_ is None:
          os.environ[bstack1lllll1l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ఐ")] = bstack111llllll_opy_
          os.environ[bstack1lllll1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡘࡊ࡙ࡔࡠࡔࡘࡒࡤࡏࡄࠨ఑")] = str(bstack11l11l11_opy_)
    except Exception as e:
      logger.debug(bstack1ll1l1lll1_opy_.format(bstack1lllll1l_opy_ (u"ࠪࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪఒ"), str(e)))
  if bstack1l1ll1lll_opy_ == bstack1lllll1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫఓ"):
    bstack1l11l1l1_opy_ = True
    if bstack1l1111l1_opy_ and bstack111l11l1_opy_:
      bstack1l1l1l1lll_opy_ = CONFIG.get(bstack1lllll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩఔ"), {}).get(bstack1lllll1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨక"))
      bstack1llll11ll_opy_(bstack1ll111ll1l_opy_)
    elif bstack1l1111l1_opy_:
      bstack1l1l1l1lll_opy_ = CONFIG.get(bstack1lllll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫఖ"), {}).get(bstack1lllll1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪగ"))
      global bstack1l1llll111_opy_
      try:
        if bstack1ll1ll111_opy_(bstack1l1111l1_opy_[bstack1lllll1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬఘ")]) and multiprocessing.current_process().name == bstack1lllll1l_opy_ (u"ࠪ࠴ࠬఙ"):
          bstack1l1111l1_opy_[bstack1lllll1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧచ")].remove(bstack1lllll1l_opy_ (u"ࠬ࠳࡭ࠨఛ"))
          bstack1l1111l1_opy_[bstack1lllll1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩజ")].remove(bstack1lllll1l_opy_ (u"ࠧࡱࡦࡥࠫఝ"))
          bstack1l1111l1_opy_[bstack1lllll1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫఞ")] = bstack1l1111l1_opy_[bstack1lllll1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬట")][0]
          with open(bstack1l1111l1_opy_[bstack1lllll1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఠ")], bstack1lllll1l_opy_ (u"ࠫࡷ࠭డ")) as f:
            bstack1l111111_opy_ = f.read()
          bstack1ll111lll_opy_ = bstack1lllll1l_opy_ (u"ࠧࠨࠢࡧࡴࡲࡱࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡪ࡫ࠡ࡫ࡰࡴࡴࡸࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨ࠿ࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࠩࡽࢀ࠭ࡀࠦࡦࡳࡱࡰࠤࡵࡪࡢࠡ࡫ࡰࡴࡴࡸࡴࠡࡒࡧࡦࡀࠦ࡯ࡨࡡࡧࡦࠥࡃࠠࡑࡦࡥ࠲ࡩࡵ࡟ࡣࡴࡨࡥࡰࡁࠊࡥࡧࡩࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠨࡴࡧ࡯ࡪ࠱ࠦࡡࡳࡩ࠯ࠤࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠠ࠾ࠢ࠳࠭࠿ࠐࠠࠡࡶࡵࡽ࠿ࠐࠠࠡࠢࠣࡥࡷ࡭ࠠ࠾ࠢࡶࡸࡷ࠮ࡩ࡯ࡶࠫࡥࡷ࡭ࠩࠬ࠳࠳࠭ࠏࠦࠠࡦࡺࡦࡩࡵࡺࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡥࡸࠦࡥ࠻ࠌࠣࠤࠥࠦࡰࡢࡵࡶࠎࠥࠦ࡯ࡨࡡࡧࡦ࠭ࡹࡥ࡭ࡨ࠯ࡥࡷ࡭ࠬࡵࡧࡰࡴࡴࡸࡡࡳࡻࠬࠎࡕࡪࡢ࠯ࡦࡲࡣࡧࠦ࠽ࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠎࡕࡪࡢ࠯ࡦࡲࡣࡧࡸࡥࡢ࡭ࠣࡁࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠋࡒࡧࡦ࠭࠯࠮ࡴࡧࡷࡣࡹࡸࡡࡤࡧࠫ࠭ࡡࡴࠢࠣࠤఢ").format(str(bstack1l1111l1_opy_))
          bstack1l111l1l1_opy_ = bstack1ll111lll_opy_ + bstack1l111111_opy_
          bstack111111l1_opy_ = bstack1l1111l1_opy_[bstack1lllll1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩణ")] + bstack1lllll1l_opy_ (u"ࠧࡠࡤࡶࡸࡦࡩ࡫ࡠࡶࡨࡱࡵ࠴ࡰࡺࠩత")
          with open(bstack111111l1_opy_, bstack1lllll1l_opy_ (u"ࠨࡹࠪథ")):
            pass
          with open(bstack111111l1_opy_, bstack1lllll1l_opy_ (u"ࠤࡺ࠯ࠧద")) as f:
            f.write(bstack1l111l1l1_opy_)
          import subprocess
          bstack11ll1l1l_opy_ = subprocess.run([bstack1lllll1l_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࠥధ"), bstack111111l1_opy_])
          if os.path.exists(bstack111111l1_opy_):
            os.unlink(bstack111111l1_opy_)
          os._exit(bstack11ll1l1l_opy_.returncode)
        else:
          if bstack1ll1ll111_opy_(bstack1l1111l1_opy_[bstack1lllll1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧన")]):
            bstack1l1111l1_opy_[bstack1lllll1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ఩")].remove(bstack1lllll1l_opy_ (u"࠭࠭࡮ࠩప"))
            bstack1l1111l1_opy_[bstack1lllll1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪఫ")].remove(bstack1lllll1l_opy_ (u"ࠨࡲࡧࡦࠬబ"))
            bstack1l1111l1_opy_[bstack1lllll1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬభ")] = bstack1l1111l1_opy_[bstack1lllll1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭మ")][0]
          bstack1llll11ll_opy_(bstack1ll111ll1l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1l1111l1_opy_[bstack1lllll1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧయ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1lllll1l_opy_ (u"ࠬࡥ࡟࡯ࡣࡰࡩࡤࡥࠧర")] = bstack1lllll1l_opy_ (u"࠭࡟ࡠ࡯ࡤ࡭ࡳࡥ࡟ࠨఱ")
          mod_globals[bstack1lllll1l_opy_ (u"ࠧࡠࡡࡩ࡭ࡱ࡫࡟ࡠࠩల")] = os.path.abspath(bstack1l1111l1_opy_[bstack1lllll1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫళ")])
          exec(open(bstack1l1111l1_opy_[bstack1lllll1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬఴ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1lllll1l_opy_ (u"ࠪࡇࡦࡻࡧࡩࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠪవ").format(str(e)))
          for driver in bstack1l1llll111_opy_:
            bstack1l1ll111_opy_.append({
              bstack1lllll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩశ"): bstack1l1111l1_opy_[bstack1lllll1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨష")],
              bstack1lllll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬస"): str(e),
              bstack1lllll1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭హ"): multiprocessing.current_process().name
            })
            bstack11lll1ll1_opy_(driver, bstack1lllll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ఺"), bstack1lllll1l_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ఻") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1l1llll111_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack11ll11ll1_opy_, CONFIG, logger)
      bstack1ll11ll1_opy_()
      bstack1l1l1l11ll_opy_()
      bstack1l1lll1l1_opy_ = {
        bstack1lllll1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ఼࠭"): args[0],
        bstack1lllll1l_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫఽ"): CONFIG,
        bstack1lllll1l_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ా"): bstack11l111l1_opy_,
        bstack1lllll1l_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨి"): bstack11ll11ll1_opy_
      }
      percy.bstack11lll1ll_opy_()
      if bstack1lllll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪీ") in CONFIG:
        bstack1ll1l1111_opy_ = []
        manager = multiprocessing.Manager()
        bstack111111l1l_opy_ = manager.list()
        if bstack1ll1ll111_opy_(args):
          for index, platform in enumerate(CONFIG[bstack1lllll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫు")]):
            if index == 0:
              bstack1l1lll1l1_opy_[bstack1lllll1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬూ")] = args
            bstack1ll1l1111_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l1lll1l1_opy_, bstack111111l1l_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack1lllll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ృ")]):
            bstack1ll1l1111_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l1lll1l1_opy_, bstack111111l1l_opy_)))
        for t in bstack1ll1l1111_opy_:
          t.start()
        for t in bstack1ll1l1111_opy_:
          t.join()
        bstack1ll111l11l_opy_ = list(bstack111111l1l_opy_)
      else:
        if bstack1ll1ll111_opy_(args):
          bstack1l1lll1l1_opy_[bstack1lllll1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧౄ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l1lll1l1_opy_,))
          test.start()
          test.join()
        else:
          bstack1llll11ll_opy_(bstack1ll111ll1l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1lllll1l_opy_ (u"ࠬࡥ࡟࡯ࡣࡰࡩࡤࡥࠧ౅")] = bstack1lllll1l_opy_ (u"࠭࡟ࡠ࡯ࡤ࡭ࡳࡥ࡟ࠨె")
          mod_globals[bstack1lllll1l_opy_ (u"ࠧࡠࡡࡩ࡭ࡱ࡫࡟ࡠࠩే")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l1ll1lll_opy_ == bstack1lllll1l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧై") or bstack1l1ll1lll_opy_ == bstack1lllll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ౉"):
    percy.init(bstack11ll11ll1_opy_, CONFIG, logger)
    percy.bstack11lll1ll_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1ll1lll1_opy_(e, bstack11llllll1_opy_)
    bstack1ll11ll1_opy_()
    bstack1llll11ll_opy_(bstack1lllllll11_opy_)
    if bstack1lllll1l_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨొ") in args:
      i = args.index(bstack1lllll1l_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩో"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1l1lll11l_opy_))
    args.insert(0, str(bstack1lllll1l_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪౌ")))
    if bstack1l1ll111ll_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1ll1ll11_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1lll1ll11l_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1lllll1l_opy_ (u"ࠨࡒࡐࡄࡒࡘࡤࡕࡐࡕࡋࡒࡒࡘࠨ్"),
        ).parse_args(bstack1ll1ll11_opy_)
        args.insert(args.index(bstack1lll1ll11l_opy_[0]), str(bstack1lllll1l_opy_ (u"ࠧ࠮࠯࡯࡭ࡸࡺࡥ࡯ࡧࡵࠫ౎")))
        args.insert(args.index(bstack1lll1ll11l_opy_[0]), str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lllll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡴࡲࡦࡴࡺ࡟࡭࡫ࡶࡸࡪࡴࡥࡳ࠰ࡳࡽࠬ౏"))))
        if bstack11l1l1ll_opy_(os.environ.get(bstack1lllll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧ౐"))) and str(os.environ.get(bstack1lllll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧ౑"), bstack1lllll1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ౒"))) != bstack1lllll1l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ౓"):
          for bstack1llll1lll_opy_ in bstack1lll1ll11l_opy_:
            args.remove(bstack1llll1lll_opy_)
          bstack1lll1l1l_opy_ = os.environ.get(bstack1lllll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠪ౔")).split(bstack1lllll1l_opy_ (u"ౕࠧ࠭ࠩ"))
          for bstack11llll1l1_opy_ in bstack1lll1l1l_opy_:
            args.append(bstack11llll1l1_opy_)
      except Exception as e:
        logger.error(bstack1lllll1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡡࡵࡶࡤࡧ࡭࡯࡮ࡨࠢ࡯࡭ࡸࡺࡥ࡯ࡧࡵࠤ࡫ࡵࡲࠡࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࠢࡈࡶࡷࡵࡲࠡ࠯ౖࠣࠦ").format(e))
    pabot.main(args)
  elif bstack1l1ll1lll_opy_ == bstack1lllll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ౗"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1ll1lll1_opy_(e, bstack11llllll1_opy_)
    for a in args:
      if bstack1lllll1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙ࠩౘ") in a:
        bstack1llll11l_opy_ = int(a.split(bstack1lllll1l_opy_ (u"ࠫ࠿࠭ౙ"))[1])
      if bstack1lllll1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩౚ") in a:
        bstack1l1l1l1lll_opy_ = str(a.split(bstack1lllll1l_opy_ (u"࠭࠺ࠨ౛"))[1])
      if bstack1lllll1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧ౜") in a:
        bstack1l1llll11l_opy_ = str(a.split(bstack1lllll1l_opy_ (u"ࠨ࠼ࠪౝ"))[1])
    bstack1ll1ll1ll1_opy_ = None
    if bstack1lllll1l_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨ౞") in args:
      i = args.index(bstack1lllll1l_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩ౟"))
      args.pop(i)
      bstack1ll1ll1ll1_opy_ = args.pop(i)
    if bstack1ll1ll1ll1_opy_ is not None:
      global bstack1l1lll1ll_opy_
      bstack1l1lll1ll_opy_ = bstack1ll1ll1ll1_opy_
    bstack1llll11ll_opy_(bstack1lllllll11_opy_)
    run_cli(args)
    if bstack1lllll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨౠ") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll1ll1lll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l1ll111_opy_.append(bstack1ll1ll1lll_opy_)
  elif bstack1l1ll1lll_opy_ == bstack1lllll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬౡ"):
    percy.init(bstack11ll11ll1_opy_, CONFIG, logger)
    percy.bstack11lll1ll_opy_()
    bstack1l1lll11_opy_ = bstack1l1111l1l_opy_(args, logger, CONFIG, bstack1ll11lll11_opy_)
    bstack1l1lll11_opy_.bstack1l11llll_opy_()
    bstack1ll11ll1_opy_()
    bstack1llll1l1_opy_ = True
    bstack1lll1111l1_opy_ = bstack1l1lll11_opy_.bstack1lllll11_opy_()
    bstack1l1lll11_opy_.bstack1l1lll1l1_opy_(bstack1l1l1ll1ll_opy_)
    bstack1l1ll11111_opy_ = bstack1l1lll11_opy_.bstack1l1l1lll1_opy_(bstack1llllll11l_opy_, {
      bstack1lllll1l_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧౢ"): bstack11l111l1_opy_,
      bstack1lllll1l_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩౣ"): bstack11ll11ll1_opy_,
      bstack1lllll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ౤"): bstack1ll11lll11_opy_
    })
    bstack1ll1l1l1l1_opy_ = 1 if len(bstack1l1ll11111_opy_) > 0 else 0
  elif bstack1l1ll1lll_opy_ == bstack1lllll1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ౥"):
    try:
      from behave.__main__ import main as bstack1ll1l1l1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1ll1lll1_opy_(e, bstack1lll111111_opy_)
    bstack1ll11ll1_opy_()
    bstack1llll1l1_opy_ = True
    bstack1ll1l111l_opy_ = 1
    if bstack1lllll1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ౦") in CONFIG:
      bstack1ll1l111l_opy_ = CONFIG[bstack1lllll1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ౧")]
    bstack1lll1l1l1l_opy_ = int(bstack1ll1l111l_opy_) * int(len(CONFIG[bstack1lllll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ౨")]))
    config = Configuration(args)
    bstack1lllllllll_opy_ = config.paths
    if len(bstack1lllllllll_opy_) == 0:
      import glob
      pattern = bstack1lllll1l_opy_ (u"࠭ࠪࠫ࠱࠭࠲࡫࡫ࡡࡵࡷࡵࡩࠬ౩")
      bstack1llll1ll11_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1llll1ll11_opy_)
      config = Configuration(args)
      bstack1lllllllll_opy_ = config.paths
    bstack1ll1lll11_opy_ = [os.path.normpath(item) for item in bstack1lllllllll_opy_]
    bstack1ll111ll1_opy_ = [os.path.normpath(item) for item in args]
    bstack1ll1l1ll1_opy_ = [item for item in bstack1ll111ll1_opy_ if item not in bstack1ll1lll11_opy_]
    import platform as pf
    if pf.system().lower() == bstack1lllll1l_opy_ (u"ࠧࡸ࡫ࡱࡨࡴࡽࡳࠨ౪"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1ll1lll11_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1111ll11l_opy_)))
                    for bstack1111ll11l_opy_ in bstack1ll1lll11_opy_]
    bstack1ll1lll1ll_opy_ = []
    for spec in bstack1ll1lll11_opy_:
      bstack1llll111l_opy_ = []
      bstack1llll111l_opy_ += bstack1ll1l1ll1_opy_
      bstack1llll111l_opy_.append(spec)
      bstack1ll1lll1ll_opy_.append(bstack1llll111l_opy_)
    execution_items = []
    for bstack1llll111l_opy_ in bstack1ll1lll1ll_opy_:
      for index, _ in enumerate(CONFIG[bstack1lllll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ౫")]):
        item = {}
        item[bstack1lllll1l_opy_ (u"ࠩࡤࡶ࡬࠭౬")] = bstack1lllll1l_opy_ (u"ࠪࠤࠬ౭").join(bstack1llll111l_opy_)
        item[bstack1lllll1l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ౮")] = index
        execution_items.append(item)
    bstack111llll1_opy_ = bstack1l111lll1_opy_(execution_items, bstack1lll1l1l1l_opy_)
    for execution_item in bstack111llll1_opy_:
      bstack1ll1l1111_opy_ = []
      for item in execution_item:
        bstack1ll1l1111_opy_.append(bstack1ll11ll11l_opy_(name=str(item[bstack1lllll1l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ౯")]),
                                             target=bstack1l1ll1l1_opy_,
                                             args=(item[bstack1lllll1l_opy_ (u"࠭ࡡࡳࡩࠪ౰")],)))
      for t in bstack1ll1l1111_opy_:
        t.start()
      for t in bstack1ll1l1111_opy_:
        t.join()
  else:
    bstack1ll1l11l11_opy_(bstack1l11llll1_opy_)
  if not bstack1l1111l1_opy_:
    bstack11111lll1_opy_()
def browserstack_initialize(bstack1llll1ll1l_opy_=None):
  run_on_browserstack(bstack1llll1ll1l_opy_, None, True)
def bstack11111lll1_opy_():
  global CONFIG
  global bstack1l1l11l1_opy_
  global bstack1ll1l1l1l1_opy_
  bstack1l1ll111ll_opy_.stop()
  bstack1l1ll111ll_opy_.bstack1lll1111_opy_()
  if bstack1l1ll11l1_opy_.bstack1l1l1llll_opy_(CONFIG):
    bstack1l1ll11l1_opy_.bstack11lll1111_opy_()
  [bstack1111l1l1l_opy_, bstack1ll1ll1l11_opy_] = bstack1ll11111l_opy_()
  if bstack1111l1l1l_opy_ is not None and bstack11ll1l1ll_opy_() != -1:
    sessions = bstack1l1l1ll11_opy_(bstack1111l1l1l_opy_)
    bstack1llll111ll_opy_(sessions, bstack1ll1ll1l11_opy_)
  if bstack1l1l11l1_opy_ == bstack1lllll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ౱") and bstack1ll1l1l1l1_opy_ != 0:
    sys.exit(bstack1ll1l1l1l1_opy_)
def bstack1l1ll11l_opy_(bstack1l11ll111_opy_):
  if bstack1l11ll111_opy_:
    return bstack1l11ll111_opy_.capitalize()
  else:
    return bstack1lllll1l_opy_ (u"ࠨࠩ౲")
def bstack1l1111l11_opy_(bstack1ll111lll1_opy_):
  if bstack1lllll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ౳") in bstack1ll111lll1_opy_ and bstack1ll111lll1_opy_[bstack1lllll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨ౴")] != bstack1lllll1l_opy_ (u"ࠫࠬ౵"):
    return bstack1ll111lll1_opy_[bstack1lllll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ౶")]
  else:
    bstack1llll1lll1_opy_ = bstack1lllll1l_opy_ (u"ࠨࠢ౷")
    if bstack1lllll1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ౸") in bstack1ll111lll1_opy_ and bstack1ll111lll1_opy_[bstack1lllll1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ౹")] != None:
      bstack1llll1lll1_opy_ += bstack1ll111lll1_opy_[bstack1lllll1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ౺")] + bstack1lllll1l_opy_ (u"ࠥ࠰ࠥࠨ౻")
      if bstack1ll111lll1_opy_[bstack1lllll1l_opy_ (u"ࠫࡴࡹࠧ౼")] == bstack1lllll1l_opy_ (u"ࠧ࡯࡯ࡴࠤ౽"):
        bstack1llll1lll1_opy_ += bstack1lllll1l_opy_ (u"ࠨࡩࡐࡕࠣࠦ౾")
      bstack1llll1lll1_opy_ += (bstack1ll111lll1_opy_[bstack1lllll1l_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫ౿")] or bstack1lllll1l_opy_ (u"ࠨࠩಀ"))
      return bstack1llll1lll1_opy_
    else:
      bstack1llll1lll1_opy_ += bstack1l1ll11l_opy_(bstack1ll111lll1_opy_[bstack1lllll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪಁ")]) + bstack1lllll1l_opy_ (u"ࠥࠤࠧಂ") + (
              bstack1ll111lll1_opy_[bstack1lllll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ಃ")] or bstack1lllll1l_opy_ (u"ࠬ࠭಄")) + bstack1lllll1l_opy_ (u"ࠨࠬࠡࠤಅ")
      if bstack1ll111lll1_opy_[bstack1lllll1l_opy_ (u"ࠧࡰࡵࠪಆ")] == bstack1lllll1l_opy_ (u"࡙ࠣ࡬ࡲࡩࡵࡷࡴࠤಇ"):
        bstack1llll1lll1_opy_ += bstack1lllll1l_opy_ (u"ࠤ࡚࡭ࡳࠦࠢಈ")
      bstack1llll1lll1_opy_ += bstack1ll111lll1_opy_[bstack1lllll1l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧಉ")] or bstack1lllll1l_opy_ (u"ࠫࠬಊ")
      return bstack1llll1lll1_opy_
def bstack1ll11ll111_opy_(bstack11l11l1l1_opy_):
  if bstack11l11l1l1_opy_ == bstack1lllll1l_opy_ (u"ࠧࡪ࡯࡯ࡧࠥಋ"):
    return bstack1lllll1l_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡅࡲࡱࡵࡲࡥࡵࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩಌ")
  elif bstack11l11l1l1_opy_ == bstack1lllll1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ಍"):
    return bstack1lllll1l_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡆࡢ࡫࡯ࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫಎ")
  elif bstack11l11l1l1_opy_ == bstack1lllll1l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤಏ"):
    return bstack1lllll1l_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿࡭ࡲࡦࡧࡱ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧ࡭ࡲࡦࡧࡱࠦࡃࡖࡡࡴࡵࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪಐ")
  elif bstack11l11l1l1_opy_ == bstack1lllll1l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥ಑"):
    return bstack1lllll1l_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡳࡧࡧ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡸࡥࡥࠤࡁࡉࡷࡸ࡯ࡳ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧಒ")
  elif bstack11l11l1l1_opy_ == bstack1lllll1l_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢಓ"):
    return bstack1lllll1l_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࠦࡩࡪࡧ࠳࠳࠸࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࠨ࡫ࡥࡢ࠵࠵࠺ࠧࡄࡔࡪ࡯ࡨࡳࡺࡺ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬಔ")
  elif bstack11l11l1l1_opy_ == bstack1lllll1l_opy_ (u"ࠣࡴࡸࡲࡳ࡯࡮ࡨࠤಕ"):
    return bstack1lllll1l_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࡗࡻ࡮࡯࡫ࡱ࡫ࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪಖ")
  else:
    return bstack1lllll1l_opy_ (u"ࠪࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࠧಗ") + bstack1l1ll11l_opy_(
      bstack11l11l1l1_opy_) + bstack1lllll1l_opy_ (u"ࠫࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪಘ")
def bstack1l1llllll1_opy_(session):
  return bstack1lllll1l_opy_ (u"ࠬࡂࡴࡳࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡵࡳࡼࠨ࠾࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠢࡶࡩࡸࡹࡩࡰࡰ࠰ࡲࡦࡳࡥࠣࡀ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦࢀࢃࠢࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤࡢࡦࡱࡧ࡮࡬ࠤࡁࡿࢂࡂ࠯ࡢࡀ࠿࠳ࡹࡪ࠾ࡼࡿࡾࢁࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼࠰ࡶࡵࡂࠬಙ").format(
    session[bstack1lllll1l_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪಚ")], bstack1l1111l11_opy_(session), bstack1ll11ll111_opy_(session[bstack1lllll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡵࡣࡷࡹࡸ࠭ಛ")]),
    bstack1ll11ll111_opy_(session[bstack1lllll1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨಜ")]),
    bstack1l1ll11l_opy_(session[bstack1lllll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪಝ")] or session[bstack1lllll1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪಞ")] or bstack1lllll1l_opy_ (u"ࠫࠬಟ")) + bstack1lllll1l_opy_ (u"ࠧࠦࠢಠ") + (session[bstack1lllll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨಡ")] or bstack1lllll1l_opy_ (u"ࠧࠨಢ")),
    session[bstack1lllll1l_opy_ (u"ࠨࡱࡶࠫಣ")] + bstack1lllll1l_opy_ (u"ࠤࠣࠦತ") + session[bstack1lllll1l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧಥ")], session[bstack1lllll1l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ದ")] or bstack1lllll1l_opy_ (u"ࠬ࠭ಧ"),
    session[bstack1lllll1l_opy_ (u"࠭ࡣࡳࡧࡤࡸࡪࡪ࡟ࡢࡶࠪನ")] if session[bstack1lllll1l_opy_ (u"ࠧࡤࡴࡨࡥࡹ࡫ࡤࡠࡣࡷࠫ಩")] else bstack1lllll1l_opy_ (u"ࠨࠩಪ"))
def bstack1llll111ll_opy_(sessions, bstack1ll1ll1l11_opy_):
  try:
    bstack1llllll1l1_opy_ = bstack1lllll1l_opy_ (u"ࠤࠥಫ")
    if not os.path.exists(bstack1l1l1l1l_opy_):
      os.mkdir(bstack1l1l1l1l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lllll1l_opy_ (u"ࠪࡥࡸࡹࡥࡵࡵ࠲ࡶࡪࡶ࡯ࡳࡶ࠱࡬ࡹࡳ࡬ࠨಬ")), bstack1lllll1l_opy_ (u"ࠫࡷ࠭ಭ")) as f:
      bstack1llllll1l1_opy_ = f.read()
    bstack1llllll1l1_opy_ = bstack1llllll1l1_opy_.replace(bstack1lllll1l_opy_ (u"ࠬࢁࠥࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡅࡒ࡙ࡓ࡚ࠥࡾࠩಮ"), str(len(sessions)))
    bstack1llllll1l1_opy_ = bstack1llllll1l1_opy_.replace(bstack1lllll1l_opy_ (u"࠭ࡻࠦࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠩࢂ࠭ಯ"), bstack1ll1ll1l11_opy_)
    bstack1llllll1l1_opy_ = bstack1llllll1l1_opy_.replace(bstack1lllll1l_opy_ (u"ࠧࡼࠧࡅ࡙ࡎࡒࡄࡠࡐࡄࡑࡊࠫࡽࠨರ"),
                                              sessions[0].get(bstack1lllll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟࡯ࡣࡰࡩࠬಱ")) if sessions[0] else bstack1lllll1l_opy_ (u"ࠩࠪಲ"))
    with open(os.path.join(bstack1l1l1l1l_opy_, bstack1lllll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡵࡩࡵࡵࡲࡵ࠰࡫ࡸࡲࡲࠧಳ")), bstack1lllll1l_opy_ (u"ࠫࡼ࠭಴")) as stream:
      stream.write(bstack1llllll1l1_opy_.split(bstack1lllll1l_opy_ (u"ࠬࢁࠥࡔࡇࡖࡗࡎࡕࡎࡔࡡࡇࡅ࡙ࡇࠥࡾࠩವ"))[0])
      for session in sessions:
        stream.write(bstack1l1llllll1_opy_(session))
      stream.write(bstack1llllll1l1_opy_.split(bstack1lllll1l_opy_ (u"࠭ࡻࠦࡕࡈࡗࡘࡏࡏࡏࡕࡢࡈࡆ࡚ࡁࠦࡿࠪಶ"))[1])
    logger.info(bstack1lllll1l_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡦࡦࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡥࡹ࡮ࡲࡤࠡࡣࡵࡸ࡮࡬ࡡࡤࡶࡶࠤࡦࡺࠠࡼࡿࠪಷ").format(bstack1l1l1l1l_opy_));
  except Exception as e:
    logger.debug(bstack1lll1111ll_opy_.format(str(e)))
def bstack1l1l1ll11_opy_(bstack1111l1l1l_opy_):
  global CONFIG
  try:
    host = bstack1lllll1l_opy_ (u"ࠨࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧࠫಸ") if bstack1lllll1l_opy_ (u"ࠩࡤࡴࡵ࠭ಹ") in CONFIG else bstack1lllll1l_opy_ (u"ࠪࡥࡵ࡯ࠧ಺")
    user = CONFIG[bstack1lllll1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭಻")]
    key = CONFIG[bstack1lllll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ಼")]
    bstack1ll1llll11_opy_ = bstack1lllll1l_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬಽ") if bstack1lllll1l_opy_ (u"ࠧࡢࡲࡳࠫಾ") in CONFIG else bstack1lllll1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪಿ")
    url = bstack1lllll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠰࡭ࡷࡴࡴࠧೀ").format(user, key, host, bstack1ll1llll11_opy_,
                                                                                bstack1111l1l1l_opy_)
    headers = {
      bstack1lllll1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩು"): bstack1lllll1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧೂ"),
    }
    proxies = bstack1ll11l111_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1lllll1l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠪೃ")], response.json()))
  except Exception as e:
    logger.debug(bstack11l1l111l_opy_.format(str(e)))
def bstack1ll11111l_opy_():
  global CONFIG
  global bstack11111l1l_opy_
  try:
    if bstack1lllll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩೄ") in CONFIG:
      host = bstack1lllll1l_opy_ (u"ࠧࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦࠪ೅") if bstack1lllll1l_opy_ (u"ࠨࡣࡳࡴࠬೆ") in CONFIG else bstack1lllll1l_opy_ (u"ࠩࡤࡴ࡮࠭ೇ")
      user = CONFIG[bstack1lllll1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬೈ")]
      key = CONFIG[bstack1lllll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ೉")]
      bstack1ll1llll11_opy_ = bstack1lllll1l_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫೊ") if bstack1lllll1l_opy_ (u"࠭ࡡࡱࡲࠪೋ") in CONFIG else bstack1lllll1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩೌ")
      url = bstack1lllll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡽࢀ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠱࡮ࡸࡵ࡮ࠨ್").format(user, key, host, bstack1ll1llll11_opy_)
      headers = {
        bstack1lllll1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨ೎"): bstack1lllll1l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭೏"),
      }
      if bstack1lllll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭೐") in CONFIG:
        params = {bstack1lllll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ೑"): CONFIG[bstack1lllll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ೒")], bstack1lllll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ೓"): CONFIG[bstack1lllll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ೔")]}
      else:
        params = {bstack1lllll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧೕ"): CONFIG[bstack1lllll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ೖ")]}
      proxies = bstack1ll11l111_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1l1l11ll_opy_ = response.json()[0][bstack1lllll1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡤࡸ࡭ࡱࡪࠧ೗")]
        if bstack1l1l11ll_opy_:
          bstack1ll1ll1l11_opy_ = bstack1l1l11ll_opy_[bstack1lllll1l_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧࡤࡻࡲ࡭ࠩ೘")].split(bstack1lllll1l_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨ࠳ࡢࡶ࡫࡯ࡨࠬ೙"))[0] + bstack1lllll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡹ࠯ࠨ೚") + bstack1l1l11ll_opy_[
            bstack1lllll1l_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ೛")]
          logger.info(bstack1111lll11_opy_.format(bstack1ll1ll1l11_opy_))
          bstack11111l1l_opy_ = bstack1l1l11ll_opy_[bstack1lllll1l_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ೜")]
          bstack111l1111l_opy_ = CONFIG[bstack1lllll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ೝ")]
          if bstack1lllll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ೞ") in CONFIG:
            bstack111l1111l_opy_ += bstack1lllll1l_opy_ (u"ࠬࠦࠧ೟") + CONFIG[bstack1lllll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨೠ")]
          if bstack111l1111l_opy_ != bstack1l1l11ll_opy_[bstack1lllll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬೡ")]:
            logger.debug(bstack1llll1l1l_opy_.format(bstack1l1l11ll_opy_[bstack1lllll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ೢ")], bstack111l1111l_opy_))
          return [bstack1l1l11ll_opy_[bstack1lllll1l_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬೣ")], bstack1ll1ll1l11_opy_]
    else:
      logger.warn(bstack1l111ll11_opy_)
  except Exception as e:
    logger.debug(bstack1111ll1l_opy_.format(str(e)))
  return [None, None]
def bstack1lllll111l_opy_(url, bstack111l1l1l_opy_=False):
  global CONFIG
  global bstack1l1111ll1_opy_
  if not bstack1l1111ll1_opy_:
    hostname = bstack11ll1ll1_opy_(url)
    is_private = bstack111l11111_opy_(hostname)
    if (bstack1lllll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ೤") in CONFIG and not bstack11l1l1ll_opy_(CONFIG[bstack1lllll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ೥")])) and (is_private or bstack111l1l1l_opy_):
      bstack1l1111ll1_opy_ = hostname
def bstack11ll1ll1_opy_(url):
  return urlparse(url).hostname
def bstack111l11111_opy_(hostname):
  for bstack1ll11ll1ll_opy_ in bstack11l1l11ll_opy_:
    regex = re.compile(bstack1ll11ll1ll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1lll1llll_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1llll11l_opy_
  if not bstack1l1ll11l1_opy_.bstack1111lllll_opy_(CONFIG, bstack1llll11l_opy_):
    logger.warning(bstack1lllll1l_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹ࠮ࠣ೦"))
    return {}
  try:
    results = driver.execute_script(bstack1lllll1l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡺࡵࡳࡰࠣࡲࡪࡽࠠࡑࡴࡲࡱ࡮ࡹࡥࠩࡨࡸࡲࡨࡺࡩࡰࡰࠣࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠱ࠦࡲࡦ࡬ࡨࡧࡹ࠯ࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡴࡼࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡥࡲࡲࡸࡺࠠࡦࡸࡨࡲࡹࠦ࠽ࠡࡰࡨࡻࠥࡉࡵࡴࡶࡲࡱࡊࡼࡥ࡯ࡶࠫࠫࡆ࠷࠱࡚ࡡࡗࡅࡕࡥࡇࡆࡖࡢࡖࡊ࡙ࡕࡍࡖࡖࠫ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡹࡴࠡࡨࡱࠤࡂࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࠪࡨࡺࡪࡴࡴࠪࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡶࡪࡳ࡯ࡷࡧࡈࡺࡪࡴࡴࡍ࡫ࡶࡸࡪࡴࡥࡳࠪࠪࡅ࠶࠷࡙ࡠࡔࡈࡗ࡚ࡒࡔࡔࡡࡕࡉࡘࡖࡏࡏࡕࡈࠫ࠱ࠦࡦ࡯ࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡹ࡯࡭ࡸࡨࠬࡪࡼࡥ࡯ࡶ࠱ࡨࡪࡺࡡࡪ࡮࠱ࡨࡦࡺࡡࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡥࡩࡪࡅࡷࡧࡱࡸࡑ࡯ࡳࡵࡧࡱࡩࡷ࠮ࠧࡂ࠳࠴࡝ࡤࡘࡅࡔࡗࡏࡘࡘࡥࡒࡆࡕࡓࡓࡓ࡙ࡅࠨ࠮ࠣࡪࡳ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡻ࡮ࡴࡤࡰࡹ࠱ࡨ࡮ࡹࡰࡢࡶࡦ࡬ࡊࡼࡥ࡯ࡶࠫࡩࡻ࡫࡮ࡵࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠤࡨࡧࡴࡤࡪࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧ࡭ࡩࡨࡺࠨࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠍࠤࠥࠦࠠࠡࠢࠣࠤࢂ࠯࠻ࠋࠢࠣࠤࠥࠨࠢࠣ೧"))
    return results
  except Exception:
    logger.error(bstack1lllll1l_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡼ࡫ࡲࡦࠢࡩࡳࡺࡴࡤ࠯ࠤ೨"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1llll11l_opy_
  if not bstack1l1ll11l1_opy_.bstack1111lllll_opy_(CONFIG, bstack1llll11l_opy_):
    logger.warning(bstack1lllll1l_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼ࠲ࠧ೩"))
    return {}
  try:
    bstack1ll1llllll_opy_ = driver.execute_script(bstack1lllll1l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦ࡮ࡦࡹࠣࡔࡷࡵ࡭ࡪࡵࡨࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࠨࡳࡧࡶࡳࡱࡼࡥ࠭ࠢࡵࡩ࡯࡫ࡣࡵࠫࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡷࡿࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡴࡶࠣࡩࡻ࡫࡮ࡵࠢࡀࠤࡳ࡫ࡷࠡࡅࡸࡷࡹࡵ࡭ࡆࡸࡨࡲࡹ࠮ࠧࡂ࠳࠴࡝ࡤ࡚ࡁࡑࡡࡊࡉ࡙ࡥࡒࡆࡕࡘࡐ࡙࡙࡟ࡔࡗࡐࡑࡆࡘ࡙ࠨࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡶࡸࠥ࡬࡮ࠡ࠿ࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥ࠮ࡥࡷࡧࡱࡸ࠮ࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡸ࡫ࡱࡨࡴࡽ࠮ࡳࡧࡰࡳࡻ࡫ࡅࡷࡧࡱࡸࡑ࡯ࡳࡵࡧࡱࡩࡷ࠮ࠧࡂ࠳࠴࡝ࡤࡘࡅࡔࡗࡏࡘࡘࡥࡓࡖࡏࡐࡅࡗ࡟࡟ࡓࡇࡖࡔࡔࡔࡓࡆࠩ࠯ࠤ࡫ࡴࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡷࡴࡲࡶࡦࠪࡨࡺࡪࡴࡴ࠯ࡦࡨࡸࡦ࡯࡬࠯ࡵࡸࡱࡲࡧࡲࡺࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡦࡪࡤࡆࡸࡨࡲࡹࡒࡩࡴࡶࡨࡲࡪࡸࠨࠨࡃ࠴࠵࡞ࡥࡒࡆࡕࡘࡐ࡙࡙࡟ࡔࡗࡐࡑࡆࡘ࡙ࡠࡔࡈࡗࡕࡕࡎࡔࡇࠪ࠰ࠥ࡬࡮ࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡪࡩࡴࡲࡤࡸࡨ࡮ࡅࡷࡧࡱࡸ࠭࡫ࡶࡦࡰࡷ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠦࡣࡢࡶࡦ࡬ࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩ࡯࡫ࡣࡵࠪࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠏࠦࠠࠡࠢࠣࠤࠥࠦࡽࠪ࠽ࠍࠤࠥࠦࠠࠣࠤࠥ೪"))
    return bstack1ll1llllll_opy_
  except Exception:
    logger.error(bstack1lllll1l_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡶ࡯ࡰࡥࡷࡿࠠࡸࡣࡶࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦ೫"))
    return {}