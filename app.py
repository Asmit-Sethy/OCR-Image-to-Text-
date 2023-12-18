from flask import Flask, render_template, jsonify
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from array import array
import os
from PIL import Image
import sys
import time

app = Flask(__name__)

subscription_key = "16b84dc698474310a8d187c77cf5f475"
endpoint = "https://ocrcomp123.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image')
def process_image():
    # Your image processing code here
    # This can be similar to the code you provided

    print("===== Batch Read File - remote =====")
    # Get an image with handwritten text
    remote_image_handw_text_url = "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive" \
                                "-services/Computer-vision/Images/readsample.jpg "

    # Call API with URL and raw response (allows you to get the operation location)
    recognize_handw_results = computervision_client.read(remote_image_handw_text_url, raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    operation_location_remote = recognize_handw_results.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = operation_location_remote.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results
    while True:
        get_handw_text_results = computervision_client.get_read_result(operation_id)
        if get_handw_text_results.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    # Print the detected text, line by line
    if get_handw_text_results.status == OperationStatusCodes.succeeded:
        for text_result in get_handw_text_results.analyze_result.read_results:
            for line in text_result.lines:
                print(line.text)
                print(line.bounding_box)
    print()


    # For demonstration purposes, let's return a dummy response
    response_text = "This is a dummy response from image processing."
    return jsonify({"result": response_text})

if __name__ == '__main__':
    app.run(debug=True)
