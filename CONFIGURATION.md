# Configuration Guide

Complete guide to configuring the KPI Report Generator for your organization.

---

## Quick Start

### For Public Use (Generic Services)

Use the default `config.yaml` which includes generic microservice examples:

```bash
# Run with default config
kpi --html
```

### For Your Organization (Private Services)

Create `config.local.yaml` with your organization's services:

```bash
# Copy template
cp config.yaml config.local.yaml

# Edit with your services
nano config.local.yaml

# Run (automatically uses config.local.yaml)
kpi --html
```

**Important:** `config.local.yaml` is gitignored and won't be pushed to GitHub.

---

## Configuration Hierarchy

The tool loads configuration in this order:
1. **config.local.yaml** (if exists) - Your private organization config
2. **config.yaml** (fallback) - Public template with generic examples

This allows maintaining private organization data while keeping the public repository generic.

---

## Configuration Structure

### Required Fields

```yaml
# Directory containing your git repositories
projects_directory: /path/to/your/repositories

# List of repository directory names to analyze
included_projects:
  - service-1
  - service-2
  - service-3

# Patterns to exclude from line count metrics
file_exclusions:
  - "*.lock"
  - "*.min.js"
  - "node_modules/*"
  - "dist/*"

# Directory for generated reports
report_output: ./reports

# Valid branch names (warns if not on these)
valid_branches:
  - main
  - dev
  - master
```

### Optional Metadata

Add service metadata for richer narrative generation in reports:

```yaml
service_metadata:
  service-1:
    category: "Core Infrastructure"
    tags: ["API", "authentication", "database"]
    description: "Authentication and authorization service"

  service-2:
    category: "Domain Services"
    tags: ["domain_logic", "reporting", "API"]
    description: "Business reporting and analytics service"
```

---

## Service Categories

Categories help organize services in reports:

- **Core Infrastructure** - Foundational services (gateways, databases, caching)
- **Domain Services** - Business logic and domain-specific functionality
- **User Features** - User-facing features and interfaces
- **Supporting Services** - Infrastructure support (logging, monitoring, auth)

Add your own categories to `category_priority`:

```yaml
category_priority:
  - "Core Infrastructure"
  - "Domain Services"
  - "User Features"
  - "Supporting Services"
  - "Your Custom Category"
```

---

## Service Tags

Tags describe service functionality and enable layer analysis:

### Common Tags

**API & Integration:**
- `API` - RESTful or GraphQL APIs
- `routing` - Request routing and orchestration
- `integration` - Third-party integrations
- `messaging` - Message queues and notifications

**Data & Storage:**
- `database` - Database operations
- `storage` - File or object storage
- `caching` - Caching layers
- `data_processing` - ETL and data pipelines

**Security & Auth:**
- `authentication` - User authentication
- `authorization` - Access control
- `security` - Security features

**Business Logic:**
- `domain_logic` - Business rules and logic
- `transaction_processing` - Transaction handling
- `analytics` - Analytics and insights
- `reporting` - Report generation

**Infrastructure:**
- `orchestration` - Service coordination
- `logging` - Logging infrastructure
- `monitoring` - Monitoring and alerting
- `infrastructure` - Infrastructure support

### Tag Descriptions

Define human-readable descriptions for tags:

```yaml
tag_descriptions:
  API: "API development"
  authentication: "authentication and authorization"
  domain_logic: "business logic"
  reporting: "report generation"
  logging: "logging infrastructure"
```

---

## Tag Groups

Group tags to analyze service layers and characteristics:

### Service Layers

```yaml
tag_groups:
  service_layers:
    data_layer: ["data_processing", "database", "storage", "caching"]
    presentation_layer: ["API", "routing", "user_interface"]
    business_layer: ["domain_logic", "analytics", "reporting"]
    infrastructure_layer: ["orchestration", "logging", "monitoring"]
```

### Technical Characteristics

```yaml
  technical_characteristics:
    real_time_services: ["messaging", "notification", "real_time"]
    batch_services: ["data_processing", "analytics", "reporting"]
    user_facing: ["API", "routing", "user_interface"]
    backend_services: ["database", "storage", "logging"]
```

---

## File Exclusions

Exclude files from line count metrics:

### Patterns Supported

```yaml
file_exclusions:
  # Lock files
  - "*.lock"
  - "package-lock.json"
  - "yarn.lock"

  # Minified files
  - "*.min.js"
  - "*.min.css"

  # Generated files
  - "*.generated.*"
  - "*.gen.ts"

  # Dependencies and build artifacts
  - "node_modules/*"
  - "vendor/*"
  - "dist/*"
  - "build/*"
  - "target/*"

  # Database migrations
  - "migrations/*"
  - "db/migrate/*"

  # Test fixtures
  - "test/fixtures/*"
  - "**/testdata/*"
```

---

## Example Configurations

### E-commerce Platform

```yaml
projects_directory: ./projects

included_projects:
  - product-catalog-service
  - shopping-cart-service
  - payment-gateway-service
  - order-fulfillment-service
  - inventory-management-service
  - customer-service-api

service_metadata:
  product-catalog-service:
    category: "Domain Services"
    tags: ["product_management", "API", "database"]
    description: "Product catalog and inventory management"

  shopping-cart-service:
    category: "User Features"
    tags: ["user_interface", "real_time", "transaction_processing"]
    description: "Shopping cart and checkout experience"

  payment-gateway-service:
    category: "Core Infrastructure"
    tags: ["transaction_processing", "integration", "security"]
    description: "Payment processing and gateway integration"
```

### SaaS Application

```yaml
projects_directory: ./projects

included_projects:
  - user-auth-service
  - subscription-management-service
  - billing-service
  - analytics-dashboard-service
  - notification-service
  - api-gateway

service_metadata:
  user-auth-service:
    category: "Core Infrastructure"
    tags: ["authentication", "authorization", "API"]
    description: "User authentication and access control"

  subscription-management-service:
    category: "Domain Services"
    tags: ["domain_logic", "transaction_processing", "API"]
    description: "Subscription lifecycle and plan management"

  analytics-dashboard-service:
    category: "User Features"
    tags: ["analytics", "data_presentation", "API"]
    description: "User analytics and insights dashboard"
```

### Fintech Application

```yaml
projects_directory: ./projects

included_projects:
  - account-service
  - transaction-processor-service
  - risk-assessment-service
  - compliance-reporting-service
  - fraud-detection-service
  - customer-kyc-service

service_metadata:
  transaction-processor-service:
    category: "Core Infrastructure"
    tags: ["transaction_processing", "real_time", "API"]
    description: "Real-time transaction processing engine"

  risk-assessment-service:
    category: "Domain Services"
    tags: ["domain_logic", "analytics", "security"]
    description: "Credit and risk assessment"

  fraud-detection-service:
    category: "Supporting Services"
    tags: ["security", "analytics", "monitoring"]
    description: "Fraud detection and prevention"
```

### Microservices Platform

```yaml
projects_directory: ./projects

included_projects:
  - api-gateway-service
  - service-mesh-controller
  - config-service
  - discovery-service
  - logging-service
  - metrics-service
  - tracing-service

service_metadata:
  api-gateway-service:
    category: "Core Infrastructure"
    tags: ["API", "routing", "orchestration"]
    description: "Central API gateway and routing"

  service-mesh-controller:
    category: "Core Infrastructure"
    tags: ["orchestration", "infrastructure", "monitoring"]
    description: "Service mesh control plane"

  logging-service:
    category: "Supporting Services"
    tags: ["logging", "monitoring", "infrastructure"]
    description: "Centralized logging and aggregation"
```

---

## Advanced Configuration

### Custom Tag Groups

Create your own tag groupings for analysis:

```yaml
tag_groups:
  service_layers:
    # Standard layers...

  deployment_characteristics:
    containerized: ["docker", "kubernetes"]
    serverless: ["lambda", "cloud_function"]
    traditional: ["vm", "bare_metal"]

  data_flow:
    ingress: ["API", "routing", "gateway"]
    processing: ["domain_logic", "data_processing"]
    egress: ["integration", "messaging", "notification"]

  compliance:
    pci_dss: ["payment", "transaction_processing", "security"]
    gdpr: ["user_data", "privacy", "consent"]
    sox: ["financial", "audit", "reporting"]
```

### Multi-Environment Support

Use different configs for different environments:

```bash
# Production
cp config.yaml config.production.yaml

# Staging
cp config.yaml config.staging.yaml

# Load specific config
# (requires code modification or wrapper script)
CONFIG_FILE=config.production.yaml kpi --html
```

### Dynamic Project Discovery

For large organizations, consider programmatic config generation:

```python
# generate_config.py
import os
import yaml

projects_dir = "/path/to/repos"
all_projects = [d for d in os.listdir(projects_dir)
                if os.path.isdir(os.path.join(projects_dir, d))]

config = {
    "projects_directory": projects_dir,
    "included_projects": all_projects,
    # ... rest of config
}

with open("config.local.yaml", "w") as f:
    yaml.dump(config, f)
```

---

## Best Practices

### 1. Use config.local.yaml for Organization Data

```bash
# ✅ DO: Keep private data in config.local.yaml
cp config.yaml config.local.yaml
nano config.local.yaml
git status  # config.local.yaml won't appear

# ❌ DON'T: Commit organization data to public repos
nano config.yaml  # This gets version controlled!
```

### 2. Document Custom Tags

```yaml
tag_descriptions:
  my_custom_tag: "Clear description of what this tag means"
  legacy_system: "Legacy monolithic components being migrated"
  high_priority: "Mission-critical services requiring 24/7 uptime"
```

### 3. Use Meaningful Categories

```yaml
category_priority:
  - "Critical Path Services"      # Revenue-impacting
  - "Customer-Facing Services"    # User-visible
  - "Backend Processing"          # Background jobs
  - "Infrastructure Support"      # DevOps and monitoring
```

### 4. Exclude Appropriately

```yaml
file_exclusions:
  # Exclude generated files
  - "*.generated.*"
  - "dist/*"

  # Exclude dependencies
  - "node_modules/*"
  - "vendor/*"

  # But include important generated files you maintain:
  # Don't exclude: "src/generated/schema.ts" if you maintain it
```

### 5. Keep Metadata Synchronized

```yaml
# ❌ BAD: Service listed but no metadata
included_projects:
  - my-service  # Will cause validation error

# ✅ GOOD: Complete metadata
included_projects:
  - my-service

service_metadata:
  my-service:
    category: "Domain Services"
    tags: ["API", "domain_logic"]
    description: "Service description"
```

---

## Troubleshooting

### Config file not found

```bash
FileNotFoundError: Configuration file not found: config.yaml

# Solution: Create config file
cp config.yaml.example config.yaml
# or
nano config.yaml
```

### Missing service metadata

```bash
ValueError: Missing service_metadata for: service-name

# Solution: Add metadata for all included projects
nano config.yaml  # or config.local.yaml
```

### Undefined tag

```bash
ValueError: Service 'my-service' uses undefined tag 'my_tag'

# Solution: Add tag to tag_descriptions
tag_descriptions:
  my_tag: "Description of tag"
```

### Undefined category

```bash
ValueError: Service 'my-service' uses undefined category 'My Category'

# Solution: Add category to category_priority
category_priority:
  - "My Category"
```

---

## Migration from v3 to v4

If upgrading from an older version:

```bash
# 1. Backup old config
cp config.yaml config.v3.yaml

# 2. Create local config for your data
cp config.yaml config.local.yaml

# 3. Update config.yaml with generic template
# (download latest from repo or manually edit)

# 4. Verify both work
kpi --html  # Should use config.local.yaml

# 5. Test public scenario
mv config.local.yaml config.local.yaml.bak
kpi --html  # Should use config.yaml with generic services
mv config.local.yaml.bak config.local.yaml
```

---

## Configuration Validation

Validate your configuration before running:

```python
# validate_config.py
from src.config_manager import load_config

try:
    config = load_config()
    print("✅ Configuration valid!")
    print(f"   Loaded {len(config.included_projects)} projects")
    print(f"   Using: {config.projects_directory}")
except Exception as e:
    print(f"❌ Configuration error: {e}")
```

---

## Additional Resources

- **README.md** - Overall project documentation
- **QUICKSTART.md** - Quick start guide
- **config.yaml** - Template configuration with examples
- **config.local.yaml** - Your private configuration (create this)
- **src/config_manager.py** - Configuration loading implementation

---

## Support

For configuration issues:

1. Check this guide for examples
2. Verify YAML syntax: `python -c "import yaml; yaml.safe_load(open('config.yaml'))"`
3. Run validation script (above)
4. Review error messages carefully
5. Check GitHub issues: https://github.com/edwardselby/kpi/issues

---

**Happy configuring!** 🎉
