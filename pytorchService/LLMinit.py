

# Initialize the tokenizer and model
PretrainedModel = 'SamLowe/roberta-base-go_emotions'

# Load model directly
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained(PretrainedModel)
model = AutoModelForSequenceClassification.from_pretrained(PretrainedModel)

