# ALPR San Diego — Flask Backend

Matches the Vue 3 frontend with four pages: Home, Learn, News, Get Involved.

## Project Structure

```
flask_app/
├── app/
│   ├── __init__.py              # App factory + CORS
│   ├── config.py                # Dev/Test/Prod configs
│   ├── api/v1/
│   │   ├── news.py              # GET /api/v1/news
│   │   ├── learn.py             # GET /api/v1/learn
│   │   ├── involvement.py       # GET /api/v1/get-involved
│   │   └── seed.py              # Sample data seeder
│   ├── models/
│   │   ├── news.py              # NewsArticle
│   │   ├── learn.py             # LearnArticle
│   │   └── involvement.py       # InvolvementItem
│   └── utils/responses.py
├── frontend_additions/
│   ├── api.js                   # → copy to frontend/src/services/api.js
│   └── vite.config.js           # → replace frontend/vite.config.js
├── run.py
└── requirements.txt
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/news | Paginated news articles (`?page=1&per_page=10`) |
| GET | /api/v1/news/:id | Single news article |
| GET | /api/v1/learn | All learn articles (`?category=privacy`) |
| GET | /api/v1/learn/categories | Distinct categories |
| GET | /api/v1/learn/:slug | Single learn article by slug |
| GET | /api/v1/get-involved | Active items (`?type=petition`) |
| GET | /api/v1/get-involved/:id | Single involvement item |

All responses follow the shape:
```json
{ "success": true, "message": "Success", "data": { ... } }
```

## Setup

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

flask --app run db init
flask --app run db migrate -m "initial"
flask --app run db upgrade

# Seed sample data
flask --app run shell
>>> from app.api.v1.seed import seed; seed()

python run.py
```

## Frontend Integration

1. Copy `frontend_additions/api.js` → `src/services/api.js` in your Vue project
2. Replace `vite.config.js` with `frontend_additions/vite.config.js` (adds `/api` proxy)
3. Use in any view:

```js
import { api } from '@/services/api'

const { articles } = await api.getNews()
const { articles: learnArticles } = await api.getLearnArticles('privacy')
const { items } = await api.getInvolvement()
```

## Production

```bash
# Set in .env:
CORS_ORIGINS=https://yourdomain.com
DATABASE_URL=postgresql://user:pass@host/dbname

gunicorn -w 4 -b 0.0.0.0:8000 "run:app"
```
