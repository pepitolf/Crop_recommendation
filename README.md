# Crop_recommendation

This project is a Crop Recommendation System developed using Django. The application aims to recommend crops to farmers based on various knowledge inputs provided by the farmers.

## Features

- **User Registration and Authentication**: Users can register as farmers or admins. Admins need to provide a security key during registration.
- **Profile Management**: Users can view and update their profiles.
- **Crop Management**: Admins can add, update, and delete crops.
- **Knowledge Management**: Admins can add, update, and delete knowledge.
- **Knowledge Rule Management**: Admins can create rules that link knowledge to crops.
- **Knowledge Fuzzy Value Management**: Admins can define fuzzy values for knowledge-crop pairs.
- **Crop Recommendation**: Farmers can input knowledge values to get crop recommendations.

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/pepitolf/Crop_recommendation.git
    cd Crop_recommendation
    ```

2. **Create and activate a virtual environment**:

    ```bash
    python -m venv env
    source env/bin/activate   # On Windows use `env\Scripts\activate`
    ```

3. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the environment variables**:
    Create a `.env` file in the root directory and add the following variables:

    ```env
    SECRET_KEY='your-secret-key'
    ```

5. **Run the migrations**:

    ```bash
    python manage.py migrate
    ```

6. **Create a superuser**:

    ```bash
    python manage.py createsuperuser
    ```

7. **Start the development server**:

    ```bash
    python manage.py runserver
    ```

## Usage

### Admin Dashboard

1. **Login as an admin**:
    Use the superuser credentials created during installation to log in.

2. **Manage Crops**:
    Navigate to the Crops section to add, update, or delete crops.

3. **Manage Knowledge**:
    Navigate to the Knowledge section to add, update, or delete knowledge entries.

4. **Manage Knowledge Rules**:
    Navigate to the Knowledge Rules section to create rules linking knowledge to crops.

5. **Manage Knowledge Fuzzy Values**:
    Navigate to the Knowledge Fuzzy Values section to define fuzzy values for knowledge-crop pairs.

### Farmer

1. **Register as a farmer**:
    Go to the registration page and choose 'Farmer' as the user type.

2. **Login as a farmer**:
    Use the credentials created during registration to log in.

3. **Get Crop Recommendations**:
    Navigate to the Crop Recommendation page.
    Input the required knowledge values and submit to get crop recommendations.

## Project Structure

- `recommendation/`: Contains the main application code.
- `templates/recommendation/`: Contains HTML templates.
- `static/recommendation/`: Contains static files such as CSS and JavaScript.
- `models.py`: Contains the database models.
- `views.py`: Contains the view functions.
- `forms.py`: Contains the forms used in the application.
- `urls.py`: Contains the URL routing.
