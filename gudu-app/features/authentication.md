# Authentication Feature

## Purpose
Splash screen with animated block, auto-redirect to home.

## Screens
- Splash (`/`) — Block animation, auto-redirect to home

## Components
- Block — Skia animated block (splash animation)

## State Flow
1. App launch > Splash animation (2s)
2. Haptic feedback on focus
3. Redirect to `/home`

## States
- Loading: Splash animation
- Error: N/A (redirect only)
- Empty: N/A
- Success: Redirect to home

## Dependencies
- @shopify/react-native-skia (Block shader)
- expo-haptics (feedback)

## Files
- `app/index.tsx` — Splash screen
