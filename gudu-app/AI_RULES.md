# AI Rules

## Before Generating Code

1. Read these files first:
   - `APP_SPEC.md` — understand the app
   - `ARCHITECTURE.md` — understand code organization
   - `CODING_STANDARDS.md` — follow code style
   - `DESIGN_SYSTEM.md` — use correct tokens
   - `TECH_STACK.md` — use approved libraries only
   - `FOLDER_STRUCTURE.md` — place files correctly

2. Check existing code for similar patterns before writing new code

3. Ask questions if requirements are unclear

## Code Generation Rules

### Architecture
- Follow existing folder structure exactly
- Do not introduce new directories without approval
- Place new code in the correct location per `FOLDER_STRUCTURE.md`
- Do not create circular dependencies

### Dependencies
- Do not add new npm packages without approval
- Use only libraries listed in `TECH_STACK.md`
- Check `package.json` before assuming a library exists

### Components
- Reuse existing components from `components/shared/` and `shared/ui/`
- Do not create duplicate components
- Follow component structure in `CODING_STANDARDS.md`
- Handle loading, error, and empty states

### State
- Use correct state tool per `STATE_MANAGEMENT.md`
- Do not create Zustand stores for local UI state
- Keep Firestore calls in `lib/` — not in components

### Styling
- Use theme tokens from `theme/colors.ts` and `theme/typography.ts`
- No hardcoded colors or font sizes
- Follow spacing system (4px base unit)
- Follow component tokens in `DESIGN_SYSTEM.md`

### Types
- TypeScript strict mode — no `any`
- Define types before use
- Export types for reuse

### Error Handling
- Every async function needs try/catch
- Every screen needs loading/error/empty states
- Never silently swallow errors

## What NOT To Do

- Do not refactor existing code unless asked
- Do not change architecture without asking
- Do not add comments unless asked
- Do not add tests unless asked
- Do not modify build configs without asking
- Do not change file naming conventions
- Do not add logging unless asked
- Do not create documentation files unless asked

## When Uncertain

- Ask the user before making assumptions
- Show the plan before implementing
- Request clarification on ambiguous requirements
