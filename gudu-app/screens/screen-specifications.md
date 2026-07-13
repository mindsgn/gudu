# Screen Specifications

## Splash Screen (`app/index.tsx`)

**Route:** `/`
**Purpose:** Loading animation while app initializes

Layout:
- Full screen
- Centered Block Skia animation
- 2-second display
- Auto-redirect to `/home` via `router.replace`

Components used:
- Block (Skia)

## Home Screen (`app/home.tsx`)

**Route:** `/home`
**Purpose:** Main entry point with course navigation

Layout:
- AnimatedHeaderScrollView with "home" title
- FlashList with course navigation buttons

Components used:
- AnimatedHeaderScrollView
- FlashList
- Button (PressableCard)

## Backend Course List (`app/backend.tsx`)

**Route:** `/backend`
**Purpose:** Display list of backend development topics

Layout:
- AnimatedHeaderScrollView with "Backend" title and subtitle
- FlashList of 11 course topics
- Each item is a Button linking to `/lesson`

Components used:
- AnimatedHeaderScrollView
- FlashList
- Button (PressableCard)

## Lesson Screen (`app/lesson.tsx`)

**Route:** `/lesson`
**Purpose:** Read course content with progress tracking

Layout:
- Scrollable markdown content
- AnimatedScrollProgress FAB with title and progress indicator
- CircularProgress indicator on FAB
- Auto-navigate to `/complete` at 100% scroll

Components used:
- AnimatedScrollProgress
- CircularProgress
- EnrichedMarkdownText

Data:
- Content from `constants/backend.ts` (HTTP lesson markdown)

## Completion Screen (`app/complete.tsx`)

**Route:** `/complete`
**Purpose:** Show lesson completion (placeholder)

Layout:
- Empty View (not yet implemented)

## Adding New Screens

1. Create `app/new-screen.tsx`
2. Use AnimatedHeaderScrollView for scrollable content
3. Handle loading, error, and empty states
4. Add to navigation from relevant screen
5. Update this file with screen specification
