INSERT INTO users (username, email, password) VALUES 
('Vanya1', 'example1@mail.ru', 'qwerty123'),
('Vanya2', 'example2@mail.ru', 'qwerty123'),
('Vanya3', 'example3@mail.ru', 'qwerty123'),
('Vanya4', 'example4@mail.ru', 'qwerty123'),
('Vanya5', 'example5@mail.ru', 'qwerty123'),
('Vanya6', 'example6@mail.ru', 'qwerty123'),
('Vanya7', 'example7@mail.ru', 'qwerty123'),
('Vanya8', 'example8@mail.ru', 'qwerty123'),
('Vanya9', 'example9@mail.ru', 'qwerty123'),
('Vanya10', 'example10@mail.ru', 'qwerty123');

INSERT INTO users (username, email, password, role) VALUES 
('admin', 'admin@mail.ru', 'qwerty123', 'admin'),
('reviewer', 'reviewer@mail.ru', 'qwerty123', 'reviewer');


INSERT INTO projects (title, description, author_id, repository_url) VALUES 
('Веб-сайт по играм', 'Сайт с обзорами на игры', (SELECT id_user FROM users WHERE username = 'Vanya7'), 'https://github.com/Vanya7/project'),
('Игра', 'Игра типа Марио', (SELECT id_user FROM users WHERE username = 'Vanya10'), 'https://github.com/Vanya10/project'),
('Приложение', 'Приложение для знакомств', (SELECT id_user FROM users WHERE username = 'Vanya5'), 'https://github.com/Vanya5/project'),
('Видеомонтаж', 'Приложение для видеомонтажа', (SELECT id_user FROM users WHERE username = 'Vanya3'), 'https://github.com/Vanya3/project');

INSERT INTO reviews (project_id, reviewer_id, rating, comment) VALUES 
(3, (SELECT id_user FROM users WHERE username = 'Vanya1'), 10, 'Эталонная работа!'),
(1, (SELECT id_user FROM users WHERE username = 'Vanya4'), 8, 'Добавь регистрацию'),
(4, (SELECT id_user FROM users WHERE username = 'Vanya2'), 1, 'Надо все переделать');