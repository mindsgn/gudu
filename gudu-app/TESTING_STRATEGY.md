# Testing Strategy

## Current State

Tests run with Jest from `gudu-app/`.

Commands:

```bash
npx tsc --noEmit
npx jest --runInBand
```

## Coverage Focus

### Unit Tests

- `lib/points.ts`
- `lib/streaks.ts`
- `lib/lesson-progress.ts`
- `lib/continue-target.ts`
- `lib/activity-heatmap.ts`

### Component Tests

- `shared/ui/organisms/activity-heatmap`
- shared constants/theme regressions

### Screen/Integration Tests

- `app/home.tsx` dashboard rendering with mocked local data

### E2E Flows

Maestro flows live in `gudu-app/.maestro/` for:

- first launch and seeded home
- backend lesson completion
- continue learning
- locked lesson visibility

## Rules

- Test local-first learning behavior, not implementation details
- Cover idempotent completion rules and continue-target logic
- Keep tests deterministic by mocking device-only dependencies
- Use stable `testID`s for Maestro-critical elements

## Tooling

- Test runner: Jest
- Type check: `npx tsc --noEmit`
- E2E authoring: Maestro YAML flows
