from flask import Flask, request, render_template
from pypmml import Model

app = Flask(__name__)

# Carregar o modelo PMML
model = Model.load('mlpPmml.pmml')

# Valores mínimos e máximos para normalização (conforme os dados fornecidos)
min_values = {
    'Gender': 0,
    'Married': 0,
    'Dependents': 0,
    'Education': 0,
    'Self_Employed': 0,
    'ApplicantIncome': 1500,  # Exemplo de valor mínimo
    'LoanAmount': 100,        # Exemplo de valor mínimo
    'Loan_Amount_Term': 12,   # Exemplo de valor mínimo
    'Credit_History': 0,
    'Property_Area': 0
}

max_values = {
    'Gender': 1,
    'Married': 1,
    'Dependents': 3,
    'Education': 1,
    'Self_Employed': 1,
    'ApplicantIncome': 80000,  # Exemplo de valor máximo
    'LoanAmount': 700,         # Exemplo de valor máximo
    'Loan_Amount_Term': 360,   # Exemplo de valor máximo
    'Credit_History': 1,
    'Property_Area': 2
}

def normalize_value(value, min_val, max_val):
    """
    Normaliza um valor usando valores mínimos e máximos fornecidos.
    :param value: O valor a ser normalizado.
    :param min_val: O valor mínimo para normalização.
    :param max_val: O valor máximo para normalização.
    :return: O valor normalizado.
    """
    if max_val - min_val == 0:
        return 0  # Evitar divisão por zero
    return (value - min_val) / (max_val - min_val)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Coletar dados do formulário e converter para float
            data = {
                'Gender': float(request.form.get('gender', 0)),
                'Married': float(request.form.get('married', 0)),
                'Dependents': float(request.form.get('dependents', 0)),
                'Education': float(request.form.get('education', 0)),
                'Self_Employed': float(request.form.get('self_employed', 0)),
                'ApplicantIncome': float(request.form.get('applicant_income', min_values['ApplicantIncome'])),
                'LoanAmount': float(request.form.get('loan_amount', min_values['LoanAmount'])),
                'Loan_Amount_Term': float(request.form.get('loan_amount_term', min_values['Loan_Amount_Term'])),
                'Credit_History': float(request.form.get('credit_history', 0)),
                'Property_Area': float(request.form.get('property_area', 0))
            }

            # Normalizar dados
            normalized_data = {key: normalize_value(value, min_values.get(key, 0), max_values.get(key, 1)) for key, value in data.items()}
            
            print(normalized_data)  # Para debug
            # Fazer a previsão usando o modelo PMML
            prediction = model.predict(normalized_data)

            # Obter os valores específicos
            predicted_Loan_Status = prediction.get('predicted_Loan_Status')
            probability_Y = prediction.get('probability_Y')
            probability_N = prediction.get('probability_N')
            
            print('Dados:', data)  # Para debug
            print('predict', prediction)

            # Passar os valores para o template
            return render_template('result.html', 
                                   probability_Y=probability_Y, 
                                   probability_N=probability_N, 
                                   predicted_Loan_Status=predicted_Loan_Status)

        except Exception as e:
            print(f'Erro: {e}')
            return "Ocorreu um erro ao processar os dados."

    return render_template('index.html')

@app.route('/result', methods=['GET'])
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
