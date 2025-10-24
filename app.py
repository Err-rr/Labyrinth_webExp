from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from flask_sock import Sock
import sqlite3
import hashlib
import jwt
import os
import base64
import json
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import re

app = Flask(__name__)
app.config.from_object('config')
sock = Sock(app)

# Initialize database
def init_db():
    conn = sqlite3.connect('labyrinth.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT, bio TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS maze_sessions
                 (id INTEGER PRIMARY KEY, user_id INTEGER, moves TEXT, completed INTEGER)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS hints
                 (id INTEGER PRIMARY KEY, level INTEGER, hint_text TEXT, unlock_condition TEXT)''')
    
    # Insert default users
    c.execute("DELETE FROM users")
    c.execute("INSERT INTO users VALUES (1, 'admin', ?, 'admin', 'System Administrator')", 
              (hashlib.sha256('sup3r_s3cr3t_4dm1n_p4ss'.encode()).hexdigest(),))
    c.execute("INSERT INTO users VALUES (2, 'player1', ?, 'user', 'Regular player')", 
              (hashlib.sha256('player123'.encode()).hexdigest(),))
    c.execute("INSERT INTO users VALUES (3, 'developer', ?, 'dev', 'Backend developer - left notes in JS')", 
              (hashlib.sha256('dev_temp_password'.encode()).hexdigest(),))
    
    # Insert hints
    c.execute("DELETE FROM hints")
    c.execute("INSERT INTO hints VALUES (1, 1, 'Check the JavaScript source code carefully. Developers sometimes leave comments...', 'basic')")
    c.execute("INSERT INTO hints VALUES (2, 2, 'Backup files might contain sensitive configuration. Check common backup patterns.', 'sql_found')")
    c.execute("INSERT INTO hints VALUES (3, 3, 'JWT tokens can be forged if you know the secret key. Chain your findings together.', 'backup_found')")
    
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play')
def play():
    return render_template('play.html')

@app.route('/api/move', methods=['POST'])
def api_move():
    data = request.get_json()
    direction = data.get('direction')
    position = data.get('position')
    token = data.get('token')
    
    # Intentionally flawed validation - always rejects winning moves
    # unless special token is provided
    if not token:
        return jsonify({
            'success': False,
            'error': 'Move validation failed',
            'debug_info': 'Token missing - hint: check /static/app.js for token generation logic',
            'position': position
        }), 403
    
    # Check for special forged token
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        if decoded.get('bypass') == 'labyrinth_master' and decoded.get('role') == 'admin':
            return jsonify({
                'success': True,
                'message': 'Bypass detected! You found the alternate route.',
                'next_step': 'Visit /flag with this token to claim your prize'
            })
    except:
        pass
    
    return jsonify({
        'success': False,
        'error': 'Invalid move sequence detected',
        'debug_info': 'Server-side validation always rejects winning paths - find another way',
        'hint': 'The maze is unsolvable by design. Look for web vulnerabilities.'
    }), 403

@app.route('/search')
def search():
    query = request.args.get('q', '')
    
    if query:
        # INTENTIONAL SQL INJECTION VULNERABILITY
        conn = sqlite3.connect('labyrinth.db')
        c = conn.cursor()
        
        try:
            # Vulnerable query - no parameterization
            sql = f"SELECT username, bio FROM users WHERE username LIKE '%{query}%' OR bio LIKE '%{query}%'"
            c.execute(sql)
            results = c.fetchall()
            conn.close()
            
            return render_template('search.html', results=results, query=query)
        except Exception as e:
            conn.close()
            # Error-based SQLi - leaks query structure
            return render_template('search.html', error=str(e), query=query)
    
    return render_template('search.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        filename = file.filename
        
        # INTENTIONAL LFI VULNERABILITY - no proper sanitization
        # Accepts path traversal in filename
        upload_path = os.path.join('uploads', filename)
        
        try:
            os.makedirs('uploads', exist_ok=True)
            file.save(upload_path)
            
            # Predictable image processing that could lead to RCE
            # Hint at potential exploit
            return jsonify({
                'success': True,
                'message': 'File uploaded successfully',
                'path': upload_path,
                'note': 'Files are processed with ImageMagick 6.9.10 (check CVE database)'
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template('upload.html')

@app.route('/profile/<int:user_id>')
def profile(user_id):
    # INTENTIONAL IDOR VULNERABILITY - no authorization check
    conn = sqlite3.connect('labyrinth.db')
    c = conn.cursor()
    c.execute("SELECT id, username, role, bio FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    
    if user:
        # Leak sensitive info for admin user
        user_data = {
            'id': user[0],
            'username': user[1],
            'role': user[2],
            'bio': user[3]
        }
        
        if user[2] == 'admin':
            user_data['note'] = 'Admin panel accessible at /admin with valid JWT'
        
        return render_template('profile.html', user=user_data)
    
    return "User not found", 404

@app.route('/admin')
def admin():
    # Check for JWT token
    token = request.cookies.get('auth_token') or request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not token:
        return render_template('admin_login.html')
    
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        if decoded.get('role') == 'admin':
            return render_template('admin_panel.html', username=decoded.get('username'))
    except:
        pass
    
    return "Unauthorized", 403

@app.route('/backup')
def backup():
    # INTENTIONAL INFORMATION DISCLOSURE - exposes config backup
    backup_file = 'config.py.bak'
    
    if os.path.exists(backup_file):
        return send_file(backup_file, as_attachment=True)
    
    return "Backup not found", 404

@app.route('/static/app.js')
def app_js():
    # Serve obfuscated JS with hints
    js_code = '''
// Labyrinth Client Controller
// Author: dev@labyrinth.local
// TODO: Remove debug comments before production!

const MazeController = {
    init: function() {
        console.log("Maze initialized - GL HF!");
        // NOTE: Server validates all moves server-side
        // No client-side bypass will work!
    },
    
    sendMove: function(direction, position) {
        // Dev note: Token generation moved to separate endpoint
        // See: aHR0cDovL2xvY2FsaG9zdDo1MDAwL3NlY3JldC9wb3J0YWw= (base64)
        
        fetch('/api/move', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                direction: direction,
                position: position,
                token: this.getToken()
            })
        }).then(r => r.json()).then(data => {
            console.log("Server response:", data);
        });
    },
    
    getToken: function() {
        // TODO: Implement proper token generation
        // For now, server expects JWT with 'bypass' claim
        return null;
    }
};

// Legacy endpoint (deprecated): /debug?source=app.js
// New debug endpoint: /ws (WebSocket echo for auth testing)

MazeController.init();
'''
    return js_code, 200, {'Content-Type': 'application/javascript'}

@app.route('/debug')
def debug():
    source = request.args.get('source', '')
    
    # INTENTIONAL PATH TRAVERSAL
    if source:
        try:
            with open(source, 'r') as f:
                content = f.read()
            return jsonify({
                'file': source,
                'content': content,
                'warning': 'Debug endpoint - disable in production!'
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    return jsonify({
        'endpoints': ['/api/move', '/search', '/upload', '/admin'],
        'hint': 'Use ?source=filename to view source code'
    })

@sock.route('/ws')
def websocket(ws):
    # INTENTIONAL WEBSOCKET TOKEN ECHO - useful for replay attacks
    while True:
        data = ws.receive()
        if data:
            try:
                msg = json.loads(data)
                if 'token' in msg:
                    ws.send(json.dumps({
                        'echo': msg['token'],
                        'decoded': 'Token echo service - useful for testing',
                        'hint': 'Tokens can be replayed if not properly validated'
                    }))
            except:
                ws.send(json.dumps({'error': 'Invalid JSON'}))

@app.route('/robots.txt')
def robots():
    return '''User-agent: *
Disallow: /admin
Disallow: /backup
Disallow: /secret/portal
Disallow: /flag
'''

@app.route('/secret/portal')
def secret_portal():
    # Hidden endpoint revealed in base64 comment in app.js
    return render_template('portal.html')

@app.route('/hint')
def hint():
    level = request.args.get('level', '1')
    
    # Progressive hints based on exploitation progress
    conn = sqlite3.connect('labyrinth.db')
    c = conn.cursor()
    c.execute("SELECT hint_text FROM hints WHERE level = ?", (level,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return jsonify({'hint': result[0]})
    
    return jsonify({'hint': 'No more hints available. You have all the pieces - chain them together!'})

@app.route('/flag')
def flag():
    token = request.args.get('token') or request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not token:
        return jsonify({
            'error': 'Token required',
            'hint': 'Forge a JWT with the right claims using the leaked secret key'
        }), 403
    
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        
        # Check for specific claims that prove complete exploitation chain
        if (decoded.get('bypass') == 'labyrinth_master' and 
            decoded.get('role') == 'admin' and
            decoded.get('source') == 'exploit'):
            
            return jsonify({
                'success': True,
                'flag': 'EHAX{l4bYr1n7_byp4ss_1s_th3_k3y}',
                'message': 'Congratulations! You navigated the labyrinth of vulnerabilities!',
                'exploitation_path': 'SQLi → Backup Discovery → JWT Key Leak → Token Forgery → Flag'
            })
        else:
            return jsonify({
                'error': 'Invalid token claims',
                'hint': 'Your token needs: bypass=labyrinth_master, role=admin, source=exploit'
            }), 403
            
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token signature - did you use the correct secret key?'}), 403

@app.route('/api/vault')
def vault():
    # Admin panel API endpoint
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        if decoded.get('role') == 'admin':
            return jsonify({
                'vault_status': 'unlocked',
                'redirect': '/flag?token=' + token
            })
    except:
        pass
    
    return jsonify({'error': 'Unauthorized'}), 403

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)