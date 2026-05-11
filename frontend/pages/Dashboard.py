import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
exec(open("frontend/templates/dashboard.py").read())