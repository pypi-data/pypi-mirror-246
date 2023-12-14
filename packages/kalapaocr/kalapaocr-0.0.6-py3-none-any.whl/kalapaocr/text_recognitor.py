import json
from typing import *

import numpy as np

from kalapaocr.recognize import OcrEngine
from kalapaocr.tool.postprocess import (
    hard_postprocess,
    parser_geo_json,
    postprocess_ocr_with_keywords,
    postprocess_privince,
)


class TextRecognitor:
    def __init__(
        self,
        cnn_path,
        encoder_path,
        decoder_path,
        vocab=None,
        street_json_path=None,
        debug=False,
        log_dir=None,
    ):
        if vocab is None:
            vocab = "aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ0123456789!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ "
        self.text_recogition = OcrEngine(
            cnn_path,
            encoder_path,
            decoder_path,
            vocab=vocab,
            debug=debug,
            log_dir=log_dir,
        )
        self.data_parser = parser_geo_json(street_parser_path=street_json_path)

    def __call__(self, image: np.ndarray) -> str:
        """Input list cropped line image and rectangle coordinates perspective
        Output List Dictionary object contains ocr result with live level and word level

        :param image: line image
        :type image: np.ndarray
        :return: ocr result
        :rtype: str
        """
        res = self.text_recogition(
            img=image, image_height=64, image_max_width=1200, image_min_width=32
        )
        res = postprocess_ocr_with_keywords(res)
        res = hard_postprocess(res)
        res = postprocess_privince(res, self.data_parser)
        res = hard_postprocess(res)
        return res
