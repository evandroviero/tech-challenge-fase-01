import os
from dotenv import load_dotenv

load_dotenv()

users = {
    os.getenv("USER1_USERNAME"): os.getenv("USER1_PASSWORD"),
    os.getenv("USER2_USERNAME"): os.getenv("USER2_PASSWORD")
}