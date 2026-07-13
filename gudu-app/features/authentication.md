# Authentication Feature

## Purpose
Allow users to create or import a wallet and authenticate for transactions.

## Screens
- Splash (`/`) — Block animation, auto-redirect to home
- Home (`/home`) — Entry point after auth check

## Components
- Block — Skia animated block (splash animation)
- Button — Navigation buttons

## Hooks
- `use-Kernal.tsx` — ZeroDev ERC-4337 wallet client setup

## Stores
- `store/wallet.ts` — Wallet address, smart address, deployment status

## API Endpoints
None — wallet creation is client-side via ZeroDev.

## State Flow
1. App launch → Splash animation (2s)
2. Check existing wallet in Zustand store
3. If no wallet → Show create/import options
4. If wallet exists → Redirect to `/home`
5. Transaction auth → ZeroDev kernel client signs

## States
- Loading: Splash animation
- Error: "Failed to create wallet" with retry
- Empty: Create/import wallet options
- Success: Redirect to home

## Dependencies
- @zerodev/ecdsa-validator
- @ethersproject/shims
- react-native-get-random-values
- buffer (polyfill)

## Files
- `app/index.tsx` — Splash screen
- `hooks/use-Kernal.tsx` — Wallet client hook
- `store/wallet.ts` — Wallet state
- `entrypoint.js` — Polyfills for wallet
