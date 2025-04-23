import os
import base64
import io
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

#Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

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
        You are a professional nutritionist. Analyze the provided image of food and provide the following information:

        1.Nutritional Breakdown:
        - List the key nutrients present in the food (e.g., proteins, carbohydrates, fats, vitamins, minerals).
        - Provide approximate content in food.

        2.Health Benefits:
        - Explain the health benefits of the food based on its nutritional content.
        
        3.Food Suggestion:
        - Recommend additional foods or ingredients to make the meal more balanced.

        4.Personalized Recommendations:
        - Provide tailored advice based on the sport or activity: {sport_name}.
        

        Format the response in clear sections with bullet points for easy readability and dont generate long answer keep it short and concise.
    """
        response = model.generate_content([prompt, image])
        
        return {
            "success": True,
            "analysis": response.text,
            "sport": sport_name
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }