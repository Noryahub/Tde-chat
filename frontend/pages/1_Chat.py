import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

exec(open(os.path.join(os.path.dirname(__file__), "../templates/app_streamlit.py"), encoding="utf-8").read())