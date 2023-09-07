from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch


def model_fn(model_dir):
    """
    Load the T5 model.
    """
    model = T5ForConditionalGeneration.from_pretrained(model_dir)
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    return {'model': model, 'tokenizer': tokenizer}


def input_fn(request_body, content_type):
    """
    Preprocess the input data.
    """
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    input_text = request_body
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    return input_ids


def predict_fn(input_data, model_artifacts):
    """
    Generate text using the model.
    """
    model = model_artifacts['model']
    with torch.no_grad():
        output = model.generate(input_data, max_length=100)
    return output


def output_fn(prediction_output, accept):
    """
    Post-process the model's prediction.
    """
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    generated_text = tokenizer.decode(prediction_output[0], skip_special_tokens=True)
    return generated_text
