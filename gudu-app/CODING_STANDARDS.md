# Coding Standards

## TypeScript

- Strict mode enabled
- No `any` types — use `unknown` and narrow
- Prefer `type` over `interface` for simple shapes
- Use `interface` for component props (e.g., `IButton`, `IChromaRing`)
- Export types alongside their implementations

## Functions

- Prefer `const` arrow functions
- No classes
- No default exports — use named exports
- Prefix custom hooks with `use`

## Naming

- Components: `PascalCase` filenames, `PascalCase` exports
- Hooks: `useCamelCase` filenames, `useCamelCase` exports
- Lib functions: `camelCase` filenames, `camelCase` exports
- Constants: `camelCase` filenames, `camelCase` exports
- Types/Interfaces: `PascalCase` (e.g., `SendState`, `IButton`)
- Files: `kebab-case.tsx` / `kebab-case.ts`

## Imports

- Use `@/*` path alias for all project imports
- Group imports: React/Expo first, third-party second, local third
- No circular dependencies

## Component Structure

```tsx
import { View } from 'react-native'
import { colors } from '@/theme/colors'

type Props = {
  // props
}

export const MyComponent = ({ prop }: Props) => {
  return (
    <View>
      {/* JSX */}
    </View>
  )
}
```

## Style Objects

- Define styles inline with `StyleSheet.create()` or as plain objects
- Reference `theme/colors.ts` and `theme/typography.ts` tokens
- No hardcoded colors — always use theme tokens
- Use theme spacing values (multiples of 4 or 8)

## Error Handling

- Every async function must have try/catch
- Every component with async data must handle loading, error, and empty states
- Never silently swallow errors — log or display them
