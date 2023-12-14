import dataclasses

from .abstract import ApiClass


@dataclasses.dataclass
class ParsingConfig(ApiClass):
    escape: str = dataclasses.field(default='"')
    csv_delimiter: str = dataclasses.field(default=None)
    file_path_with_schema: str = dataclasses.field(default=None)


@dataclasses.dataclass
class DocumentProcessingConfig(ApiClass):
    extract_bounding_boxes: bool = False
    convert_to_markdown: bool = False
    remove_header_footer: bool = False
    use_doctr: bool = False
    remove_watermarks: bool = None
    use_full_ocr: bool = None
    layout_analysis: bool = False
    enhanced_layout_detection: bool = False
    enhanced_layout_detection_v2: bool = False
    extract_tables_to_markdown: bool = False
