#!/bin/bash

CSV_FILE="routes.csv"

if [ ! -f "$CSV_FILE" ]; then
  echo "CSV file $CSV_FILE not found!"
  exit 1
fi

echo "Importing routes from $CSV_FILE..."

# Python script to read CSV and create TravelOption entries
python3 << END
import csv
from datetime import datetime
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')  # replace 'your_project' with your Django project name
django.setup()

from booking.models import TravelOption

with open("$CSV_FILE", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    count = 0
    for row in reader:
        try:
            dt = datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M')
            obj, created = TravelOption.objects.get_or_create(
                type=row['type'],
                source=row['source'],
                destination=row['destination'],
                datetime=dt,
                price=int(row['price']),
                available_seats=int(row['available_seats'])
            )
            if created:
                count += 1
        except Exception as e:
            print(f"Failed to import row {row}: {e}")

print(f"Imported {count} new travel routes.")
END
