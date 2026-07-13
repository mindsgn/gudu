# Performance Rules

## Lists

- Always use `FlashList` over `FlatList`
- Provide `estimatedItemSize` for accurate rendering
- Use `getItemType` for heterogeneous items
- Avoid inline functions in `renderItem`
- Use `keyExtractor` with stable IDs

## Images

- Use WebP format when possible
- Resize images before display
- Use `expo-image` over `Image` when available
- Lazy load off-screen images

## Re-renders

- Memoize expensive computations with `useMemo`
- Memoize callbacks passed to children with `useCallback`
- Avoid creating objects/arrays in render
- Extract shared components to reduce re-render scope

## Animations

- Use Reanimated worklets for off-thread animations
- Use Skia for GPU-accelerated visuals
- Avoid JS-thread animations during scroll
- Use `react-native-worklets` for background scheduling

## Memory

- Clean up Firestore listeners on unmount
- Cancel pending requests when component unmounts
- Limit concurrent network requests
- Use `getItemType` and stable keys for FlashList

## Bundle

- Do not add large dependencies without approval
- Tree-shake unused imports
- Use dynamic imports for heavy features
- Keep startup lean — polyfills in `entrypoint.js` only

## Startup

- Minimize synchronous work in `_layout.tsx`
- Run migrations async
- Defer non-critical initialization
- Show splash during heavy init
