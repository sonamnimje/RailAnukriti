import os
from dotenv import load_dotenv


load_dotenv()



class Settings:
	APP_NAME: str = os.getenv("APP_NAME", "RailAnukriti")
	ENV: str = os.getenv("ENV", "dev")
	API_PREFIX: str = os.getenv("API_PREFIX", "/api")
	SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-secret")
	ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
	JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

	DB_TYPE: str = os.getenv("DB_TYPE", "sqlite")  # 'sqlite' or 'postgresql'
	DB_HOST: str = os.getenv("DB_HOST", "localhost")
	DB_PORT: str = os.getenv("DB_PORT", "5432")
	DB_USER: str = os.getenv("DB_USER", "postgres")
	DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
	DB_NAME: str = os.getenv("DB_NAME", "rail")
	# Optional explicit path for SQLite files (useful on platforms with read-only project dirs)
	SQLITE_PATH: str | None = os.getenv("SQLITE_PATH")

	SQLALCHEMY_ECHO: bool = os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"

	@property
	def sync_database_uri(self) -> str:
		if self.DB_TYPE == "sqlite":
			# Prefer explicit SQLITE_PATH. On Render or non-dev, default to /var/data which is writable.
			if self.SQLITE_PATH:
				db_path = self.SQLITE_PATH
			else:
				is_render = os.getenv("RENDER") is not None
				# On Render, the writable location is /tmp; avoid /var/data which may be readonly
				if is_render or self.ENV != "dev":
					base_dir = "/tmp"
				else:
					base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
				db_path = os.path.join(base_dir, f"{self.DB_NAME}.db")
			# Ensure directory exists to avoid OperationalError on first run
			os.makedirs(os.path.dirname(db_path), exist_ok=True)
			return f"sqlite:///{db_path}"
		return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

	@property
	def async_database_uri(self) -> str:
		if self.DB_TYPE == "sqlite":
			if self.SQLITE_PATH:
				db_path = self.SQLITE_PATH
			else:
				is_render = os.getenv("RENDER") is not None
				# On Render, the writable location is /tmp; avoid /var/data which may be readonly
				if is_render or self.ENV != "dev":
					base_dir = "/tmp"
				else:
					base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
				db_path = os.path.join(base_dir, f"{self.DB_NAME}.db")
			os.makedirs(os.path.dirname(db_path), exist_ok=True)
			return f"sqlite+aiosqlite:///{db_path}"
		return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()


