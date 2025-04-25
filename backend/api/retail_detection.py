from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import os
import numpy as np

# CLIP init model
parent_dir = os.path.dirname(os.path.abspath(__file__))
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

RETAIL_CATEGORIES = [
    # High-value Items
    "electronics", "smartphone", "laptop", "tablet", "headphones", "airpods",
    "camera", "smartwatch", "gaming console", "jewelry",
    
    # Clothing and Accessories
    "designer clothing", "luxury handbag", "expensive shoes", "sunglasses",
    "wallet", "backpack",
    
    # Store Areas
    "cash register", "checkout counter", "store entrance", "store exit",
    "security camera", "store shelf", "display case",
    
    # Suspicious Activities
    "person concealing item", "group of people", "shopping cart",
    "security tag", "price tag", "receipt"
]

def get_retail_detection(image):
    """
    Detect retail-specific items and suspicious activities in image.
    
    Args:
        image: PIL Image object or path to image file
    
    Returns:
        dict: Contains detection results with confidence scores
    """
    if isinstance(image, str):
        image = Image.open(image)
    
    # Prepare image for CLIP
    inputs = clip_processor(
        images=image,
        text=RETAIL_CATEGORIES,
        return_tensors="pt",
        padding=True
    )
    
    # Get model predictions
    with torch.no_grad():
        outputs = clip_model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)
    
    # Process results
    results = []
    for category, confidence in zip(RETAIL_CATEGORIES, probs[0].tolist()):
        if confidence > 0.1:  # Only include results with >10% confidence
            results.append({
                "category": category,
                "confidence": round(confidence, 3)
            })
    
    # Sort by confidence
    results.sort(key=lambda x: x["confidence"], reverse=True)
    
    return {
        "detections": results
    }

class TensorVector:
    def __init__(self, tensor):
        self.tensor = tensor
    
    def cosineSim(self, other):
        return torch.nn.functional.cosine_similarity(
            self.tensor.unsqueeze(0),
            other.tensor.unsqueeze(0)
        ).item()

def get_image_embedding(image):
    """
    Get CLIP embedding for an image.
    
    Args:
        image: PIL Image object or path to image file
    
    Returns:
        TensorVector: Image embedding
    """
    if isinstance(image, str):
        image = Image.open(image)
    
    inputs = clip_processor(images=image, return_tensors="pt")
    
    with torch.no_grad():
        image_features = clip_model.get_image_features(**inputs)
        
    # Normalize the features
    image_features = image_features / image_features.norm(dim=-1, keepdim=True)
    
    return TensorVector(image_features[0])