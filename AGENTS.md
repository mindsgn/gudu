# AGENTS.md

## Repo Layout

- `gudu-app/` — Expo (React Native) mobile app. The only runnable codebase.
- `backend-engineering/` / `frontend-engineering/` — Auto-generated curriculum markdown. **Do not edit by hand.**
- `scripts/generate_backend_curriculum.py` / `scripts/generate_frontend_curriculum.py` — Regenerate the curriculum from repo root.
- `lessons/` — Index files pointing into the generated curricula.

## gudu-app — Key Facts

- **Expo SDK 56** · React Native 0.85.3 · React 19.2.3
- **Entry point**: `entrypoint.js` (not App.tsx). It polyfills Buffer, random values, shims, then imports `expo-router/entry`.
- **Routing**: file-based via `expo-router`. Routes live in `app/`.
- **Database**: local SQLite via `expo-sqlite` + `drizzle-orm`. Schema: `db/schema.ts`. Migrations: `drizzle/`. Client: `db/client.ts` (db name: `afika.db`).
- **State**: Zustand (`store/wallet.ts`, `store/send.ts`).
- **External services**: Firebase/Firestore (`lib/firebase.ts`), wallet/blockchain (ethers, zerodev).
- **Path alias**: `@/*` resolves to project root (e.g., `@/db/client`).
- **Shared UI**: `shared/ui/` (organisms, base, micro-interactions), `components/shared/`.
- **Theme**: `theme/colors.ts`, `theme/typography.ts`.

## Dev Commands

All commands run inside `gudu-app/`:

```
npx expo start          # start dev server
npx expo run:ios        # build and run on iOS
npx expo run:android    # build and run on Android
npx expo start --web    # web dev server
```

There are **no lint, typecheck, or test scripts** configured. TypeScript is in `tsconfig.json` (strict mode) but there is no `npm run typecheck` or similar. If you need type checking, run `npx tsc --noEmit` from `gudu-app/`.

## Regenerating Curriculum

From repo root:

```bash
python3 scripts/generate_backend_curriculum.py
python3 scripts/generate_frontend_curriculum.py
```

These overwrite `backend-engineering/*.md` and `frontend-engineering/*.md`.

## Metro & Babel Quirks

- `metro.config.js` forces the `jose` package to resolve with `browser` condition names. This is intentional — don't remove.
- `.sql` files are importable via `babel-plugin-inline-import` (used for Drizzle raw SQL).
- `events` is polyfilled through Metro's `extraNodeModules`.

## Build / Deploy

- iOS builds use EAS (`eas.json`). Configs: `development`, `preview`, `production`.
- EAS CLI requirement: `>= 20.1.0`.
- Bundle identifier: `mindsgn.studio.backend`.
- `.gitignore` excludes `ios/`, `android/`, `.env`, `node_modules`. Native platform dirs are not in the repo.

## Things That Look Wrong But Aren't

- `smartAdress` (no 'r') is used consistently across the codebase — it's an established field name, not a typo to fix.
- `app.json` says `"name": "BACKEND"` and `"slug": "backend"` but the package.json name is `"afika"`. Both are correct.

## Specification System

All specs live in `gudu-app/`. Read these before generating any code.

### Core Specs
- `APP_SPEC.md` — App purpose, features, user journeys
- `ARCHITECTURE.md` — Code organization, separation of concerns
- `CODING_STANDARDS.md` — TypeScript, naming, component structure
- `TECH_STACK.md` — Locked technology choices (do not add new libs)
- `FOLDER_STRUCTURE.md` — Exact file locations
- `AI_RULES.md` — Rules AI must follow when generating code

### UI Specs
- `DESIGN_SYSTEM.md` — Colors, typography, spacing, component tokens
- `UI_GUIDELINES.md` — Layout rules, accessibility, animations
- `NAVIGATION_SPEC.md` — Route structure, screen options

### Data Specs
- `STATE_MANAGEMENT.md` — What state goes where
- `API_SPEC.md` — Firestore collections, external APIs
- `DATA_MODELS.md` — SQLite schema, Firestore documents, app types

### Quality Specs
- `SECURITY_RULES.md` — Token storage, secrets, permissions
- `ERROR_HANDLING.md` — Error categories, component patterns
- `PERFORMANCE_RULES.md` — Lists, animations, memory
- `TESTING_STRATEGY.md` — Test coverage targets

### Operations
- `DEPLOYMENT.md` — EAS Build, versioning, release
- `ENVIRONMENT_CONFIG.md` — Env vars, config files

### Feature Specs
- `features/feature-template.md` — Template for new features
- `features/authentication.md` — Wallet creation, auth
- `features/profile.md` — Balances, wallet info
- `features/payments.md` — Send, swap, transactions

### Component & Screen Specs
- `components/component-library.md` — All reusable components
- `screens/screen-specifications.md` — All screen layouts

### Development Workflow
- `docs/decisions/architecture-decisions.md` — ADRs
- `docs/workflows/development-workflow.md` — How to add features, screens, components

### Prompt Templates
- `prompts/generate-feature.md` — Feature generation prompt
- `prompts/generate-component.md` — Component generation prompt
- `prompts/generate-screen.md` — Screen generation prompt

### Before Generating Code
1. Read `AI_RULES.md`
2. Read relevant spec files for the task
3. Check `components/component-library.md` for existing components
4. Check `TECH_STACK.md` for approved libraries
5. Follow `CODING_STANDARDS.md` and `DESIGN_SYSTEM.md`
6. Place files per `FOLDER_STRUCTURE.md`
