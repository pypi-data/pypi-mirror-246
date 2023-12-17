from videoinfo.models.metadata import Metadata
from videoinfo.interfaces.i_video_metadata_extractor import IMetadataExtractor


class MetadataExtractor(IMetadataExtractor):
    def extract_metadata(self, metadata_dict):
        return Metadata(metadata_dict)


