# Development Workflow

## Adding a New Feature

1. Read `features/feature-template.md` for structure
2. Create feature spec in `features/your-feature.md`
3. Review architecture impact
4. Identify files to create and modify
5. Implement in this order:
   a. Types (`@types/` or feature types)
   b. Lib functions (`lib/`)
   c. Hooks (`hooks/`)
   d. Store (`store/`) if needed
   e. Components (`components/shared/` or `shared/ui/`)
   f. Screen (`app/`)
6. Test all states (loading, error, empty, success)
7. Update this workflow if new patterns emerge

## Adding a New Screen

1. Create `app/screen-name.tsx`
2. Use Screen container component
3. Add AnimatedHeaderScrollView if scrollable
4. Handle all states (loading, error, empty, success)
5. Add navigation from existing screen
6. Update `screens/screen-specifications.md`

## Adding a New Component

### Simple (shared primitive)
1. Check `components/component-library.md` for existing
2. Create `components/shared/component-name.tsx`
3. Define props interface
4. Use theme tokens only
5. Update component library docs

### Complex (animated organism)
1. Create folder: `shared/ui/organisms/component-name/`
2. Create `index.tsx`, `types.ts`, `conf.ts`
3. Use Skia/Reanimated as needed
4. Update component library docs

## Adding a New Hook

1. Check `hooks/` for existing patterns
2. Create `hooks/use-thing-name.ts`
3. Return `{ data, loading, error }` shape
4. Clean up listeners on unmount
5. No Firestore calls in components

## Adding a New Table

1. Edit `db/schema.ts`
2. Generate migration: `npx drizzle-kit generate`
3. Review generated SQL in `drizzle/`
4. Do not modify migration files
5. Update `DATA_MODELS.md`

## Adding a New Dependency

1. Check `TECH_STACK.md` — is it already approved?
2. If not, ask user for approval
3. Install: `npx expo install package-name`
4. Update `TECH_STACK.md`
5. Update `package.json`

## Code Review Checklist

- [ ] Follows `CODING_STANDARDS.md`
- [ ] Uses theme tokens from `DESIGN_SYSTEM.md`
- [ ] Handles loading, error, empty states
- [ ] No hardcoded colors or values
- [ ] No new dependencies added
- [ ] Types defined and exported
- [ ] Follows file naming conventions
- [ ] Uses `@/*` path alias
- [ ] No `any` types
- [ ] Error handling for async operations
