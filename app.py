import sys
import os
import json
import secrets
import hashlib
from flask import Flask, request, render_template, send_from_directory, url_for, redirect, session, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import io

app = Flask(__name__)

if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.abspath(os.path.dirname(__file__))

CONFIG_FILE = os.path.join(base_path, 'config.json')

app.config['UPLOAD_FOLDER'] = os.path.join(base_path, 'uploads')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def load_or_create_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        config = {
            'secret_key': secrets.token_hex(16),
            'port': 8080,  # 默认端口号
            'background': '#f4f4f4',  # 默认背景色
            'site_name': 'AirImage',  # 默认网站名称
            'site_icon': '',  # 默认网站图标为空
            'max_file_size': 10,  # 默认最大文件大小为10MB
            'allowed_extensions': ["png", "jpg", "jpeg", "gif", "webp"]  # 默认允许的文件类型
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        return config

config = load_or_create_config()
app.secret_key = config['secret_key']
PORT = config.get('port', 8080)
BACKGROUND = config.get('background', '#f4f4f4')
SITE_NAME = config.get('site_name', 'AirImage')
SITE_ICON = config.get('site_icon', '')
MAX_FILE_SIZE = config.get('max_file_size', 10) * 1024 * 1024  
ALLOWED_EXTENSIONS = set(config.get('allowed_extensions', ["png", "jpg", "jpeg", "gif", "webp"]))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_webp(image):
    webp_io = io.BytesIO()
    image.save(webp_io, 'WEBP', quality=85)
    webp_io.seek(0)
    return webp_io

def get_file_hash(file_content):
    return hashlib.md5(file_content).hexdigest()

def get_unique_filename(file_content, original_filename):
    file_hash = get_file_hash(file_content)
    _, ext = os.path.splitext(original_filename)
    return f"{file_hash}{ext}"

def get_uploaded_files():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.lower().split('.')[-1] in ALLOWED_EXTENSIONS:
            file_url = url_for('uploaded_file', filename=filename, _external=True)
            files.append({'name': filename, 'url': file_url})
    return sorted(files, key=lambda x: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], x['name'])), reverse=True)

def get_background():
    bg = BACKGROUND
    if bg.startswith(('http://', 'https://')):
        return {'type': 'url', 'value': bg}
    elif os.path.isfile(bg):
        return {'type': 'file', 'value': url_for('custom_background', filename=os.path.basename(bg))}
    else:
        return {'type': 'color', 'value': bg}

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'error': '没有文件'}), 400
            return redirect(url_for('upload_file', error='没有文件'))
        
        files = request.files.getlist('file')
        if not files or files[0].filename == '':
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'error': '没有选择文件'}), 400
            return redirect(url_for('upload_file', error='没有选择文件'))
        
        uploaded_files = []
        for file in files:
            if file and allowed_file(file.filename):
                try:
                    file_content = file.read()
                    if len(file_content) > MAX_FILE_SIZE:
                        raise ValueError(f"文件大小超过限制 ({MAX_FILE_SIZE/1024/1024}MB)")
                    
                    image = Image.open(io.BytesIO(file_content))
                    filename = get_unique_filename(file_content, file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    
                    if filename.lower().endswith('.webp'):
                        with open(file_path, 'wb') as f:
                            f.write(file_content)
                    else:
                        webp_io = convert_to_webp(image)
                        webp_filename = os.path.splitext(filename)[0] + '.webp'
                        webp_path = os.path.join(app.config['UPLOAD_FOLDER'], webp_filename)
                        with open(webp_path, 'wb') as f:
                            f.write(webp_io.getvalue())
                        filename = webp_filename
                    
                    file_url = url_for('uploaded_file', filename=filename, _external=True)
                    uploaded_files.append(file_url)
                except Exception as e:
                    app.logger.error(f"Error processing file: {str(e)}")
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return jsonify({'success': False, 'error': str(e)}), 500
                    return redirect(url_for('upload_file', error=str(e)))
        
        if uploaded_files:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': True, 'file_urls': uploaded_files})
            session['success'] = True
            session['file_urls'] = uploaded_files
            return redirect(url_for('upload_file'))
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'error': '没有有效的文件被上传'}), 400
            return redirect(url_for('upload_file', error='没有有效的文件被上传'))

    success = session.pop('success', False)
    file_urls = session.pop('file_urls', [])
    error = request.args.get('error')
    uploaded_files = get_uploaded_files()
    background = get_background()
    return render_template('index.html', success=success, file_urls=file_urls, error=error, uploaded_files=uploaded_files, background=background, site_name=SITE_NAME, site_icon=SITE_ICON)

@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/custom_background/<filename>')
def custom_background(filename):
    directory = os.path.dirname(BACKGROUND)
    return send_from_directory(directory, filename)

@app.route('/get_settings')
def get_settings():
    return jsonify({
        'site_name': SITE_NAME,
        'site_icon': SITE_ICON,
        'max_file_size': MAX_FILE_SIZE // (1024 * 1024),  
        'allowed_extensions': list(ALLOWED_EXTENSIONS),
        'background': BACKGROUND
    })

@app.route('/save_settings', methods=['POST'])
def save_settings():
    global SITE_NAME, SITE_ICON, MAX_FILE_SIZE, ALLOWED_EXTENSIONS, BACKGROUND
    data = request.json
    SITE_NAME = data['site_name']
    SITE_ICON = data['site_icon']
    MAX_FILE_SIZE = int(data['max_file_size']) * 1024 * 1024  
    ALLOWED_EXTENSIONS = set(data['allowed_extensions'])
    BACKGROUND = data['background']

    config = load_or_create_config()
    config.update({
        'site_name': SITE_NAME,
        'site_icon': SITE_ICON,
        'max_file_size': int(data['max_file_size']),
        'allowed_extensions': list(ALLOWED_EXTENSIONS),
        'background': BACKGROUND
    })
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

    return jsonify({'success': True})
