"""Blockchain-based Attendance Management System (Console)

Pure Python (standard library only).

Features:
- Mark Attendance (creates a new block)
- View Attendance Records
- Verify Blockchain Integrity

Note: Data is stored in-memory for this run.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, asdict
from typing import Any, Dict, List


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class AttendanceData:
    student_id: str
    name: str
    course: str
    status: str  # Present/Absent


class Block:
    def __init__(
        self,
        index: int,
        timestamp: float,
        attendance: AttendanceData,
        previous_hash: str,
    ) -> None:
        self.index = index
        self.timestamp = timestamp
        self.attendance = attendance
        self.previous_hash = previous_hash
        self.current_hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        payload = {
            "index": self.index,
            "timestamp": self.timestamp,
            "attendance": asdict(self.attendance),
            "previous_hash": self.previous_hash,
        }
        return _sha256(json.dumps(payload, sort_keys=True))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "attendance": asdict(self.attendance),
            "previous_hash": self.previous_hash,
            "current_hash": self.current_hash,
        }


class AttendanceBlockchain:
    def __init__(self) -> None:
        self.chain: List[Block] = []
        self._create_genesis_block()

    def _create_genesis_block(self) -> None:
        genesis_attendance = AttendanceData(
            student_id="0",
            name="GENESIS",
            course="N/A",
            status="N/A",
        )
        genesis = Block(
            index=0,
            timestamp=time.time(),
            attendance=genesis_attendance,
            previous_hash="0",
        )
        self.chain.append(genesis)

    @property
    def latest_block(self) -> Block:
        return self.chain[-1]

    def add_attendance(
        self,
        student_id: str,
        name: str,
        course: str,
        status: str,
    ) -> Block:
        attendance = AttendanceData(
            student_id=student_id,
            name=name,
            course=course,
            status=status,
        )
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            attendance=attendance,
            previous_hash=self.latest_block.current_hash,
        )
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            # linkage check
            if curr.previous_hash != prev.current_hash:
                return False

            # hash check
            if curr.current_hash != curr.calculate_hash():
                return False

        return True

    def get_attendance_records(self) -> List[Dict[str, Any]]:
        # Skip genesis block
        return [b.to_dict() for b in self.chain[1:]]


def _fmt_ts(ts: float) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


def _prompt_non_empty(label: str) -> str:
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print("Value cannot be empty. Please try again.")


def _prompt_status() -> str:
    while True:
        value = input("Status (Present/Absent): ").strip().lower()
        if value in {"present", "p"}:
            return "Present"
        if value in {"absent", "a"}:
            return "Absent"
        print("Invalid status. Enter 'Present' or 'Absent'.")


def main() -> None:
    blockchain = AttendanceBlockchain()

    while True:
        print("\n=== Blockchain Attendance Management System ===")
        print("1. Mark Attendance")
        print("2. View Attendance Records")
        print("3. Verify Blockchain")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            print("\n--- Mark Attendance ---")
            student_id = _prompt_non_empty("Student ID")
            name = _prompt_non_empty("Student Name")
            course = _prompt_non_empty("Course")
            status = _prompt_status()

            block = blockchain.add_attendance(
                student_id=student_id,
                name=name,
                course=course,
                status=status,
            )

            print("\nAttendance recorded successfully!")
            print(f"Block Index: {block.index}")
            print(f"Timestamp: {_fmt_ts(block.timestamp)}")
            print(f"Current Hash: {block.current_hash}")

        elif choice == "2":
            print("\n--- Attendance Records ---")
            records = blockchain.get_attendance_records()
            if not records:
                print("No attendance records yet.")
                continue

            for rec in records:
                attendance = rec["attendance"]
                print("\n" + "-" * 40)
                print(f"Index: {rec['index']}")
                print(f"Time: {_fmt_ts(rec['timestamp'])}")
                print(f"Student ID: {attendance['student_id']}")
                print(f"Name: {attendance['name']}")
                print(f"Course: {attendance['course']}")
                print(f"Status: {attendance['status']}")
                print(f"Prev Hash: {rec['previous_hash']}")
                print(f"Current Hash: {rec['current_hash']}")
                print("-" * 40)

        elif choice == "3":
            print("\n--- Verify Blockchain ---")
            if blockchain.is_chain_valid():
                print("Blockchain is VALID. No tampering detected.")
            else:
                print("Blockchain is INVALID! Integrity check failed.")

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()

