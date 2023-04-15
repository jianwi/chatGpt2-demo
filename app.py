import os
from flask import Flask, request, jsonify, send_from_directory
from transformers import GPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")


def generate_response(input_text):
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    output = model.generate(
        input_ids,
        max_length=50,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
    )
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response


app = Flask(__name__)


@app.route("/")
def index():
    return send_from_directory(
        os.path.abspath(os.path.dirname(__file__)), "index.html"
    )


@app.route("/chat", methods=["POST"])
def chat():
    input_text = request.json["input_text"]
    response = generate_response(input_text)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run()
