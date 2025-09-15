import os
import uvicorn
from app.main import app


if __name__ == "__main__":
	port = int(os.getenv("PORT", "8000"))
	reload = os.getenv("ENV", "dev") == "dev"
	uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=reload)


