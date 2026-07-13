# Architecture Decisions

## ADR-001: File-Based Routing

**Decision:** Use Expo Router with file-based routing.
**Rationale:** Simpler mental model, less boilerplate, automatic deep linking.
**Consequence:** Routes are tied to file system structure.

## ADR-002: Flat Feature Organization

**Decision:** Keep features flat in `app/` rather than nested feature folders.
**Rationale:** Current app has few screens. Nested folders add complexity without benefit.
**Consequence:** When features grow, consider migrating to feature-based folders.

## ADR-003: Skia for Visual Effects

**Decision:** Use @shopify/react-native-skia for animated visual components.
**Rationale:** GPU-accelerated, shader support, liquid metal effects.
**Consequence:** Larger bundle size, requires careful memory management.

## ADR-004: Zustand Over Context

**Decision:** Use Zustand for global state instead of React Context.
**Rationale:** Simpler API, better performance, no provider nesting.
**Consequence:** Another dependency, but lightweight and well-maintained.

## ADR-005: Drizzle Over Raw SQLite

**Decision:** Use Drizzle ORM for SQLite operations.
**Rationale:** Type-safe queries, migration system, familiar SQL-like API.
**Consequence:** Migration generation required for schema changes.

## ADR-006: Firestore for Remote Data

**Decision:** Use Firebase/Firestore for remote data sync.
**Rationale:** Real-time listeners, offline support, managed infrastructure.
**Consequence:** Firebase vendor lock-in, but acceptable for current scale.

## ADR-007: ERC-4337 Account Abstraction

**Decision:** Use ZeroDev for smart contract wallets (ERC-4337).
**Rationale:** Gas sponsorship, social recovery, better UX.
**Consequence:** Additional complexity, but necessary for wallet features.

## ADR-008: No Custom Backend

**Decision:** No custom backend server. Use Firebase + external APIs directly.
**Rationale:** Reduces infrastructure complexity, Firebase handles auth/sync.
**Consequence:** Limited server-side logic, acceptable for current features.

## ADR-009: Shared UI Split

**Decision:** Split UI into `components/shared/` (simple) and `shared/ui/` (complex).
**Rationale:** Simple components are used everywhere, complex ones need isolation.
**Consequence:** Two locations to check for existing components.

## ADR-010: System Font

**Decision:** Use system font for all text.
**Rationale:** No custom font loading, better performance, native feel.
**Consequence:** Less brand differentiation, acceptable for utility app.
