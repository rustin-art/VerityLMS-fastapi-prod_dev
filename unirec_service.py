from ..core.openocr_manager import ocr_manager
from ..utils.numpy_utils import convert


## Service Wrappers for OCR manager
def run_unirec(image_path: str):
    output = ocr_manager.unirec(image_path=image_path)

    if isinstance(output, tuple):
        result = output[0]
    else:
        result = output

    return convert(result)