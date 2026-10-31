# Restaurant Service

Manages restaurant profiles and menus — Online Food Ordering System.

## Tech Stack
- **Runtime**: Python 3.11
- **Framework**: FastAPI
- **Database**: MongoDB (PyMongo)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/restaurants` | Register restaurant |
| GET | `/api/restaurants` | List restaurants |
| GET | `/api/restaurants/{id}` | Get restaurant + menu |
| PUT | `/api/restaurants/{id}` | Update restaurant |
| DELETE | `/api/restaurants/{id}` | Deactivate restaurant |
| POST | `/api/restaurants/{id}/menu` | Add menu item |
| PATCH | `/api/restaurants/{id}/menu/{itemId}` | Update menu item |
| DELETE | `/api/restaurants/{id}/menu/{itemId}` | Remove menu item |

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 3002
```

## Swagger UI
Visit `http://localhost:3002/docs` for interactive API docs.

## Docker
```bash
docker build -t restaurant-service .
docker run -p 3002:3002 --env-file .env restaurant-service
```
