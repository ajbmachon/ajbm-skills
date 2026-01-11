# Skill & Plugin Troubleshooting

Debugging guide for skills and plugins specifically. For general Claude Code issues, see `troubleshooting.md`.

## Table of Contents

- [Skill Not Triggering](#skill-not-triggering)
- [Plugin Not Loading](#plugin-not-loading)
- [Command Not Appearing](#command-not-appearing)
- [MCP Server Not Starting](#mcp-server-not-starting)
- [Hooks Not Firing](#hooks-not-firing)
- [False Positives](#false-positives)
- [Debugging Workflow](#debugging-workflow)

---

## Skill Not Triggering

### UserPromptSubmit Not Suggesting

**Symptoms:** Ask a question, but no skill suggestion appears.

**Common causes:**
1. Keywords don't match - check `promptTriggers.keywords`
2. Intent patterns too specific - test at regex101.com
3. Typo in skill name - must match SKILL.md frontmatter
4. JSON syntax error - validate with `jq`

**Debug:**
```bash
echo '{"session_id":"debug","prompt":"your test prompt"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts
```

### PreToolUse Not Blocking

**Common causes:**
1. File path doesn't match glob patterns
2. Excluded by pathExclusions (test files)
3. Content pattern not in file
4. Session already used skill (check state file)
5. File marker `@skip-validation` present
6. Environment variable override set

**Debug:**
```bash
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts 2>&1
{"session_id":"debug","tool_name":"Edit","tool_input":{"file_path":"/path/to/file.ts"}}
EOF
```

---

## Plugin Not Loading

**Check:**
1. `cat .claude-plugin/plugin.json | jq .` - valid JSON?
2. `ls -la .claude-plugin/` - exists?
3. `grep -r "/Users/" .claude-plugin/` - no hardcoded paths?
4. Restart Claude Code after changes

| Problem | Solution |
|---------|----------|
| `.claude-plugin/` missing | Create with `plugin.json` |
| Invalid JSON | Validate with `jq` |
| Hardcoded paths | Use `${CLAUDE_PLUGIN_ROOT}` |
| Forgot to restart | Always restart |

---

## Command Not Appearing

**Check:**
1. Commands at `commands/` in plugin root (NOT `.claude-plugin/`)
2. Has YAML frontmatter with `description`
3. File extension is `.md`
4. Restarted Claude Code

---

## MCP Server Not Starting

**Check:**
1. Paths use `${CLAUDE_PLUGIN_ROOT}`
2. Scripts executable: `chmod +x`
3. Test independently: `node server/index.js`
4. Check logs: `claude --debug`

---

## Hooks Not Firing

**Check:**
1. `hooks/hooks.json` at plugin root
2. Valid JSON: `cat hooks/hooks.json | jq .`
3. Matcher is valid regex
4. Scripts executable
5. Paths use `${CLAUDE_PLUGIN_ROOT}`

---

## False Positives

**Keywords too generic?**
```json
// BAD
"keywords": ["user", "system"]
// GOOD
"keywords": ["user authentication", "user tracking"]
```

**Patterns too broad?**
```json
// BAD
"intentPatterns": ["(create)"]
// GOOD
"intentPatterns": ["(create|add).*?(database|feature)"]
```

---

## Debugging Workflow

1. **Validate JSON:**
   ```bash
   jq . .claude-plugin/plugin.json
   jq . hooks/hooks.json
   ```

2. **Check paths:**
   ```bash
   grep -r "Users/" .  # Should find nothing
   ```

3. **Verify permissions:**
   ```bash
   find . -name "*.sh" | xargs ls -l
   ```

4. **Clean reinstall:**
   ```bash
   /plugin uninstall my-plugin@my-dev
   /plugin install my-plugin@my-dev
   # Restart Claude Code
   ```

---

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Skills in `.claude-plugin/skills/` | Move to `skills/` at root |
| Hardcoded paths | Use `${CLAUDE_PLUGIN_ROOT}` |
| Forgot restart | Always restart |
| Script not executable | `chmod +x` |
| Invalid JSON | Validate with `jq` |
| Vague description | Be specific about triggers |
