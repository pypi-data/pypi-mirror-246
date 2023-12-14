# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-08 12:43:29
# @Last Modified by:   Lakshita Jain
# @Last Modified time: 2023-11-30 16:53:18

from typing import Dict, Any, List
import torch
import multiprocessing
from ..engine import Engine
from .core import WhisperCore
from gailbot.core.utils.general import get_extension
from gailbot.configs import whisper_config_loader
from gailbot.core.utils.logger import makelogger

logger = makelogger("Whisper Engine")

WHISPER_CONFIG = whisper_config_loader()


class WhisperEngine(Engine):
    def __init__(self):
        self.core = WhisperCore()
        self._successful = False

    def __str__(self):
        """
        Returns the name of the function
        """
        return WHISPER_CONFIG.engine_name

    def __repr__(self):
        """
        Returns all the configurations and additional metadata
        """
        return self.core.__repr__()

    def transcribe(
        self,
        audio_path: str,
        language: str = None,
        detect_speakers: bool = False,
        payload_workspace: str = None,
    ) -> List[Dict]:
        """
        Use the engine to transcribe an item
        Args:
            audio_path (str) :
                path to audio file that will be transcribed
            language_customization_id (str) :
                ID of the custom acoustic model
            detet_speakers (bool) :
                specification of whether engine should detect speakers
        """
        results = self.core.transcribe(audio_path, language, detect_speakers)
        self._successful = True
        return results

    def was_transcription_successful(self) -> bool:
        """
        Return true if transcription was successful, false otherwise.
        """
        return self._successful

    def get_engine_name(self) -> str:
        """
        Obtain the name of the current engine.

        Returns:
            (str): Name of the engine.
        """
        return WHISPER_CONFIG.engine_name

    def get_supported_formats(self) -> List[str]:
        """
        Obtain a list of audio file formats that are supported.

        Returns:
            (List[str]): Supported audio file formats.
        """
        return self.core.get_supported_formats()

    def is_file_supported(self, filepath: str) -> bool:
        """
        Determine if the given file is supported by the engine.

        Args:
            file_path (str)

        Returns:
            (bool): True if file is supported. False otherwise.
        """
        return get_extension(filepath) in self.get_supported_formats()

    def get_available_models(self) -> List[str]:
        """
        Return the list of available models

        Returns:
            (List[str]): Avaible models
        """
        return self.core.get_available_models()
