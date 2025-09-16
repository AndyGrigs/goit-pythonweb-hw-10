-- Ініціалізація бази даних
\c contacts_db;

-- Створення таблиці (SQLAlchemy також створить, але для впевненості)
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    birth_date DATE NOT NULL,
    additional_data TEXT
);

-- Створення індексів
CREATE INDEX IF NOT EXISTS idx_contacts_first_name ON contacts(first_name);
CREATE INDEX IF NOT EXISTS idx_contacts_last_name ON contacts(last_name);
CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts(email);

-- Тестові дані
INSERT INTO contacts (first_name, last_name, email, phone_number, birth_date, additional_data) 
VALUES 
    ('Іван', 'Петренко', 'ivan.petrenko@example.com', '+380501234567', '1990-05-15', 'Тестовий контакт'),
    ('Марія', 'Коваленко', 'maria.kovalenko@example.com', '+380671234567', '1985-12-25', 'Новорічний контакт'),
    ('Олександр', 'Сидоренко', 'alex.sydorenko@example.com', '+380991234567', '1992-08-22', 'Літній контакт')
ON CONFLICT (email) DO NOTHING;