import openai
import os
from flask import Flask, render_template, request

app = Flask(__name__)

openai.api_key = os.environ['OPENAI_API_KEY']


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/resep', methods=['POST'])
def resep():
  # Mengambil data dari formulir
  masakan = request.form['masakan']
  jenis_masakan = request.form['jenis_masakan']
  bahan_utama = request.form['bahan_utama']
  bahan_lain1 = request.form['bahan_lain1']
  bahan_lain2 = request.form['bahan_lain2']
  bahan_lain3 = request.form['bahan_lain3']
  bahan_lain4 = request.form['bahan_lain4']
  waktu_memasak = request.form['waktu_memasak']

  # Panggil OpenAI API dan kembalikan hasil
  prompt = f"Berikan resep lengkap dengan nama, bahan-bahan dan cara membuat untuk masakan {masakan} dengan bahan utama {bahan_utama} yang dimasak dalam waktu {waktu_memasak} menit. "
  hasil = generate_resep(prompt)

  hasil = format_text(hasil)
  return render_template('resep.html', hasil=hasil, prompt=prompt)


def generate_resep(prompt):
  response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=4000,
    n=1,
    stop=None,
    temperature=0.7,
  )

  return response.choices[0].text.strip()


def format_text(hasil):
  # split the text by newline character to separate each line
  lines = hasil.split("\n")

  # extract the nama masakan
  nama_masakan = lines[0].split(": ")[1]

  # extract the bahan-bahan
  bahan_lines = []
  for line in lines[1:]:
    if line.startswith("-"):
      bahan_lines.append(line)

  # extract the cara membuat
  cara_membuat_lines = []
  for i, line in enumerate(lines):
    if line.startswith("Cara Membuat"):
      cara_membuat_start = i
      break

  cara_membuat_lines = lines[cara_membuat_start + 1:]

  # join the extracted information into the desired format
  formatted_text = f"Nama Masakan : {nama_masakan} \nBahan-bahan : \n"
  formatted_text += "\n".join(bahan_lines) + "\n"
  formatted_text += "Cara Membuat : \n"
  formatted_text += "1. " + cara_membuat_lines[0] + "\n"
  formatted_text += "\n".join(
    [f"{i}. {line}" for i, line in enumerate(cara_membuat_lines[1:], start=2)])

  return formatted_text


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
