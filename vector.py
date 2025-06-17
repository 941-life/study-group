import json
import logging
from typing import List, Dict, Any, Union
from config import *

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, LOG_LEVEL))

# Create console handler if no handlers exist
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

def validate_input(value: Any, valid_options: List[str], field_name: str) -> None:
    """
    Validate input value against a list of valid options.
    
    Args:
        value: The input value to validate
        valid_options: List of valid options
        field_name: Name of the field being validated
    
    Raises:
        ValidationError: If the input value is not valid
    """
    if value not in valid_options:
        raise ValidationError(f"Invalid {field_name}: {value}. Must be one of {valid_options}")

def validate_numeric_range(value: int, min_val: int, max_val: int, field_name: str) -> None:
    """
    Validate if a numeric value is within the specified range.
    
    Args:
        value: The numeric value to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        field_name: Name of the field being validated
    
    Raises:
        ValidationError: If the value is not within the range
    """
    if not min_val <= value <= max_val:
        raise ValidationError(f"{field_name} must be between {min_val} and {max_val}")

def process_binary(value: str, categories: List[str]) -> List[int]:
    """
    Convert binary or categorical data into a vector.
    
    Args:
        value: The input value to process
        categories: The list of all possible categories
    
    Returns:
        A one-hot encoded vector corresponding to the input value
    """
    vector = [0] * len(categories)
    if value in categories:
        vector[categories.index(value)] = 1
    return vector

def process_days(days: List[str]) -> List[int]:
    """
    Convert day-of-the-week data into a vector representation.
    
    Args:
        days: A list of days (e.g., ["Mon", "Wed"])
    
    Returns:
        A binary vector indicating presence for each day of the week
    """
    week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return [1 if day in days else 0 for day in week]

def process_grade(grade: int) -> List[int]:
    """
    Convert grade level into a one-hot encoded vector.
    
    Args:
        grade: The grade level
    
    Returns:
        A one-hot encoded vector for the grade
    """
    validate_numeric_range(grade, MIN_GRADE, MAX_GRADE, "Grade")
    vector = [0] * MAX_GRADE
    vector[grade - 1] = 1
    return vector

def process_projects(projects: int) -> List[int]:
    """
    Convert the number of projects into a one-hot encoded vector.
    
    Args:
        projects: Number of current projects
    
    Returns:
        A one-hot encoded vector for the project count
    """
    validate_numeric_range(projects, MIN_PROJECTS, MAX_PROJECTS, "Number of projects")
    vector = [0] * (MAX_PROJECTS + 1)
    vector[projects] = 1
    return vector

def create_student_vector(student: Dict[str, Any]) -> List[int]:
    """
    Transform student data into a vector representation.
    
    Args:
        student: Dictionary containing student attributes
    
    Returns:
        A combined vector representing the student's data
    """
    try:
        vector = []
        vector += process_binary(student["major"], MAJORS)
        vector += process_grade(student["grade"])
        vector += process_binary(student["study_goal"], GOALS)
        vector += process_binary(student["class_participation"], CLASS_PARTICIPATION_LEVELS)
        vector += process_binary(student["weekly_study_hours"], WEEKLY_STUDY_HOURS)
        vector += process_projects(student["current_projects"])
        vector += process_days(student["available_days"])
        vector += process_binary(student["preferred_time"], PREFERRED_TIMES)
        vector += process_binary(student["exam_preparation_time"], EXAM_PREP_TIMES)
        vector += [1 if student["uses_course_materials"] else 0]
        vector += [1 if student["self_study_ability"] else 0]
        vector += process_binary(student["preferred_environment"], ENVIRONMENTS)
        vector += process_binary(student["preferred_study_tool"], STUDY_TOOLS)
        vector += process_binary(student["study_intensity"], STUDY_INTENSITY)
        vector += process_binary(student["study_mode"], STUDY_MODES)
        vector += process_binary(student["programming_stack"], PROGRAMMING_STACKS)
        vector += [1 if student["research_experience"] else 0]
        vector += process_binary(student["foreign_languages"], FOREIGN_LANGUAGES)
        vector += process_projects(student["online_courses"])
        vector += [1 if student["leadership_experience"] else 0]
        return vector
    except KeyError as e:
        raise ValidationError(f"Missing required field: {e}")
    except Exception as e:
        logger.error(f"Error creating student vector: {e}")
        raise

def collect_user_data() -> Dict[str, Any]:
    """
    Collect input data from the user and create a student profile dictionary.
    
    Returns:
        A dictionary containing student information
    """
    try:
        print("\nEnter student details:")
        name = input("Student Name: ").strip()
        if not name:
            raise ValidationError("Name cannot be empty")

        major = input(f"Major ({', '.join(MAJORS)}): ").strip()
        validate_input(major, MAJORS, "major")

        grade = int(input("Grade (1-4): "))
        validate_numeric_range(grade, MIN_GRADE, MAX_GRADE, "Grade")

        study_goal = input(f"Study Goal ({', '.join(GOALS)}): ").strip()
        validate_input(study_goal, GOALS, "study goal")

        class_participation = input(f"Class Participation ({', '.join(CLASS_PARTICIPATION_LEVELS)}): ").strip()
        validate_input(class_participation, CLASS_PARTICIPATION_LEVELS, "class participation")

        weekly_study_hours = input(f"Weekly Study Hours ({', '.join(WEEKLY_STUDY_HOURS)}): ").strip()
        validate_input(weekly_study_hours, WEEKLY_STUDY_HOURS, "weekly study hours")

        current_projects = int(input("Current Projects (0-5): "))
        validate_numeric_range(current_projects, MIN_PROJECTS, MAX_PROJECTS, "Number of projects")

        available_days = [day.strip() for day in input("Available Days (e.g., Mon,Wed,Fri): ").split(",")]
        for day in available_days:
            validate_input(day, ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "available day")

        preferred_time = input(f"Preferred Study Time ({', '.join(PREFERRED_TIMES)}): ").strip()
        validate_input(preferred_time, PREFERRED_TIMES, "preferred time")

        exam_preparation_time = input(f"Exam Preparation Time ({', '.join(EXAM_PREP_TIMES)}): ").strip()
        validate_input(exam_preparation_time, EXAM_PREP_TIMES, "exam preparation time")

        uses_course_materials = input("Uses Course Materials? (yes/no): ").lower() == "yes"
        self_study_ability = input("Self-Study Ability? (yes/no): ").lower() == "yes"

        preferred_environment = input(f"Preferred Environment ({', '.join(ENVIRONMENTS)}): ").strip()
        validate_input(preferred_environment, ENVIRONMENTS, "preferred environment")

        preferred_study_tool = input(f"Preferred Study Tool ({', '.join(STUDY_TOOLS)}): ").strip()
        validate_input(preferred_study_tool, STUDY_TOOLS, "preferred study tool")

        study_intensity = input(f"Study Intensity ({', '.join(STUDY_INTENSITY)}): ").strip()
        validate_input(study_intensity, STUDY_INTENSITY, "study intensity")

        study_mode = input(f"Study Mode ({', '.join(STUDY_MODES)}): ").strip()
        validate_input(study_mode, STUDY_MODES, "study mode")

        programming_stack = [stack.strip() for stack in input(f"Programming Stack ({', '.join(PROGRAMMING_STACKS)}): ").split(",")]
        for stack in programming_stack:
            validate_input(stack, PROGRAMMING_STACKS, "programming stack")

        research_experience = input("Research Experience? (yes/no): ").lower() == "yes"
        
        foreign_languages = [lang.strip() for lang in input(f"Foreign Languages ({', '.join(FOREIGN_LANGUAGES)}): ").split(",")]
        for lang in foreign_languages:
            validate_input(lang, FOREIGN_LANGUAGES, "foreign language")

        online_courses = int(input("Online Courses (0-5): "))
        validate_numeric_range(online_courses, MIN_ONLINE_COURSES, MAX_ONLINE_COURSES, "Number of online courses")

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
    except ValueError as e:
        raise ValidationError(f"Invalid input format: {e}")
    except Exception as e:
        logger.error(f"Error collecting user data: {e}")
        raise

def save_to_json(data: List[Dict[str, Any]], filename: str = DATA_FILE) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: List of student data dictionaries
        filename: Name of the JSON file to save data
    """
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        logger.info(f"Data successfully saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving data to {filename}: {e}")
        raise

def load_from_json(filename: str = DATA_FILE) -> List[Dict[str, Any]]:
    """
    Load data from a JSON file.
    
    Args:
        filename: Name of the JSON file to load data from
    
    Returns:
        List of student data dictionaries
    """
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        logger.info(f"Data successfully loaded from {filename}")
        return data
    except FileNotFoundError:
        logger.warning(f"File {filename} not found. Creating new file.")
        return []
    except Exception as e:
        logger.error(f"Error loading data from {filename}: {e}")
        raise

if __name__ == "__main__":
    try:
        students = []
        while True:
            try:
                student_data = collect_user_data()
                student_vector = create_student_vector(student_data)
                student_data["vector"] = student_vector
                students.append(student_data)
                logger.info(f"Successfully added student: {student_data['name']}")

                more = input("\nAdd another student? (yes/no): ").lower()
                if more != "yes":
                    break
            except ValidationError as e:
                logger.error(f"Validation error: {e}")
                print(f"\nError: {e}")
                continue

        if students:
            save_to_json(students)
            print("\nStudent data and vectors saved to students_data.json")
            
            # Print summary
            print("\nSummary of added students:")
            for student in students:
                print(f"- {student['name']}: {student['major']} (Grade {student['grade']})")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\nAn unexpected error occurred: {e}")