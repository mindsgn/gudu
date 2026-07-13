# Profile Feature

## Purpose
Display user wallet information, balances, and settings.

## Screens
- Home (`/home`) — Main profile/balance view

## Components
- AnimatedHeaderScrollView — Large title scroll view with blur
- FlashList — Balance list
- Balance — Balance text display
- Card — Content container
- SubButton — Action buttons

## Hooks
- `use-wallet-balances.ts` — Real-time Firestore balance listener

## Lib Functions
- `lib/wallet.ts` — getActiveWalletAddress, shortenAddress
- `lib/firebase.ts` — getWallet, getWalletSettings

## Stores
- `store/wallet.ts` — Active wallet data

## State Flow
1. Home screen mounts
2. Hook subscribes to Firestore balance updates
3. Balances update in real-time
4. User can tap actions (send, swap, settings)

## States
- Loading: Skeleton/spinner in FlashList
- Error: "Failed to load balances" with retry
- Empty: "No wallets yet" with create option
- Success: Balance list with amounts

## Files
- `app/home.tsx` — Home screen
- `hooks/use-wallet-balances.ts` — Balance hook
- `lib/wallet.ts` — Wallet utilities
- `components/shared/balance.tsx` — Balance display
