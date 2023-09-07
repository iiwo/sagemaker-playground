# Load a pre-trained model and tokenizer
from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained('t5-small')
model = T5ForConditionalGeneration.from_pretrained('t5-small')

# Save the model and tokenizer
model.save_pretrained('./t5-small')
tokenizer.save_pretrained('./t5-small')

# tar -czvf model.tar.gz -C ./t5-small .
