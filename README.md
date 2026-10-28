# Web Log Analysis Using MapReduce Concepts

## Included
- `app.py`: Streamlit dashboard and local MapReduce-style counting logic.
- `requirements.txt`: required Python libraries.
- `data/access.log`: sample web-server log file.
- `project-report.md`: editable report draft.
- `viva-questions.md`: viva practice questions.

## Run on Windows (quick setup)
1. Extract the ZIP.
2. Open the extracted `WebLogAnalysis` folder in VS Code.
3. Choose Terminal → New Terminal.
4. Check Python: `python --version` (or `py --version`).
5. Create environment: `python -m venv .venv`
6. Activate: `.venv\Scripts\activate`
   - If blocked in PowerShell, open a Command Prompt terminal and run `.venv\Scripts\activate.bat`.
7. Install packages: `python -m pip install -r requirements.txt`
8. Start dashboard: `python -m streamlit run app.py`
9. If the browser does not open, visit `http://localhost:8501`.
10. Stop with `Ctrl+C`.

## Sample log format
Apache/Nginx Common or Combined Log Format, for example:
`192.168.1.10 - - [28/Oct/2026:10:20:30 +0530] "GET /home HTTP/1.1" 200 1234`

The included sample file means you do not need to download a dataset.

## Important scope note
The Streamlit starter app implements mapper/reducer-style key-value aggregation locally in Python. It demonstrates the MapReduce idea, but it is **not itself a Hadoop execution**. If your faculty requires actual Hadoop MapReduce, use the optional Hadoop Streaming approach below and confirm that the environment is available.

## Optional: genuine Hadoop Streaming (only if Hadoop is already installed)
Hadoop Streaming lets Hadoop run mapper and reducer scripts. The usual command needs a working Hadoop installation, Java, and the Streaming JAR; exact paths depend on the installed Hadoop version. Do not attempt this optional route unless Hadoop is installed and configured.

Create `mapper.py`:
```python
#!/usr/bin/env python3
import re, sys
for line in sys.stdin:
    m = re.match(r'^(\\S+) \\S+ \\S+ \\[[^\\]]+\\] "([^"]*)" (\\d{3})', line)
    if not m:
        continue
    request = m.group(2).split()
    page = request[1] if len(request) > 1 else "/"
    print(f"{page}\\t1")
```

Create `reducer.py`:
```python
#!/usr/bin/env python3
import sys
current, total = None, 0
for line in sys.stdin:
    key, value = line.rstrip("\\n").split("\\t", 1)
    value = int(value)
    if current is not None and key != current:
        print(f"{current}\\t{total}")
        total = 0
    current = key
    total += value
if current is not None:
    print(f"{current}\\t{total}")
```

This is a template only; a real Hadoop Streaming run needs the configured Hadoop installation and its Streaming JAR. The primary app does not require Hadoop.
