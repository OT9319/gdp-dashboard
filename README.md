# :earth_americas: GDP dashboard template

A simple Streamlit app showing the GDP of different countries in the world.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gdp-dashboard-template.streamlit.app/)

## Project Structure

This repository contains:
- **Streamlit GDP Dashboard**: A web app for visualizing GDP data
- **Constitutional API Configuration**: Poetry-based setup for a FastAPI constitutional API system

### How to run the Streamlit app

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```

### Development with Poetry (Constitutional API)

This project also includes a `pyproject.toml` configuration for Poetry-based dependency management, designed for developing a FastAPI constitutional API system.

1. Install Poetry (if not already installed)

   ```
   $ curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install dependencies with Poetry

   ```
   $ poetry install
   ```

3. Activate the virtual environment

   ```
   $ poetry shell
   ```
