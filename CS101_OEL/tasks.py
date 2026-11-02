from storage import save_tasks, load_tasks, load_user, save_user
import time
from datetime import datetime




def addTasks(name, priority="Medium", category="General", deadline=None):
    task = load_tasks()
    new_id = max([t['id'] for t in task], default=0) + 1
    new_task = {
        "id": new_id,
        "name": name,
        "completed": False,
        "priority": priority,
        "category": category,
        "deadline": deadline,
        "points_awarded": False,
        "time_spent": 0,
        "timer_running": False,
        "start_time": None
    }
    task.append(new_task)
    save_tasks(task)
    print(f"Task '{name}' added successfully. ID is {new_id}.")
    


def viewTasks(filter_completed=None):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    print("\n----- ALL TASKS -----")
    for task in tasks:
        print(f"""
ID: {task['id']}
Name: {task['name']}
Priority: {task['priority']}
Category: {task['category']}
Deadline: {task['deadline']}
Completed: {task['completed']}
----------------------""")
    
def searchTasks(name=None, priority=None, category=None, deadline=None):
    tasks = load_tasks()
    
    if not tasks:
        print("No tasks found.")
        return
    results = tasks
    
    if name:
        results = [task for task in results if name.lower() in task['name'].lower()]
        
    if priority:
        results = [task for task in results if task['priority'].lower() == priority.lower()]


    if category:
        results = [task for task in results if task['category'].lower() == category.lower()]
 
    if deadline:
        results = [task for task in results if task['deadline'] == deadline]
        
    if not results:
        print("\n-- No matching tasks found. --\n")
        return
    
    print("\n----- SEARCH RESULTS -----")
    for task in results:
        print(f"""
ID: {task['id']}
Name: {task['name']}    
Priority: {task['priority']}
Category: {task['category']}
Deadline: {task['deadline']}
Completed: {task['completed']}
----------------------""")

def update_level(user):
    user["level"] = user["points"] // 100 + 1


def mark_complete(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:

            if task["completed"]:
                print("Task already completed.")
                return

            task["completed"] = True
            task["completed_date"] = datetime.today().strftime("%Y-%m-%d")

            save_tasks(tasks)
            print(f"Task '{task['name']}' marked complete.")
            return

    print("Task ID not found.")



    
    
def deleteTask(task_id):
    tasks = load_tasks()
    new_tasks = [task for task in tasks if task['id'] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"Task ID {task_id} not found.")
        return
    save_tasks(new_tasks)
    print(f"Task ID {task_id} deleted successfully.")
    
    
def editTask(task_id, name=None, priority=None, category=None, deadline=None):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            if name:
                task['name'] = name
            if priority:
                task['priority'] = priority
            if category:
                task['category'] = category
            if deadline:
                task['deadline'] = deadline
            save_tasks(tasks)
            print(f"Task ID {task_id} updated successfully.")
            return
        print(f"Task ID {task_id} not found.")\
            
            
def start_task_timer(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:

            if task["timer_running"]:
                print("Timer already running for this task.")
                return

            task["start_time"] = time.time()
            task["timer_running"] = True

            save_tasks(tasks)
            print(f"Timer started for task '{task['name']}'.")
            return

    print("Task ID not found.")
    





def stop_task_timer(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:

            if not task["timer_running"]:
                print("Timer is not running for this task.")
                return

            elapsed = time.time() - task["start_time"]
            task["time_spent"] += int(elapsed)

            task["start_time"] = None
            task["timer_running"] = False

            save_tasks(tasks)

            minutes = task["time_spent"] // 60
            seconds = task["time_spent"] % 60

            print(f"Timer stopped. Total time spent: {minutes}m {seconds}s.")
            return

    print("Task ID not found.")
    
    
def completion_statistics():
    tasks = load_tasks()

    if not tasks:
        print("No tasks available.")
        return

    total_tasks = len(tasks)
    completed_tasks = [t for t in tasks if t["completed"]]

    completed_count = len(completed_tasks)
    completion_rate = (completed_count / total_tasks) * 100

    total_time_spent = sum(t["time_spent"] for t in completed_tasks)

    if completed_count > 0:
        avg_time = total_time_spent // completed_count
    else:
        avg_time = 0

    print("\n--- COMPLETION STATISTICS ---")
    print(f"Total tasks: {total_tasks}")
    print(f"Completed tasks: {completed_count}")
    print(f"Completion rate: {completion_rate:.2f}%")

    print(f"Total time spent: {total_time_spent // 60} min")
    print(f"Average time per completed task: {avg_time // 60} min")
    priorities = {"low": 0, "medium": 0, "high": 0}

    for task in completed_tasks:
        p = task["priority"].lower()
        if p in priorities:
            priorities[p] += 1

    print("\nCompleted tasks by priority:")
    for p, count in priorities.items():
        print(f"{p.capitalize()}: {count}")



def deadline_risk_analysis():
    tasks = load_tasks()

    if not tasks:
        print("No tasks available.")
        return

    today = datetime.today().date()

    print("\n--- DEADLINE RISK ANALYSIS ---")

    for task in tasks:

        if task["completed"]:
            continue

        deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
        days_left = (deadline - today).days

        if days_left < 0:
            risk = "OVERDUE"
        elif days_left == 0:
            risk = "HIGH (Due Today)"
        elif days_left <= 2:
            risk = "MEDIUM"
        elif days_left <= 5:
            risk = "LOW"
        else:
            risk = "SAFE"

        print(f"[{risk}] {task['name']} → {days_left} days left")


def daily_planner():
    tasks = load_tasks()
    today = datetime.today().date()

    today_tasks = []

    for task in tasks:
        if task["completed"]:
            continue

        deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
        days_left = (deadline - today).days

        # Skip tasks far in the future
        if days_left > 5:
            continue

        # Risk score
        if days_left < 0:
            risk_score = 0
        elif days_left == 0:
            risk_score = 1
        elif days_left <= 2:
            risk_score = 2
        else:
            risk_score = 3

        # Priority score
        priority_map = {"high": 0, "medium": 1, "low": 2}
        priority_score = priority_map.get(task["priority"].lower(), 2)

        today_tasks.append((
            risk_score,
            priority_score,
            deadline,
            task
        ))

    # Sort intelligently
    today_tasks.sort(key=lambda x: (x[0], x[1], x[2]))

    print("\n--- TODAY'S PLAN ---")

    if not today_tasks:
        print("No urgent tasks today 🎉")
        return

    for _, _, deadline, task in today_tasks:
        print(f"- {task['name']} (Due: {deadline}, Priority: {task['priority']})")



def estimate_task_time(task):
    # If task has recorded time, use it
    if task["time_spent"] > 0:
        return task["time_spent"] // 60  # minutes

    # Default estimate
    estimate = 30

    # Priority adjustment
    if task["priority"].lower() == "high":
        estimate += 10

    return estimate



def auto_scheduler(available_hours):
    tasks = load_tasks()
    today = datetime.today().date()

    available_minutes = available_hours * 60
    schedule = []

    candidate_tasks = []

    for task in tasks:
        if task["completed"]:
            continue

        deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
        days_left = (deadline - today).days

        # Skip non-urgent tasks
        if days_left > 7:
            continue

        # Risk score
        if days_left < 0:
            risk = 0
        elif days_left == 0:
            risk = 1
        elif days_left <= 2:
            risk = 2
        else:
            risk = 3

        priority_map = {"high": 0, "medium": 1, "low": 2}
        priority = priority_map.get(task["priority"].lower(), 2)

        estimated_time = estimate_task_time(task)

        candidate_tasks.append((
            risk,
            priority,
            deadline,
            estimated_time,
            task
        ))

    # Sort by urgency
    candidate_tasks.sort(key=lambda x: (x[0], x[1], x[2]))

    for _, _, _, est_time, task in candidate_tasks:
        if available_minutes >= est_time:
            schedule.append((task["name"], est_time))
            available_minutes -= est_time

    print("\n--- AUTO SCHEDULE ---")

    if not schedule:
        print("No tasks could be scheduled.")
        return

    for name, minutes in schedule:
        print(f"- {name} → {minutes} min")

    print(f"\nUnused time: {available_minutes} min")
    
    
def productivity_dashboard():
    tasks = load_tasks()
    user = load_user()
    today = datetime.today().date()

    total_tasks = len(tasks)
    completed_tasks = [t for t in tasks if t["completed"]]
    completed_count = len(completed_tasks)

    completion_rate = (completed_count / total_tasks * 100) if total_tasks else 0

    total_time = sum(t["time_spent"] for t in completed_tasks)
    avg_time = (total_time // completed_count) if completed_count else 0

    # Priority stats
    priority_count = {"low": 0, "medium": 0, "high": 0}
    for t in completed_tasks:
        p = t["priority"].lower()
        if p in priority_count:
            priority_count[p] += 1

    most_common_priority = max(priority_count, key=priority_count.get) if completed_tasks else "N/A"

    # Tasks completed today
    completed_today = 0
    for t in completed_tasks:
        if "completed_date" in t:
            completed_date = datetime.strptime(t["completed_date"], "%Y-%m-%d").date()
            if completed_date == today:
                completed_today += 1

    # Overdue tasks
    overdue_tasks = 0
    for t in tasks:
        if not t["completed"]:
            deadline = datetime.strptime(t["deadline"], "%Y-%m-%d").date()
            if deadline < today:
                overdue_tasks += 1

    print("\n📊 PRODUCTIVITY DASHBOARD")
    print("-" * 30)
    print(f"Total tasks: {total_tasks}")
    print(f"Completed tasks: {completed_count}")
    print(f"Completion rate: {completion_rate:.2f}%")
    print(f"Total time worked: {total_time // 60} min")
    print(f"Average task time: {avg_time // 60} min")
    print(f"Most completed priority: {most_common_priority.capitalize()}")
    print(f"Tasks completed today: {completed_today}")
    print(f"Overdue tasks remaining: {overdue_tasks}")

def export_to_calendar(filename="tasks.ics"):
    tasks = load_tasks()
    today = datetime.today().date()

    events = []

    for task in tasks:
        if task["completed"]:
            continue

        deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()

        # Only export upcoming tasks
        if deadline < today:
            continue

        duration_minutes = estimate_task_time(task)

        start_time = datetime.combine(deadline, datetime.min.time()).replace(hour=9)
        end_time = start_time + timedelta(minutes=duration_minutes)

        event = f"""
BEGIN:VEVENT
SUMMARY:{task['name']}
DTSTART:{start_time.strftime('%Y%m%dT%H%M%S')}
DTEND:{end_time.strftime('%Y%m%dT%H%M%S')}
DESCRIPTION:Priority: {task['priority']} | Category: {task['category']}
END:VEVENT
"""
        events.append(event)

    if not events:
        print("No tasks to export.")
        return

    calendar = "BEGIN:VCALENDAR\nVERSION:2.0\n" + "".join(events) + "END:VCALENDAR"

    with open(filename, "w") as f:
        f.write(calendar)

    print(f"📅 Calendar exported to {filename}")
