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
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1l11l11l1_opy_ import bstack1lll1ll11l_opy_
import time
import requests
def bstack1lll11111_opy_():
  global CONFIG
  headers = {
        bstack11l1ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack11l1ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack11ll1lll_opy_(CONFIG, bstack1111l11ll_opy_)
  try:
    response = requests.get(bstack1111l11ll_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack111l1l1l1_opy_ = response.json()[bstack11l1ll_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l11l1l1l_opy_.format(response.json()))
      return bstack111l1l1l1_opy_
    else:
      logger.debug(bstack1111l1l1l_opy_.format(bstack11l1ll_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1111l1l1l_opy_.format(e))
def bstack1ll11l11ll_opy_(hub_url):
  global CONFIG
  url = bstack11l1ll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack11l1ll_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack11l1ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack11l1ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack11ll1lll_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1ll111ll11_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1llll1l11_opy_.format(hub_url, e))
def bstack1111l11l1_opy_():
  try:
    global bstack1llll1111_opy_
    bstack111l1l1l1_opy_ = bstack1lll11111_opy_()
    bstack11l1ll11_opy_ = []
    results = []
    for bstack1111lll11_opy_ in bstack111l1l1l1_opy_:
      bstack11l1ll11_opy_.append(bstack1l1l11111_opy_(target=bstack1ll11l11ll_opy_,args=(bstack1111lll11_opy_,)))
    for t in bstack11l1ll11_opy_:
      t.start()
    for t in bstack11l1ll11_opy_:
      results.append(t.join())
    bstack1lll111ll1_opy_ = {}
    for item in results:
      hub_url = item[bstack11l1ll_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack11l1ll_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1lll111ll1_opy_[hub_url] = latency
    bstack1ll1ll11l_opy_ = min(bstack1lll111ll1_opy_, key= lambda x: bstack1lll111ll1_opy_[x])
    bstack1llll1111_opy_ = bstack1ll1ll11l_opy_
    logger.debug(bstack1ll111l1l1_opy_.format(bstack1ll1ll11l_opy_))
  except Exception as e:
    logger.debug(bstack1ll1l1l1l1_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils.config import Config
from bstack_utils.helper import bstack1lll1l111l_opy_, bstack1l11l11l_opy_, bstack111l1lll_opy_, bstack1l1ll1l1l1_opy_, Notset, bstack1ll1111lll_opy_, \
  bstack11l11ll1_opy_, bstack111111l1_opy_, bstack1lll1l1ll1_opy_, bstack1ll11lll11_opy_, bstack11l11lll_opy_, bstack1ll1lllll_opy_, bstack1lll1ll1ll_opy_, \
  bstack11ll111ll_opy_, bstack1l1lll11l1_opy_, bstack11l11ll1l_opy_, bstack1ll111l1l_opy_, bstack11llll11l_opy_, bstack1ll11ll1_opy_, \
  bstack1llll11111_opy_, bstack1l1lll11l_opy_
from bstack_utils.bstack11l1llll_opy_ import bstack1lll1lll_opy_
from bstack_utils.bstack11l111ll_opy_ import bstack1l1ll1llll_opy_, bstack11l1l111l_opy_
from bstack_utils.bstack1ll11l1111_opy_ import bstack1l11l1111_opy_
from bstack_utils.proxy import bstack1l11ll1l_opy_, bstack11ll1lll_opy_, bstack1111l1l11_opy_, bstack1ll11ll1l_opy_
import bstack_utils.bstack11lll1l11_opy_ as bstack11ll11ll1_opy_
from browserstack_sdk.bstack1llllll1ll_opy_ import *
from browserstack_sdk.bstack1lll1llll_opy_ import *
from bstack_utils.bstack1l1l11l11l_opy_ import bstack1l1ll1l11_opy_
bstack1ll11lll_opy_ = bstack11l1ll_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack1l1ll1111l_opy_ = bstack11l1ll_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack1ll1l11l11_opy_ = None
CONFIG = {}
bstack1lll11ll1l_opy_ = {}
bstack1llllll1l_opy_ = {}
bstack1l111l11l_opy_ = None
bstack1llllllll_opy_ = None
bstack111l11l11_opy_ = None
bstack11lll1l1l_opy_ = -1
bstack1ll1l1l111_opy_ = 0
bstack111lll1ll_opy_ = bstack11l1ll111_opy_
bstack11111111l_opy_ = 1
bstack11lllllll_opy_ = False
bstack1l1l1l111_opy_ = False
bstack1ll11llll1_opy_ = bstack11l1ll_opy_ (u"ࠨࠩࢂ")
bstack1ll111ll1_opy_ = bstack11l1ll_opy_ (u"ࠩࠪࢃ")
bstack1l1llllll1_opy_ = False
bstack11lllll1_opy_ = True
bstack1l11lll1_opy_ = bstack11l1ll_opy_ (u"ࠪࠫࢄ")
bstack1llll11lll_opy_ = []
bstack1llll1111_opy_ = bstack11l1ll_opy_ (u"ࠫࠬࢅ")
bstack1ll1ll11l1_opy_ = False
bstack1lllll11ll_opy_ = None
bstack1l111ll11_opy_ = None
bstack11l1l111_opy_ = None
bstack11111l11_opy_ = -1
bstack1l1l11l1l1_opy_ = os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠬࢄࠧࢆ")), bstack11l1ll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstack11l1ll_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack11lll111_opy_ = 0
bstack1ll1111l_opy_ = []
bstack1ll111111l_opy_ = []
bstack111l111ll_opy_ = []
bstack1ll1ll1ll_opy_ = []
bstack111l11l1l_opy_ = bstack11l1ll_opy_ (u"ࠨࠩࢉ")
bstack1l1l1l1111_opy_ = bstack11l1ll_opy_ (u"ࠩࠪࢊ")
bstack1111111l_opy_ = False
bstack111llllll_opy_ = False
bstack1l1111l1_opy_ = {}
bstack111l1l1ll_opy_ = None
bstack1l11111ll_opy_ = None
bstack1l1lll1l_opy_ = None
bstack111111111_opy_ = None
bstack1l11l11ll_opy_ = None
bstack11111l1l1_opy_ = None
bstack11lll1lll_opy_ = None
bstack1111lllll_opy_ = None
bstack1lll1l1lll_opy_ = None
bstack1ll1llll_opy_ = None
bstack111l1llll_opy_ = None
bstack1l111l111_opy_ = None
bstack11111lll1_opy_ = None
bstack1l11l111_opy_ = None
bstack1l1ll1l1l_opy_ = None
bstack1ll1l1111_opy_ = None
bstack111l111l1_opy_ = None
bstack1ll1l111ll_opy_ = None
bstack1l1l1l1lll_opy_ = None
bstack1111l11l_opy_ = None
bstack1lll1111l1_opy_ = None
bstack11ll1ll1_opy_ = bstack11l1ll_opy_ (u"ࠥࠦࢋ")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack111lll1ll_opy_,
                    format=bstack11l1ll_opy_ (u"ࠫࡡࡴࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩࢌ"),
                    datefmt=bstack11l1ll_opy_ (u"ࠬࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧࢍ"),
                    stream=sys.stdout)
bstack1ll1l11ll1_opy_ = Config.get_instance()
percy = bstack1ll11lll1_opy_()
bstack1l1l1l1ll1_opy_ = bstack1lll1ll11l_opy_()
def bstack1111l1111_opy_():
  global CONFIG
  global bstack111lll1ll_opy_
  if bstack11l1ll_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨࢎ") in CONFIG:
    bstack111lll1ll_opy_ = bstack11l1111l1_opy_[CONFIG[bstack11l1ll_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ࢏")]]
    logging.getLogger().setLevel(bstack111lll1ll_opy_)
def bstack1ll1111ll1_opy_():
  global CONFIG
  global bstack1111111l_opy_
  global bstack1ll1l11ll1_opy_
  bstack1lll111111_opy_ = bstack1l1ll11lll_opy_(CONFIG)
  if (bstack11l1ll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ࢐") in bstack1lll111111_opy_ and str(bstack1lll111111_opy_[bstack11l1ll_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ࢑")]).lower() == bstack11l1ll_opy_ (u"ࠪࡸࡷࡻࡥࠨ࢒")):
    bstack1111111l_opy_ = True
  bstack1ll1l11ll1_opy_.bstack1ll1l1ll1l_opy_(bstack1lll111111_opy_.get(bstack11l1ll_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࢓"), False))
def bstack1l11ll1l1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack11l1ll1l1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1lll11ll1_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack11l1ll_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࢔") == args[i].lower() or bstack11l1ll_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࢕") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l11lll1_opy_
      bstack1l11lll1_opy_ += bstack11l1ll_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ࢖") + path
      return path
  return None
bstack1ll1ll1l11_opy_ = re.compile(bstack11l1ll_opy_ (u"ࡳࠤ࠱࠮ࡄࡢࠤࡼࠪ࠱࠮ࡄ࠯ࡽ࠯ࠬࡂࠦࢗ"))
def bstack1llll1l11l_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1ll1ll1l11_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11l1ll_opy_ (u"ࠤࠧࡿࠧ࢘") + group + bstack11l1ll_opy_ (u"ࠥࢁ࢙ࠧ"), os.environ.get(group))
  return value
def bstack1ll111ll1l_opy_():
  bstack1ll1llll1l_opy_ = bstack1lll11ll1_opy_()
  if bstack1ll1llll1l_opy_ and os.path.exists(os.path.abspath(bstack1ll1llll1l_opy_)):
    fileName = bstack1ll1llll1l_opy_
  if bstack11l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࢚") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࢛ࠩ")])) and not bstack11l1ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨ࢜") in locals():
    fileName = os.environ[bstack11l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢝")]
  if bstack11l1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪ࢞") in locals():
    bstack11lll1l_opy_ = os.path.abspath(fileName)
  else:
    bstack11lll1l_opy_ = bstack11l1ll_opy_ (u"ࠩࠪ࢟")
  bstack1ll1l1ll_opy_ = os.getcwd()
  bstack1l11111l1_opy_ = bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ࢠ")
  bstack1llll1llll_opy_ = bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨࢡ")
  while (not os.path.exists(bstack11lll1l_opy_)) and bstack1ll1l1ll_opy_ != bstack11l1ll_opy_ (u"ࠧࠨࢢ"):
    bstack11lll1l_opy_ = os.path.join(bstack1ll1l1ll_opy_, bstack1l11111l1_opy_)
    if not os.path.exists(bstack11lll1l_opy_):
      bstack11lll1l_opy_ = os.path.join(bstack1ll1l1ll_opy_, bstack1llll1llll_opy_)
    if bstack1ll1l1ll_opy_ != os.path.dirname(bstack1ll1l1ll_opy_):
      bstack1ll1l1ll_opy_ = os.path.dirname(bstack1ll1l1ll_opy_)
    else:
      bstack1ll1l1ll_opy_ = bstack11l1ll_opy_ (u"ࠨࠢࢣ")
  if not os.path.exists(bstack11lll1l_opy_):
    bstack1l1ll1ll1l_opy_(
      bstack1ll111lll_opy_.format(os.getcwd()))
  try:
    with open(bstack11lll1l_opy_, bstack11l1ll_opy_ (u"ࠧࡳࠩࢤ")) as stream:
      yaml.add_implicit_resolver(bstack11l1ll_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࢥ"), bstack1ll1ll1l11_opy_)
      yaml.add_constructor(bstack11l1ll_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࢦ"), bstack1llll1l11l_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack11lll1l_opy_, bstack11l1ll_opy_ (u"ࠪࡶࠬࢧ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1l1ll1ll1l_opy_(bstack1l1ll111l1_opy_.format(str(exc)))
def bstack1l1lll1111_opy_(config):
  bstack1llll111ll_opy_ = bstack1l1l1ll1l_opy_(config)
  for option in list(bstack1llll111ll_opy_):
    if option.lower() in bstack111l11lll_opy_ and option != bstack111l11lll_opy_[option.lower()]:
      bstack1llll111ll_opy_[bstack111l11lll_opy_[option.lower()]] = bstack1llll111ll_opy_[option]
      del bstack1llll111ll_opy_[option]
  return config
def bstack1l111l1ll_opy_():
  global bstack1llllll1l_opy_
  for key, bstack1ll1111111_opy_ in bstack1ll1ll1l1_opy_.items():
    if isinstance(bstack1ll1111111_opy_, list):
      for var in bstack1ll1111111_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1llllll1l_opy_[key] = os.environ[var]
          break
    elif bstack1ll1111111_opy_ in os.environ and os.environ[bstack1ll1111111_opy_] and str(os.environ[bstack1ll1111111_opy_]).strip():
      bstack1llllll1l_opy_[key] = os.environ[bstack1ll1111111_opy_]
  if bstack11l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ") in os.environ:
    bstack1llllll1l_opy_[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢩ")] = {}
    bstack1llllll1l_opy_[bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")][bstack11l1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢫ")] = os.environ[bstack11l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࢬ")]
def bstack11l1l1ll1_opy_():
  global bstack1lll11ll1l_opy_
  global bstack1l11lll1_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack11l1ll_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢭ").lower() == val.lower():
      bstack1lll11ll1l_opy_[bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢮ")] = {}
      bstack1lll11ll1l_opy_[bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢯ")][bstack11l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1ll1lll111_opy_ in bstack111l1l111_opy_.items():
    if isinstance(bstack1ll1lll111_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1ll1lll111_opy_:
          if idx < len(sys.argv) and bstack11l1ll_opy_ (u"࠭࠭࠮ࠩࢱ") + var.lower() == val.lower() and not key in bstack1lll11ll1l_opy_:
            bstack1lll11ll1l_opy_[key] = sys.argv[idx + 1]
            bstack1l11lll1_opy_ += bstack11l1ll_opy_ (u"ࠧࠡ࠯࠰ࠫࢲ") + var + bstack11l1ll_opy_ (u"ࠨࠢࠪࢳ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack11l1ll_opy_ (u"ࠩ࠰࠱ࠬࢴ") + bstack1ll1lll111_opy_.lower() == val.lower() and not key in bstack1lll11ll1l_opy_:
          bstack1lll11ll1l_opy_[key] = sys.argv[idx + 1]
          bstack1l11lll1_opy_ += bstack11l1ll_opy_ (u"ࠪࠤ࠲࠳ࠧࢵ") + bstack1ll1lll111_opy_ + bstack11l1ll_opy_ (u"ࠫࠥ࠭ࢶ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1ll1llll11_opy_(config):
  bstack1l1l11ll1_opy_ = config.keys()
  for bstack1111111l1_opy_, bstack1llllll111_opy_ in bstack1l1l1ll11_opy_.items():
    if bstack1llllll111_opy_ in bstack1l1l11ll1_opy_:
      config[bstack1111111l1_opy_] = config[bstack1llllll111_opy_]
      del config[bstack1llllll111_opy_]
  for bstack1111111l1_opy_, bstack1llllll111_opy_ in bstack11l1111l_opy_.items():
    if isinstance(bstack1llllll111_opy_, list):
      for bstack1lll1111_opy_ in bstack1llllll111_opy_:
        if bstack1lll1111_opy_ in bstack1l1l11ll1_opy_:
          config[bstack1111111l1_opy_] = config[bstack1lll1111_opy_]
          del config[bstack1lll1111_opy_]
          break
    elif bstack1llllll111_opy_ in bstack1l1l11ll1_opy_:
      config[bstack1111111l1_opy_] = config[bstack1llllll111_opy_]
      del config[bstack1llllll111_opy_]
  for bstack1lll1111_opy_ in list(config):
    for bstack1ll111l1_opy_ in bstack1llll1l1ll_opy_:
      if bstack1lll1111_opy_.lower() == bstack1ll111l1_opy_.lower() and bstack1lll1111_opy_ != bstack1ll111l1_opy_:
        config[bstack1ll111l1_opy_] = config[bstack1lll1111_opy_]
        del config[bstack1lll1111_opy_]
  bstack11l1l1lll_opy_ = []
  if bstack11l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࢷ") in config:
    bstack11l1l1lll_opy_ = config[bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࢸ")]
  for platform in bstack11l1l1lll_opy_:
    for bstack1lll1111_opy_ in list(platform):
      for bstack1ll111l1_opy_ in bstack1llll1l1ll_opy_:
        if bstack1lll1111_opy_.lower() == bstack1ll111l1_opy_.lower() and bstack1lll1111_opy_ != bstack1ll111l1_opy_:
          platform[bstack1ll111l1_opy_] = platform[bstack1lll1111_opy_]
          del platform[bstack1lll1111_opy_]
  for bstack1111111l1_opy_, bstack1llllll111_opy_ in bstack11l1111l_opy_.items():
    for platform in bstack11l1l1lll_opy_:
      if isinstance(bstack1llllll111_opy_, list):
        for bstack1lll1111_opy_ in bstack1llllll111_opy_:
          if bstack1lll1111_opy_ in platform:
            platform[bstack1111111l1_opy_] = platform[bstack1lll1111_opy_]
            del platform[bstack1lll1111_opy_]
            break
      elif bstack1llllll111_opy_ in platform:
        platform[bstack1111111l1_opy_] = platform[bstack1llllll111_opy_]
        del platform[bstack1llllll111_opy_]
  for bstack111lll11l_opy_ in bstack111l111l_opy_:
    if bstack111lll11l_opy_ in config:
      if not bstack111l111l_opy_[bstack111lll11l_opy_] in config:
        config[bstack111l111l_opy_[bstack111lll11l_opy_]] = {}
      config[bstack111l111l_opy_[bstack111lll11l_opy_]].update(config[bstack111lll11l_opy_])
      del config[bstack111lll11l_opy_]
  for platform in bstack11l1l1lll_opy_:
    for bstack111lll11l_opy_ in bstack111l111l_opy_:
      if bstack111lll11l_opy_ in list(platform):
        if not bstack111l111l_opy_[bstack111lll11l_opy_] in platform:
          platform[bstack111l111l_opy_[bstack111lll11l_opy_]] = {}
        platform[bstack111l111l_opy_[bstack111lll11l_opy_]].update(platform[bstack111lll11l_opy_])
        del platform[bstack111lll11l_opy_]
  config = bstack1l1lll1111_opy_(config)
  return config
def bstack1l11ll111_opy_(config):
  global bstack1ll111ll1_opy_
  if bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫࢹ") in config and str(config[bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬࢺ")]).lower() != bstack11l1ll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨࢻ"):
    if not bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࢼ") in config:
      config[bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࢽ")] = {}
    if not bstack11l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢾ") in config[bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢿ")]:
      bstack11ll1l11_opy_ = datetime.datetime.now()
      bstack1lll11ll11_opy_ = bstack11ll1l11_opy_.strftime(bstack11l1ll_opy_ (u"ࠧࠦࡦࡢࠩࡧࡥࠥࡉࠧࡐࠫࣀ"))
      hostname = socket.gethostname()
      bstack11l1l1l1l_opy_ = bstack11l1ll_opy_ (u"ࠨࠩࣁ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11l1ll_opy_ (u"ࠩࡾࢁࡤࢁࡽࡠࡽࢀࠫࣂ").format(bstack1lll11ll11_opy_, hostname, bstack11l1l1l1l_opy_)
      config[bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣃ")][bstack11l1ll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣄ")] = identifier
    bstack1ll111ll1_opy_ = config[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣅ")][bstack11l1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣆ")]
  return config
def bstack1lll1l1l1l_opy_():
  bstack11111ll1_opy_ =  bstack1ll11lll11_opy_()[bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷ࠭ࣇ")]
  return bstack11111ll1_opy_ if bstack11111ll1_opy_ else -1
def bstack111l1111_opy_(bstack11111ll1_opy_):
  global CONFIG
  if not bstack11l1ll_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣈ") in CONFIG[bstack11l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣉ")]:
    return
  CONFIG[bstack11l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")] = CONFIG[bstack11l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣋")].replace(
    bstack11l1ll_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧ࣌"),
    str(bstack11111ll1_opy_)
  )
def bstack11111l111_opy_():
  global CONFIG
  if not bstack11l1ll_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬ࣍") in CONFIG[bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣎")]:
    return
  bstack11ll1l11_opy_ = datetime.datetime.now()
  bstack1lll11ll11_opy_ = bstack11ll1l11_opy_.strftime(bstack11l1ll_opy_ (u"ࠨࠧࡧ࠱ࠪࡨ࠭ࠦࡊ࠽ࠩࡒ࣏࠭"))
  CONFIG[bstack11l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")] = CONFIG[bstack11l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣑ࠬ")].replace(
    bstack11l1ll_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿ࣒ࠪ"),
    bstack1lll11ll11_opy_
  )
def bstack11ll1l1l_opy_():
  global CONFIG
  if bstack11l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ") in CONFIG and not bool(CONFIG[bstack11l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣔ")]):
    del CONFIG[bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣕ")]
    return
  if not bstack11l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ") in CONFIG:
    CONFIG[bstack11l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣗ")] = bstack11l1ll_opy_ (u"ࠪࠧࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣘ")
  if bstack11l1ll_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪࣙ") in CONFIG[bstack11l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣚ")]:
    bstack11111l111_opy_()
    os.environ[bstack11l1ll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪࣛ")] = CONFIG[bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣜ")]
  if not bstack11l1ll_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣝ") in CONFIG[bstack11l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣞ")]:
    return
  bstack11111ll1_opy_ = bstack11l1ll_opy_ (u"ࠪࠫࣟ")
  bstack111ll1ll1_opy_ = bstack1lll1l1l1l_opy_()
  if bstack111ll1ll1_opy_ != -1:
    bstack11111ll1_opy_ = bstack11l1ll_opy_ (u"ࠫࡈࡏࠠࠨ࣠") + str(bstack111ll1ll1_opy_)
  if bstack11111ll1_opy_ == bstack11l1ll_opy_ (u"ࠬ࠭࣡"):
    bstack11lllll11_opy_ = bstack1l1l1l11_opy_(CONFIG[bstack11l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ࣢")])
    if bstack11lllll11_opy_ != -1:
      bstack11111ll1_opy_ = str(bstack11lllll11_opy_)
  if bstack11111ll1_opy_:
    bstack111l1111_opy_(bstack11111ll1_opy_)
    os.environ[bstack11l1ll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࣣࠫ")] = CONFIG[bstack11l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣤ")]
def bstack1lll1l11_opy_(bstack1l11ll11l_opy_, bstack1ll1l1ll1_opy_, path):
  bstack1l1l1ll1l1_opy_ = {
    bstack11l1ll_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣥ"): bstack1ll1l1ll1_opy_
  }
  if os.path.exists(path):
    bstack1l1111lll_opy_ = json.load(open(path, bstack11l1ll_opy_ (u"ࠪࡶࡧࣦ࠭")))
  else:
    bstack1l1111lll_opy_ = {}
  bstack1l1111lll_opy_[bstack1l11ll11l_opy_] = bstack1l1l1ll1l1_opy_
  with open(path, bstack11l1ll_opy_ (u"ࠦࡼ࠱ࠢࣧ")) as outfile:
    json.dump(bstack1l1111lll_opy_, outfile)
def bstack1l1l1l11_opy_(bstack1l11ll11l_opy_):
  bstack1l11ll11l_opy_ = str(bstack1l11ll11l_opy_)
  bstack1lll1lll1l_opy_ = os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠬࢄࠧࣨ")), bstack11l1ll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࣩ࠭"))
  try:
    if not os.path.exists(bstack1lll1lll1l_opy_):
      os.makedirs(bstack1lll1lll1l_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠧࡿࠩ࣪")), bstack11l1ll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ࣫"), bstack11l1ll_opy_ (u"ࠩ࠱ࡦࡺ࡯࡬ࡥ࠯ࡱࡥࡲ࡫࠭ࡤࡣࡦ࡬ࡪ࠴ࡪࡴࡱࡱࠫ࣬"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11l1ll_opy_ (u"ࠪࡻ࣭ࠬ")):
        pass
      with open(file_path, bstack11l1ll_opy_ (u"ࠦࡼ࠱࣮ࠢ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11l1ll_opy_ (u"ࠬࡸ࣯ࠧ")) as bstack1lll11l1ll_opy_:
      bstack1ll1lll1_opy_ = json.load(bstack1lll11l1ll_opy_)
    if bstack1l11ll11l_opy_ in bstack1ll1lll1_opy_:
      bstack1ll11llll_opy_ = bstack1ll1lll1_opy_[bstack1l11ll11l_opy_][bstack11l1ll_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣰࠪ")]
      bstack11l11l1l_opy_ = int(bstack1ll11llll_opy_) + 1
      bstack1lll1l11_opy_(bstack1l11ll11l_opy_, bstack11l11l1l_opy_, file_path)
      return bstack11l11l1l_opy_
    else:
      bstack1lll1l11_opy_(bstack1l11ll11l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack11l11l111_opy_.format(str(e)))
    return -1
def bstack1l1l111lll_opy_(config):
  if not config[bstack11l1ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࣱࠩ")] or not config[bstack11l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࣲࠫ")]:
    return True
  else:
    return False
def bstack1llll11ll1_opy_(config, index=0):
  global bstack1l1llllll1_opy_
  bstack1ll111l11_opy_ = {}
  caps = bstack1lll11l1_opy_ + bstack1111lll1_opy_
  if bstack1l1llllll1_opy_:
    caps += bstack1llllll1l1_opy_
  for key in config:
    if key in caps + [bstack11l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࣳ")]:
      continue
    bstack1ll111l11_opy_[key] = config[key]
  if bstack11l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ") in config:
    for bstack1lll111lll_opy_ in config[bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣵ")][index]:
      if bstack1lll111lll_opy_ in caps + [bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࣶࠪ"), bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧࣷ")]:
        continue
      bstack1ll111l11_opy_[bstack1lll111lll_opy_] = config[bstack11l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣸ")][index][bstack1lll111lll_opy_]
  bstack1ll111l11_opy_[bstack11l1ll_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࣹࠪ")] = socket.gethostname()
  if bstack11l1ll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࣺࠪ") in bstack1ll111l11_opy_:
    del (bstack1ll111l11_opy_[bstack11l1ll_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫࣻ")])
  return bstack1ll111l11_opy_
def bstack1l1l11llll_opy_(config):
  global bstack1l1llllll1_opy_
  bstack1lllll1111_opy_ = {}
  caps = bstack1111lll1_opy_
  if bstack1l1llllll1_opy_:
    caps += bstack1llllll1l1_opy_
  for key in caps:
    if key in config:
      bstack1lllll1111_opy_[key] = config[key]
  return bstack1lllll1111_opy_
def bstack111111ll_opy_(bstack1ll111l11_opy_, bstack1lllll1111_opy_):
  bstack1lll1l111_opy_ = {}
  for key in bstack1ll111l11_opy_.keys():
    if key in bstack1l1l1ll11_opy_:
      bstack1lll1l111_opy_[bstack1l1l1ll11_opy_[key]] = bstack1ll111l11_opy_[key]
    else:
      bstack1lll1l111_opy_[key] = bstack1ll111l11_opy_[key]
  for key in bstack1lllll1111_opy_:
    if key in bstack1l1l1ll11_opy_:
      bstack1lll1l111_opy_[bstack1l1l1ll11_opy_[key]] = bstack1lllll1111_opy_[key]
    else:
      bstack1lll1l111_opy_[key] = bstack1lllll1111_opy_[key]
  return bstack1lll1l111_opy_
def bstack1l1ll11l11_opy_(config, index=0):
  global bstack1l1llllll1_opy_
  config = copy.deepcopy(config)
  caps = {}
  bstack1lllll1111_opy_ = bstack1l1l11llll_opy_(config)
  bstack1ll1ll111_opy_ = bstack1111lll1_opy_
  bstack1ll1ll111_opy_ += bstack1l1llll111_opy_
  if bstack1l1llllll1_opy_:
    bstack1ll1ll111_opy_ += bstack1llllll1l1_opy_
  if bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ") in config:
    if bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪࣽ") in config[bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩࣾ")][index]:
      caps[bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬࣿ")] = config[bstack11l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫऀ")][index][bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧँ")]
    if bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫं") in config[bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧः")][index]:
      caps[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऄ")] = str(config[bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index][bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨआ")])
    bstack111llll1l_opy_ = {}
    for bstack1l1l111l_opy_ in bstack1ll1ll111_opy_:
      if bstack1l1l111l_opy_ in config[bstack11l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index]:
        if bstack1l1l111l_opy_ == bstack11l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫई"):
          try:
            bstack111llll1l_opy_[bstack1l1l111l_opy_] = str(config[bstack11l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack1l1l111l_opy_] * 1.0)
          except:
            bstack111llll1l_opy_[bstack1l1l111l_opy_] = str(config[bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऊ")][index][bstack1l1l111l_opy_])
        else:
          bstack111llll1l_opy_[bstack1l1l111l_opy_] = config[bstack11l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऋ")][index][bstack1l1l111l_opy_]
        del (config[bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩऌ")][index][bstack1l1l111l_opy_])
    bstack1lllll1111_opy_ = update(bstack1lllll1111_opy_, bstack111llll1l_opy_)
  bstack1ll111l11_opy_ = bstack1llll11ll1_opy_(config, index)
  for bstack1lll1111_opy_ in bstack1111lll1_opy_ + [bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬऍ"), bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩऎ")]:
    if bstack1lll1111_opy_ in bstack1ll111l11_opy_:
      bstack1lllll1111_opy_[bstack1lll1111_opy_] = bstack1ll111l11_opy_[bstack1lll1111_opy_]
      del (bstack1ll111l11_opy_[bstack1lll1111_opy_])
  if bstack1ll1111lll_opy_(config):
    bstack1ll111l11_opy_[bstack11l1ll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩए")] = True
    caps.update(bstack1lllll1111_opy_)
    caps[bstack11l1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫऐ")] = bstack1ll111l11_opy_
  else:
    bstack1ll111l11_opy_[bstack11l1ll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫऑ")] = False
    caps.update(bstack111111ll_opy_(bstack1ll111l11_opy_, bstack1lllll1111_opy_))
    if bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪऒ") in caps:
      caps[bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧओ")] = caps[bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬऔ")]
      del (caps[bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭क")])
    if bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪख") in caps:
      caps[bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬग")] = caps[bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬघ")]
      del (caps[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ङ")])
  return caps
def bstack1l1111111_opy_():
  global bstack1llll1111_opy_
  if bstack11l1ll1l1_opy_() <= version.parse(bstack11l1ll_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭च")):
    if bstack1llll1111_opy_ != bstack11l1ll_opy_ (u"ࠧࠨछ"):
      return bstack11l1ll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤज") + bstack1llll1111_opy_ + bstack11l1ll_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨझ")
    return bstack1lllll11_opy_
  if bstack1llll1111_opy_ != bstack11l1ll_opy_ (u"ࠪࠫञ"):
    return bstack11l1ll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨट") + bstack1llll1111_opy_ + bstack11l1ll_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨठ")
  return bstack1l1l1111_opy_
def bstack1l1l1l11l_opy_(options):
  return hasattr(options, bstack11l1ll_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧड"))
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
def bstack111ll1l1_opy_(options, bstack11l11l1l1_opy_):
  for bstack1ll1lll1ll_opy_ in bstack11l11l1l1_opy_:
    if bstack1ll1lll1ll_opy_ in [bstack11l1ll_opy_ (u"ࠧࡢࡴࡪࡷࠬढ"), bstack11l1ll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬण")]:
      continue
    if bstack1ll1lll1ll_opy_ in options._experimental_options:
      options._experimental_options[bstack1ll1lll1ll_opy_] = update(options._experimental_options[bstack1ll1lll1ll_opy_],
                                                         bstack11l11l1l1_opy_[bstack1ll1lll1ll_opy_])
    else:
      options.add_experimental_option(bstack1ll1lll1ll_opy_, bstack11l11l1l1_opy_[bstack1ll1lll1ll_opy_])
  if bstack11l1ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧत") in bstack11l11l1l1_opy_:
    for arg in bstack11l11l1l1_opy_[bstack11l1ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨथ")]:
      options.add_argument(arg)
    del (bstack11l11l1l1_opy_[bstack11l1ll_opy_ (u"ࠫࡦࡸࡧࡴࠩद")])
  if bstack11l1ll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩध") in bstack11l11l1l1_opy_:
    for ext in bstack11l11l1l1_opy_[bstack11l1ll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪन")]:
      options.add_extension(ext)
    del (bstack11l11l1l1_opy_[bstack11l1ll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫऩ")])
def bstack1l1ll11ll1_opy_(options, bstack1ll1ll1l_opy_):
  if bstack11l1ll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧप") in bstack1ll1ll1l_opy_:
    for bstack1l1l1l111l_opy_ in bstack1ll1ll1l_opy_[bstack11l1ll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨफ")]:
      if bstack1l1l1l111l_opy_ in options._preferences:
        options._preferences[bstack1l1l1l111l_opy_] = update(options._preferences[bstack1l1l1l111l_opy_], bstack1ll1ll1l_opy_[bstack11l1ll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩब")][bstack1l1l1l111l_opy_])
      else:
        options.set_preference(bstack1l1l1l111l_opy_, bstack1ll1ll1l_opy_[bstack11l1ll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪभ")][bstack1l1l1l111l_opy_])
  if bstack11l1ll_opy_ (u"ࠬࡧࡲࡨࡵࠪम") in bstack1ll1ll1l_opy_:
    for arg in bstack1ll1ll1l_opy_[bstack11l1ll_opy_ (u"࠭ࡡࡳࡩࡶࠫय")]:
      options.add_argument(arg)
def bstack1l11llll_opy_(options, bstack1l1l1l11l1_opy_):
  if bstack11l1ll_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࠨर") in bstack1l1l1l11l1_opy_:
    options.use_webview(bool(bstack1l1l1l11l1_opy_[bstack11l1ll_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩऱ")]))
  bstack111ll1l1_opy_(options, bstack1l1l1l11l1_opy_)
def bstack11ll11111_opy_(options, bstack1ll1lll11l_opy_):
  for bstack1lllllll1_opy_ in bstack1ll1lll11l_opy_:
    if bstack1lllllll1_opy_ in [bstack11l1ll_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ल"), bstack11l1ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨळ")]:
      continue
    options.set_capability(bstack1lllllll1_opy_, bstack1ll1lll11l_opy_[bstack1lllllll1_opy_])
  if bstack11l1ll_opy_ (u"ࠫࡦࡸࡧࡴࠩऴ") in bstack1ll1lll11l_opy_:
    for arg in bstack1ll1lll11l_opy_[bstack11l1ll_opy_ (u"ࠬࡧࡲࡨࡵࠪव")]:
      options.add_argument(arg)
  if bstack11l1ll_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪश") in bstack1ll1lll11l_opy_:
    options.bstack1ll11l1ll1_opy_(bool(bstack1ll1lll11l_opy_[bstack11l1ll_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫष")]))
def bstack1ll1l1l1_opy_(options, bstack11111lll_opy_):
  for bstack1l1l1l1ll_opy_ in bstack11111lll_opy_:
    if bstack1l1l1l1ll_opy_ in [bstack11l1ll_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस"), bstack11l1ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧह")]:
      continue
    options._options[bstack1l1l1l1ll_opy_] = bstack11111lll_opy_[bstack1l1l1l1ll_opy_]
  if bstack11l1ll_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧऺ") in bstack11111lll_opy_:
    for bstack111ll1lll_opy_ in bstack11111lll_opy_[bstack11l1ll_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऻ")]:
      options.bstack1lllll111l_opy_(
        bstack111ll1lll_opy_, bstack11111lll_opy_[bstack11l1ll_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴ़ࠩ")][bstack111ll1lll_opy_])
  if bstack11l1ll_opy_ (u"࠭ࡡࡳࡩࡶࠫऽ") in bstack11111lll_opy_:
    for arg in bstack11111lll_opy_[bstack11l1ll_opy_ (u"ࠧࡢࡴࡪࡷࠬा")]:
      options.add_argument(arg)
def bstack1l111ll1l_opy_(options, caps):
  if not hasattr(options, bstack11l1ll_opy_ (u"ࠨࡍࡈ࡝ࠬि")):
    return
  if options.KEY == bstack11l1ll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧी") and options.KEY in caps:
    bstack111ll1l1_opy_(options, caps[bstack11l1ll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨु")])
  elif options.KEY == bstack11l1ll_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩू") and options.KEY in caps:
    bstack1l1ll11ll1_opy_(options, caps[bstack11l1ll_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪृ")])
  elif options.KEY == bstack11l1ll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧॄ") and options.KEY in caps:
    bstack11ll11111_opy_(options, caps[bstack11l1ll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨॅ")])
  elif options.KEY == bstack11l1ll_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩॆ") and options.KEY in caps:
    bstack1l11llll_opy_(options, caps[bstack11l1ll_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪे")])
  elif options.KEY == bstack11l1ll_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩै") and options.KEY in caps:
    bstack1ll1l1l1_opy_(options, caps[bstack11l1ll_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪॉ")])
def bstack1l1ll11l1_opy_(caps):
  global bstack1l1llllll1_opy_
  if isinstance(os.environ.get(bstack11l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ॊ")), str):
    bstack1l1llllll1_opy_ = eval(os.getenv(bstack11l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧो")))
  if bstack1l1llllll1_opy_:
    if bstack1l11ll1l1_opy_() < version.parse(bstack11l1ll_opy_ (u"ࠧ࠳࠰࠶࠲࠵࠭ौ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11l1ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ्")
    if bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧॎ") in caps:
      browser = caps[bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨॏ")]
    elif bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬॐ") in caps:
      browser = caps[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭॑")]
    browser = str(browser).lower()
    if browser == bstack11l1ll_opy_ (u"࠭ࡩࡱࡪࡲࡲࡪ॒࠭") or browser == bstack11l1ll_opy_ (u"ࠧࡪࡲࡤࡨࠬ॓"):
      browser = bstack11l1ll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨ॔")
    if browser == bstack11l1ll_opy_ (u"ࠩࡶࡥࡲࡹࡵ࡯ࡩࠪॕ"):
      browser = bstack11l1ll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪॖ")
    if browser not in [bstack11l1ll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫॗ"), bstack11l1ll_opy_ (u"ࠬ࡫ࡤࡨࡧࠪक़"), bstack11l1ll_opy_ (u"࠭ࡩࡦࠩख़"), bstack11l1ll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧग़"), bstack11l1ll_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩज़")]:
      return None
    try:
      package = bstack11l1ll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡼࡿ࠱ࡳࡵࡺࡩࡰࡰࡶࠫड़").format(browser)
      name = bstack11l1ll_opy_ (u"ࠪࡓࡵࡺࡩࡰࡰࡶࠫढ़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l1l1l11l_opy_(options):
        return None
      for bstack1lll1111_opy_ in caps.keys():
        options.set_capability(bstack1lll1111_opy_, caps[bstack1lll1111_opy_])
      bstack1l111ll1l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1ll11ll11l_opy_(options, bstack1ll111ll_opy_):
  if not bstack1l1l1l11l_opy_(options):
    return
  for bstack1lll1111_opy_ in bstack1ll111ll_opy_.keys():
    if bstack1lll1111_opy_ in bstack1l1llll111_opy_:
      continue
    if bstack1lll1111_opy_ in options._caps and type(options._caps[bstack1lll1111_opy_]) in [dict, list]:
      options._caps[bstack1lll1111_opy_] = update(options._caps[bstack1lll1111_opy_], bstack1ll111ll_opy_[bstack1lll1111_opy_])
    else:
      options.set_capability(bstack1lll1111_opy_, bstack1ll111ll_opy_[bstack1lll1111_opy_])
  bstack1l111ll1l_opy_(options, bstack1ll111ll_opy_)
  if bstack11l1ll_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪफ़") in options._caps:
    if options._caps[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪय़")] and options._caps[bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")].lower() != bstack11l1ll_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨॡ"):
      del options._caps[bstack11l1ll_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧॢ")]
def bstack1l11111l_opy_(proxy_config):
  if bstack11l1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॣ") in proxy_config:
    proxy_config[bstack11l1ll_opy_ (u"ࠪࡷࡸࡲࡐࡳࡱࡻࡽࠬ।")] = proxy_config[bstack11l1ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ॥")]
    del (proxy_config[bstack11l1ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ०")])
  if bstack11l1ll_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ१") in proxy_config and proxy_config[bstack11l1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ२")].lower() != bstack11l1ll_opy_ (u"ࠨࡦ࡬ࡶࡪࡩࡴࠨ३"):
    proxy_config[bstack11l1ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ४")] = bstack11l1ll_opy_ (u"ࠪࡱࡦࡴࡵࡢ࡮ࠪ५")
  if bstack11l1ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡄࡹࡹࡵࡣࡰࡰࡩ࡭࡬࡛ࡲ࡭ࠩ६") in proxy_config:
    proxy_config[bstack11l1ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ७")] = bstack11l1ll_opy_ (u"࠭ࡰࡢࡥࠪ८")
  return proxy_config
def bstack1llll11l1l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11l1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭९") in config:
    return proxy
  config[bstack11l1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧ॰")] = bstack1l11111l_opy_(config[bstack11l1ll_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨॱ")])
  if proxy == None:
    proxy = Proxy(config[bstack11l1ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩॲ")])
  return proxy
def bstack1lll1ll111_opy_(self):
  global CONFIG
  global bstack1l111l111_opy_
  try:
    proxy = bstack1111l1l11_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11l1ll_opy_ (u"ࠫ࠳ࡶࡡࡤࠩॳ")):
        proxies = bstack1l11ll1l_opy_(proxy, bstack1l1111111_opy_())
        if len(proxies) > 0:
          protocol, bstack1111ll1ll_opy_ = proxies.popitem()
          if bstack11l1ll_opy_ (u"ࠧࡀ࠯࠰ࠤॴ") in bstack1111ll1ll_opy_:
            return bstack1111ll1ll_opy_
          else:
            return bstack11l1ll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢॵ") + bstack1111ll1ll_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11l1ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦॶ").format(str(e)))
  return bstack1l111l111_opy_(self)
def bstack11ll11l1_opy_():
  global CONFIG
  return bstack1ll11ll1l_opy_(CONFIG) and bstack1ll1lllll_opy_() and bstack11l1ll1l1_opy_() >= version.parse(bstack1lllllllll_opy_)
def bstack1ll111l111_opy_():
  global CONFIG
  return (bstack11l1ll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫॷ") in CONFIG or bstack11l1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॸ") in CONFIG) and bstack1lll1ll1ll_opy_()
def bstack1l1l1ll1l_opy_(config):
  bstack1llll111ll_opy_ = {}
  if bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧॹ") in config:
    bstack1llll111ll_opy_ = config[bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॺ")]
  if bstack11l1ll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॻ") in config:
    bstack1llll111ll_opy_ = config[bstack11l1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬॼ")]
  proxy = bstack1111l1l11_opy_(config)
  if proxy:
    if proxy.endswith(bstack11l1ll_opy_ (u"ࠧ࠯ࡲࡤࡧࠬॽ")) and os.path.isfile(proxy):
      bstack1llll111ll_opy_[bstack11l1ll_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫॾ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11l1ll_opy_ (u"ࠩ࠱ࡴࡦࡩࠧॿ")):
        proxies = bstack11ll1lll_opy_(config, bstack1l1111111_opy_())
        if len(proxies) > 0:
          protocol, bstack1111ll1ll_opy_ = proxies.popitem()
          if bstack11l1ll_opy_ (u"ࠥ࠾࠴࠵ࠢঀ") in bstack1111ll1ll_opy_:
            parsed_url = urlparse(bstack1111ll1ll_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11l1ll_opy_ (u"ࠦ࠿࠵࠯ࠣঁ") + bstack1111ll1ll_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1llll111ll_opy_[bstack11l1ll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨং")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1llll111ll_opy_[bstack11l1ll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩঃ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1llll111ll_opy_[bstack11l1ll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ঄")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1llll111ll_opy_[bstack11l1ll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫঅ")] = str(parsed_url.password)
  return bstack1llll111ll_opy_
def bstack1l1ll11lll_opy_(config):
  if bstack11l1ll_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧআ") in config:
    return config[bstack11l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨই")]
  return {}
def bstack1lll1lll11_opy_(caps):
  global bstack1ll111ll1_opy_
  if bstack11l1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬঈ") in caps:
    caps[bstack11l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭উ")][bstack11l1ll_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬঊ")] = True
    if bstack1ll111ll1_opy_:
      caps[bstack11l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨঋ")][bstack11l1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪঌ")] = bstack1ll111ll1_opy_
  else:
    caps[bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧ঍")] = True
    if bstack1ll111ll1_opy_:
      caps[bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ঎")] = bstack1ll111ll1_opy_
def bstack1l1llll11_opy_():
  global CONFIG
  if bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨএ") in CONFIG and bstack1l1lll11l_opy_(CONFIG[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩঐ")]):
    bstack1llll111ll_opy_ = bstack1l1l1ll1l_opy_(CONFIG)
    bstack11ll1111_opy_(CONFIG[bstack11l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ঑")], bstack1llll111ll_opy_)
def bstack11ll1111_opy_(key, bstack1llll111ll_opy_):
  global bstack1ll1l11l11_opy_
  logger.info(bstack1lll111ll_opy_)
  try:
    bstack1ll1l11l11_opy_ = Local()
    bstack1llll11l1_opy_ = {bstack11l1ll_opy_ (u"ࠧ࡬ࡧࡼࠫ঒"): key}
    bstack1llll11l1_opy_.update(bstack1llll111ll_opy_)
    logger.debug(bstack11l11l1ll_opy_.format(str(bstack1llll11l1_opy_)))
    bstack1ll1l11l11_opy_.start(**bstack1llll11l1_opy_)
    if bstack1ll1l11l11_opy_.isRunning():
      logger.info(bstack1lll11111l_opy_)
  except Exception as e:
    bstack1l1ll1ll1l_opy_(bstack1lll11l1l1_opy_.format(str(e)))
def bstack1ll1l111l_opy_():
  global bstack1ll1l11l11_opy_
  if bstack1ll1l11l11_opy_.isRunning():
    logger.info(bstack1llll11ll_opy_)
    bstack1ll1l11l11_opy_.stop()
  bstack1ll1l11l11_opy_ = None
def bstack1l1ll1ll1_opy_(bstack1l1l1l1l1l_opy_=[]):
  global CONFIG
  bstack1lll111l_opy_ = []
  bstack11l11ll11_opy_ = [bstack11l1ll_opy_ (u"ࠨࡱࡶࠫও"), bstack11l1ll_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬঔ"), bstack11l1ll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧক"), bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭খ"), bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪগ"), bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧঘ")]
  try:
    for err in bstack1l1l1l1l1l_opy_:
      bstack1l1ll1l1ll_opy_ = {}
      for k in bstack11l11ll11_opy_:
        val = CONFIG[bstack11l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪঙ")][int(err[bstack11l1ll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧচ")])].get(k)
        if val:
          bstack1l1ll1l1ll_opy_[k] = val
      if(err[bstack11l1ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨছ")] != bstack11l1ll_opy_ (u"ࠪࠫজ")):
        bstack1l1ll1l1ll_opy_[bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪঝ")] = {
          err[bstack11l1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪঞ")]: err[bstack11l1ll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬট")]
        }
        bstack1lll111l_opy_.append(bstack1l1ll1l1ll_opy_)
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩঠ") + str(e))
  finally:
    return bstack1lll111l_opy_
def bstack1ll1lll11_opy_(file_name):
  bstack11lll1ll1_opy_ = []
  try:
    bstack1l1l1l1l1_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1l1l1l1l1_opy_):
      with open(bstack1l1l1l1l1_opy_) as f:
        bstack1l1llll1ll_opy_ = json.load(f)
        bstack11lll1ll1_opy_ = bstack1l1llll1ll_opy_
      os.remove(bstack1l1l1l1l1_opy_)
    return bstack11lll1ll1_opy_
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪড") + str(e))
def bstack111l11ll_opy_():
  global bstack11ll1ll1_opy_
  global bstack1llll11lll_opy_
  global bstack1ll1111l_opy_
  global bstack1ll111111l_opy_
  global bstack111l111ll_opy_
  global bstack1l1l1l1111_opy_
  percy.shutdown()
  bstack1l1lllllll_opy_ = os.environ.get(bstack11l1ll_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪঢ"))
  if bstack1l1lllllll_opy_ in [bstack11l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩণ"), bstack11l1ll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪত")]:
    bstack111111ll1_opy_()
  if bstack11ll1ll1_opy_:
    logger.warning(bstack1111l1l1_opy_.format(str(bstack11ll1ll1_opy_)))
  else:
    try:
      bstack1l1111lll_opy_ = bstack11l11ll1_opy_(bstack11l1ll_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫথ"), logger)
      if bstack1l1111lll_opy_.get(bstack11l1ll_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫদ")) and bstack1l1111lll_opy_.get(bstack11l1ll_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬধ")).get(bstack11l1ll_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪন")):
        logger.warning(bstack1111l1l1_opy_.format(str(bstack1l1111lll_opy_[bstack11l1ll_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ঩")][bstack11l1ll_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬপ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1llll1ll_opy_)
  global bstack1ll1l11l11_opy_
  if bstack1ll1l11l11_opy_:
    bstack1ll1l111l_opy_()
  try:
    for driver in bstack1llll11lll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11llll111_opy_)
  if bstack1l1l1l1111_opy_ == bstack11l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪফ"):
    bstack111l111ll_opy_ = bstack1ll1lll11_opy_(bstack11l1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ব"))
  if bstack1l1l1l1111_opy_ == bstack11l1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ভ") and len(bstack1ll111111l_opy_) == 0:
    bstack1ll111111l_opy_ = bstack1ll1lll11_opy_(bstack11l1ll_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬম"))
    if len(bstack1ll111111l_opy_) == 0:
      bstack1ll111111l_opy_ = bstack1ll1lll11_opy_(bstack11l1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧয"))
  bstack1ll11111l1_opy_ = bstack11l1ll_opy_ (u"ࠩࠪর")
  if len(bstack1ll1111l_opy_) > 0:
    bstack1ll11111l1_opy_ = bstack1l1ll1ll1_opy_(bstack1ll1111l_opy_)
  elif len(bstack1ll111111l_opy_) > 0:
    bstack1ll11111l1_opy_ = bstack1l1ll1ll1_opy_(bstack1ll111111l_opy_)
  elif len(bstack111l111ll_opy_) > 0:
    bstack1ll11111l1_opy_ = bstack1l1ll1ll1_opy_(bstack111l111ll_opy_)
  elif len(bstack1ll1ll1ll_opy_) > 0:
    bstack1ll11111l1_opy_ = bstack1l1ll1ll1_opy_(bstack1ll1ll1ll_opy_)
  if bool(bstack1ll11111l1_opy_):
    bstack1l11l111l_opy_(bstack1ll11111l1_opy_)
  else:
    bstack1l11l111l_opy_()
  bstack111111l1_opy_(bstack1ll1ll111l_opy_, logger)
def bstack1l1l1ll1_opy_(self, *args):
  logger.error(bstack1l1l1llll_opy_)
  bstack111l11ll_opy_()
  sys.exit(1)
def bstack1l1ll1ll1l_opy_(err):
  logger.critical(bstack11llllll1_opy_.format(str(err)))
  bstack1l11l111l_opy_(bstack11llllll1_opy_.format(str(err)), True)
  atexit.unregister(bstack111l11ll_opy_)
  bstack111111ll1_opy_()
  sys.exit(1)
def bstack1l1lll1l11_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l11l111l_opy_(message, True)
  atexit.unregister(bstack111l11ll_opy_)
  bstack111111ll1_opy_()
  sys.exit(1)
def bstack1ll1ll11ll_opy_():
  global CONFIG
  global bstack1lll11ll1l_opy_
  global bstack1llllll1l_opy_
  global bstack11lllll1_opy_
  CONFIG = bstack1ll111ll1l_opy_()
  bstack1l111l1ll_opy_()
  bstack11l1l1ll1_opy_()
  CONFIG = bstack1ll1llll11_opy_(CONFIG)
  update(CONFIG, bstack1llllll1l_opy_)
  update(CONFIG, bstack1lll11ll1l_opy_)
  CONFIG = bstack1l11ll111_opy_(CONFIG)
  bstack11lllll1_opy_ = bstack1l1ll1l1l1_opy_(CONFIG)
  bstack1ll1l11ll1_opy_.bstack11l11l11_opy_(bstack11l1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ঱"), bstack11lllll1_opy_)
  if (bstack11l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧল") in CONFIG and bstack11l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ঳") in bstack1lll11ll1l_opy_) or (
          bstack11l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ঴") in CONFIG and bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ঵") not in bstack1llllll1l_opy_):
    if os.getenv(bstack11l1ll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬশ")):
      CONFIG[bstack11l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫষ")] = os.getenv(bstack11l1ll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧস"))
    else:
      bstack11ll1l1l_opy_()
  elif (bstack11l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧহ") not in CONFIG and bstack11l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ঺") in CONFIG) or (
          bstack11l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ঻") in bstack1llllll1l_opy_ and bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ়ࠪ") not in bstack1lll11ll1l_opy_):
    del (CONFIG[bstack11l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪঽ")])
  if bstack1l1l111lll_opy_(CONFIG):
    bstack1l1ll1ll1l_opy_(bstack1l1l1111l_opy_)
  bstack1lll1l11l1_opy_()
  bstack1l1l1lll_opy_()
  if bstack1l1llllll1_opy_:
    CONFIG[bstack11l1ll_opy_ (u"ࠩࡤࡴࡵ࠭া")] = bstack1l1l1ll111_opy_(CONFIG)
    logger.info(bstack1lll1ll11_opy_.format(CONFIG[bstack11l1ll_opy_ (u"ࠪࡥࡵࡶࠧি")]))
def bstack11l1lll11_opy_(config, bstack11111l11l_opy_):
  global CONFIG
  global bstack1l1llllll1_opy_
  CONFIG = config
  bstack1l1llllll1_opy_ = bstack11111l11l_opy_
def bstack1l1l1lll_opy_():
  global CONFIG
  global bstack1l1llllll1_opy_
  if bstack11l1ll_opy_ (u"ࠫࡦࡶࡰࠨী") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l1lll1l11_opy_(e, bstack11ll11ll_opy_)
    bstack1l1llllll1_opy_ = True
    bstack1ll1l11ll1_opy_.bstack11l11l11_opy_(bstack11l1ll_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫু"), True)
def bstack1l1l1ll111_opy_(config):
  bstack1l1ll11111_opy_ = bstack11l1ll_opy_ (u"࠭ࠧূ")
  app = config[bstack11l1ll_opy_ (u"ࠧࡢࡲࡳࠫৃ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l1l11ll11_opy_:
      if os.path.exists(app):
        bstack1l1ll11111_opy_ = bstack1lll11l11_opy_(config, app)
      elif bstack1l1ll1l1_opy_(app):
        bstack1l1ll11111_opy_ = app
      else:
        bstack1l1ll1ll1l_opy_(bstack1l1111ll_opy_.format(app))
    else:
      if bstack1l1ll1l1_opy_(app):
        bstack1l1ll11111_opy_ = app
      elif os.path.exists(app):
        bstack1l1ll11111_opy_ = bstack1lll11l11_opy_(app)
      else:
        bstack1l1ll1ll1l_opy_(bstack11l1ll11l_opy_)
  else:
    if len(app) > 2:
      bstack1l1ll1ll1l_opy_(bstack1llll11l11_opy_)
    elif len(app) == 2:
      if bstack11l1ll_opy_ (u"ࠨࡲࡤࡸ࡭࠭ৄ") in app and bstack11l1ll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ৅") in app:
        if os.path.exists(app[bstack11l1ll_opy_ (u"ࠪࡴࡦࡺࡨࠨ৆")]):
          bstack1l1ll11111_opy_ = bstack1lll11l11_opy_(config, app[bstack11l1ll_opy_ (u"ࠫࡵࡧࡴࡩࠩে")], app[bstack11l1ll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨৈ")])
        else:
          bstack1l1ll1ll1l_opy_(bstack1l1111ll_opy_.format(app))
      else:
        bstack1l1ll1ll1l_opy_(bstack1llll11l11_opy_)
    else:
      for key in app:
        if key in bstack1l1l1lll1l_opy_:
          if key == bstack11l1ll_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ৉"):
            if os.path.exists(app[key]):
              bstack1l1ll11111_opy_ = bstack1lll11l11_opy_(config, app[key])
            else:
              bstack1l1ll1ll1l_opy_(bstack1l1111ll_opy_.format(app))
          else:
            bstack1l1ll11111_opy_ = app[key]
        else:
          bstack1l1ll1ll1l_opy_(bstack1ll1l111_opy_)
  return bstack1l1ll11111_opy_
def bstack1l1ll1l1_opy_(bstack1l1ll11111_opy_):
  import re
  bstack1ll1ll11_opy_ = re.compile(bstack11l1ll_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢ৊"))
  bstack1l1llll1l1_opy_ = re.compile(bstack11l1ll_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧো"))
  if bstack11l1ll_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨৌ") in bstack1l1ll11111_opy_ or re.fullmatch(bstack1ll1ll11_opy_, bstack1l1ll11111_opy_) or re.fullmatch(bstack1l1llll1l1_opy_, bstack1l1ll11111_opy_):
    return True
  else:
    return False
def bstack1lll11l11_opy_(config, path, bstack1l111l1l1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11l1ll_opy_ (u"ࠪࡶࡧ্࠭")).read()).hexdigest()
  bstack1ll1l1lll1_opy_ = bstack1l11lllll_opy_(md5_hash)
  bstack1l1ll11111_opy_ = None
  if bstack1ll1l1lll1_opy_:
    logger.info(bstack1l111l1l_opy_.format(bstack1ll1l1lll1_opy_, md5_hash))
    return bstack1ll1l1lll1_opy_
  bstack1l11l1ll1_opy_ = MultipartEncoder(
    fields={
      bstack11l1ll_opy_ (u"ࠫ࡫࡯࡬ࡦࠩৎ"): (os.path.basename(path), open(os.path.abspath(path), bstack11l1ll_opy_ (u"ࠬࡸࡢࠨ৏")), bstack11l1ll_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪ৐")),
      bstack11l1ll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ৑"): bstack1l111l1l1_opy_
    }
  )
  response = requests.post(bstack1lllll111_opy_, data=bstack1l11l1ll1_opy_,
                           headers={bstack11l1ll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ৒"): bstack1l11l1ll1_opy_.content_type},
                           auth=(config[bstack11l1ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ৓")], config[bstack11l1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭৔")]))
  try:
    res = json.loads(response.text)
    bstack1l1ll11111_opy_ = res[bstack11l1ll_opy_ (u"ࠫࡦࡶࡰࡠࡷࡵࡰࠬ৕")]
    logger.info(bstack11l111111_opy_.format(bstack1l1ll11111_opy_))
    bstack1111l1ll_opy_(md5_hash, bstack1l1ll11111_opy_)
  except ValueError as err:
    bstack1l1ll1ll1l_opy_(bstack11ll1lll1_opy_.format(str(err)))
  return bstack1l1ll11111_opy_
def bstack1lll1l11l1_opy_():
  global CONFIG
  global bstack11111111l_opy_
  bstack1l1l1l1l_opy_ = 0
  bstack1ll11111_opy_ = 1
  if bstack11l1ll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ৖") in CONFIG:
    bstack1ll11111_opy_ = CONFIG[bstack11l1ll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ৗ")]
  if bstack11l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৘") in CONFIG:
    bstack1l1l1l1l_opy_ = len(CONFIG[bstack11l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ৙")])
  bstack11111111l_opy_ = int(bstack1ll11111_opy_) * int(bstack1l1l1l1l_opy_)
def bstack1l11lllll_opy_(md5_hash):
  bstack1lll111l1_opy_ = os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠩࢁࠫ৚")), bstack11l1ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ৛"), bstack11l1ll_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬড়"))
  if os.path.exists(bstack1lll111l1_opy_):
    bstack1lll1llll1_opy_ = json.load(open(bstack1lll111l1_opy_, bstack11l1ll_opy_ (u"ࠬࡸࡢࠨঢ়")))
    if md5_hash in bstack1lll1llll1_opy_:
      bstack11l111l11_opy_ = bstack1lll1llll1_opy_[md5_hash]
      bstack1llll1ll11_opy_ = datetime.datetime.now()
      bstack1l111l11_opy_ = datetime.datetime.strptime(bstack11l111l11_opy_[bstack11l1ll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ৞")], bstack11l1ll_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫয়"))
      if (bstack1llll1ll11_opy_ - bstack1l111l11_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack11l111l11_opy_[bstack11l1ll_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ৠ")]):
        return None
      return bstack11l111l11_opy_[bstack11l1ll_opy_ (u"ࠩ࡬ࡨࠬৡ")]
  else:
    return None
def bstack1111l1ll_opy_(md5_hash, bstack1l1ll11111_opy_):
  bstack1lll1lll1l_opy_ = os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠪࢂࠬৢ")), bstack11l1ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫৣ"))
  if not os.path.exists(bstack1lll1lll1l_opy_):
    os.makedirs(bstack1lll1lll1l_opy_)
  bstack1lll111l1_opy_ = os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠬࢄࠧ৤")), bstack11l1ll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭৥"), bstack11l1ll_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ০"))
  bstack11lll11ll_opy_ = {
    bstack11l1ll_opy_ (u"ࠨ࡫ࡧࠫ১"): bstack1l1ll11111_opy_,
    bstack11l1ll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ২"): datetime.datetime.strftime(datetime.datetime.now(), bstack11l1ll_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧ৩")),
    bstack11l1ll_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ৪"): str(__version__)
  }
  if os.path.exists(bstack1lll111l1_opy_):
    bstack1lll1llll1_opy_ = json.load(open(bstack1lll111l1_opy_, bstack11l1ll_opy_ (u"ࠬࡸࡢࠨ৫")))
  else:
    bstack1lll1llll1_opy_ = {}
  bstack1lll1llll1_opy_[md5_hash] = bstack11lll11ll_opy_
  with open(bstack1lll111l1_opy_, bstack11l1ll_opy_ (u"ࠨࡷࠬࠤ৬")) as outfile:
    json.dump(bstack1lll1llll1_opy_, outfile)
def bstack111llll1_opy_(self):
  return
def bstack1lll1lllll_opy_(self):
  return
def bstack1ll111l1ll_opy_(self):
  global bstack11111lll1_opy_
  bstack11111lll1_opy_(self)
def bstack1l1l11l111_opy_():
  global bstack11l1l111_opy_
  bstack11l1l111_opy_ = True
def bstack1ll1llll1_opy_(self):
  global bstack1ll11llll1_opy_
  global bstack1l111l11l_opy_
  global bstack1l11111ll_opy_
  try:
    if bstack11l1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ৭") in bstack1ll11llll1_opy_ and self.session_id != None and bstack111l1lll_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬ৮"), bstack11l1ll_opy_ (u"ࠩࠪ৯")) != bstack11l1ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫৰ"):
      bstack1lllllll1l_opy_ = bstack11l1ll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫৱ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ৲")
      if bstack1lllllll1l_opy_ == bstack11l1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭৳"):
        bstack11llll11l_opy_(logger)
      if self != None:
        bstack1l1ll1llll_opy_(self, bstack1lllllll1l_opy_, bstack11l1ll_opy_ (u"ࠧ࠭ࠢࠪ৴").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack11l1ll_opy_ (u"ࠨࠩ৵")
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࠥ৶") + str(e))
  bstack1l11111ll_opy_(self)
  self.session_id = None
def bstack111l1ll1l_opy_(self, command_executor=bstack11l1ll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲࠵࠷࠽࠮࠱࠰࠳࠲࠶ࡀ࠴࠵࠶࠷ࠦ৷"), *args, **kwargs):
  bstack1ll1l1l1ll_opy_ = bstack111l1l1ll_opy_(self, command_executor, *args, **kwargs)
  try:
    logger.debug(bstack11l1ll_opy_ (u"ࠫࡈࡵ࡭࡮ࡣࡱࡨࠥࡋࡸࡦࡥࡸࡸࡴࡸࠠࡸࡪࡨࡲࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤ࡫ࡧ࡬ࡴࡧࠣ࠱ࠥࢁࡽࠨ৸").format(str(command_executor)))
    logger.debug(bstack11l1ll_opy_ (u"ࠬࡎࡵࡣࠢࡘࡖࡑࠦࡩࡴࠢ࠰ࠤࢀࢃࠧ৹").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ৺") in command_executor._url:
      bstack1ll1l11ll1_opy_.bstack11l11l11_opy_(bstack11l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ৻"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫৼ") in command_executor):
    bstack1ll1l11ll1_opy_.bstack11l11l11_opy_(bstack11l1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪ৽"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l11l1111_opy_.bstack1lll1111l_opy_(self)
  return bstack1ll1l1l1ll_opy_
def bstack11llll1l1_opy_(self, driver_command, *args, **kwargs):
  global bstack1111l11l_opy_
  response = bstack1111l11l_opy_(self, driver_command, *args, **kwargs)
  try:
    if driver_command == bstack11l1ll_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧ৾"):
      bstack1l11l1111_opy_.bstack1l11l1l11_opy_({
          bstack11l1ll_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ৿"): response[bstack11l1ll_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ਀")],
          bstack11l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ਁ"): bstack1l11l1111_opy_.current_test_uuid() if bstack1l11l1111_opy_.current_test_uuid() else bstack1l11l1111_opy_.current_hook_uuid()
      })
  except:
    pass
  return response
def bstack1ll1l1l11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1l111l11l_opy_
  global bstack11lll1l1l_opy_
  global bstack111l11l11_opy_
  global bstack11lllllll_opy_
  global bstack1l1l1l111_opy_
  global bstack1ll11llll1_opy_
  global bstack111l1l1ll_opy_
  global bstack1llll11lll_opy_
  global bstack11111l11_opy_
  global bstack1l1111l1_opy_
  CONFIG[bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩਂ")] = str(bstack1ll11llll1_opy_) + str(__version__)
  command_executor = bstack1l1111111_opy_()
  logger.debug(bstack111l1111l_opy_.format(command_executor))
  proxy = bstack1llll11l1l_opy_(CONFIG, proxy)
  bstack1l1ll1ll_opy_ = 0 if bstack11lll1l1l_opy_ < 0 else bstack11lll1l1l_opy_
  try:
    if bstack11lllllll_opy_ is True:
      bstack1l1ll1ll_opy_ = int(multiprocessing.current_process().name)
    elif bstack1l1l1l111_opy_ is True:
      bstack1l1ll1ll_opy_ = int(threading.current_thread().name)
  except:
    bstack1l1ll1ll_opy_ = 0
  bstack1ll111ll_opy_ = bstack1l1ll11l11_opy_(CONFIG, bstack1l1ll1ll_opy_)
  logger.debug(bstack1l1l11lll1_opy_.format(str(bstack1ll111ll_opy_)))
  if bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬਃ") in CONFIG and bstack1l1lll11l_opy_(CONFIG[bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭਄")]):
    bstack1lll1lll11_opy_(bstack1ll111ll_opy_)
  if desired_capabilities:
    bstack1ll11l11l1_opy_ = bstack1ll1llll11_opy_(desired_capabilities)
    bstack1ll11l11l1_opy_[bstack11l1ll_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪਅ")] = bstack1ll1111lll_opy_(CONFIG)
    bstack1l111lll_opy_ = bstack1l1ll11l11_opy_(bstack1ll11l11l1_opy_)
    if bstack1l111lll_opy_:
      bstack1ll111ll_opy_ = update(bstack1l111lll_opy_, bstack1ll111ll_opy_)
    desired_capabilities = None
  if options:
    bstack1ll11ll11l_opy_(options, bstack1ll111ll_opy_)
  if not options:
    options = bstack1l1ll11l1_opy_(bstack1ll111ll_opy_)
  bstack1l1111l1_opy_ = CONFIG.get(bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਆ"))[bstack1l1ll1ll_opy_]
  if bstack11ll11ll1_opy_.bstack1lll111l1l_opy_(CONFIG, bstack1l1ll1ll_opy_) and bstack11ll11ll1_opy_.bstack1llll1l1l1_opy_(bstack1ll111ll_opy_, options):
    threading.current_thread().a11yPlatform = True
    bstack11ll11ll1_opy_.set_capabilities(bstack1ll111ll_opy_, CONFIG)
  if proxy and bstack11l1ll1l1_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬਇ")):
    options.proxy(proxy)
  if options and bstack11l1ll1l1_opy_() >= version.parse(bstack11l1ll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬਈ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack11l1ll1l1_opy_() < version.parse(bstack11l1ll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ਉ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1ll111ll_opy_)
  logger.info(bstack1l1lll111l_opy_)
  if bstack11l1ll1l1_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨਊ")):
    bstack111l1l1ll_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11l1ll1l1_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ਋")):
    bstack111l1l1ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11l1ll1l1_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪ਌")):
    bstack111l1l1ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack111l1l1ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack1l1l11l1l_opy_ = bstack11l1ll_opy_ (u"ࠫࠬ਍")
    if bstack11l1ll1l1_opy_() >= version.parse(bstack11l1ll_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭਎")):
      bstack1l1l11l1l_opy_ = self.caps.get(bstack11l1ll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨਏ"))
    else:
      bstack1l1l11l1l_opy_ = self.capabilities.get(bstack11l1ll_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢਐ"))
    if bstack1l1l11l1l_opy_:
      bstack11l11ll1l_opy_(bstack1l1l11l1l_opy_)
      if bstack11l1ll1l1_opy_() <= version.parse(bstack11l1ll_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ਑")):
        self.command_executor._url = bstack11l1ll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ਒") + bstack1llll1111_opy_ + bstack11l1ll_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢਓ")
      else:
        self.command_executor._url = bstack11l1ll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨਔ") + bstack1l1l11l1l_opy_ + bstack11l1ll_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨਕ")
      logger.debug(bstack11ll111l_opy_.format(bstack1l1l11l1l_opy_))
    else:
      logger.debug(bstack1ll1ll1ll1_opy_.format(bstack11l1ll_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢਖ")))
  except Exception as e:
    logger.debug(bstack1ll1ll1ll1_opy_.format(e))
  if bstack11l1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ਗ") in bstack1ll11llll1_opy_:
    bstack11l11111l_opy_(bstack11lll1l1l_opy_, bstack11111l11_opy_)
  bstack1l111l11l_opy_ = self.session_id
  if bstack11l1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਘ") in bstack1ll11llll1_opy_ or bstack11l1ll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩਙ") in bstack1ll11llll1_opy_ or bstack11l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩਚ") in bstack1ll11llll1_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1l11l1111_opy_.bstack1lll1111l_opy_(self)
  bstack1llll11lll_opy_.append(self)
  if bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਛ") in CONFIG and bstack11l1ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪਜ") in CONFIG[bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਝ")][bstack1l1ll1ll_opy_]:
    bstack111l11l11_opy_ = CONFIG[bstack11l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪਞ")][bstack1l1ll1ll_opy_][bstack11l1ll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ਟ")]
  logger.debug(bstack1l1l1ll1ll_opy_.format(bstack1l111l11l_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1lll11l111_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1ll1ll11l1_opy_
      if(bstack11l1ll_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸ࠯࡬ࡶࠦਠ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠪࢂࠬਡ")), bstack11l1ll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫਢ"), bstack11l1ll_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧਣ")), bstack11l1ll_opy_ (u"࠭ࡷࠨਤ")) as fp:
          fp.write(bstack11l1ll_opy_ (u"ࠢࠣਥ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11l1ll_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥਦ")))):
          with open(args[1], bstack11l1ll_opy_ (u"ࠩࡵࠫਧ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11l1ll_opy_ (u"ࠪࡥࡸࡿ࡮ࡤࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡤࡴࡥࡸࡒࡤ࡫ࡪ࠮ࡣࡰࡰࡷࡩࡽࡺࠬࠡࡲࡤ࡫ࡪࠦ࠽ࠡࡸࡲ࡭ࡩࠦ࠰ࠪࠩਨ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1ll11lll_opy_)
            lines.insert(1, bstack1l1ll1111l_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11l1ll_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ਩")), bstack11l1ll_opy_ (u"ࠬࡽࠧਪ")) as bstack1ll11111l_opy_:
              bstack1ll11111l_opy_.writelines(lines)
        CONFIG[bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨਫ")] = str(bstack1ll11llll1_opy_) + str(__version__)
        bstack1l1ll1ll_opy_ = 0 if bstack11lll1l1l_opy_ < 0 else bstack11lll1l1l_opy_
        try:
          if bstack11lllllll_opy_ is True:
            bstack1l1ll1ll_opy_ = int(multiprocessing.current_process().name)
          elif bstack1l1l1l111_opy_ is True:
            bstack1l1ll1ll_opy_ = int(threading.current_thread().name)
        except:
          bstack1l1ll1ll_opy_ = 0
        CONFIG[bstack11l1ll_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢਬ")] = False
        CONFIG[bstack11l1ll_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢਭ")] = True
        bstack1ll111ll_opy_ = bstack1l1ll11l11_opy_(CONFIG, bstack1l1ll1ll_opy_)
        logger.debug(bstack1l1l11lll1_opy_.format(str(bstack1ll111ll_opy_)))
        if CONFIG.get(bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ਮ")):
          bstack1lll1lll11_opy_(bstack1ll111ll_opy_)
        if bstack11l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਯ") in CONFIG and bstack11l1ll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩਰ") in CONFIG[bstack11l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ਱")][bstack1l1ll1ll_opy_]:
          bstack111l11l11_opy_ = CONFIG[bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਲ")][bstack1l1ll1ll_opy_][bstack11l1ll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬਲ਼")]
        args.append(os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠨࢀࠪ਴")), bstack11l1ll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩਵ"), bstack11l1ll_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬਸ਼")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1ll111ll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11l1ll_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ਷"))
      bstack1ll1ll11l1_opy_ = True
      return bstack1l1ll1l1l_opy_(self, args, bufsize=bufsize, executable=executable,
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
  def bstack1l1l1lll11_opy_(self,
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
    global bstack11lll1l1l_opy_
    global bstack111l11l11_opy_
    global bstack11lllllll_opy_
    global bstack1l1l1l111_opy_
    global bstack1ll11llll1_opy_
    CONFIG[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧਸ")] = str(bstack1ll11llll1_opy_) + str(__version__)
    bstack1l1ll1ll_opy_ = 0 if bstack11lll1l1l_opy_ < 0 else bstack11lll1l1l_opy_
    try:
      if bstack11lllllll_opy_ is True:
        bstack1l1ll1ll_opy_ = int(multiprocessing.current_process().name)
      elif bstack1l1l1l111_opy_ is True:
        bstack1l1ll1ll_opy_ = int(threading.current_thread().name)
    except:
      bstack1l1ll1ll_opy_ = 0
    CONFIG[bstack11l1ll_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧਹ")] = True
    bstack1ll111ll_opy_ = bstack1l1ll11l11_opy_(CONFIG, bstack1l1ll1ll_opy_)
    logger.debug(bstack1l1l11lll1_opy_.format(str(bstack1ll111ll_opy_)))
    if CONFIG.get(bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ਺")):
      bstack1lll1lll11_opy_(bstack1ll111ll_opy_)
    if bstack11l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ਻") in CONFIG and bstack11l1ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫਼ࠧ") in CONFIG[bstack11l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭਽")][bstack1l1ll1ll_opy_]:
      bstack111l11l11_opy_ = CONFIG[bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਾ")][bstack1l1ll1ll_opy_][bstack11l1ll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪਿ")]
    import urllib
    import json
    bstack1l1l111ll_opy_ = bstack11l1ll_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨੀ") + urllib.parse.quote(json.dumps(bstack1ll111ll_opy_))
    browser = self.connect(bstack1l1l111ll_opy_)
    return browser
except Exception as e:
    pass
def bstack1ll11l11_opy_():
    global bstack1ll1ll11l1_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1l1l1lll11_opy_
        bstack1ll1ll11l1_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1lll11l111_opy_
      bstack1ll1ll11l1_opy_ = True
    except Exception as e:
      pass
def bstack1ll11ll11_opy_(context, bstack11ll1ll1l_opy_):
  try:
    context.page.evaluate(bstack11l1ll_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣੁ"), bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬੂ")+ json.dumps(bstack11ll1ll1l_opy_) + bstack11l1ll_opy_ (u"ࠤࢀࢁࠧ੃"))
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣ੄"), e)
def bstack11lll1ll_opy_(context, message, level):
  try:
    context.page.evaluate(bstack11l1ll_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧ੅"), bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ੆") + json.dumps(message) + bstack11l1ll_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩੇ") + json.dumps(level) + bstack11l1ll_opy_ (u"ࠧࡾࡿࠪੈ"))
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦ੉"), e)
def bstack111ll11ll_opy_(self, url):
  global bstack1l11l111_opy_
  try:
    bstack1ll11l1lll_opy_(url)
  except Exception as err:
    logger.debug(bstack11l1l1l1_opy_.format(str(err)))
  try:
    bstack1l11l111_opy_(self, url)
  except Exception as e:
    try:
      bstack1ll1l11l_opy_ = str(e)
      if any(err_msg in bstack1ll1l11l_opy_ for err_msg in bstack1111lll1l_opy_):
        bstack1ll11l1lll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack11l1l1l1_opy_.format(str(err)))
    raise e
def bstack1lll11lll_opy_(self):
  global bstack1l111ll11_opy_
  bstack1l111ll11_opy_ = self
  return
def bstack1l111llll_opy_(self):
  global bstack1lllll11ll_opy_
  bstack1lllll11ll_opy_ = self
  return
def bstack1llll1lll1_opy_(self, test):
  global CONFIG
  global bstack1l1lll1l_opy_
  if CONFIG.get(bstack11l1ll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ੊"), False):
    test_name = str(test.data)
    bstack1l1llll1l_opy_ = str(test.source)
    bstack1l11l1ll_opy_ = os.path.relpath(bstack1l1llll1l_opy_, start=os.getcwd())
    suite_name, bstack1l11lll11_opy_ = os.path.splitext(bstack1l11l1ll_opy_)
    bstack1llll1lll_opy_ = suite_name + bstack11l1ll_opy_ (u"ࠥ࠱ࠧੋ") + test_name
    threading.current_thread().percySessionName = bstack1llll1lll_opy_
  bstack1l1lll1l_opy_(self, test)
def bstack1111ll1l1_opy_(self, test):
  global CONFIG
  global bstack1lllll11ll_opy_
  global bstack1l111ll11_opy_
  global bstack1l111l11l_opy_
  global bstack1llllllll_opy_
  global bstack111l11l11_opy_
  global bstack111111111_opy_
  global bstack1l11l11ll_opy_
  global bstack11111l1l1_opy_
  global bstack1lll1111l1_opy_
  global bstack1llll11lll_opy_
  global bstack1l1111l1_opy_
  try:
    if not bstack1l111l11l_opy_:
      with open(os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"ࠫࢃ࠭ੌ")), bstack11l1ll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯੍ࠬ"), bstack11l1ll_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ੎"))) as f:
        bstack1ll1l11l1_opy_ = json.loads(bstack11l1ll_opy_ (u"ࠢࡼࠤ੏") + f.read().strip() + bstack11l1ll_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤࠪ੐") + bstack11l1ll_opy_ (u"ࠤࢀࠦੑ"))
        bstack1l111l11l_opy_ = bstack1ll1l11l1_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1llll11lll_opy_:
    for driver in bstack1llll11lll_opy_:
      if bstack1l111l11l_opy_ == driver.session_id:
        if test:
          bstack1llll1lll_opy_ = str(test.data)
          if CONFIG.get(bstack11l1ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ੒"), False):
            if percy.bstack1l111111l_opy_() == bstack11l1ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ੓"):
              bstack1lll1lll1_opy_ = bstack111l1lll_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ੔"), None)
              bstack111l11l1_opy_(driver, bstack1lll1lll1_opy_)
          if bstack111l1lll_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ੕"), None) and bstack111l1lll_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭੖"), None):
            logger.info(bstack11l1ll_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠦࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡺࡴࡤࡦࡴࡺࡥࡾ࠴ࠠࠣ੗"))
            bstack11ll11ll1_opy_.bstack111111l11_opy_(driver, class_name=test.parent.name, name=test.name, module_name=None, path=test.source, bstack111l11ll1_opy_=bstack1l1111l1_opy_)
        if not bstack1111111l_opy_ and bstack1llll1lll_opy_:
          bstack11ll1l1l1_opy_ = {
            bstack11l1ll_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ੘"): bstack11l1ll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫਖ਼"),
            bstack11l1ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧਗ਼"): {
              bstack11l1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪਜ਼"): bstack1llll1lll_opy_
            }
          }
          bstack1l1l1lll1_opy_ = bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫੜ").format(json.dumps(bstack11ll1l1l1_opy_))
          driver.execute_script(bstack1l1l1lll1_opy_)
        if bstack1llllllll_opy_:
          bstack11ll111l1_opy_ = {
            bstack11l1ll_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ੝"): bstack11l1ll_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪਫ਼"),
            bstack11l1ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ੟"): {
              bstack11l1ll_opy_ (u"ࠪࡨࡦࡺࡡࠨ੠"): bstack1llll1lll_opy_ + bstack11l1ll_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭੡"),
              bstack11l1ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ੢"): bstack11l1ll_opy_ (u"࠭ࡩ࡯ࡨࡲࠫ੣")
            }
          }
          if bstack1llllllll_opy_.status == bstack11l1ll_opy_ (u"ࠧࡑࡃࡖࡗࠬ੤"):
            bstack1ll1l111l1_opy_ = bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭੥").format(json.dumps(bstack11ll111l1_opy_))
            driver.execute_script(bstack1ll1l111l1_opy_)
            bstack1l1ll1llll_opy_(driver, bstack11l1ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ੦"))
          elif bstack1llllllll_opy_.status == bstack11l1ll_opy_ (u"ࠪࡊࡆࡏࡌࠨ੧"):
            reason = bstack11l1ll_opy_ (u"ࠦࠧ੨")
            bstack1ll111l11l_opy_ = bstack1llll1lll_opy_ + bstack11l1ll_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩ࠭੩")
            if bstack1llllllll_opy_.message:
              reason = str(bstack1llllllll_opy_.message)
              bstack1ll111l11l_opy_ = bstack1ll111l11l_opy_ + bstack11l1ll_opy_ (u"࠭ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥ࠭੪") + reason
            bstack11ll111l1_opy_[bstack11l1ll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ੫")] = {
              bstack11l1ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ੬"): bstack11l1ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ੭"),
              bstack11l1ll_opy_ (u"ࠪࡨࡦࡺࡡࠨ੮"): bstack1ll111l11l_opy_
            }
            bstack1ll1l111l1_opy_ = bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ੯").format(json.dumps(bstack11ll111l1_opy_))
            driver.execute_script(bstack1ll1l111l1_opy_)
            bstack1l1ll1llll_opy_(driver, bstack11l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬੰ"), reason)
            bstack1ll11ll1_opy_(reason, str(bstack1llllllll_opy_), str(bstack11lll1l1l_opy_), logger)
  elif bstack1l111l11l_opy_:
    try:
      data = {}
      bstack1llll1lll_opy_ = None
      if test:
        bstack1llll1lll_opy_ = str(test.data)
      if not bstack1111111l_opy_ and bstack1llll1lll_opy_:
        data[bstack11l1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫੱ")] = bstack1llll1lll_opy_
      if bstack1llllllll_opy_:
        if bstack1llllllll_opy_.status == bstack11l1ll_opy_ (u"ࠧࡑࡃࡖࡗࠬੲ"):
          data[bstack11l1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨੳ")] = bstack11l1ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩੴ")
        elif bstack1llllllll_opy_.status == bstack11l1ll_opy_ (u"ࠪࡊࡆࡏࡌࠨੵ"):
          data[bstack11l1ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ੶")] = bstack11l1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ੷")
          if bstack1llllllll_opy_.message:
            data[bstack11l1ll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭੸")] = str(bstack1llllllll_opy_.message)
      user = CONFIG[bstack11l1ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ੹")]
      key = CONFIG[bstack11l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ੺")]
      url = bstack11l1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧ੻").format(user, key, bstack1l111l11l_opy_)
      headers = {
        bstack11l1ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ੼"): bstack11l1ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ੽"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1ll11ll111_opy_.format(str(e)))
  if bstack1lllll11ll_opy_:
    bstack1l11l11ll_opy_(bstack1lllll11ll_opy_)
  if bstack1l111ll11_opy_:
    bstack11111l1l1_opy_(bstack1l111ll11_opy_)
  if bstack11l1l111_opy_:
    bstack1lll1111l1_opy_()
  bstack111111111_opy_(self, test)
def bstack1lllll1ll1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11lll1lll_opy_
  global CONFIG
  global bstack1llll11lll_opy_
  global bstack1l111l11l_opy_
  bstack11llll1l_opy_ = None
  try:
    if bstack111l1lll_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ੾"), None):
      try:
        if not bstack1l111l11l_opy_:
          with open(os.path.join(os.path.expanduser(bstack11l1ll_opy_ (u"࠭ࡾࠨ੿")), bstack11l1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ઀"), bstack11l1ll_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪઁ"))) as f:
            bstack1ll1l11l1_opy_ = json.loads(bstack11l1ll_opy_ (u"ࠤࡾࠦં") + f.read().strip() + bstack11l1ll_opy_ (u"ࠪࠦࡽࠨ࠺ࠡࠤࡼࠦࠬઃ") + bstack11l1ll_opy_ (u"ࠦࢂࠨ઄"))
            bstack1l111l11l_opy_ = bstack1ll1l11l1_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1llll11lll_opy_:
        for driver in bstack1llll11lll_opy_:
          if bstack1l111l11l_opy_ == driver.session_id:
            bstack11llll1l_opy_ = driver
    bstack1l1ll11ll_opy_ = bstack11ll11ll1_opy_.bstack1ll1ll1lll_opy_(CONFIG, test.tags)
    if bstack11llll1l_opy_:
      threading.current_thread().isA11yTest = bstack11ll11ll1_opy_.bstack11l1l11ll_opy_(bstack11llll1l_opy_, bstack1l1ll11ll_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1l1ll11ll_opy_
  except:
    pass
  bstack11lll1lll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1llllllll_opy_
  bstack1llllllll_opy_ = self._test
def bstack1l1l1ll11l_opy_():
  global bstack1l1l11l1l1_opy_
  try:
    if os.path.exists(bstack1l1l11l1l1_opy_):
      os.remove(bstack1l1l11l1l1_opy_)
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨઅ") + str(e))
def bstack1l1llllll_opy_():
  global bstack1l1l11l1l1_opy_
  bstack1l1111lll_opy_ = {}
  try:
    if not os.path.isfile(bstack1l1l11l1l1_opy_):
      with open(bstack1l1l11l1l1_opy_, bstack11l1ll_opy_ (u"࠭ࡷࠨઆ")):
        pass
      with open(bstack1l1l11l1l1_opy_, bstack11l1ll_opy_ (u"ࠢࡸ࠭ࠥઇ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1l1l11l1l1_opy_):
      bstack1l1111lll_opy_ = json.load(open(bstack1l1l11l1l1_opy_, bstack11l1ll_opy_ (u"ࠨࡴࡥࠫઈ")))
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡷ࡫ࡡࡥ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫઉ") + str(e))
  finally:
    return bstack1l1111lll_opy_
def bstack11l11111l_opy_(platform_index, item_index):
  global bstack1l1l11l1l1_opy_
  try:
    bstack1l1111lll_opy_ = bstack1l1llllll_opy_()
    bstack1l1111lll_opy_[item_index] = platform_index
    with open(bstack1l1l11l1l1_opy_, bstack11l1ll_opy_ (u"ࠥࡻ࠰ࠨઊ")) as outfile:
      json.dump(bstack1l1111lll_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡷࡳ࡫ࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩઋ") + str(e))
def bstack11111ll1l_opy_(bstack11l11lll1_opy_):
  global CONFIG
  bstack1l1l111ll1_opy_ = bstack11l1ll_opy_ (u"ࠬ࠭ઌ")
  if not bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩઍ") in CONFIG:
    logger.info(bstack11l1ll_opy_ (u"ࠧࡏࡱࠣࡴࡱࡧࡴࡧࡱࡵࡱࡸࠦࡰࡢࡵࡶࡩࡩࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡳ࡫ࡲࡢࡶࡨࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫ࡵࡲࠡࡔࡲࡦࡴࡺࠠࡳࡷࡱࠫ઎"))
  try:
    platform = CONFIG[bstack11l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫએ")][bstack11l11lll1_opy_]
    if bstack11l1ll_opy_ (u"ࠩࡲࡷࠬઐ") in platform:
      bstack1l1l111ll1_opy_ += str(platform[bstack11l1ll_opy_ (u"ࠪࡳࡸ࠭ઑ")]) + bstack11l1ll_opy_ (u"ࠫ࠱ࠦࠧ઒")
    if bstack11l1ll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨઓ") in platform:
      bstack1l1l111ll1_opy_ += str(platform[bstack11l1ll_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩઔ")]) + bstack11l1ll_opy_ (u"ࠧ࠭ࠢࠪક")
    if bstack11l1ll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬખ") in platform:
      bstack1l1l111ll1_opy_ += str(platform[bstack11l1ll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ગ")]) + bstack11l1ll_opy_ (u"ࠪ࠰ࠥ࠭ઘ")
    if bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ઙ") in platform:
      bstack1l1l111ll1_opy_ += str(platform[bstack11l1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧચ")]) + bstack11l1ll_opy_ (u"࠭ࠬࠡࠩછ")
    if bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬજ") in platform:
      bstack1l1l111ll1_opy_ += str(platform[bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ઝ")]) + bstack11l1ll_opy_ (u"ࠩ࠯ࠤࠬઞ")
    if bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫટ") in platform:
      bstack1l1l111ll1_opy_ += str(platform[bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬઠ")]) + bstack11l1ll_opy_ (u"ࠬ࠲ࠠࠨડ")
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"࠭ࡓࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡰࡨࡶࡦࡺࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡹࡴࡳ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡵࡩࡵࡵࡲࡵࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡳࡳ࠭ઢ") + str(e))
  finally:
    if bstack1l1l111ll1_opy_[len(bstack1l1l111ll1_opy_) - 2:] == bstack11l1ll_opy_ (u"ࠧ࠭ࠢࠪણ"):
      bstack1l1l111ll1_opy_ = bstack1l1l111ll1_opy_[:-2]
    return bstack1l1l111ll1_opy_
def bstack1111l1lll_opy_(path, bstack1l1l111ll1_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l111lll1_opy_ = ET.parse(path)
    bstack111111l1l_opy_ = bstack1l111lll1_opy_.getroot()
    bstack11l111l1l_opy_ = None
    for suite in bstack111111l1l_opy_.iter(bstack11l1ll_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧત")):
      if bstack11l1ll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩથ") in suite.attrib:
        suite.attrib[bstack11l1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨદ")] += bstack11l1ll_opy_ (u"ࠫࠥ࠭ધ") + bstack1l1l111ll1_opy_
        bstack11l111l1l_opy_ = suite
    bstack1ll1l11l1l_opy_ = None
    for robot in bstack111111l1l_opy_.iter(bstack11l1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫન")):
      bstack1ll1l11l1l_opy_ = robot
    bstack11l1llll1_opy_ = len(bstack1ll1l11l1l_opy_.findall(bstack11l1ll_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬ઩")))
    if bstack11l1llll1_opy_ == 1:
      bstack1ll1l11l1l_opy_.remove(bstack1ll1l11l1l_opy_.findall(bstack11l1ll_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭પ"))[0])
      bstack1l1lll11ll_opy_ = ET.Element(bstack11l1ll_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧફ"), attrib={bstack11l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧબ"): bstack11l1ll_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࡵࠪભ"), bstack11l1ll_opy_ (u"ࠫ࡮ࡪࠧમ"): bstack11l1ll_opy_ (u"ࠬࡹ࠰ࠨય")})
      bstack1ll1l11l1l_opy_.insert(1, bstack1l1lll11ll_opy_)
      bstack1ll11lll1l_opy_ = None
      for suite in bstack1ll1l11l1l_opy_.iter(bstack11l1ll_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬર")):
        bstack1ll11lll1l_opy_ = suite
      bstack1ll11lll1l_opy_.append(bstack11l111l1l_opy_)
      bstack1ll1111ll_opy_ = None
      for status in bstack11l111l1l_opy_.iter(bstack11l1ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ઱")):
        bstack1ll1111ll_opy_ = status
      bstack1ll11lll1l_opy_.append(bstack1ll1111ll_opy_)
    bstack1l111lll1_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡦࡸࡳࡪࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹ࠭લ") + str(e))
def bstack1ll11lllll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1ll1l111ll_opy_
  global CONFIG
  if bstack11l1ll_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨળ") in options:
    del options[bstack11l1ll_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢ઴")]
  bstack1l1l1ll1l1_opy_ = bstack1l1llllll_opy_()
  for bstack11111ll11_opy_ in bstack1l1l1ll1l1_opy_.keys():
    path = os.path.join(os.getcwd(), bstack11l1ll_opy_ (u"ࠫࡵࡧࡢࡰࡶࡢࡶࡪࡹࡵ࡭ࡶࡶࠫવ"), str(bstack11111ll11_opy_), bstack11l1ll_opy_ (u"ࠬࡵࡵࡵࡲࡸࡸ࠳ࡾ࡭࡭ࠩશ"))
    bstack1111l1lll_opy_(path, bstack11111ll1l_opy_(bstack1l1l1ll1l1_opy_[bstack11111ll11_opy_]))
  bstack1l1l1ll11l_opy_()
  return bstack1ll1l111ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1111111ll_opy_(self, ff_profile_dir):
  global bstack1111lllll_opy_
  if not ff_profile_dir:
    return None
  return bstack1111lllll_opy_(self, ff_profile_dir)
def bstack1ll11l1l1l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1ll111ll1_opy_
  bstack11l111ll1_opy_ = []
  if bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩષ") in CONFIG:
    bstack11l111ll1_opy_ = CONFIG[bstack11l1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪસ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11l1ll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤહ")],
      pabot_args[bstack11l1ll_opy_ (u"ࠤࡹࡩࡷࡨ࡯ࡴࡧࠥ઺")],
      argfile,
      pabot_args.get(bstack11l1ll_opy_ (u"ࠥ࡬࡮ࡼࡥࠣ઻")),
      pabot_args[bstack11l1ll_opy_ (u"ࠦࡵࡸ࡯ࡤࡧࡶࡷࡪࡹ઼ࠢ")],
      platform[0],
      bstack1ll111ll1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11l1ll_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡦࡪ࡮ࡨࡷࠧઽ")] or [(bstack11l1ll_opy_ (u"ࠨࠢા"), None)]
    for platform in enumerate(bstack11l111ll1_opy_)
  ]
def bstack1ll1l1111l_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1llll1111l_opy_=bstack11l1ll_opy_ (u"ࠧࠨિ")):
  global bstack1ll1llll_opy_
  self.platform_index = platform_index
  self.bstack1l1ll111l_opy_ = bstack1llll1111l_opy_
  bstack1ll1llll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1ll1ll1111_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack111l1llll_opy_
  global bstack1l11lll1_opy_
  if not bstack11l1ll_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪી") in item.options:
    item.options[bstack11l1ll_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫુ")] = []
  for v in item.options[bstack11l1ll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬૂ")]:
    if bstack11l1ll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪૃ") in v:
      item.options[bstack11l1ll_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧૄ")].remove(v)
    if bstack11l1ll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭ૅ") in v:
      item.options[bstack11l1ll_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ૆")].remove(v)
  item.options[bstack11l1ll_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪે")].insert(0, bstack11l1ll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘ࠻ࡽࢀࠫૈ").format(item.platform_index))
  item.options[bstack11l1ll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬૉ")].insert(0, bstack11l1ll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫ૊").format(item.bstack1l1ll111l_opy_))
  if bstack1l11lll1_opy_:
    item.options[bstack11l1ll_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧો")].insert(0, bstack11l1ll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘࡀࡻࡾࠩૌ").format(bstack1l11lll1_opy_))
  return bstack111l1llll_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack111l1lll1_opy_(command, item_index):
  os.environ[bstack11l1ll_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ્")] = json.dumps(CONFIG[bstack11l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ૎")][item_index % bstack1ll1l1l111_opy_])
  global bstack1l11lll1_opy_
  if bstack1l11lll1_opy_:
    command[0] = command[0].replace(bstack11l1ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ૏"), bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧૐ") + str(
      item_index) + bstack11l1ll_opy_ (u"ࠫࠥ࠭૑") + bstack1l11lll1_opy_, 1)
  else:
    command[0] = command[0].replace(bstack11l1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ૒"),
                                    bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪ૓") + str(item_index), 1)
def bstack1l1111l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1lll1l1lll_opy_
  bstack111l1lll1_opy_(command, item_index)
  return bstack1lll1l1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1ll11l1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1lll1l1lll_opy_
  bstack111l1lll1_opy_(command, item_index)
  return bstack1lll1l1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1lllll1l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1lll1l1lll_opy_
  bstack111l1lll1_opy_(command, item_index)
  return bstack1lll1l1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack11llllll_opy_(self, runner, quiet=False, capture=True):
  global bstack1ll1lll1l1_opy_
  bstack1l1l1l11ll_opy_ = bstack1ll1lll1l1_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack11l1ll_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧ૔")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11l1ll_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬ૕")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l1l1l11ll_opy_
def bstack111l11111_opy_(self, name, context, *args):
  os.environ[bstack11l1ll_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ૖")] = json.dumps(CONFIG[bstack11l1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭૗")][int(threading.current_thread()._name) % bstack1ll1l1l111_opy_])
  global bstack1l1111ll1_opy_
  if name == bstack11l1ll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ૘"):
    bstack1l1111ll1_opy_(self, name, context, *args)
    try:
      if not bstack1111111l_opy_:
        bstack11llll1l_opy_ = threading.current_thread().bstackSessionDriver if bstack11ll11l1l_opy_(bstack11l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ૙")) else context.browser
        bstack11ll1ll1l_opy_ = str(self.feature.name)
        bstack1ll11ll11_opy_(context, bstack11ll1ll1l_opy_)
        bstack11llll1l_opy_.execute_script(bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ૚") + json.dumps(bstack11ll1ll1l_opy_) + bstack11l1ll_opy_ (u"ࠧࡾࡿࠪ૛"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack11l1ll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ૜").format(str(e)))
  elif name == bstack11l1ll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ૝"):
    bstack1l1111ll1_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstack11l1ll_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ૞")):
        self.driver_before_scenario = True
      if (not bstack1111111l_opy_):
        scenario_name = args[0].name
        feature_name = bstack11ll1ll1l_opy_ = str(self.feature.name)
        bstack11ll1ll1l_opy_ = feature_name + bstack11l1ll_opy_ (u"ࠫࠥ࠳ࠠࠨ૟") + scenario_name
        bstack11llll1l_opy_ = threading.current_thread().bstackSessionDriver if bstack11ll11l1l_opy_(bstack11l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫૠ")) else context.browser
        if self.driver_before_scenario:
          bstack1ll11ll11_opy_(context, bstack11ll1ll1l_opy_)
          bstack11llll1l_opy_.execute_script(bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫૡ") + json.dumps(bstack11ll1ll1l_opy_) + bstack11l1ll_opy_ (u"ࠧࡾࡿࠪૢ"))
    except Exception as e:
      logger.debug(bstack11l1ll_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩૣ").format(str(e)))
  elif name == bstack11l1ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ૤"):
    try:
      bstack11l1l11l_opy_ = args[0].status.name
      bstack11llll1l_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ૥") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack11l1l11l_opy_).lower() == bstack11l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ૦"):
        bstack111ll111_opy_ = bstack11l1ll_opy_ (u"ࠬ࠭૧")
        bstack1ll1l1lll_opy_ = bstack11l1ll_opy_ (u"࠭ࠧ૨")
        bstack1l1lllll1l_opy_ = bstack11l1ll_opy_ (u"ࠧࠨ૩")
        try:
          import traceback
          bstack111ll111_opy_ = self.exception.__class__.__name__
          bstack111lll1l1_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1ll1l1lll_opy_ = bstack11l1ll_opy_ (u"ࠨࠢࠪ૪").join(bstack111lll1l1_opy_)
          bstack1l1lllll1l_opy_ = bstack111lll1l1_opy_[-1]
        except Exception as e:
          logger.debug(bstack1l1111l1l_opy_.format(str(e)))
        bstack111ll111_opy_ += bstack1l1lllll1l_opy_
        bstack11lll1ll_opy_(context, json.dumps(str(args[0].name) + bstack11l1ll_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ૫") + str(bstack1ll1l1lll_opy_)),
                            bstack11l1ll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ૬"))
        if self.driver_before_scenario:
          bstack11l1l111l_opy_(getattr(context, bstack11l1ll_opy_ (u"ࠫࡵࡧࡧࡦࠩ૭"), None), bstack11l1ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ૮"), bstack111ll111_opy_)
          bstack11llll1l_opy_.execute_script(bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ૯") + json.dumps(str(args[0].name) + bstack11l1ll_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨ૰") + str(bstack1ll1l1lll_opy_)) + bstack11l1ll_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ૱"))
        if self.driver_before_scenario:
          bstack1l1ll1llll_opy_(bstack11llll1l_opy_, bstack11l1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ૲"), bstack11l1ll_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢ૳") + str(bstack111ll111_opy_))
      else:
        bstack11lll1ll_opy_(context, bstack11l1ll_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧ૴"), bstack11l1ll_opy_ (u"ࠧ࡯࡮ࡧࡱࠥ૵"))
        if self.driver_before_scenario:
          bstack11l1l111l_opy_(getattr(context, bstack11l1ll_opy_ (u"࠭ࡰࡢࡩࡨࠫ૶"), None), bstack11l1ll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ૷"))
        bstack11llll1l_opy_.execute_script(bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭૸") + json.dumps(str(args[0].name) + bstack11l1ll_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨૹ")) + bstack11l1ll_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩૺ"))
        if self.driver_before_scenario:
          bstack1l1ll1llll_opy_(bstack11llll1l_opy_, bstack11l1ll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦૻ"))
    except Exception as e:
      logger.debug(bstack11l1ll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧૼ").format(str(e)))
  elif name == bstack11l1ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭૽"):
    try:
      bstack11llll1l_opy_ = threading.current_thread().bstackSessionDriver if bstack11ll11l1l_opy_(bstack11l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭૾")) else context.browser
      if context.failed is True:
        bstack11l1ll1ll_opy_ = []
        bstack111l1ll11_opy_ = []
        bstack111ll1ll_opy_ = []
        bstack11lll11l1_opy_ = bstack11l1ll_opy_ (u"ࠨࠩ૿")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack11l1ll1ll_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack111lll1l1_opy_ = traceback.format_tb(exc_tb)
            bstack1lll1l1l11_opy_ = bstack11l1ll_opy_ (u"ࠩࠣࠫ଀").join(bstack111lll1l1_opy_)
            bstack111l1ll11_opy_.append(bstack1lll1l1l11_opy_)
            bstack111ll1ll_opy_.append(bstack111lll1l1_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l1111l1l_opy_.format(str(e)))
        bstack111ll111_opy_ = bstack11l1ll_opy_ (u"ࠪࠫଁ")
        for i in range(len(bstack11l1ll1ll_opy_)):
          bstack111ll111_opy_ += bstack11l1ll1ll_opy_[i] + bstack111ll1ll_opy_[i] + bstack11l1ll_opy_ (u"ࠫࡡࡴࠧଂ")
        bstack11lll11l1_opy_ = bstack11l1ll_opy_ (u"ࠬࠦࠧଃ").join(bstack111l1ll11_opy_)
        if not self.driver_before_scenario:
          bstack11lll1ll_opy_(context, bstack11lll11l1_opy_, bstack11l1ll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ଄"))
          bstack11l1l111l_opy_(getattr(context, bstack11l1ll_opy_ (u"ࠧࡱࡣࡪࡩࠬଅ"), None), bstack11l1ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣଆ"), bstack111ll111_opy_)
          bstack11llll1l_opy_.execute_script(bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧଇ") + json.dumps(bstack11lll11l1_opy_) + bstack11l1ll_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪଈ"))
          bstack1l1ll1llll_opy_(bstack11llll1l_opy_, bstack11l1ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦଉ"), bstack11l1ll_opy_ (u"࡙ࠧ࡯࡮ࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳࡸࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡝ࡰࠥଊ") + str(bstack111ll111_opy_))
          bstack1l1l11l1_opy_ = bstack1ll111l1l_opy_(bstack11lll11l1_opy_, self.feature.name, logger)
          if (bstack1l1l11l1_opy_ != None):
            bstack1ll1ll1ll_opy_.append(bstack1l1l11l1_opy_)
      else:
        if not self.driver_before_scenario:
          bstack11lll1ll_opy_(context, bstack11l1ll_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤଋ") + str(self.feature.name) + bstack11l1ll_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤଌ"), bstack11l1ll_opy_ (u"ࠣ࡫ࡱࡪࡴࠨ଍"))
          bstack11l1l111l_opy_(getattr(context, bstack11l1ll_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ଎"), None), bstack11l1ll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥଏ"))
          bstack11llll1l_opy_.execute_script(bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩଐ") + json.dumps(bstack11l1ll_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣ଑") + str(self.feature.name) + bstack11l1ll_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣ଒")) + bstack11l1ll_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭ଓ"))
          bstack1l1ll1llll_opy_(bstack11llll1l_opy_, bstack11l1ll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨଔ"))
          bstack1l1l11l1_opy_ = bstack1ll111l1l_opy_(bstack11lll11l1_opy_, self.feature.name, logger)
          if (bstack1l1l11l1_opy_ != None):
            bstack1ll1ll1ll_opy_.append(bstack1l1l11l1_opy_)
    except Exception as e:
      logger.debug(bstack11l1ll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫକ").format(str(e)))
  else:
    bstack1l1111ll1_opy_(self, name, context, *args)
  if name in [bstack11l1ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪଖ"), bstack11l1ll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬଗ")]:
    bstack1l1111ll1_opy_(self, name, context, *args)
    if (name == bstack11l1ll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ଘ") and self.driver_before_scenario) or (
            name == bstack11l1ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ଙ") and not self.driver_before_scenario):
      try:
        bstack11llll1l_opy_ = threading.current_thread().bstackSessionDriver if bstack11ll11l1l_opy_(bstack11l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ଚ")) else context.browser
        bstack11llll1l_opy_.quit()
      except Exception:
        pass
def bstack1l1l11l1ll_opy_(config, startdir):
  return bstack11l1ll_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨଛ").format(bstack11l1ll_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣଜ"))
notset = Notset()
def bstack1111l1ll1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1ll1l1111_opy_
  if str(name).lower() == bstack11l1ll_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪଝ"):
    return bstack11l1ll_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥଞ")
  else:
    return bstack1ll1l1111_opy_(self, name, default, skip)
def bstack1llllllll1_opy_(item, when):
  global bstack111l111l1_opy_
  try:
    bstack111l111l1_opy_(item, when)
  except Exception as e:
    pass
def bstack111llll11_opy_():
  return
def bstack11111111_opy_(type, name, status, reason, bstack111ll1111_opy_, bstack11ll11lll_opy_):
  bstack11ll1l1l1_opy_ = {
    bstack11l1ll_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬଟ"): type,
    bstack11l1ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩଠ"): {}
  }
  if type == bstack11l1ll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩଡ"):
    bstack11ll1l1l1_opy_[bstack11l1ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫଢ")][bstack11l1ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨଣ")] = bstack111ll1111_opy_
    bstack11ll1l1l1_opy_[bstack11l1ll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ତ")][bstack11l1ll_opy_ (u"ࠫࡩࡧࡴࡢࠩଥ")] = json.dumps(str(bstack11ll11lll_opy_))
  if type == bstack11l1ll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ଦ"):
    bstack11ll1l1l1_opy_[bstack11l1ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩଧ")][bstack11l1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬନ")] = name
  if type == bstack11l1ll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ଩"):
    bstack11ll1l1l1_opy_[bstack11l1ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬପ")][bstack11l1ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪଫ")] = status
    if status == bstack11l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫବ"):
      bstack11ll1l1l1_opy_[bstack11l1ll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨଭ")][bstack11l1ll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ମ")] = json.dumps(str(reason))
  bstack1l1l1lll1_opy_ = bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬଯ").format(json.dumps(bstack11ll1l1l1_opy_))
  return bstack1l1l1lll1_opy_
def bstack1l1ll111ll_opy_(driver_command, response):
    if driver_command == bstack11l1ll_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬର"):
        bstack1l11l1111_opy_.bstack1l11l1l11_opy_({
            bstack11l1ll_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨ଱"): response[bstack11l1ll_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩଲ")],
            bstack11l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫଳ"): bstack1l11l1111_opy_.current_test_uuid()
        })
def bstack111111lll_opy_(item, call, rep):
  global bstack1l1l1l1lll_opy_
  global bstack1llll11lll_opy_
  global bstack1111111l_opy_
  name = bstack11l1ll_opy_ (u"ࠬ࠭଴")
  try:
    if rep.when == bstack11l1ll_opy_ (u"࠭ࡣࡢ࡮࡯ࠫଵ"):
      bstack1l111l11l_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1111111l_opy_:
          name = str(rep.nodeid)
          bstack1111llll_opy_ = bstack11111111_opy_(bstack11l1ll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨଶ"), name, bstack11l1ll_opy_ (u"ࠨࠩଷ"), bstack11l1ll_opy_ (u"ࠩࠪସ"), bstack11l1ll_opy_ (u"ࠪࠫହ"), bstack11l1ll_opy_ (u"ࠫࠬ଺"))
          threading.current_thread().bstack1lll1l1l_opy_ = name
          for driver in bstack1llll11lll_opy_:
            if bstack1l111l11l_opy_ == driver.session_id:
              driver.execute_script(bstack1111llll_opy_)
      except Exception as e:
        logger.debug(bstack11l1ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ଻").format(str(e)))
      try:
        bstack1l1ll1l11_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11l1ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪ଼ࠧ"):
          status = bstack11l1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧଽ") if rep.outcome.lower() == bstack11l1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨା") else bstack11l1ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩି")
          reason = bstack11l1ll_opy_ (u"ࠪࠫୀ")
          if status == bstack11l1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫୁ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11l1ll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪୂ") if status == bstack11l1ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ୃ") else bstack11l1ll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ୄ")
          data = name + bstack11l1ll_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪ୅") if status == bstack11l1ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ୆") else name + bstack11l1ll_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭େ") + reason
          bstack1llllll11l_opy_ = bstack11111111_opy_(bstack11l1ll_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ୈ"), bstack11l1ll_opy_ (u"ࠬ࠭୉"), bstack11l1ll_opy_ (u"࠭ࠧ୊"), bstack11l1ll_opy_ (u"ࠧࠨୋ"), level, data)
          for driver in bstack1llll11lll_opy_:
            if bstack1l111l11l_opy_ == driver.session_id:
              driver.execute_script(bstack1llllll11l_opy_)
      except Exception as e:
        logger.debug(bstack11l1ll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬୌ").format(str(e)))
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ୍࠭").format(str(e)))
  bstack1l1l1l1lll_opy_(item, call, rep)
def bstack111l11l1_opy_(driver, bstack1lllll1l11_opy_):
  PercySDK.screenshot(driver, bstack1lllll1l11_opy_)
def bstack1lll11ll_opy_(driver):
  if bstack1l1l1l1ll1_opy_.bstack1l1ll1lll1_opy_() is True or bstack1l1l1l1ll1_opy_.capturing() is True:
    return
  bstack1l1l1l1ll1_opy_.bstack1llll111l_opy_()
  while not bstack1l1l1l1ll1_opy_.bstack1l1ll1lll1_opy_():
    bstack1ll111lll1_opy_ = bstack1l1l1l1ll1_opy_.bstack11lll111l_opy_()
    bstack111l11l1_opy_(driver, bstack1ll111lll1_opy_)
  bstack1l1l1l1ll1_opy_.bstack11l1l11l1_opy_()
def bstack1ll111111_opy_(sequence, driver_command, response = None):
    try:
      if sequence != bstack11l1ll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ୎"):
        return
      if not CONFIG.get(bstack11l1ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ୏"), False):
        return
      bstack1ll111lll1_opy_ = bstack111l1lll_opy_(threading.current_thread(), bstack11l1ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ୐"), None)
      for command in bstack1ll1l11111_opy_:
        if command == driver_command:
          for driver in bstack1llll11lll_opy_:
            bstack1lll11ll_opy_(driver)
      bstack111ll111l_opy_ = percy.bstack1l111111l_opy_()
      if driver_command in bstack1ll1111l11_opy_[bstack111ll111l_opy_]:
        bstack1l1l1l1ll1_opy_.bstack111ll11l1_opy_(bstack1ll111lll1_opy_, driver_command)
    except Exception as e:
      pass
def bstack11l111l1_opy_(framework_name):
  global bstack1ll11llll1_opy_
  global bstack1ll1ll11l1_opy_
  global bstack111llllll_opy_
  bstack1ll11llll1_opy_ = framework_name
  logger.info(bstack1l1ll1111_opy_.format(bstack1ll11llll1_opy_.split(bstack11l1ll_opy_ (u"࠭࠭ࠨ୑"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack11lllll1_opy_:
      Service.start = bstack111llll1_opy_
      Service.stop = bstack1lll1lllll_opy_
      webdriver.Remote.get = bstack111ll11ll_opy_
      WebDriver.close = bstack1ll111l1ll_opy_
      WebDriver.quit = bstack1ll1llll1_opy_
      webdriver.Remote.__init__ = bstack1ll1l1l11_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.bstack1l1lll111_opy_ = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.bstack1l1l11ll_opy_ = getAccessibilityResultsSummary
    if not bstack11lllll1_opy_ and bstack1l11l1111_opy_.on():
      webdriver.Remote.__init__ = bstack111l1ll1l_opy_
    if bstack1l11l1111_opy_.on():
      WebDriver.execute = bstack11llll1l1_opy_
    bstack1ll1ll11l1_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack11lllll1_opy_:
      from bstack1ll11l1l1_opy_.keywords import browser
      browser.bstack11l11llll_opy_ = bstack1l1l11l111_opy_
  except Exception as e:
    pass
  bstack1ll11l11_opy_()
  if not bstack1ll1ll11l1_opy_:
    bstack1l1lll1l11_opy_(bstack11l1ll_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤ୒"), bstack1l1l11ll1l_opy_)
  if bstack11ll11l1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1lll1ll111_opy_
    except Exception as e:
      logger.error(bstack1l111111_opy_.format(str(e)))
  if bstack1ll111l111_opy_():
    bstack11ll111ll_opy_(CONFIG, logger)
  if (bstack11l1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ୓") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if CONFIG.get(bstack11l1ll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ୔"), False):
          bstack1lll1lll_opy_(bstack1ll111111_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1111111ll_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1l111llll_opy_
      except Exception as e:
        logger.warn(bstack1l1ll11l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1lll11lll_opy_
      except Exception as e:
        logger.debug(bstack1l1l1lllll_opy_ + str(e))
    except Exception as e:
      bstack1l1lll1l11_opy_(e, bstack1l1ll11l_opy_)
    Output.start_test = bstack1llll1lll1_opy_
    Output.end_test = bstack1111ll1l1_opy_
    TestStatus.__init__ = bstack1lllll1ll1_opy_
    QueueItem.__init__ = bstack1ll1l1111l_opy_
    pabot._create_items = bstack1ll11l1l1l_opy_
    try:
      from pabot import __version__ as bstack11ll1l11l_opy_
      if version.parse(bstack11ll1l11l_opy_) >= version.parse(bstack11l1ll_opy_ (u"ࠪ࠶࠳࠷࠵࠯࠲ࠪ୕")):
        pabot._run = bstack1lllll1l1l_opy_
      elif version.parse(bstack11ll1l11l_opy_) >= version.parse(bstack11l1ll_opy_ (u"ࠫ࠷࠴࠱࠴࠰࠳ࠫୖ")):
        pabot._run = bstack1ll11l1l11_opy_
      else:
        pabot._run = bstack1l1111l11_opy_
    except Exception as e:
      pabot._run = bstack1l1111l11_opy_
    pabot._create_command_for_execution = bstack1ll1ll1111_opy_
    pabot._report_results = bstack1ll11lllll_opy_
  if bstack11l1ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬୗ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1lll1l11_opy_(e, bstack1l1ll1l11l_opy_)
    Runner.run_hook = bstack111l11111_opy_
    Step.run = bstack11llllll_opy_
  if bstack11l1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭୘") in str(framework_name).lower():
    if not bstack11lllll1_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1l1l11l1ll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack111llll11_opy_
      Config.getoption = bstack1111l1ll1_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack111111lll_opy_
    except Exception as e:
      pass
def bstack11l1lllll_opy_():
  global CONFIG
  if bstack11l1ll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ୙") in CONFIG and int(CONFIG[bstack11l1ll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ୚")]) > 1:
    logger.warn(bstack1ll11l1ll_opy_)
def bstack1ll1llllll_opy_(arg, bstack1l1lll1l1_opy_, bstack11lll1ll1_opy_=None):
  global CONFIG
  global bstack1llll1111_opy_
  global bstack1l1llllll1_opy_
  global bstack11lllll1_opy_
  global bstack1ll1l11ll1_opy_
  bstack1l1lllllll_opy_ = bstack11l1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ୛")
  if bstack1l1lll1l1_opy_ and isinstance(bstack1l1lll1l1_opy_, str):
    bstack1l1lll1l1_opy_ = eval(bstack1l1lll1l1_opy_)
  CONFIG = bstack1l1lll1l1_opy_[bstack11l1ll_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪଡ଼")]
  bstack1llll1111_opy_ = bstack1l1lll1l1_opy_[bstack11l1ll_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬଢ଼")]
  bstack1l1llllll1_opy_ = bstack1l1lll1l1_opy_[bstack11l1ll_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ୞")]
  bstack11lllll1_opy_ = bstack1l1lll1l1_opy_[bstack11l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩୟ")]
  bstack1ll1l11ll1_opy_.bstack11l11l11_opy_(bstack11l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨୠ"), bstack11lllll1_opy_)
  os.environ[bstack11l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪୡ")] = bstack1l1lllllll_opy_
  os.environ[bstack11l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨୢ")] = json.dumps(CONFIG)
  os.environ[bstack11l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪୣ")] = bstack1llll1111_opy_
  os.environ[bstack11l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ୤")] = str(bstack1l1llllll1_opy_)
  os.environ[bstack11l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡒࡕࡈࡋࡑࠫ୥")] = str(True)
  if bstack1lll1l1ll1_opy_(arg, [bstack11l1ll_opy_ (u"࠭࠭࡯ࠩ୦"), bstack11l1ll_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ୧")]) != -1:
    os.environ[bstack11l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍࠩ୨")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack11l11l11l_opy_)
    return
  bstack11l1l1l11_opy_()
  global bstack11111111l_opy_
  global bstack11lll1l1l_opy_
  global bstack1ll111ll1_opy_
  global bstack1l11lll1_opy_
  global bstack1ll111111l_opy_
  global bstack111llllll_opy_
  global bstack11lllllll_opy_
  arg.append(bstack11l1ll_opy_ (u"ࠤ࠰࡛ࠧ୩"))
  arg.append(bstack11l1ll_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡑࡴࡪࡵ࡭ࡧࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡮ࡳࡰࡰࡴࡷࡩࡩࡀࡰࡺࡶࡨࡷࡹ࠴ࡐࡺࡶࡨࡷࡹ࡝ࡡࡳࡰ࡬ࡲ࡬ࠨ୪"))
  arg.append(bstack11l1ll_opy_ (u"ࠦ࠲࡝ࠢ୫"))
  arg.append(bstack11l1ll_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿࡚ࡨࡦࠢ࡫ࡳࡴࡱࡩ࡮ࡲ࡯ࠦ୬"))
  global bstack111l1l1ll_opy_
  global bstack1l11111ll_opy_
  global bstack11lll1lll_opy_
  global bstack1111lllll_opy_
  global bstack1ll1llll_opy_
  global bstack111l1llll_opy_
  global bstack11111lll1_opy_
  global bstack1l11l111_opy_
  global bstack1l111l111_opy_
  global bstack1ll1l1111_opy_
  global bstack111l111l1_opy_
  global bstack1l1l1l1lll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack111l1l1ll_opy_ = webdriver.Remote.__init__
    bstack1l11111ll_opy_ = WebDriver.quit
    bstack11111lll1_opy_ = WebDriver.close
    bstack1l11l111_opy_ = WebDriver.get
  except Exception as e:
    pass
  if bstack1ll11ll1l_opy_(CONFIG) and bstack1ll1lllll_opy_():
    if bstack11l1ll1l1_opy_() < version.parse(bstack1lllllllll_opy_):
      logger.error(bstack1lll1l1l1_opy_.format(bstack11l1ll1l1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l111l111_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1l111111_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1ll1l1111_opy_ = Config.getoption
    from _pytest import runner
    bstack111l111l1_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1llll1l1_opy_)
  try:
    from pytest_bdd import reporting
    bstack1l1l1l1lll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack11l1ll_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧ୭"))
  bstack1ll111ll1_opy_ = CONFIG.get(bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ୮"), {}).get(bstack11l1ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ୯"))
  bstack11lllllll_opy_ = True
  bstack11l111l1_opy_(bstack1l1llll1_opy_)
  os.environ[bstack11l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪ୰")] = CONFIG[bstack11l1ll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬୱ")]
  os.environ[bstack11l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ୲")] = CONFIG[bstack11l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ୳")]
  os.environ[bstack11l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ୴")] = bstack11lllll1_opy_.__str__()
  from _pytest.config import main as bstack1l11ll1ll_opy_
  bstack1l11ll1ll_opy_(arg)
  if bstack11l1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫ୵") in multiprocessing.current_process().__dict__.keys():
    for bstack1l1ll11l1l_opy_ in multiprocessing.current_process().bstack_error_list:
      bstack11lll1ll1_opy_.append(bstack1l1ll11l1l_opy_)
def bstack1111ll1l_opy_(arg):
  bstack11l111l1_opy_(bstack1111ll11_opy_)
  os.environ[bstack11l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ୶")] = str(bstack1l1llllll1_opy_)
  from behave.__main__ import main as bstack1lll1ll1_opy_
  bstack1lll1ll1_opy_(arg)
def bstack11lll1111_opy_():
  logger.info(bstack1llllll11_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11l1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ୷"), help=bstack11l1ll_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࠫ୸"))
  parser.add_argument(bstack11l1ll_opy_ (u"ࠫ࠲ࡻࠧ୹"), bstack11l1ll_opy_ (u"ࠬ࠳࠭ࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ୺"), help=bstack11l1ll_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬ୻"))
  parser.add_argument(bstack11l1ll_opy_ (u"ࠧ࠮࡭ࠪ୼"), bstack11l1ll_opy_ (u"ࠨ࠯࠰࡯ࡪࡿࠧ୽"), help=bstack11l1ll_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡡࡤࡥࡨࡷࡸࠦ࡫ࡦࡻࠪ୾"))
  parser.add_argument(bstack11l1ll_opy_ (u"ࠪ࠱࡫࠭୿"), bstack11l1ll_opy_ (u"ࠫ࠲࠳ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ஀"), help=bstack11l1ll_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ஁"))
  bstack1lllll1lll_opy_ = parser.parse_args()
  try:
    bstack1l1l11lll_opy_ = bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥ࡯ࡧࡵ࡭ࡨ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪஂ")
    if bstack1lllll1lll_opy_.framework and bstack1lllll1lll_opy_.framework not in (bstack11l1ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧஃ"), bstack11l1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩ஄")):
      bstack1l1l11lll_opy_ = bstack11l1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨஅ")
    bstack1lll111l11_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1l11lll_opy_)
    bstack11ll1111l_opy_ = open(bstack1lll111l11_opy_, bstack11l1ll_opy_ (u"ࠪࡶࠬஆ"))
    bstack11l1lll1l_opy_ = bstack11ll1111l_opy_.read()
    bstack11ll1111l_opy_.close()
    if bstack1lllll1lll_opy_.username:
      bstack11l1lll1l_opy_ = bstack11l1lll1l_opy_.replace(bstack11l1ll_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫஇ"), bstack1lllll1lll_opy_.username)
    if bstack1lllll1lll_opy_.key:
      bstack11l1lll1l_opy_ = bstack11l1lll1l_opy_.replace(bstack11l1ll_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧஈ"), bstack1lllll1lll_opy_.key)
    if bstack1lllll1lll_opy_.framework:
      bstack11l1lll1l_opy_ = bstack11l1lll1l_opy_.replace(bstack11l1ll_opy_ (u"࡙࠭ࡐࡗࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧஉ"), bstack1lllll1lll_opy_.framework)
    file_name = bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪஊ")
    file_path = os.path.abspath(file_name)
    bstack1llll1ll1_opy_ = open(file_path, bstack11l1ll_opy_ (u"ࠨࡹࠪ஋"))
    bstack1llll1ll1_opy_.write(bstack11l1lll1l_opy_)
    bstack1llll1ll1_opy_.close()
    logger.info(bstack1ll1l1l11l_opy_)
    try:
      os.environ[bstack11l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ஌")] = bstack1lllll1lll_opy_.framework if bstack1lllll1lll_opy_.framework != None else bstack11l1ll_opy_ (u"ࠥࠦ஍")
      config = yaml.safe_load(bstack11l1lll1l_opy_)
      config[bstack11l1ll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫஎ")] = bstack11l1ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡹࡥࡵࡷࡳࠫஏ")
      bstack1l11lll1l_opy_(bstack1llll1l111_opy_, config)
    except Exception as e:
      logger.debug(bstack1l1l1llll1_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1lllll11l_opy_.format(str(e)))
def bstack1l11lll1l_opy_(bstack111l1l1l_opy_, config, bstack111lllll_opy_={}):
  global bstack11lllll1_opy_
  global bstack1l1l1l1111_opy_
  if not config:
    return
  bstack1l1ll1ll11_opy_ = bstack11lllll1l_opy_ if not bstack11lllll1_opy_ else (
    bstack1ll11111ll_opy_ if bstack11l1ll_opy_ (u"࠭ࡡࡱࡲࠪஐ") in config else bstack1ll1l11lll_opy_)
  data = {
    bstack11l1ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ஑"): config[bstack11l1ll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪஒ")],
    bstack11l1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬஓ"): config[bstack11l1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ஔ")],
    bstack11l1ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨக"): bstack111l1l1l_opy_,
    bstack11l1ll_opy_ (u"ࠬࡪࡥࡵࡧࡦࡸࡪࡪࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ஖"): os.environ.get(bstack11l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ஗"), bstack1l1l1l1111_opy_),
    bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ஘"): bstack111l11l1l_opy_,
    bstack11l1ll_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮ࠪங"): bstack1l1lll11l1_opy_(),
    bstack11l1ll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬச"): {
      bstack11l1ll_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ஛"): str(config[bstack11l1ll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫஜ")]) if bstack11l1ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ஝") in config else bstack11l1ll_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢஞ"),
      bstack11l1ll_opy_ (u"ࠧࡳࡧࡩࡩࡷࡸࡥࡳࠩட"): bstack111ll11l_opy_(os.getenv(bstack11l1ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠥ஠"), bstack11l1ll_opy_ (u"ࠤࠥ஡"))),
      bstack11l1ll_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬ஢"): bstack11l1ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫண"),
      bstack11l1ll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭த"): bstack1l1ll1ll11_opy_,
      bstack11l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ஥"): config[bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ஦")] if config[bstack11l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ஧")] else bstack11l1ll_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥந"),
      bstack11l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬன"): str(config[bstack11l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ப")]) if bstack11l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ஫") in config else bstack11l1ll_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢ஬"),
      bstack11l1ll_opy_ (u"ࠧࡰࡵࠪ஭"): sys.platform,
      bstack11l1ll_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪம"): socket.gethostname()
    }
  }
  update(data[bstack11l1ll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬய")], bstack111lllll_opy_)
  try:
    response = bstack1lll1l111l_opy_(bstack11l1ll_opy_ (u"ࠪࡔࡔ࡙ࡔࠨர"), bstack1l11l11l_opy_(bstack111lll111_opy_), data, {
      bstack11l1ll_opy_ (u"ࠫࡦࡻࡴࡩࠩற"): (config[bstack11l1ll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧல")], config[bstack11l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩள")])
    })
    if response:
      logger.debug(bstack11ll1l111_opy_.format(bstack111l1l1l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1lll11l11l_opy_.format(str(e)))
def bstack111ll11l_opy_(framework):
  return bstack11l1ll_opy_ (u"ࠢࡼࡿ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࡽࢀࠦழ").format(str(framework), __version__) if framework else bstack11l1ll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤவ").format(
    __version__)
def bstack11l1l1l11_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack1ll1ll11ll_opy_()
    logger.debug(bstack11ll1l1ll_opy_.format(str(CONFIG)))
    bstack1111l1111_opy_()
    bstack1ll1111ll1_opy_()
  except Exception as e:
    logger.error(bstack11l1ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠨஶ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l1llll11l_opy_
  atexit.register(bstack111l11ll_opy_)
  signal.signal(signal.SIGINT, bstack1l1l1ll1_opy_)
  signal.signal(signal.SIGTERM, bstack1l1l1ll1_opy_)
def bstack1l1llll11l_opy_(exctype, value, traceback):
  global bstack1llll11lll_opy_
  try:
    for driver in bstack1llll11lll_opy_:
      bstack1l1ll1llll_opy_(driver, bstack11l1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪஷ"), bstack11l1ll_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢஸ") + str(value))
  except Exception:
    pass
  bstack1l11l111l_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l11l111l_opy_(message=bstack11l1ll_opy_ (u"ࠬ࠭ஹ"), bstack1111l111l_opy_ = False):
  global CONFIG
  bstack111l1ll1_opy_ = bstack11l1ll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠨ஺") if bstack1111l111l_opy_ else bstack11l1ll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭஻")
  try:
    if message:
      bstack111lllll_opy_ = {
        bstack111l1ll1_opy_ : str(message)
      }
      bstack1l11lll1l_opy_(bstack1ll11l11l_opy_, CONFIG, bstack111lllll_opy_)
    else:
      bstack1l11lll1l_opy_(bstack1ll11l11l_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11l111lll_opy_.format(str(e)))
def bstack1l1lll1ll1_opy_(bstack11ll1ll11_opy_, size):
  bstack1l11llll1_opy_ = []
  while len(bstack11ll1ll11_opy_) > size:
    bstack111lll11_opy_ = bstack11ll1ll11_opy_[:size]
    bstack1l11llll1_opy_.append(bstack111lll11_opy_)
    bstack11ll1ll11_opy_ = bstack11ll1ll11_opy_[size:]
  bstack1l11llll1_opy_.append(bstack11ll1ll11_opy_)
  return bstack1l11llll1_opy_
def bstack11l11111_opy_(args):
  if bstack11l1ll_opy_ (u"ࠨ࠯ࡰࠫ஼") in args and bstack11l1ll_opy_ (u"ࠩࡳࡨࡧ࠭஽") in args:
    return True
  return False
def run_on_browserstack(bstack1l1lll1l1l_opy_=None, bstack11lll1ll1_opy_=None, bstack1llll1ll1l_opy_=False):
  global CONFIG
  global bstack1llll1111_opy_
  global bstack1l1llllll1_opy_
  global bstack1l1l1l1111_opy_
  bstack1l1lllllll_opy_ = bstack11l1ll_opy_ (u"ࠪࠫா")
  bstack111111l1_opy_(bstack1ll1ll111l_opy_, logger)
  if bstack1l1lll1l1l_opy_ and isinstance(bstack1l1lll1l1l_opy_, str):
    bstack1l1lll1l1l_opy_ = eval(bstack1l1lll1l1l_opy_)
  if bstack1l1lll1l1l_opy_:
    CONFIG = bstack1l1lll1l1l_opy_[bstack11l1ll_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫி")]
    bstack1llll1111_opy_ = bstack1l1lll1l1l_opy_[bstack11l1ll_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ீ")]
    bstack1l1llllll1_opy_ = bstack1l1lll1l1l_opy_[bstack11l1ll_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨு")]
    bstack1ll1l11ll1_opy_.bstack11l11l11_opy_(bstack11l1ll_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩூ"), bstack1l1llllll1_opy_)
    bstack1l1lllllll_opy_ = bstack11l1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ௃")
  if not bstack1llll1ll1l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack11l11l11l_opy_)
      return
    if sys.argv[1] == bstack11l1ll_opy_ (u"ࠩ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬ௄") or sys.argv[1] == bstack11l1ll_opy_ (u"ࠪ࠱ࡻ࠭௅"):
      logger.info(bstack11l1ll_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡔࡾࡺࡨࡰࡰࠣࡗࡉࡑࠠࡷࡽࢀࠫெ").format(__version__))
      return
    if sys.argv[1] == bstack11l1ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫே"):
      bstack11lll1111_opy_()
      return
  args = sys.argv
  bstack11l1l1l11_opy_()
  global bstack11111111l_opy_
  global bstack1ll1l1l111_opy_
  global bstack11lllllll_opy_
  global bstack1l1l1l111_opy_
  global bstack11lll1l1l_opy_
  global bstack1ll111ll1_opy_
  global bstack1l11lll1_opy_
  global bstack1ll1111l_opy_
  global bstack1ll111111l_opy_
  global bstack111llllll_opy_
  global bstack11lll111_opy_
  bstack1ll1l1l111_opy_ = len(CONFIG[bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩை")])
  if not bstack1l1lllllll_opy_:
    if args[1] == bstack11l1ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ௉") or args[1] == bstack11l1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩொ"):
      bstack1l1lllllll_opy_ = bstack11l1ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩோ")
      args = args[2:]
    elif args[1] == bstack11l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩௌ"):
      bstack1l1lllllll_opy_ = bstack11l1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶ்ࠪ")
      args = args[2:]
    elif args[1] == bstack11l1ll_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ௎"):
      bstack1l1lllllll_opy_ = bstack11l1ll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ௏")
      args = args[2:]
    elif args[1] == bstack11l1ll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨௐ"):
      bstack1l1lllllll_opy_ = bstack11l1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ௑")
      args = args[2:]
    elif args[1] == bstack11l1ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ௒"):
      bstack1l1lllllll_opy_ = bstack11l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ௓")
      args = args[2:]
    elif args[1] == bstack11l1ll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ௔"):
      bstack1l1lllllll_opy_ = bstack11l1ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ௕")
      args = args[2:]
    else:
      if not bstack11l1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ௖") in CONFIG or str(CONFIG[bstack11l1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪௗ")]).lower() in [bstack11l1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ௘"), bstack11l1ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪ௙")]:
        bstack1l1lllllll_opy_ = bstack11l1ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ௚")
        args = args[1:]
      elif str(CONFIG[bstack11l1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ௛")]).lower() == bstack11l1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ௜"):
        bstack1l1lllllll_opy_ = bstack11l1ll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ௝")
        args = args[1:]
      elif str(CONFIG[bstack11l1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ௞")]).lower() == bstack11l1ll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ௟"):
        bstack1l1lllllll_opy_ = bstack11l1ll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ௠")
        args = args[1:]
      elif str(CONFIG[bstack11l1ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭௡")]).lower() == bstack11l1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ௢"):
        bstack1l1lllllll_opy_ = bstack11l1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ௣")
        args = args[1:]
      elif str(CONFIG[bstack11l1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ௤")]).lower() == bstack11l1ll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ௥"):
        bstack1l1lllllll_opy_ = bstack11l1ll_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ௦")
        args = args[1:]
      else:
        os.environ[bstack11l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ௧")] = bstack1l1lllllll_opy_
        bstack1l1ll1ll1l_opy_(bstack1l1lll1lll_opy_)
  os.environ[bstack11l1ll_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇࠫ௨")] = bstack1l1lllllll_opy_
  bstack1l1l1l1111_opy_ = bstack1l1lllllll_opy_
  global bstack1l1ll1l1l_opy_
  if bstack1l1lll1l1l_opy_:
    try:
      os.environ[bstack11l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭௩")] = bstack1l1lllllll_opy_
      bstack1l11lll1l_opy_(bstack1111ll11l_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack11l111lll_opy_.format(str(e)))
  global bstack111l1l1ll_opy_
  global bstack1l11111ll_opy_
  global bstack1l1lll1l_opy_
  global bstack111111111_opy_
  global bstack11111l1l1_opy_
  global bstack1l11l11ll_opy_
  global bstack11lll1lll_opy_
  global bstack1111lllll_opy_
  global bstack1lll1l1lll_opy_
  global bstack1ll1llll_opy_
  global bstack111l1llll_opy_
  global bstack11111lll1_opy_
  global bstack1l1111ll1_opy_
  global bstack1ll1lll1l1_opy_
  global bstack1l11l111_opy_
  global bstack1l111l111_opy_
  global bstack1ll1l1111_opy_
  global bstack111l111l1_opy_
  global bstack1ll1l111ll_opy_
  global bstack1l1l1l1lll_opy_
  global bstack1111l11l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack111l1l1ll_opy_ = webdriver.Remote.__init__
    bstack1l11111ll_opy_ = WebDriver.quit
    bstack11111lll1_opy_ = WebDriver.close
    bstack1l11l111_opy_ = WebDriver.get
    bstack1111l11l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1ll1l1l_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    global bstack1lll1111l1_opy_
    from bstack1ll11l1l1_opy_.keywords import browser
    bstack1lll1111l1_opy_ = browser.bstack11l11llll_opy_
  except Exception as e:
    pass
  if bstack1ll11ll1l_opy_(CONFIG) and bstack1ll1lllll_opy_():
    if bstack11l1ll1l1_opy_() < version.parse(bstack1lllllllll_opy_):
      logger.error(bstack1lll1l1l1_opy_.format(bstack11l1ll1l1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l111l111_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1l111111_opy_.format(str(e)))
  if bstack1l1lllllll_opy_ != bstack11l1ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ௪") or (bstack1l1lllllll_opy_ == bstack11l1ll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭௫") and not bstack1l1lll1l1l_opy_):
    bstack1111l11l1_opy_()
  if (bstack1l1lllllll_opy_ in [bstack11l1ll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭௬"), bstack11l1ll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ௭"), bstack11l1ll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ௮")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1111111ll_opy_
        bstack1l11l11ll_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1l1ll11l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack11111l1l1_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1l1l1lllll_opy_ + str(e))
    except Exception as e:
      bstack1l1lll1l11_opy_(e, bstack1l1ll11l_opy_)
    if bstack1l1lllllll_opy_ != bstack11l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ௯"):
      bstack1l1l1ll11l_opy_()
    bstack1l1lll1l_opy_ = Output.start_test
    bstack111111111_opy_ = Output.end_test
    bstack11lll1lll_opy_ = TestStatus.__init__
    bstack1lll1l1lll_opy_ = pabot._run
    bstack1ll1llll_opy_ = QueueItem.__init__
    bstack111l1llll_opy_ = pabot._create_command_for_execution
    bstack1ll1l111ll_opy_ = pabot._report_results
  if bstack1l1lllllll_opy_ == bstack11l1ll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ௰"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1lll1l11_opy_(e, bstack1l1ll1l11l_opy_)
    bstack1l1111ll1_opy_ = Runner.run_hook
    bstack1ll1lll1l1_opy_ = Step.run
  if bstack1l1lllllll_opy_ == bstack11l1ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ௱"):
    try:
      from _pytest.config import Config
      bstack1ll1l1111_opy_ = Config.getoption
      from _pytest import runner
      bstack111l111l1_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1llll1l1_opy_)
    try:
      from pytest_bdd import reporting
      bstack1l1l1l1lll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11l1ll_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧ௲"))
  if bstack1l1lllllll_opy_ in bstack1lll11l1l_opy_:
    try:
      framework_name = bstack11l1ll_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭௳") if bstack1l1lllllll_opy_ in [bstack11l1ll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ௴"), bstack11l1ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ௵"), bstack11l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ௶")] else bstack1llll11l_opy_(bstack1l1lllllll_opy_)
      bstack1l11l1111_opy_.launch(CONFIG, {
        bstack11l1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬ௷"): bstack11l1ll_opy_ (u"ࠬࢁ࠰ࡾ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ௸").format(framework_name) if bstack1l1lllllll_opy_ == bstack11l1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭௹") and bstack11l11lll_opy_() else framework_name,
        bstack11l1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ௺"): bstack1llll11111_opy_(framework_name),
        bstack11l1ll_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭௻"): __version__
      })
    except Exception as e:
      logger.debug(bstack1lll1ll1l_opy_.format(bstack11l1ll_opy_ (u"ࠩࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ௼"), str(e)))
  if bstack1l1lllllll_opy_ in bstack11l1111ll_opy_:
    try:
      framework_name = bstack11l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ௽") if bstack1l1lllllll_opy_ in [bstack11l1ll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ௾"), bstack11l1ll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ௿")] else bstack1l1lllllll_opy_
      if bstack11lllll1_opy_ and bstack11l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ఀ") in CONFIG and CONFIG[bstack11l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧఁ")] == True:
        if bstack11l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨం") in CONFIG:
          os.environ[bstack11l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪః")] = os.getenv(bstack11l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫఄ"), json.dumps(CONFIG[bstack11l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫఅ")]))
          CONFIG[bstack11l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬఆ")].pop(bstack11l1ll_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫఇ"), None)
          CONFIG[bstack11l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧఈ")].pop(bstack11l1ll_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ఉ"), None)
        bstack1l1l1l1l11_opy_, bstack111lllll1_opy_ = bstack11ll11ll1_opy_.bstack11l1l1111_opy_(CONFIG, bstack1l1lllllll_opy_, bstack1llll11111_opy_(framework_name))
        if not bstack1l1l1l1l11_opy_ is None:
          os.environ[bstack11l1ll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧఊ")] = bstack1l1l1l1l11_opy_
          os.environ[bstack11l1ll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣ࡙ࡋࡓࡕࡡࡕ࡙ࡓࡥࡉࡅࠩఋ")] = str(bstack111lllll1_opy_)
    except Exception as e:
      logger.debug(bstack1lll1ll1l_opy_.format(bstack11l1ll_opy_ (u"ࠫࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫఌ"), str(e)))
  if bstack1l1lllllll_opy_ == bstack11l1ll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ఍"):
    bstack11lllllll_opy_ = True
    if bstack1l1lll1l1l_opy_ and bstack1llll1ll1l_opy_:
      bstack1ll111ll1_opy_ = CONFIG.get(bstack11l1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪఎ"), {}).get(bstack11l1ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩఏ"))
      bstack11l111l1_opy_(bstack1ll11l1l_opy_)
    elif bstack1l1lll1l1l_opy_:
      bstack1ll111ll1_opy_ = CONFIG.get(bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬఐ"), {}).get(bstack11l1ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ఑"))
      global bstack1llll11lll_opy_
      try:
        if bstack11l11111_opy_(bstack1l1lll1l1l_opy_[bstack11l1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఒ")]) and multiprocessing.current_process().name == bstack11l1ll_opy_ (u"ࠫ࠵࠭ఓ"):
          bstack1l1lll1l1l_opy_[bstack11l1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨఔ")].remove(bstack11l1ll_opy_ (u"࠭࠭࡮ࠩక"))
          bstack1l1lll1l1l_opy_[bstack11l1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪఖ")].remove(bstack11l1ll_opy_ (u"ࠨࡲࡧࡦࠬగ"))
          bstack1l1lll1l1l_opy_[bstack11l1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬఘ")] = bstack1l1lll1l1l_opy_[bstack11l1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఙ")][0]
          with open(bstack1l1lll1l1l_opy_[bstack11l1ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧచ")], bstack11l1ll_opy_ (u"ࠬࡸࠧఛ")) as f:
            bstack1ll1lll1l_opy_ = f.read()
          bstack1111ll111_opy_ = bstack11l1ll_opy_ (u"ࠨࠢࠣࡨࡵࡳࡲࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡤ࡬ࠢ࡬ࡱࡵࡵࡲࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡀࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࠪࡾࢁ࠮ࡁࠠࡧࡴࡲࡱࠥࡶࡤࡣࠢ࡬ࡱࡵࡵࡲࡵࠢࡓࡨࡧࡁࠠࡰࡩࡢࡨࡧࠦ࠽ࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱ࠻ࠋࡦࡨࡪࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠩࡵࡨࡰ࡫࠲ࠠࡢࡴࡪ࠰ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࠿ࠣ࠴࠮ࡀࠊࠡࠢࡷࡶࡾࡀࠊࠡࠢࠣࠤࡦࡸࡧࠡ࠿ࠣࡷࡹࡸࠨࡪࡰࡷࠬࡦࡸࡧࠪ࠭࠴࠴࠮ࠐࠠࠡࡧࡻࡧࡪࡶࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡦࡹࠠࡦ࠼ࠍࠤࠥࠦࠠࡱࡣࡶࡷࠏࠦࠠࡰࡩࡢࡨࡧ࠮ࡳࡦ࡮ࡩ࠰ࡦࡸࡧ࠭ࡶࡨࡱࡵࡵࡲࡢࡴࡼ࠭ࠏࡖࡤࡣ࠰ࡧࡳࡤࡨࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮ࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࡓࡨࡧ࠮ࠩ࠯ࡵࡨࡸࡤࡺࡲࡢࡥࡨࠬ࠮ࡢ࡮ࠣࠤࠥజ").format(str(bstack1l1lll1l1l_opy_))
          bstack1ll1ll1l1l_opy_ = bstack1111ll111_opy_ + bstack1ll1lll1l_opy_
          bstack111ll1l11_opy_ = bstack1l1lll1l1l_opy_[bstack11l1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪఝ")] + bstack11l1ll_opy_ (u"ࠨࡡࡥࡷࡹࡧࡣ࡬ࡡࡷࡩࡲࡶ࠮ࡱࡻࠪఞ")
          with open(bstack111ll1l11_opy_, bstack11l1ll_opy_ (u"ࠩࡺࠫట")):
            pass
          with open(bstack111ll1l11_opy_, bstack11l1ll_opy_ (u"ࠥࡻ࠰ࠨఠ")) as f:
            f.write(bstack1ll1ll1l1l_opy_)
          import subprocess
          bstack11llll1ll_opy_ = subprocess.run([bstack11l1ll_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࠦడ"), bstack111ll1l11_opy_])
          if os.path.exists(bstack111ll1l11_opy_):
            os.unlink(bstack111ll1l11_opy_)
          os._exit(bstack11llll1ll_opy_.returncode)
        else:
          if bstack11l11111_opy_(bstack1l1lll1l1l_opy_[bstack11l1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨఢ")]):
            bstack1l1lll1l1l_opy_[bstack11l1ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩణ")].remove(bstack11l1ll_opy_ (u"ࠧ࠮࡯ࠪత"))
            bstack1l1lll1l1l_opy_[bstack11l1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫథ")].remove(bstack11l1ll_opy_ (u"ࠩࡳࡨࡧ࠭ద"))
            bstack1l1lll1l1l_opy_[bstack11l1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ధ")] = bstack1l1lll1l1l_opy_[bstack11l1ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧన")][0]
          bstack11l111l1_opy_(bstack1ll11l1l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1l1lll1l1l_opy_[bstack11l1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ఩")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11l1ll_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨప")] = bstack11l1ll_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩఫ")
          mod_globals[bstack11l1ll_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪబ")] = os.path.abspath(bstack1l1lll1l1l_opy_[bstack11l1ll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬభ")])
          exec(open(bstack1l1lll1l1l_opy_[bstack11l1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭మ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11l1ll_opy_ (u"ࠫࡈࡧࡵࡨࡪࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠫయ").format(str(e)))
          for driver in bstack1llll11lll_opy_:
            bstack11lll1ll1_opy_.append({
              bstack11l1ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪర"): bstack1l1lll1l1l_opy_[bstack11l1ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩఱ")],
              bstack11l1ll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ల"): str(e),
              bstack11l1ll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧళ"): multiprocessing.current_process().name
            })
            bstack1l1ll1llll_opy_(driver, bstack11l1ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩఴ"), bstack11l1ll_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨవ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1llll11lll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l1llllll1_opy_, CONFIG, logger)
      bstack1l1llll11_opy_()
      bstack11l1lllll_opy_()
      bstack1l1lll1l1_opy_ = {
        bstack11l1ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧశ"): args[0],
        bstack11l1ll_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬష"): CONFIG,
        bstack11l1ll_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧస"): bstack1llll1111_opy_,
        bstack11l1ll_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩహ"): bstack1l1llllll1_opy_
      }
      percy.bstack1llll111l1_opy_()
      if bstack11l1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ఺") in CONFIG:
        bstack1lll1ll1l1_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lll1l1ll_opy_ = manager.list()
        if bstack11l11111_opy_(args):
          for index, platform in enumerate(CONFIG[bstack11l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ఻")]):
            if index == 0:
              bstack1l1lll1l1_opy_[bstack11l1ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ఼࠭")] = args
            bstack1lll1ll1l1_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l1lll1l1_opy_, bstack1lll1l1ll_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack11l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧఽ")]):
            bstack1lll1ll1l1_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l1lll1l1_opy_, bstack1lll1l1ll_opy_)))
        for t in bstack1lll1ll1l1_opy_:
          t.start()
        for t in bstack1lll1ll1l1_opy_:
          t.join()
        bstack1ll1111l_opy_ = list(bstack1lll1l1ll_opy_)
      else:
        if bstack11l11111_opy_(args):
          bstack1l1lll1l1_opy_[bstack11l1ll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨా")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l1lll1l1_opy_,))
          test.start()
          test.join()
        else:
          bstack11l111l1_opy_(bstack1ll11l1l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11l1ll_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨి")] = bstack11l1ll_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩీ")
          mod_globals[bstack11l1ll_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪు")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l1lllllll_opy_ == bstack11l1ll_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨూ") or bstack1l1lllllll_opy_ == bstack11l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩృ"):
    percy.init(bstack1l1llllll1_opy_, CONFIG, logger)
    percy.bstack1llll111l1_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l1lll1l11_opy_(e, bstack1l1ll11l_opy_)
    bstack1l1llll11_opy_()
    bstack11l111l1_opy_(bstack1lllll11l1_opy_)
    if bstack11l1ll_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩౄ") in args:
      i = args.index(bstack11l1ll_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ౅"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack11111111l_opy_))
    args.insert(0, str(bstack11l1ll_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫె")))
    if bstack1l11l1111_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1l1ll1l111_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1lll11llll_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11l1ll_opy_ (u"ࠢࡓࡑࡅࡓ࡙ࡥࡏࡑࡖࡌࡓࡓ࡙ࠢే"),
        ).parse_args(bstack1l1ll1l111_opy_)
        args.insert(args.index(bstack1lll11llll_opy_[0]), str(bstack11l1ll_opy_ (u"ࠨ࠯࠰ࡰ࡮ࡹࡴࡦࡰࡨࡶࠬై")))
        args.insert(args.index(bstack1lll11llll_opy_[0]), str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡵࡳࡧࡵࡴࡠ࡮࡬ࡷࡹ࡫࡮ࡦࡴ࠱ࡴࡾ࠭౉"))))
        if bstack1l1lll11l_opy_(os.environ.get(bstack11l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨొ"))) and str(os.environ.get(bstack11l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨో"), bstack11l1ll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪౌ"))) != bstack11l1ll_opy_ (u"࠭࡮ࡶ࡮࡯్ࠫ"):
          for bstack11111l1ll_opy_ in bstack1lll11llll_opy_:
            args.remove(bstack11111l1ll_opy_)
          bstack1ll11l111_opy_ = os.environ.get(bstack11l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫ౎")).split(bstack11l1ll_opy_ (u"ࠨ࠮ࠪ౏"))
          for bstack1ll1111l1_opy_ in bstack1ll11l111_opy_:
            args.append(bstack1ll1111l1_opy_)
      except Exception as e:
        logger.error(bstack11l1ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡢࡶࡷࡥࡨ࡮ࡩ࡯ࡩࠣࡰ࡮ࡹࡴࡦࡰࡨࡶࠥ࡬࡯ࡳࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠰ࠤࠧ౐").format(e))
    pabot.main(args)
  elif bstack1l1lllllll_opy_ == bstack11l1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ౑"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l1lll1l11_opy_(e, bstack1l1ll11l_opy_)
    for a in args:
      if bstack11l1ll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪ౒") in a:
        bstack11lll1l1l_opy_ = int(a.split(bstack11l1ll_opy_ (u"ࠬࡀࠧ౓"))[1])
      if bstack11l1ll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ౔") in a:
        bstack1ll111ll1_opy_ = str(a.split(bstack11l1ll_opy_ (u"ࠧ࠻ౕࠩ"))[1])
      if bstack11l1ll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨౖ") in a:
        bstack1l11lll1_opy_ = str(a.split(bstack11l1ll_opy_ (u"ࠩ࠽ࠫ౗"))[1])
    bstack1ll1l1l1l_opy_ = None
    if bstack11l1ll_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩౘ") in args:
      i = args.index(bstack11l1ll_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠪౙ"))
      args.pop(i)
      bstack1ll1l1l1l_opy_ = args.pop(i)
    if bstack1ll1l1l1l_opy_ is not None:
      global bstack11111l11_opy_
      bstack11111l11_opy_ = bstack1ll1l1l1l_opy_
    bstack11l111l1_opy_(bstack1lllll11l1_opy_)
    run_cli(args)
    if bstack11l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩౚ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1ll11l1l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11lll1ll1_opy_.append(bstack1l1ll11l1l_opy_)
  elif bstack1l1lllllll_opy_ == bstack11l1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭౛"):
    bstack1ll1l1ll11_opy_ = bstack1l1lll11_opy_(args, logger, CONFIG, bstack11lllll1_opy_)
    bstack1ll1l1ll11_opy_.bstack1ll1lllll1_opy_()
    bstack1l1llll11_opy_()
    bstack1l1l1l111_opy_ = True
    bstack111llllll_opy_ = bstack1ll1l1ll11_opy_.bstack1llll1l1l_opy_()
    bstack1ll1l1ll11_opy_.bstack1l1lll1l1_opy_(bstack1111111l_opy_)
    bstack1ll111111l_opy_ = bstack1ll1l1ll11_opy_.bstack1lllll1ll_opy_(bstack1ll1llllll_opy_, {
      bstack11l1ll_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ౜"): bstack1llll1111_opy_,
      bstack11l1ll_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪౝ"): bstack1l1llllll1_opy_,
      bstack11l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ౞"): bstack11lllll1_opy_
    })
    bstack11lll111_opy_ = 1 if len(bstack1ll111111l_opy_) > 0 else 0
  elif bstack1l1lllllll_opy_ == bstack11l1ll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ౟"):
    try:
      from behave.__main__ import main as bstack1lll1ll1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l1lll1l11_opy_(e, bstack1l1ll1l11l_opy_)
    bstack1l1llll11_opy_()
    bstack1l1l1l111_opy_ = True
    bstack111lll1l_opy_ = 1
    if bstack11l1ll_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫౠ") in CONFIG:
      bstack111lll1l_opy_ = CONFIG[bstack11l1ll_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬౡ")]
    bstack11lll11l_opy_ = int(bstack111lll1l_opy_) * int(len(CONFIG[bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩౢ")]))
    config = Configuration(args)
    bstack1l1ll111_opy_ = config.paths
    if len(bstack1l1ll111_opy_) == 0:
      import glob
      pattern = bstack11l1ll_opy_ (u"ࠧࠫࠬ࠲࠮࠳࡬ࡥࡢࡶࡸࡶࡪ࠭ౣ")
      bstack1llll111_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1llll111_opy_)
      config = Configuration(args)
      bstack1l1ll111_opy_ = config.paths
    bstack11111llll_opy_ = [os.path.normpath(item) for item in bstack1l1ll111_opy_]
    bstack11l1lll1_opy_ = [os.path.normpath(item) for item in args]
    bstack1ll11ll1ll_opy_ = [item for item in bstack11l1lll1_opy_ if item not in bstack11111llll_opy_]
    import platform as pf
    if pf.system().lower() == bstack11l1ll_opy_ (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴࠩ౤"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11111llll_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11llll11_opy_)))
                    for bstack11llll11_opy_ in bstack11111llll_opy_]
    bstack1l1lllll_opy_ = []
    for spec in bstack11111llll_opy_:
      bstack11l1ll1l_opy_ = []
      bstack11l1ll1l_opy_ += bstack1ll11ll1ll_opy_
      bstack11l1ll1l_opy_.append(spec)
      bstack1l1lllll_opy_.append(bstack11l1ll1l_opy_)
    execution_items = []
    for bstack11l1ll1l_opy_ in bstack1l1lllll_opy_:
      for index, _ in enumerate(CONFIG[bstack11l1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౥")]):
        item = {}
        item[bstack11l1ll_opy_ (u"ࠪࡥࡷ࡭ࠧ౦")] = bstack11l1ll_opy_ (u"ࠫࠥ࠭౧").join(bstack11l1ll1l_opy_)
        item[bstack11l1ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ౨")] = index
        execution_items.append(item)
    bstack1lllllll11_opy_ = bstack1l1lll1ll1_opy_(execution_items, bstack11lll11l_opy_)
    for execution_item in bstack1lllllll11_opy_:
      bstack1lll1ll1l1_opy_ = []
      for item in execution_item:
        bstack1lll1ll1l1_opy_.append(bstack1l1l11111_opy_(name=str(item[bstack11l1ll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ౩")]),
                                             target=bstack1111ll1l_opy_,
                                             args=(item[bstack11l1ll_opy_ (u"ࠧࡢࡴࡪࠫ౪")],)))
      for t in bstack1lll1ll1l1_opy_:
        t.start()
      for t in bstack1lll1ll1l1_opy_:
        t.join()
  else:
    bstack1l1ll1ll1l_opy_(bstack1l1lll1lll_opy_)
  if not bstack1l1lll1l1l_opy_:
    bstack111111ll1_opy_()
def browserstack_initialize(bstack1ll1111l1l_opy_=None):
  run_on_browserstack(bstack1ll1111l1l_opy_, None, True)
def bstack111111ll1_opy_():
  global CONFIG
  global bstack1l1l1l1111_opy_
  global bstack11lll111_opy_
  bstack1l11l1111_opy_.stop()
  bstack1l11l1111_opy_.bstack11ll1llll_opy_()
  if bstack11ll11ll1_opy_.bstack111ll1l1l_opy_(CONFIG):
    bstack11ll11ll1_opy_.bstack111l1l11l_opy_()
  [bstack1l1lll1ll_opy_, bstack1lllll1l1_opy_] = bstack1ll111llll_opy_()
  if bstack1l1lll1ll_opy_ is not None and bstack1lll1l1l1l_opy_() != -1:
    sessions = bstack1l11l1l1_opy_(bstack1l1lll1ll_opy_)
    bstack11ll11l11_opy_(sessions, bstack1lllll1l1_opy_)
  if bstack1l1l1l1111_opy_ == bstack11l1ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ౫") and bstack11lll111_opy_ != 0:
    sys.exit(bstack11lll111_opy_)
def bstack1llll11l_opy_(bstack11l1l1ll_opy_):
  if bstack11l1l1ll_opy_:
    return bstack11l1l1ll_opy_.capitalize()
  else:
    return bstack11l1ll_opy_ (u"ࠩࠪ౬")
def bstack1lll1l11ll_opy_(bstack1ll1l1llll_opy_):
  if bstack11l1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨ౭") in bstack1ll1l1llll_opy_ and bstack1ll1l1llll_opy_[bstack11l1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ౮")] != bstack11l1ll_opy_ (u"ࠬ࠭౯"):
    return bstack1ll1l1llll_opy_[bstack11l1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ౰")]
  else:
    bstack1llll1lll_opy_ = bstack11l1ll_opy_ (u"ࠢࠣ౱")
    if bstack11l1ll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ౲") in bstack1ll1l1llll_opy_ and bstack1ll1l1llll_opy_[bstack11l1ll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ౳")] != None:
      bstack1llll1lll_opy_ += bstack1ll1l1llll_opy_[bstack11l1ll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ౴")] + bstack11l1ll_opy_ (u"ࠦ࠱ࠦࠢ౵")
      if bstack1ll1l1llll_opy_[bstack11l1ll_opy_ (u"ࠬࡵࡳࠨ౶")] == bstack11l1ll_opy_ (u"ࠨࡩࡰࡵࠥ౷"):
        bstack1llll1lll_opy_ += bstack11l1ll_opy_ (u"ࠢࡪࡑࡖࠤࠧ౸")
      bstack1llll1lll_opy_ += (bstack1ll1l1llll_opy_[bstack11l1ll_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ౹")] or bstack11l1ll_opy_ (u"ࠩࠪ౺"))
      return bstack1llll1lll_opy_
    else:
      bstack1llll1lll_opy_ += bstack1llll11l_opy_(bstack1ll1l1llll_opy_[bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫ౻")]) + bstack11l1ll_opy_ (u"ࠦࠥࠨ౼") + (
              bstack1ll1l1llll_opy_[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ౽")] or bstack11l1ll_opy_ (u"࠭ࠧ౾")) + bstack11l1ll_opy_ (u"ࠢ࠭ࠢࠥ౿")
      if bstack1ll1l1llll_opy_[bstack11l1ll_opy_ (u"ࠨࡱࡶࠫಀ")] == bstack11l1ll_opy_ (u"ࠤ࡚࡭ࡳࡪ࡯ࡸࡵࠥಁ"):
        bstack1llll1lll_opy_ += bstack11l1ll_opy_ (u"࡛ࠥ࡮ࡴࠠࠣಂ")
      bstack1llll1lll_opy_ += bstack1ll1l1llll_opy_[bstack11l1ll_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨಃ")] or bstack11l1ll_opy_ (u"ࠬ࠭಄")
      return bstack1llll1lll_opy_
def bstack1ll11l111l_opy_(bstack11111l1l_opy_):
  if bstack11111l1l_opy_ == bstack11l1ll_opy_ (u"ࠨࡤࡰࡰࡨࠦಅ"):
    return bstack11l1ll_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡪࡶࡪ࡫࡮࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡪࡶࡪ࡫࡮ࠣࡀࡆࡳࡲࡶ࡬ࡦࡶࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪಆ")
  elif bstack11111l1l_opy_ == bstack11l1ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣಇ"):
    return bstack11l1ll_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡷ࡫ࡤ࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡵࡩࡩࠨ࠾ࡇࡣ࡬ࡰࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬಈ")
  elif bstack11111l1l_opy_ == bstack11l1ll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥಉ"):
    return bstack11l1ll_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡐࡢࡵࡶࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫಊ")
  elif bstack11111l1l_opy_ == bstack11l1ll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦಋ"):
    return bstack11l1ll_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡊࡸࡲࡰࡴ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨಌ")
  elif bstack11111l1l_opy_ == bstack11l1ll_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣ಍"):
    return bstack11l1ll_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࠧࡪ࡫ࡡ࠴࠴࠹࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࠩࡥࡦࡣ࠶࠶࠻ࠨ࠾ࡕ࡫ࡰࡩࡴࡻࡴ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ಎ")
  elif bstack11111l1l_opy_ == bstack11l1ll_opy_ (u"ࠤࡵࡹࡳࡴࡩ࡯ࡩࠥಏ"):
    return bstack11l1ll_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡨ࡬ࡢࡥ࡮࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡨ࡬ࡢࡥ࡮ࠦࡃࡘࡵ࡯ࡰ࡬ࡲ࡬ࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫಐ")
  else:
    return bstack11l1ll_opy_ (u"ࠫࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࠨ಑") + bstack1llll11l_opy_(
      bstack11111l1l_opy_) + bstack11l1ll_opy_ (u"ࠬࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫಒ")
def bstack1l1ll1lll_opy_(session):
  return bstack11l1ll_opy_ (u"࠭࠼ࡵࡴࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡶࡴࡽࠢ࠿࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠣࡷࡪࡹࡳࡪࡱࡱ࠱ࡳࡧ࡭ࡦࠤࡁࡀࡦࠦࡨࡳࡧࡩࡁࠧࢁࡽࠣࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥࡣࡧࡲࡡ࡯࡭ࠥࡂࢀࢃ࠼࠰ࡣࡁࡀ࠴ࡺࡤ࠿ࡽࢀࡿࢂࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽࠱ࡷࡶࡃ࠭ಓ").format(
    session[bstack11l1ll_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࡟ࡶࡴ࡯ࠫಔ")], bstack1lll1l11ll_opy_(session), bstack1ll11l111l_opy_(session[bstack11l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡴࡶࡤࡸࡺࡹࠧಕ")]),
    bstack1ll11l111l_opy_(session[bstack11l1ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩಖ")]),
    bstack1llll11l_opy_(session[bstack11l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫಗ")] or session[bstack11l1ll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫಘ")] or bstack11l1ll_opy_ (u"ࠬ࠭ಙ")) + bstack11l1ll_opy_ (u"ࠨࠠࠣಚ") + (session[bstack11l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩಛ")] or bstack11l1ll_opy_ (u"ࠨࠩಜ")),
    session[bstack11l1ll_opy_ (u"ࠩࡲࡷࠬಝ")] + bstack11l1ll_opy_ (u"ࠥࠤࠧಞ") + session[bstack11l1ll_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨಟ")], session[bstack11l1ll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧಠ")] or bstack11l1ll_opy_ (u"࠭ࠧಡ"),
    session[bstack11l1ll_opy_ (u"ࠧࡤࡴࡨࡥࡹ࡫ࡤࡠࡣࡷࠫಢ")] if session[bstack11l1ll_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬಣ")] else bstack11l1ll_opy_ (u"ࠩࠪತ"))
def bstack11ll11l11_opy_(sessions, bstack1lllll1l1_opy_):
  try:
    bstack1l1l11l11_opy_ = bstack11l1ll_opy_ (u"ࠥࠦಥ")
    if not os.path.exists(bstack1lll11lll1_opy_):
      os.mkdir(bstack1lll11lll1_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1ll_opy_ (u"ࠫࡦࡹࡳࡦࡶࡶ࠳ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩದ")), bstack11l1ll_opy_ (u"ࠬࡸࠧಧ")) as f:
      bstack1l1l11l11_opy_ = f.read()
    bstack1l1l11l11_opy_ = bstack1l1l11l11_opy_.replace(bstack11l1ll_opy_ (u"࠭ࡻࠦࡔࡈࡗ࡚ࡒࡔࡔࡡࡆࡓ࡚ࡔࡔࠦࡿࠪನ"), str(len(sessions)))
    bstack1l1l11l11_opy_ = bstack1l1l11l11_opy_.replace(bstack11l1ll_opy_ (u"ࠧࡼࠧࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠪࢃࠧ಩"), bstack1lllll1l1_opy_)
    bstack1l1l11l11_opy_ = bstack1l1l11l11_opy_.replace(bstack11l1ll_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡑࡅࡒࡋࠥࡾࠩಪ"),
                                              sessions[0].get(bstack11l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡰࡤࡱࡪ࠭ಫ")) if sessions[0] else bstack11l1ll_opy_ (u"ࠪࠫಬ"))
    with open(os.path.join(bstack1lll11lll1_opy_, bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡶࡪࡶ࡯ࡳࡶ࠱࡬ࡹࡳ࡬ࠨಭ")), bstack11l1ll_opy_ (u"ࠬࡽࠧಮ")) as stream:
      stream.write(bstack1l1l11l11_opy_.split(bstack11l1ll_opy_ (u"࠭ࡻࠦࡕࡈࡗࡘࡏࡏࡏࡕࡢࡈࡆ࡚ࡁࠦࡿࠪಯ"))[0])
      for session in sessions:
        stream.write(bstack1l1ll1lll_opy_(session))
      stream.write(bstack1l1l11l11_opy_.split(bstack11l1ll_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫರ"))[1])
    logger.info(bstack11l1ll_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵࡧࡧࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡦࡺ࡯࡬ࡥࠢࡤࡶࡹ࡯ࡦࡢࡥࡷࡷࠥࡧࡴࠡࡽࢀࠫಱ").format(bstack1lll11lll1_opy_));
  except Exception as e:
    logger.debug(bstack1ll1l11ll_opy_.format(str(e)))
def bstack1l11l1l1_opy_(bstack1l1lll1ll_opy_):
  global CONFIG
  try:
    host = bstack11l1ll_opy_ (u"ࠩࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨࠬಲ") if bstack11l1ll_opy_ (u"ࠪࡥࡵࡶࠧಳ") in CONFIG else bstack11l1ll_opy_ (u"ࠫࡦࡶࡩࠨ಴")
    user = CONFIG[bstack11l1ll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧವ")]
    key = CONFIG[bstack11l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩಶ")]
    bstack1l111ll1_opy_ = bstack11l1ll_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ಷ") if bstack11l1ll_opy_ (u"ࠨࡣࡳࡴࠬಸ") in CONFIG else bstack11l1ll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫಹ")
    url = bstack11l1ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡿࢂ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠱࡮ࡸࡵ࡮ࠨ಺").format(user, key, host, bstack1l111ll1_opy_,
                                                                                bstack1l1lll1ll_opy_)
    headers = {
      bstack11l1ll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪ಻"): bstack11l1ll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ಼"),
    }
    proxies = bstack11ll1lll_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack11l1ll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࠫಽ")], response.json()))
  except Exception as e:
    logger.debug(bstack1lll1l11l_opy_.format(str(e)))
def bstack1ll111llll_opy_():
  global CONFIG
  global bstack111l11l1l_opy_
  try:
    if bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪಾ") in CONFIG:
      host = bstack11l1ll_opy_ (u"ࠨࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧࠫಿ") if bstack11l1ll_opy_ (u"ࠩࡤࡴࡵ࠭ೀ") in CONFIG else bstack11l1ll_opy_ (u"ࠪࡥࡵ࡯ࠧು")
      user = CONFIG[bstack11l1ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ೂ")]
      key = CONFIG[bstack11l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨೃ")]
      bstack1l111ll1_opy_ = bstack11l1ll_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬೄ") if bstack11l1ll_opy_ (u"ࠧࡢࡲࡳࠫ೅") in CONFIG else bstack11l1ll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪೆ")
      url = bstack11l1ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠩೇ").format(user, key, host, bstack1l111ll1_opy_)
      headers = {
        bstack11l1ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩೈ"): bstack11l1ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ೉"),
      }
      if bstack11l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧೊ") in CONFIG:
        params = {bstack11l1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫೋ"): CONFIG[bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪೌ")], bstack11l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ್ࠫ"): CONFIG[bstack11l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ೎")]}
      else:
        params = {bstack11l1ll_opy_ (u"ࠪࡲࡦࡳࡥࠨ೏"): CONFIG[bstack11l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ೐")]}
      proxies = bstack11ll1lll_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1lll1l1111_opy_ = response.json()[0][bstack11l1ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡥࡹ࡮ࡲࡤࠨ೑")]
        if bstack1lll1l1111_opy_:
          bstack1lllll1l1_opy_ = bstack1lll1l1111_opy_[bstack11l1ll_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪ೒")].split(bstack11l1ll_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࠭ࡣࡷ࡬ࡰࡩ࠭೓"))[0] + bstack11l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡳ࠰ࠩ೔") + bstack1lll1l1111_opy_[
            bstack11l1ll_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬೕ")]
          logger.info(bstack1l11ll11_opy_.format(bstack1lllll1l1_opy_))
          bstack111l11l1l_opy_ = bstack1lll1l1111_opy_[bstack11l1ll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ೖ")]
          bstack1l1lllll1_opy_ = CONFIG[bstack11l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ೗")]
          if bstack11l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ೘") in CONFIG:
            bstack1l1lllll1_opy_ += bstack11l1ll_opy_ (u"࠭ࠠࠨ೙") + CONFIG[bstack11l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ೚")]
          if bstack1l1lllll1_opy_ != bstack1lll1l1111_opy_[bstack11l1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭೛")]:
            logger.debug(bstack1l11l1lll_opy_.format(bstack1lll1l1111_opy_[bstack11l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ೜")], bstack1l1lllll1_opy_))
          return [bstack1lll1l1111_opy_[bstack11l1ll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ೝ")], bstack1lllll1l1_opy_]
    else:
      logger.warn(bstack11lll1l1_opy_)
  except Exception as e:
    logger.debug(bstack1111llll1_opy_.format(str(e)))
  return [None, None]
def bstack1ll11l1lll_opy_(url, bstack1lll1111ll_opy_=False):
  global CONFIG
  global bstack11ll1ll1_opy_
  if not bstack11ll1ll1_opy_:
    hostname = bstack1ll11ll1l1_opy_(url)
    is_private = bstack111l1l11_opy_(hostname)
    if (bstack11l1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨೞ") in CONFIG and not bstack1l1lll11l_opy_(CONFIG[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ೟")])) and (is_private or bstack1lll1111ll_opy_):
      bstack11ll1ll1_opy_ = hostname
def bstack1ll11ll1l1_opy_(url):
  return urlparse(url).hostname
def bstack111l1l11_opy_(hostname):
  for bstack1l1l111l1_opy_ in bstack1111l111_opy_:
    regex = re.compile(bstack1l1l111l1_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack11ll11l1l_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack11lll1l1l_opy_
  if not bstack11ll11ll1_opy_.bstack1lll111l1l_opy_(CONFIG, bstack11lll1l1l_opy_):
    logger.warning(bstack11l1ll_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤೠ"))
    return {}
  try:
    results = driver.execute_script(bstack11l1ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡳ࡫ࡷࠡࡒࡵࡳࡲ࡯ࡳࡦࠪࡩࡹࡳࡩࡴࡪࡱࡱࠤ࠭ࡸࡥࡴࡱ࡯ࡺࡪ࠲ࠠࡳࡧ࡭ࡩࡨࡺࠩࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡵࡽࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡹࡴࠡࡧࡹࡩࡳࡺࠠ࠾ࠢࡱࡩࡼࠦࡃࡶࡵࡷࡳࡲࡋࡶࡦࡰࡷࠬࠬࡇ࠱࠲࡛ࡢࡘࡆࡖ࡟ࡈࡇࡗࡣࡗࡋࡓࡖࡎࡗࡗࠬ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡩࡲࠥࡃࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࠫࡩࡻ࡫࡮ࡵࠫࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡷ࡫࡭ࡰࡸࡨࡉࡻ࡫࡮ࡵࡎ࡬ࡷࡹ࡫࡮ࡦࡴࠫࠫࡆ࠷࠱࡚ࡡࡕࡉࡘ࡛ࡌࡕࡕࡢࡖࡊ࡙ࡐࡐࡐࡖࡉࠬ࠲ࠠࡧࡰࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡳࡰ࡮ࡹࡩ࠭࡫ࡶࡦࡰࡷ࠲ࡩ࡫ࡴࡢ࡫࡯࠲ࡩࡧࡴࡢࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡦࡪࡤࡆࡸࡨࡲࡹࡒࡩࡴࡶࡨࡲࡪࡸࠨࠨࡃ࠴࠵࡞ࡥࡒࡆࡕࡘࡐ࡙࡙࡟ࡓࡇࡖࡔࡔࡔࡓࡆࠩ࠯ࠤ࡫ࡴࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡩ࡯ࡳࡱࡣࡷࡧ࡭ࡋࡶࡦࡰࡷࠬࡪࡼࡥ࡯ࡶࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠥࡩࡡࡵࡥ࡫ࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨ࡮ࡪࡩࡴࠩࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠎࠥࠦࠠࠡࠢࠣࠤࠥࢃࠩ࠼ࠌࠣࠤࠥࠦࠢࠣࠤೡ"))
    return results
  except Exception:
    logger.error(bstack11l1ll_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡽࡥࡳࡧࠣࡪࡴࡻ࡮ࡥ࠰ࠥೢ"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack11lll1l1l_opy_
  if not bstack11ll11ll1_opy_.bstack1lll111l1l_opy_(CONFIG, bstack11lll1l1l_opy_):
    logger.warning(bstack11l1ll_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽ࠳ࠨೣ"))
    return {}
  try:
    bstack1l1lllll11_opy_ = driver.execute_script(bstack11l1ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡷࡹࡷࡴࠠ࡯ࡧࡺࠤࡕࡸ࡯࡮࡫ࡶࡩ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࠩࡴࡨࡷࡴࡲࡶࡦ࠮ࠣࡶࡪࡰࡥࡤࡶࠬࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡹࡸࡹࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡪࡼࡥ࡯ࡶࠣࡁࠥࡴࡥࡸࠢࡆࡹࡸࡺ࡯࡮ࡇࡹࡩࡳࡺࠨࠨࡃ࠴࠵࡞ࡥࡔࡂࡒࡢࡋࡊ࡚࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡕࡘࡑࡒࡇࡒ࡚ࠩࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡷࡹࠦࡦ࡯ࠢࡀࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࠨࡦࡸࡨࡲࡹ࠯ࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡴࡨࡱࡴࡼࡥࡆࡸࡨࡲࡹࡒࡩࡴࡶࡨࡲࡪࡸࠨࠨࡃ࠴࠵࡞ࡥࡒࡆࡕࡘࡐ࡙࡙࡟ࡔࡗࡐࡑࡆࡘ࡙ࡠࡔࡈࡗࡕࡕࡎࡔࡇࠪ࠰ࠥ࡬࡮ࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡸࡵ࡬ࡷࡧࠫࡩࡻ࡫࡮ࡵ࠰ࡧࡩࡹࡧࡩ࡭࠰ࡶࡹࡲࡳࡡࡳࡻࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡧࡤࡥࡇࡹࡩࡳࡺࡌࡪࡵࡷࡩࡳ࡫ࡲࠩࠩࡄ࠵࠶࡟࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡕࡘࡑࡒࡇࡒ࡚ࡡࡕࡉࡘࡖࡏࡏࡕࡈࠫ࠱ࠦࡦ࡯ࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡷࡪࡰࡧࡳࡼ࠴ࡤࡪࡵࡳࡥࡹࡩࡨࡆࡸࡨࡲࡹ࠮ࡥࡷࡧࡱࡸ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠠࡤࡣࡷࡧ࡭ࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡰࡥࡤࡶࠫ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠐࠠࠡࠢࠣࠤࠥࠦࠠࡾࠫ࠾ࠎࠥࠦࠠࠡࠤࠥࠦ೤"))
    return bstack1l1lllll11_opy_
  except Exception:
    logger.error(bstack11l1ll_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡷࡰࡱࡦࡸࡹࠡࡹࡤࡷࠥ࡬࡯ࡶࡰࡧ࠲ࠧ೥"))
    return {}