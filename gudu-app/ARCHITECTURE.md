# Architecture

## Pattern

File-based routing with shared component library. Flat feature organization.

## Rules

### Code Organization
- Routes live in `app/` — one file per route
- Shared UI components live in `components/shared/` and `shared/ui/`
- Business logic lives in `lib/` (pure functions, utilities)
- Database schema and client live in `db/`
- Constants live in `constants/`
- Theme tokens live in `theme/`

### Separation of Concerns
- Components must NOT contain business logic
- `lib/` functions are pure — no React dependencies

### Data Flow
- Local data: SQLite → drizzle → components
- UI state: component-local useState/useReducer

### File Naming
- Components: `kebab-case.tsx` (e.g., `pressable-card.tsx`)
- Lib/utils: `kebab-case.ts`
- Types: `kebab-case.ts`
- Constants: `kebab-case.ts`

### Path Alias
- `@/*` resolves to project root (e.g., `@/theme/colors`)
