import os
import base64
import io
import logging
from flask import Flask, request, jsonify, render_template
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, static_folder='static')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sports-analyzer-secret-key')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

#  Gemini  model
model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_food_image(image_data, sport_name):
    try:
        if isinstance(image_data, str) and image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
            image = Image.open(io.BytesIO(base64.b64decode(image_data)))
        else:
            image = Image.open(io.BytesIO(image_data))
        
        # prompt for the gemini to understand 
        prompt = f"""
        Analyze this food image and provide:
        1. An estimation of the nutrients present in the food item in dictionary format
          e.g. {'carbohydrates': ,
                'protein': , 'carbs': ,
                 'fat': }
        2. Healthy / Not Healthy 
        3. Suggest some food items that can be consumed before or after playing {sport_name} in a table format. 

        Format the response in clear sections.
        """
        
        # Generate response from Gemini model
        response = model.generate_content([prompt, image])
        
        return {
            "success": True,
            "analysis": response.text,
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])

def analyze():
    try:
        if 'image' not in request.files:
            return jsonify({"success": False, "error": "No image uploaded"})
        
        image_file = request.files['image']
        sport_name = request.form.get('sport', '').strip()
        
        if not sport_name:
            return jsonify({"success": False, "error": "Sport name is required"})
        
      
        image_data = image_file.read()
        result = analyze_food_image(image_data, sport_name)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)