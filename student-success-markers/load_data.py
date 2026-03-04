import pandas as pd
import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus

def load_dotenv() -> None:
	try:
		__import__("dotenv").load_dotenv()
	except Exception:
		return None


def get_database_url() -> str:
	load_dotenv()
	database_url = os.getenv("DATABASE_URL")
	if database_url:
		return database_url

	host = os.getenv("PGHOST", "localhost")
	port = os.getenv("PGPORT", "5432")
	database = os.getenv("PGDATABASE", "UCI_Student_Info")
	user = os.getenv("PGUSER", "postgres")
	password = quote_plus(os.getenv("PGPASSWORD", ""))
	return f"postgresql://{user}:{password}@{host}:{port}/{database}"


engine = create_engine(get_database_url())

df = pd.read_csv('student-mat.csv', sep=';')

df.columns = df.columns.str.lower()

df.to_sql('raw_students', engine, if_exists='replace', index=False)

print(f"Loaded {len(df)} rows successfully")