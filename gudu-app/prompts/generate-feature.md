# Generate Feature Prompt

Use this prompt when asking AI to create a new feature.

---

Read these files before starting:
- `APP_SPEC.md`
- `ARCHITECTURE.md`
- `CODING_STANDARDS.md`
- `DESIGN_SYSTEM.md`
- `TECH_STACK.md`
- `FOLDER_STRUCTURE.md`
- `AI_RULES.md`
- `features/feature-template.md`

Then create the following feature:

## Feature Name
{name}

## Description
{description}

## Requirements
{requirements}

## Screens Involved
{screens}

## Follow These Rules
1. Create feature spec in `features/{feature-name}.md`
2. Follow folder structure from `FOLDER_STRUCTURE.md`
3. Use only approved libraries from `TECH_STACK.md`
4. Reuse existing components from `components/component-library.md`
5. Use theme tokens from `DESIGN_SYSTEM.md`
6. Handle loading, error, and empty states
7. No hardcoded colors or values
8. TypeScript strict mode — no `any`
9. Pure functions in `lib/` — no React dependencies

## Output
- List all files created and modified
- Show component structure
- Show state flow
