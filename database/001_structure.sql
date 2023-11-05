-- Author: Hariesh Varshan

-- Create database and select it for use
DROP DATABASE IF EXISTS parking_ticketing_system;
CREATE DATABASE IF NOT EXISTS parking_ticketing_system;
USE parking_ticketing_system;


-- Table structure for table vehicle_type
CREATE TABLE IF NOT EXISTS vehicle_type (
    vtID int unsigned NOT NULL,
    vType varchar(45) NOT NULL,
    PRIMARY KEY (vtID),
    UNIQUE KEY vtID_UNIQUE (vtID),
    UNIQUE KEY vType_UNIQUE (vType)
);


-- Table structure for table vehicle
CREATE TABLE IF NOT EXISTS vehicle (
    vID int unsigned NOT NULL AUTO_INCREMENT,
    vNum varchar(15) NOT NULL,
    vType varchar(30) NOT NULL,
    PRIMARY KEY (vID,vNum),
    UNIQUE KEY vID_UNIQUE (vID),
    UNIQUE KEY vNum_UNIQUE (vNum),
    KEY fk_vType_idx (vType),
    CONSTRAINT fk_vType FOREIGN KEY (vType) REFERENCES vehicle_type (vType)
);


-- Table structure for table authorized_vehicle
CREATE TABLE IF NOT EXISTS authorized_vehicle (
    avID int NOT NULL AUTO_INCREMENT,
    vNum varchar(15) NOT NULL,
    vType varchar(30) NOT NULL,
    PRIMARY KEY (avID),
    UNIQUE KEY vNum_UNIQUE (vNum),
    UNIQUE KEY avID_UNIQUE (avID),
    KEY fk_vType_2_idx (vType),
    CONSTRAINT fk_vType_2 FOREIGN KEY (vType) REFERENCES vehicle_type (vType)
);

-- Table structure for table status_type
CREATE TABLE IF NOT EXISTS status_type (
    stsID int unsigned NOT NULL,
    stsType varchar(45) NOT NULL,
    PRIMARY KEY (stsID),
    UNIQUE KEY stsID_UNIQUE (stsID),
    UNIQUE KEY stsType_UNIQUE (stsType)
);


-- Table structure for table slot_type
CREATE TABLE IF NOT EXISTS slot_type (
    stID int unsigned NOT NULL,
    sType varchar(45) NOT NULL,
    PRIMARY KEY (stID),
    UNIQUE KEY stID_UNIQUE (stID),
    UNIQUE KEY sType_UNIQUE (sType)
);



-- Table structure for table employee_type
CREATE TABLE IF NOT EXISTS employee_type (
    emptID int unsigned NOT NULL,
    empType varchar(45) NOT NULL,
    PRIMARY KEY (emptID),
    UNIQUE KEY emptID_UNIQUE (emptID),
    UNIQUE KEY empType_UNIQUE (empType)
);


-- Table structure for table employee
CREATE TABLE IF NOT EXISTS employee (
    username varchar(45) NOT NULL,
    empType varchar(45) NOT NULL,
    pwd_hash varchar(256) NOT NULL,
    lastLogin datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (username),
    UNIQUE KEY username_UNIQUE (username),
    KEY fk_empType_idx (empType),
    CONSTRAINT fk_empType FOREIGN KEY (empType) REFERENCES employee_type (empType)
);


-- Table structure for table slot
CREATE TABLE IF NOT EXISTS slot (
    sID int unsigned NOT NULL,
    vNum varchar(15) DEFAULT NULL,
    vType varchar(45) DEFAULT NULL,
    sType varchar(45) NOT NULL,
    status varchar(45) DEFAULT NULL,
    updatedBy varchar(45) DEFAULT NULL,
    PRIMARY KEY (sID),
    UNIQUE KEY sID_UNIQUE (sID),
    KEY fk_vNum_2_idx (vNum),
    KEY fk_vType_1_idx (vType),
    KEY fk_sType_idx (sType),
    KEY fk_stsType_idx (status),
    KEY fk_updatedBy_idx (updatedBy),
    CONSTRAINT fk_stsType FOREIGN KEY (status) REFERENCES status_type (stsType),
    CONSTRAINT fk_sType FOREIGN KEY (sType) REFERENCES slot_type (sType),
    CONSTRAINT fk_updatedBy FOREIGN KEY (updatedBy) REFERENCES employee (username),
    CONSTRAINT fk_vNum_2 FOREIGN KEY (vNum) REFERENCES vehicle (vNum),
    CONSTRAINT fk_vType_1 FOREIGN KEY (vType) REFERENCES vehicle_type (vType)
);


-- Table structure for table entries
CREATE TABLE IF NOT EXISTS entries (
    eID int unsigned NOT NULL AUTO_INCREMENT,
    vNum varchar(15) NOT NULL,
    entryTime datetime DEFAULT NULL,
    exitTime datetime DEFAULT NULL,
    cost float NOT NULL DEFAULT '0',
    lastUpdated datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (eID),
    UNIQUE KEY eID_UNIQUE (eID),
    KEY fk_vNum_idx (vNum),
    CONSTRAINT fk_vNum_1 FOREIGN KEY (vNum) REFERENCES vehicle (vNum)
);


-- Table structure for table contact_info
CREATE TABLE IF NOT EXISTS contact_info (
    vNum varchar(15) NOT NULL,
    phoneNum varchar(20) NOT NULL,
    KEY fk_vNum_idx (vNum),
    CONSTRAINT fk_vNum FOREIGN KEY (vNum) REFERENCES vehicle (vNum)
);