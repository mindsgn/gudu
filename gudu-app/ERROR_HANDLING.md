# Error Handling

## Principles

- Never silently swallow errors
- Always provide user-facing feedback
- Log errors for debugging
- Distinguish between recoverable and fatal errors

## Error Categories

### Network Errors
- Show retry option
- Cache last known data when possible
- Display "No internet connection" message

### API Errors
- Show error message from API when available
- Fallback to generic message
- Log full error for debugging

### Validation Errors
- Show inline field errors
- Prevent form submission until valid
- Clear errors on input change

### Database Errors
- Show "Something went wrong" message
- Log error details
- Attempt retry once

### Fatal Errors
- Show full-screen error state
- Offer app restart option
- Log crash details

## Component Pattern

```tsx
// Every screen/component with async data:
if (loading) return <LoadingState />
if (error) return <ErrorState message={error.message} onRetry={refetch} />
if (!data) return <EmptyState />
return <Content data={data} />
```

## Error Messages

- Use plain language, not technical jargon
- Be specific when possible ("Failed to load balance" not "Error")
- Always offer a next action (retry, go back, contact support)

## Logging

- Use `console.error` for development
- Do not expose error details to users in production
- Include context: function name, input parameters, timestamp
