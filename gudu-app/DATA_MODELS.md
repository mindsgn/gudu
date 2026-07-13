# Data Models

## SQLite (Local)

### Legacy

#### User
Table: `user`

Legacy table kept for migration continuity. New learner state uses `learner_profile`.

### Learner Profile
Table: `learner_profile`

| Field | Type | Constraints |
|---|---|---|
| id | text | PRIMARY KEY |
| totalPoints | integer | NOT NULL |
| currentStreak | integer | NOT NULL |
| longestStreak | integer | NOT NULL |
| lastActiveOn | text | nullable `YYYY-MM-DD` |
| createdAt | integer | NOT NULL |
| updatedAt | integer | NOT NULL |

### Courses
Table: `courses`

| Field | Type | Constraints |
|---|---|---|
| id | text | PRIMARY KEY |
| slug | text | NOT NULL |
| title | text | NOT NULL |
| description | text | NOT NULL |
| sourceIndexPath | text | NOT NULL |
| totalLessons | integer | NOT NULL |
| totalModules | integer | NOT NULL |
| sortOrder | integer | NOT NULL |
| createdAt | integer | NOT NULL |
| updatedAt | integer | NOT NULL |

### Course Modules
Table: `course_modules`

| Field | Type | Constraints |
|---|---|---|
| id | text | PRIMARY KEY |
| courseId | text | FK → `courses.id` |
| slug | text | NOT NULL |
| title | text | NOT NULL |
| summary | text | nullable |
| sortOrder | integer | NOT NULL |
| createdAt | integer | NOT NULL |
| updatedAt | integer | NOT NULL |

### Lessons
Table: `lessons`

| Field | Type | Constraints |
|---|---|---|
| id | text | PRIMARY KEY |
| courseId | text | FK → `courses.id` |
| moduleId | text | FK → `course_modules.id` |
| slug | text | NOT NULL |
| title | text | NOT NULL |
| sourcePath | text | NOT NULL |
| orderIndex | integer | NOT NULL |
| estimatedStudyMinutes | integer | nullable |
| estimatedPracticeMinutes | integer | nullable |
| difficultyLabel | text | nullable |
| prerequisitesJson | text | NOT NULL |
| unlockedConceptsJson | text | NOT NULL |
| markdown | text | NOT NULL |
| createdAt | integer | NOT NULL |
| updatedAt | integer | NOT NULL |

### Lesson Progress
Table: `lesson_progress`

| Field | Type | Constraints |
|---|---|---|
| lessonId | text | PRIMARY KEY, FK → `lessons.id` |
| status | text | `locked`, `unlocked`, `in_progress`, `completed` |
| scrollPercent | integer | NOT NULL |
| lastScrollOffset | integer | NOT NULL |
| startedAt | integer | nullable |
| completedAt | integer | nullable |
| lastOpenedAt | integer | nullable |
| pointsAwarded | integer | NOT NULL |
| createdAt | integer | NOT NULL |
| updatedAt | integer | NOT NULL |

### Daily Activity
Table: `daily_activity`

| Field | Type | Constraints |
|---|---|---|
| activityDate | text | PRIMARY KEY, `YYYY-MM-DD` |
| pointsEarned | integer | NOT NULL |
| lessonsCompleted | integer | NOT NULL |
| createdAt | integer | NOT NULL |
| updatedAt | integer | NOT NULL |

### App State
Table: `app_state`

| Field | Type | Constraints |
|---|---|---|
| key | text | PRIMARY KEY |
| value | text | NOT NULL |
| updatedAt | integer | NOT NULL |

Suggested keys:

- `curriculumVersion`
- `curriculumSeededAt`

## App Types

Shared app types live in `@/@types/index.ts`.

## Rules

- Schema changes require a new Drizzle migration
- Curriculum content is seeded from `constants/curriculum.ts`
- Progress writes must be idempotent for repeated completion events
