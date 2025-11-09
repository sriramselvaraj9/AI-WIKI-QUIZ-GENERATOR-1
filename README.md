# 🧠 AI Wiki Quiz Generator

Full-stack AI-powered quiz generator that converts any Wikipedia article into an interactive quiz using FastAPI, React, and Gemini AI.

## 📁 Project Structure

```
ai-quiz-generator/
├── backend/
│   ├── database.py          # SQLAlchemy async setup
│   ├── models.py           # Quiz database model
│   ├── scraper.py          # Wikipedia content scraper
│   ├── llm_quiz_generator.py # LangChain + Gemini integration
│   ├── main.py             # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables
├── frontend/
│   ├── src/
│   │   ├── components/    # Reusable React components
│   │   ├── services/      # API service layer
│   │   ├── tabs/         # Main application tabs
│   │   ├── App.jsx       # Main React app
│   │   ├── main.jsx      # React entry point
│   │   └── index.css     # Tailwind CSS styles
│   ├── package.json      # Node.js dependencies
│   ├── vite.config.js    # Vite configuration
│   ├── tailwind.config.js # Tailwind configuration
│   └── index.html        # HTML template
└── README.md
```

## 🚀 Features

- **Wikipedia Scraping**: Extracts article content from any Wikipedia URL
- **AI Quiz Generation**: Uses Google Gemini AI (via LangChain) to create intelligent quizzes
- **Fallback Generation**: Works offline with deterministic quiz generation when AI is unavailable
- **Quiz History**: Stores and displays all previously generated quizzes
- **Modern UI**: Beautiful, responsive interface built with React and Tailwind CSS
- **Real-time Updates**: History auto-refreshes to show new quizzes

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+ 
- Node.js 16+
- npm, yarn, or pnpm

### Backend Setup

1. **Create and activate virtual environment:**

```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Alternative for Command Prompt
python -m venv .venv
.venv\Scripts\activate.bat
```

2. **Install Python dependencies:**

```powershell
cd backend
pip install -r requirements.txt
```

3. **Configure environment variables:**

Edit `backend/.env` and set your configuration:

```env
DATABASE_URL=sqlite+aiosqlite:///./quiz.db
GEMINI_API_KEY=your_google_gemini_api_key_here
GEMINI_MODEL=gemini-pro
FRONTEND_ORIGIN=http://localhost:5173
PORT=8000
```

4. **Start the FastAPI server:**

```powershell
# From the backend directory
uvicorn main:app --reload --port 8000

# Or from project root
uvicorn backend.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Install dependencies:**

```powershell
cd frontend
npm install

# Or with yarn/pnpm
yarn install
pnpm install
```

2. **Start the development server:**

```powershell
npm run dev

# Or with yarn/pnpm
yarn dev
pnpm dev
```

The frontend will be available at `http://localhost:5173`

## 🎯 Usage

1. **Generate a Quiz:**
   - Navigate to the "Generate Quiz" tab
   - Paste a Wikipedia URL (e.g., `https://en.wikipedia.org/wiki/Artificial_intelligence`)
   - Click "Generate Quiz"
   - View the generated questions and answers

2. **View Quiz History:**
   - Navigate to the "History" tab  
   - See all previously generated quizzes
   - Click "View Quiz" to see full quiz details in a modal

## 🔧 API Endpoints

- `GET /` - API status
- `POST /generate_quiz` - Generate quiz from Wikipedia URL
  ```json
  { "url": "https://en.wikipedia.org/wiki/Topic" }
  ```
- `GET /history` - Get all quiz history
- `GET /quiz/{quiz_id}` - Get specific quiz by ID

## 🤖 AI Integration

The app uses Google's Gemini AI through LangChain to generate intelligent quiz questions. Features:

- **Smart Question Generation**: Creates relevant multiple-choice questions
- **Content Summarization**: Generates article summaries  
- **Fallback Mode**: Works without API key using deterministic generation
- **Error Handling**: Gracefully handles API failures

To use Gemini AI:
1. Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set `GEMINI_API_KEY` in `backend/.env`

## 🗄️ Database

- **Default**: SQLite (no setup required)
- **Production**: Switch to MySQL/PostgreSQL by updating `DATABASE_URL`

Example MySQL connection:
```env
DATABASE_URL=mysql+aiomysql://user:password@localhost/quiz_db
```

## 🎨 Design Features

- **Pastel Color Palette**: Soft, modern colors
- **Card-based Layout**: Clean, organized interface  
- **Responsive Design**: Works on all screen sizes
- **Smooth Animations**: Fade-in effects and hover states
- **Loading States**: Skeleton loaders and spinners
- **Error Handling**: User-friendly error messages

## 🔄 Development Workflow

1. **Backend Changes**: 
   - Modify Python files in `backend/`
   - Server auto-reloads with `--reload` flag

2. **Frontend Changes**:
   - Modify React files in `frontend/src/`
   - Vite provides hot module replacement

3. **Database Changes**:
   - Modify models in `backend/models.py`
   - Database tables auto-create on startup

## 🚀 Deployment

### Backend (FastAPI)
- Use `uvicorn` with production settings
- Set up proper environment variables
- Use PostgreSQL/MySQL for production database

### Frontend (React)
- Build: `npm run build`
- Deploy `dist/` folder to static hosting
- Set `VITE_API_BASE` environment variable

## 🐛 Troubleshooting

**Common Issues:**

1. **Import Errors**: Ensure virtual environment is activated
2. **CORS Issues**: Check `FRONTEND_ORIGIN` in backend `.env`
3. **Database Errors**: Ensure SQLite file permissions or database credentials
4. **API Key Issues**: Verify Gemini API key is correct and has quota

**Development Tips:**

- Use browser DevTools to debug API calls
- Check FastAPI automatic docs at `http://localhost:8000/docs`
- Monitor backend logs for detailed error messages

## 🎉 Project Status

✅ **COMPLETE** - The AI Wiki Quiz Generator is fully functional!

**What's Working:**
- ✅ Backend FastAPI server with all endpoints (/generate_quiz, /history, /quiz/{id})
- ✅ Wikipedia scraping with robust content extraction  
- ✅ LLM integration with Gemini API and fallback generator
- ✅ **10 questions per quiz** for comprehensive testing
- ✅ **Interactive quiz interface** - click to select answers
- ✅ **Smart answer system** - answers hidden until "Show Answers" clicked
- ✅ **Score calculation** with detailed answer popup
- ✅ **Fast generation** optimized for quick quiz creation
- ✅ SQLite database with async SQLAlchemy models
- ✅ React frontend with Tailwind CSS styling
- ✅ Tab-based UI (Generate Quiz / History)
- ✅ Modal quiz display with card-based layout
- ✅ Automatic history refresh and quiz persistence
- ✅ CORS configured for cross-origin requests
- ✅ Fallback generator works without API keys

**Ready to Use:**
1. Backend: `uvicorn main:app --reload --port 8000`
2. Frontend: `npm run dev` 
3. Browse to: http://localhost:5173

## Optional Enhancements

- Add your Gemini API key to `backend/.env` for AI-powered quiz generation
- Switch to MySQL/PostgreSQL for production by updating `DATABASE_URL`
- Deploy to cloud platforms (Vercel + Railway/Heroku)

## 📝 License

This project is for educational purposes. Please ensure you comply with Wikipedia's terms of service when scraping content.

---

**Made with ❤️ using FastAPI, React, Tailwind CSS, and Google Gemini AI**