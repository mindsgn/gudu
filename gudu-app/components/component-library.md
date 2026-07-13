# Component Library

## Shared Primitives (`components/shared/`)

### PressableCard / Button
Primary CTA button with haptic feedback and loading/disabled support.

### StatePanel
Reusable loading, error, and empty-state card with optional CTA.

### CourseCard
Dashboard card for a course with progress summary, metadata, and next-lesson context.

### LessonListItem
Course lesson row with order, status, study metadata, and locked/unlocked affordance.

## Complex Organisms (`shared/ui/organisms/`)

### AnimatedHeaderScrollView
Large-title scroll view for dashboard and course screens.

### Block
Splash animation block built with Skia.

### CircularProgress
Animated circular progress indicator for the lesson FAB.

### ActivityHeatmap
GitHub-style local activity heatmap built from daily points.

## Micro Interactions (`shared/ui/micro-interactions/`)

### AnimatedScrollProgress
Lesson reader scroll shell with floating completion/progress FAB and scroll metric callbacks.

## Rules

- Reuse these components before creating new ones
- Keep simple building blocks in `components/shared/`
- Keep animated or composition-heavy UI in `shared/ui/`
