BEGIN;

CREATE TABLE IF NOT EXISTS auth_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS django_content_type (
    id SERIAL PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS auth_permission (
    id SERIAL PRIMARY KEY,
    content_type_id INTEGER NOT NULL REFERENCES django_content_type (id) DEFERRABLE INITIALLY DEFERRED,
    codename VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS auth_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP NULL,
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(150) NOT NULL UNIQUE,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined TIMESTAMP NOT NULL,
    first_name VARCHAR(150) NOT NULL
);

CREATE TABLE myapp_person (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    birth_date DATE
);
INSERT INTO myapp_person (first_name, last_name, birth_date) VALUES
('John','Doe','1980-01-01'),
('John','Doe','1980-01-01'),
('John','Doe','1980-01-01');

CREATE TABLE IF NOT EXISTS django_migrations (
    id SERIAL PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied TIMESTAMP NOT NULL
);
INSERT INTO django_migrations (app, name, applied) VALUES
('contenttypes','0001_initial','2024-06-15 10:01:51.077190'),
('auth','0001_initial','2024-06-15 10:01:51.099063'),
('admin','0001_initial','2024-06-15 10:01:51.119620'),
('admin','0002_logentry_remove_auto_add','2024-06-15 10:01:51.142046'),
('admin','0003_logentry_add_action_flag_choices','2024-06-15 10:01:51.152055'),
('contenttypes','0002_remove_content_type_name','2024-06-15 10:01:51.180151'),
('auth','0002_alter_permission_name_max_length','2024-06-15 10:01:51.197902'),
('auth','0003_alter_user_email_max_length','2024-06-15 10:01:51.213918'),
('auth','0004_alter_user_username_opts','2024-06-15 10:01:51.230295'),
('auth','0005_alter_user_last_login_null','2024-06-15 10:01:51.243641'),
('auth','0006_require_contenttypes_0002','2024-06-15 10:01:51.252942'),
('auth','0007_alter_validators_add_error_messages','2024-06-15 10:01:51.264079'),
('auth','0008_alter_user_username_max_length','2024-06-15 10:01:51.285801'),
('auth','0009_alter_user_last_name_max_length','2024-06-15 10:01:51.301642'),
('auth','0010_alter_group_name_max_length','2024-06-15 10:01:51.317536'),
('auth','0011_update_proxy_permissions','2024-06-15 10:01:51.331331'),
('auth','0012_alter_user_first_name_max_length','2024-06-15 10:01:51.343695'),
('sessions','0001_initial','2024-06-15 10:01:51.350766');

CREATE TABLE IF NOT EXISTS auth_group_permissions (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES auth_group (id) DEFERRABLE INITIALLY DEFERRED,
    permission_id INTEGER NOT NULL REFERENCES auth_permission (id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE IF NOT EXISTS auth_user_groups (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user (id) DEFERRABLE INITIALLY DEFERRED,
    group_id INTEGER NOT NULL REFERENCES auth_group (id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE IF NOT EXISTS auth_user_user_permissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user (id) DEFERRABLE INITIALLY DEFERRED,
    permission_id INTEGER NOT NULL REFERENCES auth_permission (id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE IF NOT EXISTS django_admin_log (
    id SERIAL PRIMARY KEY,
    object_id TEXT NULL,
    object_repr VARCHAR(200) NOT NULL,
    action_flag SMALLINT NOT NULL CHECK (action_flag >= 0),
    change_message TEXT NOT NULL,
    content_type_id INTEGER NULL REFERENCES django_content_type (id) DEFERRABLE INITIALLY DEFERRED,
    user_id INTEGER NOT NULL REFERENCES auth_user (id) DEFERRABLE INITIALLY DEFERRED,
    action_time TIMESTAMP NOT NULL
);
INSERT INTO django_content_type (app_label, model) VALUES
('admin','logentry'),
('auth','permission'),
('auth','group'),
('auth','user'),
('contenttypes','contenttype'),
('sessions','session');

CREATE TABLE IF NOT EXISTS django_session (
    session_key VARCHAR(40) NOT NULL PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date TIMESTAMP NOT NULL
);

CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_no TEXT NOT NULL
);
INSERT INTO Users (username, email, phone_no) VALUES
('john_doe', 'john@example.com', '123-456-7890'),
('jane_smith', 'jane@example.com', '098-765-4321'),
('alice_jones', 'alice@example.com', '555-123-4567'),
('bipul', 'naksjnl@gmail.com', '985234758'),
('Nischal', 'nischal123@gmail.com', '9825467798');

CREATE TABLE Authentication (
    auth_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users (user_id),
    password TEXT NOT NULL
);
INSERT INTO Authentication (user_id, password) VALUES
(1, 'password123'),
(2, 'password456'),
(3, 'password789'),
(4, '154bipul'),
(5, 'Nischal123');

-- Remove SQLite-specific sequence reset, PostgreSQL handles sequences differently
-- DELETE FROM sqlite_sequence;
-- INSERT INTO sqlite_sequence VALUES('django_migrations', 18);
-- INSERT INTO sqlite_sequence VALUES('django_admin_log', 0);
-- INSERT INTO sqlite_sequence VALUES('django_content_type', 6);
-- INSERT INTO sqlite_sequence VALUES('auth_permission', 24);
-- INSERT INTO sqlite_sequence VALUES('auth_group', 0);
-- INSERT INTO sqlite_sequence VALUES('auth_user', 0);
-- INSERT INTO sqlite_sequence VALUES('auth_group_permissions', 0);
-- INSERT INTO sqlite_sequence VALUES('auth_user_groups', 0);
-- INSERT INTO sqlite_sequence VALUES('auth_user_user_permissions', 0);

COMMIT;
