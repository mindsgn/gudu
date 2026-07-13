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

## ADR-004: Drizzle Over Raw SQLite

**Decision:** Use Drizzle ORM for SQLite operations.
**Rationale:** Type-safe queries, migration system, familiar SQL-like API.
**Consequence:** Migration generation required for schema changes.

## ADR-005: Shared UI Split

**Decision:** Split UI into `components/shared/` (simple) and `shared/ui/` (complex).
**Rationale:** Simple components are used everywhere, complex ones need isolation.
**Consequence:** Two locations to check for existing components.

## ADR-006: System Font

**Decision:** Use system font for all text.
**Rationale:** No custom font loading, better performance, native feel.
**Consequence:** Less brand differentiation, acceptable for utility app.
