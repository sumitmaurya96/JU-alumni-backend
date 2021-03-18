from dotenv import load_dotenv
from os.path import join, dirname
import os


dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

EMAIL = os.environ.get("LINKEDIN_EMAIL")
PASSWORD = os.environ.get("LINKEDIN_PASSWORD")
