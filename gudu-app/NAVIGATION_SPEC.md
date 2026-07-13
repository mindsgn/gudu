# Navigation Spec

## Structure

File-based routing via Expo Router. Stack navigator with hidden headers.

## Root Layout (`app/_layout.tsx`)

- Runs Drizzle migrations before mounting the app
- Wraps the app in `SQLiteProvider`
- Wraps the app in `GestureHandlerRootView`
- Registers the splash, home, course, lesson, backend redirect, and completion routes

## Routes

| File | Route | Purpose |
|---|---|---|
| `index.tsx` | `/` | Splash and bootstrapping |
| `home.tsx` | `/home` | Dashboard with score, streaks, heatmap, continue CTA, and course cards |
| `course.tsx` | `/course` | Generic course screen driven by `courseSlug` |
| `backend.tsx` | `/backend` | Compatibility redirect to `/course?courseSlug=backend` |
| `lesson.tsx` | `/lesson` | Markdown lesson reader driven by `lessonId` |
| `complete.tsx` | `/complete` | Completion summary driven by route params |

## Navigation Rules

- Use `router.replace()` for boot redirects and completion routing
- Use `router.push()` for course and lesson navigation
- Pass `courseSlug` into `/course`
- Pass `lessonId` into `/lesson`
- Pass completion summary params into `/complete`

## Screen Options

- All screens use `headerShown: false`
- Home and course use `AnimatedHeaderScrollView`
- Lesson uses `AnimatedScrollProgress`

## Deep Linking

- Not yet configured
- Current routes use simple string pathnames with params

## Adding Routes

1. Create `app/new-route.tsx`
2. Export a default screen component
3. Register the route in `_layout.tsx` when explicit stack config is needed
4. Add navigation from the relevant dashboard or course entry point
