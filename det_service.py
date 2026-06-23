from ..core.openocr_manager import ocr_manager
from ..utils.numpy_utils import convert
from ..services.file_validator import validate_image_path


## Service Wrappers for OCR manager
def run_det(image_path: str):

    image_path = validate_image_path(image_path)

    result = ocr_manager.det(image_path=image_path)

    return convert(result) 