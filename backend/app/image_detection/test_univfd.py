from univfd_detector import UnivFDDetector

detector = UnivFDDetector()

result = detector.predict(
    "backend/app/image_detection/test_images/cat.jpeg"
)

print(result)