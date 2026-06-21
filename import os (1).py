import os
import json
import csv
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, session, flash

# ==============================================================================
# AUTOMATION LAYER: TEMPLATES UI (PREMIUM HUB DESIGN - SIAKAD CLOUD)
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# 1. TEMPLATE: LOGIN (LOGIN ENTRY - SIAKAD CLOUD)
PATH_LOGIN_HTML = os.path.join(TEMPLATES_DIR, 'login.html')
with open(PATH_LOGIN_HTML, 'w', encoding='utf-8') as f:
    f.write('''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIAKAD CLOUD - Login Sistem</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;800&family=Outfit:wght@300;400;600&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #020204;
            --neon-cyan: #00f0ff;
            --neon-purple: #a124f5;
            --neon-pink: #ff0055;
            --glass-core: rgba(10, 11, 18, 0.6);
            --glass-border: rgba(0, 240, 255, 0.15);
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body { 
            font-family: 'Outfit', sans-serif; 
            height: 100vh; display: flex; justify-content: center; align-items: center;
            background-color: var(--bg-dark); overflow: hidden; color: #fff;
            position: relative;
        }

        /* PREMIUM ANIMATED BACKGROUND: Cyber Grid & Aurora Glow */
        .cyber-bg {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: -2;
            background: radial-gradient(circle at 50% 50%, #0c081a 0%, #020204 100%);
        }
        .grid-overlay {
            position: absolute; width: 100%; height: 100%; z-index: -1;
            background-image: linear-gradient(rgba(0, 240, 255, 0.05) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(0, 240, 255, 0.05) 1px, transparent 1px);
            background-size: 40px 40px;
            transform: perspective(500px) rotateX(60deg);
            transform-origin: top;
            animation: gridMove 12s linear infinite;
            opacity: 0.4;
        }
        .aurora-wave {
            position: absolute; width: 600px; height: 600px; border-radius: 50%;
            background: linear-gradient(45deg, var(--neon-purple), var(--neon-cyan));
            filter: blur(100px); opacity: 0.3;
            animation: auroraFloat 15s ease-in-out infinite alternate;
        }
        .wave-1 { top: -10%; left: -10%; }
        .wave-2 { bottom: -10%; right: -10%; animation-delay: -7s; }

        @keyframes gridMove { from { background-position: 0 0; } to { background-position: 0 100%; } }
        @keyframes auroraFloat {
            0% { transform: translate(0, 0) scale(1) rotate(0deg); }
            100% { transform: translate(80px, 50px) scale(1.2) rotate(180deg); }
        }

        /* Cyberpunk Login Box */
        .login-box {
            background: var(--glass-core); backdrop-filter: blur(30px); -webkit-backdrop-filter: blur(30px);
            border: 1px solid var(--glass-border); border-radius: 20px; padding: 45px 40px; width: 400px;
            box-shadow: 0 0 40px rgba(0, 240, 255, 0.1), inset 0 0 20px rgba(161, 36, 245, 0.1);
            animation: bootUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            text-align: center;
        }

        @keyframes bootUp { from { opacity: 0; transform: translateY(30px) scale(0.95); } to { opacity: 1; transform: translateY(0) scale(1); } }

        h1 { font-family: 'Orbitron', sans-serif; font-weight: 800; font-size: 26px; letter-spacing: 3px; color: #fff; text-shadow: 0 0 10px var(--neon-cyan); margin-bottom: 8px; }
        p { color: #8a99ad; font-size: 13px; margin-bottom: 35px; letter-spacing: 1px; text-transform: uppercase; }

        .input-group { margin-bottom: 25px; text-align: left; }
        .input-group label { display: block; font-size: 11px; text-transform: uppercase; letter-spacing: 2px; color: var(--neon-cyan); margin-bottom: 8px; }
        .input-group input {
            width: 100%; background: rgba(5, 5, 10, 0.7); border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 15px; border-radius: 10px; color: #fff; font-family: 'JetBrains Mono', monospace; font-size: 14px;
            transition: all 0.3s ease;
        }
        .input-group input:focus { border-color: var(--neon-cyan); outline: none; box-shadow: 0 0 15px rgba(0, 240, 255, 0.3); background: rgba(0, 0, 0, 0.9); }

        .btn-submit {
            width: 100%; padding: 15px; background: linear-gradient(90deg, var(--neon-purple), var(--neon-cyan)); color: #fff; 
            border: none; border-radius: 10px; font-family: 'Orbitron', sans-serif; font-size: 14px; font-weight: 700; text-transform: uppercase;
            letter-spacing: 2px; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(161, 36, 245, 0.4);
        }
        .btn-submit:hover { transform: translateY(-2px); box-shadow: 0 0 25px var(--neon-cyan); color: #000; font-weight: 800; }
        
        .alert { background: rgba(255, 0, 85, 0.15); border: 1px solid var(--neon-pink); color: #ff3377; padding: 12px; border-radius: 8px; font-size: 13px; margin-bottom: 25px; text-shadow: 0 0 5px rgba(255,0,85,0.5); }
    </style>
</head>
<body>
    <div class="cyber-bg">
        <div class="grid-overlay"></div>
        <div class="aurora-wave wave-1"></div>
        <div class="aurora-wave wave-2"></div>
    </div>
    
    <div class="login-box">
        <h1>SIAKAD // CLOUD</h1>
        <p>Akses Portal Data Akademik</p>
        
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for msg in messages %}<div class="alert">⚠️ {{ msg }}</div>{% endfor %}
          {% endif %}
        {% endwith %}
        
        <form action="/login" method="POST">
            <div class="input-group">
                <label>ID Operator</label>
                <input type="text" name="username" required autocomplete="off" placeholder="admin">
            </div>
            <div class="input-group">
                <label>Security Key</label>
                <input type="password" name="password" required placeholder="••••••••">
            </div>
            <button type="submit" class="btn-submit">OTENTIKASI SISTEM</button>
        </form>
    </div>
</body>
</html>''')

# 2. TEMPLATE: DASHBOARD (MAIN DASHBOARD - SIAKAD CLOUD)
PATH_DASHBOARD_HTML = os.path.join(TEMPLATES_DIR, 'dashboard.html')
with open(PATH_DASHBOARD_HTML, 'w', encoding='utf-8') as f:
    f.write('''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIAKAD CLOUD - Panel Utama</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Outfit:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #040408;
            --glass-panel: rgba(13, 15, 28, 0.65);
            --glass-border: rgba(0, 240, 255, 0.12);
            --neon-cyan: #00f0ff;
            --neon-pink: #ff007a;
            --neon-purple: #9d4edd;
            --text-main: #f1f5f9;
            --text-muted: #64748b;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Outfit', sans-serif; background-color: var(--bg-dark); color: var(--text-main); min-height: 100vh; overflow-x: hidden;
            position: relative;
        }

        /* PREMIUM ANIMATED BACKGROUND */
        .cyber-bg {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -2; pointer-events: none;
            background: radial-gradient(circle at 50% 50%, #090714 0%, #030306 100%);
        }
        .grid-overlay {
            position: absolute; width: 100%; height: 100%; z-index: -1;
            background-image: linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
            background-size: 50px 50px;
        }
        .aurora-glow {
            position: absolute; border-radius: 50%; filter: blur(130px); opacity: 0.25; animation: auroraPulse 20s infinite alternate ease-in-out;
        }
        .glow-1 { width: 70vw; height: 50vh; background: var(--neon-purple); top: -10%; left: -10%; }
        .glow-2 { width: 60vw; height: 60vh; background: var(--neon-cyan); bottom: -10%; right: -10%; animation-delay: -5s; }
        
        @keyframes auroraPulse {
            0% { transform: translate(0, 0) scale(1); }
            100% { transform: translate(4vw, 5vh) scale(1.15); }
        }

        /* Navigation */
        .topbar {
            background: rgba(8, 9, 16, 0.75); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--glass-border); padding: 18px 40px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100;
        }
        .brand { font-family: 'Orbitron', sans-serif; font-size: 18px; font-weight: 800; letter-spacing: 2px; display: flex; align-items: center; gap: 12px; color: #fff; text-shadow: 0 0 10px rgba(0,240,255,0.3); }
        .brand-dot { width: 10px; height: 10px; background: var(--neon-cyan); border-radius: 50%; box-shadow: 0 0 12px var(--neon-cyan); }

        .user-hub { display: flex; align-items: center; gap: 20px; font-size: 13px; font-family: 'JetBrains Mono', monospace; }
        .logout-btn { background: rgba(255,0,122,0.12); color: var(--neon-pink); border: 1px solid rgba(255,0,122,0.3); padding: 8px 18px; border-radius: 8px; text-decoration: none; font-weight: bold; letter-spacing: 1px; transition: 0.3s; }
        .logout-btn:hover { background: var(--neon-pink); color: #fff; box-shadow: 0 0 20px var(--neon-pink); }

        .container { padding: 40px; max-width: 1600px; margin: 0 auto; display: grid; grid-template-columns: 380px 1fr; gap: 35px; }
        @media(max-width: 1100px) { .container { grid-template-columns: 1fr; } }

        /* Glassmorphism Panels */
        .glass-panel {
            background: var(--glass-panel); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border); border-radius: 18px; padding: 28px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.4); margin-bottom: 25px; transition: border 0.3s ease;
        }
        .glass-panel:hover { border-color: rgba(0, 240, 255, 0.25); }

        .panel-title { font-family: 'Orbitron', sans-serif; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; color: var(--neon-cyan); margin-bottom: 22px; display: flex; align-items: center; gap: 10px; }
        
        /* Form & inputs */
        .form-group { margin-bottom: 18px; }
        label { display: block; font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text-muted); margin-bottom: 8px; }
        input, select {
            width: 100%; background: rgba(5, 6, 12, 0.7); border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 14px; border-radius: 10px; color: #fff; font-family: 'Outfit', sans-serif; font-size: 14px; transition: all 0.3s ease;
        }
        input:focus, select:focus { border-color: var(--neon-purple); outline: none; box-shadow: 0 0 15px rgba(157,78,221,0.25); background: #000; }
        
        /* Buttons V2 */
        .btn {
            padding: 12px 20px; border-radius: 10px; border: 1px solid transparent; cursor: pointer; font-family: 'Orbitron', sans-serif;
            font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; text-align: center; text-decoration: none; transition: all 0.3s ease;
        }
        .btn-block { width: 100%; display: block; }
        .btn-cyan { background: rgba(0,240,255,0.08); color: var(--neon-cyan); border-color: rgba(0,240,255,0.25); }
        .btn-cyan:hover { background: var(--neon-cyan); color: #000; box-shadow: 0 0 25px var(--neon-cyan); }
        .btn-purple { background: rgba(157,78,221,0.12); color: #e9d5ff; border-color: rgba(157,78,221,0.3); }
        .btn-purple:hover { background: var(--neon-purple); color: #fff; box-shadow: 0 0 25px var(--neon-purple); }
        .btn-ghost { background: transparent; color: var(--text-muted); border-color: rgba(255,255,255,0.08); }
        .btn-ghost:hover { background: rgba(255,255,255,0.05); color: #fff; border-color: var(--text-main); }

        /* Modern Matrix Table */
        .table-responsive { border-radius: 18px; border: 1px solid var(--glass-border); background: var(--glass-panel); backdrop-filter: blur(20px); overflow: hidden; max-height: 85vh; overflow-y: auto; }
        table { width: 100%; border-collapse: separate; border-spacing: 0; text-align: left; }
        th { font-family: 'Orbitron', sans-serif; font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--neon-cyan); padding: 18px; border-bottom: 1px solid var(--glass-border); background: rgba(10, 12, 22, 0.8); position: sticky; top: 0; z-index: 5; }
        td { padding: 18px; border-bottom: 1px solid rgba(255,255,255,0.03); transition: 0.2s; font-size: 14px; }
        tr:hover td { background: rgba(0, 240, 255, 0.03); }
        tr:hover td:first-child { box-shadow: inset 4px 0 0 var(--neon-cyan); color: var(--neon-cyan); }
        
        .code-font { font-family: 'JetBrains Mono', monospace; font-size: 13px; }
        .badge { background: rgba(157,78,221,0.15); color: #d8b4fe; padding: 5px 12px; border-radius: 6px; font-size: 11px; font-weight: 600; text-transform: uppercase; border: 1px solid rgba(157,78,221,0.25); }
        
        /* Action Buttons */
        .act-btn { padding: 5px 12px; border-radius: 6px; font-size: 11px; text-decoration: none; border: 1px solid transparent; transition: 0.2s; font-family: 'Orbitron', sans-serif; font-weight: 600; }
        .act-edit { color: #fbbf24; background: rgba(245,158,11,0.1); border-color: rgba(245,158,11,0.2); }
        .act-edit:hover { background: #fbbf24; color: #000; box-shadow: 0 0 15px #fbbf24; }
        .act-del { color: #f43f5e; background: rgba(244,63,94,0.1); border-color: rgba(244,63,94,0.2); }
        .act-del:hover { background: #f43f5e; color: #fff; box-shadow: 0 0 15px #f43f5e; }
        .act-mail { color: #38bdf8; background: rgba(56,189,248,0.1); border-color: rgba(56,189,248,0.2); }
        .act-mail:hover { background: #38bdf8; color: #000; box-shadow: 0 0 15px #38bdf8; }

        .toast { background: rgba(0,240,255,0.08); border-left: 4px solid var(--neon-cyan); color: #fff; padding: 15px 20px; border-radius: 0 10px 10px 0; margin-bottom: 22px; font-size: 13px; font-weight: 500; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    </style>
</head>
<body>
    <div class="cyber-bg">
        <div class="grid-overlay"></div>
        <div class="aurora-glow glow-1"></div>
        <div class="aurora-glow glow-2"></div>
    </div>

    <div class="topbar">
        <div class="brand"><div class="brand-dot"></div> SIAKAD // CLOUD</div>
        <div class="user-hub">
            <span style="color: var(--text-muted); letter-spacing: 1px;">OPERATOR: <span style="color:var(--neon-cyan);">{{ session['username'] }}</span></span>
            <a href="/logout" class="logout-btn">TERMINATE</a>
        </div>
    </div>

    <div class="container">
        <div class="controls-wrapper">
            {% with messages = get_flashed_messages() %}
              {% if messages %}
                {% for msg in messages %}<div class="toast">⚡ SYSTEM // {{ msg }}</div>{% endfor %}
              {% endif %}
            {% endwith %}

            <div class="glass-panel">
                <div class="panel-title">📡 Input Entitas Mahasiswa</div>
                <form action="/mahasiswa/save" method="POST">
                    <div class="form-group">
                        <label>NIM (Primary Identifier)</label>
                        <input type="text" name="nim" class="code-font" placeholder="Contoh: 20260901" required>
                    </div>
                    <div class="form-group">
                        <label>Nama Lengkap</label>
                        <input type="text" name="nama" placeholder="Masukkan nama..." required>
                    </div>
                    <div class="form-group">
                        <label>Network Email</label>
                        <input type="email" name="email" placeholder="mahasiswa@node.id" required>
                    </div>
                    <div class="form-group">
                        <label>Klaster Prodi</label>
                        <select name="prodi">
                            <option value="Sistem Informasi">Sistem Informasi</option>
                            <option value="Teknik Informatika">Teknik Informatika</option>
                            <option value="Sains Data">Sains Data</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-cyan btn-block" style="margin-top: 10px;">COMMIT_DATA()</button>
                </form>
            </div>

            <div class="glass-panel">
                <div class="panel-title">🔎 Search & Sort Engine</div>
                <form action="/dashboard" method="GET">
                    <div class="form-group">
                        <input type="text" name="search_query" value="{{ search_query }}" placeholder="Query parameter..." style="margin-bottom: 12px;">
                        <select name="search_method" style="margin-bottom: 12px;">
                            <option value="linear" {% if search_method == 'linear' %}selected{% endif %}>Linear Search (String Nama)</option>
                            <option value="binary" {% if search_method == 'binary' %}selected{% endif %}>Binary Search (NIM Numerik)</option>
                        </select>
                        <div class="grid-2">
                            <button type="submit" class="btn btn-purple">EXECUTE</button>
                            <a href="/dashboard" class="btn btn-ghost">CLEAR</a>
                        </div>
                    </div>
                </form>
                
                <label style="margin-top: 15px;">Sort Algorithm Pipeline</label>
                <div class="grid-2">
                    <a href="/dashboard?sort=nim_bubble" class="btn btn-ghost" style="font-size: 10px;">Bubble (NIM)</a>
                    <a href="/dashboard?sort=nama_selection" class="btn btn-ghost" style="font-size: 10px;">Select (Nama)</a>
                </div>
            </div>

            <div class="glass-panel">
                <div class="panel-title">📂 Data I/O Stream</div>
                <a href="/export/csv" class="btn btn-cyan btn-block" style="margin-bottom: 15px;">📥 EXPORT TO CSV</a>
                <form action="/import/csv" method="POST" enctype="multipart/form-data">
                    <input type="file" name="file_csv" accept=".csv" required style="border: none; padding: 0; background: transparent; margin-bottom: 12px; font-size: 12px;">
                    <button type="submit" class="btn btn-purple btn-block">📤 PARSE CSV</button>
                </form>
            </div>
        </div>

        <div class="table-responsive">
            <div style="padding: 25px 25px 15px 25px; background: rgba(13, 15, 28, 0.9); border-bottom: 1px solid var(--glass-border);">
                <div class="panel-title" style="margin: 0;">📊 Live Database Matrix</div>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>ID / NIM</th>
                        <th>Identitas Nama</th>
                        <th>Alamat Email</th>
                        <th>Klaster Prodi</th>
                        <th>Sistem Operasi</th>
                    </tr>
                </thead>
                <tbody>
                    {% for mhs in mahasiswa_list %}
                    <tr>
                        <td class="code-font" style="color: var(--neon-cyan); font-weight: bold;">{{ mhs.nim }}</td>
                        <td style="font-weight: 500;">{{ mhs.nama }}</td>
                        <td class="code-font" style="color: #94a3b8; font-size: 12px;">{{ mhs.email }}</td>
                        <td><span class="badge">{{ mhs.prodi }}</span></td>
                        <td>
                            <div style="display: flex; gap: 6px;">
                                <button class="act-btn act-edit" onclick="isiForm('{{ mhs.nim }}', '{{ mhs.nama }}', '{{ mhs.email }}', '{{ mhs.prodi }}')">Edit</button>
                                <a href="/mahasiswa/delete/{{ mhs.nim }}" class="act-btn act-del" onclick="return confirm('Drop baris data ini?')">Drop</a>
                                <a href="/mahasiswa/notify/{{ mhs.nim }}" class="act-btn act-mail">Ping</a>
                            </div>
                        </td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="5" style="text-align: center; padding: 60px; color: var(--text-muted); font-family: 'JetBrains Mono', monospace; font-size: 13px;">> Array Kosong. Menunggu komit entitas baru..._</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <script>
        function isiForm(nim, nama, email, prodi) {
            document.getElementsByName('nim')[0].value = nim;
            document.getElementsByName('nama')[0].value = nama;
            document.getElementsByName('email')[0].value = email;
            document.getElementsByName('prodi')[0].value = prodi;
            const formCard = document.querySelector('.controls-wrapper .glass-panel');
            formCard.style.borderColor = 'var(--neon-cyan)';
            formCard.style.boxShadow = '0 0 30px rgba(0, 240, 255, 0.4)';
            setTimeout(() => { 
                formCard.style.borderColor = 'var(--glass-border)';
                formCard.style.boxShadow = '0 20px 40px rgba(0,0,0,0.4)'; 
            }, 1200);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    </script>
</body>
</html>''')


# ==============================================================================
# DATA MODEL OBJECT ORIENTED PROGRAMMING Layer
# ==============================================================================
class Orang:
    def __init__(self, nama, email):
        self.nama = nama            
        self._email = email         

    def get_peran(self):
        return "Entitas Umum"


class Pengguna(Orang):
    def __init__(self, username, email, password):
        super().__init__(username, email)
        self.__password = password  

    def verifikasi_password(self, password_input):
        return self.__password == password_input

    def get_peran(self):
        return "Administrator Sistem"


class MahasiswaModel(Orang):
    def __init__(self, nim, nama, email, prodi):
        super().__init__(nama, email)
        self.__nim = nim            
        self.prodi = prodi          

    @property
    def nim(self):
        return self.__nim

    @nim.setter
    def nim(self, value):
        self.__nim = value

    def get_peran(self):
        return "Mahasiswa Akademik"

    def to_dict(self):
        return {
            "nim": self.__nim,
            "nama": self.nama,
            "email": self._email,
            "prodi": self.prodi
        }


# ==============================================================================
# CORE ALGORITHMS Pipeline
# ==============================================================================
def bubble_sort_berdasarkan_nim(data_array):
    n = len(data_array)
    for i in range(n):
        for j in range(0, n - i - 1):
            try:
                if int(data_array[j]['nim']) > int(data_array[j+1]['nim']):
                    data_array[j], data_array[j+1] = data_array[j+1], data_array[j]
            except ValueError:
                if data_array[j]['nim'] > data_array[j+1]['nim']:
                    data_array[j], data_array[j+1] = data_array[j+1], data_array[j]
    return data_array


def selection_sort_berdasarkan_nama(data_array):
    n = len(data_array)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if data_array[j]['nama'].lower() < data_array[min_idx]['nama'].lower():
                min_idx = j
        data_array[i], data_array[min_idx] = data_array[min_idx], data_array[i]
    return data_array


def sequential_linear_search_nama(data_array, keyword):
    hasil = []
    for item in data_array:
        if keyword.lower() in item['nama'].lower():
            hasil.append(item)
    return hasil


def binary_search_nim(data_array, target_nim):
    sorted_list = bubble_sort_berdasarkan_nim(list(data_array))
    low = 0
    high = len(sorted_list) - 1
    
    while low <= high:
        mid = (low + high) // 2
        current_nim = sorted_list[mid]['nim']
        
        if str(current_nim).strip() == str(target_nim).strip():
            return [sorted_list[mid]]
            
        try:
            if int(current_nim) < int(target_nim):
                low = mid + 1
            else:
                high = mid - 1
        except ValueError:
            if str(current_nim) < str(target_nim):
                low = mid + 1
            else:
                high = mid - 1
    return []


# ==============================================================================
# REAL-TIME SMTP NOTIFICATION INFRASTRUCTURE
# ==============================================================================
def prosedur_kirim_email_realtime(email_penerima, nama_mahasiswa):
    sender_email = "notifikasi.kampus.pro@gmail.com"
    sender_password = "your-app-password-here"
    
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email_penerima
        msg['Subject'] = "⚙️ [SYSTEM PING] Verifikasi Node Academic"
        
        body = f"Akses diberikan untuk {nama_mahasiswa}.\n\nData node akademik telah direkam di server utama secara real-time.\n\n-- SysAdmin Akademik"
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email_penerima, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"[ERROR] Koneksi Node SMTP Gagal: {e}")
        return False


# ==============================================================================
# FLASK WEB SERVER ROUTING & CORE CONTROLLER
# ==============================================================================
app = Flask(__name__)
app.secret_key = "kunci_rahasia_pro_algoritma_dua"

FILE_JSON_DATABASE = os.path.join(BASE_DIR, "mahasiswa.json")

if not os.path.exists(FILE_JSON_DATABASE):
    with open(FILE_JSON_DATABASE, 'w') as f:
        json.dump([], f)


@app.route('/')
def beranda():
    if 'username' in session:
        return redirect('/dashboard')
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def fungsi_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin_auth = Pengguna("admin", "admin@kampus.ac.id", "admin123")
        
        if username == admin_auth.nama and admin_auth.verifikasi_password(password):
            session['username'] = username
            return redirect('/dashboard')
        else:
            flash("ACCESS DENIED: Kredensial tidak valid.")
            return redirect('/login')
            
    return render_template('login.html')


@app.route('/dashboard')
def fungsi_tampilkan_data():
    if 'username' not in session:
        return redirect('/login')

    try:
        with open(FILE_JSON_DATABASE, 'r') as f:
            mahasiswa_list = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        mahasiswa_list = []

    search_query = request.args.get('search_query', '')
    search_method = request.args.get('search_method', 'linear')
    
    if search_query:
        if search_method == 'binary':
            mahasiswa_list = binary_search_nim(mahasiswa_list, search_query)
        else:
            mahasiswa_list = sequential_linear_search_nama(mahasiswa_list, search_query)

    sort_type = request.args.get('sort', '')
    if sort_type == 'nim_bubble':
        mahasiswa_list = bubble_sort_berdasarkan_nim(mahasiswa_list)
        flash("SORTING EXECUTED: Bubble Sort (NIM).")
    elif sort_type == 'nama_selection':
        mahasiswa_list = selection_sort_berdasarkan_nama(mahasiswa_list)
        flash("SORTING EXECUTED: Selection Sort (Nama).")

    return render_template('dashboard.html', mahasiswa_list=mahasiswa_list, search_query=search_query, search_method=search_method)


@app.route('/mahasiswa/save', methods=['POST'])
def fungsi_simpan_dan_edit():
    if 'username' not in session:
        return redirect('/login')

    nim = request.form.get('nim')
    nama = request.form.get('nama')
    email = request.form.get('email')
    prodi = request.form.get('prodi')

    if not re.match(r'^\d{3,15}$', nim) or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        flash("SYNTAX ERROR: Format NIM (Min 3 Angka) atau Email salah.")
        return redirect('/dashboard')

    mhs_obj = MahasiswaModel(nim, nama, email, prodi)

    try:
        with open(FILE_JSON_DATABASE, 'r') as f:
            data_lama = json.load(f)
    except Exception:
        data_lama = []

    index_ditemukan = -1
    for idx, item in enumerate(data_lama):
        if str(item['nim']) == str(mhs_obj.nim):
            index_ditemukan = idx
            break

    if index_ditemukan != -1:
        data_lama[index_ditemukan] = mhs_obj.to_dict()
        flash(f"DATA OVERRIDE: Node NIM {mhs_obj.nim} telah diperbarui.")
    else:
        data_lama.append(mhs_obj.to_dict())
        flash(f"NEW NODE ADDED: {mhs_obj.nama} terekam di database.")

    with open(FILE_JSON_DATABASE, 'w') as f:
        json.dump(data_lama, f, indent=4)

    return redirect('/dashboard')


@app.route('/mahasiswa/delete/<nim>')
def fungsi_hapus_data(nim):
    if 'username' not in session:
        return redirect('/login')

    try:
        with open(FILE_JSON_DATABASE, 'r') as f:
            data = json.load(f)
        data_baru = [item for item in data if str(item['nim']) != str(nim)]
        with open(FILE_JSON_DATABASE, 'w') as f:
            json.dump(data_baru, f, indent=4)
        flash(f"NODE DROPPED: ID {nim} berhasil di-wipe.")
    except Exception:
        pass
    return redirect('/dashboard')


@app.route('/mahasiswa/notify/<nim>')
def fungsi_notifikasi(nim):
    if 'username' not in session:
        return redirect('/login')

    with open(FILE_JSON_DATABASE, 'r') as f:
        data = json.load(f)
    mhs_target = next((item for item in data if str(item['nim']) == str(nim)), None)
    
    if mhs_target:
        prosedur_kirim_email_realtime(mhs_target['email'], mhs_target['nama'])
        flash(f"PING SUCCESS: Packet dikirim ke {mhs_target['email']}.")
    return redirect('/dashboard')


@app.route('/export/csv')
def fungsi_export_csv():
    if 'username' not in session:
        return redirect('/login')

    try:
        with open(FILE_JSON_DATABASE, 'r') as f:
            data = json.load(f)
        csv_file_path = os.path.join(BASE_DIR, "export_data_mahasiswa.csv")
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['NIM', 'Nama', 'Email', 'Program Studi'])
            for mhs in data:
                writer.writerow([mhs['nim'], mhs['nama'], mhs['email'], mhs['prodi']])
        flash("I/O STREAM: Sinkronisasi ekspor file *.csv selesai.")
    except Exception:
        pass
    return redirect('/dashboard')


@app.route('/import/csv', methods=['POST'])
def fungsi_import_csv():
    if 'username' not in session:
        return redirect('/login')

    file = request.files.get('file_csv')
    if file:
        try:
            temp_path = os.path.join(BASE_DIR, "temp_import.csv")
            file.save(temp_path)
            with open(temp_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                with open(FILE_JSON_DATABASE, 'r') as jf:
                    database = json.load(jf)
                for row in reader:
                    if len(row) >= 4:
                        nim, nama, email, prodi = row[0], row[1], row[2], row[3]
                        if re.match(r'^\d{3,15}$', nim):
                            database = [item for item in database if str(item['nim']) != str(nim)]
                            database.append({"nim": nim, "nama": nama, "email": email, "prodi": prodi})
                with open(FILE_JSON_DATABASE, 'w') as jf:
                    json.dump(database, jf, indent=4)
            os.remove(temp_path)
            flash("I/O STREAM: Integrasi data eksternal CSV ke JSON sukses.")
        except Exception:
            pass
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


# ==============================================================================
# OPTIMIZED PRODUCTION RUNNER (PREPARED FOR HOSTING PLATFORMS)
# ==============================================================================
if __name__ == '__main__':
    # Otomatis menyesuaikan IP dan Port lingkungan server hosting
    cloud_host = os.environ.get("HOST", "0.0.0.0")
    cloud_port = int(os.environ.get("PORT", 5000))
    
    print(f"[SYSTEM] Mengaktifkan Engine Produksi SIAKAD CLOUD pada {cloud_host}:{cloud_port}...")
    app.run(host=cloud_host, port=cloud_port, debug=False)