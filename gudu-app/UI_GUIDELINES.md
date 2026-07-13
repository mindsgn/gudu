# UI Guidelines

## Design Language

Clean, minimal, dark-accented. Black surfaces on light backgrounds. Green accents for primary actions.

## Screen Requirements

Every screen must handle:

1. **Loading state** — Spinner or skeleton
2. **Error state** — Message with retry option
3. **Empty state** — Helpful message when no data
4. **Success state** — Confirmation feedback

## Layout Rules

- Screen container: `flex: 1`, `paddingTop: 48`
- Content padding: 16px horizontal
- Section spacing: 24px between sections
- Element spacing: 8px between related items, 16px between groups

## Touch Targets

- Minimum touch target: 48px height
- Buttons: minimum 48px height
- Pressable areas: minimum 44px height

## Animations

- Use Reanimated for layout animations
- Use Skia for complex visual effects (gradients, shaders)
- Keep animations under 300ms for feedback
- Use `expo-haptics` for tactile feedback on interactions

## Lists

- Use `FlashList` for all lists (not FlatList)
- Always provide `estimatedItemSize`
- Use `getItemType` for heterogeneous lists

## Typography

- Reference `theme/typography.ts` for all text styles
- Never hardcode font sizes or weights
- System font for all text

## Accessibility

- All interactive elements need accessibility labels
- Support dynamic type where possible
- Minimum contrast ratio: 4.5:1 for text
