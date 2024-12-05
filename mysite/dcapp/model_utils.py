from PIL import Image
import torch
from transformers import LayoutLMv2Processor, LayoutLMv2ForSequenceClassification
import torchvision.transforms as transforms
# Ensure these are initialized somewhere in your application,
# e.g., during startup or as a part of the module's initialization
# Define the model directory
model_directory = r'C:\\Users\\Kounen Fathima\\django\\mysite\\dcapp\\NEWModelDirectory'

# Load the processor and model
processor = LayoutLMv2Processor.from_pretrained(model_directory)
model = LayoutLMv2ForSequenceClassification.from_pretrained(model_directory)
model.eval()  # Set the model to evaluation mode if not already done

# It's generally a good practice to map your device placement at the beginning.
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Dictionary mapping model output labels to human-readable labels
idx2label = {
    0: 'advertisement', 
    1: 'budget', 
    2: 'email', 
    3: 'file_folder', 
    4: 'form', 
    5: 'handwritten', 
    6: 'invoice', 
    7: 'letter', 
    8: 'memo', 
    9: 'news_article', 
    10: 'presentation', 
    11: 'questionnaire', 
    12: 'resume', 
    13: 'scientific_publication', 
    14: 'scientific_report', 
    15: 'specification'
}

from transformers import LayoutLMv2Processor

def load_and_preprocess_image(image_file):
    try:
        image = Image.open(image_file).convert('RGB')
        # Assuming the use of a LayoutLMv2Processor that you already have loaded
        encoded_inputs = processor(images=image, return_tensors="pt", truncation=True, max_length=512)
        return encoded_inputs
    except Exception as e:
        print(f"Failed to load and preprocess image: {e}")
        return None


def predict(encoded_inputs):
    if encoded_inputs is None:
        print("No inputs to process.")
        return None

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)  # Ensure the model is on the correct device

    try:
        # Adjust this to your model's needs, such as adding attention masks
        inputs = {k: v.to(device) for k, v in encoded_inputs.items()}
        model.eval()
        with torch.no_grad():
            outputs = model(**inputs)
            predictions = torch.argmax(outputs.logits, dim=-1)
            predicted_class = idx2label[predictions.item()]
        return predicted_class
    except Exception as e:
        print(f"Error during model prediction: {str(e)}")
        return None

