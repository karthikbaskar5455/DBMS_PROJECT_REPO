CREATE DATABASE AWS_HELP_CHATBOT_BACKEND;
USE AWS_HELP_CHATBOT_BACKEND;

-- CREATING USER_AUTH TABLE
CREATE TABLE USER_AUTH (
    Pwd_ID INT PRIMARY KEY AUTO_INCREMENT ,
    Hashed_Pwd VARCHAR(255) NOT NULL,
    pwd VARCHAR(255) NOT NULL,
    Hashing_Algorithm VARCHAR(50) NOT NULL
);

-- creating chatbot model table
CREATE TABLE CHATBOT_MODEL (
    Model_ID INT PRIMARY KEY AUTO_INCREMENT ,
    Model_Name VARCHAR(100) NOT NULL,
    Version VARCHAR(50) NOT NULL,
    Release_Date DATE NOT NULL,
    Developer_Company VARCHAR(100) NOT NULL,
    UNIQUE (Model_Name, Version)  -- Ensures that the same model name cannot have the same version
);

-- creating user table
CREATE TABLE USER_ (
    User_ID INT PRIMARY KEY AUTO_INCREMENT ,
    Username VARCHAR(200) NOT NULL,
    Name VARCHAR(100) NOT NULL,
    Age INT CHECK (Age >= 0),  -- Ensures age is a non-negative value
    DOB DATE NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Created_At DATETIME DEFAULT NOW(),
    Pwd_ID INT,
    FOREIGN KEY (Pwd_ID) REFERENCES USER_AUTH(Pwd_ID)  -- Foreign key reference
);

-- creating location info table
CREATE TABLE LOCATION_INFO (
    Location_ID INT PRIMARY KEY AUTO_INCREMENT ,
    Location_Coordinates VARCHAR(200) NOT NULL,  -- Assuming coordinates are stored as a string
    Country_Code CHAR(2) NOT NULL,         -- Typically a 2-letter ISO country code
    Region VARCHAR(100) NOT NULL,
    City VARCHAR(100) NOT NULL
);

-- creating device info table
CREATE TABLE DEVICE_INFO (
	device_Info_ID int PRIMARY KEY AUTO_INCREMENT,
    IP_Address VARCHAR(145) ,  -- Supports both IPv4 and IPv6 addresses
    System_OS VARCHAR(100) NOT NULL,
    Release_ VARCHAR(500) NOT NULL,
    Version VARCHAR(500) NOT NULL,
    Machine VARCHAR(500) NOT NULL,
    Processor VARCHAR(500) NOT NULL
);

-- create session table
CREATE TABLE SESSION_ (
    Session_ID INT PRIMARY KEY AUTO_INCREMENT ,
    Start_Time DATETIME NOT NULL,
    End_Time DATETIME NOT NULL,
    Duration INT NOT NULL,                        -- Duration in seconds or another unit as needed
    User_ID INT,
    Device_ID INT,                       -- To accommodate both IPv4 and IPv6 addresses
    Location_ID INT,
    Model_ID INT,
    FOREIGN KEY (User_ID) REFERENCES USER_(User_ID),                 -- foreign key reference to USER_
    FOREIGN KEY (Device_ID) REFERENCES DEVICE_INFO(device_Info_ID),    -- foreign key reference to DEVICE_INFO
    FOREIGN KEY (Location_ID) REFERENCES LOCATION_INFO(Location_ID),  -- foreign key reference to LOCATION_INFO
    FOREIGN KEY (Model_ID) REFERENCES CHATBOT_MODEL(Model_ID)       -- foreign key reference to CHATBOT_MODEL
);



-- creating login attempts history table
CREATE TABLE LOGIN_ATTEMPTS (
    login_session_ID INT PRIMARY KEY AUTO_INCREMENT ,
    Status ENUM('Success', 'Failure') NOT NULL,  -- Enum to specify login status
    Timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ,
    User_ID INT,
    Location_ID INT,
    device_Info_ID INT,
    FOREIGN KEY (User_ID) REFERENCES USER_(User_ID),  -- foreign key reference to USER_
    FOREIGN KEY (Location_ID) REFERENCES LOCATION_INFO(Location_ID),  -- foreign key reference to LOCATION_INFO
    FOREIGN KEY (device_Info_ID) REFERENCES DEVICE_INFO(device_Info_ID)  -- foreign key reference to DEVICE_INFO
);

-- creating user prompt table
CREATE TABLE USER_PROMPT (
    Prompt_ID INT PRIMARY KEY AUTO_INCREMENT ,
    Prompt TEXT NOT NULL,                     -- Use TEXT for potentially long prompts
    Timestamp DATETIME NOT NULL,
    User_ID INT,
    Session_ID INT,
    FOREIGN KEY (User_ID) REFERENCES USER_(User_ID),             -- foreign key reference to USER_
--     FOREIGN KEY (Response_ID) REFERENCES RESPONSES(Response_ID),  -- foreign key reference to RESPONSES
    FOREIGN KEY (Session_ID) REFERENCES SESSION_(Session_ID)       -- foreign key reference to SESSION_
);

-- creating responses table
CREATE TABLE RESPONSES (
    Response_ID INT PRIMARY KEY AUTO_INCREMENT ,
    Timestamp DATETIME NOT NULL,
    Response TEXT NOT NULL,                     -- Use TEXT for potentially long responses
    Model_ID INT,
    Session_ID INT,
    Prompt_ID INT,
    FOREIGN KEY (Model_ID) REFERENCES CHATBOT_MODEL(Model_ID),    -- foreign key reference to CHATBOT_MODEL
    FOREIGN KEY (Session_ID) REFERENCES SESSION_(Session_ID),       -- foreign key reference to SESSION_
    FOREIGN KEY (Prompt_ID) REFERENCES USER_PROMPT(Prompt_ID)     -- foreign key reference to USER_PROMPT
);


-- SHOW DATABASES;
-- SHOW TABLES;
-- -- -- 
-- DESC CHATBOT_MODEL;
-- DESC DEVICE_INFO;
-- DESC LOCATION_INFO;
-- DESC LOGIN_ATTEMPTS;
-- DESC RESPONSES;
-- DESC SESSION_;
-- DESC USER_;
-- DESC USER_AUTH;
-- DESC USER_PROMPT;

-- THIS INSERT OPERATION IS TO BE PERFORMED AFTER THE TABLES AND THE DB ITSELF IS SUCCESSFULLY CREATED
-- INSERT INTO CHATBOT_MODEL (Model_Name, Version, Release_Date, Developer_Company) VALUES
-- ('ChatGPT', 'v1.0', '2022-11-30', 'OpenAI'),
-- ('Bard', 'v1.2', '2023-01-15', 'Google'),
-- ('Claude', 'v2.0', '2023-05-10', 'Anthropic'),
-- ('ChatGPT', 'v1.5', '2023-07-20', 'OpenAI'),
-- ('Jasper', 'v3.1', '2023-03-12', 'Jasper AI');
