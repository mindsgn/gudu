# Screen Specifications

## Splash Screen (`app/index.tsx`)

**Route:** `/`
**Purpose:** Bootstrap migrations and curriculum seed before routing into the dashboard

Layout:
- Centered Block animation
- Local boot loading state
- Retry state when bootstrapping fails

## Home Screen (`app/home.tsx`)

**Route:** `/home`
**Purpose:** Show score, streaks, heatmap, continue CTA, and both courses

Layout:
- Animated header
- Score/streak summary card
- Continue button when a lesson target exists
- Activity heatmap
- Course cards for backend and frontend

## Course Screen (`app/course.tsx`)

**Route:** `/course`
**Params:** `courseSlug`
**Purpose:** Show ordered modules and lessons for one course

Layout:
- Animated header
- Course summary card
- Continue button for the course
- Flattened module headers + lesson rows

## Backend Redirect (`app/backend.tsx`)

**Route:** `/backend`
**Purpose:** Redirect legacy backend navigation to `/course?courseSlug=backend`

## Lesson Screen (`app/lesson.tsx`)

**Route:** `/lesson`
**Params:** `lessonId`
**Purpose:** Render markdown, track reading progress, restore scroll position, and complete at 100 percent

Layout:
- Floating progress FAB
- Course/module context
- Markdown lesson body
- Completion routing at full scroll

## Completion Screen (`app/complete.tsx`)

**Route:** `/complete`
**Purpose:** Summarize first-time lesson completion and route home or into the next lesson

Layout:
- Completion title
- Points earned
- Total score and streak cards
- Next lesson summary
- Continue Next Lesson CTA
- Exit to Home CTA
