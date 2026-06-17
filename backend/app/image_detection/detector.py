from PIL import Image

from backend.app.image_detection.univfd_detector import UnivFDDetector


class ImageDetector:

    def __init__(self):

        print("Image Detector Initialized")

        self.univfd = UnivFDDetector()

    def predict(self, image_path):

        image = Image.open(image_path)

        width, height = image.size
        image_format = image.format

        probability = self.univfd.predict(image_path)

        classification = (
            "AI Generated"
            if probability > 0.5
            else "Human Generated"
        )

        return {
            "classification": classification,
            "ai_probability": round(probability * 100, 2),
            "width": width,
            "height": height,
            "format": image_format
        }