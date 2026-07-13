# Design System

## Colors

All colors defined in `theme/colors.ts`. Never hardcode colors.

| Token | Value | Usage |
|---|---|---|
| background | #F2F4F5 | Screen background |
| surface | #15161A | Cards, buttons, dark surfaces |
| buttonBackground | #15161A | Button fill |
| buttonTextBackground | #F2F4F5 | Text on dark buttons |
| primary | #16A34A | Primary actions, active states |
| primaryMuted | #15803D | Secondary green |
| accent | #22C55E | Highlights, progress |
| danger | #EF4444 | Errors, destructive actions |
| textPrimary | #15161A | Main text |
| textSecondary | #9CA3AF | Secondary text, placeholders |
| border | #1F1F1F | Borders, dividers |

## Typography

All values defined in `theme/typography.ts`.

| Token | Size | Weight | Usage |
|---|---|---|---|
| title | 28px | 800 | Screen titles |
| button | 28px | 800 | Button labels |
| balance | 32px | 800 | Balance display |
| subtitle | 18px | 700 | Section headers |
| body | 14px | 400 | Body text |
| caption | 12px | 400 | Captions, labels |

## Spacing

Base unit: 4px

| Token | Value |
|---|---|
| xs | 4px |
| sm | 8px |
| md | 16px |
| lg | 24px |
| xl | 32px |
| xxl | 48px |

## Border Radius

| Token | Value | Usage |
|---|---|---|
| small | 8px | Inputs, small cards |
| medium | 12px | Cards |
| large | 16px | Modals |
| pill | 999px | Pills, badges |
| block | 20px | Block components |

## Shadows

Use elevation for Android, shadow properties for iOS. Keep shadows subtle.

## Component Tokens

### Button
- Height: 48px minimum
- Border radius: matches `borderRadius` prop
- Background: `colors.buttonBackground`
- Text: `colors.buttonTextBackground`

### Card
- Background: `colors.surface`
- Border radius: 12px
- Padding: 16px

### Screen
- Background: `colors.background`
- Padding top: 48px (safe area)
- Padding horizontal: 16px
