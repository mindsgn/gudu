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
- Screen container

## Home Screen (`app/home.tsx`)

**Route:** `/home`
**Purpose:** Main entry point showing wallet info and navigation

Layout:
- AnimatedHeaderScrollView with "Gudu" title
- FlashList with balance items and navigation buttons
- Backdrop gradient on scroll

Components used:
- AnimatedHeaderScrollView
- FlashList
- Button
- Screen container

## Backend Course List (`app/backend.tsx`)

**Route:** `/backend`
**Purpose:** Display list of backend development topics

Layout:
- AnimatedHeaderScrollView with "Backend" title
- FlashList of 11 course topics
- Each item is a Button linking to `/lesson`

Components used:
- AnimatedHeaderScrollView
- FlashList
- Button
- Screen container

## Lesson Screen (`app/lesson.tsx`)

**Route:** `/lesson`
**Purpose:** Read course content with progress tracking

Layout:
- Scrollable markdown content
- AnimatedScrollProgress FAB
- CircularProgress indicator
- Auto-navigate to `/complete` at 100% scroll

Components used:
- AnimatedScrollProgress
- CircularProgress
- EnrichedMarkdownText
- Screen container

Data:
- Content from `constants/backend.ts` (HTTP lesson markdown)

## Completion Screen (`app/complete.tsx`)

**Route:** `/complete`
**Purpose:** Show lesson completion (placeholder)

Layout:
- Empty View (not yet implemented)

## Adding New Screens

1. Create `app/new-screen.tsx`
2. Use Screen container
3. Use AnimatedHeaderScrollView for scrollable content
4. Handle loading, error, and empty states
5. Add to navigation from relevant screen
6. Update this file with screen specification
