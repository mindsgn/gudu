# Navigation Spec

## Structure

File-based routing via Expo Router. Stack navigator.

## Root Layout (`app/_layout.tsx`)

- Wraps app in `SQLiteProvider` (runs Drizzle migrations)
- Wraps in `GestureHandlerRootView`
- Stack navigator with `headerShown: false` globally

## Routes

| File | Route | Purpose |
|---|---|---|
| `index.tsx` | `/` | Splash — 2s Block animation, then redirect to `/home` |
| `home.tsx` | `/home` | Home — AnimatedHeaderScrollView + FlashList |
| `backend.tsx` | `/backend` | Course list — FlashList of 11 topics |
| `lesson.tsx` | `/lesson` | Lesson reader — Markdown + scroll progress |
| `complete.tsx` | `/complete` | Completion — placeholder |

## Navigation Rules

- Use `router.push()` for forward navigation
- Use `router.replace()` for redirect (splash → home)
- Use `router.back()` for back navigation
- Pass data via route params: `router.push({ pathname: '/lesson', params: { id } })`
- No tab navigator currently — Stack only

## Screen Options

- All screens: `headerShown: false`
- Custom headers via `AnimatedHeaderScrollView` organism
- Back navigation handled by Stack navigator default behavior

## Deep Linking

- Not yet configured
- Route names are simple strings (home, backend, lesson, complete)

## Adding Routes

1. Create `app/new-route.tsx`
2. Export a default component
3. Use `Stack.Screen` options if needed
4. Import and navigate from existing screens
