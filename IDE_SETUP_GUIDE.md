# Running UPI Expense Tracker in Different IDEs

## 🎯 Visual Studio Code

### Setup:
1. **Install VS Code** from https://code.visualstudio.com/
2. **Install Python Extension** (by Microsoft)
3. **Open project folder** in VS Code
4. **Open integrated terminal** (`Ctrl+` ` or `View > Terminal`)

### Run Commands:
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

### VS Code Features:
- ✅ **Debug mode**: Set breakpoints and debug
- ✅ **IntelliSense**: Auto-completion
- ✅ **Git integration**: Built-in version control
- ✅ **Extensions**: Flask snippets, Python linting

---

## 🐍 PyCharm

### Setup:
1. **Install PyCharm** (Community Edition is free)
2. **Open project folder**
3. **Configure Python Interpreter**:
   - Go to `File > Settings > Project > Python Interpreter`
   - Click gear icon → `Add`
   - Choose `Virtual Environment > New Environment`

### Run:
1. **Right-click `app.py`** → `Run 'app'`
2. **Or use Run Configuration**:
   - `Run > Edit Configurations`
   - Add new Python configuration
   - Set script path to `app.py`

### PyCharm Features:
- ✅ **Professional debugging**
- ✅ **Database tools** (for viewing SQLite)
- ✅ **Flask framework support**
- ✅ **Automatic virtual environment**

---

## 📓 Jupyter Notebook

### Setup:
```bash
# Install Jupyter
pip install jupyter

# Start Jupyter
jupyter notebook
```

### Create a new notebook and run:
```python
# Cell 1: Install dependencies (if needed)
!pip install flask flask-sqlalchemy flask-cors python-dateutil

# Cell 2: Run the Flask app
import subprocess
import threading

def run_flask():
    subprocess.run(['python', 'app.py'])

# Start Flask in background
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

print("Flask app starting... Visit http://localhost:5000")
```

---

## 🔥 Sublime Text

### Setup:
1. **Install Sublime Text**
2. **Install Package Control**
3. **Install Python packages**:
   - `Anaconda` (Python IDE features)
   - `SublimeREPL` (for running Python)

### Run:
1. **Open project folder**
2. **Use SublimeREPL**: `Tools > SublimeREPL > Python`
3. **Run commands** in REPL:
```python
import subprocess
subprocess.run(['python', 'app.py'])
```

---

## 🌐 Online IDEs

### Replit
1. **Create new Python Repl**
2. **Upload project files**
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Run**: `python app.py`

### Gitpod
1. **Open in Gitpod** (if project is on GitHub)
2. **Terminal opens automatically**
3. **Run setup commands**

### CodeSandbox
1. **Create Python sandbox**
2. **Upload files**
3. **Install dependencies**
4. **Run application**

---

## 🖥️ Simple Text Editors + Terminal

### Any Text Editor + Terminal:
1. **Edit files** in your favorite editor (Notepad++, Vim, Emacs, etc.)
2. **Use separate terminal** for running:
```bash
cd your-project-folder
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

---

## 🚀 Quick Start for Any IDE

### Universal Steps:
1. **Open project folder** in your IDE
2. **Create virtual environment**: `python -m venv venv`
3. **Activate virtual environment**:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. **Install dependencies**: `pip install -r requirements.txt`
5. **Run application**: `python app.py`
6. **Open browser**: http://localhost:5000

### IDE-Specific Benefits:
- **VS Code**: Best overall experience, free
- **PyCharm**: Professional features, excellent debugging
- **Jupyter**: Great for experimenting and data analysis
- **Sublime**: Lightweight and fast
- **Online IDEs**: No local setup required

Choose the IDE you're most comfortable with - they all work great! 🎉