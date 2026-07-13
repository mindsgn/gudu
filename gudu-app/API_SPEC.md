# API Spec

## Backend

No custom backend server. All remote data via Firebase/Firestore.

## Firebase/Firestore

### Connection
- Config in `lib/firebase.ts`
- Uses `@react-native-firebase/firestore`

### Collections

| Collection | Document ID | Fields |
|---|---|---|
| `wallets` | `{address}` | balances[], currency, push tokens |
| `transactions` | `{txHash}` | from, to, amount, token, state, chainId, timestamps |

### Operations

| Function | File | Purpose |
|---|---|---|
| `upsertWallet` | lib/firebase.ts | Create/update wallet document |
| `getWallet` | lib/firebase.ts | Fetch wallet data |
| `getTransaction` | lib/firebase.ts | Fetch single transaction |
| `getWalletSettings` | lib/firebase.ts | Fetch wallet preferences |
| `setWalletCurrencyPreference` | lib/firebase.ts | Update currency |
| `hasPushNotificationDetails` | lib/firebase.ts | Check push registration |
| `savePushNotificationDetails` | lib/firebase.ts | Register push token |
| `deletePushNotificationDetails` | lib/firebase.ts | Unregister push |
| `createPendingTransaction` | lib/transactions.ts | Record pending tx |
| `updateTransaction` | lib/transactions.ts | Update tx state |
| `finalizeTransaction` | lib/transactions.ts | Mark tx complete |

## External APIs

### 0x.org (Token Swaps)
- File: `lib/swap.ts`
- Endpoint: `https://api.0x.org/swap/permit2/quote`
- Auth: `EXPO_PUBLIC_0X_API_KEY` header
- Chain: Base (8453)

## API Rules

- All Firestore calls go through `lib/` functions
- Components never call Firestore directly
- Hooks wrap lib functions with loading/error states
- Handle network errors gracefully
- Retry failed requests once before showing error
