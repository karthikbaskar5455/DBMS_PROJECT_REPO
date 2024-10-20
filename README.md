# AWS Chatbot Help Service

This project is an AWS-based chatbot that provides help services using the AWS Bedrock API. It features a user-friendly interface built with Streamlit and a robust backend powered by MySQL.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Running the Application](#running-the-application)
- [License](#license)

## Features

- User authentication with login and sign-up functionality
- Main app page for chatbot interactions
- Utilizes AWS Bedrock API for AI-driven responses
- MySQL database for storing user information and session data

## Technologies Used

- **Frontend:** Streamlit
- **Backend:** MySQL
- **API:** AWS Bedrock
- **Programming Languages:** Python (specifically tested with Python 3.11.3; other versions may have compatibility issues)


## PROJECT STRUCTURE

![Screenshot from 2024-10-20 12-40-50](https://github.com/user-attachments/assets/cad82e1b-6e16-47e1-b481-fba9aac43b3e)

**Warning Note:** The project uses streamlit switch_pages functionality for linking multiple pages(app,signup,login) and subsequent navigation. In a rare case where the directory structure
interferes with the navigation it is advised to move the Backend_Functionality and the DB_Backend_MySQL folders outside the project directory , without moving the pages folder 

## Running the Application

**Compatibility Note:** This project has been tested and confirmed to work with Python version 3.11.3. Users are strongly advised to utilize this specific version, as compatibility with other versions—either previous or subsequent—cannot be guaranteed.
To run the application, execute the following commands:



Cloning the repository

```bash
git clone https://github.com/karthikbaskar5455/DBMS_PROJECT_REPO.git
```
navigate to the project directory 
```bash
cd DBMS_PROJECT_REPO
```

Installing all the necessary modules and packages 
```bash
pip install -r requirements.txt
```

the showSidebarNavigation being set to false will hide the pages connected using streamlit navigation which is essential for security else the underlying 
app can be accessed without authentication using credentials 

```bash
streamlit run login.py --client.showSidebarNavigation False 
```

## OUTPUT 

sign up page
![Screenshot from 2024-10-20 18-38-49](https://github.com/user-attachments/assets/3589ae32-86af-43e5-943b-e1b07f3d1127)

login page
![Screenshot from 2024-10-20 18-41-43](https://github.com/user-attachments/assets/d79dfd19-9ed2-47fc-b87d-4a3ca4a2232f)

aws help chatbot

img1
![image](https://github.com/user-attachments/assets/08359e13-5a96-43cc-96dc-e8adea4730f2)

img2
![image](https://github.com/user-attachments/assets/b2121ca8-b3f4-4208-9b2a-bd8e86ced8f4)




## License

This project is licensed under the **GNU General Public License v3.0**. You can freely use, modify, and distribute this project, but any derivative work must also be licensed under the GPL. 

**Disclaimer:** This software is provided "as-is", without any warranty of any kind. The authors are not liable for any damages or issues arising from its use.

See the [LICENSE](LICENSE) file for details.


