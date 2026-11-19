import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

# --- 1. INITIALIZE FIRESTORE ---
# Load the secret service account key and connect to the cloud database
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


# --- 2. CREATE (INSERT DATA) ---
def add_workout():
    """Inserts a new workout document into the 'workouts' collection."""
    date = input("Enter date (YYYY-MM-DD): ")
    split = input("Enter workout split (e.g., Push, Pull, Legs, Upper): ")
    duration = int(input("Enter duration in minutes: "))
    notes = input("Enter session notes: ")

    # Data dictionary to send to Firestore
    workout_data = {
        "date": date,
        "split": split,
        "duration": duration,
        "notes": notes
    }

    # Add document to 'workouts' collection; Firestore generates a unique ID
    update_time, doc_ref = db.collection("workouts").add(workout_data)
    print(f"\n[SUCCESS] Workout saved! Workout ID: {doc_ref.id}")


def add_exercise_log():
    """Inserts an exercise set into 'exercise_logs' linked to a workout_id."""
    # Show existing workouts first so the user can copy/paste the ID
    view_all_workouts()
    
    workout_id = input("\nEnter the Workout ID to link this exercise to: ")
    exercise = input("Enter exercise name (e.g., Bench Press, Squat): ")
    sets = int(input("Enter number of sets: "))
    reps = int(input("Enter reps per set: "))
    weight = float(input("Enter weight (lbs): "))

    # Data dictionary including the relational 'workout_id' link
    log_data = {
        "workout_id": workout_id,
        "exercise": exercise,
        "sets": sets,
        "reps": reps,
        "weight": weight
    }

    # Add document to 'exercise_logs' collection
    update_time, doc_ref = db.collection("exercise_logs").add(log_data)
    print(f"\n[SUCCESS] Exercise logged! Log ID: {doc_ref.id}")


# --- 3. READ (RETRIEVE & QUERY DATA) ---
def view_all_workouts():
    """Retrieves all workouts and their linked exercise logs."""
    print("\n--- ALL WORKOUT SESSIONS ---")
    workouts = db.collection("workouts").stream()

    for w in workouts:
        w_data = w.to_dict()
        print(f"\nWorkout ID: {w.id} | Date: {w_data['date']} | Split: {w_data['split']} ({w_data['duration']} mins)")
        print(f"Notes: {w_data['notes']}")

        # Query 'exercise_logs' where 'workout_id' matches the current workout's ID
        logs = db.collection("exercise_logs").where(
            filter=FieldFilter("workout_id", "==", w.id)
        ).stream()

        for log in logs:
            l_data = log.to_dict()
            print(f"   -> [Log ID: {log.id}] {l_data['exercise']}: {l_data['sets']}x{l_data['reps']} @ {l_data['weight']} lbs")


def filter_by_exercise():
    """Queries the 'exercise_logs' collection for a specific movement."""
    search_name = input("Enter exercise name to search for: ")
    print(f"\n--- HISTORY FOR: {search_name.upper()} ---")

    # Filter documents in the cloud where 'exercise' equals the user's input
    logs = db.collection("exercise_logs").where(
        filter=FieldFilter("exercise", "==", search_name)
    ).stream()

    found = False
    for log in logs:
        found = True
        data = log.to_dict()
        print(f"Log ID: {log.id} | Workout ID: {data['workout_id']} | {data['sets']} sets x {data['reps']} reps @ {data['weight']} lbs")

    if not found:
        print("No matching exercise logs found.")


# --- 4. UPDATE (MODIFY DATA) ---
def update_exercise_log():
    """Updates the weight and reps of an existing exercise log."""
    log_id = input("Enter the Log ID you want to update: ")
    new_weight = float(input("Enter new weight (lbs): "))
    new_reps = int(input("Enter new reps: "))

    # Point to the specific document by ID and update only the specified fields
    log_ref = db.collection("exercise_logs").document(log_id)
    log_ref.update({
        "weight": new_weight,
        "reps": new_reps
    })
    print(f"\n[SUCCESS] Log {log_id} updated!")


# --- 5. DELETE (REMOVE DATA) ---
def delete_workout():
    """Deletes a workout AND all exercise logs linked to it."""
    workout_id = input("Enter the Workout ID to delete: ")

    # 1. Delete the parent workout document
    db.collection("workouts").document(workout_id).delete()

    linked_logs = db.collection("exercise_logs").where(
    # 2. Find and delete all child exercise logs linked to this workout
        filter=FieldFilter("workout_id", "==", workout_id)
    ).stream()

    deleted_count = 0
    for log in linked_logs:
        db.collection("exercise_logs").document(log.id).delete()
        deleted_count += 1

    print(f"\n[SUCCESS] Workout {workout_id} and {deleted_count} linked exercise logs deleted!")


# --- 6. INTERACTIVE CLI MENU ---
def main():
    """Runs the main command-line interface loop."""
    while True:
        print("\n=== CLOUD WORKOUT TRACKER ===")
        print("1. Add Workout Session")
        print("2. Log Exercise to a Workout")
        print("3. View All Workouts & Exercises")
        print("4. Search History by Exercise Name")
        print("5. Update Exercise Weight/Reps")
        print("6. Delete Workout Session")
        print("7. Exit")

        choice = input("Select an option (1-7): ")

        if choice == "1":
            add_workout()
        elif choice == "2":
            add_exercise_log()
        elif choice == "3":
            view_all_workouts()
        elif choice == "4":
            filter_by_exercise()
        elif choice == "5":
            update_exercise_log()
        elif choice == "6":
            delete_workout()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")

if __name__ == "__main__":
    main()