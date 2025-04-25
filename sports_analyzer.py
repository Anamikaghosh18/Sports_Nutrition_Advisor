import os
import base64
import io
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()

# Configure the Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
 

app = Flask(__name__)


def analyze_food_image(image_data, sport_name):
    """
    Analyze sports image using Gemini model and provide recommendations

    Args:
        image_data: Binary image data or base64 encoded image string
        sport_name: Name of the sport for customized analysis

    Returns:
        Dictionary containing analysis results or error information
    """
    try:
        # Process image for Gemini
        if isinstance(image_data, str) and image_data.startswith('data:image'):
            # Handle base64 encoded image
            image_data = image_data.split(',')[1]
            image = Image.open(io.BytesIO(base64.b64decode(image_data)))
        else:
            # Handle direct binary data
            image = Image.open(io.BytesIO(image_data))

        prompt = f"""
        You are a professional nutritionist. Analyze the provided image of food and provide the following concise information:

        1. **Nutritional Breakdown**:
            - Proteins: Approximate grams
            - Carbohydrates: Approximate grams
            - Fats: Approximate grams
            - Vitamins and Minerals: Key highlights

        2. **Food Suggestions**:
            - Recommend 1-2 additional foods or ingredients to make the meal more balanced.

        3. **Personalized Recommendations**:
            - Provide 1-2 actionable tips tailored to the sport or activity: {sport_name}.

        Keep the response concise, structured, and easy to read. Avoid unnecessary details.
        """

        # Generate response with a token limit
        response = model.generate_content(
            [prompt, image],
            max_output_tokens=150 
        )
        if response and response.text: 
            return {
                "success": True,
                "analysis": response.text,
                "sport": sport_name
            }
        else:
            return {
                "success": False,
                "error": "No analysis generated", 
                "sport": sport_name
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
