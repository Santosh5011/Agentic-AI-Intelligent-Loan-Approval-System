#!/bin/bash

# Install dependencies if needed
pip install -r requirements.txt

# Start FastAPI backend server in the background
echo "Starting FastAPI gateway gateway layer..."
python -m api.main &
API_PID=$!

# Give the API engine a second to boot up fully
sleep 2

# Start Streamlit Presentation UI Layer
echo "Spinning up presentation panel view..."
streamlit run ui/app.py

# Terminate process loops when closing out script execution instance
kill $API_PID