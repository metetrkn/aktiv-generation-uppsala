# En värld för alla 🌍

## Om Organisationen

**Aktiv Generation Uppsala** är en ideell och politiskt obunden förening som främjar barns och ungas utveckling genom att skapa en inkluderande och stödjande gemenskap. Vi erbjuder mötesplatser och aktiviteter där unga kan dela med sig av sina erfarenheter, utveckla sig själva och stötta yngre generationer. Genom våra olika aktiviteter arbetar vi för att främja samarbeten mellan barn, mentorer och familjer samt främja socialt ansvar, miljö- och humanitärt bistånd och kulturell förståelse.

---

## Features
  - Secure Internal Mailing System
  - Photo Management System
  - Multilingual Support
  - Dark/Night Mode
  - Responsive & Modern Design for different type of devices
  - Role-Based Access Control
  - Customizable Activities & Events
  - Privacy & Cookie Policy Management
  - Admin Dashboard
  - Automated Testing & CI/CD


## Project Structure

```
aktiv-generation-uppsala/
├── apps/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── context_processors.py
│   │   ├── models.py
│   │   ├── static/
│   │   │   └── core/
│   │   │       ├── css/
│   │   │       │   ├── cookies.css
│   │   │       │   ├── navbar.css
│   │   │       │   ├── nightmode.css
│   │   │       │   ├── privacy_policy.css
│   │   │       │   └── style.css
│   │   │       ├── favicon.ico
│   │   │       ├── images/
│   │   │       │   ├── background.png
│   │   │       │   ├── logo.png
│   │   │       │   └── om-oss.jpeg
│   │   │       └── js/
│   │   │           ├── nightmode.js
│   │   │           ├── script.js
│   │   │           └── swiperScript.js
│   │   ├── templates/
│   │   │   └── core/
│   │   │       ├── base.html
│   │   │       └── includes/
│   │   │           ├── cookies.html
│   │   │           ├── mail-us.html
│   │   │           ├── navbar.html
│   │   │           └── privacy_policy.html
│   │   ├── urls.py
│   │   └── views.py
│   ├── mail/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   │   └── 0001_initial.py
│   │   ├── models.py
│   │   ├── static/
│   │   │   └── mail/
│   │   │       └── css/
│   │   │           └── mail-us.css
│   │   ├── templates/
│   │   │   ├── admin/
│   │   │   │   └── mail/
│   │   │   │       ├── adminreply/
│   │   │   │       │   ├── add_form.html
│   │   │   │       │   └── change_form.html
│   │   │   │       └── message/
│   │   │   │           └── change_form.html
│   │   │   └── mail/
│   │   │       ├── mail-reply.html
│   │   │       └── mail-us.html
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── photo/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── management/
│       │   ├── __init__.py
│       │   └── commands/
│       │       ├── __init__.py
│       │       ├── import_media_images.py
│       │       └── import_static_images.py
│       ├── migrations/
│       │   ├── __init__.py
│       │   ├── 0001_initial.py
│       │   └── 0002_photo_url_path_alter_photo_image.py
│       ├── models.py
│       ├── tests.py
│       └── views.py
├── configuration/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .env.example
├── manage.py
├── media/
├── poetry.lock
├── pyproject.toml
├── README.md
└── staticfiles/
```

## Tech Stack 💻

### Backend & Database
- Python (Django)
- PostgreSQL (or your DB of choice)

### Infrastructure & Deployment
- Render (CI/CD + Web App Hosting)
- Railway (eller annan tjänst) → Database Hosting

### Frontend & Assets
- HTML, CSS, JavaScript (Django templates)

---

## Getting Started 🏁

### System Requirements, Recommended 🔧

- **Windows**: Windows 10 or later (64-bit)
- **macOS**: macOS 10.15 (Catalina) or later
- **Linux**: Ubuntu 20.04 LTS, Debian 11, or equivalent
- **Python**: 3.10.x (required, not compatible with Python 4.0+)
- **Package Manager**: Poetry (latest version)
- **Database**: PostgreSQL 17.5
- **Libraries**: Automatically handled by poetry (via poetry.lock and pyproject.toml files)

### How to install the Project

#### Windows Users - Automatic

```
❗ setup.bat file clones project folder into the aktiva-generation-uppsala folder in the current directory, if project alreaady did not cloned.

1️⃣ Download setup.bat file from Github project

➖ Double click to run setup.bat

⚠️ You’ll likely get a Windows SmartScreen warning running setup.bat. To proceed, select “More info” → “Run anyway.”

!!OR!!

✅ Recommendation for smoother execution:
Right-click setup.bat → Run as Administrator
```

#### Windows Users - Manual

```sh
# Install Python (version used in this project)
choco install python --version=3.10.0

# Ensure the installed Python is in PATH before continuing
refreshenv

# Option 2: Manual installation from python.org
  1. Download Python 3.10.0 installer from:
    https://www.python.org/downloads/release/python-3100/

  2. Run the installer:
    - Check "Add Python 3.10 to PATH" before clicking Install.
    - Or manually add the installation path to the System Environment Variable called Path.

# Install Poetry
pip install poetry

# (Optional) Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Clone the project
git clone git@github.com:your-org/your-repo.git
cd your-repo

# Install dependencies
poetry install
```

#### Linux / macOS Users

```sh
# Ubuntu/Debian
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update
sudo apt-get install python3.10 python3.10-venv python3-pip

# macOS (using Homebrew)
brew install python@3.10

# Ensure you're using Python 3.10
python3.10 --version

# Install Poetry
python3.10 -m pip install poetry

# (Optional) Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Clone the project
git clone git@github.com:metetrkn/aktiv-generation-uppsala.git
cd your-repo

# Install dependencies
poetry install
```

---

### Environment Variables ⚙️
```sh
cp .env.example .env
# Edit .env with your local settings (e.g., database credentials, secret key)
```

### Media - Images ⚙️
```sh
move "media-" "media"
# Change media- folder (contains mock images) name to media, mock images can be replaced via admin interface photos application


---

### Database Setup 🗄️

By default, Django uses SQLite, but for production or advanced local development, you may want to use PostgreSQL or another database.

**PostgreSQL (version 17.5) Example:**

```sh
# Install PostgreSQL
# Windows: Download from https://www.postgresql.org/download/windows/
# Ubuntu/Debian:
sudo apt-get install postgresql postgresql-contrib
# macOS:
brew install postgresql

# Create a database and user (replace <user> and <db> with your values)
sudo -u postgres createuser <user> --pwprompt
sudo -u postgres createdb <db> --owner=<user>

# Update your .env or configuration/settings.py with the correct DB credentials
```

---

### How to Run the Project

```sh
# Activate virtual environment
poetry shell

# Run migrations
poetry run python manage.py migrate

# (Optional) Collect static files (for production or if needed)
poetry run python manage.py collectstatic

# Start the development server
poetry run python manage.py runserver
```

The application will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

### Superuser/Admin Account 👤

To access the Django admin panel, create a superuser and use this credentials to sign-in this admin url:
```
your_base_local_url/
---

```sh
poetry run python manage.py createsuperuser
# Follow the prompts to set username, email, and password
```

---

## Project Structure 📁

```
apps/
  core/    - Main application
  mail/    - Handles mail and messaging features
  photo/   - Photo management and uploads
configuration/ - Django settings, URLs, WSGI
manage.py  - Django management script
media/     - User uploaded media files
staticfiles/ - Collected static files
```

---

## Development Commands 🔧

### System & Dependencies

```sh
poetry install         # Install dependencies
poetry shell           # Activate virtual environment
```

### Local Development

```sh
make local-run         # Start Django development server
```

### Database Operations

```sh
make db-init           # Initialize database
# ... other database commands
```

### Code Quality & Pre-commit Hooks

Before committing your changes, ensure:

- Code follows our style guide (`make quality-check-all`)
- All quality checks pass

`make quality-check-all` performs a comprehensive check of your code:

#### Code Style & Formatting

- `black`: Enforces consistent code formatting
- `isort`: Organizes imports according to PEP8

To fix formatting errors:

```sh
make quality-format  # Fixes code formatting errors only (black, isort)
```

To modify files in place and removes unused imports/variables flagged by flake8.
```sh
poetry run autoflake --remove-all-unused-imports --remove-unused-variables --in-place -r apps/core apps/mail apps/photo
```

#### Code Quality & Analysis

- `flake8`: Checks for style guide violations
- `pylint`: Analyzes code complexity and potential issues
- `mypy`: Performs static type checking
- `vulture`: Detects unused code

#### Testing

- `pytest`: Runs the complete test suite

#### Security

- `bandit`: Scans for common security issues
- `safety`: Checks dependencies for known vulnerabilities

### Pre-commit Hooks (Optional)

```sh
poetry run pre-commit install
```

This ensures code quality checks run automatically before each commit.

> **Note:** These checks are mandatory for:
> - Creating pull requests
> - Passing CI/CD pipeline (automatically runs on every commit/push)
> - Maintaining code quality standards

---

## Troubleshooting & Common Issues 🛠️

- **Python/Poetry not found:**
  - Ensure Python 3.10 and Poetry are installed and available in your PATH.
- **Database connection errors:**
  - Double-check your .env or settings for correct database credentials.
  - Ensure your database server is running.
- **Static files not loading:**
  - Run `poetry run python manage.py collectstatic` and ensure your static and media directories are correctly configured.
- **Migration issues:**
  - Try `poetry run python manage.py makemigrations` and `poetry run python manage.py migrate`.
- **Permission errors:**
  - On Linux/macOS, you may need to adjust file permissions or use `sudo` for some commands.

---

## Development Workflow

1. Create a feature branch
2. Make your changes
3. (Optional) To push/pull request without quality check
   ```sh
   git push --no-verify origin your_branch_name
   ```
4. Run quality checks:
   ```sh
   make quality-check-all
   ```
5. Commit your changes (pre-commit hooks will run automatically)
6. Create a pull request (CI will run all checks)
7. After review and approval, merge to main branch

> **Note:** All pull requests must pass:
> - Code quality checks
> - Security checks
> - Test coverage requirements
> - Documentation updates (if applicable)

---

## 📝 Commit Message Format

We use file-based commit messages for clarity and simplicity:

```
<path/to/file>: <description>
```

**Examples:**

```sh
# Update model
organizations/models.py: Add is_active field to organization model

# Fix template
core/templates/landing.html: Fix home page broken link

# Multiple files example - Add feature
core: Add password reset feature
- Add view in views.py
- Add URL pattern in urls.py
- Add template in templates/

# Multiple files example - Update something
core: Update user authentication flow
- Add login/logout views in views.py
- Update URL patterns in urls.py
- Add authentication middleware
- Update templates for auth pages
```

> Keep descriptions concise but descriptive. If the change affects multiple files, use the common directory name.

---

## Deployment 🚀

Coming soon!

---

## Credit

This project is developed by [@MeteTurkan](https://github.com/metetrkn)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

