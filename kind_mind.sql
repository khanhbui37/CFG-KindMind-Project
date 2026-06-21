-- =========================================================
-- KindMind Database Setup
-- Cleaned to match the current main / khanh cleanup structure
-- =========================================================
-- Notes:
-- - Uses lowercase snake_case table and column names.
-- - Removes MoodOptions, WeatherOptions, and separate Recommendations table.
-- - Stores OpenWeather result directly in journal_entries.weather as text.
-- - Stores recommendation text directly in journal_entries.recommendations.
-- - This script recreates the local development database.
-- =========================================================

DROP DATABASE IF EXISTS kindMind;
CREATE DATABASE kindMind;
USE kindMind;

-- =========================================================
-- 01 - TABLES
-- =========================================================

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE mood_category (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE mood_score (
    score_id INT PRIMARY KEY AUTO_INCREMENT,
    score_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE energy_level (
    energy_id INT PRIMARY KEY AUTO_INCREMENT,
    energy_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE journal_entries (
    entry_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    mood_category_id INT NOT NULL,
    mood_score_id INT NOT NULL,
    energy_level_id INT NOT NULL,
    free_time BOOLEAN NOT NULL,
    weather VARCHAR(50) NOT NULL,
    recommendations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE CASCADE,

    FOREIGN KEY (mood_category_id)
        REFERENCES mood_category(category_id),

    FOREIGN KEY (mood_score_id)
        REFERENCES mood_score(score_id),

    FOREIGN KEY (energy_level_id)
        REFERENCES energy_level(energy_id)
);

-- =========================================================
-- 02 - LOOKUP DATA
-- =========================================================
-- IDs are explicit so they match the console menu choices in main.py.

INSERT INTO mood_category (category_id, category_name)
VALUES
    (1, 'Negative'),
    (2, 'Neutral'),
    (3, 'Positive'),
    (4, 'Ambiguous');

INSERT INTO mood_score (score_id, score_name)
VALUES
    (1, 'Terrible'),
    (2, 'Bad'),
    (3, 'Off'),
    (4, 'Ok'),
    (5, 'Good'),
    (6, 'Great'),
    (7, 'Fantastic'),
    (8, 'Mixed'),
    (9, 'Unsure');

INSERT INTO energy_level (energy_id, energy_name)
VALUES
    (1, 'Drained'),
    (2, 'Sluggish'),
    (3, 'Mellow'),
    (4, 'Steady'),
    (5, 'Vibrant'),
    (6, 'Driven'),
    (7, 'Radiant');

-- =========================================================
-- 03 - MOCK USERS
-- =========================================================

INSERT INTO users (user_id, name, email, hashed_password, created_at)
VALUES
    (1, 'Emma Smith', 'emma.smith@example.com', '$2b$12$e0MYzXy6D.GkP61R8NfhOexnK4L8y6b7u3v1c5x7z9q2w1e3r4t5y', '2026-04-01 09:00:00'),
    (2, 'Liam Johnson', 'liam.johnson@example.com', '$2b$12$K1v8NfhOexnK4L8y6b7u3v1c5x7z9q2w1e3r4t5ye0MYzXy6D.GkP6', '2026-05-01 09:00:00'),
    (3, 'Olivia Williams', 'olivia.williams@example.com', '$2b$12$3v1c5x7z9q2w1e3r4t5ye0MYzXy6D.GkP61R8NfhOexnK4L8y6b7u', '2026-04-15 09:00:00'),
    (4, 'Noah Brown', 'noah.brown@example.com', '$2b$12$q2w1e3r4t5ye0MYzXy6D.GkP61R8NfhOexnK4L8y6b7u3v1c5x7z9', '2026-04-18 09:00:00'),
    (5, 'Ava Jones', 'ava.jones@example.com', '$2b$12$GkP61R8NfhOexnK4L8y6b7u3v1c5x7z9q2w1e3r4t5ye0MYzXy6D.', '2026-04-28 09:00:00'),
    (6, 'Oliver Miller', 'oliver.miller@example.com', '$2b$12$8NfhOexnK4L8y6b7u3v1c5x7z9q2w1e3r4t5ye0MYzXy6D.GkP61R', '2026-04-04 09:00:00'),
    (7, 'Sophia Davis', 'sophia.davis@example.com', '$2b$12$y6b7u3v1c5x7z9q2w1e3r4t5ye0MYzXy6D.GkP61R8NfhOexnK4L8', '2026-05-02 09:00:00'),
    (8, 'Elijah Garcia', 'elijah.garcia@example.com', '$2b$12$5x7z9q2w1e3r4t5ye0MYzXy6D.GkP61R8NfhOexnK4L8y6b7u3v1c', '2026-04-24 09:00:00'),
    (9, 'Isabella Rodriguez', 'isabella.rodriguez@example.com', '$2b$12$e3r4t5ye0MYzXy6D.GkP61R8NfhOexnK4L8y6b7u3v1c5x7z9q2w1', '2026-04-05 09:00:00'),
    (10, 'James Wilson', 'james.wilson@example.com', '$2b$12$D.GkP61R8NfhOexnK4L8y6b7u3v1c5x7z9q2w1e3r4t5ye0MYzXy6', '2026-04-12 09:00:00');

-- =========================================================
-- 04 - MOCK JOURNAL ENTRIES
-- =========================================================
-- Weather values use OpenWeather-style main conditions:
-- Clear, Clouds, Rain, Drizzle, Thunderstorm, Snow, Mist, Fog, Haze.

INSERT INTO journal_entries
(user_id, title, content, mood_category_id, mood_score_id, energy_level_id, free_time, weather, recommendations, created_at)
VALUES
    (1, 'Great start to the week',
     'Woke up early and went for a run. The weather was beautiful and I feel incredibly productive today.',
     3, 6, 5, FALSE, 'Clear',
     'Keep up the positive momentum. A short outdoor walk could help you enjoy the clear weather.',
     '2026-04-02 09:30:00'),

    (1, 'A bit overwhelmed',
     'Too many tasks at work today. Feeling a bit buried under pressure and my head hurts.',
     1, 2, 2, FALSE, 'Clouds',
     'Try a short breathing break and choose one small task to complete first.',
     '2026-04-03 18:45:00'),

    (6, 'Creative spark',
     'Woke up with an awesome idea for my hobby project. Spent hours drafting it out.',
     3, 6, 6, TRUE, 'Clear',
     'Use your energy creatively. A focused hobby session could feel rewarding.',
     '2026-04-05 13:15:00'),

    (9, 'Bored out of my mind',
     'Had literally nothing to do at the office today. Clicking around just trying to pass time.',
     2, 4, 2, FALSE, 'Clouds',
     'Try a small reset activity, such as tidying one area or making a short plan for tomorrow.',
     '2026-04-06 15:00:00'),

    (6, 'Exhausted after a long week',
     'Friday night and I am completely dead. No energy to do anything but scroll on my phone.',
     1, 2, 1, TRUE, 'Clouds',
     'Choose a gentle low-effort activity tonight and prioritise rest.',
     '2026-04-10 20:45:00'),

    (9, 'Perfect afternoon',
     'Sat in the backyard garden all afternoon. The weather was amazing.',
     3, 6, 4, TRUE, 'Clear',
     'Spend a little more time outside if you can. Notice what felt good today.',
     '2026-04-11 16:30:00'),

    (10, 'Freezing day',
     'The weather is terrible, icy sleet everywhere. Stayed inside and did chores.',
     2, 4, 3, FALSE, 'Snow',
     'Stay warm and keep tasks simple. A hot drink and gentle routine could help.',
     '2026-04-14 14:00:00'),

    (3, 'Feeling off today',
     'Can barely keep my eyes open and everything is annoying me. Going to sleep early.',
     1, 3, 1, FALSE, 'Clouds',
     'Keep things gentle. Rest and a simple evening routine may help.',
     '2026-04-15 21:00:00'),

    (9, 'Sad news',
     'Found out my childhood pet passed away today. Heartbroken.',
     1, 1, 1, TRUE, 'Rain',
     'Be kind to yourself. Reach out to someone safe or do something comforting.',
     '2026-04-16 12:00:00'),

    (3, 'Spring walk',
     'The sunshine came out after a week of rain! Took a long walk through the park after work.',
     3, 5, 5, TRUE, 'Clear',
     'A walk worked well today. Consider repeating that when the weather allows.',
     '2026-04-18 18:00:00'),

    (10, 'Inspired to cook',
     'Tried a brand new complex recipe tonight and it turned out incredible! Proud of myself.',
     3, 6, 5, TRUE, 'Clouds',
     'Use your energy on something creative or nourishing.',
     '2026-04-20 20:15:00'),

    (3, 'Anxious about tomorrow',
     'Have a massive presentation tomorrow morning and my stomach is in knots. Trying to calm down.',
     1, 2, 4, FALSE, 'Rain',
     'Prepare one small thing, then give yourself permission to rest.',
     '2026-04-22 22:10:00'),

    (3, 'Celebration!',
     'The presentation went flawlessly! Everyone loved it. Celebrating with a nice dinner tonight.',
     3, 7, 7, TRUE, 'Clear',
     'Celebrate the win and write down what helped you succeed.',
     '2026-04-23 19:45:00'),

    (1, 'Rainy weekend relaxation',
     'Spent the whole afternoon reading on the couch while it poured outside. Exactly what I needed.',
     3, 5, 3, TRUE, 'Rain',
     'A calm indoor activity suited your mood. Keep that option in mind for rainy days.',
     '2026-04-26 15:00:00'),

    (10, 'Running on empty',
     'Stayed up way too late watching a show and paid the price at work today. Struggling to stay awake.',
     1, 2, 1, FALSE, 'Clouds',
     'Aim for an early night and reduce pressure where possible.',
     '2026-04-28 13:00:00'),

    (5, 'Just a normal day',
     'Nothing special happened today. Work was fine, traffic was fine, dinner was fine. Standard.',
     2, 4, 4, FALSE, 'Clouds',
     'A steady day still counts. Note one small thing that went okay.',
     '2026-04-29 17:00:00'),

    (2, 'Super lazy Sunday',
     'Literally did nothing today. Slept in, ordered pizza, and watched movies. Total couch potato vibes.',
     2, 4, 2, TRUE, 'Clouds',
     'Rest can be useful. Try adding one tiny reset task if you want balance.',
     '2026-05-03 20:00:00'),

    (7, 'Fresh start',
     'First day tracking my habits again. Feeling optimistic and steady.',
     3, 5, 4, FALSE, 'Clear',
     'Keep it simple and repeatable. One small habit is enough to start.',
     '2026-05-03 08:00:00'),

    (2, 'Midweek focus',
     'Completely locked into my code today. Had great flow and zero distractions.',
     3, 6, 6, FALSE, 'Clouds',
     'Use the focus while it is there, but plan a break afterwards.',
     '2026-05-06 17:30:00'),

    (7, 'Gym motivation',
     'Had a crazy good workout session today. Felt like I could lift a house.',
     3, 7, 7, TRUE, 'Clear',
     'Enjoy the energy. A short cooldown could help you recover well.',
     '2026-05-07 19:30:00'),

    (5, 'Stormy evening',
     'Massive thunderstorm tonight. Watching the lightning from the window with a hot cup of tea.',
     2, 4, 3, TRUE, 'Thunderstorm',
     'Stay cosy indoors and choose something calming.',
     '2026-05-10 22:30:00'),

    (6, 'Cozy and quiet',
     'It is snowing outside nicely. Cleaned up the apartment and enjoying the quiet space.',
     2, 4, 4, TRUE, 'Snow',
     'A quiet indoor reset seems to fit well today.',
     '2026-05-11 11:00:00'),

    (2, 'Frustrated',
     'Spilled coffee on my laptop and argued with support. Just a genuinely annoying day.',
     1, 2, 3, FALSE, 'Clouds',
     'Pause before tackling anything else. A short reset may prevent the frustration from snowballing.',
     '2026-05-12 11:15:00'),

    (7, 'Stressed over deadlines',
     'Too much on my plate and not enough hours in the day. Brain feels fried.',
     1, 2, 2, FALSE, 'Clouds',
     'Pick one priority and park the rest. A tiny list may help reduce the mental load.',
     '2026-05-12 16:00:00'),

    (1, 'Bittersweet evening',
     'Had a long talk with an old friend moving away. Happy for them but sad they are leaving.',
     4, 8, 3, TRUE, 'Clouds',
     'Mixed feelings make sense. Try writing down both sides of the feeling.',
     '2026-05-15 21:15:00'),

    (5, 'Blah',
     'I do not even know how I feel today. Not sad, not happy, just completely blank and emotionally flat.',
     4, 9, 2, FALSE, 'Mist',
     'Keep things low-pressure. Naming the feeling as unclear is still useful information.',
     '2026-05-16 14:00:00'),

    (7, 'Grateful for small things',
     'Someone paid for my coffee today. It really turned my whole mood around.',
     3, 5, 5, FALSE, 'Clear',
     'Notice the small positive moment. It may be worth recording what made it matter.',
     '2026-05-18 10:30:00'),

    (6, 'Angry at the traffic',
     'Commute took two hours because of a minor accident. Ruined my whole morning mood.',
     1, 2, 5, FALSE, 'Drizzle',
     'Use a short decompression ritual after a difficult commute.',
     '2026-05-22 09:15:00'),

    (7, 'Mixed up day',
     'Got some great news about a promotion, but a close coworker announced they are quitting.',
     4, 8, 4, FALSE, 'Clouds',
     'Hold both feelings without forcing a single mood label.',
     '2026-05-24 15:45:00'),

    (1, 'Crushing my goals',
     'Finished the big project layout ahead of schedule. On absolute top of the world right now!',
     3, 7, 6, FALSE, 'Clear',
     'Celebrate and note what helped you make progress.',
     '2026-05-25 16:20:00'),

    (10, 'Unstoppable mood',
     'Got a great night of sleep, sun is shining, feeling absolutely radiant today.',
     3, 7, 7, TRUE, 'Clear',
     'Use the momentum, but remember recovery still matters.',
     '2026-05-29 09:00:00');

-- =========================================================
-- 05 - FUNCTIONS
-- =========================================================

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
-- 06 - VIEW
-- =========================================================

CREATE VIEW mood_board_view AS
SELECT
    u.user_id,
    u.name AS user_name,
    u.email,

    je.entry_id,
    je.created_at,
    je.title,
    je.content,

    mc.category_id,
    mc.category_name,

    ms.score_id,
    ms.score_name,
    get_mood_score_label(ms.score_id) AS mood_score_label,

    el.energy_id,
    el.energy_name,
    get_energy_support_label(el.energy_id) AS energy_support_label,

    je.free_time,
    get_free_time_label(je.free_time) AS free_time_label,

    je.weather AS weather_name,
    je.recommendations

FROM journal_entries je
INNER JOIN users u
    ON je.user_id = u.user_id
INNER JOIN mood_category mc
    ON je.mood_category_id = mc.category_id
INNER JOIN mood_score ms
    ON je.mood_score_id = ms.score_id
INNER JOIN energy_level el
    ON je.energy_level_id = el.energy_id;

-- =========================================================
-- 07 - STORED PROCEDURES
-- =========================================================

DELIMITER //

CREATE PROCEDURE get_user_mood_history(IN input_user_id INT)
BEGIN
    SELECT
        entry_id,
        created_at,
        title,
        content,
        category_name,
        score_name,
        mood_score_label,
        energy_name,
        energy_support_label,
        free_time_label,
        weather_name,
        recommendations
    FROM mood_board_view
    WHERE user_id = input_user_id
    ORDER BY created_at DESC;
END //

CREATE PROCEDURE search_user_entries(
    IN input_user_id INT,
    IN input_keyword VARCHAR(255),
    IN input_mood_category_id INT,
    IN input_sort_order VARCHAR(10)
)
BEGIN
    SELECT
        entry_id,
        created_at,
        title,
        content,
        category_name,
        score_name,
        energy_name,
        free_time_label,
        weather_name,
        recommendations
    FROM mood_board_view
    WHERE user_id = input_user_id
      AND (
          input_keyword IS NULL
          OR input_keyword = ''
          OR LOWER(title) LIKE CONCAT('%', LOWER(input_keyword), '%')
          OR LOWER(content) LIKE CONCAT('%', LOWER(input_keyword), '%')
      )
      AND (
          input_mood_category_id IS NULL
          OR category_id = input_mood_category_id
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

CREATE PROCEDURE get_user_mood_summary(IN input_user_id INT)
BEGIN
    SELECT
        user_id,
        COUNT(entry_id) AS total_entries,
        ROUND(AVG(score_id), 2) AS average_score_id,
        ROUND(AVG(energy_id), 2) AS average_energy_id,

        SUM(CASE WHEN category_name = 'Positive' THEN 1 ELSE 0 END) AS positive_entries,
        SUM(CASE WHEN category_name = 'Neutral' THEN 1 ELSE 0 END) AS neutral_entries,
        SUM(CASE WHEN category_name = 'Negative' THEN 1 ELSE 0 END) AS negative_entries,
        SUM(CASE WHEN category_name = 'Ambiguous' THEN 1 ELSE 0 END) AS ambiguous_entries,

        MAX(created_at) AS latest_entry,

        CASE
            WHEN AVG(score_id) <= 3 AND AVG(energy_id) <= 2
                THEN 'Gentle support may be helpful.'
            WHEN SUM(CASE WHEN category_name = 'Negative' THEN 1 ELSE 0 END) >= 3
                THEN 'Several challenging check-ins logged.'
            WHEN AVG(score_id) >= 5
                THEN 'Mostly positive pattern in this sample.'
            ELSE 'Mixed or steady mood pattern.'
        END AS supportive_summary
    FROM mood_board_view
    WHERE user_id = input_user_id
    GROUP BY user_id;
END //

CREATE PROCEDURE get_user_moodboard_overview(IN input_user_id INT)
BEGIN
    SELECT
        category_name,
        COUNT(entry_id) AS entry_count,
        ROUND(AVG(score_id), 2) AS average_score_id,
        ROUND(AVG(energy_id), 2) AS average_energy_id,
        MAX(created_at) AS latest_entry
    FROM mood_board_view
    WHERE user_id = input_user_id
    GROUP BY category_name
    ORDER BY entry_count DESC;
END //

CREATE PROCEDURE get_user_recommendations(IN input_user_id INT)
BEGIN
    SELECT
        created_at AS entry_created_at,
        title AS entry_title,
        category_name,
        score_name,
        energy_name,
        weather_name,
        recommendations
    FROM mood_board_view
    WHERE user_id = input_user_id
      AND recommendations IS NOT NULL
      AND recommendations <> ''
    ORDER BY created_at DESC;
END //

DELIMITER ;

-- =========================================================
-- 08 - OPTIONAL SHOWCASE QUERIES
-- =========================================================
-- These are safe examples for DBeaver/MySQL Workbench or a project demo.

-- CALL get_user_mood_history(1);
-- CALL search_user_entries(1, 'stress', NULL, 'newest');
-- CALL get_user_mood_summary(1);
-- CALL get_user_moodboard_overview(1);
-- CALL get_user_recommendations(1);

-- SELECT weather_name, COUNT(*) AS entry_count
-- FROM mood_board_view
-- GROUP BY weather_name
-- ORDER BY entry_count DESC;
