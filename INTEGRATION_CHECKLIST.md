# Integration Checklist

Use this checklist when setting up or updating the Blake Archive application with data from this repository.

## Initial Setup

### 1. Prerequisites
- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] PostgreSQL 14+ installed and running
- [ ] Solr 8.11+ installed and running
- [ ] Git installed

### 2. Clone Repositories
```bash
cd /your/project/directory
[ ] git clone https://github.com/blakearchive/data.git
[ ] git clone https://github.com/blakearchive/archive.git
```

### 3. Checkout Claude Branch (for modernized app)
```bash
cd archive
[ ] git checkout claude/modernize-framework-011CUrmRaN8ZWgGznb5NtPwK
[ ] git status  # Verify you're on the correct branch
```

### 4. Install Python Dependencies
```bash
cd archive
[ ] pip install pipenv
[ ] pipenv install
[ ] pipenv shell
```

Or with virtualenv:
```bash
[ ] pip install virtualenv
[ ] virtualenv venv
[ ] source venv/bin/activate  # On Windows: venv\Scripts\activate
[ ] pip install -r requirements.txt
```

### 5. Install Frontend Dependencies
```bash
cd archive/frontend
[ ] npm install
```

### 6. Configure Database
```bash
# PostgreSQL setup
[ ] Create database: CREATE DATABASE blake_archive;
[ ] Copy config: cp config.py.example blakearchive/config.py
[ ] Edit blakearchive/config.py with your database credentials
```

### 7. Configure Solr
```bash
cd /path/to/solr
[ ] Start Solr: bin/solr start
[ ] Create cores: blake_object, blake_copy, blake_work
[ ] Link configs from archive/solr/* to Solr cores
```

### 8. Validate Data
```bash
cd /path/to/data
[ ] python validate_data.py
[ ] Verify all checks pass (0 errors)
```

### 9. Import Data
```bash
cd /path/to/archive/blakearchive
[ ] python import.py '../../data'
[ ] python solrimport.py
[ ] python homepageimport.py '../../data'
[ ] Check for any error messages
```

### 10. Start Application
```bash
# Terminal 1 - Backend
cd archive
[ ] python run.py
[ ] Verify running on http://localhost:5000

# Terminal 2 - Frontend
cd archive/frontend
[ ] npm start
[ ] Verify running on http://localhost:4200
```

### 11. Verify Application
- [ ] Open http://localhost:4200 in browser
- [ ] Home page loads with featured works
- [ ] Search functionality works
- [ ] Can view a work page
- [ ] Can view a copy page
- [ ] Can view an object page
- [ ] Images load correctly
- [ ] No console errors

---

## Updating Data

Use this checklist when you make changes to the data repository.

### Before Making Changes
- [ ] Pull latest changes from both repositories
- [ ] Verify application is running correctly
- [ ] Make note of current data state

### Making Changes
- [ ] Edit CSV or XML files as needed
- [ ] Follow data format guidelines in README.md
- [ ] Keep backup of original files (if major changes)

### After Making Changes
- [ ] Run validation: `python validate_data.py`
- [ ] Fix any validation errors
- [ ] Re-import data:
  ```bash
  cd /path/to/archive/blakearchive
  python import.py '../../data'
  python solrimport.py  # If search data changed
  python homepageimport.py '../../data'  # If homepage data changed
  ```
- [ ] Check import logs for errors
- [ ] Restart Flask server (if running)
- [ ] Clear browser cache (Ctrl+Shift+R)
- [ ] Verify changes in application
- [ ] Test affected functionality

### Commit Changes
- [ ] Review changes: `git status`
- [ ] Add files: `git add <files>`
- [ ] Commit with descriptive message
- [ ] Push to appropriate branch

---

## Common Tasks

### Adding a New Work
- [ ] Create TEI XML file in `works/`
- [ ] Create info XML file in `info/`
- [ ] Add entry to `csv/works.csv`
- [ ] Add related entries to `csv/blake-relations.csv` (if needed)
- [ ] Run validation script
- [ ] Re-import data
- [ ] Verify work appears in application

### Updating Work Information
- [ ] Edit corresponding file in `info/`
- [ ] Or edit entry in `csv/works.csv`
- [ ] Run validation script
- [ ] Re-import: `python import.py '../../data'`
- [ ] Verify changes in application

### Adding Relationships
- [ ] Edit `csv/blake-relations.csv`
- [ ] Run validation script
- [ ] Re-import: `python import.py '../../data'`
- [ ] Verify relationships in application

### Updating Featured Works
- [ ] Edit `csv/home-page-images.csv`
- [ ] Run validation script
- [ ] Re-import: `python homepageimport.py '../../data'`
- [ ] Clear browser cache
- [ ] Verify home page

### Adding/Updating Exhibits
- [ ] Create or edit XML in `exhibits/`
- [ ] Run validation script
- [ ] Re-import: `python import.py '../../data'`
- [ ] Verify exhibit in application

---

## Troubleshooting

### Validation Errors
- [ ] Check error messages from `validate_data.py`
- [ ] Verify file encoding is UTF-8
- [ ] Validate XML with xmllint
- [ ] Check for special characters or formatting issues

### Import Errors
- [ ] Check Python error messages
- [ ] Verify database is running
- [ ] Verify file paths are correct
- [ ] Check database credentials in config.py
- [ ] Look for malformed XML or CSV

### Application Not Working
- [ ] Check both Flask and Angular are running
- [ ] Check browser console for errors
- [ ] Clear browser cache
- [ ] Check Flask logs
- [ ] Verify data was imported successfully
- [ ] Check Solr is running (http://localhost:8983/solr)

### Search Not Working
- [ ] Verify Solr is running
- [ ] Check Solr cores exist
- [ ] Re-run solrimport.py
- [ ] Check Solr admin interface
- [ ] Look for errors in Flask logs

### Images Not Loading
- [ ] Verify image paths in CSV files
- [ ] Check image directory in config.py
- [ ] Verify image files exist
- [ ] Check file permissions
- [ ] Review Flask logs for path errors

---

## Production Deployment

### Pre-Deployment
- [ ] All validation checks pass
- [ ] All tests pass
- [ ] Code reviewed and merged
- [ ] Database backup created
- [ ] Solr indexes backed up

### Deployment Steps
- [ ] Pull latest code
- [ ] Install/update dependencies
- [ ] Run database migrations (if any)
- [ ] Import updated data
- [ ] Rebuild Solr indexes
- [ ] Build frontend: `npm run build`
- [ ] Restart application server
- [ ] Clear CDN/proxy caches

### Post-Deployment
- [ ] Verify application is accessible
- [ ] Smoke test key functionality
- [ ] Monitor logs for errors
- [ ] Check performance metrics
- [ ] Verify search is working
- [ ] Test on multiple browsers/devices

---

## Quick Reference Commands

### Validation
```bash
python validate_data.py
```

### Full Data Import
```bash
cd archive/blakearchive
python import.py '../../data'
python solrimport.py
python homepageimport.py '../../data'
```

### Start Development
```bash
# Terminal 1
cd archive && python run.py

# Terminal 2
cd archive/frontend && npm start
```

### Database Reset (careful!)
```bash
psql -U postgres
DROP DATABASE blake_archive;
CREATE DATABASE blake_archive;
\q
# Then re-run import scripts
```

### Solr Index Reset
```bash
cd archive/blakearchive
python solrimport.py  # This clears and rebuilds indexes
```

---

## Need Help?

- [ ] Check README.md for documentation
- [ ] Check CLAUDE_BRANCH_COMPATIBILITY.md for integration details
- [ ] Review error messages carefully
- [ ] Check application logs
- [ ] Search GitHub issues
- [ ] Create new issue with details
