"""Streamlit Cloud entrypoint. Locally you can also run: streamlit run frontend.py"""

from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).resolve().parent / "frontend.py"), run_name="__main__")
