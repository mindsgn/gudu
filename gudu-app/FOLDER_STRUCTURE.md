# Folder Structure

```
gudu-app/
├── app/                    # Expo Router routes (file-based)
│   ├── _layout.tsx         # Root layout (SQLite, GestureHandler, Stack)
│   ├── index.tsx           # Splash screen
│   ├── home.tsx            # Home screen
│   ├── backend.tsx         # Course list
│   ├── lesson.tsx          # Lesson reader
│   └── complete.tsx        # Completion screen
│
├── components/
│   └── shared/             # Simple shared UI primitives
│       ├── balance.tsx
│       ├── block.tsx
│       ├── body.tsx
│       ├── button.tsx
│       ├── card.tsx
│       ├── haptic-pressable.tsx
│       ├── pressable-card.tsx
│       ├── screen.tsx
│       ├── sub-button.tsx
│       ├── text.tsx
│       └── title.tsx
│
├── shared/
│   └── ui/                 # Complex reusable UI organisms
│       ├── base/           # Base components (animated button)
│       ├── micro-interactions/  # Scroll progress, etc.
│       └── organisms/      # Skia blocks, rings, orbs, gradients
│
├── db/
│   ├── schema.ts           # Drizzle table definitions
│   └── client.ts           # Database connection
│
├── drizzle/                # Generated SQL migrations
│
├── hooks/                  # Custom React hooks
│   ├── shorten-address.ts
│   ├── use-Kernal.tsx
│   └── use-wallet-balances.ts
│
├── lib/                    # Pure business logic (no React)
│   ├── amount.ts
│   ├── firebase.ts
│   ├── haptics.ts
│   ├── swap.ts
│   ├── transactions.ts
│   └── wallet.ts
│
├── store/                  # Zustand stores
│   ├── wallet.ts
│   └── send.ts
│
├── theme/                  # Design tokens
│   ├── colors.ts
│   └── typography.ts
│
├── constants/              # Static data
│   ├── index.ts
│   └── backend.ts
│
├── @types/                 # Shared TypeScript types
│   └── index.ts
│
└── assets/                 # Images, icons, splash
```

## Adding New Files

- New route → `app/new-route.tsx`
- New shared primitive → `components/shared/new-component.tsx`
- New complex UI → `shared/ui/organisms/new-component/` (index.tsx, types.ts, conf.ts)
- New hook → `hooks/use-new-thing.ts`
- New lib → `lib/new-thing.ts`
- New store → `store/new-thing.ts`
- New table → `db/schema.ts` (add to existing file)
- New type → `@types/index.ts` or feature-specific types file
