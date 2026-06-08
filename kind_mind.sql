CREATE DATABASE IF NOT EXISTS KindMind;

USE KindMind;

CREATE TABLE IF NOT EXISTS Users (
User_id INT PRIMARY KEY AUTO_INCREMENT,
Name VARCHAR(100) NOT NULL,
Email VARCHAR(100) UNIQUE NOT NULL,
Hashed_password VARCHAR(255) NOT NULL,
Created_at DATE NOT NULL,
Deleted_at DATE
);

CREATE TABLE IF NOT EXISTS MoodCategory (
Category_id INT PRIMARY KEY AUTO_INCREMENT,
Category_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS MoodScore (
Score_id INT PRIMARY KEY AUTO_INCREMENT,
Score_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS MoodOptions (
Mood_id INT PRIMARY KEY AUTO_INCREMENT,
Mood_name VARCHAR(100) NOT NULL,
Mood_category INT NOT NULL,
FOREIGN KEY (Mood_category)
REFERENCES MoodCategory(Category_id),
Mood_score INT NOT NULL, 
FOREIGN KEY (Mood_score)
REFERENCES MoodScore(Score_id),
Description VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS EnergyLevel (
Energy_id INT PRIMARY KEY AUTO_INCREMENT,
Energy_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS WeatherOptions (
Weather_id INT PRIMARY KEY AUTO_INCREMENT,
Weather_name VARCHAR (100) NOT NULL
);

CREATE TABLE IF NOT EXISTS JournalEntries (
Entry_id INT PRIMARY KEY AUTO_INCREMENT,
User_id INT NOT NULL, 
FOREIGN KEY (User_id)
REFERENCES Users(User_id) ON DELETE CASCADE,
Title VARCHAR(100) NOT NULL,
Content TEXT NOT NULL,
Mood INT NOT NULL,
FOREIGN KEY (Mood)
REFERENCES MoodOptions(Mood_id),
Energy_level INT NOT NULL,
FOREIGN KEY (Energy_level)
REFERENCES EnergyLevel(Energy_id),
Free_time BOOLEAN NOT NULL,
Weather INT NOT NULL,
FOREIGN KEY (Weather)
REFERENCES WeatherOptions(Weather_id),
Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS Recommendations(
Recommendation_id INT PRIMARY KEY AUTO_INCREMENT,
Entry_id INT NOT NULL,
FOREIGN KEY (Entry_id)
REFERENCES JournalEntries(Entry_id) ON DELETE CASCADE,
Recommendation_text VARCHAR(255) NOT NULL,
Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
Deleted_at TIMESTAMP
);

-- =========================================================
-- 02- KINDMIND MOCK DATA
-- =========================================================

INSERT IGNORE INTO EnergyLevel
VALUES 
(1,'Drained'),
(2,'Sluggish'),
(3,'Mellow'),
(4,'Steady'),
(5,'Vibrant'),
(6,'Driven'),
(7,'Radiant');


INSERT INTO MoodCategory
VALUES
(1,'Negative'),
(2,'Neutral'),
(3,'Positive'),
(4,'Ambiguous');

INSERT INTO MoodScore
VALUES
(1,'Terrible'),
(2,'Bad'),
(3,'Off'),
(4,'Ok'),
(5,'Good'),
(6,'Great'),
(7,'Fantastic'),
(8,'Mixed'),
(9,'Unsure');

INSERT INTO MoodOptions (Mood_name, Mood_category, Mood_score, Description) 
VALUES
('Miserable', 1, 1, 'Deeply unhappy, overwhelmed, or completely drained.'),
('Angry', 1, 2, 'Irritated, frustrated, or experiencing high-tension negative energy.'),
('Anxious', 1, 2, 'Nervous, worried, or feeling on edge about something.'),
('Sad', 1, 2, 'Down, gloomy, or feeling a sense of emotional loss.'),
('Stressed', 1, 3, 'Under pressure, mentally fatigued, or dealing with heavy demands.'),
('Tired', 1, 3, 'Low physical energy affecting your mood; sluggish.'),
('Calm', 2, 4, 'Peaceful, relaxed, and emotionally steady.'),
('Bored', 2, 4, 'Unstimulated, flat, or lacking interest in current activities.'),
('Focused', 2, 4, 'Engaged, clear-headed, and locked into a specific task.'),
('Normal', 2, 4, 'Coasting along; standard baseline day with no major highlights.'),
('Happy', 3, 5, 'Content, smiling, and experiencing a generally pleasant day.'),
('Grateful', 3, 5, 'Appreciative, warm, and focusing on the good things.'),
('Excited', 3, 6, 'Enthusiastic, eager, and looking forward to something.'),
('Proud', 3, 6, 'Feeling a strong sense of accomplishment or self-worth.'),
('Inspired', 3, 6, 'Creative, motivated, and full of fresh, positive ideas.'),
('Ecstatic', 3, 7, 'Overjoyed, on top of the world, and full of peak positive energy.'),
('Mixed Feelings', 4, 8, 'Experiencing a combination of good and bad emotions simultaneously.'),
('Hard to Tell', 4, 9, 'Feeling emotionally numb, detached, or simply unable to pinpoint a specific state.');

INSERT INTO WeatherOptions
VALUES
(1,'Sunny'),
(2,'Mostly Sunny'),
(3,'Hot & Scorching'),
(4,'Partly Cloudy'),
(5,'Mostly Cloudy'),
(6,'Overcast'),
(7,'Light Drizzle'),
(8,'Showers'),
(9,'Heavy Rain'),
(10,'Light Snow'),
(11,'Heavy Snow'),
(12,'Freezing Rain'),
(13,'Thunderstorm'),
(14,'Windy'),
(15,'Foggy / Misty');

INSERT INTO Users (Name, Email, Hashed_password, Created_at, Deleted_at)
VALUES
('Emma Smith', 'emma.smith@example.com', '$2b$12$e0MYzXy6D.GkP61R8NfhOexnK4L8y6b7u3v1c5x7z9q2w1e3r4t5y', '2026-04-01', NULL),
('Liam Johnson', 'liam.johnson@example.com', '$2b$12$K1v8NfhOexnK4L8y6b7u3v1c5x7z9q2w1e3r4t5ye0MYzXy6D.GkP6', '2026-05-01', NULL),
('Olivia Williams', 'olivia.williams@example.com', '$2b$12$3v1c5x7z9q2w1e3r4t5ye0MYzXy6D.GkP61R8NfhOexnK4L8y6b7u', '2026-04-15', NULL),
('Noah Brown', 'noah.brown@example.com', '$2b$12$q2w1e3r4t5ye0MYzXy6D.GkP61R8NfhOexnK4L8y6b7u3v1c5x7z9', '2026-04-18', '2026-04-30'),
('Ava Jones', 'ava.jones@example.com', '$2b$12$GkP61R8NfhOexnK4L8y6b7u3v1c5x7z9q2w1e3r4t5ye0MYzXy6D.', '2026-04-28', NULL),
('Oliver Miller', 'oliver.miller@example.com', '$2b$12$8NfhOexnK4L8y6b7u3v1c5x7z9q2w1e3r4t5ye0MYzXy6D.GkP61R', '2026-04-04', NULL),
('Sophia Davis', 'sophia.davis@example.com', '$2b$12$y6b7u3v1c5x7z9q2w1e3r4t5ye0MYzXy6D.GkP61R8NfhOexnK4L8', '2026-05-02', NULL),
('Elijah Garcia', 'elijah.garcia@example.com', '$2b$12$5x7z9q2w1e3r4t5ye0MYzXy6D.GkP61R8NfhOexnK4L8y6b7u3v1c', '2026-04-24', '2026-05-04'),
('Isabella Rodriguez', 'isabella.rodriguez@example.com', '$2b$12$e3r4t5ye0MYzXy6D.GkP61R8NfhOexnK4L8y6b7u3v1c5x7z9q2w1', '2026-04-05', NULL),
('James Wilson', 'james.wilson@example.com', '$2b$12$D.GkP61R8NfhOexnK4L8y6b7u3v1c5x7z9q2w1e3r4t5ye0MYzXy6', '2026-04-12', NULL);

INSERT INTO JournalEntries (User_id, Title, Content, Mood, Energy_level, Free_time, Weather, Created_at) 
VALUES
(1, 'Great start to the week', 'Woke up early and went for a run. The weather was beautiful and I feel incredibly productive today.', 11, 5, FALSE, 1, '2026-04-02 09:30:00'),
(1, 'A bit overwhelmed', 'Too many tasks at work today. Feeling a bit buried under pressure and my head hurts.', 5, 2, FALSE, 6, '2026-04-03 18:45:00'),
(6, 'Creative spark', 'Woke up with an awesome idea for my hobby project. Spent hours drafting it out.', 15, 6, TRUE, 1, '2026-04-05 13:15:00'),
(9, 'Bored out of my mind', 'Had literally nothing to do at the office today. Clicking around just trying to pass time.', 8, 2, FALSE, 5, '2026-04-06 15:00:00'),
(6, 'Exhausted after a long week', 'Friday night and I am completely dead. No energy to do anything but scroll on my phone.', 6, 1, TRUE, 6, '2026-04-10 20:45:00'),
(9, 'Perfect afternoon', 'Sat in the backyard garden all afternoon. The weather was amazing.', 11, 4, TRUE, 1, '2026-04-11 16:30:00'),
(10, 'Freezing day', 'The weather is terrible, icy sleet everywhere. Stayed inside and did chores.', 10, 3, FALSE, 12, '2026-04-14 14:00:00'),
(3, 'Feeling off today', 'Can barely keep my eyes open and everything is annoying me. Going to sleep early.', 6, 1, FALSE, 6, '2026-04-15 21:00:00'),
(9, 'Sad news', 'Found out my childhood pet passed away today. Heartbroken.', 4, 1, TRUE, 9, '2026-04-16 12:00:00'),
(3, 'Spring walk', 'The sunshine came out after a week of rain! Took a long walk through the park after work.', 11, 5, TRUE, 1, '2026-04-18 18:00:00'),
(10, 'Inspired to cook', 'Tried a brand new complex recipe tonight and it turned out incredible! Proud of myself.', 14, 5, TRUE, 6, '2026-04-20 20:15:00'),
(3, 'Anxious about tomorrow', 'Have a massive presentation tomorrow morning and my stomach is in knots. Trying to calm down.', 3, 4, FALSE, 8, '2026-04-22 22:10:00'),
(3, 'Celebration!', 'The presentation went flawlessly! Everyone loved it. Celebrating with a nice dinner tonight.', 13, 7, TRUE, 2, '2026-04-23 19:45:00'),
(1, 'Rainy weekend relaxation', 'Spent the whole afternoon reading on the couch while it poured outside. Exactly what I needed.', 7, 3, TRUE, 9, '2026-04-26 15:00:00'),
(10, 'Running on empty', 'Stayed up way too late watching a show and paid the price at work today. Struggling to stay awake.', 6, 1, FALSE, 5, '2026-04-28 13:00:00'),
(5, 'Just a normal day', 'Nothing special happened today. Work was fine, traffic was fine, dinner was fine. Standard.', 10, 4, FALSE, 4, '2026-04-29 17:00:00'),
(2, 'Super lazy Sunday', 'Literally did nothing today. Slept in, ordered pizza, and watched movies. Total couch potato vibes.', 10, 2, TRUE, 6, '2026-05-03 20:00:00'),
(7, 'Fresh start', 'First day tracking my habits again. Feeling optimistic and steady.', 11, 4, FALSE, 2, '2026-05-03 08:00:00'),
(2, 'Midweek focus', 'Completely locked into my code today. Had great flow and zero distractions.', 9, 6, FALSE, 5, '2026-05-06 17:30:00'),
(7, 'Gym motivation', 'Had a crazy good workout session today. Felt like I could lift a house.', 13, 7, TRUE, 1, '2026-05-07 19:30:00'),
(5, 'Stormy evening', 'Massive thunderstorm tonight. Watching the lightning from the window with a hot cup of tea.', 7, 3, TRUE, 13, '2026-05-10 22:30:00'),
(6, 'Cozy and quiet', 'It''s snowing outside nicely. Cleaned up the apartment and enjoying the quiet space.', 7, 4, TRUE, 10, '2026-05-11 11:00:00'),
(2, 'Frustrated', 'Spilled coffee on my laptop and argued with support. Just a genuinely annoying day.', 2, 3, FALSE, 14, '2026-05-12 11:15:00'),
(7, 'Stressed over deadlines', 'Too much on my plate and not enough hours in the day. Brain feels fried.', 5, 2, FALSE, 6, '2026-05-12 16:00:00'),
(1, 'Bittersweet evening', 'Had a long talk with an old friend moving away. Happy for them but sad they are leaving.', 17, 3, TRUE, 5, '2026-05-15 21:15:00'),
(5, 'Blah', 'I don''t even know how I feel today. Not sad, not happy, just completely blank and emotionally flat.', 18, 2, FALSE, 15, '2026-05-16 14:00:00'),
(7, 'Grateful for small things', 'Someone paid for my coffee today. It really turned my whole mood around.', 12, 5, FALSE, 2, '2026-05-18 10:30:00'),
(6, 'Angry at the traffic', 'Commute took two hours because of a minor accident. Ruined my whole morning mood.', 2, 5, FALSE, 7, '2026-05-22 09:15:00'),
(7, 'Mixed up day', 'Got some great news about a promotion, but a close coworker announced they are quitting.', 17, 4, FALSE, 4, '2026-05-24 15:45:00'),
(1, 'Crushing my goals', 'Finished the big project layout ahead of schedule. On absolute top of the world right now!', 16, 6, FALSE, 2, '2026-05-25 16:20:00'),
(10, 'Unstoppable mood', 'Got a great night of sleep, sun is shining, feeling absolutely radiant today.', 16, 7, TRUE, 1, '2026-05-29 09:00:00');

INSERT INTO Recommendations (Entry_id, Recommendation_text, Created_at, Deleted_at)
VALUES 
(1, 'Great momentum! Consider scheduling your next workout to keep this streak going.', '2026-04-02 09:35:00', '2026-04-02 23:59:59'),
(2, 'When feeling overwhelmed, try taking a 5-minute breathing break away from your screen.', '2026-04-03 18:50:00', '2026-04-03 23:59:59'),
(3, 'A creative spark is rare! Capture these ideas in a brainstorm file before the energy fades.', '2026-04-05 13:20:00', '2026-04-05 23:59:59'),
(4, 'Since you have a bit of quiet time at the office, look into that short online course you saved.', '2026-04-06 15:05:00', '2026-04-06 23:59:59'),
(5, 'Low energy on a Friday night is your body asking for rest. Turn off screens 30 mins before bed.', '2026-04-10 20:50:00', '2026-04-10 23:59:59'),
(6, 'Perfect day for a walk or outdoor reading session. Enjoy the sunshine!', '2026-04-11 16:35:00', '2026-04-11 23:59:59'),
(7, 'Since you are stuck inside with the sleet, it is a great time to tackle a small indoor project.', '2026-04-14 14:05:00', '2026-04-14 23:59:59'),
(8, 'Listen to your body. Drink a warm glass of water and try to aim for 8 hours of sleep tonight.', '2026-04-15 21:05:00', '2026-04-15 23:59:59'),
(9, 'Be gentle with yourself today. It is completely okay to step back and process your emotions.', '2026-04-16 12:05:00', '2026-04-16 23:59:59'),
(10, 'Enjoy the pleasant weather! Maybe take your evening tea or coffee outside to unwind.', '2026-04-18 18:05:00', '2026-04-18 23:59:59'),
(11, 'Awesome job cooking! Try packing the leftovers now so you have a healthy lunch ready for tomorrow.', '2026-04-20 20:20:00', '2026-04-20 23:59:59'),
(12, 'Pre-presentation anxiety is normal. Try a quick guided meditation to stop overthinking.', '2026-04-22 22:15:00', '2026-04-22 23:59:59'),
(13, 'Celebrate your win! Treat yourself to something small tonight to reward your hard work.', '2026-04-23 19:50:00', '2026-04-23 23:59:59'),
(14, 'Rainy days are perfect for listening to a new podcast or starting a cozy fiction book.', '2026-04-26 15:05:00', '2026-04-26 23:59:59'),
(15, 'Late-night screen time caught up to you. Try setting an alarm tonight to remind you to log off.', '2026-04-28 13:05:00', '2026-04-28 23:59:59'),
(16, 'A baseline day is a great canvas. Write down one small goal you want to achieve tomorrow.', '2026-04-29 17:05:00', '2026-04-29 23:59:59'),
(17, 'Enjoy the lazy day completely guilt-free! True rest is highly productive for your mental health.', '2026-05-03 20:05:00', '2026-05-03 23:59:59'),
(18, 'Starting fresh feels great. Pick your top 3 habits to focus on this week and ignore the rest.', '2026-05-03 08:05:00', '2026-05-03 23:59:59'),
(19, 'You are in the zone! Capitalize on this deep focus block before taking a solid break.', '2026-05-06 17:35:00', '2026-05-06 23:59:59'),
(20, 'Incredible workout! Make sure to stretch well and refuel with a high-protein meal.', '2026-05-07 19:35:00', '2026-05-07 23:59:59'),
(21, 'The sound of a thunderstorm is great for relaxation. Put on some soothing music and stretch.', '2026-05-10 22:35:00', '2026-05-10 23:59:59'),
(22, 'Snowy days call for comfort. Put on your favorite warm sweater and enjoy a hot soup.', '2026-05-11 11:05:00', '2026-05-11 23:59:59'),
(23, 'Spilling coffee is frustrating, but don''t let it ruin the whole day. Step away for a fresh beverage.', '2026-05-12 11:20:00', '2026-05-12 23:59:59'),
(24, 'When deadlines pile up, block out 1 hour of deep work on just ONE single task to gain control.', '2026-05-12 16:05:00', '2026-05-12 23:59:59'),
(25, 'Mixed emotions are part of life change. Write down three things you are happy about to ground yourself.', '2026-05-15 21:20:00', '2026-05-15 23:59:59'),
(26, 'Feeling flat happens. Don''t force a mood; instead, focus on a simple physical comfort like a hot bath.', '2026-05-16 14:05:00', '2026-05-16 23:59:59'),
(27, 'Kindness from strangers is beautiful. Pay it forward today by offering someone a sincere compliment.', '2026-05-18 10:35:00', '2026-05-18 23:59:59'),
(28, 'Traffic frustration is a heavy burden. Put on an interesting audiobook next time to distract your mind.', '2026-05-22 09:20:00', '2026-05-22 23:59:59'),
(29, 'Big transitions bring waves of different feelings. Give yourself permission to feel both proud and sad.', '2026-05-24 15:50:00', '2026-05-24 23:59:59'),
(30, 'You are absolutely crushing it! Take a moment to write down what exactly went right so you can copy it later.', '2026-05-25 16:25:00', '2026-05-25 23:59:59'),
(31, 'When you feel this radiant, it is highly contagious. Use this energy to reach out and uplift a friend.', '2026-05-29 09:05:00', '2026-05-29 23:59:59');
