import os
from os.path import join, dirname
from dotenv import load_dotenv

# 環境変数設定
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

PINATA_API_KEY = os.environ.get("PINATA_API_KEY")
PINATA_API_SECRET = os.environ.get("PINATA_API_SECRET")
PINATA_JWT = os.environ.get("PINATA_JWT")
PUBLIC_GATEWAY_URL=os.environ.get("PUBLIC_GATEWAY_URL")
