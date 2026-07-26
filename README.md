# AIBridge

**Bridging People with AI**

AIBridge is an AI Adoption Platform that helps Students, Freelancers, Teachers, Professionals and Small Business Owners discover, learn, and effectively use AI tools for their goals.

---

## 1. Problem Statement

Millions of people know AI exists but struggle to:

- Choose the right AI tools for their needs
- Write effective prompts
- Learn practical AI skills
- Apply AI in their studies
- Apply AI in freelance work
- Apply AI in business

Generic tutorials and endless "top 10 AI tools" lists don't solve this — they're not personalized to a real goal.

## 2. Solution

AIBridge turns a simple description of your goal into a personalized, AI-generated action plan:

- **AI Tool Recommender** — describe your goal, get the AI tools worth using, why they help, learning resources, and concrete next steps.
- **Prompt Generator** — describe a task, get beginner / professional / advanced prompts ready to copy and paste.
- **Learning Resources** — curated resources across AI, Programming, Freelancing, Marketing and Education.
- **Dashboard** — a running history of every recommendation and prompt you've generated.

## 3. Features

- Modern, responsive, Stripe/Notion/Linear/Vercel-inspired marketing site
- AI Tool Recommender powered by Google Gemini
- Prompt Generator powered by Google Gemini
- Learning Resources library across 5 categories
- Personal dashboard with stats, charts, and activity history
- Custom SVG logo & favicon (bridge + AI spark concept)
- Lightweight scroll-reveal and hover animations (pure CSS/JS, no build step)
- Mobile-first, fully responsive layout built on Tabler
- Production-ready static file serving via WhiteNoise

## 4. AI Feature

AIBridge integrates the **Google Gemini API** via the official `google-genai` SDK ([`core/services.py`](core/services.py)):

- `get_ai_recommendations(name, user_type, goal)` — returns recommended tools, learning resources, and next steps as structured JSON.
- `generate_prompt(task)` — returns beginner, professional, and advanced prompts as structured JSON.

Both functions degrade gracefully: if `GEMINI_API_KEY` is missing or the API call fails, the page shows a friendly error instead of crashing.

## 5. Technology Stack

| Layer          | Technology                          |
|----------------|--------------------------------------|
| Backend        | Django 5.2 (LTS)                     |
| Database       | SQLite                                |
| Frontend       | Django Templates                      |
| UI Framework   | Tabler (via CDN) + custom design layer|
| AI             | Google Gemini API (`google-genai`)   |
| Fonts          | Google Fonts — Inter                  |
| Config         | python-dotenv                         |
| Static serving | WhiteNoise                            |
| WSGI server    | Gunicorn                              |

## 6. Project Structure

```
aibridge/
├── manage.py
├── requirements.txt
├── README.md
├── .env.example
│
├── static/
│   └── tabler/
│       ├── css/custom.css
│       ├── js/app.js
│       └── img/logo.svg, favicon.svg
│
├── templates/
│   ├── base.html
│   ├── home.html, about.html, dashboard.html
│   ├── recommender.html, prompt_generator.html
│   ├── resources.html, contact.html
│   └── components/ (navbar, footer, messages)
│
├── core/
│   ├── models.py       # UserProfile, Recommendation, PromptHistory
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── services.py     # Gemini integration
│   ├── utils.py         # learning resources data
│   ├── admin.py
│   └── context_processors.py
│
└── aibridge/            # Django project settings
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── asgi.py
```

## 7. Installation (Local Development)

**Prerequisites:** Python 3.12+

```bash
# 1. Clone the repository
git clone <your-repo-url> aibridge
cd aibridge

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and set GEMINI_API_KEY (get one at https://aistudio.google.com/apikey)

# 5. Run database migrations
python manage.py makemigrations
python manage.py migrate

# 6. (Optional) create an admin user
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to view the site, and `http://127.0.0.1:8000/admin/` for the Django admin.

### Environment Variables

| Variable         | Description                                         | Default              |
|------------------|------------------------------------------------------|-----------------------|
| `SECRET_KEY`     | Django secret key                                     | dev-only placeholder  |
| `DEBUG`          | `True`/`False`                                        | `True`                |
| `ALLOWED_HOSTS`  | Comma-separated list of allowed hosts                 | `127.0.0.1,localhost` |
| `GEMINI_API_KEY` | Your Google Gemini API key                            | *(required for AI)*   |
| `GEMINI_MODEL`   | Gemini model name                                     | `gemini-3-flash-preview` |

**Never commit your `.env` file or hardcode the API key.**

## 8. Deployment

AIBridge is ready to deploy to **Render**, **Railway**, or **PythonAnywhere**.

### Render / Railway

1. Push your code to GitHub.
2. Create a new Web Service and connect the repository.
3. Set the build command:
   ```
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   ```
4. Set the start command:
   ```
   gunicorn aibridge.wsgi:application
   ```
5. Add environment variables (`SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `GEMINI_API_KEY`, `GEMINI_MODEL`) in the platform's dashboard.

### PythonAnywhere

1. Upload the project (or clone via a Bash console).
2. Create a virtualenv and `pip install -r requirements.txt`.
3. Configure a new Web App with a **Manual configuration** WSGI file pointing to `aibridge.wsgi.application`.
4. Set environment variables in the WSGI config file or a `.env` file.
5. Run `python manage.py migrate` and `python manage.py collectstatic` from a Bash console.
6. Reload the web app.

## 9. Screenshots

_Add screenshots of the Home, Dashboard, Recommender, and Prompt Generator pages here once deployed._

- `docs/screenshots/home.png`
- `docs/screenshots/dashboard.png`
- `docs/screenshots/recommender.png`
- `docs/screenshots/prompt-generator.png`

## 10. Live URL

🔗 **Live demo:** `https://your-deployment-url.example.com` _(replace once deployed)_

## 11. GitHub Repository

🔗 **Repository:** `https://github.com/your-username/aibridge` _(replace with your repository URL)_

---

Built with Django and Google Gemini.
