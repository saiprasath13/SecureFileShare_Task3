import os
from pathlib import Path
import pkgutil

# ---- FIX for pkgutil.get_loader missing (Python 3.14 + Flask issue) ----
if not hasattr(pkgutil, "get_loader"):
    import importlib.util

    def get_loader(name):
        try:
            return importlib.util.find_spec(name)
        except (ValueError, ImportError):
            # For __main__ or anything weird, just return None
            return None

    pkgutil.get_loader = get_loader
# ------------------------------------------------------------------------

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
    flash,
)
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet

# Base paths
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "files"
UPLOAD_FOLDER.mkdir(exist_ok=True)

# Key generation / loading
KEY_PATH = BASE_DIR / "secret.key"
if KEY_PATH.exists():
    key = KEY_PATH.read_bytes()
else:
    key = Fernet.generate_key()
    KEY_PATH.write_bytes(key)

fernet = Fernet(key)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.secret_key = "super-secret-key-change-this"


def encrypt_file(filepath: Path) -> str:
    """Encrypt file in place and return encrypted filename."""
    data = filepath.read_bytes()
    encrypted = fernet.encrypt(data)

    enc_path = filepath.with_suffix(filepath.suffix + ".enc")
    enc_path.write_bytes(encrypted)

    # remove original clear file
    filepath.unlink(missing_ok=True)
    return enc_path.name


def decrypt_file(filename: str) -> Path:
    """Decrypt given encrypted file and return decrypted file path."""
    enc_path = UPLOAD_FOLDER / filename
    data = enc_path.read_bytes()
    decrypted = fernet.decrypt(data)

    original_name = filename.replace(".enc", "")
    dec_path = UPLOAD_FOLDER / f"decrypted_{original_name}"
    dec_path.write_bytes(decrypted)
    return dec_path


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part in request")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("No file selected")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        save_path = UPLOAD_FOLDER / filename
        file.save(save_path)

        enc_name = encrypt_file(save_path)
        flash(f"File encrypted and saved as: {enc_name}")
        return redirect(url_for("index"))

    encrypted_files = [
        f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith(".enc")
    ]
    return render_template("index.html", files=encrypted_files)


@app.route("/download/<filename>")
def download(filename):
    dec_path = decrypt_file(filename)
    return send_from_directory(
        directory=UPLOAD_FOLDER,
        path=dec_path.name,
        as_attachment=True,
        download_name=dec_path.name,
    )


if __name__ == "__main__":
    app.run(debug=True)
