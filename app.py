from flask import Flask, render_template, request, send_from_directory, url_for, redirect
import os
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('success.html')

@app.route('/', methods=['POST'])
def upload_file():
  materia = request.form['materia']
  file = request.files['file']
  codigo_materia = request.form['codigo-materia']

  if file and materia:
    filename = f"Notas Transformadas {materia}.csv"
    
    os.makedirs("uploads", exist_ok=True)
    
    file.save(os.path.join("uploads", filename))
    
    df = pd.read_excel(os.path.join("uploads", filename))
    df.columns = ["Nom", "Ape", "Num", "Inst", "Depa", "Cues", "Ult"]
    df = df.drop(columns=["Nom", "Ape", "Inst", "Ult"])
    df.columns = ["Personal", "CursadaId", "Nota"]
    df.iloc[0:, 1] = codigo_materia
    df.replace("-", "Ausente", inplace=True)
    df.to_csv(os.path.join("uploads", filename), index=False)

    return redirect(url_for("download_file", filename=filename))

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory("uploads", filename, as_attachment=True)

if __name__ == '__main__':
  app.run(debug=True)