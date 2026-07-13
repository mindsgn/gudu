# Feature Template

Use this template when creating new features.

```markdown
# {Feature Name}

## Purpose
One sentence describing what this feature does.

## Screens
- Screen 1 — description
- Screen 2 — description

## Components
- ComponentName — description (new or existing)

## Hooks
- useSomething — description

## Lib Functions
- functionName — description

## Stores
- storeName — description (if needed)

## API Endpoints
- METHOD /path — description (if needed)

## State Flow
1. User action →
2. State change →
3. API call →
4. UI update

## States
- Loading: what the user sees
- Error: what the user sees
- Empty: what the user sees
- Success: what the user sees

## Dependencies
- Existing components used
- New libraries needed (require approval)

## Files to Create
- app/route.tsx
- components/shared/new-component.tsx (if needed)
- hooks/use-new-thing.ts (if needed)
- lib/new-thing.ts (if needed)

## Files to Modify
- None / list files
```
