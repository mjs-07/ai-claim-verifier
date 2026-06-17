from pathlib import Path
from detector import ImageDetector

detector = ImageDetector()

image_path = (
    Path(__file__).parent
    / "test_images"
    / "cat.jpeg"
)

result = detector.predict(str(image_path))

print(result)