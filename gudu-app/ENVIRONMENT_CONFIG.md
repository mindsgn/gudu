# Environment Config

## Structure

```
gudu-app/
├── .env                  # Local environment (gitignored)
├── .env.example          # Template (committed)
├── app.json              # Expo config
├── eas.json              # Build profiles
├── metro.config.js       # Metro bundler config
├── babel.config.js       # Babel config
├── drizzle.config.ts     # Drizzle Kit config
└── tsconfig.json         # TypeScript config
```

## Environment Variables

All prefixed with `EXPO_PUBLIC_` for client access.

| Variable | Purpose | Required |
|---|---|---|
| `EXPO_PUBLIC_0X_API_KEY` | 0x.org swap API key | Yes (for swaps) |
| `EXPO_PUBLIC_ZERODEV_ID` | ZeroDev project ID | Yes (for wallets) |

## Adding New Variables

1. Add to `.env` (local)
2. Add to `.env.example` (template, no values)
3. Add to EAS environment variables for builds
4. Reference in code as `process.env.EXPO_PUBLIC_*`

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
- Polyfills `events` module

### babel.config.js
- `babel-preset-expo`
- `inline-import` for `.sql` files
- `react-native-worklets/plugin`

### drizzle.config.ts
- Dialect: sqlite
- Driver: expo
- Schema: `./db/schema.ts`
- Output: `./drizzle`
