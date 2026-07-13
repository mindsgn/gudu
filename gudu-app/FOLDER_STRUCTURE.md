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
│       └── pressable-card.tsx
│
├── shared/
│   └── ui/                 # Complex reusable UI organisms
│       ├── micro-interactions/  # Scroll progress
│       └── organisms/      # Skia blocks, animated header, circular progress
│
├── db/
│   ├── schema.ts           # Drizzle table definitions
│   └── client.ts           # Database connection
│
├── drizzle/                # Generated SQL migrations
│
├── lib/                    # Pure business logic (no React)
│   └── haptics.ts          # Haptic feedback utilities
│
├── theme/                  # Design tokens
│   ├── colors.ts
│   └── typography.ts
│
├── constants/              # Static data
│   ├── index.ts
│   └── backend.ts          # Backend course content
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
- New lib → `lib/new-thing.ts`
- New table → `db/schema.ts` (add to existing file)
- New type → `@types/index.ts` or feature-specific types file
