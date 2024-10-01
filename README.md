
# AI-Fitness-Coach

Personal Fitness Coach Powered By AI


## Deployment

**Install Ollama Client**
 1. Visit the [Ollama Download page](https://ollama.com/download)
 2. Choose your Operating System and press download
 3. After downloading do basic installation 
 
**Install Required Dependencies**

```bash
  pip install -r requirements.txt
```

**To deploy backend for this project**

open **main.py** and run

```bash
  uvicorn main:app --reload 
```
then open the **index.html** using a [live server](https://www.geeksforgeeks.org/how-to-enable-live-server-on-visual-studio-code/)

## Pending Features
- Visualization system for Logged calories user wise
- Calorie dashboard for user to track daily/monthly calorie burns
- Overall UI upgrade/improvement
## Known Issues
- Page reloads after Nutrition Plan Generation
## Key Components
- **User Management:** Handles user profiles with attributes like age, height, weight, body type, and activity level.
- **Workout Planning:** Generates personalized 30-day workout plans based on user profiles.
- **Nutrition Planning:** Creates custom nutrition plans tailored to individual user characteristics.
- **Workout Logging:** Allows users to log their workouts, including date and calories burned.
## Key Features

- **FastAPI Backend:** Utilizes FastAPI for efficient API development, -with SQLAlchemy for ORM and SQLite for data persistence.
- **AI Integration:** Incorporates the Ollama client to generate personalized workout and nutrition plans using the llama3.2 model.
- **User Profiling:** Captures detailed user information including body type and activity level for tailored recommendations.
- **RESTful API:** Implements endpoints for user signup, workout/nutrition plan generation, and workout logging.
- **Responsive Frontend:** Features a clean, mobile-friendly UI built with vanilla JavaScript, HTML, and CSS.
- **CORS Middleware:** Enables cross-origin resource sharing for local development and potential future scaling.
## Technical Stack
- Backend: Python 3.x, FastAPI, SQLAlchemy, Ollama
- Database: SQLite
- Frontend: HTML5, CSS3, Vanilla JavaScript
- AI Model: llama3.2 (via Ollama client)
## Contributors

<a href="https://github.com/ayushmankoley/AI-Fitness-Coach/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ayushmankoley/AI-Fitness-Coach" />
</a>
