# Generate Component Prompt

Use this prompt when asking AI to create a new component.

---

Read these files before starting:
- `CODING_STANDARDS.md`
- `DESIGN_SYSTEM.md`
- `components/component-library.md`
- `FOLDER_STRUCTURE.md`
- `AI_RULES.md`

Then create the following component:

## Component Name
{name}

## Description
{description}

## Props
{props}

## Visual Design
{visual-description}

## Follow These Rules
1. Check existing components — do not duplicate
2. Choose location:
   - Simple: `components/shared/{name}.tsx`
   - Complex animated: `shared/ui/organisms/{name}/index.tsx`
3. Use named export (not default)
4. Define props interface as `I{Name}` for complex, `Props` for simple
5. Use theme tokens from `theme/colors.ts` and `theme/typography.ts`
6. No hardcoded colors, font sizes, or spacing
7. No business logic — pure presentation
8. Handle all prop edge cases
9. TypeScript strict — no `any`
10. Follow file naming: `kebab-case.tsx`

## Output
- Component file content
- Types file content (if complex)
- Config file content (if needed)
- Usage example
