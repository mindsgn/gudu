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

## Firestore (Remote)

### Wallet
Collection: `wallets/{address}`

| Field | Type |
|---|---|
| address | string |
| balances | WalletBalance[] |
| currency | string |
| pushTokens | string[] |

### WalletBalance
| Field | Type |
|---|---|
| tokenSymbol | string |
| tokenAddress | string |
| balance | string |
| chainId | number |

### Transaction
Collection: `transactions/{txHash}`

| Field | Type |
|---|---|
| txHash | string |
| from | string |
| to | string |
| amount | string |
| tokenSymbol | string |
| chainId | number |
| state | TransactionState |
| kind | TransactionKind |
| createdAt | timestamp |
| updatedAt | timestamp |

## App Types

### SendState
Type union defined in `@/types/index.ts`:

```
"method" | "amount" | "recipient" | "review" | "auth" | "sending" | "sent"
```

### SendMethod
Type union defined in `@/types/index.ts`:

```
"token" | "nft" | "point"
```

### TransactionState
Defined in `lib/transactions.ts`:

```
"pending" | "confirmed" | "failed"
```

### TransactionKind
Defined in `lib/transactions.ts`:

```
"send" | "swap" | "receive"
```

## Rules

- Database schema changes require a new Drizzle migration
- Run `npx drizzle-kit generate` to create migration SQL
- Never modify generated migration files
- Types auto-inferred from schema via `$inferSelect` / `$inferInsert`
