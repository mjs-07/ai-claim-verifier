from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

print("Loading Flan-T5 Small...")

tokenizer = AutoTokenizer.from_pretrained(
    "google/flan-t5-small"
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    "google/flan-t5-small"
)

print("Model Loaded!")

text = """
The Earth revolves around the Sun.
I think astronomy is fascinating.
Water boils at 100 degrees Celsius at sea level.
"""

prompt = f"""
Extract only factual claims from the text.

Text:
{text}

Claims:
"""

inputs = tokenizer(
    prompt,
    return_tensors="pt"
)

outputs = model.generate(
    **inputs,
    max_new_tokens=100
)

result = tokenizer.decode(
    outputs[0],
    skip_special_tokens=True
)

print("\nResult:")
print(result)