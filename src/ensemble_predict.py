import torch
import timm
from torchvision import transforms
from PIL import Image

class AgriEnsemble:
    def __init__(self, model_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        checkpoint = torch.load(model_path, map_location=self.device)
        
    
        self.classes = [
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

        num_classes_in_checkpoint = 38 
        print(f"[AI] Initializing Ensemble for {num_classes_in_checkpoint} classes...")

    
        self.m1 = timm.create_model("efficientnet_b0", num_classes=num_classes_in_checkpoint).to(self.device)
        self.m2 = timm.create_model("resnet18", num_classes=num_classes_in_checkpoint).to(self.device)
        self.m3 = timm.create_model("mobilenetv3_large_100", num_classes=num_classes_in_checkpoint).to(self.device)

        
        self.m1.load_state_dict(checkpoint['eff_state'])
        self.m2.load_state_dict(checkpoint['res_state'])
        self.m3.load_state_dict(checkpoint['mob_state'])
        
        self.m1.eval(); self.m2.eval(); self.m3.eval()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)), 
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def predict(self, img_path):
        img = Image.open(img_path).convert("RGB")
        img_t = self.transform(img).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            p1 = self.m1(img_t)
            p2 = self.m2(img_t)
            p3 = self.m3(img_t)
            
            
            final = (0.4 * p1 + 0.3 * p2 + 0.3 * p3)
            prob = torch.nn.functional.softmax(final, dim=1)
            conf, pred = torch.max(prob, 1)
            
        try:
            name = self.classes[pred.item()]
        except IndexError:
            name = f"Unknown Disease (ID: {pred.item()})"
            
        return name, conf.item()