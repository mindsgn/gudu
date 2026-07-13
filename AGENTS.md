# AGENTS.md

## Repo Layout

- `gudu-app/` — Expo (React Native) mobile app. The only runnable codebase.
- `backend-engineering/` — Auto-generated backend curriculum (105 markdown chapters). **Do not edit by hand.**
- `frontend-engineering/` — Auto-generated frontend curriculum (180 markdown chapters). **Do not edit by hand.**
- `scripts/generate_backend_curriculum.py` / `scripts/generate_frontend_curriculum.py` — Python scripts that regenerate the curriculum. Run from repo root.
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

These overwrite `backend-engineering/*.md` and `frontend-engineering/*.md`. Never hand-edit generated files.

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
