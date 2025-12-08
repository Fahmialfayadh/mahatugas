-- 1. Rata-rata semua nilai submission
SELECT AVG(score) AS avg_score
FROM tracker_submission;

-- 2. Rata-rata nilai per course
SELECT c.course_name, AVG(s.score) AS avg_score
FROM tracker_submission s
JOIN tracker_assignment a ON s.assignment_id = a.assignment_id
JOIN tracker_course c ON a.course_id = c.course_id
GROUP BY c.course_name;

-- 3. Total submission per student
SELECT st.name, COUNT(s.submission_id) AS total_submit
FROM tracker_student st
LEFT JOIN tracker_submission s ON st.student_id = s.student_id
GROUP BY st.name;

-- 4. Jumlah assignment per course
SELECT c.course_name, COUNT(a.assignment_id) AS total_assignments
FROM tracker_course c
LEFT JOIN tracker_assignment a ON c.course_id = a.course_id
GROUP BY c.course_name;

-- 5. Assignment dengan submission terbanyak (populer)
SELECT a.title, COUNT(s.submission_id) AS submission_count
FROM tracker_assignment a
LEFT JOIN tracker_submission s ON a.assignment_id = s.assignment_id
GROUP BY a.title
ORDER BY submission_count DESC
LIMIT 1;

-- 6. Mahasiswa dengan nilai tertinggi
SELECT name, score
FROM tracker_student
JOIN tracker_submission USING(student_id)
WHERE score = (SELECT MAX(score) FROM tracker_submission);

-- 7. Assignment yang belum pernah disubmit
SELECT title
FROM tracker_assignment
WHERE assignment_id NOT IN (
    SELECT assignment_id FROM tracker_submission
);

-- 8. Dosen yang mengajar lebih dari satu course
SELECT lecturer_name
FROM tracker_lecturer
WHERE lecturer_id IN (
    SELECT lecturer_id
    FROM tracker_course
    GROUP BY lecturer_id
    HAVING COUNT(*) > 1
);

-- 9. Mahasiswa yang belum submit assignment dalam course tertentu (contoh: course_id = 1)
SELECT name
FROM tracker_student
WHERE student_id NOT IN (
    SELECT student_id 
    FROM tracker_submission
    JOIN tracker_assignment USING(assignment_id)
    WHERE course_id = 1
);

-- 10. Mahasiswa dengan rata-rata nilai lebih tinggi dari rata-rata keseluruhan
SELECT st.name, AVG(s.score) AS avg_student
FROM tracker_student st
JOIN tracker_submission s ON st.student_id = s.student_id
GROUP BY st.student_id
HAVING AVG(s.score) > (
    SELECT AVG(score) FROM tracker_submission
);

-- 11. Submission terlambat
SELECT st.name, a.title, s.submitted_at, a.due_date
FROM tracker_submission s
JOIN tracker_assignment a ON s.assignment_id = a.assignment_id
JOIN tracker_student st ON s.student_id = st.student_id
WHERE s.submitted_at > a.due_date;

-- 12. Submission tepat waktu
SELECT st.name, a.title, s.submitted_at
FROM tracker_submission s
JOIN tracker_assignment a ON s.assignment_id = a.assignment_id
JOIN tracker_student st ON s.student_id = st.student_id
WHERE s.submitted_at <= a.due_date;

-- 13. Daftar course beserta dosennya
SELECT c.course_code, c.course_name, l.lecturer_name
FROM tracker_course c
JOIN tracker_lecturer l ON c.lecturer_id = l.lecturer_id;

-- 14. Semua submission + nama course + nama student
SELECT st.name AS student, c.course_name, a.title, s.score
FROM tracker_submission s
JOIN tracker_assignment a ON s.assignment_id = a.assignment_id
JOIN tracker_course c ON a.course_id = c.course_id
JOIN tracker_student st ON s.student_id = st.student_id;

-- 15. Assignment dengan deadline yang sudah lewat
SELECT title, due_date
FROM tracker_assignment
WHERE due_date < CURRENT_TIMESTAMP;
