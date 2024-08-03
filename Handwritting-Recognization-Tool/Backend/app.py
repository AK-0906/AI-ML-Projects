from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

app = Flask(__name__)
CORS(app)  

def load_model_and_processor(model_path='./saved_model'):
    processor = TrOCRProcessor.from_pretrained(model_path)
    model = VisionEncoderDecoderModel.from_pretrained(model_path)
    return processor, model

def predict(image, model_path='./saved_model'):
    processor, model = load_model_and_processor(model_path)
    
    # Load the image
    Final_image = Image.open(image).convert("RGB")
    
    # Process the image
    pixel_values = processor(images=Final_image, return_tensors="pt").pixel_values
    
    # Generate text from image
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    return generated_text

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        # Assuming you have a function `generate_text_from_image` that processes the image and returns text
        generated_text = predict(file)
        return jsonify({'text': generated_text})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

