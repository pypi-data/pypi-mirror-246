# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-07-31 16:21:27
# @Last Modified by:   Lakshita Jain
# @Last Modified time: 2023-11-30 16:32:31
import os
from typing import List, Union
from .payloadObject import PayLoadObject, PayLoadStatus
from ...organizer.source import SourceObject
from typing import List, Union
from gailbot.core.utils.general import get_extension, copy
from gailbot.core.utils.media import VideoHandler
from gailbot.core.utils.media import AudioHandler
from gailbot.workspace.manager import WorkspaceManager
from gailbot.core.utils.logger import makelogger

SUPPORTED_VIDEO = ["mp4"]
logger = makelogger("videoPayload")
MERGED_FILE_NAME = "merged"


def load_video_payload(source: SourceObject, ws_manager: WorkspaceManager) -> Union[bool, List[PayLoadObject]]:
    """
    Loads an instance of the video payload with a given source object
    """
    
    if not source.setting:
        logger.info("from source.setting")
        return False
    if not VideoPayload.is_supported(source.source_path()):
        logger.info("from is_supported(...)")
        return False
    try:
        return [VideoPayload(source, ws_manager)]
    except Exception as e:
        logger.error(source.__class__)
        logger.error(e, exc_info=e)
        return False


class VideoPayload(PayLoadObject):
    def __init__(self, source: SourceObject, workspace: WorkspaceManager) -> None:
        super().__init__(source, workspace)

    @staticmethod
    def is_supported(file_path: str) -> bool:
        """
        Determines if a given file path has a supported file extension

        Args:
            file_path: str: name of the file path to check

        Returns:
            True if filepath is supported, false if not
        """
        logger.info(file_path)
        return get_extension(file_path) in SUPPORTED_VIDEO

    def _copy_file(self) -> None:
        """
        Copies file to workspace
        """
        extension = get_extension(self.original_source)
        tgt_path = os.path.join(self.workspace.data_copy, f"{self.name}.{extension}")
        copy(self.original_source, tgt_path)
        self.data_files = [tgt_path]

    def _set_initial_status(self) -> None:
        """
        Sets the initial status of the payload object to initialized
        """
        self.status = PayLoadStatus.INITIALIZED

    @staticmethod
    def supported_format() -> list[str]:
        """
        Contains and accesses a list of the supported formats
        """
        return SUPPORTED_VIDEO

    def _merge_audio(self) -> bool:
        """
        Converts video file to audio file
        """
        video_handler = VideoHandler()
        audio_handler = AudioHandler()
        source = self.data_files[0]
        videoStream = video_handler.read_file(source)
        audioStream = video_handler.extract_audio(videoStream)
        path = audio_handler.write_stream(audioStream, self.out_dir.media_file, MERGED_FILE_NAME, format="wav")
        self.merged_audio = path
        assert path



    def __repr__(self) -> str:
        return "Video payload"
