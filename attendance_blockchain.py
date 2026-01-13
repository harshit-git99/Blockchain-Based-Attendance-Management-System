import hashlib
import json
import time

# ---------------- BLOCK ----------------
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()


# ---------------- BLOCKCHAIN ----------------
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.ctime(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        prev_block = self.get_latest_block()
        new_block = Block(
            len(self.chain),
            time.ctime(),
            data,
            prev_block.hash
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

        return True

    def display_chain(self):
        for block in self.chain:
            print("=" * 50)
            print(f"Index: {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.data}")
            print(f"Hash: {block.hash}")
            print(f"Previous Hash: {block.previous_hash}")
        print("=" * 50)


# ---------------- ATTENDANCE SYSTEM ----------------
class AttendanceSystem:
    def __init__(self):
        self.blockchain = Blockchain()

    def mark_attendance(self):
        name = input("Enter student name: ")
        roll = input("Enter roll number: ")
        subject = input("Enter subject: ")

        record = {
            "name": name,
            "roll": roll,
            "subject": subject,
            "status": "Present"
        }

        self.blockchain.add_block(record)
        print("\n✅ Attendance recorded successfully!\n")

    def view_attendance(self):
        self.blockchain.display_chain()

    def verify_blockchain(self):
        if self.blockchain.is_chain_valid():
            print("\n✅ Blockchain is VALID\n")
        else:
            print("\n❌ Blockchain has been TAMPERED\n")

    def menu(self):
        while True:
            print("\n===== Blockchain Attendance System =====")
            print("1. Mark Attendance")
            print("2. View Attendance Records")
            print("3. Verify Blockchain")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.mark_attendance()
            elif choice == "2":
                self.view_attendance()
            elif choice == "3":
                self.verify_blockchain()
            elif choice == "4":
                print("Exiting system...")
                break
            else:
                print("Invalid choice! Try again.")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    system = AttendanceSystem()
    system.menu()
