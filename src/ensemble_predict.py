import os
import logging
from typing import Tuple, List
try:
    import torch
    import torch.nn.functional as F
    import timm
    from torchvision import transforms
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None
    timm = None
    transforms = None

from PIL import Image
from config import config

logger = logging.getLogger(__name__)

TARGET_CLASSES: List[str] = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy',
    'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
    'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
]


class AgriEnsemble:

    def __init__(self, model_path: str = config.ENSEMBLE_MODEL_PATH) -> None:
        self.model_path = model_path
        self.classes = TARGET_CLASSES
        self.num_classes = len(self.classes)

        if not HAS_TORCH:
            logger.warning("PyTorch/Timm dependencies not detected. Vision Ensemble operates in fallback mode.")
            self.device = None
            return

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Initializing PyTorch Vision Ensemble on device: {self.device}")

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model checkpoint file not found at: {self.model_path}")

        self._load_checkpoint()
        self._setup_transforms()

    def _load_checkpoint(self) -> None:
        try:
            checkpoint = torch.load(self.model_path, map_location=self.device)

            self.m1 = timm.create_model("efficientnet_b0", num_classes=self.num_classes).to(self.device)
            self.m2 = timm.create_model("resnet18", num_classes=self.num_classes).to(self.device)
            self.m3 = timm.create_model("mobilenetv3_large_100", num_classes=self.num_classes).to(self.device)

            self.m1.load_state_dict(checkpoint['eff_state'])
            self.m2.load_state_dict(checkpoint['res_state'])
            self.m3.load_state_dict(checkpoint['mob_state'])

            self.m1.eval()
            self.m2.eval()
            self.m3.eval()

            logger.info("Successfully loaded state dicts for EfficientNet-B0, ResNet-18, and MobileNetV3.")
        except Exception as e:
            logger.error(f"Failed to load vision ensemble checkpoint: {e}", exc_info=True)
            raise RuntimeError(f"Vision ensemble loading failed: {e}")

    def _setup_transforms(self) -> None:
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def predict(self, img_path: str) -> Tuple[str, float]:
        if not HAS_TORCH:
            logger.warning("PyTorch unavailable for image inference. Skipping vision layer.")
            return "N/A", 0.0

        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Input leaf image not found: {img_path}")

        try:
            image = Image.open(img_path).convert("RGB")
            tensor = self.transform(image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                out1 = self.m1(tensor)
                out2 = self.m2(tensor)
                out3 = self.m3(tensor)

                fused_logits = (0.40 * out1 + 0.30 * out2 + 0.30 * out3)
                probabilities = F.softmax(fused_logits, dim=1)
                confidence, pred_idx = torch.max(probabilities, dim=1)

            idx = pred_idx.item()
            conf_val = confidence.item()

            if 0 <= idx < len(self.classes):
                predicted_label = self.classes[idx]
            else:
                predicted_label = f"Unknown Disease (ID: {idx})"

            logger.info(f"Ensemble Inference Complete: '{predicted_label}' with confidence {conf_val:.4f}")
            return predicted_label, conf_val

        except Exception as e:
            logger.error(f"Image inference error on file {img_path}: {e}", exc_info=True)
            raise RuntimeError(f"Image classification failed: {e}")