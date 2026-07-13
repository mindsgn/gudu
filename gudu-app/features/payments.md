# Payments Feature

## Purpose
Send tokens, swap tokens, and view transaction history.

## Screens
- Send flow (multi-step, not yet implemented as separate screens)
- Lesson (`/lesson`) — Uses transaction data for progress

## Components
- Button — Action buttons for send/swap
- CircularProgressBar — Transaction progress indicator
- AnimatedScrollProgress — Scroll-based progress

## Hooks
- `use-Kernal.tsx` — Wallet client for signing
- `use-wallet-balances.ts` — Balance checking

## Lib Functions
- `lib/amount.ts` — parseTokenAmount, formatTokenAmount, amountExceedsBalance
- `lib/swap.ts` — getSwapQuote (0x.org)
- `lib/transactions.ts` — createPendingTransaction, updateTransaction, finalizeTransaction
- `lib/firebase.ts` — upsertWallet, getTransaction

## Stores
- `store/send.ts` — Send flow state machine (nextState/prevState)
- `@/types/index.ts` — SendState, SendMethod types

## API Endpoints
- 0x.org: `GET /swap/permit2/quote` — Token swap quotes

## State Flow (Send)
1. Select method (token/nft/point) → "method"
2. Enter amount → "amount"
3. Enter recipient → "recipient"
4. Review details → "review"
5. Authenticate (biometric/PIN) → "auth"
6. Processing → "sending"
7. Complete → "sent"

## State Flow (Swap)
1. Select tokens
2. Get quote from 0x.org
3. Review swap details
4. Confirm and execute
5. Wait for confirmation

## States
- Loading: Spinner during transaction
- Error: "Transaction failed" with retry/details
- Empty: "No transactions yet"
- Success: Transaction confirmed with hash

## Transaction States
- `pending` — Submitted, not confirmed
- `confirmed` — Verified on chain
- `failed` — Reverted or error

## Files
- `store/send.ts` — Send state machine
- `@/types/index.ts` — Send types
- `lib/amount.ts` — Amount utilities
- `lib/swap.ts` — Swap quotes
- `lib/transactions.ts` — Transaction CRUD
