from openocr import OpenOCR


class SafeOpenOCR:
    def __init__(self, model):
        self.model = model

    def __call__(self, *args, **kwargs):
        output = self.model(*args, **kwargs)

        if isinstance(output, (tuple, list)):
            return output[0]

        return output

class OpenOCRManager:

    def __init__(self):

        self.det = OpenOCR(
            task="det",
            backend="onnx",
            use_gpu="auto",
        )

        self.ocr = OpenOCR(
            task="ocr",
            mode="mobile",
            backend="onnx",
            use_gpu="auto",
        )

        self.doc = OpenOCR(
            task="doc",
            use_gpu="auto",
            auto_download=True,
        )

        self.unirec = OpenOCR(
            task="unirec",
            use_gpu="auto",
            auto_download=True,
        )


ocr_manager = OpenOCRManager()