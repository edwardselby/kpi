# KPI Report Generator - Quick Start Guide

## Installation

```bash
# 1. Navigate to project
cd /path/to/your/kpi-report-generator

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Install package (creates 'kpi' command)
pip install -e .
```

---

## Basic Usage

### 📊 Console Report (Quick Check)

```bash
kpi
```

**What you get:**
- Last 5 releases per service
- Commit counts between releases
- Lines added/removed with file exclusions
- Formatted console output

---

### 📈 HTML Report with Charts

```bash
kpi --html
```

**What you get:**
- Professional HTML report at `reports/kpi-report-all.html`
- 5 embedded charts (PNG images):
  - Summary metrics bar chart
  - Commits by service comparison
  - Lines added by service comparison
  - Net change by service comparison
  - Release activity timeline
- Print/PDF ready format

---

## Command Reference

| Command | Description |
|---------|-------------|
| `kpi` | Console output (default) |
| `kpi --html` | Generate HTML report with charts |
| `kpi --html --period 2025-11` | Report for specific month |
| `kpi --html -o ./reports` | Custom output directory |
| `kpi --version` | Show version |
| `kpi --help` | Show detailed help |

---

## Common Workflows

### Daily Standup Prep

```bash
# Quick console check
kpi
```

### Weekly Team Report

```bash
# 1. Generate HTML with charts
kpi --html

# 2. Open in browser
open reports/kpi-report-all.html

# 3. Print to PDF (Cmd+P in browser)
# 4. Share with team
```

### Monthly Executive Summary

```bash
# Generate report for specific period
kpi --html --period 2025-12 -o ./monthly-reports

# Review and export to PDF
open monthly-reports/kpi-report-2025-12.html
```

---

## Configuration

**Two Options:**

### Option 1: config.local.yaml (Recommended)

```bash
# Copy template for private use
cp config.yaml config.local.yaml

# Edit with your services (gitignored - safe for private data)
nano config.local.yaml

# Run as normal - config.local.yaml is automatically used
kpi --html
```

### Option 2: Edit config.yaml directly

```yaml
# Path to repositories
projects_directory: ./projects

# Which repos to analyze
included_projects:
  - api-gateway-service
  - user-service
  - payment-service

# Files to exclude from line counts
file_exclusions:
  - "*.lock"
  - "*.min.js"
  - "node_modules/*"
  - "dist/*"
```

After editing, just run `kpi` or `kpi --html` - changes take effect immediately.

---

## Viewing Reports

### Console Output
Already displayed in terminal after running `kpi`

### HTML Reports

```bash
# Open in default browser (macOS)
open reports/kpi-report-all.html

# Or copy file path and open in browser:
# file:///path/to/your/kpi-report-generator/reports/kpi-report-all.html
```

### Export to PDF

1. Open HTML report in browser
2. File → Print (or Cmd+P)
3. Destination: Save as PDF
4. Layout is automatically optimized for print

---

## Troubleshooting

### Command not found: kpi

```bash
# Reinstall package
pip install -e .
```

### No projects found

```bash
# Check config.yaml paths
cat config.yaml

# Verify repositories exist
ls /path/to/your/projects/api-gateway-service
```

### Charts not appearing

```bash
# Regenerate report
kpi --html

# Verify charts created
ls -lh reports/.charts/
```

---

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term

# Generate HTML coverage report
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

---

## Advanced Usage

### Help System

```bash
# Detailed help with examples
kpi --help

# Version information
kpi --version
```

### Custom Output

```bash
# Different output directory
kpi --html -o ./custom/path

# Different periods (future enhancement)
kpi --html --period 2025-Q4
```

---

## What Gets Generated

```
reports/
├── kpi-report-all.html          # Main HTML report
└── .charts/                      # Chart images
    ├── summary-all.png           # ~41KB - Summary metrics
    ├── project-total_commits-all.png        # ~36KB
    ├── project-total_lines_added-all.png    # ~39KB
    ├── project-net_change-all.png           # ~41KB
    └── timeline-all.png          # ~37KB - Release timeline
```

All charts are:
- Static PNG images (150 DPI)
- Print/PDF friendly
- Embedded in HTML report
- Consistently styled

---

## Quick Tips

1. **Run `kpi` daily** for quick activity checks
2. **Use `kpi --html` weekly** for team reports
3. **Edit config.yaml** to add/remove projects
4. **Charts auto-generate** - no extra steps needed
5. **PDF export** works perfectly for presentations
6. **All data comes from git** - no manual input needed

---

## Next Steps

- Add more repositories to `config.yaml`
- Set up weekly automation with cron
- Customize file exclusions for your stack
- Export PDFs for stakeholder reporting
- Use console output in daily standups

---

## Getting Help

```bash
# Built-in help
kpi --help

# Check README
cat README.md

# View documentation
ls docs/

# Run tests to verify setup
pytest tests/ -v
```

---

**That's it! You're ready to generate professional KPI reports.** 🎉

Start with `kpi --html` to see the full power of the tool with charts and visualizations.
