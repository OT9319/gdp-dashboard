#!/bin/bash
# Startup script to run both Streamlit app and FastAPI

echo "Starting Constitutional Architecture System - CEREBRUM-1"
echo "==========================================================="

# Check if we're in the right directory
if [[ ! -f "streamlit_app.py" ]]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Install dependencies if needed
echo "Installing dependencies..."
pip install -r requirements.txt

# Set environment variables
export JWT_SECRET_KEY="${JWT_SECRET_KEY:-constitutional-architecture-secret-key-change-in-production}"

# Start API in background
echo "Starting Constitutional Architecture API on port 8000..."
python -m api.main &
API_PID=$!

# Wait for API to start
sleep 3

# Test API connectivity
echo "Testing API connectivity..."
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ API is running successfully"
else
    echo "❌ API failed to start"
    kill $API_PID 2>/dev/null
    exit 1
fi

# Start Streamlit app
echo "Starting GDP Dashboard on port 8501..."
streamlit run streamlit_app.py --server.port 8501 &
STREAMLIT_PID=$!

# Wait for Streamlit to start
sleep 5

echo ""
echo "🚀 System is ready!"
echo "📊 GDP Dashboard: http://localhost:8501"
echo "🔗 API Endpoints: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for user to stop
wait $API_PID $STREAMLIT_PID