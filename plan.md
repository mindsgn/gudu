# Gudu Learning App Plan

## Aim

Build Gudu into a local-first mobile learning app that helps the user learn backend and frontend engineering from the lesson content already in this repo.

The app should:

- use the lesson documents in `lessons/` as the entry point for course discovery
- use the generated curriculum content in `backend-engineering/` and `frontend-engineering/` as the actual lesson source
- keep track of lesson progress, streaks, points, and daily activity
- let the user continue where they left off
- unlock lessons in order after a lesson is fully read
- render lessons as markdown and trigger completion at 100 percent scroll
- stay fully local using SQLite + Drizzle
- include Jest tests and Maestro end-to-end flows

## Current Repo Reality

These points should drive the implementation plan:

- `gudu-app/` is the only runnable app.
- The stack is fixed: Expo Router, Expo SQLite, Drizzle ORM, FlashList, Reanimated, Skia, and `react-native-enriched-markdown`.
- No backend server is required for core functionality.
- The current app is a prototype:
  - `app/home.tsx` only shows one hardcoded backend button
  - `app/backend.tsx` shows 11 hardcoded topics
  - `app/lesson.tsx` reads one hardcoded markdown string from `constants/backend.ts`
  - `app/complete.tsx` is empty
  - `db/schema.ts` only contains a `user` table
- The curriculum size is large enough to matter:
  - backend: 105 chapters plus `README.md`, about 1.7 MB of markdown
  - frontend: 180 chapters plus `README.md`, about 4.5 MB of markdown
- `backend-engineering/` and `frontend-engineering/` are generated content and should not be edited by hand.

## Important Content Constraints

The lesson source is not fully normalized yet.

- `lessons/backend.md` is app-friendly. It already maps the backend course into phases and links to actual chapter files.
- `lessons/frontend.md` is not app-friendly yet. It is mostly a plain topic list, does not link to chapter files, and also contains a stray `# Backend Fundamentals` section that should not be part of the frontend course flow.
- `frontend-engineering/README.md` is currently the best canonical frontend index because it already maps the 180 chapters into 18 modules with linked files.

This means the app should not directly trust `lessons/frontend.md` in its current form. The plan should include a normalization step so both courses can be loaded through one consistent model.

## V1 Product Decisions

These defaults remove ambiguity and keep the first implementation small:

- Single local learner profile only. No auth and no sync.
- Two courses in V1:
  - Backend Engineering
  - Frontend Engineering
- Lessons unlock strictly in order within each course.
- The first lesson in each course is unlocked by default.
- A lesson becomes complete only once, when scroll progress first reaches 100 percent.
- Reopening a completed lesson is allowed, but it does not award points again.
- Continue behavior:
  - first choice: resume the most recent in-progress lesson
  - second choice: open the next unlocked but incomplete lesson
  - third choice: open the first unlocked lesson in the selected course
- Points in V1 should be simple and deterministic:
  - `10` points per first-time lesson completion
- A day counts toward the streak if at least one lesson is completed on that calendar day.
- The home score is lifetime total points.
- The heatmap should use daily points earned, GitHub-style.

## Recommended Product Shape

### Home Screen

Show:

- current total score
- current streak and longest streak
- GitHub-style activity heatmap for recent days
- one Continue button if there is an in-progress or next unlocked lesson
- both courses as tappable cards with lesson counts and progress summary

Recommended mobile heatmap shape:

- 7 rows by 12 to 16 columns
- horizontally scrollable if needed
- intensity based on points earned that day

### Course Screen

Replace the backend-only list with one generic course screen driven by params.

Show:

- course title and summary
- grouped lessons in order by phase/module
- locked, unlocked, in-progress, and completed states
- progress summary for the course

Rules:

- locked lessons are visible but not openable
- completed lessons can be reopened
- the next lesson unlocks only after the current lesson is completed

### Lesson Screen

Show:

- lesson title
- course/module context
- markdown content
- scroll progress
- restore previous reading position if the lesson is in progress

Rules:

- save scroll progress as the user reads
- when progress reaches 100 percent the app marks the lesson complete exactly once
- completion updates score, streak, heatmap, course progress, and continue target
- after completion, navigate to the complete screen

### Complete Screen

Show:

- success state
- points just earned
- total score
- streak update
- unlocked next lesson
- Continue Next Lesson button
- Exit to Home button

## Content Strategy

Because the curriculum is too large for a single hardcoded string approach, content should be normalized through a build-time pipeline instead of being manually maintained in app files.

### Canonical Inputs

- `lessons/backend.md`
- `lessons/frontend.md`
- `backend-engineering/README.md`
- `frontend-engineering/README.md`
- all chapter files under `backend-engineering/`
- all chapter files under `frontend-engineering/`

### Recommended Ingestion Approach

Add a repo-level generation step that produces app-ready curriculum artifacts inside `gudu-app/`.

Recommended script:

- `scripts/generate_app_curriculum.py`

Recommended outputs:

- normalized course metadata
- normalized module/phase metadata
- normalized lesson metadata
- lesson markdown payloads
- a content version or hash so the app can detect when curriculum content changed

### Why This Matters

- avoids hand-maintaining 285 lesson definitions
- keeps the app in sync when curriculum generators change
- lets the app read one consistent shape for backend and frontend
- avoids leaving `constants/backend.ts` as a dead-end prototype

### Frontend Index Fix

Before or during ingestion, normalize the frontend course definition:

- treat `frontend-engineering/README.md` as canonical for order and grouping
- update `lessons/frontend.md` so it becomes a proper course index like `lessons/backend.md`
- remove the stray backend section from the frontend lesson doc

## Proposed Drizzle Schema

The app should move from one `user` table to a curriculum-aware schema.

### `learner_profile`

One local learner record.

| Field | Type | Notes |
|---|---|---|
| id | text | primary key, fixed local id |
| totalPoints | integer | cached lifetime points |
| currentStreak | integer | consecutive active days |
| longestStreak | integer | best streak so far |
| lastActiveOn | text | `YYYY-MM-DD` |
| createdAt | integer | timestamp_ms |
| updatedAt | integer | timestamp_ms |

### `courses`

Static seeded course metadata.

| Field | Type | Notes |
|---|---|---|
| id | text | primary key |
| slug | text | `backend`, `frontend` |
| title | text | display name |
| description | text | short summary |
| sourceIndexPath | text | points to `lessons/*.md` |
| totalLessons | integer | count |
| totalModules | integer | count of phases/modules |
| sortOrder | integer | display order |
| createdAt | integer | timestamp_ms |
| updatedAt | integer | timestamp_ms |

### `course_modules`

Stores backend phases and frontend modules in one shape.

| Field | Type | Notes |
|---|---|---|
| id | text | primary key |
| courseId | text | foreign key to `courses.id` |
| slug | text | stable module identifier |
| title | text | phase/module title |
| summary | text | optional goal text |
| sortOrder | integer | order within course |

### `lessons`

Stores lesson metadata and content source details.

| Field | Type | Notes |
|---|---|---|
| id | text | primary key |
| courseId | text | foreign key |
| moduleId | text | foreign key |
| slug | text | stable identifier |
| title | text | lesson title |
| sourcePath | text | original markdown file path |
| orderIndex | integer | absolute order within course |
| estimatedStudyMinutes | integer | parsed from source when available |
| estimatedPracticeMinutes | integer | parsed from source when available |
| difficultyLabel | text | parsed when available |
| prerequisitesJson | text | serialized list |
| unlockedConceptsJson | text | serialized list |
| markdown | text | actual lesson content |
| createdAt | integer | timestamp_ms |
| updatedAt | integer | timestamp_ms |

### `lesson_progress`

One row per lesson per local learner.

| Field | Type | Notes |
|---|---|---|
| lessonId | text | primary key, foreign key |
| status | text | `locked`, `unlocked`, `in_progress`, `completed` |
| scrollPercent | integer | `0-100` |
| lastScrollOffset | integer | for resume |
| startedAt | integer | nullable |
| completedAt | integer | nullable |
| lastOpenedAt | integer | nullable |
| pointsAwarded | integer | `0` or `10` in V1 |
| createdAt | integer | timestamp_ms |
| updatedAt | integer | timestamp_ms |

### `daily_activity`

Feeds the score history and heatmap.

| Field | Type | Notes |
|---|---|---|
| activityDate | text | primary key, `YYYY-MM-DD` |
| pointsEarned | integer | total earned that day |
| lessonsCompleted | integer | total completed that day |
| createdAt | integer | timestamp_ms |
| updatedAt | integer | timestamp_ms |

### `app_state`

Stores app-level version and seed state.

| Field | Type | Notes |
|---|---|---|
| key | text | primary key |
| value | text | serialized value |
| updatedAt | integer | timestamp_ms |

Suggested keys:

- `curriculumVersion`
- `curriculumSeededAt`

## Core App Logic

These pure functions should exist in `lib/` and be heavily tested:

- curriculum normalization helpers
- initial course seed helpers
- unlock calculation
- continue target selection
- points award logic
- streak update logic
- heatmap intensity mapping
- lesson completion transaction helper

Important rule:

- the lesson completion write must be idempotent so repeated 100 percent scroll events do not duplicate points or streaks

## Screen and File Plan

This keeps the app close to the current architecture while making it scalable.

### Routes

- `app/index.tsx`
  - keep splash behavior
  - add seed/readiness handling
- `app/home.tsx`
  - real dashboard
- `app/course.tsx`
  - generic course lesson list driven by route params
- `app/lesson.tsx`
  - real lesson reader driven by `lessonId`
- `app/complete.tsx`
  - completion summary

If the team prefers to keep named course routes, `app/backend.tsx` and a new `app/frontend.tsx` could work, but a generic `app/course.tsx` will reduce duplication.

### App-Level Files Likely Needed

- `db/schema.ts`
- `db/client.ts`
- `lib/curriculum.ts`
- `lib/lesson-progress.ts`
- `lib/streaks.ts`
- `lib/points.ts`
- `lib/continue-target.ts`
- `constants/curriculum.ts` or another generated constants file
- `components/shared/lesson-list-item.tsx`
- `shared/ui/organisms/activity-heatmap/`

### Existing Files That Should Be Reworked

- `app/home.tsx`
- `app/backend.tsx` or replaced by `app/course.tsx`
- `app/lesson.tsx`
- `app/complete.tsx`
- `constants/backend.ts`
- `db/schema.ts`

## Implementation Phases

### Phase 0: Normalize Content and Align Docs

Effort: Medium

Deliverables:

- confirm canonical course definitions
- fix or regenerate `lessons/frontend.md`
- decide generated artifact format for the app
- document the final content ingestion rule

Acceptance:

- both courses can be expressed as ordered modules and ordered lessons
- every lesson resolves to one real markdown file

### Phase 1: Schema and Seed Pipeline

Effort: Large

Deliverables:

- expand Drizzle schema
- create new migration
- generate curriculum seed artifacts
- seed or refresh curriculum content locally on first run or version change

Acceptance:

- app can bootstrap a fresh database with all course, module, and lesson metadata
- lesson content is locally readable without network access

### Phase 2: Repository and Progress Logic

Effort: Medium

Deliverables:

- data access helpers for courses, lessons, and progress
- lesson completion transaction
- streak and score update helpers
- continue-target helper

Acceptance:

- progress rules work without the UI
- completion is idempotent

### Phase 3: Home Dashboard

Effort: Medium

Deliverables:

- score card
- streak summary
- GitHub-style heatmap
- Continue button
- backend and frontend course cards with progress

Acceptance:

- home shows meaningful data on a seeded fresh install
- home handles loading, empty, and error states

### Phase 4: Course Screen

Effort: Medium

Deliverables:

- ordered lesson list grouped by phase/module
- lesson lock states
- progress badges

Acceptance:

- locked lessons are visible but disabled
- tapping an unlocked lesson opens the reader

### Phase 5: Lesson Reader and Completion Flow

Effort: Large

Deliverables:

- load lesson by `lessonId`
- restore reading progress
- track scroll percent
- complete at 100 percent
- unlock next lesson
- show completion summary screen

Acceptance:

- first completion updates all dependent state
- repeat opens do not double-award points
- Continue Next Lesson takes the user to the correct lesson

### Phase 6: Testing

Effort: Medium

Deliverables:

- Jest unit tests
- Jest component/integration tests
- Maestro flows
- stable `testID` coverage on critical screens

Acceptance:

- core logic is covered by Jest
- happy-path app flow is covered by Maestro

### Phase 7: Docs and Cleanup

Effort: Small

Deliverables:

- update app specs to match the new flow
- update data model docs
- update testing docs
- update component library docs
- update screen documentation

Acceptance:

- repo docs describe the implemented app, not the prototype

## Testing Plan

### Jest Unit Tests

Test pure logic in `lib/`:

- curriculum parsing and normalization
- unlock calculation
- continue-target selection
- points awarding
- streak updates
- heatmap value mapping
- content version detection

### Jest Component Tests

Test UI behavior:

- home dashboard states
- heatmap rendering
- course list lock/completed states
- lesson completion transition
- complete screen CTA behavior

### Jest Integration Tests

Test combined flows:

- seed database -> render home
- open course -> open lesson -> complete lesson
- complete lesson -> unlock next lesson -> update score/streak

### Maestro End-to-End Flows

Create flows for:

- first launch -> home loads seeded content
- open backend course -> first lesson -> scroll to complete -> completion screen
- continue from home after a partial lesson
- locked lesson cannot be opened
- complete lesson -> return home -> heatmap and score update

Important implementation detail:

- add stable `testID`s to course cards, lesson rows, continue button, heatmap cells, and completion CTAs

## Docs To Update During Implementation

These should be updated alongside the code:

- `gudu-app/APP_SPEC.md`
- `gudu-app/NAVIGATION_SPEC.md`
- `gudu-app/FOLDER_STRUCTURE.md`
- `gudu-app/DATA_MODELS.md`
- `gudu-app/TESTING_STRATEGY.md`
- `gudu-app/components/component-library.md`
- `gudu-app/screens/screen-specifications.md`
- `lessons/frontend.md`

Optional cleanup if desired:

- align AGENTS or repo docs with the fact that `gudu-app/package.json` already includes `test` and `typecheck` scripts

## Risks and Guardrails

- Do not hand-edit `backend-engineering/` or `frontend-engineering/`.
- Do not add new npm packages unless explicitly approved.
- Do not keep lesson content as one-off hardcoded constants.
- Do not query or render full markdown blobs on the home screen.
- Do not allow lesson completion to write duplicate points.
- Do not lose reading position for in-progress lessons.
- Do not skip loading, error, and empty states on screens with async DB reads.

## Definition of Done for V1

V1 is done when all of the following are true:

- the app shows both backend and frontend courses
- lesson order comes from normalized repo content, not hardcoded arrays
- progress is persisted in SQLite with Drizzle
- continue works reliably
- points, streaks, and daily heatmap update from real completions
- lessons unlock in order
- the completion screen shows points earned and routes correctly
- Jest covers core logic and key components
- Maestro covers the main learning flow
- the relevant docs are updated to match the implemented app
