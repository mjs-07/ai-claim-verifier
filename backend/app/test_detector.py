# from transformers import pipeline

# classifier = pipeline(
#     "text-classification",
#     model="ogmatrixllm/glyph-v1.1"
# )

# human_text = """
# Yesterday I missed my bus and had to walk to class.
# """

# ai_text = """
# Artificial intelligence is transforming industries worldwide by
# enhancing productivity and enabling organizations to automate
# complex workflows efficiently.
# """

# print("\nHuman Test:")
# print(classifier(human_text))

# print("\nAI Test:")
# print(classifier(ai_text))
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    "ogmatrixllm/glyph-v1.1"
)

print(model.config.id2label)