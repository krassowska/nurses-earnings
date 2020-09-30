INSERT INTO nursing_course (course_name, course_level) VALUES ('Pielęgniarstwo', 'magister');


INSERT INTO person (
    username, hashed_password, date_added, date_modified,
    year_of_birth, sex, years_of_experience
)
VALUES (
    'test1', '1234', NOW(), NOW(),
    '1994', 'female', '5'
);


INSERT INTO employment (
    date_from, date_to, place, position, type_of_contract, 
    wage, wage_per_x, person_id, date_entered, date_modified
)
VALUES (
    NOW(), NOW(), 'Warsaw', 'nurse', 'full-time',
    '2300', 'month', '1', NOW(), NOW()
);

INSERT INTO education (
    year_course_finished, nursing_course_id,
    person_id, date_entered, date_modified
)
VALUES (
    '2016', '1',
    '1', NOW(), NOW()
);


    