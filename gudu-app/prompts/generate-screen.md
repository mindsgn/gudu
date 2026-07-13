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
- `screens/screen-specifications.md`
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
2. Use Screen container component
3. Use AnimatedHeaderScrollView for scrollable content
4. Handle all states: loading, error, empty, success
5. Use FlashList for lists (not FlatList)
6. Add navigation (push/replace/back)
7. Pass route params if needed
8. No Firestore calls in screen — use hooks
9. Use theme tokens from `DESIGN_SYSTEM.md`
10. Export default component
11. Update `screens/screen-specifications.md`

## Output
- Screen file content
- Navigation code
- Component structure
- State handling
- Files modified
