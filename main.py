"""Terminal user interface, menus, dashboard, and report views."""

import sys
import getpass
from datetime import datetime
from theme import ThemeManager
from auth import AuthManager
from models import EquipmentService, BorrowerService, BorrowService

class LabBorrowingApp:
    def __init__(self):
        self.current_user = None

    def print_table(self, headers, rows):
        t = ThemeManager.get()
        if not rows:
            print(f"{t['muted']}  No records found.{t['reset']}")
            return

        col_widths = [len(h) for h in headers]
        str_rows = []
        for row in rows:
            str_row = [str(item) if item is not None else "-" for item in row]
            str_rows.append(str_row)
            for i, val in enumerate(str_row):
                if len(val) > col_widths[i]:
                    col_widths[i] = len(val)

        header_str = " | ".join(headers[i].ljust(col_widths[i]) for i in range(len(headers)))
        sep_str = "-+-".join("-" * col_widths[i] for i in range(len(headers)))

        print(f"{t['secondary']}+{sep_str}+{t['reset']}")
        print(f"{t['accent']}| {header_str} |{t['reset']}")
        print(f"{t['secondary']}+{sep_str}+{t['reset']}")
        for row in str_rows:
            row_str = " | ".join(row[i].ljust(col_widths[i]) for i in range(len(row)))
            print(f"| {row_str} |")
        print(f"{t['secondary']}+{sep_str}+{t['reset']}")

    def pause(self):
        t = ThemeManager.get()
        input(f"\n{t['muted']}[Press ENTER to return...]{t['reset']}")

    def run(self):
        while True:
            if not self.current_user:
                self.login_menu()
            else:
                self.main_dashboard()

    def login_menu(self):
        ThemeManager.clear()
        ThemeManager.banner()
        t = ThemeManager.get()
        print(f"{t['primary']}╔══════════════════════════════════════════════════╗")
        print(f"║                   USER LOGIN                     ║")
        print(f"╚══════════════════════════════════════════════════╝{t['reset']}\n")

        print("1. Login with Credentials")
        print("2. Exit System")
        choice = input(f"\n{t['accent']}Enter Option: {t['reset']}").strip()

        if choice == "1":
            user = input("Username: ").strip()
            password = getpass.getpass("Password: ").strip()
            auth_user = AuthManager.authenticate(user, password)
            if auth_user:
                self.current_user = auth_user
            else:
                print(f"{t['error']}\n[!] Invalid username or password.{t['reset']}")
                self.pause()
        elif choice == "2":
            print(f"{t['primary']}\nExiting system. Goodbye!{t['reset']}")
            sys.exit(0)

    def main_dashboard(self):
        ThemeManager.clear()
        ThemeManager.banner()
        t = ThemeManager.get()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        stats = BorrowService.get_summary_stats()
        print(f"{t['primary']}╔══════════════════════════════════════════════════════════════════╗")
        print(f"║ User: {self.current_user['full_name']} ({self.current_user['role']}) | Date: {now} ")
        print(f"╠══════════════════════════════════════════════════════════════════╣")
        print(f"║ STATS: Catalog Items: {stats['unique_items']} | Active Loans: {stats['active_loans']} | Borrowers: {stats['borrowers']}")
        print(f"╚══════════════════════════════════════════════════════════════════╝{t['reset']}\n")

        print("1. Equipment Inventory Management (CRUD)")
        print("2. Borrower Records Management (CRUD)")
        print("3. Borrow & Return Transactions")
        print("4. Reports & Summary Analysis")
        print("5. System Settings & Customization")
        print("6. Logout")

        choice = input(f"\n{t['accent']}Select Module: {t['reset']}").strip()

        if choice == "1":
            self.equipment_menu()
        elif choice == "2":
            self.borrower_menu()
        elif choice == "3":
            self.transaction_menu()
        elif choice == "4":
            self.reports_menu()
        elif choice == "5":
            self.settings_menu()
        elif choice == "6":
            self.current_user = None

    # ----------------- EQUIPMENT CRUD -----------------
    def equipment_menu(self):
        while True:
            ThemeManager.clear()
            t = ThemeManager.get()
            print(f"{t['primary']}=== [ EQUIPMENT INVENTORY ] ==={t['reset']}\n")
            print("1. View All Equipment")
            print("2. Register New Equipment")
            print("3. Update Equipment Details")
            print("4. Delete Equipment Record")
            print("5. Search Equipment")
            print("6. Back to Dashboard")

            opt = input(f"\n{t['accent']}Select Option: {t['reset']}").strip()
            if opt == "1":
                items = EquipmentService.get_all()
                rows = [[i['id'], i['item_code'], i['item_name'], i['category'], i['total_qty'], i['available_qty'], i['condition_status']] for i in items]
                self.print_table(["ID", "Code", "Name", "Category", "Total", "Available", "Condition"], rows)
                self.pause()
            elif opt == "2":
                code = input("Item Code (e.g. EQ-LAB-01): ").strip()
                name = input("Item Name: ").strip()
                cat = input("Category: ").strip()
                try:
                    qty = int(input("Total Quantity: "))
                except ValueError:
                    print(f"{t['error']}[!] Invalid quantity.{t['reset']}")
                    self.pause()
                    continue
                cond = input("Condition (Good/Fair/Damaged): ").strip().capitalize()
                if cond not in ["Good", "Fair", "Damaged"]:
                    cond = "Good"

                res = EquipmentService.create(code, name, cat, qty, cond)
                print(f"{t['success']}Equipment registered successfully!{t['reset']}" if res else f"{t['error']}Failed to add item.{t['reset']}")
                self.pause()
            elif opt == "3":
                try:
                    eq_id = int(input("Enter Equipment ID to update: "))
                    eq = EquipmentService.get_by_id(eq_id)
                    if not eq:
                        print(f"{t['error']}Item not found.{t['reset']}")
                        self.pause()
                        continue
                    name = input(f"New Name [{eq['item_name']}]: ").strip() or eq['item_name']
                    cat = input(f"New Category [{eq['category']}]: ").strip() or eq['category']
                    t_qty = input(f"Total Qty [{eq['total_qty']}]: ").strip()
                    t_qty = int(t_qty) if t_qty else eq['total_qty']
                    a_qty = input(f"Available Qty [{eq['available_qty']}]: ").strip()
                    a_qty = int(a_qty) if a_qty else eq['available_qty']
                    cond = input(f"Condition [{eq['condition_status']}]: ").strip() or eq['condition_status']
                    
                    EquipmentService.update(eq_id, name, cat, t_qty, a_qty, cond)
                    print(f"{t['success']}Equipment updated!{t['reset']}")
                except ValueError:
                    print(f"{t['error']}Invalid numerical value.{t['reset']}")
                self.pause()
            elif opt == "4":
                if self.current_user['role'] != 'Administrator':
                    print(f"{t['error']}[!] Access Denied: Only Administrators can delete equipment.{t['reset']}")
                    self.pause()
                    continue
                try:
                    eq_id = int(input("Enter Equipment ID to delete: "))
                    confirm = input("Are you sure? (y/n): ").strip().lower()
                    if confirm == 'y':
                        EquipmentService.delete(eq_id)
                        print(f"{t['success']}Equipment record removed.{t['reset']}")
                except ValueError:
                    print(f"{t['error']}Invalid ID.{t['reset']}")
                self.pause()
            elif opt == "5":
                kw = input("Enter search term (name/code/category): ").strip()
                res = EquipmentService.search(kw)
                rows = [[i['id'], i['item_code'], i['item_name'], i['category'], i['available_qty'], i['condition_status']] for i in res]
                self.print_table(["ID", "Code", "Name", "Category", "Available", "Condition"], rows)
                self.pause()
            elif opt == "6":
                break

    # ----------------- BORROWER CRUD -----------------
    def borrower_menu(self):
        while True:
            ThemeManager.clear()
            t = ThemeManager.get()
            print(f"{t['primary']}=== [ BORROWER DIRECTORY ] ==={t['reset']}\n")
            print("1. View All Borrowers")
            print("2. Register New Borrower")
            print("3. Update Borrower Details")
            print("4. Delete Borrower")
            print("5. Search Borrower")
            print("6. Back to Dashboard")

            opt = input(f"\n{t['accent']}Select Option: {t['reset']}").strip()
            if opt == "1":
                items = BorrowerService.get_all()
                rows = [[b['id'], b['id_number'], b['full_name'], b['department'], b['contact_number']] for b in items]
                self.print_table(["ID", "ID Number", "Full Name", "Department", "Contact"], rows)
                self.pause()
            elif opt == "2":
                idn = input("Student/Faculty ID Number: ").strip()
                name = input("Full Name: ").strip()
                dept = input("Department: ").strip()
                contact = input("Contact Number: ").strip()
                res = BorrowerService.create(idn, name, dept, contact)
                print(f"{t['success']}Borrower registered!{t['reset']}" if res else f"{t['error']}Error adding borrower.{t['reset']}")
                self.pause()
            elif opt == "3":
                try:
                    b_id = int(input("Enter Borrower ID to update: "))
                    b = BorrowerService.get_by_id(b_id)
                    if not b:
                        print(f"{t['error']}Record not found.{t['reset']}")
                        self.pause()
                        continue
                    name = input(f"New Name [{b['full_name']}]: ").strip() or b['full_name']
                    dept = input(f"New Department [{b['department']}]: ").strip() or b['department']
                    cnt = input(f"New Contact [{b['contact_number']}]: ").strip() or b['contact_number']
                    BorrowerService.update(b_id, name, dept, cnt)
                    print(f"{t['success']}Borrower updated!{t['reset']}")
                except ValueError:
                    print(f"{t['error']}Invalid ID.{t['reset']}")
                self.pause()
            elif opt == "4":
                if self.current_user['role'] != 'Administrator':
                    print(f"{t['error']}[!] Access Denied: Admin role required.{t['reset']}")
                    self.pause()
                    continue
                try:
                    b_id = int(input("Enter Borrower ID to delete: "))
                    BorrowerService.delete(b_id)
                    print(f"{t['success']}Borrower record deleted.{t['reset']}")
                except ValueError:
                    print(f"{t['error']}Invalid ID.{t['reset']}")
                self.pause()
            elif opt == "5":
                kw = input("Enter keyword (Name/ID/Dept): ").strip()
                res = BorrowerService.search(kw)
                rows = [[b['id'], b['id_number'], b['full_name'], b['department']] for b in res]
                self.print_table(["ID", "ID Number", "Name", "Department"], rows)
                self.pause()
            elif opt == "6":
                break

    # ----------------- BORROW / RETURN TRANSACTIONS -----------------
    def transaction_menu(self):
        while True:
            ThemeManager.clear()
            t = ThemeManager.get()
            print(f"{t['primary']}=== [ BORROWING & RETURNS ] ==={t['reset']}\n")
            print("1. View All Loan Transactions")
            print("2. Issue Equipment (Borrow Item)")
            print("3. Return Equipment")
            print("4. Back to Dashboard")

            opt = input(f"\n{t['accent']}Select Option: {t['reset']}").strip()
            if opt == "1":
                records = BorrowService.get_all_records()
                rows = [[r['id'], r['borrower_name'], r['equipment_name'], r['quantity'], str(r['borrow_date'])[:10], str(r['expected_return_date']), r['status'], r['issued_by']] for r in records]
                self.print_table(["ID", "Borrower", "Equipment", "Qty", "Borrow Date", "Due Date", "Status", "Staff"], rows)
                self.pause()
            elif opt == "2":
                try:
                    b_id = int(input("Enter Borrower ID: "))
                    e_id = int(input("Enter Equipment ID: "))
                    qty = int(input("Quantity to borrow: "))
                    due = input("Expected Return Date (YYYY-MM-DD): ").strip()
                    rem = input("Remarks/Experiment: ").strip()

                    ok, msg = BorrowService.issue_item(b_id, e_id, qty, due, self.current_user["id"], rem)
                    print(f"{t['success']}{msg}{t['reset']}" if ok else f"{t['error']}{msg}{t['reset']}")
                except ValueError:
                    print(f"{t['error']}Invalid numeric values provided.{t['reset']}")
                self.pause()
            elif opt == "3":
                try:
                    rec_id = int(input("Enter Transaction Record ID to return: "))
                    ok, msg = BorrowService.return_item(rec_id)
                    print(f"{t['success']}{msg}{t['reset']}" if ok else f"{t['error']}{msg}{t['reset']}")
                except ValueError:
                    print(f"{t['error']}Invalid Record ID.{t['reset']}")
                self.pause()
            elif opt == "4":
                break

    # ----------------- REPORTS & SUMMARIES -----------------
    def reports_menu(self):
        while True:
            ThemeManager.clear()
            t = ThemeManager.get()
            print(f"{t['primary']}=== [ REPORTS & SYSTEM SUMMARIES ] ==={t['reset']}\n")
            print("1. Inventory Availability Summary")
            print("2. Currently Overdue & Active Loans")
            print("3. Equipment Condition Breakdown")
            print("4. Back to Dashboard")

            opt = input(f"\n{t['accent']}Select Report: {t['reset']}").strip()
            if opt == "1":
                items = EquipmentService.get_all()
                rows = [[i['item_code'], i['item_name'], i['category'], i['total_qty'], i['available_qty'], f"{round((i['available_qty']/i['total_qty'])*100, 1)}%"] for i in items if i['total_qty'] > 0]
                self.print_table(["Code", "Name", "Category", "Total Units", "In Stock", "Stock Rate"], rows)
                self.pause()
            elif opt == "2":
                records = BorrowService.get_all_records()
                active = [r for r in records if r['status'] == 'Borrowed']
                rows = [[r['id'], r['borrower_name'], r['equipment_name'], r['quantity'], str(r['expected_return_date']), "PENDING"] for r in active]
                self.print_table(["Rec ID", "Borrower", "Equipment", "Qty", "Due Date", "Status"], rows)
                self.pause()
            elif opt == "3":
                items = EquipmentService.get_all()
                breakdown = {}
                for i in items:
                    c = i['condition_status']
                    breakdown[c] = breakdown.get(c, 0) + i['total_qty']
                rows = [[cond, qty] for cond, qty in breakdown.items()]
                self.print_table(["Condition", "Total Equipment Units"], rows)
                self.pause()
            elif opt == "4":
                break

    # ----------------- SETTINGS & THEMES -----------------
    def settings_menu(self):
        while True:
            ThemeManager.clear()
            t = ThemeManager.get()
            print(f"{t['primary']}=== [ SYSTEM SETTINGS ] ==={t['reset']}\n")
            print("1. Switch Terminal Color Theme")
            print("2. Change Account Password")
            print("3. Back to Main Menu")

            opt = input(f"\n{t['accent']}Select Option: {t['reset']}").strip()
            if opt == "1":
                print("\nAvailable Themes:")
                for k, v in ThemeManager.THEMES.items():
                    print(f"  [{k}] {v['name']}")
                chosen = input("Choose Theme (1-3): ").strip()
                if ThemeManager.set_theme(chosen):
                    print(f"\nTheme changed to {ThemeManager.get()['name']}.")
                else:
                    print(f"{t['error']}Invalid selection.{t['reset']}")
                self.pause()
            elif opt == "2":
                old_p = getpass.getpass("Current Password: ").strip()
                new_p = getpass.getpass("New Password: ").strip()
                confirm = getpass.getpass("Confirm New Password: ").strip()
                if new_p != confirm:
                    print(f"{t['error']}Passwords do not match.{t['reset']}")
                else:
                    ok, msg = AuthManager.update_password(self.current_user["id"], old_p, new_p)
                    print(f"{t['success']}{msg}{t['reset']}" if ok else f"{t['error']}{msg}{t['reset']}")
                self.pause()
            elif opt == "3":
                break

if __name__ == "__main__":
    app = LabBorrowingApp()
    app.run()
