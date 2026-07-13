# Component Library

## Shared Primitives (`components/shared/`)

Simple, single-purpose components used across screens.

### PressableCard
Button variant with flex-start alignment.
- Props: `label`, `onPress`, `width`, `backgroundColor`, `color`
- Style: `typography.button`, `colors.buttonBackground`, `colors.buttonTextBackground`
- Includes haptic feedback on press

## Complex Organisms (`shared/ui/organisms/`)

Advanced components with animations and shaders.

### AnimatedHeaderScrollView
iOS-style large title scroll view with blur effects.
- Large title fades/scales on scroll
- Small header fades in
- Uses `expo-blur`, `MaskedView`, `react-native-easing-gradient`
- Props: `largeTitle`, `subtitle`, `children`, header height config

### Block (Skia)
Animated block with liquid metal border shader.
- Props: `width`, `height`, `borderRadius`, `borderWidth`, `speed`, `base`, `glow`, `background`
- Uses `@shopify/react-native-skia`

### AnimatedScrollProgress
ScrollView wrapper with floating FAB tracking scroll progress.
- Props: `children`, `onScrollProgressChange`, initial/end content
- Uses `react-native-worklets`

### CircularProgress
Animated SVG circular progress indicator.
- Props: `progress` (SharedValue 0-100), `renderIcon`, `size`, `strokeWidth`
- Uses `react-native-svg`

## Rules

- Never create custom versions of these components
- Reuse existing components before creating new ones
- Add new shared components to `components/shared/`
- Add complex animated components to `shared/ui/organisms/`
- Each organism gets its own folder: `index.tsx`, `types.ts`, `conf.ts`
