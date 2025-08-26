# AI Trading Assistant

This project is a full-stack AI-powered trading assistant. It consists of a FastAPI backend and a React + Vite frontend. The backend parses natural language trading commands and executes trades via Alpaca, while the frontend provides a user-friendly interface.

---

## Features
- **Natural Language Trading**: Enter commands like "Buy 10 shares of AAPL at $180 limit".
- **AI Parsing**: Uses OpenAI to interpret trading instructions.
- **Alpaca Integration**: Places real or mock trades via Alpaca API.
- **Clarification**: If the command is ambiguous, the assistant asks for more details.
- **Modern UI**: Built with React, TailwindCSS, and Vite.

---

## Prerequisites
- Python 3.10+
- Node.js 18+
- npm

---

## Backend Setup (FastAPI)

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Environment variables:**
   - Create a `.env` file in `backend/` with the following (replace with your keys):
     ```env
     OPENAI_API_KEY=your_openai_key
     ALPACA_API_KEY=your_alpaca_key
     ALPACA_SECRET_KEY=your_alpaca_secret
     ALPACA_BASE_URL=https://paper-api.alpaca.markets
     ALLOWED_ORIGINS=http://localhost:5173
     MOCK_OPENAI=true
     MOCK_ALPACA=true
     ```
   - For testing/demo, leave `MOCK_OPENAI` and `MOCK_ALPACA` as `true`.

3. **Run the backend server:**
   ```bash
   uvicorn main:app --reload
   ```
   - The API will be available at `http://localhost:8000`

---

## Frontend Setup (React + Vite)

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```
   - The app will be available at `http://localhost:5173`

---

## Usage
- Open `http://localhost:5173` in your browser.
- Enter a trading command (e.g., "Buy 10 shares of AAPL at $180 limit") and submit.
- The backend will parse and execute the trade (mock or real, based on `.env`).

---

## Project Structure
```
ai_trading_assistant/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── services/
│   ├── utils.py
│   ├── requirements.txt
│   └── ...
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── api.js
│   ├── index.html
│   ├── package.json
│   └── ...
└── README.md
```

---

## Notes
- Ensure both backend and frontend are running for full functionality.
- You can use your own OpenAI and Alpaca API keys for live trading.
- For production, set `MOCK_OPENAI` and `MOCK_ALPACA` to `false` in `.env`.

---

## Troubleshooting
- If the frontend does not show anything, ensure `main.jsx` is present and `index.html` loads it.
- If CORS errors occur, check `ALLOWED_ORIGINS` in `.env`.
- For API errors, check backend logs and environment variables.

---

## License
MIT