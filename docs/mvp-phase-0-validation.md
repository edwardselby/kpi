# Phase 0: Pre-Development Validation

## Purpose

Validate all assumptions about repository structure, changelog format, and tagging conventions before writing any code. Discover edge cases early to inform implementation decisions.

## Duration

1-2 hours

## Why This Phase Matters

Building on wrong assumptions wastes time. If changelogs aren't actually consistent, or tags use different formats, we need to know **now** before building parsers.

---

## Tasks Checklist

### 1. Repository Audit

**Objective:** Verify repositories match expected patterns

**Steps:**

```bash
# Navigate to projects directory
cd ../PyProjects

# For each project, check:
1. Does CHANGELOG.md exist?
   ls -la */CHANGELOG.md

2. What's the changelog format?
   head -n 50 feed-orchestrator/CHANGELOG.md
   head -n 50 betslip-service/CHANGELOG.md
   head -n 50 odds-engine/CHANGELOG.md

3. What tags exist?
   cd feed-orchestrator && git tag --sort=-creatordate | head -20
   cd ../betslip-service && git tag --sort=-creatordate | head -20

4. Are tags semantic versioning?
   git tag | grep -E '^v?[0-9]+\.[0-9]+\.[0-9]+'
```

**Document findings in:** `docs/repo-audit-findings.md`

### 2. Changelog Format Verification

**Expected format (Keep a Changelog):**

```markdown
# Changelog

## [Unreleased]

## [1.2.3] - 2025-11-15

### Added
- IDT-123 New feature description

### Fixed
- SODA-456 Bug fix description
- IDT-789 Another fix

### Changed
- Updated dependency versions

### Removed
- Deprecated API endpoint
```

**Questions to answer:**

- [ ] Do all changelogs follow this format exactly?
- [ ] Are dates always in `YYYY-MM-DD` format?
- [ ] Are version numbers always in `[X.Y.Z]` format?
- [ ] Do entries consistently use section headers (Added, Fixed, etc.)?
- [ ] Are ticket references present? (IDT-*, SODA-*, GSWP-*)
- [ ] What percentage of entries have ticket references?

**Edge cases to find:**

- Missing dates: `## [1.2.3]` (no date)
- Malformed dates: `## [1.2.3] - Nov 15 2025`
- Unreleased section: `## [Unreleased]`
- Release candidates: `## [1.2.3-rc1] - 2025-11-15`
- Missing sections: No "Added" or "Fixed" headers
- Unstructured entries: Bullet points without categories

### 3. Tag Format Verification

**Expected format:**
- Semantic versioning: `9.2.6`
- **No** `v` prefix: `v9.2.6` ❌
- Optional suffix: `9.2.6-rc1` (acceptable)

**Check:**

```bash
# Get all unique tag patterns
find ../PyProjects -name .git -type d -exec sh -c '
  cd "$1/.." && echo "=== $(basename $(pwd)) ===" && git tag | head -10
' _ {} \;
```

**Questions to answer:**

- [ ] Are all tags semantic versioning?
- [ ] Do any use `v` prefix?
- [ ] Do any use other prefixes? (`release-`, `version-`, etc.)
- [ ] Are there non-version tags? (`production`, `staging`)
- [ ] How common are RC/beta tags?

### 4. Edge Case Discovery

**Look for:**

1. **Repositories with no tags**
   ```bash
   for dir in ../PyProjects/*/; do
     cd "$dir" && [ -z "$(git tag)" ] && echo "No tags: $(basename $PWD)"
   done
   ```

2. **Repositories with no CHANGELOG.md**
   ```bash
   for dir in ../PyProjects/*/; do
     [ ! -f "$dir/CHANGELOG.md" ] && echo "No changelog: $(basename $dir)"
   done
   ```

3. **Repositories on unexpected branches**
   ```bash
   for dir in ../PyProjects/*/; do
     cd "$dir" && branch=$(git branch --show-current)
     [ "$branch" != "main" ] && [ "$branch" != "dev" ] && \
       echo "$(basename $PWD): $branch"
   done
   ```

4. **Large file counts (might need aggressive exclusions)**
   ```bash
   cd feed-orchestrator
   git diff --stat 9.2.5 9.2.6 | wc -l
   ```

5. **Generated files that should be excluded**
   ```bash
   git diff --name-only 9.2.5 9.2.6 | grep -E '\.(lock|min\.js|min\.css)$'
   ```

---

## Deliverables

### 1. Audit Findings Document

**File:** `docs/repo-audit-findings.md`

**Structure:**

```markdown
# Repository Audit Findings

**Date:** 2025-12-04
**Auditor:** [Your Name]
**Repositories Audited:** 8

## Summary

- Changelog Format: ✅ Consistent across all repos
- Tag Format: ⚠️ 2 repos use 'v' prefix
- Coverage: ✅ All repos have changelogs and tags

## Changelog Analysis

### Format Consistency
- 8/8 repos use Keep a Changelog format
- 7/8 have dates in correct format
- 1 repo (auth-service) has 3 entries without dates

### Ticket Reference Coverage
- feed-orchestrator: 95% (38/40 entries)
- betslip-service: 80% (24/30 entries)
- odds-engine: 90% (27/30 entries)
...

### Edge Cases Found
1. auth-service v2.3.1: Missing date
2. legacy-service: Has "Unreleased" section with 5 entries
3. payment-service: Uses "Deprecated" section (not standard)

## Tag Analysis

### Format
- Standard: 9.2.6 (6 repos)
- With 'v' prefix: v1.2.3 (2 repos - legacy-service, auth-service)
- RC tags: Found in 3 repos (e.g., 9.2.6-rc1)

### Tag Count Distribution
- Highest: feed-orchestrator (47 tags)
- Lowest: new-service (3 tags)
- Average: 18 tags per repo

## Recommendations

### Must Handle
- Mixed tag formats (with/without 'v' prefix)
- Missing changelog dates
- Unreleased sections
- RC/beta tags

### File Exclusions Needed
- *.lock (package-lock.json, yarn.lock)
- *.min.js, *.min.css
- migrations/* (large auto-generated files)

### Projects to Exclude from Initial Testing
- new-service (only 3 tags, insufficient data)
```

### 2. Test Fixture Repository

**File:** `tests/fixtures/sample_repo/`

**Create a real git repository with:**

```bash
cd tests/fixtures
mkdir sample_repo && cd sample_repo
git init

# Create initial commit
echo "# Sample Project" > README.md
git add . && git commit -m "Initial commit"

# Create CHANGELOG.md with various edge cases
cat > CHANGELOG.md << 'EOF'
# Changelog

## [Unreleased]
### Added
- Work in progress feature

## [1.2.3] - 2025-11-15
### Added
- IDT-123 New authentication system

### Fixed
- SODA-456 Payment processing bug
- IDT-789 Timezone handling issue

## [1.2.2] - 2025-10-10
### Changed
- Updated dependencies

## [1.2.1]
### Fixed
- Critical security patch (note: missing date!)

## [1.2.0-rc1] - 2025-09-15
### Added
- Beta feature testing
EOF

git add CHANGELOG.md && git commit -m "Add changelog"
git tag 1.2.0-rc1

# Add more commits and tags
echo "src/file1.py" > src/file1.py
echo "src/file2.py" > src/file2.py
git add . && git commit -m "Add source files"
git tag 1.2.1

# Add substantial changes
for i in {1..10}; do
  echo "line $i" >> src/file1.py
done
echo "*.lock" > .gitignore
git add . && git commit -m "Substantial changes"
git tag 1.2.2

# More changes
echo "new feature" > src/feature.py
git add . && git commit -m "Add feature"
git tag 1.2.3
```

**This fixture tests:**
- Standard semantic versions
- RC versions
- Missing dates in changelog
- Unreleased section
- Multiple commit between tags
- File exclusions (.gitignore patterns)

---

## Validation Checklist

Before proceeding to Phase 1:

- [ ] Audited at least 3 real repositories
- [ ] Documented changelog format consistency (or inconsistency)
- [ ] Documented tag format patterns
- [ ] Identified all edge cases
- [ ] Created test fixture repository
- [ ] Chosen 2-3 projects for Phase 1 testing
- [ ] Documented file exclusion patterns needed
- [ ] Confirmed assumptions or adjusted expectations

---

## Decision Points

Based on audit findings, answer:

### 1. Changelog Parser Complexity

**If changelogs are consistent:**
→ Proceed with strict parser, fail on malformed entries

**If changelogs have variations:**
→ Build lenient parser, attempt partial parsing, warn on issues

### 2. Tag Format Handling

**If all tags use same format:**
→ Simple regex parsing

**If tags have 'v' prefix mix:**
→ Strip 'v' prefix automatically, normalize all tags

**If non-version tags exist:**
→ Filter to only semantic version pattern

### 3. Scope Adjustments

**If >20% of repos lack changelogs:**
→ Consider git-only metrics, make changelog optional

**If >50% of entries lack ticket references:**
→ Don't rely on ticket metrics, focus on change types

### 4. Initial Test Set

**Choose 2-3 repos that:**
- Have good changelog coverage
- Use standard tag format
- Have 10+ releases
- Represent typical project structure

**Examples:**
1. `feed-orchestrator` (highest activity)
2. `betslip-service` (moderate activity)
3. `odds-engine` (well-maintained)

---

## Output Template

Complete this before moving to Phase 1:

```markdown
## Phase 0 Complete ✅

**Audit Findings:** docs/repo-audit-findings.md
**Test Fixture:** tests/fixtures/sample_repo/

### Key Findings

1. **Changelog Consistency:** [High/Medium/Low]
   - Format: [Describe]
   - Edge cases: [List]

2. **Tag Format:** [Consistent/Mixed]
   - Pattern: [Describe]
   - Variations: [List]

3. **Recommended Adjustments:**
   - [Adjustment 1]
   - [Adjustment 2]

### Phase 1 Test Projects

1. [Project 1 name] - [Reason]
2. [Project 2 name] - [Reason]
3. [Project 3 name] - [Reason]

### Ready to Proceed: YES/NO

If NO, what's blocking: [Describe]
```

---

## Time Box

**Maximum time:** 2 hours

If audit reveals major inconsistencies requiring >2 hours to document, that's valuable information. Don't spend days auditing—get enough data to make informed decisions and proceed.

**Next Phase:** Phase 1 - Walking Skeleton
