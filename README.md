python -m venv venv

source venv/Scripts/activate

pip install -r requirements.txt

uvicorn app.main:app --reload

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc