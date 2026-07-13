// Mock expo-haptics
jest.mock("expo-haptics", () => ({
  impactAsync: jest.fn(() => Promise.resolve()),
  notificationAsync: jest.fn(() => Promise.resolve()),
  ImpactFeedbackStyle: {
    Light: "light",
    Medium: "medium",
    Heavy: "heavy",
    Rigid: "rigid",
    Soft: "soft",
  },
  NotificationFeedbackType: {
    Success: "success",
    Warning: "warning",
    Error: "error",
  },
}));

// Mock @shopify/react-native-skia
jest.mock("@shopify/react-native-skia", () => ({
  Canvas: "Canvas",
  Shader: "Shader",
  Fill: "Fill",
  Skia: {
    RuntimeEffect: {
      Make: jest.fn(() => ({})),
    },
  },
}));

// Mock react-native-reanimated
jest.mock("react-native-reanimated", () => {
  const mockSharedValue = (v) => ({ value: v });
  return {
    __esModule: true,
    default: {
      View: "AnimatedView",
      Text: "AnimatedText",
      ScrollView: "AnimatedScrollView",
      createAnimatedComponent: (c) => c,
    },
    useSharedValue: mockSharedValue,
    useAnimatedStyle: (fn) => fn(),
    useDerivedValue: (fn) => fn(),
    useAnimatedScrollHandler: (config) => config,
    useAnimatedProps: (fn) => fn(),
    withRepeat: (v) => v,
    withTiming: (v) => v,
    withSpring: (v) => v,
    interpolate: (v) => v,
    Extrapolation: { CLAMP: "clamp" },
    Easing: {
      linear: "linear",
      bezier: () => "bezier",
      bezierFn: () => "bezierFn",
    },
    interpolateColor: (v) => v,
  };
});

// Mock react-native-gesture-handler
jest.mock("react-native-gesture-handler", () => ({
  GestureHandlerRootView: "GestureHandlerRootView",
}));

// Mock expo-router
jest.mock("expo-router", () => {
  const React = require("react");
  const router = {
    replace: jest.fn(),
    push: jest.fn(),
    back: jest.fn(),
  };

  return {
    useRouter: () => router,
    useFocusEffect: (cb) => {
      React.useEffect(() => cb(), [cb]);
    },
    useLocalSearchParams: jest.fn(() => ({})),
    Stack: {
      Screen: "StackScreen",
    },
  };
});

// Mock expo-blur
jest.mock("expo-blur", () => ({
  BlurView: "BlurView",
}));

// Mock expo-linear-gradient
jest.mock("expo-linear-gradient", () => ({
  LinearGradient: "LinearGradient",
}));

// Mock @react-native-masked-view/masked-view
jest.mock("@react-native-masked-view/masked-view", () => ({
  __esModule: true,
  default: "MaskedView",
}));

// Mock react-native-easing-gradient
jest.mock("react-native-easing-gradient", () => ({
  easeGradient: (config) => {
    const colors = Object.values(config.colorStops).map((s) => s.color);
    const locations = Object.keys(config.colorStops).map(Number);
    return { colors, locations };
  },
}));

// Mock react-native-safe-area-context
jest.mock("react-native-safe-area-context", () => ({
  useSafeAreaInsets: () => ({ top: 0, bottom: 0, left: 0, right: 0 }),
}));

// Mock expo-symbols
jest.mock("expo-symbols", () => ({
  SymbolView: "SymbolView",
}));

// Mock react-native-enriched-markdown
jest.mock("react-native-enriched-markdown", () => ({
  EnrichedMarkdownText: "EnrichedMarkdownText",
}));

// Mock @shopify/flash-list
jest.mock("@shopify/flash-list", () => ({
  FlashList: ({ data = [], renderItem, ListHeaderComponent, testID }) => {
    const React = require("react");
    const { View } = require("react-native");
    const header =
      typeof ListHeaderComponent === "function"
        ? React.createElement(ListHeaderComponent)
        : ListHeaderComponent;

    return React.createElement(
      View,
      { testID },
      header,
      data.map((item, index) =>
        React.createElement(
          View,
          { key: item?.id ?? `${index}` },
          renderItem({ item, index }),
        ),
      ),
    );
  },
}));

// Mock expo-sqlite
jest.mock("expo-sqlite", () => ({
  openDatabaseSync: jest.fn(() => ({})),
  SQLiteProvider: "SQLiteProvider",
}));

// Mock drizzle-orm
jest.mock("drizzle-orm/expo-sqlite", () => ({
  drizzle: jest.fn(() => ({})),
}));

jest.mock("drizzle-orm/expo-sqlite/migrator", () => ({
  useMigrations: jest.fn(() => ({ success: true, error: null })),
}));

jest.mock("drizzle-orm/sqlite-core", () => ({
  sqliteTable: jest.fn((name, columns) => ({ name, columns })),
  text: jest.fn(() => ({})),
  integer: jest.fn(() => ({})),
  real: jest.fn(() => ({})),
}));

// Mock @/drizzle/migrations
jest.mock("@/drizzle/migrations", () => ({
  default: { journal: {}, migrations: {} },
}));

// Mock react-native
jest.mock("react-native", () => {
  const RN = jest.requireActual("react-native");
  RN.Dimensions = { get: () => ({ width: 375, height: 812 }) };
  return RN;
});
