import sys

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool

load_dotenv()

sys.stdout.reconfigure(encoding="utf-8")

# book seat
