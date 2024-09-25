from flask import Flask, request, jsonify
from datetime import datetime

from prediction import predict_model
from log import create_logger

logger = create_logger(__name__)

today = datetime.now().strftime('%Y%m%d')


# define application

app = Flask(__name__)


# paths

@app.route('/analysis', methods=['POST'])
def doc_analysis():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    # file extraction
    file = request.files['file']
    logger.info(f"Document name: {file.filename}")

    if file.filename == '':
        message = "No file selected."
        logger.error(message)
        return jsonify({"ERROR": message}), 400

    # prediction
    try:
        result, prob = predict_model(file)
        logger.info("Prediction done successfully.")
        return jsonify({"result": result, 
                        "probability": max(prob)}), 200
    except Exception as e:
        logger.error(str(e))
        return jsonify({"ERROR": str(e)}), 400
    

#start application

if __name__ == '__main__':
    logger.info("Starting application.")
    app.run(debug=False, host="0.0.0.0", port=80)
    # app.run(debug=True, host="localhost", port=5000)