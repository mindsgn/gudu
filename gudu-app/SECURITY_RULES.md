# Security Rules

## Token Storage

- Never store private keys in AsyncStorage or SQLite
- Use `expo-securestore` for sensitive data (when adopted)
- ZeroDev handles key management via ERC-4337

## Secrets

- Environment variables via `EXPO_PUBLIC_*` prefix only
- Never log API keys, tokens, or secrets
- Never commit `.env` files
- `.env` is in `.gitignore`

### Known Secrets
| Variable | Purpose |
|---|---|
| `EXPO_PUBLIC_0X_API_KEY` | 0x.org swap API |
| `EXPO_PUBLIC_ZERODEV_ID` | ZeroDev project ID |

## Data Handling

- Wallet addresses are public — safe to store/display
- Transaction hashes are public — safe to store/display
- User balances are sensitive — encrypt at rest if needed
- Push notification tokens — store securely, delete on logout

## Network

- All external calls use HTTPS
- Firebase SDK handles auth and encryption
- No custom certificates

## Permissions

- Request minimum necessary permissions
- Document why each permission is needed
- Handle permission denial gracefully

## Code Rules

- Never hardcode secrets in source code
- Never expose private keys in logs or error messages
- Sanitize user input before display
- Validate all data from external sources
