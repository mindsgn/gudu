# Security Rules

## Data Handling

- User data stored locally in SQLite
- No remote data synchronization
- No sensitive data transmitted over network

## Code Rules

- Never hardcode secrets in source code
- Sanitize user input before display
- Validate all data from external sources

## Network

- No external API calls required for core functionality
- All course content bundled with the app
