-- Option with insert all data to JournalEntries table

CREATE DATABASE IF NOT EXISTS KindMind;

USE KindMind;

CREATE TABLE IF NOT EXISTS users (
user_id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(100) NOT NULL,
email VARCHAR(100) UNIQUE NOT NULL,
hashed_password VARCHAR(255) NOT NULL,
created_at DATE NOT NULL,
deleted_at DATE
);

CREATE TABLE IF NOT EXISTS mood_category (
category_id INT PRIMARY KEY AUTO_INCREMENT,
category_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS mood_score (
score_id INT PRIMARY KEY AUTO_INCREMENT,
score_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS energy_level (
energy_id INT PRIMARY KEY AUTO_INCREMENT,
energy_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS journal_entries (
entry_id INT PRIMARY KEY AUTO_INCREMENT,
user_id INT NOT NULL,
FOREIGN KEY (user_id)
REFERENCES users(user_id) ON DELETE CASCADE,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
title VARCHAR(100) NOT NULL,
content TEXT NOT NULL,
energy_level INT NOT NULL,
FOREIGN KEY (energy_level)
REFERENCES energy_level(energy_id),
free_time BOOLEAN NOT NULL,
mood INT NOT NULL,
FOREIGN KEY (mood)
REFERENCES mood_score(score_id),
city VARCHAR(100), -- We need to decide if city, temperature and weather must be completed, or if they can be empty
temperature DECIMAL(4,1), -- Added for future API integration to allow filtering/searching journal entries by weather/temperature
weather VARCHAR(100)
);


-- =========================================================
-- 02- KINDMIND MOCK DATA
-- =========================================================

INSERT IGNORE INTO energy_level
VALUES
(1,'Drained'),
(2,'Sluggish'),
(3,'Mellow'),
(4,'Steady'),
(5,'Vibrant'),
(6,'Driven'),
(7,'Radiant');


INSERT IGNORE INTO mood_category
VALUES
(1,'Negative'),
(2,'Neutral'),
(3,'Positive'),
(4,'Ambiguous');

INSERT IGNORE INTO mood_score
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

INSERT IGNORE INTO users (name, email, hashed_password, created_at, deleted_at)
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

-- Changes in data to make
INSERT IGNORE INTO journal_entries (user_id, created_at, title, content, energy_level, free_time, mood, city, temperature, weather)
VALUES
(1, '2026-04-02 09:30:00', 'Great start to the week', 'Woke up early and went for a run. The weather was beautiful and I feel incredibly productive today.', 5, FALSE, 1, NULL, NULL, NULL),
(1, '2026-04-03 18:45:00', 'A bit overwhelmed', 'Too many tasks at work today. Feeling a bit buried under pressure and my head hurts.', 2, FALSE, 6, NULL, NULL, NULL),
(6, '2026-04-05 13:15:00', 'Creative spark', 'Woke up with an awesome idea for my hobby project. Spent hours drafting it out.', 6, TRUE, 1, NULL, NULL, NULL),
(9, '2026-04-06 15:00:00', 'Bored out of my mind', 'Had literally nothing to do at the office today. Clicking around just trying to pass time.', 2, FALSE, 5, NULL, NULL, NULL),
(6, '2026-04-10 20:45:00', 'Exhausted after a long week', 'Friday night and I am completely dead. No energy to do anything but scroll on my phone.', 1, TRUE, 6, NULL, NULL, NULL),
(9, '2026-04-11 16:30:00', 'Perfect afternoon', 'Sat in the backyard garden all afternoon. The weather was amazing.', 4, TRUE, 1, NULL, NULL, NULL),
(10, '2026-04-14 14:00:00', 'Freezing day', 'The weather is terrible, icy sleet everywhere. Stayed inside and did chores.', 3, FALSE, 12, NULL, NULL, NULL),
(3, '2026-04-15 21:00:00', 'Feeling off today', 'Can barely keep my eyes open and everything is annoying me. Going to sleep early.', 1, FALSE, 6, NULL, NULL, NULL),
(9, '2026-04-16 12:00:00', 'Sad news', 'Found out my childhood pet passed away today. Heartbroken.', 1, TRUE, 9, NULL, NULL, NULL),
(3, '2026-04-18 18:00:00', 'Spring walk', 'The sunshine came out after a week of rain! Took a long walk through the park after work.', 5, TRUE, 1, NULL, NULL, NULL),
(10, '2026-04-20 20:15:00', 'Inspired to cook', 'Tried a brand new complex recipe tonight and it turned out incredible! Proud of myself.', 5, TRUE, 6, NULL, NULL, NULL),
(3, '2026-04-22 22:10:00', 'Anxious about tomorrow', 'Have a massive presentation tomorrow morning and my stomach is in knots. Trying to calm down.', 4, FALSE, 8, NULL, NULL, NULL),
(3, '2026-04-23 19:45:00', 'Celebration!', 'The presentation went flawlessly! Everyone loved it. Celebrating with a nice dinner tonight.', 7, TRUE, 2, NULL, NULL, NULL),
(1, '2026-04-26 15:00:00', 'Rainy weekend relaxation', 'Spent the whole afternoon reading on the couch while it poured outside. Exactly what I needed.', 3, TRUE, 9, NULL, NULL, NULL),
(10, '2026-04-28 13:00:00', 'Running on empty', 'Stayed up way too late watching a show and paid the price at work today. Struggling to stay awake.', 1, FALSE, 5, NULL, NULL, NULL),
(5, '2026-04-29 17:00:00', 'Just a normal day', 'Nothing special happened today. Work was fine, traffic was fine, dinner was fine. Standard.', 4, FALSE, 4, NULL, NULL, NULL),
(2, '2026-05-03 20:00:00', 'Super lazy Sunday', 'Literally did nothing today. Slept in, ordered pizza, and watched movies. Total couch potato vibes.', 2, TRUE, 6, NULL, NULL, NULL),
(7, '2026-05-03 08:00:00', 'Fresh start', 'First day tracking my habits again. Feeling optimistic and steady.', 4, FALSE, 2, NULL, NULL, NULL),
(2, '2026-05-06 17:30:00', 'Midweek focus', 'Completely locked into my code today. Had great flow and zero distractions.', 6, FALSE, 5, NULL, NULL, NULL),
(7, '2026-05-07 19:30:00', 'Gym motivation', 'Had a crazy good workout session today. Felt like I could lift a house.', 7, TRUE, 1, NULL, NULL, NULL),
(5, '2026-05-10 22:30:00', 'Stormy evening', 'Massive thunderstorm tonight. Watching the lightning from the window with a hot cup of tea.', 3, TRUE, 13, NULL, NULL, NULL),
(6, '2026-05-11 11:00:00', 'Cozy and quiet', 'It''s snowing outside nicely. Cleaned up the apartment and enjoying the quiet space.', 4, TRUE, 10, NULL, NULL, NULL),
(2, '2026-05-12 11:15:00', 'Frustrated', 'Spilled coffee on my laptop and argued with support. Just a genuinely annoying day.', 3, FALSE, 14, NULL, NULL, NULL),
(7, '2026-05-12 16:00:00', 'Stressed over deadlines', 'Too much on my plate and not enough hours in the day. Brain feels fried.', 2, FALSE, 6, NULL, NULL, NULL),
(1, '2026-05-15 21:15:00', 'Bittersweet evening', 'Had a long talk with an old friend moving away. Happy for them but sad they are leaving.', 3, TRUE, 5, NULL, NULL, NULL),
(5, '2026-05-16 14:00:00', 'Blah', 'I don''t even know how I feel today. Not sad, not happy, just completely blank and emotionally flat.', 2, FALSE, 15, NULL, NULL, NULL),
(7, '2026-05-18 10:30:00', 'Grateful for small things', 'Someone paid for my coffee today. It really turned my whole mood around.', 5, FALSE, 2, NULL, NULL, NULL),
(6, '2026-05-22 09:15:00', 'Angry at the traffic', 'Commute took two hours because of a minor accident. Ruined my whole morning mood.', 5, FALSE, 7, NULL, NULL, NULL),
(7, '2026-05-24 15:45:00', 'Mixed up day', 'Got some great news about a promotion, but a close coworker announced they are quitting.', 4, FALSE, 4, NULL, NULL, NULL),
(1, '2026-05-25 16:20:00', 'Crushing my goals', 'Finished the big project layout ahead of schedule. On absolute top of the world right now!', 6, FALSE, 2, NULL, NULL, NULL),
(10, '2026-05-29 09:00:00', 'Unstoppable mood', 'Got a great night of sleep, sun is shining, feeling absolutely radiant today.', 7, TRUE, 1, NULL, NULL, NULL);


-- =========================================================
-- SECTION 3 ONWARDS - MOODBOARD QUERIES MARRIED TO MAGDA'S SETUP
-- =========================================================

-- =========================================================
-- 03 - KINDMIND MOODBOARD QUERIES
-- =========================================================
-- Purpose:
--   1. Create reusable MoodBoard queries for the KindMind journal system.
--   2. Use functions, a view, and stored procedures to keep the Flask API clean.
--   3. Focus on journal history, mood summaries, search/sort, recommendations,
--      and simple wellbeing insights.
--
-- Notes:
--   Each query includes a short "Why" comment to explain its practical purpose
--   in the KindMind app.
--
--   The main app does not need to run every single analysis query. The Flask API
--   should mainly call the stored procedures and the MoodBoardView.
--
--   The final section contains optional showcase queries for DBeaver, the report,
--   or the presentation.
--
--   These queries avoid MySQL 8-only window functions such as LAG() and ROW_NUMBER().
--   This should make the file safer to run in DBeaver even if the database version
--   is older.
--
--   The wording is kept non-medical. The app describes mood patterns and gentle
--   support ideas, not diagnoses.
-- =========================================================


-- =========================================================
-- HOW TO RUN THIS SECTION
-- =========================================================
-- Run this after:
--   1. Creating the KindMind database and tables.
--   2. Inserting the lookup data and mock data.
--
-- In DBeaver, you can:
--   1. Highlight one query and run it with Ctrl + Enter, or
--   2. Run the full script using Alt + X.
--
-- Stored procedures can be a bit picky in SQL editors because they use multiple
-- statements. If DBeaver complains, run each stored procedure block separately.
-- =========================================================

USE KindMind;


-- =========================================================
-- USER-DEFINED FUNCTIONS
-- =========================================================

-- ---------------------------------------------------------
-- Get Mood Score Label FUNCTION
-- ---------------------------------------------------------
-- Groups mood score IDs into readable labels.
-- Why: the MoodScore table stores values like Terrible, Bad, Ok, Good, etc.
-- This function turns those scores into broader labels that are easier to
-- display in a MoodBoard summary.
DROP FUNCTION IF EXISTS get_mood_score_label;

DELIMITER //

CREATE FUNCTION get_mood_score_label(input_score_id INT)
RETURNS VARCHAR(80)
DETERMINISTIC
BEGIN
    RETURN CASE
        WHEN input_score_id = 1 THEN 'Very difficult mood'
        WHEN input_score_id IN (2, 3) THEN 'Low or pressured mood'
        WHEN input_score_id = 4 THEN 'Neutral or steady mood'
        WHEN input_score_id IN (5, 6, 7) THEN 'Positive mood'
        WHEN input_score_id = 8 THEN 'Mixed mood'
        WHEN input_score_id = 9 THEN 'Unclear mood'
        ELSE 'Mood score unavailable'
    END;
END //

DELIMITER ;


-- ---------------------------------------------------------
-- Get Energy Support Label FUNCTION
-- ---------------------------------------------------------
-- Groups energy levels into support labels.
-- Why: this helps the app explain whether a user may benefit from a gentle,
-- balanced, or more active recommendation.
DROP FUNCTION IF EXISTS get_energy_support_label;

DELIMITER //

CREATE FUNCTION get_energy_support_label(input_energy_id INT)
RETURNS VARCHAR(100)
DETERMINISTIC
BEGIN
    RETURN CASE
        WHEN input_energy_id IN (1, 2) THEN 'Low energy - suggest gentle option'
        WHEN input_energy_id IN (3, 4) THEN 'Moderate energy - suggest balanced option'
        WHEN input_energy_id >= 5 THEN 'Higher energy - suggest active option'
        ELSE 'Energy unavailable'
    END;
END //

DELIMITER ;


-- ---------------------------------------------------------
-- Get Free Time Label FUNCTION
-- ---------------------------------------------------------
-- Converts the Free_time boolean into a readable label.
-- Why: the current table stores free time as TRUE/FALSE, but a readable label
-- makes the console output and dashboard easier to understand.
DROP FUNCTION IF EXISTS get_free_time_label;

DELIMITER //

CREATE FUNCTION get_free_time_label(input_free_time BOOLEAN)
RETURNS VARCHAR(80)
DETERMINISTIC
BEGIN
    RETURN CASE
        WHEN input_free_time = TRUE THEN 'Free time available'
        WHEN input_free_time = FALSE THEN 'Limited free time'
        ELSE 'Free time unknown'
    END;
END //

DELIMITER ;


-- =========================================================
-- REUSABLE VIEW
-- =========================================================

-- ---------------------------------------------------------
-- MoodBoard View
-- ---------------------------------------------------------
-- Joins the main journal, mood, energy, weather, user, and recommendation data.
-- Why: this avoids repeating the same long JOINs in every query or Flask route.
-- The Flask API can query MoodBoardView directly, almost like a normal table.
DROP VIEW IF EXISTS mood_board_view;

CREATE VIEW mood_board_view AS
SELECT
    u.user_id AS user_id,
    u.name AS user_name,
    u.email AS email,

    je.entry_id AS entry_id,
    je.created_at AS created_at,
    je.title AS title,
    je.content AS content,

    mo.mood_id AS mood_id,
    mo.mood_name AS mood_name, -- Aamna can you please check it?

    mc.category_id AS category_id,
    mc.category_name AS category_name,

    ms.score_id AS score_id,
    ms.score_name AS score_name,
    get_mood_score_label(ms.score_id) AS mood_score_label,

    el.energy_id AS energy_id,
    el.energy_name AS energy_name,
    get_energy_support_label(el.energy_id) AS energy_support_label,

    je.free_time AS free_time,
    get_free_time_label(je.free_time) AS free_time_label,
-- please add city and temperature
    wo.weather_id AS weather_id,
    wo.weather_name AS weather_name,

    --COUNT(r.recommendation_id) AS recommendation_count,

    --SUM(
    --    CASE
    --        WHEN r.deleted_at IS NULL
    --             AND r.recommendation_id IS NOT NULL
   --             THEN 1
     --       ELSE 0
    --    END
   -- ) AS active_recommendation_count

FROM journal_entries je

INNER JOIN users u
    ON je.user_id = u.user_id

INNER JOIN mood_options mo
    ON je.mood = mo.mood_id

INNER JOIN mood_category mc
    ON mo.mood_category = mc.category_id

INNER JOIN mood_score ms
    ON mo.mood_score = ms.score_id

INNER JOIN energy_level el
    ON je.energy_level = el.energy_id

INNER JOIN weather_options wo
    ON je.weather = wo.weather_id

--LEFT JOIN recommendations r
--    ON je.entry_id = r.entry_id

-- Deleted_at is being treated as a soft delete.
-- This keeps deleted users out of the main dashboard view.
WHERE u.deleted_at IS NULL

GROUP BY
    u.user_id,
    u.name,
    u.email,
    je.entry_id,
    je.created_at,
    je.title,
    je.content,
    mo.mood_id,
    mo.mood_name,
    mc.category_id,
    mc.category_name,
    ms.score_id,
    ms.score_name,
    el.energy_id,
    el.energy_name,
    je.free_time,
    wo.weather_id,
    wo.weather_name;


-- =========================================================
-- CORE APP STORED PROCEDURES
-- =========================================================
-- These are the procedures the Flask API should actually call.
-- They keep the app focused and stop the API file from filling up with
-- long SQL queries.
-- =========================================================

DROP PROCEDURE IF EXISTS get_user_mood_history;
DROP PROCEDURE IF EXISTS search_user_entries;
DROP PROCEDURE IF EXISTS get_user_mood_summary;
DROP PROCEDURE IF EXISTS get_user_moodboard_overview;
--DROP PROCEDURE IF EXISTS get_user_recommendations;

DELIMITER //


-- ---------------------------------------------------------
-- Get User Mood History PROCEDURE
-- ---------------------------------------------------------
-- Returns all journal entries for one user.
-- Why: supports the console option "View my entries".
CREATE PROCEDURE get_user_mood_history(IN input_user_id INT)
BEGIN
    SELECT
        entry_id,
        created_at,
        title,
        content,
        mood_name,
        score_name,
        category_name,
        mood_score_label,
        energy_name,
        energy_support_label,
        free_time_label,
        weather_name,
        recommendation_count
    FROM mood_board_view
    WHERE user_id = input_user_id
    ORDER BY created_at DESC;
END //


-- ---------------------------------------------------------
-- Search User Entries PROCEDURE
-- ---------------------------------------------------------
-- Searches a user's journal entries by keyword and optional mood.
-- Why: this is the main specialist topic feature. It demonstrates search/sort
-- using stored data, while still being useful in the console app.
CREATE PROCEDURE search_user_entries(
    IN input_user_id INT,
    IN input_keyword VARCHAR(255),
    IN input_mood_name VARCHAR(100),
    IN input_sort_order VARCHAR(10)
)
BEGIN
    SELECT
        entry_id,
        created_at,
        title,
        content,
        mood_name,
        category_name,
        score_name,
        energy_name,
        free_time_label,
        weather_name
    FROM mood_board_view
    WHERE user_id = input_user_id

      AND (
          input_keyword IS NULL
          OR input_keyword = ''
          OR LOWER(title) LIKE CONCAT('%', LOWER(input_keyword), '%')
          OR LOWER(content) LIKE CONCAT('%', LOWER(input_keyword), '%')
      )

      AND (
          input_mood_name IS NULL
          OR input_mood_name = ''
          OR LOWER(mood_name) = LOWER(input_mood_name)
      )

    ORDER BY
        CASE
            WHEN LOWER(input_sort_order) = 'oldest'
                THEN created_at
        END ASC,

        CASE
            WHEN LOWER(input_sort_order) <> 'oldest'
                THEN created_at
        END DESC;
END //


-- ---------------------------------------------------------
-- Get User Mood Summary PROCEDURE
-- ---------------------------------------------------------
-- Counts how often a user has logged each mood.
-- Why: supports the console option "View mood summary" and gives the user
-- a simple overview of their mood patterns.
CREATE PROCEDURE get_user_mood_summary(IN input_user_id INT)
BEGIN
    SELECT
        mood_name,
        category_name,
        score_name,
        COUNT(*) AS total_entries,
        ROUND(AVG(score_id), 2) AS average_score_id,
        ROUND(AVG(energy_id), 2) AS average_energy_id,
        MIN(created_at) AS first_entry,
        MAX(created_at) AS latest_entry
    FROM mood_board_view
    WHERE user_id = input_user_id
    GROUP BY
        mood_name,
        category_name,
        score_name
    ORDER BY
        total_entries DESC,
        average_score_id ASC;
END //


-- ---------------------------------------------------------
-- Get User MoodBoard Overview PROCEDURE
-- ---------------------------------------------------------
-- Returns a one-row dashboard summary for one user.
-- Why: this gives the console app a simple MoodBoard overview without needing
-- several separate queries.
CREATE PROCEDURE get_user_moodboard_overview(IN input_user_id INT)
BEGIN
    SELECT
        user_id,
        user_name,
        COUNT(entry_id) AS total_entries,
        ROUND(AVG(score_id), 2) AS average_score_id,
        ROUND(AVG(energy_id), 2) AS average_energy_id,

        SUM(CASE WHEN category_name = 'Positive' THEN 1 ELSE 0 END) AS positive_entries,
        SUM(CASE WHEN category_name = 'Neutral' THEN 1 ELSE 0 END) AS neutral_entries,
        SUM(CASE WHEN category_name = 'Negative' THEN 1 ELSE 0 END) AS negative_entries,
        SUM(CASE WHEN category_name = 'Ambiguous' THEN 1 ELSE 0 END) AS ambiguous_entries,

        MAX(created_at) AS latest_entry,

        CASE
            WHEN AVG(score_id) <= 3
                 AND AVG(energy_id) <= 2
                THEN 'Gentle support may be helpful.'
            WHEN SUM(CASE WHEN category_name = 'Negative' THEN 1 ELSE 0 END) >= 3
                THEN 'Several challenging check-ins logged.'
            WHEN AVG(score_id) >= 5
                THEN 'Mostly positive pattern in this sample.'
            ELSE 'Mixed or steady mood pattern.'
        END AS supportive_summary

    FROM mood_board_view
    WHERE user_id = input_user_id
    GROUP BY
        user_id,
        user_name;
END //


-- ---------------------------------------------------------
-- Get User Recommendations PROCEDURE
-- ---------------------------------------------------------
-- Returns recommendations linked to one user's journal entries.
-- Why: supports the console option "View recommendations" and lets the user
-- see what suggestions were generated from their check-ins.


--CREATE PROCEDURE GetUserRecommendations(IN input_user_id INT)
--BEGIN
--    SELECT
--        mbv.created_at AS entry_created_at,
--        mbv.title AS entry_title,
--        mbv.mood_name,
--        mbv.energy_name,
--        mbv.weather_name,
--        r.Recommendation_id AS recommendation_id,
--        r.Recommendation_text AS recommendation_text,
--        r.Created_at AS recommendation_created_at,
--        r.Deleted_at AS deleted_at
--    FROM Recommendations r
--
--    INNER JOIN JournalEntries je
--        ON r.Entry_id = je.Entry_id
--
--    INNER JOIN MoodBoardView mbv
--        ON je.Entry_id = mbv.entry_id
--
--    WHERE mbv.user_id = input_user_id
--    ORDER BY
--        r.Created_at DESC;
--END //
--
--DELIMITER ;


-- =========================================================
-- CORE APP TEST CALLS
-- =========================================================
-- These are the calls the group can test in DBeaver before connecting
-- them to the Flask API.
-- =========================================================

CALL get_user_mood_history(1);

CALL search_user_entries(1, 'stress', '', 'newest');

CALL get_user_mood_summary(1);

CALL get_user_moodboard_overview(1);

--CALL get_user_recommendations(1);


-- =========================================================
-- OPTIONAL SHOWCASE QUERIES
-- =========================================================
-- These are not all needed in the console app.
-- They are useful for the report, screenshots, presentation, or future
-- dashboard ideas.
-- =========================================================


-- ---------------------------------------------------------
-- QUERY 1: User Journaling Overview
-- ---------------------------------------------------------
-- Shows who has journaled most and what their average mood/energy scores are.
-- Why: gives a quick overview of engagement across users.
SELECT
    user_name AS `User`,
    COUNT(entry_id) AS `Total Entries`,
    MIN(created_at) AS `First Entry`,
    MAX(created_at) AS `Latest Entry`,
    ROUND(AVG(score_id), 2) AS `Average Mood Score ID`,
    ROUND(AVG(energy_id), 2) AS `Average Energy ID`
FROM mood_board_view
GROUP BY
    user_id,
    user_name
ORDER BY
    `Total Entries` DESC;


-- ---------------------------------------------------------
-- QUERY 2: Mood Frequency by User
-- ---------------------------------------------------------
-- Shows how many times each user has logged each mood.
-- Why: helps identify repeated patterns, such as often logging Stressed,
-- Tired, Happy, or Calm.
SELECT
    user_name AS `User`,
    mood_name AS `Mood`,
    category_name AS `Mood Category`,
    score_name AS `Mood Score`,
    COUNT(*) AS `Times Logged`
FROM mood_board_view
GROUP BY
    user_id,
    user_name,
    mood_name,
    category_name,
    score_name
ORDER BY
    user_name,
    `Times Logged` DESC;


-- ---------------------------------------------------------
-- QUERY 3: Overall Mood Distribution
-- ---------------------------------------------------------
-- Shows which moods appear most often across all journal entries.
-- Why: useful for a report chart or presentation screenshot.
SELECT
    mood_name AS `Mood`,
    category_name AS `Mood Category`,
    score_name AS `Mood Score`,
    COUNT(*) AS `Total Entries`,
    ROUND(
        100 * COUNT(*) / NULLIF((SELECT COUNT(*) FROM JournalEntries), 0),
        2
    ) AS `Percentage of All Entries`
FROM mood_board_view
GROUP BY
    mood_name,
    category_name,
    score_name
ORDER BY
    `Total Entries` DESC;


-- ---------------------------------------------------------
-- QUERY 4: Weather and Mood Pattern
-- ---------------------------------------------------------
-- Groups entries by weather and compares average mood/energy scores.
-- Why: supports the Weather API part of the project and gives the group a
-- data engineering angle.
--
-- Note: this shows association only, not causation.
SELECT
    weather_name AS `Weather`,
    COUNT(*) AS `Entries`,
    ROUND(AVG(score_id), 2) AS `Average Mood Score ID`,
    ROUND(AVG(energy_id), 2) AS `Average Energy ID`
FROM mood_board_view
GROUP BY
    weather_name
ORDER BY
    `Average Mood Score ID` DESC,
    `Entries` DESC;


-- ---------------------------------------------------------
-- QUERY 5: Entries Where Gentle Support May Be Useful
-- ---------------------------------------------------------
-- Finds entries with lower mood scores or lower energy levels.
-- Why: helps explain how journal data can connect to recommendations.
SELECT
    user_name AS `User`,
    created_at AS `Date`,
    title AS `Entry Title`,
    mood_name AS `Mood`,
    score_name AS `Mood Score`,
    energy_name AS `Energy`,
    energy_support_label AS `Energy Support Label`,
    weather_name AS `Weather`,
    CASE
        WHEN score_id <= 2
             AND energy_id <= 2
            THEN 'High support - very gentle suggestion'
        WHEN score_id <= 3
             OR energy_id <= 2
            THEN 'Medium support - low effort suggestion'
        ELSE 'Standard reflection'
    END AS `Support Flag`
FROM mood_board_view
WHERE score_id <= 3
   OR energy_id <= 2
ORDER BY
    score_id ASC,
    energy_id ASC,
    created_at DESC;


-- ---------------------------------------------------------
-- QUERY 6: Weekly Journaling Frequency
-- ---------------------------------------------------------
-- Counts entries per user per week.
-- Why: helps show journaling consistency over time.
SELECT
    user_name AS `User`,
    YEARWEEK(created_at, 1) AS `Year Week`,
    COUNT(*) AS `Entries This Week`,
    ROUND(AVG(score_id), 2) AS `Average Mood Score ID`,
    ROUND(AVG(energy_id), 2) AS `Average Energy ID`
FROM mood_board_view
GROUP BY
    user_id,
    user_name,
    YEARWEEK(created_at, 1)
ORDER BY
    `Year Week`,
    user_name;


-- ---------------------------------------------------------
-- QUERY 7: Free Time and Mood Pattern
-- ---------------------------------------------------------
-- Compares mood and energy depending on whether the user had free time.
-- Why: useful for checking whether limited time appears alongside lower mood
-- or lower energy in the sample data.
SELECT
    free_time_label AS `Free Time`,
    COUNT(*) AS `Total Entries`,
    ROUND(AVG(score_id), 2) AS `Average Mood Score ID`,
    ROUND(AVG(energy_id), 2) AS `Average Energy ID`
FROM mood_board_view
GROUP BY
    free_time_label
ORDER BY
    `Total Entries` DESC;

-- ---------------------------------------------------------
-- QUERY 8: Latest Entry Per User
-- ---------------------------------------------------------
-- Finds the latest journal entry for each user without using ROW_NUMBER().
-- Why: useful for a simple "latest check-in" dashboard idea while avoiding
-- MySQL 8-only window functions.
SELECT
    mbv.user_name AS `User`,
    mbv.created_at AS `Latest Entry Date`,
    mbv.title AS `Latest Entry Title`,
    mbv.mood_name AS `Mood`,
    mbv.energy_name AS `Energy`,
    mbv.weather_name AS `Weather`
FROM mood_board_view mbv

INNER JOIN (
    SELECT
        user_id,
        MAX(created_at) AS latest_entry
    FROM mood_board_view
    GROUP BY user_id
) latest
    ON mbv.user_id = latest.user_id
   AND mbv.created_at = latest.latest_entry

ORDER BY
    mbv.created_at DESC;

