
# Dairy Project Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Directory Structure](#directory-structure)
3. [Project Setup](#project-setup)
    - [Cloning the Repository](#cloning-the-repository)
    - [Setting Up Virtual Environment](#setting-up-virtual-environment)
    - [Installing Dependencies](#installing-dependencies)
    - [Environment Variables Setup](#environment-variables-setup)
4. [Application Components](#application-components)
    - [Main Application](#main-application)
    - [Controllers](#controllers)
    - [Models](#models)
    - [Views](#views)
5. [Running the Application](#running-the-application)
6. [Configuration](#configuration)

---

## Introduction

The Dairy Project is a Flask-based web application that provides a platform for managing dairy operations. The project follows a modular structure, making use of blueprints for different roles such as `admin`, `dairyOwner`, and `farmer`. Each blueprint manages its own views and business logic.

---

## Directory Structure

The project is organized as follows:

```bash
│   .gitignore
│   README.md
│   run.py
│
└───app
    │   __init__.py
    │
    ├───controllers
    │   │   __init__.py
    │   │
    │   ├───admin
    │   │       __init__.py
    │   │
    │   ├───dairyOwner
    │   │       __init__.py
    │   │
    │   └───farmer
    │           __init__.py
    │
    ├───models
    │       __init__.py
    │
    └───views
        ├───admin
        ├───dairyOwner
        └───farmer
```

---

 
## NOTE
### Create Separate folders for each controller and view to avoid confusion and update it in this documentation


## Project Setup

### Cloning the Repository

To start, clone the repository by running the following command:

```bash
git clone <repository-url>
cd Dairy_project
```

### Setting Up Virtual Environment

To create a virtual environment, run:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### Installing Dependencies

After activating the virtual environment, install the required packages by running:

```bash
pip install -r requirements.txt
```

### Environment Variables Setup

Make sure to set up the following environment variables, either in a `.env` file or through the terminal:

- `DATABASE_URI`: PostgreSQL database connection string
- `MAIL_SERVER`: SMTP server for sending emails
- `MAIL_PORT`: Port for SMTP server
- `MAIL_USERNAME`: Email account username
- `MAIL_PASSWORD`: Email account password
- `MAIL_USE_TLS`: Enable TLS (True/False)
- `MAIL_DEFAULT_SENDER`: Default email sender address
- `SECRET_KEY`: Flask secret key for session management
- `TEMPLATES_AUTO_RELOAD`: Auto reload templates (True/False)

---

## Application Components

### Main Application

The main entry point for the application is the `run.py` file.

#### `run.py`

```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    # During Production/Deployment change debug=True to False
    app.run(debug=True)
```

This file initializes the Flask application by calling `create_app()` and runs the application in debug mode for development purposes.

#### `app/__init__.py`

```python
from flask import Flask
from app.models import db
from flask_mail import Mail
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__, template_folder='views', static_folder='views/static')
    
    # Load environment variables
    load_dotenv()
    
    # Add app configuration (e.g., database, mail server)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
    app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS")
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Initialize extensions
    mail = Mail(app)
    db.init_app(app)

    # Register the Blueprints/Controllers here (for admin, dairyOwner, farmer)
    # e.g., app.register_blueprint(admin_blueprint)
    
    return app
```

#### `models/__init__.py`

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

This file initializes the SQLAlchemy object for database interactions. You can add more models to this file or create separate files for each model.

---

### Controllers

Controllers manage the routing and business logic of the application. In this project, there are three main controllers:

- **Admin**: Handles admin-related routes and logic.
- **DairyOwner**: Manages routes and logic for dairy owners.
- **Farmer**: Handles farmer-related actions.

Each controller has its own `__init__.py` file to define routes and manage view logic.

---

### Models

The `models` directory contains the database models for the application. These models are managed using SQLAlchemy and will be extended to represent various entities such as farmers, dairy owners, admins, transactions, and more.

---

### Views

The `views` directory holds the HTML templates that render the front-end interface for each section of the application. These are organized by role (admin, dairyOwner, farmer) to provide a modular and maintainable structure for UI development.

---

## Running the Application

To run the application, use the following command after setting up the virtual environment:

```bash
python run.py
```

This will start the Flask development server, which will be accessible at `http://127.0.0.1:5000`.

---

## Configuration

- **Database Configuration**: 
  The database is configured via the `SQLALCHEMY_DATABASE_URI` environment variable. Ensure your PostgreSQL database URI is correctly set up in your `.env` file.

- **Mail Configuration**: 
  The mail server is set up using Flask-Mail. Make sure to configure the mail server, port, username, and password correctly in the `.env` file for sending emails.

- **Environment Variables**:
  Set up the required environment variables either in a `.env` file or by exporting them in your terminal before running the application.


## Application Components

### Main Application
The main application entry point is located in `run.py`.

### Controllers
Controllers are responsible for handling requests and returning responses. The structure of the controllers for the farmer module includes:

- **Farmers**

## 1. `controllers/farmer/Login/farmer_login_controller.py`
   - **Login**: Handles farmer login functionality.

## 2. `controllers/farmer/Register/Registerfarmer.py`
   - **Register**: Handles farmer registration functionality.
   
## 3. `controllers/farmer/Register/validate_farmer.py`
   - **Validate**: Validates the OTP sent to the user during registration.

## 4. `controllers/farmers/farmer_reset_password.py`

This controller manages the password reset functionality for farmers. It consists of the following main features:

- **Password Reset Request:**
  - Users can reset their password by providing either their UID or email, date of birth, and phone number.
  - The system checks if the provided details match a farmer in the database. If a match is found, an OTP is generated and sent to the user's phone.
  
- **OTP Validation and Password Reset:**
  - Once the user receives the OTP, they can submit it along with their new password. If the OTP matches and the new password fields are valid (password and confirm password match), the password is updated in the database.

---

## 5. `controllers/dairyOwner/DairyOwnerLogin.py`

This controller handles the login process for dairy owners. It features:

- **Dairy Owner Login:**
  - Dairy owners can log in using either their email or unique dairy ID along with their password.
  - The system verifies the entered credentials against the database and initiates a session for the logged-in dairy owner.
  - Passwords are hashed using bcrypt for security, and the login page provides appropriate feedback for invalid credentials or server errors.

---

## 6. `controllers/dairyOwner/DairyOwnerRegister.py`

This controller facilitates dairy owner registration and OTP validation. It includes:

- **Registration Form:**
  - Users provide their email, password, address, and phone number during registration.
  - After filling in the form, OTPs (One Time Passwords) are generated and sent to both the user's email and phone for verification.
  
- **OTP Validation:**
  - After receiving OTPs via email and mobile, the user must input both OTPs to verify their identity. If the OTPs are correct, a new dairy owner record is created in the database with the provided details.

- **Error Handling:**
  - The system manages errors related to mail sending or OTP validation, providing relevant feedback for users.

---

## 7. `controllers/dairyOwner/DairyOwnerSuccessMilkEntry.py`

This controller manages the functionality for dairy owners to view and download milk entry confirmations. It includes:

- **Success Page:**
  - Displays the details of a successful milk entry transaction, including the farmer's name, quantity of milk collected, fat content, and payment status.
  
- **PDF Download:**
  - Users can download the milk entry details as a PDF. The PDF includes all relevant information about the transaction, such as collection date, milk quantity, fat content, and payment method.
  - The PDF is generated dynamically using ReportLab, and the user is prompted to download it upon request.



### Models
Models represent the data structure of the application and interact with the database. The models used in this application include:

1. **Farmer**: Represents the farmer entity with related attributes.
   - File: `models/farmer.py`

2. **Cow**: Represents the cow entity associated with farmers.
   - File: `models/cows.py`

3. **FarmerBank**: Represents the banking details of farmers.
   - File: `models/farmer_bank.py`

# Dairy Project Controllers Documentation

## `controllers/dairyOwner/ValidateFarmer.py`

This controller handles the validation process for farmers under a dairy owner. It includes OTP verification and the creation of new farmers in the database.

### **Endpoints**

- **POST `/dairyowner/validate-farmer`**
  
  Validates a farmer based on the data sent by the dairy owner. If the OTP is correct, the farmer is verified and added to the dairy's farmer list.

### **Request Parameters**

| Parameter | Type   | Description                                           |
|-----------|--------|-------------------------------------------------------|
| otp       | String | The OTP code sent to the farmer for verification.      |
| farmer_id | String | Unique identifier for the farmer being validated.      |

### **Response**

- **200 OK**: Farmer successfully validated.
- **400 Bad Request**: Invalid OTP or farmer ID.

---

## `controllers/dairyOwner/ViewMuster.py`

This controller allows dairy owners to view milk entry records grouped into 10-day periods. It calculates totals for milk, fat, rate, and the amount for each period.

### **Endpoints**

- **GET `/dairyowner/view-muster`**
  
  Retrieves the milk muster details for the dairy owner, grouping the entries by 10-day periods.

### **Request Parameters**

None.

### **Response**

- **200 OK**: Returns the milk entry records for the requested period, including total milk, fat, rate, and amount calculations.
  
---

## `controllers/dairyOwner/list_farmers.py`

This controller provides a list of all farmers associated with the dairy. Dairy owners can view the details of their farmers.

### **Endpoints**

- **GET `/dairyowner/list-farmers`**
  
  Retrieves a list of farmers associated with the dairy.

### **Request Parameters**

None.

### **Response**

- **200 OK**: Returns the list of farmers with details such as farmer name, farmer ID, and contact information.

---

## Farmer Password Reset Controller

The `controllers/farmer/farmer_reset_password.py` file handles the functionality for farmers to reset their password. It allows farmers to request a password reset by providing their email or UID, date of birth, and phone number. An OTP (One-Time Password) is generated and sent to their phone, which they must verify to reset their password.

### Routes

#### 1. `/farmer_request_reset`
This route handles the farmer's request to reset their password.

- **Method**: `GET`, `POST`
- **Description**:
  - On `GET`, it renders the password reset request form.
  - On `POST`, it collects the farmer’s UID or email, date of birth, and phone number to verify the farmer's identity. If the provided details match a record in the database, an OTP is generated and sent to the farmer's phone number.

- **Session**:
  - On successful verification, the provided details and the generated OTP are stored in the session as `reset_data`.

- **Form Data**:
  - `uid_or_email`: Farmer’s UID or email.
  - `date_of_birth`: Farmer’s date of birth.
  - `phone_number`: Farmer’s registered phone number.

- **Validation**:
  - The system checks if the farmer exists in the database by verifying the provided UID/email, date of birth, and phone number.
  - If the farmer is found, an OTP is generated and sent to the farmer.

- **Flash Messages**:
  - "OTP sent successfully!!" – Shown if an OTP is successfully generated and sent to the farmer.
  - "No user found with the details provided." – Shown if the provided information does not match any record in the database.

- **Redirects**:
  - Redirects to the `/farmer_reset_password` route to verify the OTP and reset the password.


---

## Farmer Registration Controller

The `controllers/farmer/farmer_register.py` file manages the registration process for new farmers. It collects basic personal information, farm details, and bank details from the farmer, generates an OTP for verification, and sends it via email and mobile.

### Routes

#### 1. `/farmer/signup`
This route handles the farmer registration process.

- **Method**: `GET`, `POST`
- **Description**:
  - On `GET`, it renders the farmer registration form.
  - On `POST`, it processes the registration by collecting the farmer’s personal information, farm details, and bank information, then generates and sends OTPs for validation.

- **Session**:
  - Stores farmer information in the session (`farmer_data`) after form submission, which includes the farmer’s personal, farm, and bank details.
  - Also stores the generated OTPs (`email_otp`, `mobile_otp`) for validation.

- **Form Data**:
  - **Personal Information**:
    - `firstname`: Farmer's first name.
    - `lastname`: Farmer's last name.
    - `mobile_number`: Farmer's mobile number.
    - `email`: Farmer's email address.
    - `dob`: Farmer's date of birth.
    - `address`: Farmer's residential address.
    - `password`: Farmer's password (stored temporarily, will be hashed before saving).
  - **Farm Information**:
    - `no_of_cattle`: Number of cattle the farmer owns.
    - `cattle`: A list of cattle UIDs.
    - `cattle_name`: Names of the cattle.
    - `breed`: Breed of the cattle.
    - `age`: Age of the cattle.
    - `milk_yield`: Daily milk yield per cattle.
    - `health_status`: Health status of the cattle.
  - **Bank Information**:
    - `bank_name`: Farmer’s bank name.
    - `account_no`: Farmer's account number.
    - `branch_name`: Bank branch name.
    - `ifsc_code`: IFSC code of the bank branch.

- **Validation**:
  - Ensures that all required fields (personal, farm, and bank details) are filled. If not, it flashes an error message and redirects back to the registration page.
  
- **OTP Generation**:
  - Generates a random OTP for both email and mobile number validation using `GenerateRandomOTP`.

- **Email OTP**:
  - Sends the generated OTP via email using Flask-Mail. If sending the OTP fails, it redirects to the `/Mail Error` page.

- **Flash Messages**:
  - "Please fill in all required fields." – Shown when any required field is missing.

- **Redirects**:
  - On successful OTP generation and email sending, redirects to the OTP validation page (`/validate_otp`).
  - If email sending fails, redirects to `/Mail Error`.

---

## Farmer OTP Validation Controller

The `controllers/farmer/farmer_validate.py` file manages the validation of OTPs (One Time Passwords) sent to farmers during the registration process. It handles OTP verification, inserts new farmer data into the database, and creates associated records for farmer bank details and cattle.

### Routes

#### 1. `/farmer/validate-otp`
This route handles the validation of OTPs entered by the farmer.

- **Method**: `GET`, `POST`
- **Description**:
  - On `GET`, it renders the OTP validation form.
  - On `POST`, it processes the OTP entered by the farmer, verifies it against the session data, and if valid, stores the farmer's information in the database.

- **Session**:
  - Utilizes session data to retrieve the generated OTPs (`email_otp`, `mobile_otp`) and farmer registration data (`farmer_data`).

- **Form Data**:
  - **OTP Information**:
    - `email_otp`: OTP sent to the farmer's email.
    - `mobile_otp`: OTP sent to the farmer's mobile number.

- **Validation**:
  - Checks if the OTPs entered match the stored session OTPs.
  - If valid, proceeds to insert the farmer's data into the database; if invalid, returns a 400 error with a message.

- **Database Operations**:
  - Creates a new `Farmer` object using the data from the session and hashes the password using `bcrypt`.
  - Commits the new farmer to the database to obtain the farmer ID, which is used as a foreign key for related records.
  - Creates a new `FarmerBank` object and associates it with the newly created farmer.
  - Loops through the list of cattle data and creates `Cow` objects for each entry, associating them with the farmer.

- **Session Cleanup**:
  - Clears the session data related to OTP and farmer registration once the data is successfully stored in the database.

- **Redirects**:
  - On successful validation and data insertion, redirects to the success page (`/Registration Successfull`).
  - If the OTP is invalid, it responds with an error message.



---

## `controllers/dairyOwner/AddFarmerToDairy.py`

This controller handles adding a new farmer to the dairy. It collects the farmer's basic information, cattle details, and bank details for registration.

### **Endpoints**

- **POST `/dairyowner/add-farmer`**

  Adds a new farmer to the dairy, collecting their personal information, cattle details, and bank details.

### **Request Parameters**

| Parameter         | Type   | Description                                     |
|-------------------|--------|-------------------------------------------------|
| farmer_name       | String | Name of the farmer being added.                 |
| farmer_contact    | String | Contact number of the farmer.                   |
| cattle_details    | List   | Details about the cattle owned by the farmer.   |
| bank_details      | String | Bank account details of the farmer.             |

### **Response**

- **201 Created**: Farmer successfully added to the dairy.
- **400 Bad Request**: Missing or invalid parameters.

---

## Milk Entry Controller

The `controllers/dairyStaff/milkEntry.py` file provides functionality for dairy staff to make milk entries for farmers, save them in the database, and generate downloadable PDF confirmations. Below are the key routes and their descriptions:

### Routes

#### 1. `/milk_entry/<farmer_id>`
This route handles the milk entry form for a specific farmer.

- **Method**: `GET`, `POST`
- **Description**: 
  - On `GET`, it retrieves the farmer’s information using the `farmer_id` and displays a form for inputting milk collection data.
  - On `POST`, the form data is captured and saved in the `MilkEntry` database table. The fields collected include:
    - Collection Date
    - Collection Time
    - Quantity of Milk
    - Milk Type
    - Fat Content
    - SNF (Solid Not Fat) Content
    - Rate per Liter
    - Total Amount
    - Payment Status
    - Payment Method
    - Collected By
  - After successful submission, the user is redirected to the success page.

- **Redirects**:
  - If the `farmer_id` is invalid or not found, the user is redirected to the dairy owner login page.
  - On successful entry, the user is redirected to `/dairyOwner/successmilkentry`.

#### 2. `/dairyOwner/successmilkentry`
This route displays a confirmation page for a successful milk entry.

- **Method**: `GET`
- **Description**: Renders the `SuccessMilkEntry.html` page which shows the success of the milk entry. The session data contains the milk entry details that will be used for PDF generation.

#### 3. `/dairyOwner/Download Milk Entry`
This route allows the dairy staff to download the milk entry details as a PDF.

- **Method**: `GET`
- **Description**: 
  - Retrieves the milk entry data from the session.
  - Generates a PDF using the `reportlab` library, which contains the following details:
    - Date of Milk Collection
    - Farmer Name
    - Farmer ID
    - Quantity of Milk
    - Milk Type
    - Fat Content
    - SNF Content
    - Density of Milk
    - Rate per Liter
    - Total Amount
    - Payment Status
    - Payment Method
    - Collected By
  - The PDF is returned as a downloadable file.

### Database Models Used
- **Farmer**: Retrieves farmer information by `farmer_id`.
- **MilkEntry**: Stores the milk entry data including collection details and payment information.

---

## Farmer Login Controller

The `controllers/farmer/farmer_login_control.py` file handles the login functionality for farmers, allowing them to log in using either their email or farmer ID. It validates the credentials by comparing the entered password with the stored hashed password in the database.

### Route

#### 1. `/farmer/login`
This route processes the login form for farmers.

- **Method**: `GET`, `POST`
- **Description**: 
  - On `GET`, it renders the farmer login page.
  - On `POST`, it captures the email or farmer ID and password from the form, retrieves the farmer record from the database, and checks if the provided password matches the stored hashed password.
  - If the login is successful, the farmer ID is stored in the session, and the farmer is logged in.
  - If the login fails, an appropriate failure message is returned.

- **Session**:
  - On successful login, the farmer's `farmer_id` is stored in the session for future identification.

- **Form Data**:
  - `email`: The farmer’s email or UID.
  - `password`: The farmer’s password.

- **Validation**:
  - First, it checks if the farmer exists in the database by searching with the provided email or farmer ID.
  - It uses bcrypt to compare the entered password with the hashed password stored in the database.

- **Redirects**:
  - If the farmer is not found by email or UID, an error message is displayed asking the user to register first.
  - On successful login, the session is updated, and the user is logged in.

---

## `controllers/farmers/farmer_reset_password.py`

This controller handles the password reset process for farmers, including OTP generation, OTP validation, and password updating.

### **Endpoints**

- **POST `/farmers/reset-password`**

  Initiates the password reset process by generating and sending an OTP to the farmer’s registered contact details.

### **Request Parameters**

| Parameter   | Type   | Description                                     |
|-------------|--------|-------------------------------------------------|
| farmer_id   | String | Unique identifier of the farmer requesting reset. |
| contact     | String | Contact number or email for sending the OTP.    |

### **Response**

- **200 OK**: OTP sent successfully.
- **400 Bad Request**: Invalid farmer ID or contact information.

- **POST `/farmers/verify-otp`**

  Verifies the OTP for resetting the farmer's password.

### **Request Parameters**

| Parameter   | Type   | Description                                     |
|-------------|--------|-------------------------------------------------|
| farmer_id   | String | Unique identifier of the farmer resetting password. |
| otp         | String | The OTP code sent for verification.             |
| new_password| String | The new password to be set.                     |

### **Response**

- **200 OK**: Password successfully updated.
- **400 Bad Request**: Invalid OTP or password format.

---

## `controllers/dairyOwner/DairyOwnerLogin.py`

This controller manages the login functionality for dairy owners. It verifies dairy owners using their email or UID and checks the password.

### **Endpoints**

- **POST `/dairyowner/login`**

  Authenticates a dairy owner by verifying their email or UID and password.

### **Request Parameters**

| Parameter | Type   | Description                                |
|-----------|--------|--------------------------------------------|
| emailoruid| String | Email or unique identifier (UID) of the dairy owner. |
| password  | String | Password of the dairy owner.               |

### **Response**

- **200 OK**: Login successful.
- **401 Unauthorized**: Invalid credentials.

---

## `controllers/dairyOwner/DairyOwnerRegister.py`

This controller handles the registration of dairy owners. It involves OTP validation sent via email and phone, and adding a new dairy owner to the database upon successful OTP verification.

### **Endpoints**

- **POST `/dairyowner/register`**

  Registers a new dairy owner by verifying the OTP and adding them to the system.

### **Request Parameters**

| Parameter   | Type   | Description                                     |
|-------------|--------|-------------------------------------------------|
| email       | String | Email of the dairy owner being registered.      |
| phone       | String | Phone number of the dairy owner.                |
| otp         | String | OTP sent for verification.                      |
| owner_name  | String | Name of the dairy owner.                        |
| password    | String | Password for the dairy owner.                   |

### **Response**

- **201 Created**: Dairy owner successfully registered.
- **400 Bad Request**: Invalid OTP or missing required parameters.

---

## `controllers/dairyOwner/DairyOwnerSuccessMilkEntry.py`

This controller provides functionality for dairy owners to view and download milk entry confirmation details as a PDF.

### **Endpoints**

- **GET `/dairyowner/milk-entry-success`**

  Generates and returns a confirmation of a successful milk entry for the dairy owner, with an option to download the details as a PDF.

### **Request Parameters**

| Parameter   | Type   | Description                                     |
|-------------|--------|-------------------------------------------------|
| entry_id    | String | ID of the milk entry being confirmed.           |

### **Response**

- **200 OK**: Milk entry confirmation successfully generated.
- **404 Not Found**: Milk entry not found.



### Views
Views are responsible for rendering templates and presenting data to the user. Views are organized based on the user roles: `admin`, `dairy owner`, and `farmer`.

## Running the Application
Instructions on how to run the application locally.

## Configuration
Details about configuring the application settings and any other relevant configurations.


# Models Documentation

## 1. `Admin` Model
- **Table Name**: `admin`
- **Description**: Represents the admin users in the system.
  
| Column     | Data Type    | Description                         | Constraints                |
|------------|--------------|-------------------------------------|----------------------------|
| `admin_id` | `Integer`    | Unique ID of the admin.             | Primary Key                |
| `username` | `String`     | Admin's username.                   | Not Null                   |
| `role`     | `String`     | Admin's role.                       | Not Null                   |
| `created_at`| `Date`      | Date when the admin was created.    |                            |
| `updated_at`| `Date`      | Date when the admin was last updated.|                            |

---

## 2. `DairyOwner` Model
- **Table Name**: `dairy_owner`
- **Description**: Represents a dairy owner.
  
| Column           | Data Type  | Description                                  | Constraints              |
|------------------|------------|----------------------------------------------|--------------------------|
| `dairy_id`       | `Integer`  | Unique ID for the dairy owner.               | Primary Key, Auto Increment |
| `email`          | `String`   | Email of the dairy owner.                    |                          |
| `password`       | `String`   | Hashed password for the dairy owner.         |                          |
| `address`        | `String`   | Address of the dairy.                        |                          |
| `phone_number`   | `String`   | Phone number of the dairy owner.             |                          |

### Relationships:
- `supplies`: One-to-many with `Supplies`.
- `farmer_transactions`: One-to-many with `Transaction`.
- `supply_transactions`: One-to-many with `SupplyTransaction`.
- `farmers`: One-to-many with `Farmer`.
- `milk_entry`: One-to-many with `MilkEntry`.

---

## 3. `Cow` Model
- **Table Name**: `cattle`
- **Description**: Represents the cows owned by farmers.
  
| Column         | Data Type    | Description                             | Constraints              |
|----------------|--------------|-----------------------------------------|--------------------------|
| `cattle_id`    | `String`     | Unique ID given to the cow.             | Primary Key              |
| `farmer_id`    | `Integer`    | Foreign key to the farmer owning the cow.| Foreign Key (`farmers.farmer_id`) |
| `cattle_name`  | `String`     | Name of the cow.                        |                          |
| `breed`        | `String`     | Breed of the cow.                       |                          |
| `age`          | `Integer`    | Age of the cow.                         |                          |
| `milk_yield`   | `Integer`    | Milk yield of the cow.                  |                          |
| `health_status`| `String`     | Health status of the cow.               |                          |
| `created_at`   | `Date`       | Date when the cow was added.            |                          |
| `updated_at`   | `Date`       | Date when the cow was last updated.     |                          |

---

## 4. `FarmerBank` Model
- **Table Name**: `farmer_bank`
- **Description**: Represents the bank details of a farmer.
  
| Column        | Data Type  | Description                          | Constraints              |
|---------------|------------|--------------------------------------|--------------------------|
| `account_no`  | `String`   | Farmer's bank account number.         | Primary Key              |
| `bank_name`   | `String`   | Name of the bank.                    | Not Null                 |
| `branch_name` | `String`   | Branch of the bank.                  | Not Null                 |
| `ifsc_code`   | `String`   | IFSC code of the bank.               | Not Null                 |
| `farmer_id`   | `Integer`  | Foreign key to the farmer.           | Foreign Key (`farmers.farmer_id`) |

---

## 5. `Farmer` Model
- **Table Name**: `farmers`
- **Description**: Represents the farmers associated with the dairy.
  
| Column       | Data Type   | Description                          | Constraints              |
|--------------|-------------|--------------------------------------|--------------------------|
| `farmer_id`  | `Integer`   | Unique ID of the farmer.             | Primary Key, Auto Increment |
| `first_name` | `String`    | First name of the farmer.            | Not Null                 |
| `last_name`  | `String`    | Last name of the farmer.             | Not Null                 |
| `cows`       | `Integer`   | Number of cows owned by the farmer.  |                          |
| `gender`     | `String`    | Gender of the farmer.                |                          |
| `email`      | `String`    | Email of the farmer.                 | Not Null                 |
| `phone_number`| `String`   | Phone number of the farmer.          | Not Null                 |
| `dob`        | `Date`      | Date of birth of the farmer.         |                          |
| `password`   | `String`    | Hashed password of the farmer.       | Not Null                 |
| `address`    | `String`    | Farm address of the farmer.          |                          |
| `created_at` | `Date`      | Date when the farmer was added.      |                          |
| `updated_at` | `Date`      | Date when the farmer was last updated.|                          |
| `dairy_id`   | `Integer`   | Foreign key to the dairy owner.      | Foreign Key (`dairy_owner.dairy_id`) |

### Relationships:
- `cows_relation`: One-to-many with `Cow`.
- `farmer_bank_relation`: One-to-many with `FarmerBank`.
- `supply_transactions`: One-to-many with `SupplyTransaction`.
- `farmer_payment_transactions_relation`: One-to-many with `Transaction`.
- `milk_entries`: One-to-many with `MilkEntry`.

---

## 6. `MilkEntry` Model
- **Table Name**: `milk_entries`
- **Description**: Represents the milk collection entries.
  
| Column            | Data Type   | Description                          | Constraints              |
|-------------------|-------------|--------------------------------------|--------------------------|
| `id`              | `Integer`   | Unique ID of the entry.              | Primary Key, Auto Increment |
| `farmer_id`       | `Integer`   | Foreign key to the farmer.           | Foreign Key (`farmers.farmer_id`), Not Null |
| `dairy_id`        | `Integer`   | Foreign key to the dairy owner.      | Foreign Key (`dairy_owner.dairy_id`) |
| `collection_date` | `Date`      | Date of milk collection.             | Not Null                 |
| `collection_time` | `Time`      | Time of milk collection.             | Not Null                 |
| `quantity_milk`   | `Float`     | Quantity of milk collected.          | Not Null                 |
| `milk_type`       | `String`    | Type of milk collected.              | Not Null                 |
| `fat_content`     | `Float`     | Fat content of the milk.             | Not Null                 |
| `snf_content`     | `Float`     | SNF content of the milk.             | Not Null                 |
| `rate_per_l`      | `Float`     | Rate per litre of milk.              | Not Null                 |
| `total_amount`    | `Float`     | Total amount to be paid.             | Not Null                 |
| `payment_status`  | `String`    | Payment status of the entry.         | Not Null                 |
| `payment_method`  | `String`    | Payment method for the entry.        | Not Null                 |
| `collected_by`    | `String`    | Collector of the milk.               | Not Null                 |

---

## 7. `Payment` Model
- **Table Name**: `payment`
- **Description**: Represents the payment transactions.
  
| Column         | Data Type    | Description                              | Constraints                |
|----------------|--------------|------------------------------------------|----------------------------|
| `payment_id`   | `Integer`    | Unique ID of the payment.                | Primary Key                |
| `sale_id`      | `Integer`    | Sale ID associated with the payment.     | Not Null                   |
| `payment_date` | `Date`       | Date of payment.                         |                            |
| `amount_paid`  | `Numeric`    | Amount paid.                             |                            |
| `created_at`   | `Date`       | Date when the payment was created.       |                            |
| `updated_at`   | `Date`       | Date when the payment was last updated.  |                            |

---

## 8. `Supplies` Model
- **Table Name**: `supplies`
- **Description**: Represents the supplies provided by the dairy.
  
| Column         | Data Type  | Description                              | Constraints              |
|----------------|------------|------------------------------------------|--------------------------|
| `supply_id`    | `Integer`  | Unique ID of the supply.                 | Primary Key, Auto Increment |
| `supply_name`  | `String`   | Name of the supply.                      |                          |
| `price`        | `Numeric`  | Price of the supply.                     | Not Null                 |
| `dairy_id`     | `Integer`  | Foreign key to the dairy owner.          | Foreign Key (`dairy_owner.dairy_id`), Not Null |
| `created_at`   | `Date`     | Date when the supply was added.          |                          |
| `updated_at`   | `Date`     | Date when the supply was last updated.   |                          |

---

## 9. `Transaction` Model
- **Table Name**: `transactions`
- **Description**: Represents financial transactions between the farmers and the dairy.
  
| Column         | Data Type  | Description                              | Constraints              |
|----------------|------------|------------------------------------------|--------------------------|
| `transaction_id` | `Integer` | Unique ID of the transaction.            | Primary Key, Auto Increment |
| `farmer_id`    | `Integer`  | Foreign key to the farmer.               | Foreign Key (`farmers.farmer_id`) |
| `amount`       | `Numeric`  | Transaction amount.                      | Not Null                 |
| `transaction_date`| `Date`  | Date of the transaction.                 | Not Null                 |
| `payment_status` | `String` | Status of the payment (paid/unpaid).     |                          |
| `dairy_id`     | `Integer`  | Foreign key to the dairy owner.          | Foreign Key (`dairy_owner.dairy_id`) |

---

## 10. `SupplyTransaction` Model
- **Table Name**: `supply_transaction`
- **Description**: Represents transactions related to dairy supplies.
  
| Column           | Data Type  | Description                              | Constraints              |
|------------------|------------|------------------------------------------|--------------------------|
| `transaction_id` | `Integer`  | Unique ID of the transaction.            | Primary Key, Auto Increment |
| `farmer_id`      | `Integer`  | Foreign key to the farmer.               | Foreign Key (`farmers.farmer_id`) |
| `supply_id`      | `Integer`  | Foreign key to the supply.               | Foreign Key (`supplies.supply_id`) |
| `amount`         | `Numeric`  | Amount of the transaction.               | Not Null                 |
| `transaction_date`| `Date`    | Date of the transaction.                 | Not Null                 |
| `dairy_id`       | `Integer`  | Foreign key to the dairy owner.          | Foreign Key (`dairy_owner.dairy_id`) |
