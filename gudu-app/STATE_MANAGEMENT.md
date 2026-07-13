# State Management

## Principles

- Minimize global state
- Keep UI state local to components

## State Categories

### Local Database (SQLite)
**Tool:** Drizzle ORM

- User records: `db/schema.ts` (user table)
- Course content: `constants/backend.ts`

### Component State
**Tool:** useState / useReducer

- Form inputs
- UI toggles (modals, dropdowns)
- Animation values (via Reanimated shared values)

## Anti-Patterns

- Do not create Zustand stores for UI-only state
- Keep state as local as possible
