# AI Impact Visualization

## Prerequisites

- **Poetry**: Install via [official instructions](https://python-poetry.org/docs/).  
- **Docker**: If you plan to use containers.  
- **Python**: (3.9+ recommended)  

---

## Local Development (Without Docker)

1. **Install dependencies** with Poetry:
   ```bash
   poetry install
   ```
   
2. **Activate your virtual environment**:
   ```bash
   poetry shell
   ```
   
3. **Start the FastAPI server**:
   ```bash
   python app/main.py
   ```

---

## Local Development (With Docker Compose)

1. Build and run the containers:
   ```bash
   docker-compose up --build
   ```

---

## Environment Variables

1. **Create a `.env` file** in the root directory.

2. **Add the environment variables from .env.sample**:

---

## CLI

CLI tool provides a set of commands to add data from CSV files to the database: add-engineers, add-teams, add-projects,
add-repositories, add-issues, add-commits. The order is important, as the data is related to each other. Please follow
the order mentioned above. You can use command add-all to add all data at once in the correct order.

## Testing

1. **Run tests** with Poetry:
   ```bash
   pytest
   ```
2. **Run tests** inside Docker:
   ```bash
   docker-compose exec ai-impact-visualization-app pytest
   ```

## API Documentation

1. **Swagger UI**: http://[host]:[port]/docs
2. **Redoc**: http://[host]:[port]/redoc
