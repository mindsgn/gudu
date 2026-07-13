# Learning Feature

## Purpose
Browse courses, read lessons with scroll progress, and track completion.

## Screens
- Backend (`/backend`) — Course list of 11 backend topics
- Lesson (`/lesson`) — Markdown lesson reader with scroll progress
- Complete (`/complete`) — Lesson completion celebration

## Components
- AnimatedHeaderScrollView — Large title scroll view with blur
- FlashList — Course topic list
- AnimatedScrollProgress — Scroll-based progress tracking with FAB
- CircularProgress — Progress indicator on FAB
- Button — Navigation buttons

## State Flow
1. User selects course from home > navigates to `/backend`
2. User selects topic > navigates to `/lesson`
3. User scrolls through lesson > progress tracked
4. Reaching end of lesson > haptic feedback > navigate to `/complete`
5. Completion screen shown

## States
- Loading: Splash animation
- Error: "Failed to load lesson" with retry
- Empty: "No content available"
- Success: Lesson content with scroll progress

## Files
- `app/backend.tsx` — Course list
- `app/lesson.tsx` — Lesson reader
- `app/complete.tsx` — Completion screen
- `constants/backend.ts` — Course content
