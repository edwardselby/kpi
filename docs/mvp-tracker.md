# KPI Report Generator - MVP Tracker

## Project Overview

Building a KPI report generator for demonstrating development output across multiple microservices. Focus: pragmatic MVP that delivers value quickly through iterative development.

## Development Philosophy

**Thin Vertical Slices:** Build features end-to-end, not layer-by-layer
**Validate Early:** Test against real repos before building more
**Working Software:** Console output beats pretty reports that don't work
**Iterative Enhancement:** Each phase adds value to the previous

---

## Phase 0: Pre-Development Validation

**Status:** ⏳ Pending
**Duration:** 1-2 hours
**Purpose:** Validate assumptions before writing code

### Tasks

- [ ] Audit 3-5 real repositories for CHANGELOG.md presence
- [ ] Verify Keep a Changelog format consistency
- [ ] Confirm semantic versioning tag format (no 'v' prefix)
- [ ] Document edge cases found (malformed dates, missing sections, etc.)
- [ ] Create test fixture repository with sample data
- [ ] Identify projects for initial testing

### Deliverables

- `docs/repo-audit-findings.md` - Documented assumptions and edge cases
- `tests/fixtures/sample_repo/` - Git repo with tagged releases and changelog

### Success Criteria

✅ Confirmed at least 3 repos have consistent changelog format
✅ Documented all tag format variations found
✅ Test fixture repo created with 5+ tagged releases
✅ Edge cases documented for handling

---

## Phase 1: Walking Skeleton (Core Data Flow)

**Status:** ⏳ Pending
**Duration:** 1-2 days
**Purpose:** Prove entire pipeline works end-to-end with minimal features

### Goals

- Hardcoded configuration (2-3 projects)
- Basic git tag parsing and commit counting
- Console output only (no HTML)
- Working end-to-end data flow

### Tasks

- [ ] Create minimal project structure
- [ ] Implement `get_tags()` - parse semantic version tags
- [ ] Implement `count_commits_between()` - count commits between refs
- [ ] Create simple `main.py` with hardcoded projects
- [ ] Test with 2-3 real repositories
- [ ] Write tests for tag parsing logic

### Deliverables

```
src/
├── __init__.py
├── main.py              # Hardcoded orchestration
└── git_analyzer.py      # Tag parsing + commit counting

tests/
├── test_git_analyzer.py
└── fixtures/sample_repo/
```

### Success Criteria

```bash
$ python -m src.main
📦 feed-orchestrator
--------------------------------------------------
  9.2.6 (2025-11-15): 23 commits
  9.2.5 (2025-10-12): 18 commits
  9.2.4 (2025-09-08): 15 commits
```

### Exit Criteria

✅ Can parse tags from real repositories
✅ Accurately counts commits between tags
✅ Handles edge cases (single tag, no tags)
✅ Console output is readable and correct
✅ Tests pass for tag parsing logic

**Document:** `docs/mvp-phase-1-walking-skeleton.md`

---

## Phase 2: Complete Data Collection

**Status:** ⏳ Pending
**Duration:** 3-4 days
**Purpose:** Build robust data collection layer with all metrics

### Goals

- YAML configuration support
- Full changelog parsing (change types, tickets)
- Line count metrics with file exclusions
- Project scanning and validation
- Comprehensive warning system

### Tasks

- [ ] Implement `config_manager.py` - YAML loading
- [ ] Implement `changelog_parser.py` - Full Keep a Changelog parsing
- [ ] Add line count calculation to `git_analyzer.py`
- [ ] Implement file exclusion pattern matching
- [ ] Create `project_scanner.py` - Discovery and validation
- [ ] Add warning collection system
- [ ] Implement `data_aggregator.py` - Cross-project metrics
- [ ] Write comprehensive test suite (90%+ coverage)

### Deliverables

```
config.yaml              # Real configuration file
src/
├── config_manager.py
├── project_scanner.py
├── changelog_parser.py  # Enhanced
├── git_analyzer.py      # Enhanced with line counts
└── data_aggregator.py

tests/
├── test_config_manager.py
├── test_project_scanner.py
├── test_changelog_parser.py
├── test_git_analyzer.py
└── test_data_aggregator.py
```

### Success Criteria

```bash
$ python -m src.main
✓ Loaded configuration: 8 projects whitelisted
✓ Found 8 valid projects
✓ Parsed 8 changelogs (142 total releases)
✓ Analyzed 8 repositories (87 tagged releases)

Summary:
  Total Releases: 23 (Nov 2025)
  Total Commits: 156
  Lines Added: 8,453
  Lines Removed: 3,210

⚠️  3 warnings:
  - Project 'legacy-service' not on valid branch
  - Project 'new-service' has no git tags
  - CHANGELOG.md malformed date in 'auth-service' v2.3.1
```

### Exit Criteria

✅ All data collection components implemented
✅ Handles all edge cases gracefully
✅ Warning system captures all issues
✅ Test coverage >90%
✅ Can process 20+ projects without errors
✅ Configuration fully externalized

**Document:** `docs/mvp-phase-2-data-collection.md`

---

## Phase 3: Basic Reporting

**Status:** ⏳ Pending
**Duration:** 2-3 days
**Purpose:** Generate professional HTML reports (tables only, no charts)

### Goals

- Clean HTML template with tables
- Summary metrics section
- Per-project breakdown
- File output with proper naming
- Basic CLI interface

### Tasks

- [ ] Design HTML template structure (CSS only, no charts)
- [ ] Implement Jinja2 template rendering
- [ ] Create `report_generator.py` core
- [ ] Add summary metrics card section
- [ ] Add per-project breakdown table
- [ ] Implement CLI argument parsing
- [ ] Add period filtering (month, quarter, all)
- [ ] Test HTML rendering in multiple browsers
- [ ] Verify print/PDF export works

### Deliverables

```
src/
├── report_generator.py  # Template rendering
└── main.py              # Enhanced with CLI

templates/
└── report.html          # Basic template (no charts)

reports/                 # Auto-generated
└── kpi-report-2025-11.html
```

### Success Criteria

```bash
$ python -m src.main --period 2025-11
✓ Report generated: reports/kpi-report-2025-11.html

# Open in browser shows:
- Professional header with period/date
- Summary cards (4 metrics)
- Per-project breakdown table (all metrics)
- Warnings section (if any)
- Clean, readable layout
```

### Exit Criteria

✅ HTML renders correctly in Chrome, Firefox, Safari
✅ Print/PDF export works without issues
✅ CLI supports all period formats
✅ Report filename follows convention
✅ Template is maintainable and well-structured
✅ Ready to show to management (even without charts)

**Document:** `docs/mvp-phase-3-basic-reporting.md`

---

## Phase 4: Visualization

**Status:** ⏳ Pending
**Duration:** 3-4 days
**Purpose:** Add charts and finalize presentation quality

### Goals

- Matplotlib chart generation
- Month-over-month comparison
- Per-project breakdown charts
- Change type distribution
- Timeline visualization
- Chart integration into template

### Tasks

- [ ] Set up matplotlib with PDF-friendly backend
- [ ] Implement `chart_generator.py` core
- [ ] Create month-over-month comparison bar chart
- [ ] Create per-project breakdown horizontal bars
- [ ] Create change type distribution pie chart
- [ ] Create timeline chart (releases over time)
- [ ] Define consistent color palette
- [ ] Integrate charts into HTML template
- [ ] Test chart rendering and quality
- [ ] Verify PDF export with charts
- [ ] Polish template styling
- [ ] Add chart cleanup option (--keep-charts flag)

### Deliverables

```
src/
└── chart_generator.py   # All chart generation

templates/
└── report.html          # Enhanced with chart sections

reports/
├── kpi-report-2025-11.html
└── .charts/             # Temporary chart storage
    ├── mom-comparison-2025-11.png
    ├── project-releases-2025-11.png
    ├── change-types-2025-11.png
    └── timeline-2025-11.png
```

### Success Criteria

```bash
$ python -m src.main --period 2025-11
Generating charts...
  ✓ Month-over-month comparison
  ✓ Project breakdown (releases)
  ✓ Change type distribution
  ✓ Release timeline
✓ Report generated: reports/kpi-report-2025-11.html

# Report includes:
- All Phase 3 content
- 4 embedded charts (PNG images)
- Professional visualization
- PDF-ready output
```

### Exit Criteria

✅ All chart types render correctly
✅ Charts are PDF-friendly (static images)
✅ Consistent styling across charts
✅ Charts enhance understanding (not decoration)
✅ PDF export includes all charts
✅ Performance acceptable (<30s for 20 projects)
✅ Ready to present to management

**Document:** `docs/mvp-phase-4-visualization.md`

---

## Overall Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 0: Validation | 1-2 hours | Day 1 |
| Phase 1: Walking Skeleton | 1-2 days | Day 2-3 |
| Phase 2: Data Collection | 3-4 days | Day 6-7 |
| Phase 3: Basic Reporting | 2-3 days | Day 9-10 |
| Phase 4: Visualization | 3-4 days | Day 13-14 |
| **Total** | **~2 weeks** | **Day 14** |

## Success Metrics

### Technical
- [ ] Test coverage >90%
- [ ] Processes 20+ projects in <30 seconds
- [ ] Handles all edge cases gracefully
- [ ] Zero hardcoded values (fully configurable)

### Product
- [ ] Report is presentation-ready
- [ ] Demonstrates team output clearly
- [ ] Management can understand without explanation
- [ ] PDF export works perfectly

### Process
- [ ] Each phase delivers working software
- [ ] Can demo progress at end of each phase
- [ ] Easy to pivot if requirements change
- [ ] Well-documented and maintainable

---

## Risk Management

### Risk: Inconsistent Changelog Format
**Mitigation:** Phase 0 validation catches this early
**Fallback:** Skip changelog parsing, use git metrics only

### Risk: Complex Git History
**Mitigation:** Extensive testing with real repos in Phase 1
**Fallback:** Warn and skip problematic repos

### Risk: Performance Issues
**Mitigation:** Test with full project set in Phase 2
**Fallback:** Add caching, parallel processing

### Risk: PDF Export Problems
**Mitigation:** Test print early in Phase 3
**Fallback:** Document browser-based PDF export process

---

## Future Enhancements (Post-MVP)

Out of scope for initial 2-week MVP, but documented for later:

1. **Automated Execution**
   - Cron job for monthly runs
   - Automatic git pull before analysis
   - Email delivery of reports

2. **Enhanced Metrics**
   - Test coverage integration
   - Deployment frequency
   - Mean time to recovery
   - Ticket closure rates

3. **Interactive Features**
   - Web dashboard
   - Interactive charts (Chart.js)
   - Drill-down capability
   - Historical trend analysis

4. **Team Attribution**
   - Per-developer metrics (if needed)
   - Team comparison
   - Contribution trends

5. **Integration**
   - CI/CD pipeline metrics
   - Jira/Linear integration
   - Slack notifications
   - GitHub Actions automation

---

## Decision Log

### Why Console Output First?
Validates data collection works before investing in presentation. Can pivot quickly if git/changelog parsing has issues.

### Why Tables Before Charts?
Tables are essential, charts are enhancement. Report is useful without charts; useless without data.

### Why Static HTML vs Web App?
Small team, manual execution. Static files are simpler, more portable, easier to share. No infrastructure needed.

### Why Matplotlib vs Chart.js?
PDF export requirement. Matplotlib generates static images that work in print. Chart.js requires browser.

### Why Whitelist vs Auto-Discovery?
Explicit control prevents accidental inclusion of personal projects, experiments, or archived repos. Better for small team.

---

## Notes

- **Working Directory:** `/Users/edward/PycharmProjects/SportsCoreKPI`
- **Projects Directory:** `../PyProjects` (sibling to KPI reporter)
- **Python Version:** 3.10+
- **Primary Developer:** Solo/small team
- **Target Audience:** Project Manager, Technical Lead

---

## Quick Reference

### Run Report
```bash
# Default (last month)
python -m src.main

# Specific period
python -m src.main --period 2025-11
python -m src.main --period 2025-Q4
python -m src.main --period all
```

### Run Tests
```bash
pytest tests/ -v --cov=src --cov-report=html
```

### Project Status Check
```bash
git status
git log --oneline -10
```
