### Hexlet tests and linter status:
[![Actions Status](https://github.com/Pikachy337/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Pikachy337/python-project-52/actions)
[![Python CI](https://github.com/Pikachy337/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/Pikachy337/python-project-52/actions/workflows/pyci.yml)
<a href="https://qlty.sh/gh/Pikachy337/projects/python-project-52"><img src="https://qlty.sh/badges/00de5bbb-b1f0-4722-8fb8-dcb815e9266e/maintainability.svg" alt="Maintainability" /></a>
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Pikachy337_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Pikachy337_python-project-52)  
[My deployment project](https://hexlet-code-huv8.onrender.com)


A task manager with full CRUD operations for managing:
- Users
- Tasks
- Statuses
- Labels

## Key Features
- User authentication and authorization
- Task filtering by statuses, assignees and labels
- Responsive Bootstrap 5 interface
- Deployment on Render.com with PostgreSQL
- Error monitoring via Rollbar

## Technology Stack
**Backend**: Django 4.2  
**Frontend**: Bootstrap 5, Django Templates  
**Database**: PostgreSQL (production), SQLite (development)  
**Infrastructure**: Render.com (PaaS)  
**Additional components**: Whitenoise, dj-database-url, python-dotenv

## Development Setup

1. Clone the repository:
```bash
https://github.com/Pikachy337/python-project-52.git
cd python-project-52
```
2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Configure environment variables (create .env file):
```ini
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```
5. Apply migrations:
```bash
python manage.py migrate
```
6. Run development server:
```bash
make dev
```