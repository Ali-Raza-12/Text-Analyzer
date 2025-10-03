1 — Prerequisites

Python 3.10+ installed

Node.js + npm installed

A Google Gemini API key (put in .env)

Internet connection (for Gemini and NLTK downloads)



2 — Backend (Flask) — Run steps (Windows CMD / PowerShell)

Open a terminal, go to backend folder:

cd backend

Create & activate a virtual environment:

Windows (cmd / PowerShell):

python -m venv venv
venv\Scripts\activate

macOS / Linux:

python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install flask flask-cors python-dotenv google-genai nltk

or 

pip install -r requirements.txt


<!-- I already add my Gemini api key for testing  -->
<!-- Optional -->

Create a .env file in the same backend folder and add your API key (no spaces!):  

GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Start the backend:

python main.py

Backend runs at: http://127.0.0.1:5000





3 — Frontend (React) — Run steps

Open a new terminal and go to frontend folder:

cd frontend

Install and start:

npm install
npm run dev # or `npm start` depending on the repo

Frontend runs at: http://localhost:3000

Make sure the backend is running first.




4 — How frontend talks to backend

Analyze: POST http://127.0.0.1:5000/analyze
Body (JSON):

{ "text": "Paste your article or blog text here" }

Search: GET http://127.0.0.1:5000/search?topic=<term>

History: GET http://127.0.0.1:5000/history

If your frontend uses relative paths, set the fetch URL to http://127.0.0.1:5000 (or add "proxy" in package.json).




