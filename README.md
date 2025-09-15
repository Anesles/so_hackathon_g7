## Wine Price Intelligence Platform (so_hackathon_g7)

A small full‑stack project that aggregates wine product data from multiple retailers, stores it in MySQL, and exposes a simple web dashboard and API for browsing wines and comparing prices. The stack combines a Node.js/Express app with EJS views and a set of Python web‑scraping scripts.

### Key features
- **Product catalog**: Store wines with EAN, brand, sub‑brand, and capacity.
- **Price aggregation**: Python scrapers collect prices from several stores and write to the database.
- **Dashboard (EJS/Express)**: Home page lists wines and links into product detail views.
- **Authentication**: Basic login with password hashing and cookie‑based JWT session.
- **REST API**: Endpoints to fetch wines and store price snapshots.

### Repository structure
```
so_hackathon_g7/
  front/                 # Node.js + Express app (EJS views, routes, static assets)
    app.js               # App entrypoint, registers routes and view engine
    routes/              # Page, API, and user routes
    guards/              # Authentication middleware
    model/               # MySQL connection
    public/              # Static assets (CSS, images)
    views/               # EJS templates (home, login, add/remove forms, product page)
  webscraping/           # Python scrapers (requests/selenium/bs4)
  requirements.txt       # Python dependencies for scrapers
  README.md              # You are here
```

### Tech stack
- **Frontend/Server**: Node.js, Express, EJS, Axios, Body‑Parser
- **Auth**: bcrypt, jsonwebtoken, HTTP‑only cookies
- **Database**: MySQL
- **Scraping**: Python, Requests, BeautifulSoup4, Selenium

### Data model (high‑level)
- `wines` table: `EAN` (primary key), `name`, `capacity`, `Brand`, `Subrand`
- `scrape` table: price records keyed by `EAN` plus store metadata and timestamp

You can review the insert/remove logic in `front/routes/api.js` for exact field usage.

### Getting started
Prerequisites:
- Node.js 18+
- Python 3.10+
- MySQL 5.7+/8.0+

1) Backend and dashboard (Node/Express)
```
cd front
npm install
npm start
```
- App defaults to `http://localhost:3000`.
- Static assets are served from `front/public` and views from `front/views`.

2) Database configuration
- Connection is defined in `front/model/database.js`.
- Update `host`, `user`, `password`, and `database` to match your environment.
- Suggested tables (align with code in `front/routes/api.js`):
  - `wines (EAN BIGINT PRIMARY KEY, name VARCHAR(255), capacity VARCHAR(50), Brand VARCHAR(255), Subrand VARCHAR(255))`
  - `scrape (id INT AUTO_INCREMENT PRIMARY KEY, EAN BIGINT, StoreName VARCHAR(255), Price DECIMAL(10,2), Date DATETIME, ... )`

3) Python scrapers
```
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cd webscraping
python continente.py         # run any scraper script as needed
```
- Ensure scrapers write into the same MySQL schema used by the Node app.

### Application routes
- Pages (`front/routes/route.js`):
  - `GET /` → Home (requires auth) – renders wine list via `/api/vinhos`
  - `GET /login` → Login form
  - `GET /addProduto` → Add wine form (requires auth)
  - `GET /removeProduto` → Remove wine form (requires auth)
  - `GET /Produto` → Example chart page (placeholder data)

- API (`front/routes/api.js`, mounted at `/api`):
  - `GET /api/vinhos` → Returns all wines plus their store price data
  - `GET /api/vinho?EAN=...` → Renders product page with price history/details
  - `POST /api/submit` → Insert a new wine (requires auth)
  - `POST /api/remove` → Remove wine and related price data

- Auth (`front/routes/user.js`, mounted at `/user`):
  - `POST /user/login` → Login, sets JWT cookie
  - `GET /user/logout` → Clear session cookie
  - `POST /user/register` → Register new user (protected by auth guard)

### Authentication
- Passwords are hashed with bcrypt.
- Sessions use a JWT stored in an HTTP‑only cookie.
- Protected routes use the middleware in `front/guards/autenticate.js`.

### Environment configuration
For local development, consider moving secrets and DB settings to environment variables (e.g., via `.env`) and loading them in `front/model/database.js`. Example variables:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=wines
JWT_SECRET=change_me
PORT=3000
```

### Screenshots
- See `front/public/images/localhost_3000.png` for the dashboard landing page.

### Troubleshooting
- Port already in use: stop other processes on 3000 or set `PORT`.
- Cannot connect to DB: verify credentials in `front/model/database.js` and that MySQL is reachable.
- Empty dashboard: ensure scrapers have populated `wines` and `scrape` tables.