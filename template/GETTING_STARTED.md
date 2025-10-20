# Getting Started with ACD

Welcome! This checklist will guide you through setting up ACD in your project.

## ✅ Setup Checklist

### 1. Initialize ACD (Required)

```bash
chmod +x scripts/acd_init.sh
./scripts/acd_init.sh
```

**What this does:**
- Creates directory structure
- Downloads ACD tools (validate_acd.py, acd_parser.py, gdb_acd.py)
- Configures .gitignore

---

### 2. Customize Configuration (Required)

Edit `.acd/config.yml`:

- [ ] Update project name and repository
- [ ] Define your project's phases
- [ ] Review validation settings
- [ ] Adjust file patterns if needed

**Example phases:**
```yaml
phases:
  - name: "AUTHENTICATION"
    description: "User authentication"
    complexity: "HIGH"
  
  - name: "DATABASE"
    description: "Database operations"
    complexity: "MEDIUM"
```

---

### 3. Update README (Recommended)

Edit `README.md`:

- [ ] Replace `[Your Project Name]` with your project name
- [ ] Replace `[Your License Here]` with your license
- [ ] Add project-specific information
- [ ] Keep the ACD section intact

---

### 4. Add Metadata to Your Code (Required)

Start with existing functions or write new code with SCIS metadata:

**Minimum required:**
```cpp
/*
 * AI_PHASE: YOUR_PHASE
 * AI_STATUS: IMPLEMENTED
 */
void your_function() {
    // code
}
```

**Recommended:**
```cpp
/*
 * AI_PHASE: YOUR_PHASE
 * AI_STATUS: IMPLEMENTED
 * AI_COMPLEXITY: MEDIUM
 * AI_NOTE: Description of what this does
 * AI_DEPENDENCIES: OTHER_PHASE
 * AI_COMMIT: abc123f
 */
```

---

### 5. Validate Your Metadata (Required)

```bash
python3 scripts/validate_acd.py src/
```

Fix any errors reported by the validator.

---

### 6. Test CI/CD (If using GitHub)

- [ ] Push code to GitHub
- [ ] Check Actions tab for validation workflow
- [ ] Verify workflow passes
- [ ] Fix any issues reported

---

### 7. Generate Your First Report (Optional)

```bash
python3 scripts/acd_parser.py src/ --analyze --markdown report.md
cat report.md
```

---

### 8. Create a Fix Summary (Optional)

When you fix an issue:

1. Copy template: `cp docs/fix_summaries/FIX_TEMPLATE.md docs/fix_summaries/FIX_20241020_your_fix.md`
2. Fill in the details
3. Commit with your code changes

---

## 🎓 Learning Resources

### Essential Reading

1. **Quick Reference** - `docs/QUICK_REFERENCE.md`
   - Tag reference
   - Code examples
   - Common commands

2. **Implementation Guide** - `docs/IMPLEMENTATION_GUIDE.md`
   - Step-by-step instructions
   - Best practices
   - Troubleshooting

3. **Template Usage** - `../TEMPLATE_USAGE.md` (in parent directory)
   - Complete template guide
   - Installation methods
   - Customization

### Examples

- `examples/example_with_acd.c` - C example
- `examples/example_with_acd.py` - Python example

### External Resources

- [ACD Specification](https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification)
- [Tools Guide](https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification/blob/main/docs/TOOLS_GUIDE.md)

---

## 🚀 Quick Tips

### Start Simple

Begin with just the required tags:
- `AI_PHASE`
- `AI_STATUS`

Add more tags as you become comfortable.

### Use Existing Phases

Before creating new phases, check if an existing phase fits:
- INIT
- ERROR_HANDLING
- VALIDATION
- CORE_LOGIC

### Validate Often

Run validation frequently during development:
```bash
python3 scripts/validate_acd.py src/
```

### Keep Metadata Current

Update `AI_STATUS` as implementation progresses:
- Start: `PARTIAL` or `NOT_STARTED`
- Complete: `IMPLEMENTED`
- Fixed: `FIXED`

---

## 📋 Common Tasks

### Add New Feature

1. Plan phase in `.acd/config.yml`
2. Write code with `AI_STATUS: PARTIAL`
3. Complete implementation
4. Change to `AI_STATUS: IMPLEMENTED`
5. Update `AI_COMMIT` after committing

### Fix a Bug

1. Fix the code
2. Change `AI_STATUS: FIXED`
3. Create fix summary
4. Update `AI_COMMIT` and `AI_COMMIT_HISTORY`

### Refactor Code

1. Validate before changes
2. Refactor while maintaining metadata
3. Validate after changes
4. Update `AI_COMMIT` and history

---

## ❓ Need Help?

### Check Documentation

- `docs/QUICK_REFERENCE.md` - Quick command reference
- `docs/IMPLEMENTATION_GUIDE.md` - Detailed guide
- `../TEMPLATE_USAGE.md` - Template-specific help

### Common Issues

**"Scripts not executable"**
```bash
chmod +x scripts/*.sh scripts/*.py
```

**"PyYAML not installed"**
```bash
pip install pyyaml
```

**"Validation fails on examples"**
- Update commit hashes from "initial" to real commits
- Or ignore examples directory during validation

### Get Support

- GitHub Issues: https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification/issues
- Documentation: https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification

---

## ✨ Next Steps

After completing the checklist:

1. Add metadata to all your source files
2. Set up CI/CD validation
3. Generate dependency graphs
4. Create fix summaries for past issues
5. Share your experience with the ACD community

---

**Welcome to autonomous continuous development!** 🎉

Your codebase now has the intelligence and historical memory to work effectively with AI agents.

---

**Powered by the [ACD Standard v1.0](https://github.com/R-E-C-A-L-L-Foundation/Autonomous-Continuous-Development-ACD-Standard-Specification)**
