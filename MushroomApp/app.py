from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Load the trained model
model_path = os.path.join('models', 'best_model.pkl')
model = joblib.load(model_path)

# Feature list and possible values
feature_values = {
    'cap-shape': ['b', 'c', 'x', 'f', 'k', 's'],
    'cap-surface': ['f', 'g', 'y', 's'],
    'cap-color': ['n', 'b', 'c', 'g', 'r', 'p', 'u', 'e', 'w', 'y'],
    'bruises': ['t', 'f'],
    'odor': ['a', 'l', 'c', 'y', 'f', 'm', 'n', 'p', 's'],
    'gill-attachment': ['a', 'd', 'f', 'n'],
    'gill-spacing': ['c', 'w', 'd'],
    'gill-size': ['b', 'n'],
    'gill-color': ['k', 'n', 'b', 'h', 'g', 'r', 'o', 'p', 'u', 'e', 'w', 'y'],
    'stalk-shape': ['e', 't'],
    'stalk-root': ['b', 'c', 'u', 'e', 'z', 'r', '?'],
    'stalk-surface-above-ring': ['f', 'y', 'k', 's'],
    'stalk-surface-below-ring': ['f', 'y', 'k', 's'],
    'stalk-color-above-ring': ['n', 'b', 'c', 'g', 'o', 'p', 'e', 'w', 'y'],
    'stalk-color-below-ring': ['n', 'b', 'c', 'g', 'o', 'p', 'e', 'w', 'y'],
    'veil-type': ['p', 'u'],
    'veil-color': ['n', 'o', 'w', 'y'],
    'ring-number': ['n', 'o', 't'],
    'ring-type': ['c', 'e', 'f', 'l', 'n', 'p', 's', 'z'],
    'spore-print-color': ['k', 'n', 'b', 'h', 'r', 'o', 'u', 'w', 'y'],
    'population': ['a', 'c', 'n', 's', 'v', 'y'],
    'habitat': ['g', 'l', 'm', 'p', 'u', 'w', 'd']
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Collect user input
        input_data = {}
        for feature in feature_values.keys():
            input_data[feature] = request.form.get(feature)
        
        # Convert input data to DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        result = 'Poisonous' if prediction == 'p' else 'Edible'
        
        return render_template('result.html', prediction=result)
    else:
        return render_template('index.html', feature_values=feature_values)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
