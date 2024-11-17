from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Path to your Excel file
excel_file_path = 'stdname.xlsx'

# Load the Excel file into a pandas DataFrame
def load_data():
    df = pd.read_excel(excel_file_path)
    return df

# Route for the Dashboard
@app.route('/')
@app.route('/dashboard')
def dashboard():
    df = load_data()
    # Convert DataFrame to a list of dictionaries to pass to the template
    data = df.to_dict(orient='records')
    return render_template('dashboard.html', data=data)

# Route for the Admin page
@app.route('/admin')
def admin():
    df = load_data()
    # Convert DataFrame to a list of dictionaries to pass to the template
    data = df.to_dict(orient='records')
    return render_template('admin.html', data=data)

# Route for updating the payment status from the Admin page
@app.route('/update_payment/<int:index>', methods=['GET', 'POST'])
def update_payment(index):
    df = load_data()
    if request.method == 'POST':
        # Update the payment status of the student
        status = request.form.get('status')
        df.at[index, 'สถานะ'] = status
        # Save the updated DataFrame back to Excel
        df.to_excel(excel_file_path, index=False)
        return redirect(url_for('admin'))

    # Show the current student data for editing
    student = df.iloc[index]
    return render_template('update_payment.html', student=student, index=index)

if __name__ == "__main__":
    app.run(debug=True)
