# Architecture

## Pattern

File-based routing with shared component library. Flat feature organization.

## Rules

### Code Organization
- Routes live in `app/` — one file per route
- Shared UI components live in `components/shared/` and `shared/ui/`
- Business logic lives in `lib/` (pure functions, API calls, utilities)
- Custom hooks live in `hooks/`
- Global state lives in `store/` (Zustand)
- Database schema and client live in `db/`
- Constants live in `constants/`
- Theme tokens live in `theme/`

### Separation of Concerns
- Components must NOT contain business logic
- Components must NOT make API/Firestore calls directly
- Hooks abstract stateful logic away from components
- `lib/` functions are pure — no React dependencies
- Store files define state shape and actions only

### Data Flow
- Server data: Firestore → hooks → components
- Local data: SQLite → drizzle → hooks → components
- UI state: component-local useState/useReducer
- Global state: Zustand store → hooks → components

### File Naming
- Components: `kebab-case.tsx` (e.g., `pressable-card.tsx`)
- Hooks: `use-kebab-case.ts` or `useCamelCase.tsx`
- Lib/utils: `kebab-case.ts`
- Types: `kebab-case.ts`
- Constants: `kebab-case.ts`
- Stores: `kebab-case.ts`

### Path Alias
- `@/*` resolves to project root (e.g., `@/theme/colors`, `@/lib/firebase`)
