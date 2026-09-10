#Sonya Manley
#CIS261
#WK10 VIBE CODING - Student Grade Calculator

import os
import json

class Student:
    """Class to represent a student with grades"""
    def __init__(self, name, student_id, test1, test2, test3):
        self.name = name
        self.id = student_id
        self.test1 = test1
        self.test2 = test2
        self.test3 = test3
        self.average = self.calculate_average()
        self.grade = self.calculate_grade()
    
    def calculate_average(self):
        """Calculate average of three test scores"""
        return (self.test1 + self.test2 + self.test3) / 3
    
    def calculate_grade(self):
        """Calculate letter grade based on average"""
        if self.average >= 90:
            return 'A'
        elif self.average >= 80:
            return 'B'
        elif self.average >= 70:
            return 'C'
        elif self.average >= 60:
            return 'D'
        else:
            return 'F'
    
    def __str__(self):
        """String representation for file output"""
        return f"{self.name}|{self.id}|{self.test1:.2f}|{self.test2:.2f}|{self.test3:.2f}|{self.average:.2f}|{self.grade}"


def add_student(students):
    """Add a new student record"""
    try:
        print("\n--- Add New Student ---")
        name = input("Enter student name: ").strip()
        if not name:
            print("Error: Student name cannot be empty.")
            return
        
        student_id = input("Enter student ID: ").strip()
        if not student_id:
            print("Error: Student ID cannot be empty.")
            return
        
        # Check if ID already exists
        if any(s.id == student_id for s in students):
            print(f"Error: Student ID {student_id} already exists.")
            return
        
        test1 = get_valid_score("Enter Test 1 score (0-100): ")
        if test1 is None:
            return
        
        test2 = get_valid_score("Enter Test 2 score (0-100): ")
        if test2 is None:
            return
        
        test3 = get_valid_score("Enter Test 3 score (0-100): ")
        if test3 is None:
            return
        
        student = Student(name, student_id, test1, test2, test3)
        students.append(student)
        print(f"\nStudent {name} added successfully!")
        print(f"Average: {student.average:.2f} | Grade: {student.grade}")
    
    except Exception as e:
        print(f"Error adding student: {e}")


def get_valid_score(prompt):
    """Get and validate a test score"""
    while True:
        try:
            score = float(input(prompt))
            if 0 <= score <= 100:
                return score
            else:
                print("Error: Score must be between 0 and 100.")
        except ValueError:
            print("Error: Please enter a valid number.")


def display_all_students(students):
    """Display all students in a formatted table"""
    if not students:
        print("\nNo students in the system yet.")
        return
    
    print("\n" + "="*100)
    print(f"{'Name':<20} {'ID':<12} {'Test 1':<10} {'Test 2':<10} {'Test 3':<10} {'Average':<10} {'Grade':<8}")
    print("="*100)
    
    for student in students:
        print(f"{student.name:<20} {student.id:<12} {student.test1:<10.2f} {student.test2:<10.2f} {student.test3:<10.2f} {student.average:<10.2f} {student.grade:<8}")
    
    print("="*100)


def display_class_statistics(students):
    """Calculate and display class statistics"""
    if not students:
        print("\nNo students in the system yet.")
        return
    
    averages = [s.average for s in students]
    
    highest = max(averages)
    lowest = min(averages)
    class_average = sum(averages) / len(averages)
    
    print("\n" + "="*50)
    print("CLASS STATISTICS")
    print("="*50)
    print(f"Number of Students: {len(students)}")
    print(f"Highest Average: {highest:.2f}")
    print(f"Lowest Average: {lowest:.2f}")
    print(f"Class Average: {class_average:.2f}")
    print("="*50)


def search_student(students):
    """Search for a student by name (case-insensitive)"""
    if not students:
        print("\nNo students in the system yet.")
        return
    
    search_name = input("\nEnter student name to search: ").strip().lower()
    results = [s for s in students if s.name.lower() == search_name]
    
    if results:
        print("\n" + "="*100)
        print(f"SEARCH RESULTS FOR '{search_name.upper()}'")
        print("="*100)
        print(f"{'Name':<20} {'ID':<12} {'Test 1':<10} {'Test 2':<10} {'Test 3':<10} {'Average':<10} {'Grade':<8}")
        print("-"*100)
        for student in results:
            print(f"{student.name:<20} {student.id:<12} {student.test1:<10.2f} {student.test2:<10.2f} {student.test3:<10.2f} {student.average:<10.2f} {student.grade:<8}")
        print("="*100)
    else:
        print(f"\nNo student found with name '{search_name}'")


def save_to_file(students, filename="student_grades.txt"):
    """Save student records to a pipe-delimited file"""
    try:
        with open(filename, 'w') as file:
            for student in students:
                file.write(str(student) + '\n')
        print(f"\nStudents saved to {filename} successfully!")
    except Exception as e:
        print(f"Error saving to file: {e}")


def load_from_file(filename="student_grades.txt"):
    """Load student records from file"""
    students = []
    
    if not os.path.exists(filename):
        print(f"File {filename} does not exist. Starting with empty student list.")
        return students
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 7:
                        name, student_id, test1, test2, test3, average, grade = parts
                        try:
                            student = Student(name, student_id, float(test1), float(test2), float(test3))
                            students.append(student)
                        except ValueError:
                            print(f"Warning: Skipping invalid record: {line}")
        print(f"Loaded {len(students)} student(s) from {filename}")
    except Exception as e:
        print(f"Error loading from file: {e}")
    
    return students


def display_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("STUDENT GRADE CALCULATOR")
    print("="*50)
    print("1. Add New Student")
    print("2. Display All Students")
    print("3. Display Class Statistics")
    print("4. Search Student by Name")
    print("5. Save and Exit")
    print("Press ESC to Exit Without Saving")
    print("="*50)


def main():
    """Main program loop"""
    students = load_from_file()
    
    while True:
        display_menu()
        choice = input("Select an option (1-5) or press ESC to exit: ").strip().upper()
        
        if choice == '\x1b':  # ESC key
            print("\nExiting without saving. Goodbye!")
            break
        elif choice == '1':
            add_student(students)
        elif choice == '2':
            display_all_students(students)
        elif choice == '3':
            display_class_statistics(students)
        elif choice == '4':
            search_student(students)
        elif choice == '5':
            save_to_file(students)
            print("Thank you for using the Student Grade Calculator!")
            break
        else:
            print("Invalid option. Please select 1-5 or press ESC.")


if __name__ == "__main__":
    main()