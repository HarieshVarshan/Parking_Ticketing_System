USE parking_ticketing_system;

DROP procedure IF EXISTS addNewSlots;
DELIMITER //
CREATE DEFINER=root@localhost PROCEDURE addNewSlots(IN start_id INT, IN end_id INT, IN _vType VARCHAR(45), IN _sType VARCHAR(45))
BEGIN
    DECLARE i INT DEFAULT start_id;
    WHILE i <= end_id DO
        INSERT INTO slot (sID, vNum, vType, sType, status, updatedBy) 
        VALUES (i, NULL, _vType, _sType, 'free', NULL);
        SET i = i + 1;
        END WHILE;
END //
DELIMITER ;


DROP procedure IF EXISTS takeSnapShot;
DELIMITER //
CREATE DEFINER=root@localhost PROCEDURE takeSnapShot()
BEGIN
  SELECT * FROM contact_info;
  SELECT * FROM employee;
  SELECT * FROM employee_type;
  SELECT * FROM entries;
  SELECT * FROM slot;
  SELECT * FROM slot_type;
  SELECT * FROM status_type;
  SELECT * FROM vehicle;
  SELECT * FROM vehicle_type;
END //
DELIMITER ;
