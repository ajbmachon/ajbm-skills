# Code Examples Template

**Include ONLY when needed - for tricky patterns, framework-specific syntax, or easy-to-get-wrong implementations.**

---

## When to Include Code Examples

✅ Include when:
- Pattern is specific to this codebase/framework
- Implementation is easy to get wrong
- Current documentation differs from training data
- Codebase has conventions that override defaults

❌ Skip when:
- Claude would write it correctly anyway
- It's standard/obvious implementation
- No special considerations needed

---

## Template

```markdown
## Code Examples

> These patterns are specific to this codebase/framework. Follow them exactly.

### [Pattern Name]

**Why this matters:** [Brief explanation of why this pattern vs. the default]

```[language]
// Example code
```

**Key points:**
- [Important detail 1]
- [Important detail 2]

### [Another Pattern]

**From codebase:** `[file path where this pattern exists]`

```[language]
// Example matching codebase style
```
```

---

## Guidance

### Reference Codebase Patterns

When the codebase has specific patterns, cite them:

```markdown
### Error Handling

**From codebase:** `src/utils/errors.ts`

```typescript
// Use AppError, not generic Error
throw new AppError('USER_NOT_FOUND', { userId });

// NOT this:
throw new Error('User not found');
```

**Key points:**
- First argument is error code (uppercase, underscores)
- Second argument is context object
- Error codes defined in `src/constants/errors.ts`
```

### Show Current API Usage

When APIs have changed since training:

```markdown
### React Query v5 (Current)

**Note:** Codebase uses React Query v5, which differs from v4.

```typescript
// v5 syntax (correct)
const { data } = useQuery({
  queryKey: ['users', userId],
  queryFn: () => fetchUser(userId),
});

// NOT v4 syntax
const { data } = useQuery(['users', userId], () => fetchUser(userId));
```
```

### Keep Examples Minimal

Show only what's necessary:

```
❌ Full component with imports, types, styling, all handlers
✅ Just the specific pattern that needs attention
```

### Don't Over-Comment

The example should be self-explanatory with minimal comments:

```typescript
// Good: minimal, focused
const cache = new LRUCache<string, User>({ max: 1000, ttl: 1000 * 60 * 5 });

// Bad: over-explained
// Create a new LRU cache instance
// Set the maximum number of items to 1000
// Set the time-to-live to 5 minutes (1000ms * 60 * 5)
const cache = new LRUCache<string, User>({ max: 1000, ttl: 1000 * 60 * 5 });
```
