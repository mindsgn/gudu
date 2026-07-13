# Technology Stack

## Locked Choices

Do not introduce new libraries without explicit approval.

### Framework
- Expo SDK 56
- React Native 0.85.3
- React 19.2.3
- TypeScript (strict mode)

### Routing
- Expo Router (file-based, Stack navigator)

### UI
- @shopify/react-native-skia (animations, shaders)
- react-native-reanimated (animations)
- react-native-gesture-handler (gestures)
- @shopify/flash-list (lists)
- react-native-svg (icons, progress)
- expo-linear-gradient (gradients)
- expo-blur (blur effects)
- react-native-easing-gradient (fade gradients)
- react-native-enriched-markdown (markdown rendering)
- @expo/vector-icons (icons)
- react-native-worklets (background scheduling)

### State
- Zustand (global client state)

### Database
- expo-sqlite (local storage)
- drizzle-orm (query builder + migrations)

### Backend
- Firebase/Firestore (remote sync, wallet data, transactions)

### Blockchain
- ethers (address utilities)
- @zerodev/ecdsa-validator (ERC-4337 wallets)
- viem (token amount parsing)
- 0x.org API (token swaps)

### Forms & Validation
- Not yet adopted. Do not add without approval.

### Build
- EAS Build (iOS + Android)
- babel-plugin-inline-import (.sql files)
- react-native-worklets/plugin (Babel)
