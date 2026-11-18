"""OOP Domain Models and CRUD Operations for Tables."""

from database import Database

class EquipmentService:
    @staticmethod
    def get_all():
        return Database.execute_query("SELECT * FROM equipment ORDER BY id ASC")

    @staticmethod
    def get_by_id(eq_id):
        return Database.execute_single("SELECT * FROM equipment WHERE id = %s", (eq_id,))

    @staticmethod
    def create(item_code, name, category, qty, condition):
        query = """
            INSERT INTO equipment (item_code, item_name, category, total_qty, available_qty, condition_status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return Database.execute_query(query, (item_code, name, category, qty, qty, condition), commit=True)

    @staticmethod
    def update(eq_id, name, category, total_qty, available_qty, condition):
        query = """
            UPDATE equipment
            SET item_name = %s, category = %s, total_qty = %s, available_qty = %s, condition_status = %s
            WHERE id = %s
        """
        return Database.execute_query(query, (name, category, total_qty, available_qty, condition, eq_id), commit=True)

    @staticmethod
    def delete(eq_id):
        return Database.execute_query("DELETE FROM equipment WHERE id = %s", (eq_id,), commit=True)

    @staticmethod
    def search(keyword):
        q = f"%{keyword}%"
        query = """
            SELECT * FROM equipment
            WHERE item_code LIKE %s OR item_name LIKE %s OR category LIKE %s
        """
        return Database.execute_query(query, (q, q, q))


class BorrowerService:
    @staticmethod
    def get_all():
        return Database.execute_query("SELECT * FROM borrowers ORDER BY id ASC")

    @staticmethod
    def get_by_id(b_id):
        return Database.execute_single("SELECT * FROM borrowers WHERE id = %s", (b_id,))

    @staticmethod
    def create(id_number, full_name, department, contact):
        query = """
            INSERT INTO borrowers (id_number, full_name, department, contact_number)
            VALUES (%s, %s, %s, %s)
        """
        return Database.execute_query(query, (id_number, full_name, department, contact), commit=True)

    @staticmethod
    def update(b_id, full_name, department, contact):
        query = """
            UPDATE borrowers
            SET full_name = %s, department = %s, contact_number = %s
            WHERE id = %s
        """
        return Database.execute_query(query, (full_name, department, contact, b_id), commit=True)

    @staticmethod
    def delete(b_id):
        return Database.execute_query("DELETE FROM borrowers WHERE id = %s", (b_id,), commit=True)

    @staticmethod
    def search(keyword):
        q = f"%{keyword}%"
        query = """
            SELECT * FROM borrowers
            WHERE id_number LIKE %s OR full_name LIKE %s OR department LIKE %s
        """
        return Database.execute_query(query, (q, q, q))


class BorrowService:
    @staticmethod
    def get_all_records():
        query = """
            SELECT br.id, b.full_name AS borrower_name, e.item_name AS equipment_name,
                   br.quantity, br.borrow_date, br.expected_return_date, br.status, u.username AS issued_by
            FROM borrow_records br
            JOIN borrowers b ON br.borrower_id = b.id
            JOIN equipment e ON br.equipment_id = e.id
            JOIN users u ON br.issued_by_user_id = u.id
            ORDER BY br.id DESC
        """
        return Database.execute_query(query)

    @staticmethod
    def issue_item(borrower_id, equipment_id, quantity, return_date, user_id, remarks):
        # Check stock availability
        eq = EquipmentService.get_by_id(equipment_id)
        if not eq or eq["available_qty"] < quantity:
            return False, "Insufficient equipment quantity available."

        insert_query = """
            INSERT INTO borrow_records (borrower_id, equipment_id, quantity, expected_return_date, issued_by_user_id, remarks)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        res = Database.execute_query(insert_query, (borrower_id, equipment_id, quantity, return_date, user_id, remarks), commit=True)
        if res:
            # Deduct available count
            Database.execute_query(
                "UPDATE equipment SET available_qty = available_qty - %s WHERE id = %s",
                (quantity, equipment_id),
                commit=True
            )
            return True, "Item issued successfully."
        return False, "Failed to record transaction."

    @staticmethod
    def return_item(record_id):
        rec = Database.execute_single("SELECT * FROM borrow_records WHERE id = %s AND status = 'Borrowed'", (record_id,))
        if not rec:
            return False, "Active borrow record not found."

        # Mark as returned
        update_rec = "UPDATE borrow_records SET status = 'Returned', actual_return_date = NOW() WHERE id = %s"
        Database.execute_query(update_rec, (record_id,), commit=True)

        # Restore inventory
        Database.execute_query(
            "UPDATE equipment SET available_qty = available_qty + %s WHERE id = %s",
            (rec["quantity"], rec["equipment_id"]),
            commit=True
        )
        return True, "Equipment returned and inventory restored."

    @staticmethod
    def get_summary_stats():
        total_items = Database.execute_single("SELECT COUNT(*) as count, IFNULL(SUM(total_qty), 0) as units FROM equipment")
        borrowed = Database.execute_single("SELECT COUNT(*) as count FROM borrow_records WHERE status = 'Borrowed'")
        registered_borrowers = Database.execute_single("SELECT COUNT(*) as count FROM borrowers")
        return {
            "unique_items": total_items["count"],
            "total_units": total_items["units"],
            "active_loans": borrowed["count"],
            "borrowers": registered_borrowers["count"]
        }
