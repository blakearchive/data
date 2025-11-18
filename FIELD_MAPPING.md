# Blake Archive Field Mapping Guide

This guide shows exactly where each field in your CSV and XML files gets populated on the Blake Archive website.

## Quick Reference

```
Data Files → import.py → PostgreSQL Database → Flask API → Angular Frontend → Website Display
```

---

## 📊 CSV File: `works.csv`

Location: `data/csv/works.csv`

### Field Mappings

| CSV Column | Database Field | API Response | Website Display | Example |
|------------|----------------|--------------|-----------------|---------|
| `title` | `work.title` | `work.title` | **Work page header** | "Songs of Innocence" |
| `medium` | `work.medium` | `work.medium` | **Work page** (converted to label like "Illuminated Book") | `illbk` → "Illuminated Book" |
| `composition_date` | `work.composition_date_string` | `work.composition_date_string` | **Work page** in parentheses | "c. 1789" |
| `composition_date_value` | `work.composition_date` | `work.composition_date` | Used for sorting/filtering | `1789` |
| `image` | `work.image` | `work.image` | **Thumbnail images** on homepage/search | `songsie.a.p1-100.jpg` |
| `copies` | N/A (relationship) | `work.copies[]` | **List of copies** on work page | `songsie.a, songsie.b` |
| `bad_id` | `work.bad_id` | `work.bad_id` | **URL parameter**, identifiers | `songsie` |
| `info` | `work.info` | `work.work_information` | **"Work Information" section** on work page (HTML content) | `<p>Blake's illuminated...</p>` |
| `info_filename` | Used to locate info XML file | N/A | Processed into `work.info` | `songsie.info.xml` |
| `virtual` | `work.virtual` | `work.virtual` | Determines if work is virtual/composite | `0` or `1` |
| `preview` | `work.preview` | `work.preview` | Shows if work has preview available | `0` or `1` |

### Where You'll See It

**Work Page** (`/work/songsie`):
- Title at top: from `title`
- Medium label: from `medium` (converted to readable name)
- Composition date: from `composition_date`
- Work information text: from `info` (HTML rendered)
- List of copies: from `copies` relationship

**Search Results**:
- Thumbnail: from `image`
- Title: from `title`
- Medium filter: from `medium`
- Date range filter: from `composition_date_value`

**Homepage**:
- Featured work images: from `csv/home-page-images.csv` which references work images

---

## 📄 XML Files: `works/*.xml`

Location: `data/works/` (e.g., `songsie.a.xml`)

### Root Element Attributes

These are read from the root `<bad>` element:

| XML Attribute | Database Field | Website Display |
|---------------|----------------|-----------------|
| `id` | `copy.bad_id` | **Copy identifier** in URLs and headers |
| `type` | `copy.copy_type` | Determines copy type |
| `work` | `copy.work_id` | Links copy to parent work |

### Example:
```xml
<bad id="songsie.a" type="copy" work="songsie">
```
- `id="songsie.a"` → Copy page URL: `/copy/songsie.a`
- `work="songsie"` → Links to work page: `/work/songsie`

### Composition Date Elements

| XML Element | Database Field | Website Display |
|-------------|----------------|-----------------|
| `<objdescid><compdate>` | `copy.composition_date_string` | **Copy information** |
| Value extracted from text | `copy.composition_date` | Date filtering/sorting |

### Example:
```xml
<objdescid>
    <compdate>c. 1789</compdate>
</objdescid>
```
- Displays as: "Composed c. 1789" on copy page

### Print Date Elements

| XML Element | Database Field | Website Display |
|-------------|----------------|-----------------|
| `<printdate>` | `copy.print_date_string` | **Copy information section** |
| Value extracted | `copy.print_date` | Date filtering |

### Header Element

| XML Element | Database Field | Website Display |
|-------------|----------------|-----------------|
| `<header>` (entire element) | `copy.header` (JSON) | **Copy page header section** |

### Example:
```xml
<header>
    <filedesc>
        <titlestmt>
            <title>Songs of Innocence and of Experience</title>
            <author>William Blake</author>
        </titlestmt>
    </filedesc>
</header>
```
- Renders as formatted header on copy page

### Object Elements (`<desc>`)

Each `<desc>` element becomes a `BlakeObject`:

| XML Attribute/Element | Database Field | Website Display |
|----------------------|----------------|-----------------|
| `dbi` attribute | `object.dbi` | **Image filename** identifier |
| `id` attribute | `object.desc_id` | **Object URL**: `/object/{desc_id}` |
| `<objtitle>` | `object.title` | **Object page header** |
| `<physdesc>` | `object.physical_description` (JSON) | Physical description section |
| `<illusdesc>` | `object.illustration_description` (JSON) | **"Information" tab** on object page |
| `<phystext>` | `object.text` (JSON) | **"Transcription" tab** on object page |

### Example:
```xml
<desc dbi="songsie.a.p1" id="songsie.a.illbk.01">
    <objtitle>
        <title>Title Page</title>
    </objtitle>
    <physdesc>
        <objsize>18.4 x 12.1 cm</objsize>
        <windowsize>600 x 700 pixels</windowsize>
    </physdesc>
    <illusdesc>
        <illustration>
            <illusobjdesc>Blake depicted himself...</illusobjdesc>
        </illustration>
    </illusdesc>
    <phystext>
        <lg>
            <l>Songs of Innocence</l>
            <l>and of</l>
            <l>Experience</l>
        </lg>
    </phystext>
</desc>
```

**Result on Website**:
- **Copy page**: Shows thumbnail with "Title Page" caption
- **Object page** (`/object/songsie.a.illbk.01`):
  - Header: "Title Page"
  - Image tab: Shows image from `dbi` (songsie.a.p1)
  - Transcription tab: Shows formatted text "Songs of Innocence and of Experience"
  - Information tab: Shows illustration description

---

## 📋 CSV File: `blake-relations.csv`

Location: `data/csv/blake-relations.csv`

### Field Mappings

| CSV Column | Database Table | Website Display |
|------------|----------------|-----------------|
| `primary_desc_id` | `object_id` in relationship tables | Source object |
| `related_desc_id` | `related_object_id` | Related object |
| `relationship_type` | Determines which table: | Shows in "Related Objects" sections |
| - `motif` | `motif__object` | **"Same Motif"** section |
| - `matrix` | `matrix__object` | **"Same Matrix"** section |
| - `production_sequence` | `production_sequence__object` | **"Production Sequence"** section |
| - `textual_reference` | `textual_reference__object` | **"Textual Reference"** section |

### Example:
```csv
primary_desc_id,related_desc_id,relationship_type,notes
songsie.a.illbk.01,songsex.a.illbk.01,motif,"Similar composition"
```

**Result on Object Page**:
- Under "Related Objects" → "Same Motif" section
- Shows link to `songsex.a.illbk.01`
- Displays note: "Similar composition"

---

## 📋 CSV File: `blake_superfast_matches.csv`

Location: `data/csv/blake_superfast_matches.csv`

### Field Mappings

| CSV Column | Database Field | Website Display |
|------------|----------------|-----------------|
| `primary_desc_id` | `fragmentpair.desc_id1` | Source object |
| `match_desc_id` | `fragmentpair.desc_id2` | Matched object |
| `fragment` | `fragmentpair.fragment` | **Text fragment** shown in comparison |

### Example:
```csv
primary_desc_id,match_desc_id,fragment
songsie.a.illbk.05,songsex.a.illbk.05,"Little Lamb who made thee"
```

**Result on Object Page**:
- Under "Text Matches" section
- Shows matching object with shared text fragment
- Allows side-by-side comparison

---

## 📋 CSV File: `copy-handprints.csv`

Location: `data/csv/copy-handprints.csv`

### Field Mappings

| CSV Column | Database Field | Website Display |
|------------|----------------|-----------------|
| `copy_id` | `copy_handprint.copy_id` | Links to copy |
| `handprint_type` | `copy_handprint.handprint_type` | Type of handprint |
| `notes` | `copy_handprint.notes` | **Copy information** section |

### Example:
```csv
copy_id,handprint_type,notes
songsie.a,coloring,"Hand-colored by Blake"
```

**Result on Copy Page**:
- In "Copy Information" section
- Shows: "Coloring: Hand-colored by Blake"

---

## 📋 CSV File: `home-page-images.csv`

Location: `data/csv/home-page-images.csv`

### Field Mappings

| CSV Column | Database Field | Website Display |
|------------|----------------|-----------------|
| `dbi` | `featured_work.dbi` | **Image displayed** on homepage |
| `desc_id` | `featured_work.desc_id` | Links to object page |
| `byline` | `featured_work.byline` | **Caption text** below image |
| `title` | `featured_work.title` | **Title** in caption |
| `bad_id` | `featured_work.bad_id` | Links to work page |

### Example:
```csv
dbi,desc_id,byline,title,bad_id
songsie.a.p1,songsie.a.illbk.01,William Blake - 1789,Songs of Innocence,songsie
```

**Result on Homepage**:
- Featured image shows: `songsie.a.p1`
- Caption: "Songs of Innocence"
- Byline: "William Blake - 1789"
- Clicking goes to: `/work/songsie`

---

## 📄 XML Files: `info/*.info.xml`

Location: `data/info/` (e.g., `songsie.info.xml`)

### Field Mappings

The entire `<info>` element content is stored as HTML:

| XML Content | Database Field | Website Display |
|-------------|----------------|-----------------|
| All content inside `<info>` | `work.info` | **"Work Information"** section on work page |

### Example:
```xml
<info>
    <p>William Blake's <i>Songs of Innocence and of Experience</i>
    is one of the most important works of the Romantic period...</p>

    <p>First etched in 1789, <i>Songs of Innocence</i>...</p>
</info>
```

**Result on Work Page**:
- Entire content displayed in "Work Information" section
- HTML formatting preserved (italics, paragraphs, etc.)
- Can include images, links, and complex formatting

---

## 📄 XML Files: `exhibits/*.xml`

Location: `data/exhibits/` (e.g., `exhibits/gates/gates-sexes.xml`)

### Root Element Attributes

| XML Attribute | Database Field | Website Display |
|---------------|----------------|-----------------|
| `id` | `exhibit.exhibit_id` | **URL**: `/exhibit/{id}` |
| `title` | `exhibit.title` | **Exhibit page header** |
| `article` | `exhibit.article` | Article/essay content |
| `composition_date_string` | `exhibit.composition_date_string` | Exhibit date |

### Image Elements

Each `<image>` element in exhibit:

| XML Attribute | Database Field | Website Display |
|---------------|----------------|-----------------|
| `id` | `exhibit_image.image_id` | Image identifier |
| `dbi` | `exhibit_image.dbi` | **Image file** to display |
| `<title>` | `exhibit_image.title` | **Image caption title** |
| `<caption>` | `exhibit_caption.caption` | **Full image caption** |

### Example:
```xml
<exhibit id="gates-sexes" title="The Gates of Paradise: For the Sexes">
    <image id="img1" dbi="gates.a.p1">
        <title>Frontispiece</title>
        <caption title="What is Man!">
            The frontispiece shows...
        </caption>
    </image>
</exhibit>
```

**Result on Exhibit Page** (`/exhibit/gates-sexes`):
- Header: "The Gates of Paradise: For the Sexes"
- Image displayed: `gates.a.p1`
- Caption title: "What is Man!"
- Caption text: "The frontispiece shows..."

---

## 🖼️ Image Display

### How Image Paths are Constructed

Images are referenced by `dbi` field and constructed at runtime:

```
Database: object.dbi = "songsie.a.p1"
           ↓
API: Returns dbi in response
           ↓
Frontend: Constructs URL
           ↓
Display: /images/songsie.a.p1.100.jpg (thumbnail)
        /images/songsie.a.p1.300.jpg (medium)
        /images/songsie.a.p1.jpg     (full size)
```

### Image Sizes

The frontend automatically requests different sizes:
- **Thumbnails** (copy page grid): `.100.jpg`
- **Preview** (lightbox): `.300.jpg`
- **Full view** (object page): `.jpg` (original)

---

## 🔍 Search and Filtering

### Solr Index Fields

After import, `solrimport.py` creates searchable indexes:

#### blake_object Core

| Source Field | Solr Field | Searchable By |
|--------------|------------|---------------|
| `object.title` | `title` | Title search |
| `object.text` (JSON) | `text` | **Full-text search** |
| `object.illustration_description` (JSON) | `illustration_description` | **Description search** |
| `object.components` (JSON) | `components` | Component search |
| `object.notes` (JSON) | `notes` | Notes search |
| `copy.composition_date` | `composition_date` | **Date range filter** |
| `copy.institution` | `copy_institution` | **Institution filter** |
| `work.medium` | `medium` | **Medium filter** |

#### blake_copy Core

| Source Field | Solr Field | Searchable By |
|--------------|------------|---------------|
| `copy.title` | `title` | Copy title search |
| `copy.header` (JSON) | `header` | Header search |
| `copy.institution` | `institution` | **Institution filter** |
| `copy.composition_date` | `composition_date` | Date filter |

#### blake_work Core

| Source Field | Solr Field | Searchable By |
|--------------|------------|---------------|
| `work.title` | `title` | **Work title search** |
| `work.info` | `info` | **Work information search** |
| `work.medium` | `medium` | **Medium filter** |
| `work.composition_date` | `composition_date` | **Date filter** |

### Search Page Filters

When users search on `/search`:
- **Search box**: Queries `title`, `text`, `illustration_description`, `info`
- **Medium checkboxes**: Filters by `medium` field
- **Date sliders**: Filters by `composition_date` and `composition_date_value`
- **Institution dropdown**: Filters by `institution`

---

## 🎯 Complete Data Flow Example

Let's trace one work from CSV to website:

### 1. Source Data (`works.csv`)
```csv
title,medium,composition_date,composition_date_value,image,copies,bad_id,info,...
"Songs of Innocence",illbk,c. 1789,1789,songsie.a.p1-100.jpg,songsie.a,"<p>Blake's masterwork...</p>",songsie.info.xml,...
```

### 2. Source Data (`works/songsie.a.xml`)
```xml
<bad id="songsie.a" type="copy" work="songsie">
    <desc dbi="songsie.a.p1" id="songsie.a.illbk.01">
        <objtitle><title>Title Page</title></objtitle>
        <phystext>
            <lg><l>Songs of Innocence</l></lg>
        </phystext>
    </desc>
</bad>
```

### 3. After `python import.py '../../data'`

**work table**:
```
bad_id: songsie
title: Songs of Innocence
medium: illbk
composition_date: 1789
composition_date_string: c. 1789
info: <p>Blake's masterwork...</p>
```

**copy table**:
```
bad_id: songsie.a
work_id: songsie
```

**object table**:
```
desc_id: songsie.a.illbk.01
dbi: songsie.a.p1
title: Title Page
copy_bad_id: songsie.a
text: [JSON with "Songs of Innocence"]
```

### 4. After `python solrimport.py`

**blake_work index**:
```
id: songsie
title: Songs of Innocence
medium: illbk
composition_date: 1789
```

### 5. API Response (`GET /api/work/songsie`)
```json
{
  "bad_id": "songsie",
  "title": "Songs of Innocence",
  "medium": "illbk",
  "composition_date": "1789",
  "composition_date_string": "c. 1789",
  "work_information": "<p>Blake's masterwork...</p>"
}
```

### 6. Website Display (`/work/songsie`)

```
┌─────────────────────────────────┐
│  Illuminated Book               │ ← medium converted
│                                 │
│  Songs of Innocence (1789)      │ ← title + composition_date
│                                 │
│  Blake's masterwork...          │ ← work_information (HTML)
│                                 │
│  Copies:                        │
│  ┌─────────────────┐           │
│  │ Copy songsie.a  │           │ ← from copies relationship
│  │ View Copy →     │           │
│  └─────────────────┘           │
└─────────────────────────────────┘
```

---

## 📌 Quick Lookup Tables

### Where to Edit What

| To Change... | Edit This File... | Field Name... |
|--------------|-------------------|---------------|
| Work title | `csv/works.csv` | `title` |
| Work info text | `info/*.info.xml` | Content inside `<info>` |
| Composition date | `csv/works.csv` | `composition_date` & `composition_date_value` |
| Medium type | `csv/works.csv` | `medium` |
| Object transcription | `works/*.xml` | `<phystext>` element |
| Object description | `works/*.xml` | `<illusdesc>` element |
| Object title | `works/*.xml` | `<objtitle>` element |
| Copy institution | `works/*.xml` | `<institution>` in header |
| Related objects | `csv/blake-relations.csv` | Add row |
| Text matches | `csv/blake_superfast_matches.csv` | Add row |
| Homepage images | `csv/home-page-images.csv` | Add row |
| Exhibit content | `exhibits/**/*.xml` | Exhibit XML |

### Medium Codes

| Code | Website Display |
|------|-----------------|
| `illbk` | Illuminated Book |
| `cbi` | Commercial Book Illustration |
| `spri` | Separate Print |
| `mono` | Monotype |
| `draw` | Drawing |
| `paint` | Painting |
| `ms` | Manuscript |
| `rmpage` | Related Material |

---

## 🔧 Testing Your Changes

After editing data:

1. **Validate**: `python validate_data.py`
2. **Import**: `cd ../archive/blakearchive && python import.py '../../data'`
3. **Reindex**: `python solrimport.py` (if search data changed)
4. **Restart**: Restart Flask server
5. **Clear cache**: Hard refresh browser (Ctrl+Shift+R)
6. **Check pages**:
   - Work page: `/work/{bad_id}`
   - Copy page: `/copy/{copy_id}`
   - Object page: `/object/{desc_id}`
   - Search: `/search`
   - Homepage: `/`

---

## 💡 Common Questions

### Q: Where does the object image come from?
**A**: From the `dbi` attribute in `works/*.xml` → stored in `object.dbi` → frontend constructs image URL like `/images/{dbi}.jpg`

### Q: How do I add a new work?
**A**: Add to `works.csv`, create `works/{id}.xml`, create `info/{id}.info.xml`, then re-import

### Q: Where is the transcription text displayed?
**A**: From `<phystext>` in `works/*.xml` → `object.text` (JSON) → "Transcription" tab on object page

### Q: How do relationships work?
**A**: Add to `csv/blake-relations.csv` with `primary_desc_id`, `related_desc_id`, and `relationship_type` → shows in "Related Objects" sections

### Q: Can I use HTML in work information?
**A**: Yes! The `info` field in `works.csv` and `info/*.info.xml` supports full HTML

---

For more detailed information, see:
- [README.md](README.md) - Repository overview
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to add/edit data
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture

**Last Updated**: 2025-11-18
