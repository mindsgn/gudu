# Testing Strategy

## Current State

No tests configured. This section defines the target strategy.

## Target Coverage

### Unit Tests
- Pure functions in `lib/` — test inputs/outputs
- Zustand store logic — test state transitions
- Validation functions — test edge cases

### Component Tests
- Shared components — test rendering with different props
- UI organisms — test interaction callbacks
- Error/loading/empty states — test all branches

### Integration Tests
- Screen flows — test navigation and data flow
- Firestore operations — test with emulator
- Send flow — test state machine transitions

### E2E Tests (Future)
- Critical user journeys
- Wallet creation and sending
- Course completion flow

## Rules

- Test behavior, not implementation
- Mock external dependencies (Firestore, APIs)
- Use descriptive test names
- One assertion per test when possible
- Test error states and edge cases

## Tooling (When Adopted)

- Test runner: Jest (comes with Expo)
- Component testing: React Native Testing Library
- E2E: Detox (when needed)
