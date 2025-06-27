#!/bin/bash
# Setup script for Provider Lookup application (Linux/Mac)
# This script:
# 1. Creates a virtual environment
# 2. Installs all required dependencies
# 3. Imports data from the CSV file
# 4. Runs the Flask application

# Exit on any error
set -e

echo "==== Provider Lookup Setup Script (Linux/Mac) ===="
echo "Setting up the application..."

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if virtual environment module is available
python3 -c "import venv" &>/dev/null || {
    echo "The 'venv' module is not available. Please install it and try again."
    exit 1
}

# Check for data file
DATA_FILE="data/endpoint_pfile_20250407-20250413.csv"
if [ ! -f "$DATA_FILE" ]; then
    echo "Data file not found: $DATA_FILE"
    echo "Please download the NPI data file and place it in the data directory."
    echo "You can download it from: https://download.cms.gov/nppes/NPI_Files.html"
    
    # Ask if user wants to continue without data import
    read -p "Continue without importing data? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup aborted."
        exit 1
    fi
    SKIP_IMPORT=true
else
    SKIP_IMPORT=false
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install werkzeug==2.0.3
pip install flask==2.0.1
pip install sqlalchemy==1.4.46
pip install flask-sqlalchemy==2.5.1
pip install flask-migrate==3.1.0
pip install python-dotenv==0.19.0
pip install numpy==1.21.6 
pip install pandas==1.3.5
pip install gunicorn==20.1.0
pip install pymysql==1.0.2

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env 2>/dev/null || {
        echo "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(16))')" > .env
        echo "FLASK_APP=run.py" >> .env
        echo "FLASK_ENV=development" >> .env
        echo "DATABASE_URL=sqlite:///provider_lookup.db" >> .env
        echo "# GOOGLE_MAPS_API_KEY=your-api-key-here" >> .env
    }
fi

# Create database tables
echo "Initializing database..."
python run.py &
PID=$!
sleep 3
kill $PID

# Import data if available
if [ "$SKIP_IMPORT" = false ]; then
    echo "Importing data (this may take some time)..."
    python scripts/import_data.py "$DATA_FILE"
fi

echo "Setup complete!"
echo ""
echo "To run the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Start the server: python run.py"
echo ""
echo "Starting the application now..."
python run.py