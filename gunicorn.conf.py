import os
from dotenv import load_dotenv


bind = "0.0.0.0:8000"
workers = 4

environment = "local"
# os.getenv("ENVIRONMENT")
# --env-file .local.env

env = os.path.join(os.getcwd(), f".{environment}.env")
if os.path.exists(env):
    load_dotenv(env)
