# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-06 14:55:34
# @Last Modified by:   Lakshita Jain
# @Last Modified time: 2023-12-07 12:46:34


__version__ = "0.0.2a5"

from .api import GailBot
from .core.engines import Engine, Watson, WatsonAMInterface, WatsonLMInterface
from .plugins import Plugin, Methods
from .services import GBPluginMethods, UttDict, UttObj
