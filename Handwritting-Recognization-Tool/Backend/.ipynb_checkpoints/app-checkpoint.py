# # app.py
# from flask import Flask, request, jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # This will enable CORS for all routes

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'image' not in request.files:
#         return jsonify({'error': 'No file part'})
    
#     file = request.files['image']
    
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'})
    
#     if file:
#         # Assuming you have a function `generate_text_from_image` that processes the image and returns text
#         generated_text = generate_text_from_image(file)
#         return jsonify({'text': generated_text})

# def generate_text_from_image(image):
#     # Implement your image processing and text generation logic here
#     # For this example, we will return a dummy text
#     return "Generated text based on the image."

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

# Load the tokenizer and model
# model_dir = "/pytorch_model.bin"  # Update this path
# tokenizer = AutoTokenizer.from_pretrained(model_dir)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)

# # Preprocess the image
# def preprocess_image(image_path):
#     image = Image.open(image_path).convert("RGB")
#     preprocess = transforms.Compose([
#         transforms.Resize((256, 256)),  # Adjust as necessary
#         transforms.ToTensor(),
#         transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
#     ])
#     return preprocess(image).unsqueeze(0)

image_path = "Backend/Images/image.jpg"  # Update this path
image = Image.open(image_path)
image = image.convert("RGB")
# image_tensor = preprocess_image(image_path)

# # Generate text from image
# # Ensure your model accepts this input format. Some models may need different input keys.
# inputs = {"pixel_values": image_tensor}

# # Generate text
# with torch.no_grad():
#     output = model.generate(**inputs)

# # Decode the generated text
# generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
# print(generated_text)


processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')
pixel_values = processor(images=image, return_tensors="pt").pixel_values

generated_ids = model.generate(pixel_values)
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
