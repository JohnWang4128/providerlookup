# Provider Lookup Application

A web application that allows users to search for and locate healthcare providers in the United States based on the National Plan and Provider Enumeration System (NPPES) database.

## Overview

Provider Lookup is a Flask-based web application that provides an intuitive interface for searching healthcare provider information. The application imports and processes data from the official NPPES NPI Registry, making it accessible through a user-friendly search interface.

## Features

- **Provider Search**: Find providers by name, NPI number, or location
- **Filtering Options**: Filter results by state and city
- **Detailed Provider Profiles**: View comprehensive information about each provider
- **Location Visualization**: See provider locations on an integrated map (with Google Maps API)
- **Responsive Design**: Works on both desktop and mobile devices
- **RESTful API**: Programmatic access to provider data

## Data Sources

The application uses data from:
- [NPPES NPI Files](https://download.cms.gov/nppes/NPI_Files.html)
- [Provider Taxonomy Codes](https://www.nucc.org/index.php/code-sets-mainmenu-41/provider-taxonomy-mainmenu-40/csv-mainmenu-57)

## Setup Instructions

### Automated Setup

For convenience, automated setup scripts are provided for both Windows and Unix-based systems:

#### Linux/Mac:
```bash
chmod +x setup.sh
./setup.sh
```

#### Windows:
```
setup.bat
```

These scripts will:
1. Create a virtual environment
2. Install all required dependencies
3. Set up the database
4. Import provider data (if available)
5. Start the application

### Manual Setup

If you prefer manual setup:

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Linux/Mac
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   - Copy `.env.example` to `.env` (or create it with appropriate settings)
   - Add a Google Maps API key if you want map functionality

4. **Initialize database**:
   ```bash
   python run.py
   ```

5. **Import data**:
   ```bash
   python scripts/import_data.py data/your_npi_data_file.csv
   ```

## Using the Application

Once the application is running, you can access it at http://localhost:5000

### Homepage
- The homepage presents a search form where you can enter provider details
- You can search by name, NPI number, state, or city

### Search Process
1. Enter your search criteria in the form
2. Click the "Search" button
3. Browse through paginated results of matching providers
4. Click on any provider to view their detailed information

### Provider Details
- The details page displays comprehensive information about the selected provider
- Information includes contact details, address, and endpoint information
- If Google Maps integration is enabled, you'll see the provider's location on a map

### Advanced Filtering
- On the search results page, you can further refine your search
- Filter by state, city, or additional search terms
- Results update dynamically based on your filter criteria

## API Endpoints

The application provides the following API endpoints:

- `GET /api/providers?query=SEARCH_TERM&state=STATE&city=CITY&limit=LIMIT`
  Returns a list of providers matching the search criteria

- `GET /api/states`
  Returns a list of all states with registered providers

## Project Structure

```
provider_lookup/
│
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── requirements.txt          # Project dependencies
├── run.py                    # Script to run the application
│
├── data/                     # Directory for data files
│
├── scripts/
│   └── import_data.py        # Script to import CSV data into database
│
├── static/                   # Static files (CSS, JS, images)
│
├── templates/                # HTML templates
│
└── models/                   # Database models
```

