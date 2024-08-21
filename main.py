import datetime
import random

class VaccinationSystem:
    def __init__(self):
        self.records = {}
        self.hospitals = [
            "Healthcare 1: Mahipalpur",
            "Healthcare 2: Gurudwara Bangla Sahib",
            "Healthcare 3: Rajiv Chowk",
            "Healthcare 4: Lal Quila",
            "Healthcare 5: Lajpat Nagar",
            "Healthcare 6: Faridabad",
            "Healthcare 7: Rohini",
            "Healthcare 8: Cannaught Place"
        ]
        self.vaccine_schedule = {
            "Birth to 6 Months": {
                "Hepatitis B (HepB)": ["Birth", "1-2 months", "6-18 months"],
                "Rotavirus (RV)": ["2 months", "4 months", "6 months if needed"],
                "Diphtheria, Tetanus, and acellular Pertussis (DTaP)": ["2 months", "4 months", "6 months"],
                "Haemophilus influenzae type b (Hib)": ["2 months", "4 months", "6 months"],
                "Pneumococcal conjugate (PCV13)": ["2 months", "4 months", "6 months"],
                "Inactivated Poliovirus (IPV)": ["2 months", "4 months", "6-18 months"]
            },
            "6 to 18 Months": {
                "Influenza (Flu)": ["Annually starting at 6 months"],
                "Measles, Mumps, and Rubella (MMR)": ["12-15 months"],
                "Varicella (Chickenpox)": ["12-15 months"],
                "Hepatitis A (HepA)": ["12-23 months (2 doses, 6 months apart)"]
            },
            "18 Months to 4 Years": {
                "DTaP": ["15-18 months"],
                "Hib": ["12-15 months"],
                "PCV13": ["12-15 months"],
                "IPV": ["4-6 years"]
            },
            "4 to 6 Years": {
                "DTaP": ["4-6 years"],
                "MMR": ["4-6 years"],
                "Varicella": ["4-6 years"]
            },
            "7 to 10 Years": {
                "Influenza (Flu)": ["Annually"]
            }
        }

    def generate_unique_id(self):
        while True:
            user_id = str(random.randint(1000, 9999))
            if user_id not in self.records:
                return user_id

    def add_child(self):
        name = input("Enter child's name: ")
        dob = input("Enter child's date of birth (YYYY-MM-DD): ")
        user_id = self.generate_unique_id()
        self.records[user_id] = {
            'Name': name,
            'DOB': dob,
            'appointments': [],
            'growth': {}
        }
        print(f"Child {name} added successfully with User ID: {user_id}!\n")

    def select_child(self):
        if not self.records:
            print("No children have been added yet.\n")
            return None

        print("Select a child:")
        for idx, (user_id, info) in enumerate(self.records.items(), 1):
            print(f"{idx}. {info['Name']} (User ID: {user_id})")

        while True:
            try:
                choice = int(input("Enter your choice: "))
                if 1 <= choice <= len(self.records):
                    selected_user_id = list(self.records.keys())[choice - 1]
                    return selected_user_id
                else:
                    print("Invalid choice! Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def select_location(self):
        print("Select a location:")
        for idx, hospital in enumerate(self.hospitals, 1):
            print(f"{idx}. {hospital}")

        while True:
            try:
                choice = int(input("Enter your choice: "))
                if 1 <= choice <= len(self.hospitals):
                    selected_location = self.hospitals[choice - 1]
                    return selected_location
                else:
                    print("Invalid choice! Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def calculate_age(self, dob):
        dob_date = datetime.datetime.strptime(dob, "%Y-%m-%d")
        today = datetime.datetime.today()
        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
        return age

    def get_vaccine_options(self, age):
        if age < 6:
            return self.vaccine_schedule["Birth to 6 Months"]
        elif 6 <= age < 18:
            return self.vaccine_schedule["6 to 18 Months"]
        elif 18 <= age < 48:
            return self.vaccine_schedule["18 Months to 4 Years"]
        elif 48 <= age < 72:
            return self.vaccine_schedule["4 to 6 Years"]
        else:
            return self.vaccine_schedule["7 to 10 Years"]

    def book_appointment(self):
        user_id = self.select_child()
        if user_id:
            child_info = self.records[user_id]
            dob = child_info['DOB']
            age = self.calculate_age(dob)
            vaccine_options = self.get_vaccine_options(age)
            
            print("Select a vaccine:")
            for idx, (vaccine, schedule) in enumerate(vaccine_options.items(), 1):
                print(f"{idx}. {vaccine} ({', '.join(schedule)})")

            while True:
                try:
                    choice = int(input("Enter your choice: "))
                    if 1 <= choice <= len(vaccine_options):
                        selected_vaccine = list(vaccine_options.keys())[choice - 1]
                        break
                    else:
                        print("Invalid choice! Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
            
            while True:
                date_str = input("Enter the appointment date (YYYY-MM-DD): ")
                appointment_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                if appointment_date > datetime.datetime.today():
                    break
                else:
                    print("Appointment date must be in the future. Please try again.")

            location = self.select_location()
            self.records[user_id]['appointments'].append({
                'vaccine': selected_vaccine,
                'date': appointment_date,
                'location': location
            })
            print(f"Appointment for {selected_vaccine} scheduled for your kid {child_info['Name']} on {appointment_date.date()} at {location}.\n")

    def view_updates(self):
        user_id = self.select_child()
        if user_id:
            info = self.records[user_id]
            print(f"Child: {info['Name']}")
            print(f"DOB: {info['DOB']}")
            print("Appointments:")
            for appt in info['appointments']:
                print(f"  Vaccine: {appt['vaccine']}, Date: {appt['date'].date()}, Location: {appt['location']}")
            print("Growth Records:")
            for metric, value in info['growth'].items():
                print(f"  {metric}: {value}")
            print()

    def view_reminders(self):
        today = datetime.datetime.today()
        print("Upcoming Appointments:")
        for user_id, info in self.records.items():
            dob = info['DOB']
            age = self.calculate_age(dob)
            vaccines_due = self.get_vaccine_options(age)
            
            for appt in info['appointments']:
                due_date = appt['date']
                if today <= due_date <= today + datetime.timedelta(days=10):
                    print(f"Reminder: {info['Name']} (User ID: {user_id}) has an appointment for {appt['vaccine']} on {due_date.date()} at {appt['location']}.")
                    
            for vaccine, schedule in vaccines_due.items():
                for dose in schedule:
                    if "months" in dose:
                        months = int(dose.split()[0])
                        next_due_date = datetime.datetime.strptime(dob, "%Y-%m-%d") + datetime.timedelta(days=months*30)
                        if today <= next_due_date <= today + datetime.timedelta(days=10):
                            print(f"Reminder: {info['Name']} needs the {vaccine} vaccine on {next_due_date.date()}.")
        print()

    def add_growth_record(self):
        user_id = self.select_child()
        if user_id:
            height = input("Enter child's height (in cm): ")
            weight = input("Enter child's weight (in kg): ")
            self.records[user_id]['growth'] = {'Height': height, 'Weight': weight}
            print(f"Growth records for {self.records[user_id]['Name']} updated successfully!\n")

    def run(self):
        while True:
            print("Vaccination Management System")
            print("1. Add Child")
            print("2. Book Vaccination Appointment")
            print("3. View Updates")
            print("4. View Reminders")
            print("5. Add Growth Record")
            print("6. Exit")
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self.add_child()
            elif choice == '2':
                self.book_appointment()
            elif choice == '3':
                self.view_updates()
            elif choice == '4':
                self.view_reminders()
            elif choice == '5':
                self.add_growth_record()
            elif choice == '6':
                print("Exiting the system.")
                break
            else:
                print("Invalid choice! Please select a valid option.")

if __name__ == "__main__":
    system = VaccinationSystem()
    system.run()

