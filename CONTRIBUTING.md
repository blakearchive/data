# Contributing to Blake Archive Data

Thank you for your interest in contributing to the Blake Archive data repository! This guide will help you add or modify data while maintaining compatibility with the application.

## Table of Contents

- [Getting Started](#getting-started)
- [Data Standards](#data-standards)
- [Adding New Content](#adding-new-content)
- [Modifying Existing Content](#modifying-existing-content)
- [Testing Your Changes](#testing-your-changes)
- [Submitting Changes](#submitting-changes)

## Getting Started

### Prerequisites

- Familiarity with TEI XML encoding
- Understanding of Blake's works and the archive structure
- Git knowledge for version control
- Python 3.11+ for validation scripts

### Setup

1. Fork and clone both repositories:
   ```bash
   git clone https://github.com/YOUR_USERNAME/data.git
   git clone https://github.com/blakearchive/archive.git
   ```

2. Set up the archive application (see [QUICKSTART.md](QUICKSTART.md))

3. Create a feature branch:
   ```bash
   cd data
   git checkout -b feature/your-feature-name
   ```

## Data Standards

### File Encoding

- **All files must be UTF-8 encoded**
- Use Unix line endings (LF, not CRLF)
- No BOM (Byte Order Mark)

### CSV Files

All CSV files should follow these rules:

- UTF-8 encoding
- Comma-separated values
- Header row required
- Quote fields containing commas
- Use empty string for null values (not "null" or "NULL")

Example:
```csv
title,medium,composition_date
"The Book of Thel",relief etching,1789
"Songs of Innocence",relief etching,1789
```

### XML Files

All XML files must:

- Be well-formed (validate with xmllint)
- Follow TEI P5 guidelines
- Use consistent indentation (2 or 4 spaces, not tabs)
- Include XML declaration: `<?xml version="1.0" encoding="UTF-8"?>`
- Have meaningful element IDs

Example structure:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<work id="thel" title="The Book of Thel">
    <metadata>
        <!-- Work metadata -->
    </metadata>
    <content>
        <!-- Work content -->
    </content>
</work>
```

### Naming Conventions

- **Work IDs**: Lowercase, short codes (e.g., `thel`, `songsie`, `mhh`)
- **Object IDs**: Work ID + copy + plate number (e.g., `thel.a.p1`)
- **File names**: Match IDs with appropriate extension (e.g., `thel.a.xml`)

## Adding New Content

### Adding a New Work

1. **Create the TEI XML file** in `works/`:
   ```bash
   works/newwork.a.xml
   ```

2. **Create the info file** in `info/`:
   ```bash
   info/newwork.info.xml
   ```

3. **Add entry to works.csv**:
   ```csv
   title,medium,composition_date,composition_date_value,image,copies,bad_id,info,info_filename,virtual,virtual_objects,preview,preview_copies
   "New Work Title",relief etching,1789,1789,newwork.1.1.com.100.jpg,newwork.a,newwork,"<p>Description...</p>",newwork.info.xml,0,,0,
   ```

4. **Validate**:
   ```bash
   python validate_data.py
   xmllint --noout works/newwork.a.xml
   xmllint --noout info/newwork.info.xml
   ```

5. **Test import**:
   ```bash
   cd ../archive/blakearchive
   python import.py '../../data'
   ```

6. **Verify in application**:
   - Check work appears in search
   - View work page
   - Verify all data displays correctly

### Adding Relationships

Edit `csv/blake-relations.csv`:

```csv
object_id,related_object_id,relationship_type,notes
thel.a.p1,songsie.a.p2,motif,"Similar imagery"
```

Relationship types:
- `motif` - Visual motifs
- `matrix` - Same printing matrix
- `production_sequence` - Production sequence
- `textual_reference` - Textual references

### Adding an Exhibit

1. **Create exhibit XML** in `exhibits/`:
   ```bash
   exhibits/category/exhibit-name.xml
   ```

2. **Follow exhibit schema**:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <exhibit id="exhibit-name" title="Exhibit Title">
       <description>
           <p>Exhibit description...</p>
       </description>
       <images>
           <image id="image1" dbi="image.file.name" />
       </images>
   </exhibit>
   ```

3. **Validate and test**:
   ```bash
   xmllint --noout exhibits/category/exhibit-name.xml
   python validate_data.py
   ```

### Adding Featured Works

Edit `csv/home-page-images.csv`:

```csv
dbi,desc_id,byline,title,bad_id
image.file.name,object.desc.id,Artist Name - Year,Work Title,work_id
```

## Modifying Existing Content

### Updating Work Information

1. **Find the work**:
   ```bash
   grep -r "work title" info/
   ```

2. **Edit the info file**:
   ```bash
   vi info/workid.info.xml
   ```

3. **Validate and test**:
   ```bash
   xmllint --noout info/workid.info.xml
   python validate_data.py
   cd ../archive/blakearchive
   python import.py '../../data'
   ```

### Updating Relationships

1. **Edit blake-relations.csv**
2. **Validate**:
   ```bash
   python validate_data.py
   ```
3. **Re-import**:
   ```bash
   cd ../archive/blakearchive
   python import.py '../../data'
   ```

### Fixing Data Errors

If you find errors:

1. **Document the error** - Note what's wrong and where
2. **Research the correct information** - Use reliable sources
3. **Make the correction** in the appropriate file
4. **Validate** your changes
5. **Test** in the application
6. **Document** in commit message what was fixed and why

## Testing Your Changes

### 1. Automated Validation

Run the validation script:
```bash
python validate_data.py
```

All checks should pass (0 errors). Warnings are okay but should be reviewed.

### 2. XML Validation

Validate specific XML files:
```bash
xmllint --noout works/*.xml
xmllint --noout info/*.xml
```

### 3. Import Test

Test the import process:
```bash
cd ../archive/blakearchive
python import.py '../../data'
python solrimport.py
python homepageimport.py '../../data'
```

Check for error messages in the output.

### 4. Application Testing

1. Start the application (Flask + Angular)
2. Test your specific changes:
   - Search for affected works
   - View affected pages
   - Check images load
   - Verify relationships display

3. Test related functionality:
   - Search still works
   - Related works display correctly
   - Navigation works

### 5. Browser Testing

Test in multiple browsers:
- Chrome/Edge
- Firefox
- Safari

## Submitting Changes

### 1. Commit Your Changes

```bash
git add <changed files>
git commit -m "Descriptive commit message

- Detail what was changed
- Explain why it was changed
- Note any related issues"
```

### 2. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 3. Create Pull Request

1. Go to GitHub
2. Create pull request from your branch
3. Fill in the PR template:
   - **What**: Describe changes
   - **Why**: Explain reasoning
   - **Testing**: Document testing done
   - **Validation**: Confirm validation passed

### 4. PR Checklist

Before submitting, verify:

- [ ] All validation checks pass
- [ ] XML files are well-formed
- [ ] CSV files are UTF-8 encoded
- [ ] Import scripts run without errors
- [ ] Changes tested in application
- [ ] Commit messages are descriptive
- [ ] No unrelated changes included
- [ ] Documentation updated (if needed)

## Best Practices

### Do's ✅

- **Validate frequently** - Run `validate_data.py` often
- **Test thoroughly** - Test in the actual application
- **Document changes** - Clear commit messages
- **Follow standards** - Maintain consistency
- **Ask questions** - If unsure, ask before making changes
- **Back up data** - Keep copies before major changes

### Don'ts ❌

- **Don't skip validation** - Always run validation scripts
- **Don't mix changes** - One logical change per commit
- **Don't break compatibility** - Maintain data format
- **Don't guess** - Research correct information
- **Don't commit secrets** - No credentials or keys
- **Don't use tabs** - Use spaces for indentation

## Common Tasks

### Add a Copy to an Existing Work

1. Create XML file: `works/workid.newcopy.xml`
2. Update `csv/works.csv` - add copy to `copies` field
3. Validate and test

### Fix a Typo in Work Info

1. Edit `info/workid.info.xml`
2. Validate: `xmllint --noout info/workid.info.xml`
3. Re-import: `python import.py '../../data'`

### Update Composition Date

1. Edit `csv/works.csv`
2. Update both `composition_date` and `composition_date_value`
3. Validate and re-import

### Add Text Matches

1. Edit `csv/blake_superfast_matches.csv`
2. Add row with object IDs and match info
3. Validate and re-import

## Getting Help

### Documentation

- [README.md](README.md) - Repository overview
- [CLAUDE_BRANCH_COMPATIBILITY.md](CLAUDE_BRANCH_COMPATIBILITY.md) - Integration guide
- [INTEGRATION_CHECKLIST.md](INTEGRATION_CHECKLIST.md) - Setup checklist

### Support Channels

- **GitHub Issues** - Report bugs or ask questions
- **Pull Requests** - Discuss proposed changes
- **Documentation** - Review existing docs first

### Useful Commands

```bash
# Validate all data
python validate_data.py

# Validate specific XML
xmllint --noout works/workid.xml

# Check encoding
file -bi filename.csv

# Find works by title
grep -i "title" csv/works.csv

# Import with helper
./import_helper.sh
```

## Code of Conduct

- Be respectful and professional
- Focus on the data and scholarship
- Collaborate and communicate
- Accept constructive feedback
- Help maintain data quality

## Questions?

If you have questions:

1. Check this guide and other documentation
2. Search existing GitHub issues
3. Open a new issue with your question
4. Be specific about what you're trying to do

---

Thank you for contributing to the Blake Archive! Your work helps preserve and share William Blake's incredible artistic legacy. 🎨
