import os
from flask import Flask, request, jsonify
import replicate

os.environ["REPLICATE_API_TOKEN"] = "01c6df94ecaf955997fd6cb0ad0ab00eead53f47"

# Initialize Flask app
app = Flask(__name__)

# Define endpoint for receiving messages
@app.route('/chat', methods=['POST'])
def chat():
    # Get the message from the request
    message = request.json['message']

    # Prompts
    pre_prompt = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    prompt_input = message

    # Generate LLM response
    output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5',
                           input={
                               "prompt": f"{pre_prompt} {prompt_input} Assistant: ",
                               "temperature": 0.1,
                               "top_p": 0.9,
                               "max_length": 128,
                               "repetition_penalty": 1
                           })

    # Extract the response from the output
    full_response = ""
    for item in output:
        full_response += item

    # Return the response as JSON
    return jsonify({'response': full_response})

# Run the Flask app
if __name__ == '__main__':
    app.run()