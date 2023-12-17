from fractions import Fraction
from videoscope.models.timecode import Timecode
from videoscope.interfaces.i_thumbnail_generator import IThumbnailGenerator
from videoscope.interfaces.i_video_metadata_extractor import IMetadataExtractor
from videoscope.interfaces.i_video_handler import IVideoHandler
from videoscope.errors.video_info_errors import VideoInfoErrors


class VideoInfo:
    def __init__(
        self,
        video_handler: IVideoHandler,
        audio_metadata_extractor: IMetadataExtractor,
        video_metadata_extractor: IMetadataExtractor,
        format_metadata_extractor: IMetadataExtractor,
        data_metadata_extractor: IMetadataExtractor,
        thumbnail_generator: IThumbnailGenerator,
        thumbnail_factor=0.25,
    ):
        self.video_handler = video_handler
        self.audio_metadata_extractor = audio_metadata_extractor
        self.video_metadata_extractor = video_metadata_extractor
        self.format_metadata_extractor = format_metadata_extractor
        self.data_metadata_extractor = data_metadata_extractor
        self.thumbnail_generator = thumbnail_generator
        self.video_path = None
        self.thumbnail_factor = thumbnail_factor
        self.file = None
        self.audios_metadata = []
        self.video_metadata = None
        self.data_metadata = []
        self.format_metadata = None
        self.first_frame = None
        self.thumbnail = None
        self.timecode = None
        self.__initialize_file()
        self.__initialize_video_info()

    def __initialize_file(self):
        self.file = self.video_handler.open_video()
        self._probe_data = self.video_handler.get_probe()
        self.video_path = self.video_handler.path
        self.__video_stream = next(
            (
                stream
                for stream in self._probe_data["streams"]
                if stream["codec_type"] == "video"
            ),
            None,
        )
        if self.__video_stream is None:
            raise ValueError(VideoInfoErrors.NO_VIDEO_STREAM_FOUND)

        self.__audio_streams = [
            stream
            for stream in self._probe_data["streams"]
            if stream.get("codec_type") == "audio"
        ]

        self.__data_streams = [
            stream
            for stream in self._probe_data["streams"]
            if stream.get("codec_type") == "data"
        ]

    def __initialize_video_info(self):
        try:
            self.video_metadata = self.video_metadata_extractor.extract_metadata(
                self.__video_stream
            )

            self.audios_metadata = [
                self.audio_metadata_extractor.extract_metadata(stream)
                for stream in self.__audio_streams
            ]

            self.format_metadata = self.format_metadata_extractor.extract_metadata(
                self._probe_data["format"]
            )

            self.data_metadata = [
                self.data_metadata_extractor.extract_metadata(stream)
                for stream in self.__data_streams
            ]

            self.first_frame = self.video_handler.get_first_frame(
                self.video_metadata.width, self.video_metadata.height
            )

            self.thumbnail = self.thumbnail_generator.generate_thumbnail(
                self.first_frame,
                self.thumbnail_factor,
            )

            frame_rate = None
            if self.video_metadata.r_frame_rate:
                frame_rate = float(Fraction(self.video_metadata.r_frame_rate))
            elif self.video_metadata.frame_rate:
                float(Fraction(self.video_metadata.frame_rate))

            if frame_rate and hasattr(self.format_metadata, "tags"):
                self.timecode = Timecode(
                    frame_rate,
                    self.format_metadata.tags.get("timecode", "00:00:00:00"),
                    float(self.format_metadata.duration),
                )

        finally:
            self.video_handler.close_video()

    @property
    def fps(self):
        return self.video_metadata.r_frame_rate

    @property
    def width(self):
        return self.video_metadata.width

    @property
    def height(self):
        return self.video_metadata.height

    def __str__(self) -> str:
        return f"{self.video_path}"
