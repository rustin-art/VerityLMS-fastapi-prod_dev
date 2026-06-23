from ..core.openocr_manager import ocr_manager
from ..utils.numpy_utils import convert



## Service Wrappers for OCR manager
def run_doc(image_path: str):

    result = ocr_manager.doc(
        image_path=image_path
    )

    return convert(result) 