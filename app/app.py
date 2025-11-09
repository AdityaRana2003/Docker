import os
from datetime import datetime
from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

INDEX_HTML = """
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>LocalCloud</title>
<style>
  :root {
    --bg-light: #f4f6f8; --bg-dark: #1e1e2f;
    --card-light: #fff; --card-dark: #2b2b3d;
    --text-light: #333; --text-dark: #ddd;
    --accent: #3498db; --success: #27ae60; --danger: #e74c3c;
  }
  body { font-family: Arial, sans-serif; background: var(--bg-light); color: var(--text-light); margin:0; padding:0;}
  .dark { background: var(--bg-dark); color: var(--text-dark); }
  header { padding:15px 30px; background: var(--accent); color:#fff; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; }
  header h1 { margin:0; font-size:1.8em; }
  .menu { display:flex; gap:10px; align-items:center; }
  .menu button { padding:6px 12px; border:none; border-radius:5px; cursor:pointer; color:#fff; background:#2980b9; transition:0.3s; }
  .menu button:hover { background:#1f618d; }
  .container { padding:20px; max-width:1000px; margin:auto; }
  .upload-box { border: 2px dashed var(--accent); padding:30px; text-align:center; border-radius:10px; cursor:pointer; margin-bottom:20px; transition:0.3s; background:#ecf0f1;}
  .upload-box:hover { background:#d6eaf8; }
  input[type=file] { display:none; }
  .files { display:flex; flex-direction:column; gap:10px; }
  .file-item { display:flex; justify-content:space-between; align-items:center; padding:10px 15px; border-radius:8px; background:var(--card-light); box-shadow:0 2px 5px rgba(0,0,0,0.1); transition:0.2s; }
  .dark .file-item { background: var(--card-dark); }
  .file-item:hover { transform: translateY(-2px); box-shadow:0 4px 10px rgba(0,0,0,0.15);}
  .btn { padding:5px 10px; border:none; border-radius:5px; cursor:pointer; margin-left:5px; color:#fff; text-decoration:none; }
  .btn-download { background: var(--success); }
  .btn-download:hover { background:#2ecc71; }
  .btn-delete { background: var(--danger); }
  .btn-delete:hover { background:#c0392b; }
  .btn-google { background:#db4437; }
  .btn-google:hover { background:#c23321; }
  .btn-dropbox { background:#0061ff; }
  .btn-dropbox:hover { background:#004ed1; }
  .alert { padding:10px; margin-top:10px; border-radius:5px; }
  .alert-success { background: var(--success); color:#fff;}
  .alert-error { background: var(--danger); color:#fff;}
  #search { padding:5px 10px; margin-bottom:15px; width:100%; border-radius:5px; border:1px solid #ccc; }
  footer { text-align:center; padding:15px; margin-top:30px; color:#777; font-size:0.9em; }
</style>
</head>
<body>
<header>
  <h1>📂 LocalCloud</h1>
  <div class="menu">
    <button onclick="toggleTheme()">Toggle Theme</button>
    <form action="/google" method="get" style="display:inline;">
      <button type="submit" class="btn-google">Import PDF from Google Drive</button>
    </form>
    <form action="/dropbox" method="get" style="display:inline;">
      <button type="submit" class="btn-dropbox">Import PDF from Dropbox</button>
    </form>
  </div>
</header>

<div class="container">
  <div class="upload-box" onclick="document.getElementById('fileInput').click()">
    Click or drag file here to upload
    <form method="post" enctype="multipart/form-data" action="/upload">
      <input type="file" name="file" id="fileInput" onchange="this.form.submit()">
    </form>
  </div>

  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      {% for category, message in messages %}
        <div class="alert alert-{{ category }}">{{ message }}</div>
      {% endfor %}
    {% endif %}
  {% endwith %}

  <input type="text" id="search" placeholder="Search files..." onkeyup="filterFiles()">

  <div class="files" id="fileList">
    {% for f in files %}
      <div class="file-item">
        <div>
          {% if f.name.lower().endswith('.pdf') %}📄{% elif f.name.lower().endswith('.jpg') or f.name.lower().endswith('.png') %}🖼️{% elif f.name.lower().endswith('.zip') %}🗜️{% else %}📁{% endif %}
          <strong>{{f.name}}</strong> - {{f.size}} KB - {{f.date}}
        </div>
        <div>
          <a href="/files/{{f.name}}" class="btn btn-download">Download</a>
          <form action="/delete/{{f.name}}" method="post" style="display:inline;">
            <button type="submit" class="btn btn-delete">Delete</button>
          </form>
        </div>
      </div>
    {% else %}
      <p>No files uploaded yet</p>
    {% endfor %}
  </div>
</div>

<footer>LocalCloud © 2025 | Made with ❤️ by Aditya</footer>

<script>
function toggleTheme(){
  document.body.classList.toggle("dark");
}
const uploadBox = document.querySelector('.upload-box');
uploadBox.addEventListener('dragover', e=>{ e.preventDefault(); uploadBox.style.background='#d6eaf8'; });
uploadBox.addEventListener('dragleave', e=>{ e.preventDefault(); uploadBox.style.background=''; });
uploadBox.addEventListener('drop', e=>{
  e.preventDefault();
  const input = document.getElementById('fileInput');
  input.files = e.dataTransfer.files;
  input.form.submit();
});
function filterFiles(){
  let filter = document.getElementById("search").value.toLowerCase();
  let items = document.getElementById("fileList").getElementsByClassName("file-item");
  for (let i=0; i<items.length; i++){
    let txt = items[i].innerText.toLowerCase();
    items[i].style.display = txt.indexOf(filter)>-1 ? "" : "none";
  }
}
</script>
</body>
</html>
"""

@app.route("/", methods=['GET'])
def index():
    files = []
    for f in sorted(os.listdir(UPLOAD_FOLDER), key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER,x)), reverse=True):
        path = os.path.join(UPLOAD_FOLDER,f)
        files.append({
            'name': f,
            'size': round(os.path.getsize(path)/1024,2),
            'date': datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M")
        })
    return render_template_string(INDEX_HTML, files=files)

@app.route("/upload", methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash("No file selected", "error")
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename=='':
        flash("No file selected", "error")
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{filename}"
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        flash(f"'{file.filename}' uploaded successfully!", "success")
        return redirect(url_for('index'))
    else:
        flash("File type not allowed!", "error")
        return redirect(url_for('index'))

@app.route("/files/<filename>", methods=['GET'])
def uploaded_file(filename):
    filename = secure_filename(filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(path):
        flash("File not found", "error")
        return redirect(url_for('index'))
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/delete/<filename>", methods=['POST'])
def delete_file(filename):
    filename = secure_filename(filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
        flash(f"'{filename}' deleted successfully!", "success")
    else:
        flash("File not found", "error")
    return redirect(url_for('index'))

# Placeholder routes for Google Drive & Dropbox selection
@app.route("/google", methods=['GET'])
def google_drive():
    flash("Google Drive integration placeholder", "success")
    return redirect(url_for('index'))

@app.route("/dropbox", methods=['GET'])
def dropbox():
    flash("Dropbox integration placeholder", "success")
    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
