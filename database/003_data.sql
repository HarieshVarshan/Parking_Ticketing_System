USE parking_ticketing_system;

INSERT INTO employee_type (emptID, empType) VALUES 
    (1, 'admin'),
    (2, 'staff');


INSERT INTO employee (username, empType, pwd_hash) VALUES 
    ('vrshn', 'admin', SHA2('welcome', 256)),
    ('staff1', 'staff', SHA2('welcome1', 256)),
    ('staff2', 'staff', SHA2('welcome2', 256));


INSERT INTO vehicle_type (vtID, vType) VALUES 
    (1, '4w'),
    (2, '2w');


INSERT INTO status_type (stsID, stsType) VALUES 
    (1, 'free'),
    (2, 'occupied'),
    (3, 'maintenance'),
    (4, 'reserved');


INSERT INTO slot_type (stID, sType) VALUES 
    (1, 'public'),
    (2, 'authorized');


INSERT INTO authorized_vehicle (vNum, vType) VALUES
    ('AU37CR0181', '4w'),
    ('AU37CR0182', '4w'),
    ('AU37CR0183', '4w'),
    ('AU37CR0184', '4w'),
    ('AU37CR0185', '4w'),
    ('AU37CR0186', '4w'),
    ('AU37CR0187', '4w'),
    ('AU37CR0188', '4w'),
    ('AU37CR0189', '4w'),
    ('AU37CR0190', '4w'),
    ('AU37BK0191', '2w'),
    ('AU37BK0192', '2w'),
    ('AU37BK0193', '2w'),
    ('AU37BK0194', '2w'),
    ('AU37BK0195', '2w'),
    ('AU37BK0196', '2w'),
    ('AU37BK0197', '2w'),
    ('AU37BK0198', '2w'),
    ('AU37BK0199', '2w'),
    ('AU37BK0200', '2w');


INSERT INTO vehicle (vNum, vType) VALUES
    ('AU37CR0181', '4w'),
    ('AU37CR0182', '4w'),
    ('AU37CR0183', '4w'),
    ('AU37CR0184', '4w'),
    ('AU37CR0185', '4w'),
    ('AU37CR0186', '4w'),
    ('AU37CR0187', '4w'),
    ('AU37CR0188', '4w'),
    ('AU37CR0189', '4w'),
    ('AU37CR0190', '4w'),
    ('AU37BK0191', '2w'),
    ('AU37BK0192', '2w'),
    ('AU37BK0193', '2w'),
    ('AU37BK0194', '2w'),
    ('AU37BK0195', '2w'),
    ('AU37BK0196', '2w'),
    ('AU37BK0197', '2w'),
    ('AU37BK0198', '2w'),
    ('AU37BK0199', '2w'),
    ('AU37BK0200', '2w');


INSERT INTO contact_info (vNum, phoneNum) VALUES
    ('AU37CR0181', '3000000000'),
    ('AU37CR0182', '3000000001'),
    ('AU37CR0183', '3000000002'),
    ('AU37CR0184', '3000000003'),
    ('AU37CR0185', '3000000004'),
    ('AU37CR0186', '3000000005'),
    ('AU37CR0187', '3000000006'),
    ('AU37CR0188', '3000000007'),
    ('AU37CR0189', '3000000008'),
    ('AU37CR0190', '3000000009'),
    ('AU37BK0191', '4000000000'),
    ('AU37BK0192', '4000000001'),
    ('AU37BK0193', '4000000002'),
    ('AU37BK0194', '4000000003'),
    ('AU37BK0195', '4000000004'),
    ('AU37BK0196', '4000000005'),
    ('AU37BK0197', '4000000006'),
    ('AU37BK0198', '4000000007'),
    ('AU37BK0199', '4000000008'),
    ('AU37BK0200', '4000000009');




CALL addNewSlots(1,   100, '4w', 'public');
CALL addNewSlots(101, 180, '2w', 'public');
CALL addNewSlots(181, 190, '4w', 'authorized');
CALL addNewSlots(191, 200, '2w', 'authorized');