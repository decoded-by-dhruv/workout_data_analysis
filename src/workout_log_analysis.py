import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# Directory for saving images
relative_directory = "../reports/visuals"

# Generic Utility Functions
def transform_to_long_df(df, id_vars, value_vars, var_name, value_name, filter_col=None, filter_condition=None):
    """Transform wide-format DataFrame to long-format with optional filtering."""
    melted_df = df.melt(id_vars=id_vars, value_vars=value_vars, var_name=var_name, value_name=value_name)
    if filter_col and filter_condition:
        melted_df = melted_df[filter_condition(melted_df[filter_col])]
    return melted_df

def aggregate_data(df, group_by_cols, agg_col, agg_func='mean', sort_by=None, ascending=True):
    """Aggregate data with grouping and optional sorting."""
    agg_df = df.groupby(group_by_cols)[agg_col].agg(agg_func).reset_index()
    if sort_by:
        agg_df = agg_df.sort_values(by=sort_by, ascending=ascending)
    return agg_df

def find_extremes(df, group_col, value_col, extreme='max'):
    """Find max or min value in grouped data."""
    grouped = df.groupby(group_col)[value_col].sum()
    return grouped.idxmax() if extreme == 'max' else grouped.idxmin()

def generic_plot(plot_type, data, x, y, hue=None, title=None, xlabel=None, ylabel=None, 
                 color=None, marker=None, grid=False, legend=False, figsize=(8, 5), 
                 rotation=None, pie_legend_title=None):
    """Generic plotting function with customization options."""
    plt.figure(figsize=figsize)
    if plot_type == 'bar':
        if hue:
            sns.barplot(data=data, x=x, y=y, hue=hue, width=0.5)
        else:
            plt.bar(data[x], data[y], color=color or 'skyblue',width=0.5)
    elif plot_type == 'pie':
        wedges, texts, autotexts = plt.pie(data[y], autopct='%1.1f%%')
        plt.legend(wedges, data[x], title=pie_legend_title, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.axis('equal')
    elif plot_type == 'line':
        sns.lineplot(data=data, x=x, y=y, hue=hue, marker=marker, color=color)
    elif plot_type == 'scatter':
        sns.scatterplot(data=data, x=x, y=y, hue=hue, color=color, marker=marker, s=100)
    
    if title:
        plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    if rotation:
        plt.xticks(rotation=rotation)
    if grid:
        plt.grid(True)
    if legend:
        plt.legend()

    plt.tight_layout()

    file_name = f"{title}.png"
    file_path = os.path.join(relative_directory,file_name)
    plt.savefig(file_path)

    plt.show()

def display_line_card(lines):
    """For displaying results as a visual card."""
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.axis('off')  # Hide axes

    # Join all lines into a single text block
    content = "\n\n".join(lines)

    # Display text inside a rounded box
    ax.text(0.5, 0.5, content,
            ha='center', va='center', fontsize=12,
            bbox=dict(boxstyle='round,pad=0.8', facecolor='lightgreen', edgecolor='black'))
    plt.show()


# Main Analysis Functions
def analyze_meal_effect(analysis_df, target_muscle='chest'):
    """
    Analyzes the effect of pre-workout meals on total workout volume.
    Also, find what's the best meal & qty for a particular target muscle.
    Args:
        analysis_df: DataFrame with workout and meal data.
        target_muscle (str): Muscle group to analyze (default: 'chest').
    
    Returns:
        dict: Contains best meal overall & best meal for a specific muscle
    """

    melted_df = transform_to_long_df(
        analysis_df, 
        id_vars=['date', 'muscle_targeted', 'total_volume'],                    # columns to be keep as-is
        value_vars=['banana_qty', 'apple_qty', 'coffee_qty', 'sandwich_qty'],   # columns to be stack vertically
        var_name='food',                                                        # name of the new column that will hold the original column names from value_vars
        value_name='qty',                                                       # name of the new column that will hold the values from those value_vars columns
        filter_col='qty',                                                       # on a particular date if only banana was taken. So, filter to show only those rec where qty>0
        filter_condition=lambda qty: qty > 0
    )

    melted_df['food'] = melted_df['food'].str.replace('_qty', '')               # removing the _qty from the food name to get just the food name!
    eaten_df = melted_df.sort_values(by='date')
    
    # best meal overall - calculated by doing a groupBy
    best_meal_overall = aggregate_data(eaten_df, ['food'], 'total_volume', 'sum', 'total_volume', False)

    # Plotting now    
    generic_plot('bar', best_meal_overall, 'food', 'total_volume', title='Total Workout Volume by Pre-Workout Meal', 
                 xlabel='Pre-Workout Meal', ylabel='Total Volume')

    # Best Meal & Qty for a Specific Muscle Group
    muscle_df = eaten_df[eaten_df['muscle_targeted'].str.lower() == target_muscle]
    best_meal_for_target_muscle = None
    if not muscle_df.empty:
        best_food_qty_pair = muscle_df.loc[muscle_df['total_volume'].idxmax()]
        best_meal_for_target_muscle = {'muscle': target_muscle, 'food': best_food_qty_pair['food'], 
                                       'qty': best_food_qty_pair['qty']}
        
        # plotting best performance for a muscle group
        line = [f"Best performance for {target_muscle}", f"Meal: {best_meal_for_target_muscle['food']} (Qty: {best_meal_for_target_muscle['qty']})"]
        display_line_card(line)

    else:
        print("No data available for this muscle and food combination.")

    return {'Best meal overall ': best_meal_overall, 'Best meal for target muscle': best_meal_for_target_muscle}


def analyze_muscle_training(exercise_df, excluded_muscles=['Mix', 'Cardio']):
    """
    Analyzes muscle training frequency and common exercises.
    
    Args:
        exercise_df: DataFrame with exercise data.
        excluded_muscles (list): Muscles to exclude (default: ['Mix', 'Cardio']).
    
    Returns:
        dict: Contains muscle stats and exercise frequencies.
    """

    excluded_df = exercise_df[~exercise_df['muscle_targeted'].isin(excluded_muscles)]
    muscle_count = aggregate_data(excluded_df, 'muscle_targeted', 'date', 'nunique', 'date')

    """
    ---------------------------------------------------------------------------------------------------------------------
    least_trained_muscle = muscle_count.idxmin()
    most_trained_muscle = muscle_count.idxmax() 
    
    The above gives error as index is reset. 
    So, this return the index of the row where the minimum or maximum value occurs in a Series or DataFrame.
    ---------------------------------------------------------------------------------------------------------------------
    """

    # correct code
    least_trained_muscle = muscle_count['muscle_targeted'].iloc[0]
    most_trained_muscle = muscle_count['muscle_targeted'].iloc[-1]

    line = [f"Least trained muscle is {least_trained_muscle}", f"Most trained muscle is {most_trained_muscle}"]
    display_line_card(line)
    
    generic_plot('bar', muscle_count, 'muscle_targeted', 'date', title='Muscle Training Frequency', xlabel='Muscle Targeted', ylabel='Frequency')

    
    """
    ---------------------------------------------------------------------------------------------------------------------
        Issue here - it shows all exercises done for a muscle including cardio...so need to add a filter like below!
    ---------------------------------------------------------------------------------------------------------------------
    """

    exclude_exercises = ['Cross fit','Treadmill','Russian kettlebell swing','Cycle','Jumping jack','Cross trainer','Reverse curls(forearms)','Push Ups']

    # Exercise frequency for most trained muscle                                
    exercise_freq_for_most_trained = (
        exercise_df[(exercise_df['muscle_targeted'] == most_trained_muscle) & (~exercise_df['exercise'].isin(exclude_exercises))]
        .groupby('exercise')['date'].nunique().rename('freq')
        .sort_values(ascending=False).reset_index()
    )
    
    generic_plot('pie',data=exercise_freq_for_most_trained,x='exercise',y='freq',
                 pie_legend_title='Exercises',title=f'Exercise frequency for most trained muscle - {most_trained_muscle}')

    # Exercise frequency for least trained muscle
    exercise_freq_for_least_trained = (
        exercise_df[(exercise_df['muscle_targeted'] == least_trained_muscle) & (~exercise_df['exercise'].isin(exclude_exercises))]
        .groupby('exercise')['date'].nunique().rename('freq')
        .sort_values(ascending=False).reset_index()
    )
    
    generic_plot('pie',data=exercise_freq_for_least_trained,x='exercise',y='freq',
                 pie_legend_title='Exercises',title=f'Exercise frequency for least trained muscle - {least_trained_muscle}')
    
    lines = [f"For {most_trained_muscle}, most frequent exercise is - {exercise_freq_for_most_trained['exercise'].iloc[0]}",
             f"For {most_trained_muscle}, least frequent exercise is - {exercise_freq_for_most_trained['exercise'].iloc[-1]}",
             f"For {least_trained_muscle}, most frequent exercise is - {exercise_freq_for_least_trained['exercise'].iloc[0]}",
             f"For {least_trained_muscle}, least frequent exercise is - {exercise_freq_for_least_trained['exercise'].iloc[-1]}"]
    
    display_line_card(lines)
    
    return {'least_trained': least_trained_muscle, 'most_trained': most_trained_muscle, 
            'frequency for least trained': exercise_freq_for_least_trained, 'frequency for most trained': exercise_freq_for_most_trained }


def track_progress_by_phase(analysis_df):
    """
    Tracks workout progress over time both cumulative & in phases.
    
    Args:
        analysis_df: DataFrame with workout and meal data.
    
    Returns:
        dict: Contains cumulative and phase averages.
    """
    
    analysis_df['cumulative_avg_volume'] = analysis_df['total_volume'].expanding().mean()
    generic_plot('line', analysis_df, 'date', 'cumulative_avg_volume', title='Workout Progress Over Time (Cumulative)', 
                 ylabel='Cumulative Avg Volume', xlabel='Time Period', marker='o', color='coral', grid=True, figsize=(20, 5))

    start_date = analysis_df['date'].min()
    def get_phase_label(date):
        delta_days = (date - start_date).days
        if delta_days < 90: return '0-3 months'
        elif delta_days < 100: return '3-6 months'
        elif delta_days < 270: return '6-9 months'
        elif delta_days < 360: return '9-12 months'
        else: return '12+ months'
    
    analysis_df['phase'] = analysis_df['date'].apply(get_phase_label)
    phase_avg = aggregate_data(analysis_df, 'phase', 'total_volume', 'mean')
    generic_plot('bar', phase_avg, 'phase', 'total_volume', 
                 title='Workout Progress Over Time (3-Month Phase)', ylabel='Avg Volume', xlabel='Phases', color='lightgreen')

    return {'cumulative_avg': analysis_df[['date', 'cumulative_avg_volume']], 'phase_avg': phase_avg}


def analyze_hydration_impact(analysis_df):
    """
    Analyzes water intakes impact during workout on overall performance.
    
    Args:
        analysis_df: DataFrame with workout and meal data.
    
    Returns:
        dataframe: Hydration performance data.
    """
    
    analysis_df['vol_per_min'] = analysis_df['total_volume'] / analysis_df['workout_duration']
    
    def hydration_level(val):
        if val < 500: return '<500'
        elif val < 750: return '500-750'
        elif val < 1000: return '750-1000'
        elif val < 1250: return '1000-1250'
        elif val < 1500: return '1250-1500'
        else: return '1500+'
    
    analysis_df['hydration_level'] = analysis_df['hydration'].apply(hydration_level)
    hydration_perf = aggregate_data(analysis_df, 'hydration_level', 'vol_per_min', 'mean')

    generic_plot('bar', hydration_perf, 'hydration_level', 'vol_per_min', title='Hydration impact (during workout) on volume of workout (per minute)', 
                 ylabel='Avg Volume per Minute', xlabel='Water Intake (mL)', hue='hydration_level')
    
    return hydration_perf


def correlate_calories_by_muscle(analysis_df):
    """
    Correlates calorie burn with muscle focus.
    
    Args:
        analysis_df: DataFrame with workout and meal data.
    
    Returns:
        dataframe: Average calories data.
    """
    
    avg_cal = aggregate_data(analysis_df, 'muscle_targeted', 'workout_calories_burnt', 'mean', 'workout_calories_burnt', False)
    generic_plot('line', avg_cal, 'muscle_targeted', 'workout_calories_burnt',
                 title='Average Calories burnt per Workout by Muscle Group', ylabel='Avg Calories (kcal)', xlabel='Muscle Targeted')
    
    return avg_cal


def detect_stall_points(exercise_df, exercise_name='Lat pulldown', muscle_group='Back'):
    """
    Detects stall points in exercise progression.
    
    Args:
        exercise_df: DataFrame with exercise data.
        exercise_name (str): Exercise to analyze (default: 'Lat pulldown').
        muscle_group (str): Muscle group to analyze (default: 'Back').
    
    Returns:
        dataFrame: Stall points data.
    """
    
    # Aggregate and process data
    stall_df = aggregate_data(exercise_df, ['muscle_targeted', 'exercise', 'date'], 'weight', 'mean')
    stall_df = stall_df.sort_values(['muscle_targeted', 'exercise', 'date'])
    stall_df['weight_diff'] = stall_df.groupby(['muscle_targeted', 'exercise'])['weight'].transform('diff')
    stall_df['is_stall'] = stall_df['weight_diff'] == 0
    
    # Filter for the specific exercise and muscle group
    exercise_name_df = stall_df[(stall_df['exercise'] == exercise_name) & (stall_df['muscle_targeted'] == muscle_group)]
    stall_points = exercise_name_df[exercise_name_df['is_stall']]
    
    # Create a single figure
    plt.figure(figsize=(10, 6))
    
    # Plot the line for weight progression
    sns.lineplot(data=exercise_name_df, x='date', y='weight', marker='o', color='blue', label='Weight Progression')
    
    # Plot the scatter for stall points (on the same axes)
    sns.scatterplot(data=stall_points, x='date', y='weight', color='red', marker='X', s=100, label='Stall Points')
    
    # Customize the plot
    plt.title(f'Weight Progression for {exercise_name} ({muscle_group})')
    plt.xlabel('Date')
    plt.ylabel('Average Weight')
    plt.grid(True)
    plt.legend()  # Show legend to differentiate line and scatter
    plt.tight_layout()

    file_name = f"Weight Progression for {exercise_name} ({muscle_group}).png"
    file_path = os.path.join(relative_directory,file_name)
    plt.savefig(file_path)
    
    # Display the plot
    plt.show()
    
    return stall_points


def compare_cardio_strength(analysis_df):
    """
    Compares cardio vs strength workout metrics.
    
    Args:
        analysis_df: DataFrame with workout and meal data.
    
    Returns:
        dict: Contains Summary and trend data.
    """
    
    analysis_df['focus_type'] = analysis_df['muscle_targeted'].apply(lambda x: 'Cardio' if x == 'Cardio' else 'Strength')
    focus_summary = aggregate_data(analysis_df, 'focus_type', ['workout_avg_heart_rate', 'workout_calories_burnt'], 'mean')
    print(focus_summary)
    
    melted = transform_to_long_df(focus_summary, 'focus_type', ['workout_avg_heart_rate', 'workout_calories_burnt'], 'metric', 'value')
    generic_plot('bar', melted, 'metric', 'value', hue='focus_type', 
                 title='Average Heart Rate & Calories- Cardio vs Strength Days', 
                 ylabel='Average Value', xlabel='Metric', grid=False)

    analysis_df['month'] = pd.to_datetime(analysis_df['date']).dt.to_period('M')
    trend_df = aggregate_data(analysis_df, ['month', 'focus_type'], ['workout_avg_heart_rate', 'workout_calories_burnt'], 'mean')
    trend_df['month'] = trend_df['month'].dt.to_timestamp()
    
    generic_plot('line', trend_df, 'month', 'workout_avg_heart_rate', hue='focus_type', 
                 title='Average Heart Rate Over Time', ylabel='Avg Heart Rate', xlabel='Month', 
                 marker='o', grid=True, figsize=(10, 5))
    generic_plot('line', trend_df, 'month', 'workout_calories_burnt', hue='focus_type', 
                 title='Calories Burnt Over Time', ylabel='Avg Calories', xlabel='Month', 
                 marker='o', grid=True, figsize=(10, 5))
    
    return {'focus_summary': focus_summary, 'trends': trend_df}
