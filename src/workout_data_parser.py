import pandas as pd

class WorkoutDataParser:
    """This script parses a workout log text file and into structured CSV files.

    This class reads a manually recorded workout log in a text file, extracts daily workout
    details (exercises, sets, pre-workout nutrition, hydration, and fitness tracker data),
    and exports the data into two CSV files: one for exercise details and one for session
    summaries.

    Attributes:
        txt_file_path (str): Path to the input text file containing workout logs.
        exercise_data (list): List of dictionaries storing parsed exercise data.
        session_data (list): List of dictionaries storing parsed session data.
    """
        
    def __init__(self, txt_file_path):
        """Initialize the parser with the path to the workout log text file.
        
        Args:
            txt_file_path (str): Path to the input text file.
        """
        self.txt_file_path = txt_file_path
        self.exercise_data = []
        self.session_data = []
    

    def parse_fueling(self, fueling_info):
        """Extract pre-workout meal and hydration data from a fueling info string.

        Args:
            fueling_info (str): String containing fueling details, e.g.,
            "Fueling: Preworkout - 1 Sandwich, Workout Hydration - 500mL".

        Returns:
            tuple: (preworkout, hydration) where preworkout is a string (e.g., "1 Sandwich")
            and hydration is an integer (e.g., 500).

        Example:
            Input: "Fueling: Preworkout - 1 Sandwich, Workout Hydration - 500mL"
            Output: ("1 Sandwich", 500)
        """
        preworkout = ""
        hydration = 0

        # Remove "Fueling:" prefix and split into segments
        fueling_info_segments = fueling_info.replace("Fueling:","").strip().split(",")

        for segment in fueling_info_segments:
            if "Preworkout" in segment:
                preworkout = segment.split("-")[1].strip()
            elif "Workout Hydration" in segment:
                hydration = int(segment.split("-")[1].strip().replace("mL","").strip())
        
        return preworkout,hydration
    

    def parse_amazefit_log(self, amazefit_info):
        """Extract fitness tracker data from an AmazeFit log string.

        Args:
            amazefit_info (str): String containing fitness tracker data, e.g.,
            "AmazeFit log: duration - 40 min, avg heart rate - 105, calories - 276kcal".

        Returns:
            tuple: (duration, avg_heart_rate, calories) where all are integers.

        Example:
            Input: "AmazeFit log: duration - 40 min, avg heart rate - 105, calories - 276kcal"
            Output: (40, 105, 276)
        """
        duration = avg_heart_rate = calories = 0

        # Remove "AmazeFit log:" prefix and split into segments
        amazefit_info_segments = amazefit_info.replace("AmazeFit log:","").strip().split(",")

        for segment in amazefit_info_segments:
            if "duration" in segment:
                duration = int(segment.split("-")[1].strip().replace("min","").strip())
            elif "avg heart rate" in segment:
                avg_heart_rate = int(segment.split("-")[1].strip())
            elif "calories" in segment:
                calories = int(segment.split("-")[1].strip().replace("kcal","").strip())

        return duration,avg_heart_rate,calories
    

    def parse_sets(self, exercise_name, sets_str_list):
        """Parse exercise sets into structured data for strength or cardio exercises.

        Args:
            exercise_name (str): Name of the exercise (e.g., "Bench Press").
            sets_str_list (list): List of strings representing sets, e.g.,
            ["10X12", "8X15"] or ["5 min"].

        Returns:
            list: List of dictionaries, each containing exercise details (exercise name,
            weight, reps, cardio_duration).
        """
        parsed_sets = []
        for s in sets_str_list:
            s = s.split()
            if "min" in s[0]:   # Cardio exercise
                duration = int(s[0].replace("min","").strip())
                parsed_sets.append({
                    "exercise": exercise_name,
                    "weight": None,
                    "reps": None,
                    "cardio_duration": duration
                })
            elif "X" in s[0]:   # Strength exercise
                weight, reps = s[0].split("X")
                reps = reps.strip().replace('.','').strip()
                parsed_sets.append({
                    "exercise": exercise_name,
                    "weight": float(weight.strip()),
                    "reps": int(reps),
                    "cardio_duration": None
                })
        return parsed_sets
    

    def process_entry(self, entry):
        """Process a single day's workout log entry and extract relevant data.

        Args:
            entry (str): A string containing one day's workout log, with lines for date,
            muscle targeted, fueling, exercises, and AmazeFit log.

        Notes:
            - Stores exercise data in self.exercise_data and session data in self.session_data.
            - Handles both strength (weight/reps) and cardio (duration) exercises.
        """
        lines = []
        for line in entry.split('\n'):      # splits the text block into separate lines, every time it sees a new line character
            cleaned_line = line.strip()     # removes extra spaces from the beginning and end of each line.
            if cleaned_line:
                lines.append(cleaned_line)
        
        # checks if lines list is empty or not. If yes, it stops right there
        if not lines:
            return
        
        # Initialize entry data
        date = lines[0]
        muscle_targeted = ""
        preworkout = ""
        hydration = ""
        workout_duration = 0
        workout_avg_heart_rate = 0
        workout_calories_burnt = 0
        is_field_exercise = False

        for line in lines[1:]:
            if line.startswith("Muscle targeted:"):
                muscle_targeted = line.split(":",1)[1].strip()
            elif line.startswith("Fueling:"):
                preworkout, hydration = self.parse_fueling(line)
            elif line.startswith("Exercise:"):
                is_field_exercise = True
                continue
            elif line.startswith("AmazeFit log:"):
                workout_duration, workout_avg_heart_rate, workout_calories_burnt = self.parse_amazefit_log(line)
                is_field_exercise = False
            elif is_field_exercise and ":" in line:
                exercise_name, sets_str = line.split(":",1)
                sets = sets_str.split(",")
                parsed = self.parse_sets(exercise_name.strip(),sets)

                # Add date and muscle_targeted to each set
                for p in parsed:
                    p.update({
                        "date": date,
                        "muscle_targeted": muscle_targeted
                    })
                    self.exercise_data.append(p)
        
        # Store session data
        self.session_data.append({
            "date": date,
            "workout_duration": workout_duration,
            "workout_avg_heart_rate": workout_avg_heart_rate,
            "workout_calories_burnt": workout_calories_burnt,
            "preworkout": preworkout,
            "hydration": hydration
        })

    
    def parse_and_export(self, exercise_csv_out, session_csv_out):
        """Parse the workout log file and export data to CSV files.

        Args:
            exercise_csv_out (str): Path to save the exercise data CSV.
            session_csv_out (str): Path to save the session data CSV.

        Notes:
            - The input text file is expected to have entries separated by double newlines.
            - Outputs two CSVs: one for exercise details and one for session summaries.
        """
        with open(self.txt_file_path, "r") as file:
            content = file.read()

        # Split content into daily entries
        entries = [entry.strip() for entry in content.strip().split('\n\n') if entry.strip()]

        # Process each entry
        for entry in entries:
            self.process_entry(entry)
        
        # Export data to CSVs
        pd.DataFrame(self.exercise_data).to_csv(exercise_csv_out, index=False)
        pd.DataFrame(self.session_data).to_csv(session_csv_out, index=False)
        print("Exercise log saved to:", exercise_csv_out)
        print("Session log saved to:", session_csv_out)

parser = WorkoutDataParser("data/raw/workout_data.txt")
parser.parse_and_export("data/processed/exercise_log.csv", "data/processed/session_log.csv")