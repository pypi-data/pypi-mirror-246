# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-07-31 16:21:27
# @Last Modified by:   Lakshita Jain
# @Last Modified time: 2023-12-07 12:48:19
from typing import List, Dict
from gailbot.core.utils.logger import makelogger

logger = makelogger("pluginObject")


class PluginSuiteSetObj:
    def __init__(self, plugins: Dict[str, Dict[str, List[str]]]) -> None:
        self.data = plugins

    def get_data(self) -> Dict[str, Dict[str, List[str]]]:
        return self.data