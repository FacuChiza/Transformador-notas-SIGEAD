from flask import Flask, render_template, request, send_from_directory, url_for, redirect
import os
import pandas as pd

app = Flask(__name__)

def redondear_dig_dec(num):
  try:
    num = round(num, 0)
    return int(num)
  except:
    return "Ausente"

def redondear_dig(num):
  try:
    if float(num) >= 10.01 :
        return int(round(num / 10 ,0))    
    else:
        return num
  except ValueError:
    return "Ausente"
  
@app.route('/')
def index():
  return render_template('success.html')

@app.route('/', methods=['POST'])
def upload_file():
  materia = request.form['materia']
  file = request.files['file']
  codigo_materia = request.form['codigo-materia']

  if file and materia:
    filename = f"Archivo Transformado {materia}.csv"
    
    os.makedirs("uploads", exist_ok=True)
    file.save(os.path.join("uploads", filename))
    df = pd.read_excel(os.path.join("uploads", filename))
    df.columns = ["Nom", "Ape", "Num", "Inst", "Depa", "Cues", "Ult"]
    df = df.drop(columns=["Nom", "Ape", "Inst", "Ult"])
    df.columns = ["Personal", "CursadaId", "Nota"]
    df["Nota"] = df["Nota"].apply(redondear_dig_dec)
    df["Nota"] = df["Nota"].apply(redondear_dig)
    df.iloc[0:, 1] = codigo_materia    
    df.to_csv(os.path.join("uploads", filename), index=False)

    return redirect(url_for("download_file", filename=filename))

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory("uploads", filename, as_attachment=True)

@app.errorhandler(Exception)
def error_handler(error):
    imagen_url = url_for('static', filename='static/css/images/ejemplo.png')
    return render_template('error.html', error_message=str(error), imagen_url=imagen_url)

if __name__ == '__main__':
  app.run(debug=True)