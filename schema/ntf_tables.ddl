CREATE SCHEMA IF NOT EXISTS notification;

-- CREATE TABLE IF NOT EXISTS notification.users (
--     user_id uuid PRIMARY KEY,
--     first_name TEXT,
--     last_name TEXT,
--     email TEXT NOT NULL,
--     subscribe TEXT NOT NULL
-- );

CREATE TABLE IF NOT EXISTS notification.email_template (
    id UUID PRIMARY KEY,

    message TEXT NOT NULL UNIQUE,
    destination TEXT NOT NULL,

    title TEXT,
    text TEXT,
    content TEXT,

    subject TEXT,
    source TEXT NOT NULL,
    html_code TEXT NOT NULL
);

-- user_id, ntf_id, email, first_name, last_name, destination, type, subject, title, text, priority, source, time, status
-- id,destination,type,subject,title,text,priority,time,source

CREATE TABLE IF NOT EXISTS notification.user_ntf (
    user_id uuid,
    ntf_id uuid,
    email TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    destination TEXT NOT NULL,
    type TEXT NOT NULL,
    subject TEXT NOT NULL,
    title TEXT,
    text TEXT,
    content TEXT,
    priority TEXT,
    source TEXT NOT NULL,
    time timestamp,
    status TEXT NOT NULL
);
--
-- CREATE UNIQUE INDEX user_ntf_idx ON notification.user_ntf (user_id, ntf_id, status);

INSERT INTO notification.email_template (id, message, destination, title, text, content, subject, source, html_code)
VALUES ('5c159abc-f3c5-49ca-ab01-fbc0a60f97cf',
        'welcome',
        'Email',
        'Congratulation!',
        'You have been registered in Movie Service.',
        'main_page',
        'Registration',
        'Service',
        '<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
    <div style="width: 630px; font: var(--font-500,600 Suisse,Arial,Helvetica,sans-serif); text-align: center;">
		<div style="text-align: center;">
			<h1>{{title}}</h1>
		</div>
		<div style="width: 100%; background: #f0f5f8; border-radius: 10px; margin-top: 10px; padding: 10px;">
			<h2 style="color: #0474ff;">
				Hello, {{user}}!
			</h2>
			<p style="width: 95%; margin: 10px auto; font-size: 18px;">
				{{text}} {{content}}
			</p>
		</div>
		<div>
			<p style="text-align: center;">
				<a href="{{unsubscribe}}" style="color: #0474ff; font-size: 12px;">Click here to unsubscribe</a>
			</p>
		</div>
	</div>
</body>
</html>'),
    ('c3b165e1-c229-42b0-a424-852b8acff74e',
     'best_movies',
     'Email',
     'Best movies',
     'Movies list:',
     'movies',
     'Best movies',
     'Auto',
     '<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
    <div style="width: 630px; font: var(--font-500,600 Suisse,Arial,Helvetica,sans-serif); text-align: center;">
		<div style="text-align: center;">
			<h1>{{title}}</h1>
		</div>
		<div style="width: 100%; background: #f0f5f8; border-radius: 10px; margin-top: 10px; padding: 10px;">
			<h2 style="color: #0474ff;">
				Hello, {{user}}!
			</h2>
			<p style="width: 95%; margin: 10px auto; font-size: 18px;">
				{{text}} {{content}}
			</p>
		</div>
		<div>
			<p style="text-align: center;">
				<a href="{{unsubscribe}}" style="color: #0474ff; font-size: 12px;">Click here to unsubscribe</a>
			</p>
		</div>
	</div>
</body>
</html>'),

    ('66e00eb1-f72d-4b29-8fbd-083fe2fca747',
     'personal',
     'Email',
     '',
     '',
     '',
     '',
     'Admin',
     '<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
    <div style="width: 630px; font: var(--font-500,600 Suisse,Arial,Helvetica,sans-serif); text-align: center;">
		<div style="text-align: center;">
			<h1>{{title}}</h1>
		</div>
		<div style="width: 100%; background: #f0f5f8; border-radius: 10px; margin-top: 10px; padding: 10px;">
			<h2 style="color: #0474ff;">
				Hello, {{user}}!
			</h2>
			<p style="width: 95%; margin: 10px auto; font-size: 18px;">
				{{text}} {{content}}
			</p>
		</div>
		<div>
			<p style="text-align: center;">
				<a href="{{unsubscribe}}" style="color: #0474ff; font-size: 12px;">Click here to unsubscribe</a>
			</p>
		</div>
	</div>
</body>
</html>'),

    ('379521a0-d46d-4ea5-863f-076b6bbfa007',
     'new_movie',
     'Email',
     '',
     '',
     '',
     '',
     'Admin',
     '<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
    <div style="width: 630px; font: var(--font-500,600 Suisse,Arial,Helvetica,sans-serif); text-align: center;">
		<div style="text-align: center;">
			<h1>{{title}}</h1>
		</div>
		<div style="width: 100%; background: #f0f5f8; border-radius: 10px; margin-top: 10px; padding: 10px;">
			<h2 style="color: #0474ff;">
				Hello, {{user}}!
			</h2>
			<p style="width: 95%; margin: 10px auto; font-size: 18px;">
				{{text}}: {{content}}
			</p>
		</div>
		<div>
			<p style="text-align: center;">
				<a href="{{unsubscribe}}" style="color: #0474ff; font-size: 12px;">Click here to unsubscribe</a>
			</p>
		</div>
	</div>
</body>
</html>'),

    ('294eb4d3-bd62-4d24-9393-e0ac40f2385c',
     'event',
     'Email',
     '',
     '',
     '',
     '',
     'Admin',
     '<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
    <div style="width: 630px; font: var(--font-500,600 Suisse,Arial,Helvetica,sans-serif); text-align: center;">
		<div style="text-align: center;">
			<h1>{{title}}</h1>
		</div>
		<div style="width: 100%; background: #f0f5f8; border-radius: 10px; margin-top: 10px; padding: 10px;">
			<h2 style="color: #0474ff;">
				Hello, {{user}}!
			</h2>
			<p style="width: 95%; margin: 10px auto; font-size: 18px;">
				{{text}} {{content}}
			</p>
		</div>
		<div>
			<p style="text-align: center;">
				<a href="{{unsubscribe}}" style="color: #0474ff; font-size: 12px;">Click here to unsubscribe</a>
			</p>
		</div>
	</div>
</body>
</html>');

-- docker cp schema/ntf_tables.ddl postgres_db:/ntf_tables.ddl
-- docker exec -it postgres_db psql -h 127.0.0.1 -U app -d movies_db -f ntf_tables.ddl


-- psql -h 127.0.0.1 -U app -d movies_db
-- docker exec -it postgres bash

