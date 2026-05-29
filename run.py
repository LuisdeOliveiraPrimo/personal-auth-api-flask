import subprocess
import sys
import time

print("🚀 Iniciando o Backend (Flask)...")
backend = subprocess.Popen([sys.executable, "backend/app.py"])

time.sleep(2)

print("🎨 Iniciando o Frontend (Streamlit)...")
try:
    # AQUI FOI ALTERADO PARA Login.py 👇
    subprocess.run([sys.executable, "-m", "streamlit", "run", "frontend/Login.py"])
except KeyboardInterrupt:
    print("\n🛑 Desligando os sistemas...")
finally:
    backend.terminate()