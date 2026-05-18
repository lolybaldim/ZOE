<div align="center">

<img src="https://img.shields.io/badge/Built%20for-Humanity-ff6b6b?style=for-the-badge" />
<img src="https://img.shields.io/badge/Powered%20by-Google%20Gemma%204-4285F4?style=for-the-badge&logo=google" />
<img src="https://img.shields.io/badge/Track-Health%20%26%20Sciences-10b981?style=for-the-badge" />
<img src="https://img.shields.io/badge/Hackathon-Gemma%204%20Good-f59e0b?style=for-the-badge" />

# ZOE

### AI Health Access for the People Who Need It Most

*Built for Rwanda. Built for Sudan. Built for every community where a hospital is a day's journey away.*

</div>

&nbsp;

## The Story Behind ZOE

Somewhere in rural Rwanda, a mother notices her child has had a fever for three days. The nearest clinic is two hours away. She has no car, no money for the bus, and no way of knowing if this is serious or something that will pass. She waits. Sometimes, that wait costs everything.

ZOE was built for her.

ZOE is an AI-powered healthcare platform that puts real medical intelligence in the hands of people who have been left out of the healthcare system entirely. Not a simple chatbot. Not a symptom Googler. A full healthcare companion that thinks, responds, warns, guides, and remembers — in your language, on your phone, without a hospital in sight.

&nbsp;

## What ZOE Can Do

**Talk to you about your symptoms** and tell you honestly if something sounds urgent, moderate, or an emergency that cannot wait. ZOE uses Google Gemma 4 to analyze what you describe and respond with clarity and empathy, not medical jargon.

**Scream when it needs to.** If your symptoms suggest a stroke, a heart attack, difficulty breathing, or heavy bleeding, ZOE does not stay calm. It triggers a loud, unmissable emergency alert and tells you exactly what to do in the next five minutes.

**Find the nearest help.** Through Google Maps integration, ZOE shows you every hospital, clinic, pharmacy, and emergency center near you. Because knowing where to go is half the battle.

**Remember you.** ZOE keeps your full health profile — blood type, allergies, chronic conditions, past consultations, and medication history — so you never have to start from scratch, and neither does your doctor.

**Speak your language.** ZOE responds in English, French, Arabic, and Swahili. Arabic renders right to left. The language of care should never be a barrier.

**Remind you.** Medications only work if you take them. ZOE lets you set daily reminders and tracks whether you have taken your doses — simple, persistent, and reliable.

**Show you the bigger picture.** Your health analytics dashboard gives you a visual timeline of your consultations, vitals, and trends over time. Because patterns matter.

**Export your story.** Any consultation can be downloaded as a full PDF medical report, ready to hand to a doctor, a clinic, or a specialist.

&nbsp;

## Built With

ZOE runs on a carefully chosen stack that keeps it fast, accessible, and free to deploy for teams without enterprise budgets.

The backend is Python and Flask, with Flask-Login handling authentication and bcrypt protecting every password. The database is Supabase, which gives a fully managed PostgreSQL database with a generous free tier and real-time capabilities. The AI brain is Google Gemma 4, accessed through the Google AI Studio API with a system prompt engineered specifically for healthcare triage in low-resource settings. Maps come from the Google Maps JavaScript API. Charts are rendered with Chart.js. The frontend is built on Tailwind CSS for a mobile-first, fast-loading interface that works on a three-year-old Android phone on a slow connection.

&nbsp;

## Getting Started

You will need Python 3.10 or newer, a free Supabase account, a Google AI Studio API key for Gemma 4, and a Google Maps API key.

Clone the repository and step inside it.

```bash
git clone https://github.com/lolybaldim/ZOE.git
cd ZOE
```

Create a virtual environment and activate it.

```bash
python -m venv venv
source venv/bin/activate
```

Install all dependencies.

```bash
pip install -r requirements.txt
```

Copy the environment file and fill in your keys.

```bash
cp .env.example .env
```

Open your `.env` file and add your values.

```
SECRET_KEY=something_long_and_random
GOOGLE_API_KEY=your_gemma_api_key
MAPS_API_KEY=your_google_maps_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key
DATABASE_URL=your_supabase_postgres_connection_string
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_gmail_app_password
```

Set up your database by going to your Supabase SQL Editor and running the contents of `supabase_schema.sql`. Then start the app.

```bash
flask run
```

Visit `http://localhost:5000` and ZOE is alive.

&nbsp;

## How to Deploy for Free

ZOE is designed to run on zero budget. The recommended setup is Render for hosting and Supabase for the database, both of which have free tiers that are more than enough for a demo or an MVP.

On Render, create a new Web Service, connect your GitHub repository, set your environment variables in the dashboard, and deploy. Your live URL will be ready within minutes. No credit card required.

&nbsp;

## Project Structure

```
ZOE/
  app.py                   Entry point
  config.py                All configuration, reads from environment
  extensions.py            Flask extensions setup
  requirements.txt         Python dependencies
  supabase_schema.sql      Full database schema

  models/                  Database models for users, patients,
                           appointments, consultations, medications,
                           and emergency logs

  routes/                  One file per feature — auth, dashboard,
                           ai_chat, hospitals, medications,
                           appointments, analytics, education,
                           reports, emergency, admin, patients

  utils/                   Gemma 4 API wrapper with prompt engineering,
                           Supabase client, and PDF generator

  templates/               All HTML pages including the admin panel,
                           error pages, and patient-facing views

  static/                  CSS, JavaScript, and assets
```

&nbsp;

## Who ZOE Is For

ZOE was designed with three people in mind.

The patient in a rural community who needs to know if their symptoms are serious before spending money they do not have on a journey they may not need. The elderly person living alone who just needs a reminder to take their medication at eight in the morning. The caregiver managing the health of three family members across two countries, trying to keep records that paper and memory alone cannot hold.

ZOE is also for the doctor who wants to walk into an appointment already knowing the patient's history. And for the healthcare administrator who needs to see emergency trends, manage appointments, and keep a clinic running with a small team.

&nbsp;

## What Comes Next

ZOE is an MVP today. The roadmap includes SMS emergency alerts via Twilio, a Progressive Web App mode for full offline access, telemedicine video consultations, a mobile app in React Native, and eventually partnerships with government health systems and NGOs across sub-Saharan Africa and the MENA region.

The goal is not to replace doctors. The goal is to make sure that when you finally reach one, you have already done everything right.

&nbsp;

## A Note on Safety

ZOE is not a diagnostic tool and does not claim to be. Every response from the AI includes a clear reminder to consult a qualified healthcare professional for any medical decision. ZOE exists to triage, to guide, to alert, and to inform. The final word always belongs to a human doctor.

&nbsp;

<div align="center">

*ZOE — Because everyone deserves access to healthcare, regardless of where they live.*

Made with purpose in Rwanda 🇷🇼

</div>
