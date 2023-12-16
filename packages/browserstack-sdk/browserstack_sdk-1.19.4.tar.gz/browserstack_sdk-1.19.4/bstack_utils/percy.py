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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack11lll1lll_opy_, bstack1lll1ll1_opy_
class bstack1l1lll1l1l_opy_:
  working_dir = os.getcwd()
  bstack11l111111_opy_ = False
  config = {}
  binary_path = bstack1lllll1l_opy_ (u"ࠬ࠭ጩ")
  bstack111llll1ll_opy_ = bstack1lllll1l_opy_ (u"࠭ࠧጪ")
  bstack1111l1ll1_opy_ = False
  bstack11l1111111_opy_ = None
  bstack111ll11lll_opy_ = {}
  bstack111lll1lll_opy_ = 300
  bstack111ll1llll_opy_ = False
  logger = None
  bstack111lll1111_opy_ = False
  bstack111ll1111l_opy_ = bstack1lllll1l_opy_ (u"ࠧࠨጫ")
  bstack111lll111l_opy_ = {
    bstack1lllll1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨጬ") : 1,
    bstack1lllll1l_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪጭ") : 2,
    bstack1lllll1l_opy_ (u"ࠪࡩࡩ࡭ࡥࠨጮ") : 3,
    bstack1lllll1l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫጯ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111ll11l11_opy_(self):
    bstack111ll11l1l_opy_ = bstack1lllll1l_opy_ (u"ࠬ࠭ጰ")
    bstack111l1l111l_opy_ = sys.platform
    bstack111lll11l1_opy_ = bstack1lllll1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬጱ")
    if re.match(bstack1lllll1l_opy_ (u"ࠢࡥࡣࡵࡻ࡮ࡴࡼ࡮ࡣࡦࠤࡴࡹࠢጲ"), bstack111l1l111l_opy_) != None:
      bstack111ll11l1l_opy_ = bstack11ll11lll1_opy_ + bstack1lllll1l_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡱࡶࡼ࠳ࢀࡩࡱࠤጳ")
      self.bstack111ll1111l_opy_ = bstack1lllll1l_opy_ (u"ࠩࡰࡥࡨ࠭ጴ")
    elif re.match(bstack1lllll1l_opy_ (u"ࠥࡱࡸࡽࡩ࡯ࡾࡰࡷࡾࡹࡼ࡮࡫ࡱ࡫ࡼࢂࡣࡺࡩࡺ࡭ࡳࢂࡢࡤࡥࡺ࡭ࡳࢂࡷࡪࡰࡦࡩࢁ࡫࡭ࡤࡾࡺ࡭ࡳ࠹࠲ࠣጵ"), bstack111l1l111l_opy_) != None:
      bstack111ll11l1l_opy_ = bstack11ll11lll1_opy_ + bstack1lllll1l_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡼ࡯࡮࠯ࡼ࡬ࡴࠧጶ")
      bstack111lll11l1_opy_ = bstack1lllll1l_opy_ (u"ࠧࡶࡥࡳࡥࡼ࠲ࡪࡾࡥࠣጷ")
      self.bstack111ll1111l_opy_ = bstack1lllll1l_opy_ (u"࠭ࡷࡪࡰࠪጸ")
    else:
      bstack111ll11l1l_opy_ = bstack11ll11lll1_opy_ + bstack1lllll1l_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭࡭࡫ࡱࡹࡽ࠴ࡺࡪࡲࠥጹ")
      self.bstack111ll1111l_opy_ = bstack1lllll1l_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧጺ")
    return bstack111ll11l1l_opy_, bstack111lll11l1_opy_
  def bstack111l1l1lll_opy_(self):
    try:
      bstack111l1lllll_opy_ = [os.path.join(expanduser(bstack1lllll1l_opy_ (u"ࠤࢁࠦጻ")), bstack1lllll1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪጼ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111l1lllll_opy_:
        if(self.bstack111l1l1l1l_opy_(path)):
          return path
      raise bstack1lllll1l_opy_ (u"࡚ࠦࡴࡡ࡭ࡤࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣጽ")
    except Exception as e:
      self.logger.error(bstack1lllll1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡻࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠰ࠤࢀࢃࠢጾ").format(e))
  def bstack111l1l1l1l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111lllll11_opy_(self, bstack111ll11l1l_opy_, bstack111lll11l1_opy_):
    try:
      bstack111l1l1111_opy_ = self.bstack111l1l1lll_opy_()
      bstack11l111111l_opy_ = os.path.join(bstack111l1l1111_opy_, bstack1lllll1l_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࢀࡩࡱࠩጿ"))
      bstack111llll1l1_opy_ = os.path.join(bstack111l1l1111_opy_, bstack111lll11l1_opy_)
      if os.path.exists(bstack111llll1l1_opy_):
        self.logger.info(bstack1lllll1l_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡥࡱࡺࡲࡱࡵࡡࡥࠤፀ").format(bstack111llll1l1_opy_))
        return bstack111llll1l1_opy_
      if os.path.exists(bstack11l111111l_opy_):
        self.logger.info(bstack1lllll1l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡻ࡫ࡳࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡹࡳࢀࡩࡱࡲ࡬ࡲ࡬ࠨፁ").format(bstack11l111111l_opy_))
        return self.bstack111ll1l11l_opy_(bstack11l111111l_opy_, bstack111lll11l1_opy_)
      self.logger.info(bstack1lllll1l_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡳࡱࡰࠤࢀࢃࠢፂ").format(bstack111ll11l1l_opy_))
      response = bstack1lll1ll1_opy_(bstack1lllll1l_opy_ (u"ࠪࡋࡊ࡚ࠧፃ"), bstack111ll11l1l_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack11l111111l_opy_, bstack1lllll1l_opy_ (u"ࠫࡼࡨࠧፄ")) as file:
          file.write(response.content)
        self.logger.info(bstack111ll1lll1_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡣࡱࡨࠥࡹࡡࡷࡧࡧࠤࡦࡺࠠࡼࡤ࡬ࡲࡦࡸࡹࡠࡼ࡬ࡴࡤࡶࡡࡵࡪࢀࠦፅ"))
        return self.bstack111ll1l11l_opy_(bstack11l111111l_opy_, bstack111lll11l1_opy_)
      else:
        raise(bstack111ll1lll1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪ࠴ࠠࡔࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠿ࠦࡻࡳࡧࡶࡴࡴࡴࡳࡦ࠰ࡶࡸࡦࡺࡵࡴࡡࡦࡳࡩ࡫ࡽࠣፆ"))
    except:
      self.logger.error(bstack1lllll1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦፇ"))
  def bstack111l1ll11l_opy_(self, bstack111ll11l1l_opy_, bstack111lll11l1_opy_):
    try:
      bstack111llll1l1_opy_ = self.bstack111lllll11_opy_(bstack111ll11l1l_opy_, bstack111lll11l1_opy_)
      bstack111l1ll1ll_opy_ = self.bstack111lll1ll1_opy_(bstack111ll11l1l_opy_, bstack111lll11l1_opy_, bstack111llll1l1_opy_)
      return bstack111llll1l1_opy_, bstack111l1ll1ll_opy_
    except Exception as e:
      self.logger.error(bstack1lllll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡱࡣࡷ࡬ࠧፈ").format(e))
    return bstack111llll1l1_opy_, False
  def bstack111lll1ll1_opy_(self, bstack111ll11l1l_opy_, bstack111lll11l1_opy_, bstack111llll1l1_opy_, bstack111llll111_opy_ = 0):
    if bstack111llll111_opy_ > 1:
      return False
    if bstack111llll1l1_opy_ == None or os.path.exists(bstack111llll1l1_opy_) == False:
      self.logger.warn(bstack1lllll1l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡶࡪࡺࡲࡺ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢፉ"))
      bstack111llll1l1_opy_ = self.bstack111lllll11_opy_(bstack111ll11l1l_opy_, bstack111lll11l1_opy_)
      self.bstack111lll1ll1_opy_(bstack111ll11l1l_opy_, bstack111lll11l1_opy_, bstack111llll1l1_opy_, bstack111llll111_opy_+1)
    bstack111l1l1l11_opy_ = bstack1lllll1l_opy_ (u"ࠥࡢ࠳࠰ࡀࡱࡧࡵࡧࡾࡢ࠯ࡤ࡮࡬ࠤࡡࡪ࠮࡝ࡦ࠮࠲ࡡࡪࠫࠣፊ")
    command = bstack1lllll1l_opy_ (u"ࠫࢀࢃࠠ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪፋ").format(bstack111llll1l1_opy_)
    bstack111lll11ll_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111l1l1l11_opy_, bstack111lll11ll_opy_) != None:
      return True
    else:
      self.logger.error(bstack1lllll1l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡧࡩ࡭ࡧࡧࠦፌ"))
      bstack111llll1l1_opy_ = self.bstack111lllll11_opy_(bstack111ll11l1l_opy_, bstack111lll11l1_opy_)
      self.bstack111lll1ll1_opy_(bstack111ll11l1l_opy_, bstack111lll11l1_opy_, bstack111llll1l1_opy_, bstack111llll111_opy_+1)
  def bstack111ll1l11l_opy_(self, bstack11l111111l_opy_, bstack111lll11l1_opy_):
    try:
      working_dir = os.path.dirname(bstack11l111111l_opy_)
      shutil.unpack_archive(bstack11l111111l_opy_, working_dir)
      bstack111llll1l1_opy_ = os.path.join(working_dir, bstack111lll11l1_opy_)
      os.chmod(bstack111llll1l1_opy_, 0o755)
      return bstack111llll1l1_opy_
    except Exception as e:
      self.logger.error(bstack1lllll1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡸࡲࡿ࡯ࡰࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢፍ"))
  def bstack111lllllll_opy_(self):
    try:
      percy = str(self.config.get(bstack1lllll1l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ፎ"), bstack1lllll1l_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢፏ"))).lower()
      if percy != bstack1lllll1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢፐ"):
        return False
      self.bstack1111l1ll1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1lllll1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧፑ").format(e))
  def bstack111lll1l11_opy_(self):
    try:
      bstack111lll1l11_opy_ = str(self.config.get(bstack1lllll1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧፒ"), bstack1lllll1l_opy_ (u"ࠧࡧࡵࡵࡱࠥፓ"))).lower()
      return bstack111lll1l11_opy_
    except Exception as e:
      self.logger.error(bstack1lllll1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹࠡࡥࡤࡴࡹࡻࡲࡦࠢࡰࡳࡩ࡫ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢፔ").format(e))
  def init(self, bstack11l111111_opy_, config, logger):
    self.bstack11l111111_opy_ = bstack11l111111_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111lllllll_opy_():
      return
    self.bstack111ll11lll_opy_ = config.get(bstack1lllll1l_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ፕ"), {})
    self.bstack111ll111ll_opy_ = config.get(bstack1lllll1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫፖ"), bstack1lllll1l_opy_ (u"ࠤࡤࡹࡹࡵࠢፗ"))
    try:
      bstack111ll11l1l_opy_, bstack111lll11l1_opy_ = self.bstack111ll11l11_opy_()
      bstack111llll1l1_opy_, bstack111l1ll1ll_opy_ = self.bstack111l1ll11l_opy_(bstack111ll11l1l_opy_, bstack111lll11l1_opy_)
      if bstack111l1ll1ll_opy_:
        self.binary_path = bstack111llll1l1_opy_
        thread = Thread(target=self.bstack11l1111l11_opy_)
        thread.start()
      else:
        self.bstack111lll1111_opy_ = True
        self.logger.error(bstack1lllll1l_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡵ࡫ࡲࡤࡻࠣࡴࡦࡺࡨࠡࡨࡲࡹࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡒࡨࡶࡨࡿࠢፘ").format(bstack111llll1l1_opy_))
    except Exception as e:
      self.logger.error(bstack1lllll1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧፙ").format(e))
  def bstack11l11111ll_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1lllll1l_opy_ (u"ࠬࡲ࡯ࡨࠩፚ"), bstack1lllll1l_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࡲ࡯ࡨࠩ፛"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1lllll1l_opy_ (u"ࠢࡑࡷࡶ࡬࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࡷࠥࡧࡴࠡࡽࢀࠦ፜").format(logfile))
      self.bstack111llll1ll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1lllll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡫ࡴࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࠤࡵࡧࡴࡩ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤ፝").format(e))
  def bstack11l1111l11_opy_(self):
    bstack111lll1l1l_opy_ = self.bstack111l1l11ll_opy_()
    if bstack111lll1l1l_opy_ == None:
      self.bstack111lll1111_opy_ = True
      self.logger.error(bstack1lllll1l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠧ፞"))
      return False
    command_args = [bstack1lllll1l_opy_ (u"ࠥࡥࡵࡶ࠺ࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠦ፟") if self.bstack11l111111_opy_ else bstack1lllll1l_opy_ (u"ࠫࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠨ፠")]
    bstack111ll1l1ll_opy_ = self.bstack111l1lll1l_opy_()
    if bstack111ll1l1ll_opy_ != None:
      command_args.append(bstack1lllll1l_opy_ (u"ࠧ࠳ࡣࠡࡽࢀࠦ፡").format(bstack111ll1l1ll_opy_))
    env = os.environ.copy()
    env[bstack1lllll1l_opy_ (u"ࠨࡐࡆࡔࡆ࡝ࡤ࡚ࡏࡌࡇࡑࠦ።")] = bstack111lll1l1l_opy_
    bstack111l1lll11_opy_ = [self.binary_path]
    self.bstack11l11111ll_opy_()
    self.bstack11l1111111_opy_ = self.bstack111ll1l1l1_opy_(bstack111l1lll11_opy_ + command_args, env)
    self.logger.debug(bstack1lllll1l_opy_ (u"ࠢࡔࡶࡤࡶࡹ࡯࡮ࡨࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠣ፣"))
    bstack111llll111_opy_ = 0
    while self.bstack11l1111111_opy_.poll() == None:
      bstack111ll1l111_opy_ = self.bstack111ll1ll1l_opy_()
      if bstack111ll1l111_opy_:
        self.logger.debug(bstack1lllll1l_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠦ፤"))
        self.bstack111ll1llll_opy_ = True
        return True
      bstack111llll111_opy_ += 1
      self.logger.debug(bstack1lllll1l_opy_ (u"ࠤࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡔࡨࡸࡷࡿࠠ࠮ࠢࡾࢁࠧ፥").format(bstack111llll111_opy_))
      time.sleep(2)
    self.logger.error(bstack1lllll1l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡋࡧࡩ࡭ࡧࡧࠤࡦ࡬ࡴࡦࡴࠣࡿࢂࠦࡡࡵࡶࡨࡱࡵࡺࡳࠣ፦").format(bstack111llll111_opy_))
    self.bstack111lll1111_opy_ = True
    return False
  def bstack111ll1ll1l_opy_(self, bstack111llll111_opy_ = 0):
    try:
      if bstack111llll111_opy_ > 10:
        return False
      bstack111ll11111_opy_ = os.environ.get(bstack1lllll1l_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡗࡊࡘࡖࡆࡔࡢࡅࡉࡊࡒࡆࡕࡖࠫ፧"), bstack1lllll1l_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡲ࡯ࡤࡣ࡯࡬ࡴࡹࡴ࠻࠷࠶࠷࠽࠭፨"))
      bstack111ll1ll11_opy_ = bstack111ll11111_opy_ + bstack11ll11llll_opy_
      response = requests.get(bstack111ll1ll11_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack111l1l11ll_opy_(self):
    bstack111llllll1_opy_ = bstack1lllll1l_opy_ (u"࠭ࡡࡱࡲࠪ፩") if self.bstack11l111111_opy_ else bstack1lllll1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ፪")
    bstack11ll11l111_opy_ = bstack1lllll1l_opy_ (u"ࠣࡣࡳ࡭࠴ࡧࡰࡱࡡࡳࡩࡷࡩࡹ࠰ࡩࡨࡸࡤࡶࡲࡰ࡬ࡨࡧࡹࡥࡴࡰ࡭ࡨࡲࡄࡴࡡ࡮ࡧࡀࡿࢂࠬࡴࡺࡲࡨࡁࢀࢃࠢ፫").format(self.config[bstack1lllll1l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ፬")], bstack111llllll1_opy_)
    uri = bstack11lll1lll_opy_(bstack11ll11l111_opy_)
    try:
      response = bstack1lll1ll1_opy_(bstack1lllll1l_opy_ (u"ࠪࡋࡊ࡚ࠧ፭"), uri, {}, {bstack1lllll1l_opy_ (u"ࠫࡦࡻࡴࡩࠩ፮"): (self.config[bstack1lllll1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ፯")], self.config[bstack1lllll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ፰")])})
      if response.status_code == 200:
        bstack111lllll1l_opy_ = response.json()
        if bstack1lllll1l_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨ፱") in bstack111lllll1l_opy_:
          return bstack111lllll1l_opy_[bstack1lllll1l_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢ፲")]
        else:
          raise bstack1lllll1l_opy_ (u"ࠩࡗࡳࡰ࡫࡮ࠡࡐࡲࡸࠥࡌ࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾࠩ፳").format(bstack111lllll1l_opy_)
      else:
        raise bstack1lllll1l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡶࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡳࡵࡣࡷࡹࡸࠦ࠭ࠡࡽࢀ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡃࡱࡧࡽࠥ࠳ࠠࡼࡿࠥ፴").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1lllll1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡵࡸ࡯࡫ࡧࡦࡸࠧ፵").format(e))
  def bstack111l1lll1l_opy_(self):
    bstack111l1llll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1lllll1l_opy_ (u"ࠧࡶࡥࡳࡥࡼࡇࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠣ፶"))
    try:
      if bstack1lllll1l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ፷") not in self.bstack111ll11lll_opy_:
        self.bstack111ll11lll_opy_[bstack1lllll1l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ፸")] = 2
      with open(bstack111l1llll1_opy_, bstack1lllll1l_opy_ (u"ࠨࡹࠪ፹")) as fp:
        json.dump(self.bstack111ll11lll_opy_, fp)
      return bstack111l1llll1_opy_
    except Exception as e:
      self.logger.error(bstack1lllll1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡩࡲࡦࡣࡷࡩࠥࡶࡥࡳࡥࡼࠤࡨࡵ࡮ࡧ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤ፺").format(e))
  def bstack111ll1l1l1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111ll1111l_opy_ == bstack1lllll1l_opy_ (u"ࠪࡻ࡮ࡴࠧ፻"):
        bstack111l1ll111_opy_ = [bstack1lllll1l_opy_ (u"ࠫࡨࡳࡤ࠯ࡧࡻࡩࠬ፼"), bstack1lllll1l_opy_ (u"ࠬ࠵ࡣࠨ፽")]
        cmd = bstack111l1ll111_opy_ + cmd
      cmd = bstack1lllll1l_opy_ (u"࠭ࠠࠨ፾").join(cmd)
      self.logger.debug(bstack1lllll1l_opy_ (u"ࠢࡓࡷࡱࡲ࡮ࡴࡧࠡࡽࢀࠦ፿").format(cmd))
      with open(self.bstack111llll1ll_opy_, bstack1lllll1l_opy_ (u"ࠣࡣࠥᎀ")) as bstack111ll11ll1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111ll11ll1_opy_, text=True, stderr=bstack111ll11ll1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111lll1111_opy_ = True
      self.logger.error(bstack1lllll1l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠣࡻ࡮ࡺࡨࠡࡥࡰࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᎁ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111ll1llll_opy_:
        self.logger.info(bstack1lllll1l_opy_ (u"ࠥࡗࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡖࡥࡳࡥࡼࠦᎂ"))
        cmd = [self.binary_path, bstack1lllll1l_opy_ (u"ࠦࡪࡾࡥࡤ࠼ࡶࡸࡴࡶࠢᎃ")]
        self.bstack111ll1l1l1_opy_(cmd)
        self.bstack111ll1llll_opy_ = False
    except Exception as e:
      self.logger.error(bstack1lllll1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡳࡵࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧᎄ").format(cmd, e))
  def bstack11lll1ll_opy_(self):
    if not self.bstack1111l1ll1_opy_:
      return
    try:
      bstack111l1l1ll1_opy_ = 0
      while not self.bstack111ll1llll_opy_ and bstack111l1l1ll1_opy_ < self.bstack111lll1lll_opy_:
        if self.bstack111lll1111_opy_:
          self.logger.info(bstack1lllll1l_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤ࡫ࡧࡩ࡭ࡧࡧࠦᎅ"))
          return
        time.sleep(1)
        bstack111l1l1ll1_opy_ += 1
      os.environ[bstack1lllll1l_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡂࡆࡕࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭ᎆ")] = str(self.bstack111l1ll1l1_opy_())
      self.logger.info(bstack1lllll1l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠤᎇ"))
    except Exception as e:
      self.logger.error(bstack1lllll1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᎈ").format(e))
  def bstack111l1ll1l1_opy_(self):
    if self.bstack11l111111_opy_:
      return
    try:
      bstack111llll11l_opy_ = [platform[bstack1lllll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᎉ")].lower() for platform in self.config.get(bstack1lllll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᎊ"), [])]
      bstack111ll111l1_opy_ = sys.maxsize
      bstack111l1l11l1_opy_ = bstack1lllll1l_opy_ (u"ࠬ࠭ᎋ")
      for browser in bstack111llll11l_opy_:
        if browser in self.bstack111lll111l_opy_:
          bstack11l11111l1_opy_ = self.bstack111lll111l_opy_[browser]
        if bstack11l11111l1_opy_ < bstack111ll111l1_opy_:
          bstack111ll111l1_opy_ = bstack11l11111l1_opy_
          bstack111l1l11l1_opy_ = browser
      return bstack111l1l11l1_opy_
    except Exception as e:
      self.logger.error(bstack1lllll1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡣࡧࡶࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᎌ").format(e))