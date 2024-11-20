import json

# Define a function to convert binary/categorical data into vectors
def process_binary(value, categories):
    """
    Convert binary or categorical data into a vector.
    Args:
        value (str): The input value to process.
        categories (list of str): The list of all possible categories.

    Returns:
        list of int: A one-hot encoded vector corresponding to the input value.
    """
    vector = [0] * len(categories)  # Initialize a zero vector with the same length as the categories
    if value in categories:
        vector[categories.index(value)] = 1  # Set the position corresponding to the value to 1
    return vector

# Convert days of the week into a vector
def process_days(days):
    """
    Convert day-of-the-week data into a vector representation.
    Args:
        days (list of str): A list of days (e.g., ["Mon", "Wed"]).

    Returns:
        list of int: A binary vector indicating presence for each day of the week.
    """
    week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]  # Standard order of days
    return [1 if day in days else 0 for day in week]  # Mark 1 for present days, 0 otherwise

# Convert grade levels into a one-hot encoded vector
def process_grade(grade, max_grade=4):
    """
    Convert grade level into a one-hot encoded vector.
    Args:
        grade (int): The grade level (1 to max_grade).
        max_grade (int): The maximum possible grade level.

    Returns:
        list of int: A one-hot encoded vector for the grade.
    """
    vector = [0] * max_grade  # Initialize a zero vector
    vector[grade - 1] = 1  # Set the corresponding grade position to 1
    return vector

# Process the number of projects into a one-hot encoded vector
def process_projects(projects, max_projects=5):
    """
    Convert the number of projects into a one-hot encoded vector.
    Args:
        projects (int): Number of current projects.
        max_projects (int): Maximum number of possible projects.

    Returns:
        list of int: A one-hot encoded vector for the project count.
    """
    vector = [0] * max_projects  # Initialize a zero vector
    if projects < max_projects:  # Ensure the value is within range
        vector[projects] = 1  # Set the corresponding index
    return vector

# Main function to vectorize student data
def create_student_vector(student, major_list, goal_list, env_list, tool_list, stack_list, max_grade=4, max_projects=5):
    """
    Transform student data into a vector representation.
    Args:
        student (dict): Dictionary containing student attributes.
        major_list (list): List of possible majors.
        goal_list (list): List of study goals.
        env_list (list): List of preferred study environments.
        tool_list (list): List of preferred study tools.
        stack_list (list): List of programming stacks.
        max_grade (int): Maximum grade level.
        max_projects (int): Maximum number of projects.

    Returns:
        list of int: A combined vector representing the student's data.
    """
    vector = []
    vector += process_binary(student["major"], major_list)
    vector += process_grade(student["grade"], max_grade)
    vector += process_binary(student["study_goal"], goal_list)
    vector += process_binary(student["class_participation"], ["Low", "Moderate", "High"])
    vector += process_binary(student["weekly_study_hours"], ["<5", "5-10", "10-15", "15+"])
    vector += process_projects(student["current_projects"], max_projects)
    vector += process_days(student["available_days"])
    vector += process_binary(student["preferred_time"], ["Morning", "Afternoon", "Evening"])
    vector += process_binary(student["exam_preparation_time"], ["<1 week", "1-2 weeks", ">2 weeks"])
    vector += [1 if student["uses_course_materials"] else 0]  # Binary feature
    vector += [1 if student["self_study_ability"] else 0]  # Binary feature
    vector += process_binary(student["preferred_environment"], env_list)
    vector += process_binary(student["preferred_study_tool"], tool_list)
    vector += process_binary(student["study_intensity"], ["Light", "Moderate", "Intensive"])
    vector += process_binary(student["study_mode"], ["In-person", "Online"])
    vector += process_binary(student["programming_stack"], stack_list)
    vector += [1 if student["research_experience"] else 0]  # Binary feature
    vector += process_binary(student["foreign_languages"], ["English", "Spanish", "Chinese", "Japanese"])
    vector += process_projects(student["online_courses"], max_projects)
    vector += [1 if student["leadership_experience"] else 0]  # Binary feature
    return vector

# Collect user input and construct a student data dictionary
def collect_user_data(major_list, goal_list, env_list, tool_list, stack_list):
    """
    Collect input data from the user and create a student profile dictionary.
    Args:
        major_list (list): List of possible majors.
        goal_list (list): List of possible study goals.
        env_list (list): List of preferred study environments.
        tool_list (list): List of preferred study tools.
        stack_list (list): List of programming stacks.

    Returns:
        dict: A dictionary containing student information.
    """
    print("Enter student details:")
    name = input("Student Name: ")
    major = input(f"Major ({', '.join(major_list)}): ")
    grade = int(input("Grade (1-4): "))
    study_goal = input(f"Study Goal ({', '.join(goal_list)}): ")
    class_participation = input("Class Participation (Low, Moderate, High): ")
    weekly_study_hours = input("Weekly Study Hours (<5, 5-10, 10-15, 15+): ")
    current_projects = int(input("Current Projects (0-5): "))
    available_days = input("Available Days (e.g., Mon,Wed,Fri): ").split(",")
    preferred_time = input("Preferred Study Time (Morning, Afternoon, Evening): ")
    exam_preparation_time = input("Exam Preparation Time (<1 week, 1-2 weeks, >2 weeks): ")
    uses_course_materials = input("Uses Course Materials? (yes/no): ").lower() == "yes"
    self_study_ability = input("Self-Study Ability? (yes/no): ").lower() == "yes"
    preferred_environment = input(f"Preferred Environment ({', '.join(env_list)}): ")
    preferred_study_tool = input(f"Preferred Study Tool ({', '.join(tool_list)}): ")
    study_intensity = input("Study Intensity (Light, Moderate, Intensive): ")
    study_mode = input("Study Mode (In-person, Online): ")
    programming_stack = input("Programming Stack (e.g., Python,Java): ").split(",")
    research_experience = input("Research Experience? (yes/no): ").lower() == "yes"
    foreign_languages = input("Foreign Languages (e.g., English,Chinese): ").split(",")
    online_courses = int(input("Online Courses (0-5): "))
    leadership_experience = input("Leadership Experience? (yes/no): ").lower() == "yes"

    return {
        "name": name,
        "major": major,
        "grade": grade,
        "study_goal": study_goal,
        "class_participation": class_participation,
        "weekly_study_hours": weekly_study_hours,
        "current_projects": current_projects,
        "available_days": available_days,
        "preferred_time": preferred_time,
        "exam_preparation_time": exam_preparation_time,
        "uses_course_materials": uses_course_materials,
        "self_study_ability": self_study_ability,
        "preferred_environment": preferred_environment,
        "preferred_study_tool": preferred_study_tool,
        "study_intensity": study_intensity,
        "study_mode": study_mode,
        "programming_stack": programming_stack,
        "research_experience": research_experience,
        "foreign_languages": foreign_languages,
        "online_courses": online_courses,
        "leadership_experience": leadership_experience
    }

# Save collected data to a JSON file
def save_to_json(data, filename="students_data.json"):
    """
    Save data to a JSON file.
    Args:
        data (list of dict): List of student data dictionaries.
        filename (str): Name of the JSON file to save data.

    Returns:
        None
    """
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# Main execution block
if __name__ == "__main__":
    # Predefined configuration values
    majors = ["Computer Science", "Math", "Biology"]
    goal_list = ["Exam Preparation", "Project", "Research"]
    env_list = ["Library", "Cafe", "Home"]
    tool_list = ["Laptop", "Tablet", "Notebook"]
    stack_list = ["Python", "Java", "C++"]

    # Collect and process student data
    students = []
    while True:
        student_data = collect_user_data(majors, goal_list, env_list, tool_list, stack_list)
        student_vector = create_student_vector(student_data, majors, goal_list, env_list, tool_list, stack_list)
        student_data["vector"] = student_vector
        students.append(student_data)

        more = input("Add another student? (yes/no): ").lower()
        if more != "yes":
            break

    # Save data to JSON file
    save_to_json(students)
    print("Student data and vectors saved to students_data.json.")

    # Print results
    for student in students:
        print(f"{student['name']} Data: {student}")


def load_from_json(filename):
    with open(filename, "r") as f:
        return json.load(f)