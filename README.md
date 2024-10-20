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

![image](https://github.com/user-attachments/assets/52dc15df-7cf6-49a9-9f29-053b18ec3535)


## Running the Application

**Note:** This project has been tested to work with Python 3.11.3. It may or may not work with other subsequent or previous versions.

To run the application, navigate to the project directory and execute the following commands:



Cloning the repository

```bash
git clone https://github.com/karthikbaskar5455/AWS-HELP-CHATBOT.git
```

Installing all the necessary modules and packages 
```bash
pip install -r requirements.txt
```
the showSidebarNavigation being set to false will hide the pages connected using streamlit navigation which is essential for security else the underlying 
app can be accessed without authentication using credentials 

```bash
streamlit run login.py --showSidebarNavigation False
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


