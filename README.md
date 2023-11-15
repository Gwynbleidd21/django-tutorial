# Extended Django Polls Application

This project is an extension of the official Django tutorial project, incorporating additional functionalities into the basic polls app.

## Getting Started

These instructions will get your copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3
- pip (Python package manager)

### Setting Up the Development Environment

1. **Clone the Repository**
   
   ```bash
   git clone [URL to your repository]
   cd mysite
   ```
2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   ```
    Activate the virtual environment:

    * On Windows: ``` venv\Scripts\activate```
    * On Unix or MacOS: ``` source venv/bin/activate```

3. **Install Required Packages**
    
    ```bash
   pip install -r requirements.txt
    ```

4. **Setting Up the Database**
    
    Run the following command to populate your database:
    ```bash
   python manage.py generate_data
    ```
   
### Running the Application
    
```bash
   python manage.py runserver
   ```
   
Visit http://localhost:8000/polls in your browser to view the application.

## Application Structure

    IndexView: Lists the latest 25 questions in the poll.
    DetailView: Shows specific details of a selected question.
    ResultsView: Displays the results for a specific poll.
    vote: Handles the voting action for a question.
    poll_results_api: API view that returns the results of a poll in JSON format.