# Quick Start Guide

Get up and running with the Blake Archive in under 10 minutes!

## Prerequisites

Make sure you have:
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Solr 8.11+

## 5-Step Setup

### 1️⃣ Clone Both Repositories

```bash
mkdir blake-archive
cd blake-archive
git clone https://github.com/blakearchive/data.git
git clone https://github.com/blakearchive/archive.git
```

### 2️⃣ Set Up Archive Application

```bash
cd archive

# Checkout the modernized Angular 20 version
git checkout claude/modernize-framework-011CUrmRaN8ZWgGznb5NtPwK

# Install Python dependencies
pip install pipenv
pipenv install
pipenv shell

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 3️⃣ Configure Database

```bash
# Create PostgreSQL database
psql -U postgres -c "CREATE DATABASE blake_archive;"

# Copy and edit config
cp config.py.example blakearchive/config.py
# Edit blakearchive/config.py with your database credentials
```

### 4️⃣ Set Up Solr (Optional but Recommended)

```bash
# In your Solr installation directory
cd /path/to/solr
bin/solr start

# Create cores
cd server/solr
mkdir blake_object blake_copy blake_work

# Link configurations
ln -s /path/to/archive/solr/blake-object/conf blake_object/conf
ln -s /path/to/archive/solr/blake-copy/conf blake_copy/conf
ln -s /path/to/archive/solr/blake-work/conf blake_work/conf

# In Solr admin (http://localhost:8983/solr/admin):
# Add cores: blake_object, blake_copy, blake_work
```

### 5️⃣ Import Data and Run

```bash
cd blakearchive

# Import data (from the data repository)
python import.py '../../data'
python solrimport.py  # If Solr is set up
python homepageimport.py '../../data'

# Start backend
cd ..
python run.py  # Runs on http://localhost:5000

# In another terminal, start frontend
cd frontend
npm start  # Runs on http://localhost:4200
```

## ✅ Verify It's Working

Open http://localhost:4200 in your browser. You should see:
- Featured works on the home page
- Working search functionality
- Ability to browse works, copies, and objects

## 🚀 Even Faster: Use the Helper Script

From the data repository:

```bash
cd data
./import_helper.sh
```

This automatically:
- Validates your data
- Imports everything
- Rebuilds Solr indexes
- Shows helpful next steps

## 📝 Making Changes

### Update Data

1. Edit files in the `data/` repository
2. Validate: `python validate_data.py`
3. Re-import: `cd ../archive/blakearchive && python import.py '../../data'`
4. Restart Flask and clear browser cache

### Develop Frontend

1. Make changes in `archive/frontend/src/`
2. Changes auto-reload at http://localhost:4200
3. No restart needed!

### Develop Backend

1. Make changes in `archive/blakearchive/`
2. Restart Flask: `Ctrl+C` then `python run.py`

## 🔍 Troubleshooting

**Port already in use?**
```bash
# Change Flask port in run.py
# Change Angular port: npm start -- --port 4201
```

**Database connection error?**
```bash
# Check PostgreSQL is running
psql -U postgres -l
# Verify credentials in config.py
```

**Import errors?**
```bash
# Validate data first
cd data
python validate_data.py
```

**Frontend not loading?**
```bash
# Clear npm cache and reinstall
cd archive/frontend
rm -rf node_modules package-lock.json
npm install
```

## 📚 Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [CLAUDE_BRANCH_COMPATIBILITY.md](CLAUDE_BRANCH_COMPATIBILITY.md) for integration details
- Use [INTEGRATION_CHECKLIST.md](INTEGRATION_CHECKLIST.md) for systematic setup
- Review [CONTRIBUTING.md](CONTRIBUTING.md) to add/modify data

## 🆘 Need Help?

1. Check the troubleshooting sections in README.md
2. Run `python validate_data.py` to check data integrity
3. Review application logs
4. Open an issue on GitHub

---

**Happy coding!** 🎨 You're now ready to work with the Blake Archive.
