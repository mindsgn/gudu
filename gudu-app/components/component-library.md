# Component Library

## Shared Primitives (`components/shared/`)

Simple, single-purpose components used across screens.

### Screen
Container for all screens. Handles safe area and background.
- Props: `children`
- Style: `flex: 1`, `paddingTop: 48`, `backgroundColor: colors.background`

### Title
Large bold text for screen titles.
- Props: `children`
- Style: `typography.title`

### Subtitle
Section header text.
- Props: `children`
- Style: `typography.subtitle`

### Body
Centered body text.
- Props: `children`
- Style: `typography.body`

### Text
General body text wrapper.
- Props: `children`
- Style: `typography.body`

### Balance
Large balance display text.
- Props: `children`
- Style: `typography.balance`

### Button
Primary action button with haptic feedback.
- Props: `title`, `onPress`
- Style: `typography.button`, `colors.buttonBackground`, `colors.buttonTextBackground`
- Includes haptic feedback on press

### SubButton
Pill-shaped secondary action button.
- Props: `title`, `onPress`
- Style: pill shape, `borderRadius: 999`, border

### Card
Content container card.
- Props: `children`
- Style: `colors.surface` background, `borderRadius: 12`

### PressableCard
Button variant with flex-start alignment.
- Props: `title`, `onPress`
- Same as Button but `alignItems: flex-start`

### HapticPressable
Pressable wrapper with haptic feedback.
- Props: `onPress`, `children`, haptic type
- Wraps `expo-haptics`

### Block
Simple white square block (100x100, radius 20).
- Props: `children`
- Style: white background, `borderRadius: 20`

## Complex Organisms (`shared/ui/organisms/`)

Advanced components with animations and shaders.

### AnimatedHeaderScrollView
iOS-style large title scroll view with blur effects.
- Large title fades/scales on scroll
- Small header fades in
- Uses `expo-blur`, `MaskedView`, `react-native-easing-gradient`
- Props: `title`, `children`, header height config

### Block (Skia)
Animated block with liquid metal border shader.
- Props: `width`, `height`, `borderRadius`, `borderWidth`, `speed`, `baseColor`, `glowColor`, `background`
- Uses `@shopify/react-native-skia`

### ChromaRing
Animated ring with liquid metal shader.
- Props: similar to Block
- Uses `@shopify/react-native-skia`

### EnergyOrb
Animated glowing orb with configurable colors.
- Props: `colors[]`, `speed`, `intensity`, `glowRadius`
- Uses `@shopify/react-native-skia`

### GrainyGradient
Animated grainy gradient background.
- Props: `colors[]` (up to 5), grain settings
- Uses `@shopify/react-native-skia`

### AnimatedScrollProgress
ScrollView wrapper with floating FAB tracking scroll progress.
- Props: `children`, `onEndReached`, initial/end content
- Uses `react-native-worklets`

### CircularProgress
Animated SVG circular progress indicator.
- Props: `progress` (SharedValue 0-100), `renderIcon`
- Uses `react-native-svg`

### Checkbox
Animated SVG checkbox with spring scale.
- Props: `checked`, `onChange`
- Uses `react-native-svg`

## Rules

- Never create custom versions of these components
- Reuse existing components before creating new ones
- Add new shared components to `components/shared/`
- Add complex animated components to `shared/ui/organisms/`
- Each organism gets its own folder: `index.tsx`, `types.ts`, `conf.ts`
