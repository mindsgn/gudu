# Generate Screen Prompt

Use this prompt when asking AI to create a new screen.

---

Read these files before starting:
- `APP_SPEC.md`
- `ARCHITECTURE.md`
- `CODING_STANDARDS.md`
- `DESIGN_SYSTEM.md`
- `TECH_STACK.md`
- `FOLDER_STRUCTURE.md`
- `NAVIGATION_SPEC.md`
- `AI_RULES.md`

Then create the following screen:

## Screen Name
{name}

## Route
{route}

## Description
{description}

## Layout
{layout}

## Data Requirements
{data}

## Follow These Rules
1. Create `app/{route}.tsx`
2. Use AnimatedHeaderScrollView for scrollable content
3. Handle all states: loading, error, empty, success
4. Use FlashList for lists (not FlatList)
5. Add navigation (push/replace/back)
6. Pass route params if needed
7. Use theme tokens from `DESIGN_SYSTEM.md`
8. Export default component

## Output
- Screen file content
- Navigation code
- Component structure
- State handling
- Files modified
