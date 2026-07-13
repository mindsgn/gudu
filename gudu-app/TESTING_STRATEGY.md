# Testing Strategy

## Current State

Tests use Jest (comes with Expo). Run with `npm test` from `gudu-app/`.

## Coverage Targets

### Unit Tests
- Pure functions in `lib/` — test inputs/outputs
- Helper functions — test edge cases
- Theme tokens — verify shape and values
- Constants — verify structure

### Component Tests
- Shared components — test rendering with different props
- UI organisms — test interaction callbacks
- Error/loading/empty states — test all branches

### Integration Tests
- Screen flows — test navigation and data flow

### E2E Tests (Future)
- Critical user journeys
- Course completion flow

## Rules

- Test behavior, not implementation
- Use descriptive test names
- One assertion per test when possible
- Test error states and edge cases

## Tooling

- Test runner: Jest (comes with Expo)
- Config: `jest.config.js`
- Setup: `jest.setup.js` (mocks for React Native modules)
