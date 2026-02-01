# Testing Setup for Confluence v2 API Development

This document explains how to set up secure credentials for testing the Confluence v2 API implementation.

## Quick Setup

1. **Create the secrets directory (if it doesn't exist):**
   ```bash
   mkdir .secrets
   ```

2. **Copy the example environment file:**
   ```bash
   copy .env.example .secrets\test.env
   ```

3. **Edit `.secrets\test.env` with your actual credentials:**
   ```bash
   # Your Confluence Cloud URL
   CONFLUENCE_URL=https://your-domain.atlassian.net
   
   # Your Atlassian account email  
   CONFLUENCE_USERNAME=your-email@domain.com
   
   # Your API token (generate at: https://id.atlassian.com/manage-profile/security/api-tokens)
   CONFLUENCE_API_TOKEN=ATATT3xFfGF0...your-token-here
   
   # Optional: Test space key
   CONFLUENCE_TEST_SPACE=TESTSPACE
   ```

4. **Test the configuration:**
   ```bash
   python test_config.py
   ```

## Generating an API Token

1. Go to [Atlassian Account Security](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Give it a label like "Confluence v2 API Development"
4. Copy the generated token to your `.env` file

## Security Notes

- ✅ `.secrets/` directory is excluded from git (never committed)
- ✅ `test_config.py` is excluded from git (contains helper functions)
- ✅ API tokens are more secure than passwords
- ✅ Tokens can be revoked at any time from your Atlassian account

## Testing Different Environments

You can create multiple environment files for different test scenarios:

```bash
.secrets\test.env      # Main testing environment
.secrets\dev.env       # Development Confluence instance
.secrets\staging.env   # Staging environment  
```

Load specific environments by modifying the `env_path` in `test_config.py`:
```python
env_path = os.path.join('.secrets', 'dev.env')  # Load specific environment
```

## Troubleshooting

### "Missing required environment variables" error
- Ensure your `.secrets/test.env` file exists and contains all required variables
- Check that variable names match exactly (case-sensitive)
- Verify there are no extra spaces around the `=` sign

### Authentication failures
- Verify your API token is correct and not expired
- Ensure your username is the email address associated with your Atlassian account
- Check that your Confluence URL is correct (should end with .atlassian.net for Cloud)

### Permission errors
- Ensure your account has appropriate permissions in the Confluence space
- For testing, you may need to create a dedicated test space where you have admin rights