module.exports = {
  preset: "jest-expo",
  setupFiles: ["./jest.setup.js"],
  moduleNameMapper: {
    "^@/(.*)$": "<rootDir>/$1",
  },
  transformIgnorePatterns: [
    "node_modules/(?!((react-native|@react-native|react-native-reanimated|react-native-gesture-handler|react-native-svg|react-native-safe-area-context|expo|expo-.*|@expo-.*|@shopify/react-native-skia|@shopify/flash-list|react-native-easing-gradient|react-native-enriched-markdown|react-native-webview|react-native-worklets)/))",
  ],
  testMatch: ["**/__tests__/**/*.test.ts", "**/__tests__/**/*.test.tsx"],
};
