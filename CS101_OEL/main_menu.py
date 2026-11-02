from tasks import (
    addTasks, editTask, deleteTask,
    searchTasks, mark_complete,
    start_task_timer, stop_task_timer,
    completion_statistics,
    deadline_risk_analysis,
    daily_planner,
    auto_scheduler,
    viewTasks, productivity_dashboard, export_to_calendar
)

from storage import load_user




def main_menu():
    while True:
        print("\n==== TASK MANAGER ====")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Edit Task")
        print("4. Delete Task")
        print("5. Mark Task Complete")
        print("6. Search Tasks")
        print("7. Start Task Timer")
        print("8. Stop Task Timer")
        print("9. View Completion Statistics")
        print("10. Deadline Risk Analysis")
        print("11. Daily Planner")
        print("12. Auto Scheduler")
        print("13. View User Info")
        print("14. Productivity Dashboard")
        print("15. Export Tasks to Calendar")
        print("16. Exit")


        choice = input("Choose an option (1-16): ")

        if choice == "1":
            name = input("Task Name: ")
            priority = input("Priority (Low/Medium/High): ")
            category = input("Category: ")
            deadline = input("Deadline (YYYY-MM-DD): ")
            addTasks(name, priority, category, deadline)

        elif choice == "2":
            viewTasks()

        elif choice == "3":
            task_id = int(input("Enter Task ID to edit: "))
            new_name = input("New name (leave empty to skip): ") or None
            new_priority = input("New priority (leave empty to skip): ") or None
            new_category = input("New category (leave empty to skip): ") or None
            new_deadline = input("New deadline (leave empty to skip): ") or None
            editTask(task_id, new_name, new_priority, new_category, new_deadline)

        elif choice == "4":
            task_id = int(input("Enter Task ID to delete: "))
            deleteTask(task_id)

        elif choice == "5":
            task_id = int(input("Enter Task ID to mark complete: "))
            mark_complete(task_id)

        elif choice == "6":
            print("\nSearch Options:")
            print("Leave blank if you don't want to filter by that field.")
            name = input("Search by name: ") or None
            priority = input("Search by priority: ") or None
            category = input("Search by category: ") or None
            deadline = input("Search by deadline (YYYY-MM-DD): ") or None
            searchTasks(name=name, priority=priority, category=category, deadline=deadline)

        elif choice == "7":
            task_id = int(input("Enter Task ID to start timer: "))
            start_task_timer(task_id)
            
        elif choice == "8":
            task_id = int(input("Enter Task ID to stop timer: "))
            stop_task_timer(task_id)
        
        elif choice == "9":
         completion_statistics()
    
        elif choice == "10":
         deadline_risk_analysis()
         
        elif choice == "11":
             daily_planner()
             
        elif choice == "12":
             hours = int(input("Hours available today: "))
             auto_scheduler(hours)
        
        elif choice == "13":
            user_data = load_user()
            print(f"User: {user_data['name']}, Points: {user_data['points']}, Level: {user_data['level']}")
        
        elif choice == "14":
            export_to_calendar()
            
        elif choice == "15":
            productivity_dashboard()

        elif choice == "16":
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid option. Please enter a number from 1 to 16.")

if __name__ == "__main__":
    main_menu()
