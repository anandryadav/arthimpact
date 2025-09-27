## Vendor Management API (FastAPI, DDD, API v1)

A comprehensive vendor and service contract management system with automated reminders, built using FastAPI, Domain-Driven Design (DDD) architecture, and API versioning.

### Features
- **JWT Authentication** with argon2 password hashing
- **Vendor Management** with full CRUD operations
- **Service Contract Management** with status tracking
- **Automated Reminders** for expiring contracts and payment due dates
- **Email Notifications** (configurable via SMTP)
- **Color-coded Flags** for contract status visualization
- **Pagination** for all listing endpoints
- **Interactive API Documentation** with Swagger UI
- **Domain-Driven Design** architecture
- **API Versioning** (v1)

### Setup
1. **Python 3.11+ recommended** (tested on 3.13):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment** (optional):
   - The system comes with a secure default JWT secret key
   - For production, set `SECRET_KEY` in `.env` file
   - Configure SMTP settings for email notifications

3. **Run the server**:
   ```bash
   ./run.sh
   ```
   - **API Documentation**: `http://localhost:8000/docs`
   - **Health Check**: `http://localhost:8000/healthz`

### Authentication
- **OAuth2 password flow** with JWT tokens
- **argon2 password hashing** (no 72-byte limit like bcrypt)
- **Secure JWT secret key** pre-configured
- **Token expiration**: 24 hours by default
- **Registration**: `POST /api/v1/auth/register`
- **Login**: `POST /api/v1/auth/login`

### API v1 Endpoints
- Auth
  - `POST /api/v1/auth/register` → create user
  - `POST /api/v1/auth/login` → token

- Vendors
  - `POST /api/v1/vendors` (auth) → create vendor
  - `GET /api/v1/vendors?limit&offset` (auth) → list vendors (paginated)
  - `GET /api/v1/vendors/count?limit&offset` (auth) → count metadata
  - `GET /api/v1/vendors/{id}` (auth) → get vendor
  - `PUT /api/v1/vendors/{id}` (auth) → update vendor
  - `DELETE /api/v1/vendors/{id}` (auth) → delete vendor
  - `GET /api/v1/vendors/with-active-services?limit&offset` (auth)

- Services
  - `POST /api/v1/services/vendor/{vendor_id}` (auth)
  - `GET /api/v1/services/vendor/{vendor_id}?limit&offset` (auth)
  - `PUT /api/v1/services/{service_id}` (auth)
  - `DELETE /api/v1/services/{service_id}` (auth)
  - `POST /api/v1/services/{service_id}/status` (auth)
  - `GET /api/v1/services/expiring?days=15&limit&offset` (auth)
  - `GET /api/v1/services/payment-due?days=15&limit&offset` (auth)

- Reminders
  - `POST /api/v1/reminders/run` (auth) → run daily reminder now

### Reminder Flags and Email
- Color flags: `yellow` for within 15 days, `red` if past due/expired.
- Configure SMTP in `.env` to enable emails. Without SMTP, flags still return in API responses.

### Architecture

#### Domain-Driven Design (DDD)
- **`app/domain/`**: Repository interfaces and domain models
- **`app/application/`**: Use-case services and business logic
- **`app/infrastructure/`**: SQLAlchemy repository implementations and dependency injection
- **`app/api/v1/routers/`**: FastAPI endpoints calling application services
- **`app/core/`**: Core components (config, database, security)
- **`app/models/`**: Database entities (SQLAlchemy models)
- **`app/schemas/`**: Pydantic schemas for request/response validation
- **`app/services/`**: Service layer (email, reminders, dependencies)
- **`app/utils/`**: Utility functions (date calculations, flags)

### Database Schema
- **User**: `id, email, hashed_password, is_active, created_at`
- **Vendor**: `id, name, contact_person, email, phone, status, created_at, updated_at`
- **ServiceContract**: `id, vendor_id, service_name, start_date, expiry_date, payment_due_date, amount, status, created_at, updated_at`

### Security Features
- **argon2 password hashing**: Modern, secure password hashing without length limitations
- **JWT tokens**: Stateless authentication with configurable expiration
- **CORS enabled**: Cross-origin resource sharing configured
- **Input validation**: Pydantic schemas for request/response validation
- **SQL injection protection**: SQLAlchemy ORM with parameterized queries

### Quick Start

#### 1. Register a new user:
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"secret123"}'
```

#### 2. Login to get JWT token:
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=admin@example.com&password=secret123'
```

#### 3. Use the token for authenticated requests:
```bash
# Get vendors
curl -H "Authorization: Bearer <your-token>" \
  http://localhost:8000/api/v1/vendors/

# Create a vendor
curl -X POST http://localhost:8000/api/v1/vendors/ \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Acme Corp","contact_person":"John Doe","email":"john@acme.com","phone":"+1234567890"}'
```

### Environment Variables
```bash
# JWT Configuration (optional - secure defaults provided)
SECRET_KEY=your-secure-jwt-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Database (optional - defaults to SQLite)
DATABASE_URL=sqlite:///./app.db

# Email Configuration (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com

# Reminder Configuration (optional)
REMINDER_DAYS=15
ENABLE_SCHEDULER=1
```

### Technology Stack
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **argon2-cffi**: Secure password hashing
- **python-jose**: JWT token handling
- **SQLite**: Default database (easily replaceable with PostgreSQL/MySQL)
- **APScheduler**: Advanced Python scheduler (optional)

### Development Notes
- **SQLite**: Used for simplicity; easily replaceable with PostgreSQL/MySQL via `DATABASE_URL`
- **Scheduler**: Daily reminder scheduler disabled by default; trigger manually via `POST /api/v1/reminders/run`
- **Password Security**: Uses argon2 instead of bcrypt for better security and no password length limits
- **API Versioning**: All endpoints are versioned under `/api/v1/` for future compatibility
- **Error Handling**: Comprehensive error responses with proper HTTP status codes

### License
MIT License - see LICENSE file for details.


