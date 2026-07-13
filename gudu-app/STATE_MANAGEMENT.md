# State Management

## Principles

- Minimize global state
- Prefer server state over cached global state
- Keep UI state local to components

## State Categories

### Server Data (Firestore)
**Tool:** Direct Firestore listeners in hooks

- Wallet balances: `use-wallet-balances.ts` — real-time listener on `wallets/{address}/balances`
- Wallet settings: `lib/firebase.ts` functions
- Transaction records: `lib/transactions.ts` functions

### Local Database (SQLite)
**Tool:** Drizzle ORM

- User records: `db/schema.ts` (user table)
- Future: progress tracking, preferences, cached data

### Global Client State
**Tool:** Zustand

- `store/wallet.ts` — Wallet address, smart address, deployment status
- `store/send.ts` — Send flow state machine (not a Zustand store, pure functions)

### Component State
**Tool:** useState / useReducer

- Form inputs
- UI toggles (modals, dropdowns)
- Animation values (via Reanimated shared values)

## Store Rules

- One store per domain
- Flat state shape — no nested objects
- Actions as methods on the store
- No async logic in stores — use hooks or lib functions
- Derive computed values outside the store

## Hook Rules

- One hook per data concern
- Hooks abstract Firestore/SQLite access
- Hooks return `{ data, loading, error }` shape
- Hooks handle cleanup (unsubscribe listeners)

## Anti-Patterns

- Do not put Firestore calls in components
- Do not create Zustand stores for UI-only state
- Do not duplicate state across stores
- Do not use useEffect for data fetching — use hooks
