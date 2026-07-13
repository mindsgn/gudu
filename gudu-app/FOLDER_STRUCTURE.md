# Folder Structure

```
gudu-app/
├── app/
│   ├── _layout.tsx
│   ├── index.tsx
│   ├── home.tsx
│   ├── course.tsx
│   ├── backend.tsx
│   ├── lesson.tsx
│   └── complete.tsx
│
├── components/
│   └── shared/
│       ├── pressable-card.tsx
│       ├── state-panel.tsx
│       ├── course-card.tsx
│       └── lesson-list-item.tsx
│
├── shared/
│   └── ui/
│       ├── micro-interactions/
│       │   └── animated-scroll-progress/
│       └── organisms/
│           ├── activity-heatmap/
│           ├── animated-header-scrollview/
│           ├── block/
│           └── circular-progress/
│
├── db/
│   ├── schema.ts
│   ├── client.ts
│   └── learning.ts
│
├── drizzle/
│   ├── migrations.js
│   └── *.sql
│
├── lib/
│   ├── activity-heatmap.ts
│   ├── continue-target.ts
│   ├── haptics.ts
│   ├── lesson-progress.ts
│   ├── points.ts
│   └── streaks.ts
│
├── constants/
│   ├── index.ts
│   ├── backend.ts
│   └── curriculum.ts
│
├── @types/
│   └── index.ts
│
├── __tests__/
│   ├── app/
│   ├── lib/
│   ├── shared/
│   ├── constants/
│   └── theme/
│
├── screens/
│   └── screen-specifications.md
│
└── .maestro/
    └── *.yaml
```

## Adding New Files

- New route → `app/new-route.tsx`
- New shared primitive → `components/shared/new-component.tsx`
- New complex UI organism → `shared/ui/organisms/new-component/`
- New pure helper → `lib/new-helper.ts`
- New data access helper → `db/new-helper.ts`
- New shared type → `@types/index.ts` or a colocated feature type file
