# CURSOR_RECOMMENDATIONS.md

## Recommendations for jgtutils (config/settings/documentation)

1. **Unify config and settings schema documentation**
   - Provide JSON schema or YAML examples for both config.json and settings.json in the documentation.
   - Document all possible keys and their expected types/values.

2. **Add CLI examples for config/settings usage**
   - Show how to use `jgtset` and other tools to view, export, or update settings.
   - Include example commands for common workflows.

3. **Improve error handling and user feedback**
   - Make error messages for missing/invalid config/settings more user-friendly.
   - Suggest next steps or fixes in error output.

4. **Add tests for config/settings precedence**
   - Unit tests to verify the correct precedence and merging of settings from all sources.

5. **Document environment variable usage**
   - List all environment variables that affect config/settings loading, with examples.

6. **Consider supporting TOML for settings**
   - Evaluate adding support for TOML files, as they are increasingly common for Python projects.

7. **Clarify demo/real credential switching**
   - Add explicit documentation and CLI flags for switching between demo and real credentials, and document the fallback logic.

8. **Add a troubleshooting section**
   - Common issues and solutions for config/settings problems.

9. **Automate .env export in CI/CD**
   - Provide scripts or Makefile targets to automate exporting settings for CI/CD pipelines.

10. **Review and refactor jgtcommon.py for modularity**
    - Split large functions and group related logic for easier maintenance. 