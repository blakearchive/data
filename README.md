# Blake Archive Data Repository

This repository contains the data files for the Blake Archive application. It works in conjunction with the [blakearchive/archive](https://github.com/blakearchive/archive) repository, which contains the web application (Flask backend + Angular frontend).

## Repository Structure

```
data/
├── csv/                          # CSV metadata files
│   ├── blake-relations.csv       # Relationships between objects
│   ├── blake_superfast_matches.csv  # Text matching data
│   ├── works.csv                 # Works metadata
│   ├── copy-handprints.csv       # Copy handprint information
│   └── home-page-images.csv      # Featured works for homepage
├── works/                        # TEI-encoded XML files for works
│   └── *.xml                     # Individual work files
├── info/                         # Information files for works
│   └── *.info.xml               # Work information files
├── exhibits/                     # Exhibition data
│   └── **/*.xml                 # Exhibition files
├── groups/                       # Virtual group definitions
│   └── *.xml                    # Virtual copy group files
├── previews/                     # Preview content
│   └── **/*.xml                 # Preview files
├── thesaurus/                    # Thesaurus data
│   └── thesaurus.xml            # Controlled vocabulary
└── webpages/                     # Static webpage content
    └── various HTML/XML files
```

## Integration with Archive Repository

### Setup

The Blake Archive application expects both repositories to be cloned in the same parent directory:

```bash
cd /path/to/your/projects
git clone https://github.com/blakearchive/data.git
git clone https://github.com/blakearchive/archive.git
```

### Data Import Process

The archive repository contains three Python import scripts that read data from this repository:

1. **import.py** - Imports works, copies, objects, exhibits, and relationships
   ```bash
   cd archive/blakearchive
   python import.py '../../data'
   ```

   This script reads:
   - `csv/blake-relations.csv` - Object and work relationships
   - `csv/blake_superfast_matches.csv` - Text matching data
   - `csv/works.csv` - Work metadata
   - `csv/copy-handprints.csv` - Copy handprint information
   - `works/*.xml` - TEI-encoded work files
   - `info/*.xml` - Work information files
   - `exhibits/**/*.xml` - Exhibition files
   - `groups/*.xml` - Virtual copy groups

2. **solrimport.py** - Populates Solr search indexes
   ```bash
   cd archive/blakearchive
   python solrimport.py
   ```

   This script reads from the PostgreSQL database (populated by import.py) and creates Solr indexes for:
   - Blake objects
   - Blake copies
   - Blake works

3. **homepageimport.py** - Imports featured works for the homepage
   ```bash
   cd archive/blakearchive
   python homepageimport.py '../../data'
   ```

   This script reads:
   - `csv/home-page-images.csv` - Featured works configuration

### Compatibility with Claude Branch Enhancements

This data repository is fully compatible with the modernized Angular 20 application in the claude branches of the archive repository. The enhancements in the claude branch include:

- **Modern Angular 20** - Complete migration from AngularJS 1.8 to Angular 20
- **TypeScript** - Full type safety throughout the frontend
- **Improved Architecture** - Standalone components with lazy loading
- **Better Performance** - Optimized bundle sizes and faster load times

**No changes to the data format or structure are required** - the import scripts and API endpoints remain compatible with this data repository.

### Data Format

#### CSV Files

All CSV files should be UTF-8 encoded and follow standard CSV format with headers.

**works.csv** structure:
- `title` - Work title
- `medium` - Medium of the work
- `composition_date` - Human-readable composition date
- `composition_date_value` - Numeric year value for sorting
- `image` - Featured image filename
- `copies` - Associated copy IDs
- `bad_id` - Blake Archive ID
- `info` - Information text
- `info_filename` - Associated info file
- `virtual` - Whether this is a virtual work (0/1)
- `virtual_objects` - Virtual object associations
- `preview` - Whether this work has a preview (0/1)
- `preview_copies` - Preview copy IDs

#### XML Files

All XML files in `works/`, `info/`, `exhibits/`, and `groups/` should follow the Blake Archive TEI schema. The import scripts use LXML for parsing and expect well-formed XML.

## Updating Data

When making changes to the data:

1. **Edit the appropriate files** in this repository
2. **Test locally** by running the import scripts in the archive repository
3. **Commit and push** to this repository
4. **Re-import** in any deployed environments:
   ```bash
   cd archive/blakearchive
   python import.py '../../data'
   python solrimport.py
   python homepageimport.py '../../data'
   ```

### Common Data Updates

- **Adding a new work**: Add XML to `works/`, info XML to `info/`, entry to `csv/works.csv`
- **Updating relationships**: Modify `csv/blake-relations.csv`
- **Changing featured works**: Update `csv/home-page-images.csv`
- **Adding exhibitions**: Add XML files to `exhibits/`

## Validation

To validate data integrity:

1. Ensure all CSV files are UTF-8 encoded
2. Validate XML files are well-formed: `xmllint --noout works/*.xml`
3. Check that all referenced files exist (e.g., image files referenced in works.csv)
4. Ensure consistent ID usage across CSV and XML files

## Development Workflow

### Local Development

1. Clone both repositories
2. Set up the archive application (see archive/README.md)
3. Import data using the scripts above
4. Make changes to data files
5. Re-run import scripts to test changes
6. Verify changes in the running application

### Production Deployment

When deploying to production:

1. Pull latest changes from both repositories
2. Run all three import scripts in order
3. Restart the Flask application
4. Clear Solr caches if needed

## Troubleshooting

**Import script errors:**
- Check file paths are correct (relative to archive/blakearchive/)
- Ensure CSV files are UTF-8 encoded
- Validate XML files with xmllint
- Check PostgreSQL and Solr are running

**Missing data in application:**
- Verify import scripts completed without errors
- Check Solr indexes were populated
- Clear browser cache and Solr caches
- Check application logs for errors

## Additional Resources

- [Archive Repository](https://github.com/blakearchive/archive)
- [Blake Archive Website](http://www.blakearchive.org)
- Archive Setup Guide: See archive/README.md

## License

This data is maintained for the William Blake Archive project.
