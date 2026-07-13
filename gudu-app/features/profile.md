# Profile Feature

## Purpose
Display user progress and course completion status.

## Screens
- Home (`/home`) — Main view with course list

## Components
- AnimatedHeaderScrollView — Large title scroll view with blur
- FlashList — Course list
- Button — Navigation buttons

## State Flow
1. Home screen mounts
2. Display available courses
3. User taps course to navigate to course list
4. Track lesson completion

## States
- Loading: Splash animation
- Error: "Something went wrong" with retry
- Empty: "No courses available"
- Success: Course list with navigation

## Files
- `app/home.tsx` — Home screen
