"""Flask web app for the Blockchain Attendance Management System.

This is the frontend+backend integration requested.

Runs with standard-library only *for the blockchain logic*.
Flask is an external dependency and is declared in requirements.txt.
"""

from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any, Dict, List

from flask import Flask, jsonify, render_template, request

# Import blockchain logic
from attendance_blockchain import AttendanceBlockchain


app = Flask(__name__)

# Single in-memory blockchain instance for this server run.
blockchain = AttendanceBlockchain()


@app.get("/")
def index() -> str:
    return render_template("index.html")


@app.post("/api/attendance")
def api_mark_attendance() -> Any:
    data = request.get_json(silent=True) or {}

    student_id = str(data.get("student_id", "")).strip()
    name = str(data.get("name", "")).strip()
    course = str(data.get("course", "")).strip()

    status_raw = str(data.get("status", "")).strip().lower()
    if status_raw in {"present", "p"}:
        status = "Present"
    elif status_raw in {"absent", "a"}:
        status = "Absent"
    else:
        return jsonify({"error": "status must be Present/Absent"}), 400

    if not student_id or not name or not course:
        return jsonify({"error": "student_id, name, course are required"}), 400

    block = blockchain.add_attendance(
        student_id=student_id,
        name=name,
        course=course,
        status=status,
    )

    return jsonify({"message": "Recorded", "block": block.to_dict()})


@app.get("/api/attendance")
def api_get_attendance() -> Any:
    return jsonify({"records": blockchain.get_attendance_records()})


@app.get("/api/verify")
def api_verify() -> Any:
    return jsonify({"valid": blockchain.is_chain_valid()})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    # For development only
    app.run(host="0.0.0.0", port=port, debug=True)

