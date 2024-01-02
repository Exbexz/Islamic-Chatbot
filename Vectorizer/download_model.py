from transformers import AutoModelForSequenceClassification, AutoTokenizer


model_name = input("Model name:") # Replace with your model name

# Download the model
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

path_to_save_model = "\\{model_name}"
path_to_save_tokenizer = "\\{model_name}"

print("Saving to", path_to_save_model)
# Save the model and tokenizer (optional)
model.save_pretrained(path_to_save_model)
tokenizer.save_pretrained(path_to_save_tokenizer)
