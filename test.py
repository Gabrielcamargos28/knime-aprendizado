from flask import Flask, request, jsonify
import pandas as pd
from pypmml import Model

app = Flask(__name__)

# Carregar o modelo PMML
model_path = 'mlpPmml.pmml'
model = Model.load(model_path)

@app.route('/')
def index():
    return '''
        <form action="/predict" method="post">
            <label for="Gender">Gender:</label>
            <input type="number" id="Gender" name="Gender" step="1" min="0" max="1" required><br>
            <label for="Married">Married:</label>
            <input type="number" id="Married" name="Married" step="1" min="0" max="1" required><br>
            <label for="Dependents">Dependents:</label>
            <input type="number" id="Dependents" name="Dependents" step="1" min="0" max="1" required><br>
            <label for="Education">Education:</label>
            <input type="number" id="Education" name="Education" step="1" min="0" max="1" required><br>
            <label for="Self_Employed">Self Employed:</label>
            <input type="number" id="Self_Employed" name="Self_Employed" step="1" min="0" max="1" required><br>
            <label for="ApplicantIncome">Applicant Income:</label>
            <input type="number" id="ApplicantIncome" name="ApplicantIncome" step="0.01" required><br>
            <label for="LoanAmount">Loan Amount:</label>
            <input type="number" id="LoanAmount" name="LoanAmount" step="0.01" required><br>
            <label for="Loan_Amount_Term">Loan Amount Term:</label>
            <input type="number" id="Loan_Amount_Term" name="Loan_Amount_Term" step="0.01" required><br>
            <label for="Credit_History">Credit History:</label>
            <input type="number" id="Credit_History" name="Credit_History" step="0.01" required><br>
            <label for="Property_Area">Property Area:</label>
            <input type="number" id="Property_Area" name="Property_Area" step="0.01" required><br>
            <input type="submit" value="Submit">
        </form>
    '''

@app.route('/predict', methods=['POST'])
def predict():
    # Receber dados do formulário
    data = request.form.to_dict()
    
    # Converter os dados em um DataFrame do pandas
    df = pd.DataFrame([data])
    
    # Fazer a previsão usando o modelo PMML
    results = model.predict(df)
    
    # Extrair a previsão e converter para JSON
    predictions = results['Loan_Status']
    
    # Retornar as previsões como resposta
    return jsonify({"Loan_Status": predictions.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
