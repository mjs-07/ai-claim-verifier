import torch
from PIL import Image
from torchvision import transforms
import sys

# Add UnivFD repo to path
sys.path.append(
    r"D:\Projects\AI-claim-verifier\UniversalFakeDetect\UniversalFakeDetect"
)

from models.imagenet_models import ImagenetModel
from models.clip_models import CLIPModel


class UnivFDDetector:

    def __init__(self):

        print("Loading UnivFD...")


        self.model = CLIPModel("ViT-L/14")

        state_dict = torch.load(
            r"D:\Projects\AI-claim-verifier\UniversalFakeDetect\UniversalFakeDetect\pretrained_weights\fc_weights.pth",
            map_location="cpu"
        )

        self.model.fc.load_state_dict(state_dict)

        self.model.eval()

        self.transform = transforms.Compose([
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            ),
        ])

        print("Model Loaded")

    def predict(self, image_path):

        image = Image.open(image_path).convert("RGB")

        image = self.transform(image)

        image = image.unsqueeze(0)

        with torch.no_grad():

            output = self.model(image)

            probability = torch.sigmoid(
                output
            ).item()

        return probability