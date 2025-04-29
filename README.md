# Workout Data Analysis: Turning Sweat into Insights

Welcome to my **Workout Data Analysis** project! This project is a deep dive into my fitness journey, where I transform raw workout logs into actionable insights using Python, pandas, and data visualization. As part of my GitHub portfolio, this project showcases my skills in **data wrangling**, **data parsing**, **data transformation**, **visualization** and **storytelling** through code. Whether you're a fitness enthusiast, a data nerd, or both, I hope this project inspires you to explore your own data!

## Why This Project?
I started logging my workouts to track my progress, but I quickly realized that my scribbled notes in `workout_data.txt` held a goldmine of insights. Driven by curiosity about my fitness journey, I explored how factors like my pre-workout meals, hydartion, muscle group focus affect my performance. To explore these questions, I built a pipeline to parse, structure, and analyze my workout data, culminating in a Jupyter notebook packed with visualizations and findings. This project reflects my passion for fitness, coding, and uncovering patterns in data.

The analyses also serve as a case study in data-driven performance optimization, applicable to domains like health tech or business analytics.

## Table of Contents
- [Project Overview](#project-overview)
- [What You’ll Find Here](#what-youll-find-here)
- [Tech Stack](#tech-stack)
- [How It Works](#how-it-works)
- [Repository Structure](#repository-structure)
- [Setup and Installation](#setup-and-installation)
- [Running the Project](#running-the-project)
- [Diving into the Data](#diving-into-the-data)
- [Key Insights](#key-insights)
- [Challenges and Learnings](#challenges-and-learnings)
- [What’s Next?](#whats-next)
- [License](#license)

## Project Overview
This project takes raw workout logs—like sets of pull-ups, pre-workout sandwiches, and heart rate data from my AmazeFit tracker and turns them into structured, analyzable data. The pipeline consists of:
1. **Parsing**: A Python script (`workout_data_parser.py`) reads the raw text file and outputs two CSV files: one for exercise details and one for session summaries.
2. **Analysis**: A Jupyter notebook (`workout_data_analysis.ipynb`) processes the CSVs, cleans the data, and runs analyses to explore relationships between nutrition, hydration, muscle focus, and workout outcomes.
3. **Visualization**: Using Matplotlib and Seaborn, I generate plots to visualize trends, such as the impact of bananas on bicep workouts or calorie burn by muscle group.

The result? A set of insights that help me optimize my workouts and a portfolio piece that demonstrates my data analyses skills.

## What You’ll Find Here
This project is packed with features that highlight both my analytical and visualization abilities:
- **Data Parsing**: Converts messy, human-written workout logs into clean CSVs.
- **Data Cleaning**: Handles missing values, formats dates, and splits complex fields like pre-workout meals.
- **Custom Functions**: Modular scripts for parsing meals (`split_preworkout.py`) and generating visualizations (`workout_log_analysis.py`).
- **Comprehensive Analysis**:
  - Impact of pre-workout meals on workout volume.
  - Frequency of muscle group training and exercise preferences.
  - Progress tracking over time (cumulative and by 3-month phases).
  - Hydration’s effect on performance (volume per minute).
  - Calorie burn by muscle group.
  - Detection of strength plateaus.
  - Comparison of cardio vs. strength workouts.
- **Visualizations**: Bar plots, pie charts, line plots, and scatter plots saved in `reports/visuals/`.
- **Documentation**: Clear code comments, a detailed notebook, and this README to guide you through the project.

## Tech Stack
- **Python**: Core language for parsing and analysis.
- **Pandas**: Data manipulation and CSV handling.
- **Matplotlib & Seaborn**: Data visualization.
- **Jupyter Notebook**: Interactive analysis and storytelling.
- **Git**: Version control for collaboration and project hosting.

## How It Works
The project follows a clear workflow:
1. **Input**: A raw text file (`workout_data.txt`) containing daily workout logs with details like date, muscle targeted, pre-workout meals, exercises, and AmazeFit tracker data.
2. **Parsing**: The `WorkoutDataParser` class reads the text file, extracts structured data (e.g., sets, reps, hydration), and saves it to `exercise_log.csv` (exercise-specific) and `session_log.csv` (session summaries).
3. **Preprocessing**: The notebook cleans the data by filling missing values, converting dates to datetime, and splitting pre-workout meals into quantities (e.g., banana_qty, apple_qty).
4. **Analysis**: Custom functions in `workout_log_analysis.py` compute metrics like workout volume (weight × reps), group data by date or muscle, and generate insights.
5. **Visualization**: Plots are created to visualize trends, saved to `reports/visuals/`, and displayed in the notebook.

## Repository Structure
Here’s how the project is organized:
```
workout_data_analysis
├── data/
│   ├── raw/
│   │   └── workout_data.txt        # Raw workout logs
│   ├── processed/
│   │   ├── exercise_log.csv        # Parsed exercise data
│   │   └── session_log.csv         # Parsed session data
├── notebooks/
|   ├── workout_data_analysis.ipynb # Analysis notebook
├── src/
│   ├── split_preworkout.py         # Parses pre-workout meals
│   ├── workout_log_analysis.py     # Analysis and plotting functions
|   |── workout_data_parser.py      # Main parsing script from TXT to CSV
├── reports/
│   ├── visuals/                    # Saved plots (bar, pie, line, scatter)
├── LICENSE
└── README.md                       # You’re reading it!
```

## Setup and Installation
Ready to explore the project? Follow these steps:
1. **Clone the Repository**
2. **Install Dependencies**
   ```bash
   pip install pandas matplotlib seaborn jupyter
   ```
4. **Verify Data**: Ensure `data/raw/workout_data.txt` exists. You can use the provided data or log your own (see [Data Format](#data-format)).

## Running the Project
1. **Parse the Data**:
   Run the parser `workout_data_parser.py` to generate CSVs.
   This creates `exercise_log.csv` and `session_log.csv` in `data/processed/`.
2. **Analyze the Data**:
   Open `workout_data_analysis.ipynb` and run the cells to preprocess, analyze, and visualize the data.
3. **Explore Results**:
   - Visualizations are saved in `reports/visuals/`.
   - Insights are displayed as text cards and plots in the notebook.

## Diving into the Data
The raw workout log (`workout_data.txt`) is structured like a diary entry. Here’s a sample:
```
02/05/24
Muscle targeted: Mix
Fueling: Preworkout - 1 Sandwich, Workout Hydration - 500mL
Exercise:
Pull Ups: 1X7, 1X3
Push Ups: 1X10, 1X4
Bench Press: 1X12, 2.5X4
...
AmazeFit log: duration - 40 min, avg heart rate - 105, calories - 276kcal
```
The parser extracts:
- **Exercises**: Name, weight, reps, or cardio duration.
- **Session Details**: Date, muscle targeted, pre-workout meal, hydration, duration, heart rate, and calories.
The notebook then analyzes metrics like workout volume (weight × reps), calories burned, and heart rate trends.

## Key Insights
Here’s what I discovered from the analysis:
1. **Pre-Workout Meals Matter**:
   - Bananas consistently lead to higher workout volumes, likely due to their quick-digesting carbs.
   - For biceps, 3 bananas before a workout yielded the best performance.
2. **Muscle Imbalances**:
   - Biceps are my most-trained muscle (aesthetic goals, guilty as charged 😅), with barbell curls dominating.
   - Back muscles are undertrained, with pull-ups as the primary exercise. Time to diversify!
3. **Progress Over Time**:
   - My cumulative workout volume shows an upward trend, with beginner gains early on.
   - Later 3-month phases (9-12 months) show higher average volumes, confirming strength gains.
4. **Hydration Boosts Performance**:
   - Hydration levels of 1000-1250 mL maximize volume per minute, but beyond 1250 mL, returns diminish.
5. **Calorie Burn**:
   - Leg workouts burn the most calories, making them ideal for weight loss goals.
   - Mixed workouts burn the least, suggesting a need for more focused sessions.
6. **Stall Points**:
   - For exercises like leg press, I identified plateaus where weight progression stalled, signaling a need for changes in intensity or recovery.
7. **Cardio vs. Strength**:
   - Cardio workouts elevate heart rate and burn more calories, but strength workouts are catching up as intensity increases.

These insights are backed by visualizations (saved in `reports/visuals/`) that make the data come alive.

## Challenges and Learnings
This project wasn’t without its hurdles:
- **Parsing Complexity**: The raw text file had inconsistent formatting (e.g., “1X7” vs. “10min”). Writing robust parsing logic in `workout_data_parser.py` taught me to anticipate edge cases.
- **Data Cleaning**: Handling missing values and splitting pre-workout meals (e.g., “2 banana & 1 coffee”) required carefull string manipulation, solved elegantly in `split_preworkout.py`.
- **Visualization Design**: Creating clear, informative plots took iteration. I learned to balance aesthetics and clarity using Seaborn.
- **Modularity**: Writing reusable functions in `workout_log_analysis.py` (e.g., `generic_plot`) made the code more maintainable and scalable.

These challenges honed my skills in Python, data wrangling, and visualization, which I’m excited to apply to future projects.

## What’s Next?
Future enhancements include:
- **More Data**: Adding more workout logs to improve statistical significance.
- **Advanced Metrics**: Incorporating rest intervals, perceived exertion, or sleep data.
- **Machine Learning**: Predicting optimal pre-workout meals or detecting plateaus using regression or clustering.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Thanks for exploring my **Workout Data Analysis** project! This is a cornerstone of my GitHub portfolio, showcasing my ability to turn raw data into meaningful insights. If you enjoyed this, check out my other projects or connect with me on [LinkedIn](https://www.linkedin.com/in/dhruv-gupta-90224a12a/) or [GitHub](https://github.com/decoded-by-dhruv). Let’s code, lift, and learn together!