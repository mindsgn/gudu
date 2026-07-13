# Deployment

## Build System

EAS Build (Expo Application Services).

## Profiles

| Profile | Purpose | Distribution |
|---|---|---|
| development | Local dev with dev tools | Internal |
| preview | Testing builds | Internal |
| production | App Store / Play Store | Store |

## Commands

```bash
# Development
eas build --profile development --platform ios
eas build --profile development --platform android

# Preview
eas build --profile preview

# Production
eas build --profile production
```

## Versioning

- Managed by EAS (`appVersionSource: remote`)
- Auto-increment on production builds
- Version in `app.json` and `eas.json`

## Bundle Identifiers

- iOS: `mindsgn.studio.backend`
- Android: `mindsgn.studio.backend`

## Release Process

1. Test on preview build
2. Update version if needed
3. Build production profile
4. Submit to App Store / Play Store
5. Monitor crash reports

## Requirements

- EAS CLI >= 20.1.0
- Apple Developer account (iOS)
- Google Play Developer account (Android)
- Expo account
