# GitHub Copilot Instructions for Site Project

## 🏗️ Project Architecture

Це Flask веб-додаток для інтернет-магазину техніки з системою управління замовленнями та відгуків.

### Key Components:
- **Frontend**: HTML шаблони в `templates/` з Jinja2
- **Backend**: Flask в `app.py` з SQLAlchemy ORM
- **Database**: SQLite (`db.sqlite`) з таблицями: products, orders, feedback, accounts
- **API**: REST API в `routes/api/` для versioned endpoints (`/api/v1/`)
- **Routes**: Блюпринти в `routes/` для модульної структури

## 📁 File Structure & Responsibilities

```
site/
├── app.py                 # Flask app initialization, blueprint registration
├── models.py              # Database connection & CRUD functions
├── requirements.txt       # Python dependencies
├── db.sqlite             # SQLite database
├── routes/
│   ├── __init__.py       # Blueprints initialization
│   ├── shop.py           # Shop/catalog functionality
│   ├── accounts.py       # User authentication & accounts
│   ├── feedback.py       # Feedback collection & display
│   ├── admin.py          # Admin panel functionality
│   ├── api/              # REST API endpoints (NEW)
│   │   ├── __init__.py
│   │   ├── products.py   # GET/POST/PUT/DELETE /api/v1/products
│   │   ├── orders.py     # GET/POST /api/v1/orders
│   │   ├── feedback.py   # GET/POST /api/v1/feedback
│   │   ├── users.py      # GET/POST /api/v1/users
│   │   └── errors.py     # Error handling utilities
│   └── __pycache__/
├── templates/            # Jinja2 HTML templates
│   ├── base.html        # Base template with navigation
│   ├── home.html        # Homepage
│   ├── shop.html        # Product catalog
│   ├── cart.html        # Shopping cart
│   ├── feedback.html    # Feedback form
│   ├── accounts.html    # Login/register
│   ├── admin.html       # Admin dashboard
│   └── order_details.html
└── static/              # CSS, JS, images (when needed)
```

## 🔄 Data Flow Patterns

### When editing API routes:
1. **API Layer** (`routes/api/products.py`) - handles HTTP requests, validation
2. **Data Layer** (`models.py`) - database operations via direct SQL or SQLAlchemy
3. **Response Format** - always JSON with `{status, data/message}` structure

Example pattern:
```python
# In routes/api/products.py
@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'status': 'error', 'message': 'Not found'}), 404
        return jsonify({'status': 'success', 'data': product.to_dict()}), 200
    except Exception as e:
        return error_handler(e, 500)
```

## 🎯 Common Workflows

### Adding a New API Endpoint:
1. **Identify resource** (products, orders, feedback, users)
2. **Create route** in `routes/api/{resource}.py`
3. **Add blueprint** registration in `app.py` with `/api/v1/{resource}` prefix
4. **Add documentation** using docstring with `---` for Flasgger Swagger integration
5. **Add error handling** using `error_handler()` utility from `errors.py`

### Modifying Database Schema:
1. Update table creation in `models.py` `init_db()` function
2. Create migration if needed (currently manual)
3. Update model definitions (SQLAlchemy ORM models if used)
4. Update CRUD functions in models.py

### Testing API:
- Use Postman collection (to be created in `tests/postman_collection.json`)
- Test endpoints manually: `curl http://localhost:5000/api/v1/products`
- Check response format: `{"status": "success", "data": [...]}`

## 🛠️ Conventions & Patterns

### Naming:
- **Routes/endpoints**: kebab-case (`/api/v1/order-items`)
- **Functions**: snake_case (`get_all_products()`)
- **Variables**: snake_case
- **Classes**: PascalCase (Flask/SQLAlchemy models)

### Error Handling:
Always use `error_handler(exception, status_code)` from `routes/api/errors.py`:
```python
except Exception as e:
    return error_handler(e, 500)
```

### Response Format:
**Success**: `{"status": "success", "data": {...}, "message": "..."}`
**Error**: `{"status": "error", "message": "...", "code": 400}`

### Database Operations:
- Direct SQL in `models.py` with connection pooling via `get_db_connection()`
- Also uses SQLAlchemy ORM for new code (`db.session` in app.py context)
- Always close connections: `conn.close()`

## 📋 File Location Rules for "Apply in Editor"

When suggesting code changes:
1. **For Flask routes** → `routes/{module_name}.py` or `routes/api/{resource}.py`
2. **For database functions** → `models.py`
3. **For templates** → `templates/{page_name}.html`
4. **For main app** → `app.py`
5. **For dependencies** → `requirements.txt`

**Always specify the full absolute path** when making suggestions:
`d:\OneDrive\Робочий стіл\site\routes\api\products.py`

## 🔗 Key Integration Points

1. **Session Management**: Using `session` object from Flask (see `accounts.py`)
2. **Database Context**: All operations need `db.session.commit()` or connection close
3. **Blueprint Registration**: All new blueprints must be registered in `app.py`
4. **Swagger Docs**: Routes with docstrings containing `---` auto-generate docs

## 📌 Current Status (Lab 4-5)
- ✅ Basic Flask app with SQLite database
- ✅ CRUD operations for products, orders, feedback
- ✅ Blueprint-based modular structure
- 🚧 REST API in development (`/api/v1/` prefix)
- 📝 Swagger documentation via Flasgger
- ⏳ Postman tests and API documentation

## ⚠️ Important Notes
- **Secret Key**: Currently hardcoded in `app.py` - use environment variables in production
- **Database**: Currently uses mixed approach (raw SQL + SQLAlchemy) - migrate fully to ORM
- **Validation**: Add input validation decorators in `routes/api/errors.py`
- **Authentication**: Implement JWT or session-based auth in future versions
