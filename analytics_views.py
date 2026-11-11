import csv
from collections import Counter, defaultdict
from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render

from .models import Room, Student


@login_required
def analytics_dashboard(request):
    """
    Build the main analytics from the live Hostel Management System database.
    The optional sensor CSV is shown separately as sample/demo data only.
    """
    rooms = list(Room.objects.annotate(student_count=Count("student")).order_by("room_number"))
    total_rooms = len(rooms)
    total_students = Student.objects.count()
    total_capacity = sum(max(room.capacity, 0) for room in rooms)
    occupied_beds = sum(room.student_count for room in rooms)
    available_beds = max(total_capacity - occupied_beds, 0)
    occupancy_rate = round((occupied_beds / total_capacity) * 100, 1) if total_capacity else 0

    occupied_rooms = sum(1 for room in rooms if room.student_count > 0)
    vacant_rooms = total_rooms - occupied_rooms
    full_rooms = sum(
        1 for room in rooms
        if room.capacity > 0 and room.student_count >= room.capacity
    )

    # Numerical distribution: each room's utilisation percentage.
    utilisation_bins = {
        "0%": 0,
        "1–25%": 0,
        "26–50%": 0,
        "51–75%": 0,
        "76–100%": 0,
        ">100%": 0,
    }
    scatter_points = []
    for room in rooms:
        capacity = max(room.capacity, 0)
        count = room.student_count
        utilisation = (count / capacity * 100) if capacity else (100 if count else 0)

        if utilisation == 0:
            bucket = "0%"
        elif utilisation <= 25:
            bucket = "1–25%"
        elif utilisation <= 50:
            bucket = "26–50%"
        elif utilisation <= 75:
            bucket = "51–75%"
        elif utilisation <= 100:
            bucket = "76–100%"
        else:
            bucket = ">100%"
        utilisation_bins[bucket] += 1

        scatter_points.append({
            "x": count,
            "y": capacity,
            "room": str(room.room_number),
            "utilisation": round(utilisation, 1),
        })

    # Categorical distribution: room status and student allocation by room.
    room_status_labels = ["Vacant", "Partially occupied", "Full", "Over capacity"]
    room_status_counts = [0, 0, 0, 0]
    for room in rooms:
        if room.student_count == 0:
            room_status_counts[0] += 1
        elif room.capacity > 0 and room.student_count < room.capacity:
            room_status_counts[1] += 1
        elif room.student_count == room.capacity:
            room_status_counts[2] += 1
        else:
            room_status_counts[3] += 1

    assigned_by_room = [
        {"room": str(room.room_number), "students": room.student_count}
        for room in rooms if room.student_count > 0
    ]

    most_occupied = max(rooms, key=lambda room: room.student_count, default=None)
    if total_rooms:
        insight = (
            f"{occupied_rooms} of {total_rooms} rooms currently have at least one student; "
            f"{vacant_rooms} rooms are vacant. Overall bed utilisation is {occupancy_rate}% "
            f"({occupied_beds} of {total_capacity} beds)."
        )
    else:
        insight = "No rooms have been added yet. Add rooms and student assignments to populate these charts."

    chart_data = {
        "utilisation_labels": list(utilisation_bins.keys()),
        "utilisation_counts": list(utilisation_bins.values()),
        "room_status_labels": room_status_labels,
        "room_status_counts": room_status_counts,
        "allocation_labels": [item["room"] for item in assigned_by_room],
        "allocation_counts": [item["students"] for item in assigned_by_room],
        "scatter_points": scatter_points,
    }

    # Keep the supplied sensor dataset as a clearly separate demonstration section.
    sensor_data = None
    csv_path = Path(settings.BASE_DIR) / "data" / "Occupancy_Estimation.csv"
    if csv_path.exists():
        counts = Counter()
        hourly = defaultdict(lambda: {"temp": [], "co2": []})
        temps, co2s = [], []
        total_rows = 0
        try:
            with csv_path.open("r", newline="", encoding="utf-8-sig") as file:
                for row in csv.DictReader(file):
                    total_rows += 1
                    try:
                        counts[int(float(row.get("Room_Occupancy_Count", 0)))] += 1
                    except (TypeError, ValueError):
                        pass
                    hour = (row.get("Time") or "")[:2]
                    try:
                        value = float(row.get("S1_Temp", ""))
                        temps.append(value)
                        hourly[hour]["temp"].append(value)
                    except (TypeError, ValueError):
                        pass
                    try:
                        value = float(row.get("S5_CO2", ""))
                        co2s.append(value)
                        hourly[hour]["co2"].append(value)
                    except (TypeError, ValueError):
                        pass

            hours = sorted(hour for hour in hourly if hour.isdigit())
            average = lambda values: round(sum(values) / len(values), 2) if values else None
            sensor_data = {
                "total_rows": total_rows,
                "avg_temp": average(temps) or 0,
                "avg_co2": average(co2s) or 0,
                "hours": [hour + ":00" for hour in hours],
                "temperature": [average(hourly[hour]["temp"]) for hour in hours],
                "co2": [average(hourly[hour]["co2"]) for hour in hours],
                "occupancy_labels": ["0 people", "1 person", "2 people", "3 people"],
                "occupancy_counts": [counts.get(index, 0) for index in range(4)],
            }
        except (OSError, csv.Error):
            sensor_data = None

    return render(request, "analytics.html", {
        "total_rooms": total_rooms,
        "total_students": total_students,
        "total_capacity": total_capacity,
        "occupied_beds": occupied_beds,
        "available_beds": available_beds,
        "occupancy_rate": occupancy_rate,
        "occupied_rooms": occupied_rooms,
        "vacant_rooms": vacant_rooms,
        "full_rooms": full_rooms,
        "insight": insight,
        "chart_data": chart_data,
        "sensor_data": sensor_data,
    })
