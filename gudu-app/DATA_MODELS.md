# Data Models

## SQLite (Local)

### User
Table: `user`

| Field | Type | Constraints |
|---|---|---|
| id | text | PRIMARY KEY |
| createdAt | integer (timestamp_ms) | NOT NULL |
| updatedAt | integer (timestamp_ms) | NOT NULL |

Schema: `db/schema.ts`

## App Types

Shared types defined in `@/types/index.ts`.

## Rules

- Database schema changes require a new Drizzle migration
- Run `npx drizzle-kit generate` to create migration SQL
- Never modify generated migration files
- Types auto-inferred from schema via `$inferSelect` / `$inferInsert`
