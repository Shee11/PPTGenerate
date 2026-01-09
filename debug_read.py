
import os
try:
    with open("content step response.xml", "r") as f:
        data = f.read()
    print(f"File size: {len(data)}")
except Exception as e:
    print(f"Error: {e}")
