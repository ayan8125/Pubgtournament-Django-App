# Pubgtournament Django App

A web-application built with Django (plus JavaScript/HTML/CSS frontend) to manage tournaments — suitable for gaming events like PUBG (or similar), including user management, tournament creation, match scheduling and result tracking.  

## 🚀 Project Overview  
This project provides a full-stack solution to create, manage, and run gaming tournaments online. With modules for user authentication, tournament and game-management logic, and a responsive frontend UI, it aims to simplify the workflow for organising gaming events — from registering players to scheduling matches and tracking results.

### Why this project exists  
Many community-run tournaments or amateur e-sports events lack an easy-to-use, ready-made platform. This app serves as a minimal-effort template — developers or event organisers can clone and customize it to suit their own game (not necessarily limited to PUBG), tweak the tournament rules, adjust UI, and deploy it quickly. It’s ideal as a prototype or MVP to build upon.

## 📦 Features  

- User registration & authentication (via Django)  
- Tournament creation and management (create tournaments, define rules/settings)  
- Game/match management (including scheduling, result submission)  
- Basic frontend using HTML / CSS / JS — easy to customize and extend  
- SQLite database by default (easy for quick local setup)  

## 🛠️ Tech Stack  

- Backend: Python, Django  
- Frontend: HTML, CSS/SCSS, JavaScript  
- Database: SQLite (default)  
- (Optionally you can migrate to PostgreSQL/MySQL for production)  

## 🔧 Getting Started (Local Setup)  

1. Clone the repository  
   ```bash
   git clone https://github.com/ayan8125/Pubgtournament-Django-App.git
   cd Pubgtournament-Django-App
   ```

2. (Recommended) Create a virtual environment and activate it
```
python -m venv venv
source venv/bin/activate   # on Windows use `venv\Scripts\activate`

```
3. Install dependencies
```
pip install -r requirements.txt

```

4. Apply migrations
```
python manage.py migrate

```

5. (Optional) Create a superuser (for admin access)
```
python manage.py createsuperuser
```

6. Run the development server
```
python manage.py runserver

```
7.  Open your browser at http://127.0.0.1:8000/ — you should see the application alive.

## 🧑‍💻 Usage

- Register a new user or login (if you created superuser)

- Navigate to “Tournaments” section to create a new tournament — define name, rules, schedule, participants etc.

- Manage games/matches under each tournament: schedule matches, update results, track standings (you may need to customise as per game logic)

- (Optional) Extend or tweak frontend UI (HTML/CSS/JS) or backend logic (models, views) as per your needs

## ⚠️ Known Limitations / To-Do

- Default DB is SQLite — fine for testing or small tournaments, but not ideal for production or large user base. Consider migrating to PostgreSQL/MySQL.

- No built-in support for real-time updates or live match tracking: all operations are manual through web UI.

- Frontend is basic — no polished design or responsive UI out-of-the-box. Might require CSS/JS overhaul for production-grade look.

- No automated tests — adding Django unit tests / integration tests is recommended.

## 🤝 Contributing

- Contributions are welcome! If you want to contribute:

- Fork the repo

- Create a new branch for your feature/bugfix

- Make changes and test thoroughly

- Open a pull request describing your changes

## You might consider adding:

- Docker / Docker-Compose setup for easier deployment

- Support for PostgreSQL / production-ready settings

- Better UI (responsive layout, user-friendly design)

- Automated testing suite (unit + integration tests)

- Role-based user permissions (admin / moderator / player)


