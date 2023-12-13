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
from bstack_utils.helper import bstack1l11l11l_opy_, bstack1lll1l111l_opy_
class bstack1ll11lll1_opy_:
  working_dir = os.getcwd()
  bstack11111l11l_opy_ = False
  config = {}
  binary_path = bstack11l1ll_opy_ (u"ࠧࠨጏ")
  bstack111l11ll11_opy_ = bstack11l1ll_opy_ (u"ࠨࠩጐ")
  bstack1l1l1l1ll1_opy_ = False
  bstack111ll1111l_opy_ = None
  bstack111lll11l1_opy_ = {}
  bstack111lll1111_opy_ = 300
  bstack111l1llll1_opy_ = False
  logger = None
  bstack111l1lll1l_opy_ = False
  bstack111lll111l_opy_ = bstack11l1ll_opy_ (u"ࠩࠪ጑")
  bstack111ll1llll_opy_ = {
    bstack11l1ll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪጒ") : 1,
    bstack11l1ll_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬጓ") : 2,
    bstack11l1ll_opy_ (u"ࠬ࡫ࡤࡨࡧࠪጔ") : 3,
    bstack11l1ll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ጕ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111l1ll1l1_opy_(self):
    bstack111l1l1l11_opy_ = bstack11l1ll_opy_ (u"ࠧࠨ጖")
    bstack111llll111_opy_ = sys.platform
    bstack111lllll11_opy_ = bstack11l1ll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ጗")
    if re.match(bstack11l1ll_opy_ (u"ࠤࡧࡥࡷࡽࡩ࡯ࡾࡰࡥࡨࠦ࡯ࡴࠤጘ"), bstack111llll111_opy_) != None:
      bstack111l1l1l11_opy_ = bstack11ll11l1ll_opy_ + bstack11l1ll_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡳࡸࡾ࠮ࡻ࡫ࡳࠦጙ")
      self.bstack111lll111l_opy_ = bstack11l1ll_opy_ (u"ࠫࡲࡧࡣࠨጚ")
    elif re.match(bstack11l1ll_opy_ (u"ࠧࡳࡳࡸ࡫ࡱࢀࡲࡹࡹࡴࡾࡰ࡭ࡳ࡭ࡷࡽࡥࡼ࡫ࡼ࡯࡮ࡽࡤࡦࡧࡼ࡯࡮ࡽࡹ࡬ࡲࡨ࡫ࡼࡦ࡯ࡦࢀࡼ࡯࡮࠴࠴ࠥጛ"), bstack111llll111_opy_) != None:
      bstack111l1l1l11_opy_ = bstack11ll11l1ll_opy_ + bstack11l1ll_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳ࡷࡪࡰ࠱ࡾ࡮ࡶࠢጜ")
      bstack111lllll11_opy_ = bstack11l1ll_opy_ (u"ࠢࡱࡧࡵࡧࡾ࠴ࡥࡹࡧࠥጝ")
      self.bstack111lll111l_opy_ = bstack11l1ll_opy_ (u"ࠨࡹ࡬ࡲࠬጞ")
    else:
      bstack111l1l1l11_opy_ = bstack11ll11l1ll_opy_ + bstack11l1ll_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯࡯࡭ࡳࡻࡸ࠯ࡼ࡬ࡴࠧጟ")
      self.bstack111lll111l_opy_ = bstack11l1ll_opy_ (u"ࠪࡰ࡮ࡴࡵࡹࠩጠ")
    return bstack111l1l1l11_opy_, bstack111lllll11_opy_
  def bstack111lllllll_opy_(self):
    try:
      bstack111l11llll_opy_ = [os.path.join(expanduser(bstack11l1ll_opy_ (u"ࠦࢃࠨጡ")), bstack11l1ll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬጢ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111l11llll_opy_:
        if(self.bstack111l11ll1l_opy_(path)):
          return path
      raise bstack11l1ll_opy_ (u"ࠨࡕ࡯ࡣ࡯ࡦࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥጣ")
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡰࡦࡴࡦࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࠲ࠦࡻࡾࠤጤ").format(e))
  def bstack111l11ll1l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111l1l11ll_opy_(self, bstack111l1l1l11_opy_, bstack111lllll11_opy_):
    try:
      bstack111l1l11l1_opy_ = self.bstack111lllllll_opy_()
      bstack111ll1lll1_opy_ = os.path.join(bstack111l1l11l1_opy_, bstack11l1ll_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮ࡻ࡫ࡳࠫጥ"))
      bstack111llll1l1_opy_ = os.path.join(bstack111l1l11l1_opy_, bstack111lllll11_opy_)
      if os.path.exists(bstack111llll1l1_opy_):
        self.logger.info(bstack11l1ll_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦጦ").format(bstack111llll1l1_opy_))
        return bstack111llll1l1_opy_
      if os.path.exists(bstack111ll1lll1_opy_):
        self.logger.info(bstack11l1ll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡽ࡭ࡵࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡻ࡮ࡻ࡫ࡳࡴ࡮ࡴࡧࠣጧ").format(bstack111ll1lll1_opy_))
        return self.bstack111ll11lll_opy_(bstack111ll1lll1_opy_, bstack111lllll11_opy_)
      self.logger.info(bstack11l1ll_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࠦࡻࡾࠤጨ").format(bstack111l1l1l11_opy_))
      response = bstack1lll1l111l_opy_(bstack11l1ll_opy_ (u"ࠬࡍࡅࡕࠩጩ"), bstack111l1l1l11_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack111ll1lll1_opy_, bstack11l1ll_opy_ (u"࠭ࡷࡣࠩጪ")) as file:
          file.write(response.content)
        self.logger.info(bstack111lll1ll1_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡥࡳࡪࠠࡴࡣࡹࡩࡩࠦࡡࡵࠢࡾࡦ࡮ࡴࡡࡳࡻࡢࡾ࡮ࡶ࡟ࡱࡣࡷ࡬ࢂࠨጫ"))
        return self.bstack111ll11lll_opy_(bstack111ll1lll1_opy_, bstack111lllll11_opy_)
      else:
        raise(bstack111lll1ll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡴࡩࡧࠣࡪ࡮ࡲࡥ࠯ࠢࡖࡸࡦࡺࡵࡴࠢࡦࡳࡩ࡫࠺ࠡࡽࡵࡩࡸࡶ࡯࡯ࡵࡨ࠲ࡸࡺࡡࡵࡷࡶࡣࡨࡵࡤࡦࡿࠥጬ"))
    except:
      self.logger.error(bstack11l1ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨጭ"))
  def bstack111lll1l1l_opy_(self, bstack111l1l1l11_opy_, bstack111lllll11_opy_):
    try:
      bstack111llll1l1_opy_ = self.bstack111l1l11ll_opy_(bstack111l1l1l11_opy_, bstack111lllll11_opy_)
      bstack111llll1ll_opy_ = self.bstack111ll1l1ll_opy_(bstack111l1l1l11_opy_, bstack111lllll11_opy_, bstack111llll1l1_opy_)
      return bstack111llll1l1_opy_, bstack111llll1ll_opy_
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡶࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡳࡥࡹ࡮ࠢጮ").format(e))
    return bstack111llll1l1_opy_, False
  def bstack111ll1l1ll_opy_(self, bstack111l1l1l11_opy_, bstack111lllll11_opy_, bstack111llll1l1_opy_, bstack111ll111l1_opy_ = 0):
    if bstack111ll111l1_opy_ > 1:
      return False
    if bstack111llll1l1_opy_ == None or os.path.exists(bstack111llll1l1_opy_) == False:
      self.logger.warn(bstack11l1ll_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡴࡦࡺࡨࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡸࡥࡵࡴࡼ࡭ࡳ࡭ࠠࡥࡱࡺࡲࡱࡵࡡࡥࠤጯ"))
      bstack111llll1l1_opy_ = self.bstack111l1l11ll_opy_(bstack111l1l1l11_opy_, bstack111lllll11_opy_)
      self.bstack111ll1l1ll_opy_(bstack111l1l1l11_opy_, bstack111lllll11_opy_, bstack111llll1l1_opy_, bstack111ll111l1_opy_+1)
    bstack111l1ll111_opy_ = bstack11l1ll_opy_ (u"ࠧࡤ࠮ࠫࡂࡳࡩࡷࡩࡹ࡝࠱ࡦࡰ࡮ࠦ࡜ࡥ࠰࡟ࡨ࠰࠴࡜ࡥ࠭ࠥጰ")
    command = bstack11l1ll_opy_ (u"࠭ࡻࡾࠢ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬጱ").format(bstack111llll1l1_opy_)
    bstack111l1l1lll_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111l1ll111_opy_, bstack111l1l1lll_opy_) != None:
      return True
    else:
      self.logger.error(bstack11l1ll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡤࡪࡨࡧࡰࠦࡦࡢ࡫࡯ࡩࡩࠨጲ"))
      bstack111llll1l1_opy_ = self.bstack111l1l11ll_opy_(bstack111l1l1l11_opy_, bstack111lllll11_opy_)
      self.bstack111ll1l1ll_opy_(bstack111l1l1l11_opy_, bstack111lllll11_opy_, bstack111llll1l1_opy_, bstack111ll111l1_opy_+1)
  def bstack111ll11lll_opy_(self, bstack111ll1lll1_opy_, bstack111lllll11_opy_):
    try:
      working_dir = os.path.dirname(bstack111ll1lll1_opy_)
      shutil.unpack_archive(bstack111ll1lll1_opy_, working_dir)
      bstack111llll1l1_opy_ = os.path.join(working_dir, bstack111lllll11_opy_)
      os.chmod(bstack111llll1l1_opy_, 0o755)
      return bstack111llll1l1_opy_
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡺࡴࡺࡪࡲࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠤጳ"))
  def bstack111l1lllll_opy_(self):
    try:
      percy = str(self.config.get(bstack11l1ll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨጴ"), bstack11l1ll_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤጵ"))).lower()
      if percy != bstack11l1ll_opy_ (u"ࠦࡹࡸࡵࡦࠤጶ"):
        return False
      self.bstack1l1l1l1ll1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢጷ").format(e))
  def bstack1l111111l_opy_(self):
    try:
      bstack1l111111l_opy_ = str(self.config.get(bstack11l1ll_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩጸ"), bstack11l1ll_opy_ (u"ࠢࡢࡷࡷࡳࠧጹ"))).lower()
      return bstack1l111111l_opy_
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻࠣࡧࡦࡶࡴࡶࡴࡨࠤࡲࡵࡤࡦ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤጺ").format(e))
  def init(self, bstack11111l11l_opy_, config, logger):
    self.bstack11111l11l_opy_ = bstack11111l11l_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111l1lllll_opy_():
      return
    self.bstack111lll11l1_opy_ = config.get(bstack11l1ll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨጻ"), {})
    self.bstack111lllll1l_opy_ = config.get(bstack11l1ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭ጼ"), bstack11l1ll_opy_ (u"ࠦࡦࡻࡴࡰࠤጽ"))
    try:
      bstack111l1l1l11_opy_, bstack111lllll11_opy_ = self.bstack111l1ll1l1_opy_()
      bstack111llll1l1_opy_, bstack111llll1ll_opy_ = self.bstack111lll1l1l_opy_(bstack111l1l1l11_opy_, bstack111lllll11_opy_)
      if bstack111llll1ll_opy_:
        self.binary_path = bstack111llll1l1_opy_
        thread = Thread(target=self.bstack111llllll1_opy_)
        thread.start()
      else:
        self.bstack111l1lll1l_opy_ = True
        self.logger.error(bstack11l1ll_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡰࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡪࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡔࡪࡸࡣࡺࠤጾ").format(bstack111llll1l1_opy_))
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢጿ").format(e))
  def bstack111ll1ll1l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11l1ll_opy_ (u"ࠧ࡭ࡱࡪࠫፀ"), bstack11l1ll_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮࡭ࡱࡪࠫፁ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11l1ll_opy_ (u"ࠤࡓࡹࡸ࡮ࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࡹࠠࡢࡶࠣࡿࢂࠨፂ").format(logfile))
      self.bstack111l11ll11_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࠦࡰࡢࡶ࡫࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦፃ").format(e))
  def bstack111llllll1_opy_(self):
    bstack111ll1l1l1_opy_ = self.bstack111l1lll11_opy_()
    if bstack111ll1l1l1_opy_ == None:
      self.bstack111l1lll1l_opy_ = True
      self.logger.error(bstack11l1ll_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯ࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠢፄ"))
      return False
    command_args = [bstack11l1ll_opy_ (u"ࠧࡧࡰࡱ࠼ࡨࡼࡪࡩ࠺ࡴࡶࡤࡶࡹࠨፅ") if self.bstack11111l11l_opy_ else bstack11l1ll_opy_ (u"࠭ࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠪፆ")]
    bstack111llll11l_opy_ = self.bstack111l1l1111_opy_()
    if bstack111llll11l_opy_ != None:
      command_args.append(bstack11l1ll_opy_ (u"ࠢ࠮ࡥࠣࡿࢂࠨፇ").format(bstack111llll11l_opy_))
    env = os.environ.copy()
    env[bstack11l1ll_opy_ (u"ࠣࡒࡈࡖࡈ࡟࡟ࡕࡑࡎࡉࡓࠨፈ")] = bstack111ll1l1l1_opy_
    bstack111l1ll11l_opy_ = [self.binary_path]
    self.bstack111ll1ll1l_opy_()
    self.bstack111ll1111l_opy_ = self.bstack111ll11l1l_opy_(bstack111l1ll11l_opy_ + command_args, env)
    self.logger.debug(bstack11l1ll_opy_ (u"ࠤࡖࡸࡦࡸࡴࡪࡰࡪࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠥፉ"))
    bstack111ll111l1_opy_ = 0
    while self.bstack111ll1111l_opy_.poll() == None:
      bstack111lll11ll_opy_ = self.bstack111lll1l11_opy_()
      if bstack111lll11ll_opy_:
        self.logger.debug(bstack11l1ll_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࠨፊ"))
        self.bstack111l1llll1_opy_ = True
        return True
      bstack111ll111l1_opy_ += 1
      self.logger.debug(bstack11l1ll_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡖࡪࡺࡲࡺࠢ࠰ࠤࢀࢃࠢፋ").format(bstack111ll111l1_opy_))
      time.sleep(2)
    self.logger.error(bstack11l1ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡆࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࢁࡽࠡࡣࡷࡸࡪࡳࡰࡵࡵࠥፌ").format(bstack111ll111l1_opy_))
    self.bstack111l1lll1l_opy_ = True
    return False
  def bstack111lll1l11_opy_(self, bstack111ll111l1_opy_ = 0):
    try:
      if bstack111ll111l1_opy_ > 10:
        return False
      bstack111ll11l11_opy_ = os.environ.get(bstack11l1ll_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤ࡙ࡅࡓࡘࡈࡖࡤࡇࡄࡅࡔࡈࡗࡘ࠭ፍ"), bstack11l1ll_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶ࠽࠹࠸࠹࠸ࠨፎ"))
      bstack111ll11ll1_opy_ = bstack111ll11l11_opy_ + bstack11ll11ll11_opy_
      response = requests.get(bstack111ll11ll1_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack111l1lll11_opy_(self):
    bstack111l1ll1ll_opy_ = bstack11l1ll_opy_ (u"ࠨࡣࡳࡴࠬፏ") if self.bstack11111l11l_opy_ else bstack11l1ll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫፐ")
    bstack11l1ll1ll1_opy_ = bstack11l1ll_opy_ (u"ࠥࡥࡵ࡯࠯ࡢࡲࡳࡣࡵ࡫ࡲࡤࡻ࠲࡫ࡪࡺ࡟ࡱࡴࡲ࡮ࡪࡩࡴࡠࡶࡲ࡯ࡪࡴ࠿࡯ࡣࡰࡩࡂࢁࡽࠧࡶࡼࡴࡪࡃࡻࡾࠤፑ").format(self.config[bstack11l1ll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩፒ")], bstack111l1ll1ll_opy_)
    uri = bstack1l11l11l_opy_(bstack11l1ll1ll1_opy_)
    try:
      response = bstack1lll1l111l_opy_(bstack11l1ll_opy_ (u"ࠬࡍࡅࡕࠩፓ"), uri, {}, {bstack11l1ll_opy_ (u"࠭ࡡࡶࡶ࡫ࠫፔ"): (self.config[bstack11l1ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩፕ")], self.config[bstack11l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫፖ")])})
      if response.status_code == 200:
        bstack111ll11111_opy_ = response.json()
        if bstack11l1ll_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣፗ") in bstack111ll11111_opy_:
          return bstack111ll11111_opy_[bstack11l1ll_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤፘ")]
        else:
          raise bstack11l1ll_opy_ (u"࡙ࠫࡵ࡫ࡦࡰࠣࡒࡴࡺࠠࡇࡱࡸࡲࡩࠦ࠭ࠡࡽࢀࠫፙ").format(bstack111ll11111_opy_)
      else:
        raise bstack11l1ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡱࡧࡵࡧࡾࠦࡴࡰ࡭ࡨࡲ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡵࡷࡥࡹࡻࡳࠡ࠯ࠣࡿࢂ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡅࡳࡩࡿࠠ࠮ࠢࡾࢁࠧፚ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡰࡳࡱ࡭ࡩࡨࡺࠢ፛").format(e))
  def bstack111l1l1111_opy_(self):
    bstack111ll1l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll_opy_ (u"ࠢࡱࡧࡵࡧࡾࡉ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠥ፜"))
    try:
      if bstack11l1ll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩ፝") not in self.bstack111lll11l1_opy_:
        self.bstack111lll11l1_opy_[bstack11l1ll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪ፞")] = 2
      with open(bstack111ll1l11l_opy_, bstack11l1ll_opy_ (u"ࠪࡻࠬ፟")) as fp:
        json.dump(self.bstack111lll11l1_opy_, fp)
      return bstack111ll1l11l_opy_
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡤࡴࡨࡥࡹ࡫ࠠࡱࡧࡵࡧࡾࠦࡣࡰࡰࡩ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ፠").format(e))
  def bstack111ll11l1l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111lll111l_opy_ == bstack11l1ll_opy_ (u"ࠬࡽࡩ࡯ࠩ፡"):
        bstack111ll111ll_opy_ = [bstack11l1ll_opy_ (u"࠭ࡣ࡮ࡦ࠱ࡩࡽ࡫ࠧ።"), bstack11l1ll_opy_ (u"ࠧ࠰ࡥࠪ፣")]
        cmd = bstack111ll111ll_opy_ + cmd
      cmd = bstack11l1ll_opy_ (u"ࠨࠢࠪ፤").join(cmd)
      self.logger.debug(bstack11l1ll_opy_ (u"ࠤࡕࡹࡳࡴࡩ࡯ࡩࠣࡿࢂࠨ፥").format(cmd))
      with open(self.bstack111l11ll11_opy_, bstack11l1ll_opy_ (u"ࠥࡥࠧ፦")) as bstack111ll1l111_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111ll1l111_opy_, text=True, stderr=bstack111ll1l111_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111l1lll1l_opy_ = True
      self.logger.error(bstack11l1ll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠥࡽࡩࡵࡪࠣࡧࡲࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨ፧").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111l1llll1_opy_:
        self.logger.info(bstack11l1ll_opy_ (u"࡙ࠧࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡑࡧࡵࡧࡾࠨ፨"))
        cmd = [self.binary_path, bstack11l1ll_opy_ (u"ࠨࡥࡹࡧࡦ࠾ࡸࡺ࡯ࡱࠤ፩")]
        self.bstack111ll11l1l_opy_(cmd)
        self.bstack111l1llll1_opy_ = False
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡵࡰࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡤࡱࡰࡱࡦࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢ፪").format(cmd, e))
  def bstack1llll111l1_opy_(self):
    if not self.bstack1l1l1l1ll1_opy_:
      return
    try:
      bstack111ll1ll11_opy_ = 0
      while not self.bstack111l1llll1_opy_ and bstack111ll1ll11_opy_ < self.bstack111lll1111_opy_:
        if self.bstack111l1lll1l_opy_:
          self.logger.info(bstack11l1ll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡦࡢ࡫࡯ࡩࡩࠨ፫"))
          return
        time.sleep(1)
        bstack111ll1ll11_opy_ += 1
      os.environ[bstack11l1ll_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡄࡈࡗ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࠨ፬")] = str(self.bstack111l1l1l1l_opy_())
      self.logger.info(bstack11l1ll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠦ፭"))
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ፮").format(e))
  def bstack111l1l1l1l_opy_(self):
    if self.bstack11111l11l_opy_:
      return
    try:
      bstack111l11lll1_opy_ = [platform[bstack11l1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ፯")].lower() for platform in self.config.get(bstack11l1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ፰"), [])]
      bstack111lll1lll_opy_ = sys.maxsize
      bstack111l1l111l_opy_ = bstack11l1ll_opy_ (u"ࠧࠨ፱")
      for browser in bstack111l11lll1_opy_:
        if browser in self.bstack111ll1llll_opy_:
          bstack111l1l1ll1_opy_ = self.bstack111ll1llll_opy_[browser]
        if bstack111l1l1ll1_opy_ < bstack111lll1lll_opy_:
          bstack111lll1lll_opy_ = bstack111l1l1ll1_opy_
          bstack111l1l111l_opy_ = browser
      return bstack111l1l111l_opy_
    except Exception as e:
      self.logger.error(bstack11l1ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡥࡩࡸࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤ፲").format(e))