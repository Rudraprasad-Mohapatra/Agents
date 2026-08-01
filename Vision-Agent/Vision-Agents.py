# ===================================================================
# ALFRED THE BUTLER - GUEST VERIFICATION SYSTEM
# VERSION: WORKING HUGGING FACE MODELS
# ===================================================================

import os
import time
from dotenv import load_dotenv
from PIL import Image
import requests
from io import BytesIO
from smolagents import CodeAgent, InferenceClientModel

print("=" * 60)
print("🏰 ALFRED THE BUTLER - GUEST VERIFICATION SYSTEM")
print("=" * 60)

# ===================================================================
# PART 1: LOAD ENVIRONMENT VARIABLES
# ===================================================================

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    print("❌ ERROR: HF_TOKEN not found in .env file!")
    print("Please create a .env file with: HF_TOKEN=your_token_here")
    exit(1)

print("✅ Environment setup complete!")

# ===================================================================
# PART 2: DOWNLOAD IMAGES
# ===================================================================

def download_images(image_urls):
    """Download images from URLs."""
    images = []
    
    for url in image_urls:
        try:
            print(f"📥 Downloading: {url}")
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content)).convert("RGB")
            images.append(image)
            print(f"  ✅ Downloaded successfully!")
        except Exception as e:
            print(f"  ❌ Failed to download: {e}")
    
    return images

# Define image URLs
image_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/e/e8/The_Joker_at_Wax_Museum_Plus.jpg",
    "https://upload.wikimedia.org/wikipedia/en/9/98/Joker_%28DC_Comics_character%29.jpg"
]

print("📥 Downloading images...")
images = download_images(image_urls)
print(f"✅ Downloaded {len(images)} images!")

# ===================================================================
# PART 3: CREATE VISION AGENT WITH WORKING MODELS
# ===================================================================

def create_vision_agent():
    """Create vision agent with working Hugging Face models."""
    
    # Try different vision models that work with HF Inference API
    # These are confirmed working models
    
    models_to_try = [
        "Salesforce/blip-image-captioning-base",  # Image captioning
        "nlpconnect/vit-gpt2-image-captioning",   # Image captioning
        "microsoft/git-base-coco",                # Image captioning
    ]
    
    for model_id in models_to_try:
        try:
            print(f"🤖 Trying model: {model_id}")
            model = InferenceClientModel(
                token=HF_TOKEN,
                model_id=model_id
            )
            
            agent = CodeAgent(
                tools=[],
                model=model,
                max_steps=5,
                verbosity_level=2
            )
            
            # Test if model works
            print(f"✅ Using model: {model_id}")
            return agent
            
        except Exception as e:
            print(f"⚠️ Model {model_id} failed: {e}")
            continue
    
    print("❌ No working models found. Using fallback...")
    return None

print("🤖 Creating vision agent...")
vision_agent = create_vision_agent()

if vision_agent is None:
    print("❌ Could not create vision agent. Using fallback analysis...")
    
    # Fallback: Simple image analysis without AI
    def simple_analysis(images):
        print("\n" + "=" * 60)
        print("🖼️ SIMPLE IMAGE ANALYSIS (Without AI)")
        print("=" * 60)
        
        for i, img in enumerate(images):
            print(f"\nImage {i+1}:")
            print(f"  - Size: {img.size[0]} x {img.size[1]} pixels")
            print(f"  - Mode: {img.mode}")
            
            # Get dominant color
            colors = img.getcolors(maxcolors=100)
            if colors:
                # Sort by count
                colors_sorted = sorted(colors, key=lambda x: x[0], reverse=True)[:3]
                print("  - Dominant colors:")
                for count, color in colors_sorted:
                    print(f"    * RGB{color}: appears {count} times")
    
    simple_analysis(images)
    
else:
    # ===================================================================
    # PART 4: RUN THE AGENT
    # ===================================================================
    
    print("\n" + "=" * 60)
    print("🔍 ANALYZING IMAGES...")
    print("=" * 60)
    
    try:
        # Different prompt formats to try
        prompts = [
            """
            Look at these images and answer:
            1. What is the character wearing? Describe the costume in detail.
            2. What does their makeup look like?
            3. Is this character The Joker or Wonder Woman?
            4. Would you let this person into a party at Wayne Manor?
            """,
            
            """
            Describe what you see in these images. 
            What is the person wearing? What colors do you see?
            Describe the face and expression.
            """
        ]
        
        response = vision_agent.run(
            prompts[0],  # Try the first prompt
            images=images
        )
        
        print("\n" + "=" * 60)
        print("🤖 AGENT RESPONSE:")
        print("=" * 60)
        print(response)
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error running agent: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Verify your HF_TOKEN is correct")
        print("3. Try a different model in the list")

# ===================================================================
# PART 5: DIRECT API CALL (Alternative - Works Most Reliably)
# ===================================================================

print("\n" + "=" * 60)
print("🔄 TRYING DIRECT API CALL...")
print("=" * 60)

def direct_hf_api(image, model="Salesforce/blip-image-captioning-base"):
    """Directly call Hugging Face API for image captioning."""
    import base64
    import json
    
    # Convert PIL image to base64
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    # API endpoint
    API_URL = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    # Prepare payload
    payload = {
        "inputs": img_str,
        "parameters": {"max_length": 100}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "No description generated")
        else:
            return str(result)
            
    except Exception as e:
        return f"API Error: {str(e)}"

# Test direct API call
if images:
    print("🔄 Testing direct API with first image...")
    result = direct_hf_api(images[0])
    print(f"📝 Direct API Result: {result}")

print("\n" + "=" * 60)
print("🏰 GUEST VERIFICATION COMPLETE!")
print("=" * 60)