# App Specification

## Purpose

Gudu is a mobile crypto wallet and learning platform. Users manage digital assets on the Base chain, send/receive tokens, swap tokens, and take blockchain development courses.

## Platforms

- iOS (primary)
- Android

## Framework

Expo SDK 56 + React Native 0.85.3

## Core Features

1. **Wallet Management** — Create/import wallets, view balances, manage multiple wallets
2. **Token Sending** — Multi-step send flow (method > amount > recipient > review > auth > sending > sent)
3. **Token Swapping** — Swap tokens via 0x.org DEX aggregator on Base chain
4. **Learning Platform** — Blockchain development courses with progress tracking
5. **Push Notifications** — Transaction updates and learning reminders

## User Journeys

### First Launch
Splash animation > Home screen > Create/import wallet

### Send Tokens
Home > Select token > Enter amount > Enter recipient > Review > Authenticate > Sending > Sent confirmation

### Learn
Home > Course list > Lesson > Read with scroll progress > Completion

## Business Rules

- All transactions are on Base chain (chain ID 8453)
- Smart contract wallets via ZeroDev ERC-4337 (account abstraction)
- User data stored locally (SQLite) and synced to Firestore
- Currency preferences stored per wallet

## Target Users

- Crypto-native users on Base chain
- Blockchain developers learning through the app
- Users who want a clean, minimal wallet experience
