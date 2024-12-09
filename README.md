# DOCDOC

## Introduction
This website leverages the advanced capabilities of the [LayoutLMv2] (#https://huggingface.co/docs/transformers/en/model_doc/layoutlm2) AI model to classify uploaded document images into predefined categories such as letters, forms, emails, resumes, and memos, enhancing efficient document management.

## Key Features
- **Document Classification**: Automatically categorize documents based on content and layout.
- **User-Friendly Interface**: Easy navigation and interaction with minimalistic design.
- **Secure Uploads**: Ensures confidentiality and integrity of data.
- **Real-Time Processing**: Immediate classification feedback upon document uploads.
- **Accessibility**: Accessible features for users with disabilities.

## Technologies Used
- **LayoutLMv2**: Fine-tuned on diverse datasets, including the RVL-CDIP subset for robust document classification.
- **Django Framework**: Supports robust data handling and user management.
- **Front-End**: Developed with HTML5, CSS3, and JavaScript for a responsive experience.

## Potential Use Cases
- **Enterprise Document Management**: Streamline document management processes in business environments.
- **Academic Research**: Assist researchers in organizing and categorizing academic materials.
- **Legal Document Sorting**: Aid law firms in managing and sorting legal documents.

## Future Enhancements
- **Machine Learning Enhancements**: Plans to incorporate newer models and additional datasets.
- **Multi-Language Support**: Expanding to include non-English documents.
- **Advanced Security Features**: Enhance data security protocols to protect user data.

## Installation

To set up and run this project locally, follow these simple steps:

### Prerequisites

Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/), and this project requires Python 3.8 or higher.

### Setting Up a Virtual Environment

Using a virtual environment to manage the dependencies and keep your system organized is recommended. You can set up a virtual environment by running the following commands in your terminal:

# Install virtualenv if it's not installed
- pip install virtualenv

# Create a virtual environment
- virtualenv venv

# Activate the virtual environment
# On Windows
- venv\Scripts\activate
# On MacOS/Linux
- source venv/bin/activate

## Installing Dependencies
- All required dependencies are listed in the requirements.txt file which is provided in the project. Once your virtual environment is active, install these dependencies by running:
- pip install -r requirements.txt
- This will install all necessary packages to ensure the project runs correctly.

## Running the Application
- With the dependencies installed, you can now run the application:
- python manage.py runserver
- Navigate to http://localhost:8000 in your web browser to access the application.


