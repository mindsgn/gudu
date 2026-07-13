# Environment Config

## Structure

```
gudu-app/
├── app.json              # Expo config
├── eas.json              # Build profiles
├── metro.config.js       # Metro bundler config
├── babel.config.js       # Babel config
├── drizzle.config.ts     # Drizzle Kit config
└── tsconfig.json         # TypeScript config
```

## Environment Variables

No environment variables required for core functionality.

## Config Files

### app.json
- App name: GUDU
- Slug: gudu
- Orientation: portrait
- Bundle ID: mindsgn.studio.backend

### eas.json
- CLI >= 20.1.0
- appVersionSource: remote

### metro.config.js
- Forces `jose` to resolve with `browser` condition
- Adds `.sql` source extension

### babel.config.js
- `babel-preset-expo`
- `inline-import` for `.sql` files
- `react-native-worklets/plugin`

### drizzle.config.ts
- Dialect: sqlite
- Driver: expo
- Schema: `./db/schema.ts`
- Output: `./drizzle`
