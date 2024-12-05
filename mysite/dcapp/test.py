from transformers import LayoutLMv2ForSequenceClassification

label2idx = {
    'advertisement': 0, 
    'budget': 1, 
    'email': 2, 
    'file_folder': 3, 
    'form': 4, 
    'handwritten': 5, 
    'invoice': 6, 
    'letter': 7, 
    'memo': 8, 
    'news_article': 9, 
    'presentation': 10, 
    'questionnaire': 11, 
    'resume': 12, 
    'scientific_publication': 13, 
    'scientific_report': 14, 
    'specification': 15
}

model = LayoutLMv2ForSequenceClassification.from_pretrained(
    "microsoft/layoutlmv2-base-uncased",
    num_labels=len(label2idx),
    id2label={str(idx): label for idx, label in enumerate(label2idx.keys())},  # Correctly map indexes to labels
    label2id={label: idx for label, idx in label2idx.items()}  # Direct mapping as required
)

from transformers import LayoutLMv2ForSequenceClassification

# Load the model
loaded_model = LayoutLMv2ForSequenceClassification.from_pretrained('C:\\Users\\Kounen Fathima\\django\\mysite\\dcapp\\NEWModelDirectory')

# Check the labels
print("Label to ID:", loaded_model.config.label2id)
print("ID to Label:", loaded_model.config.id2label)
