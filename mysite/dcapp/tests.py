from django.test import TestCase

# Create your tests here.
from transformers import LayoutLMv2ForTokenClassification, LayoutLMv2Config

# First, define the configuration for your model if you have specific configurations
# Adjust the number of labels (num_labels) based on your model's classification task
config = LayoutLMv2Config.from_pretrained('microsoft/layoutlmv2-base-uncased', num_labels=16)

# Instantiate the model with this configuration
model = LayoutLMv2ForTokenClassification(config)
import torch

# Load the state dictionary from your .pt file
model.load_state_dict(torch.load('C:\Users\\Kounen Fathima\\django\\mysite\\dcapp\\model\\model.pt.'))
