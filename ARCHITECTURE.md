# Blake Archive Architecture Overview

This document provides a high-level overview of how the data repository integrates with the archive application.

## Repository Relationship

```
┌─────────────────────────────────────────────────────────────┐
│                     Project Structure                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  blake-archive/                                              │
│  ├── data/              ← THIS REPOSITORY (Data Storage)    │
│  │   ├── csv/          ← Metadata CSV files                 │
│  │   ├── works/        ← TEI XML work files                 │
│  │   ├── info/         ← Work information                   │
│  │   ├── exhibits/     ← Exhibition data                    │
│  │   └── ...                                                 │
│  │                                                            │
│  └── archive/          ← Application Repository             │
│      ├── blakearchive/ ← Flask Backend (Python)             │
│      │   ├── import.py        (reads from ../data/)         │
│      │   ├── models.py        (database models)             │
│      │   ├── routes.py        (API endpoints)               │
│      │   └── solrimport.py    (search indexing)             │
│      │                                                        │
│      └── frontend/     ← Angular Frontend (TypeScript)      │
│          └── src/      ← Modern Angular 20 app              │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## Data Flow

### Import Process

```
┌──────────────┐
│  Data Repo   │
│              │
│  CSV Files   │ ──┐
│  XML Files   │   │
│  Exhibits    │   │
└──────────────┘   │
                   ├──> import.py ──> PostgreSQL Database
                   │                         │
                   │                         ├─> SQLAlchemy Models
                   │                         │   (BlakeWork, BlakeCopy,
                   │                         │    BlakeObject, etc.)
                   │                         │
                   │                         └─> solrimport.py ──> Solr Indexes
                   │                                                   │
                   │                                                   ├─> blake_object
                   │                                                   ├─> blake_copy
                   │                                                   └─> blake_work
                   │
                   └──> homepageimport.py ──> Featured Works Table
```

### Runtime Architecture

```
┌─────────────────┐
│   Web Browser   │
│  (Angular App)  │
└────────┬────────┘
         │ HTTP Requests
         │
         ▼
┌─────────────────┐
│  Angular 20     │
│  Frontend       │     ┌──────────────────────┐
│                 │     │  Development Mode    │
│  Components:    │     │  http://localhost:   │
│  - Home         │◄────┤  :4200 (Angular)     │
│  - Search       │     │  :5000 (Flask)       │
│  - Work         │     │                      │
│  - Copy         │     │  Production Mode     │
│  - Object       │     │  Flask serves both   │
│  - Lightbox     │     │  frontend & API      │
│  etc.           │     └──────────────────────┘
└────────┬────────┘
         │ API Calls (/api/*)
         │
         ▼
┌─────────────────────────────────────────┐
│         Flask Backend                    │
│                                          │
│  Routes (API Endpoints):                │
│  GET  /api/work/{id}                    │
│  GET  /api/copy/{id}                    │
│  GET  /api/object/{id}                  │
│  POST /api/query_objects                │
│  POST /api/query_works                  │
│  etc.                                    │
└─────┬─────────────────────┬─────────────┘
      │                     │
      ▼                     ▼
┌──────────────┐    ┌──────────────┐
│ PostgreSQL   │    │    Solr      │
│   Database   │    │   Indexes    │
│              │    │              │
│ Tables:      │    │ Cores:       │
│ - work       │    │ - blake_work │
│ - copy       │    │ - blake_copy │
│ - object     │    │ - blake_object│
│ - exhibit    │    └──────────────┘
│ - featured   │
│   _work      │
│ etc.         │
└──────────────┘
```

## Component Responsibilities

### Data Repository (This Repo)

**Purpose**: Source of truth for Blake Archive content

**Contains**:
- Original TEI XML files for works
- Metadata CSV files
- Exhibition and preview content
- Virtual groups
- Thesaurus data

**Responsibilities**:
- ✅ Store authoritative Blake content
- ✅ Maintain data integrity
- ✅ Version control for content changes
- ✅ Provide validation tools

**Does NOT**:
- ❌ Run any services
- ❌ Process data at runtime
- ❌ Serve web requests
- ❌ Maintain databases

### Archive Repository - Backend

**Purpose**: Application server and data processing

**Contains**:
- Flask web framework
- SQLAlchemy models
- Import scripts
- API routes

**Responsibilities**:
- ✅ Import data from data repo into PostgreSQL
- ✅ Index data in Solr for search
- ✅ Serve RESTful API endpoints
- ✅ Handle business logic
- ✅ Manage database connections

### Archive Repository - Frontend

**Purpose**: User interface

**Contains**:
- Angular 20 application
- TypeScript components
- Stylesheets and assets

**Responsibilities**:
- ✅ Render user interface
- ✅ Handle user interactions
- ✅ Make API requests
- ✅ Manage client-side state
- ✅ Display images and content

## Technology Stack

### Data Repository
```
├── Python Scripts (validation)
├── CSV (structured metadata)
├── TEI XML (content encoding)
└── Bash Scripts (helpers)
```

### Backend Stack
```
┌─────────────────────────────┐
│  Flask 3.1.0                │  Web Framework
├─────────────────────────────┤
│  SQLAlchemy 2.0.36          │  ORM
├─────────────────────────────┤
│  PostgreSQL 14+             │  Database
├─────────────────────────────┤
│  Apache Solr 8.11+          │  Search Engine
├─────────────────────────────┤
│  lxml, pandas, xmltodict    │  Data Processing
└─────────────────────────────┘
```

### Frontend Stack
```
┌─────────────────────────────┐
│  Angular 20                 │  Framework
├─────────────────────────────┤
│  TypeScript 5.7+            │  Language
├─────────────────────────────┤
│  RxJS 7.8+                  │  Reactive Programming
├─────────────────────────────┤
│  Standalone Components      │  Architecture
├─────────────────────────────┤
│  Signals                    │  State Management
└─────────────────────────────┘
```

## Data Models

### Core Entities

```
┌──────────────┐
│   BlakeWork  │
│              │
│ - bad_id     │ (primary key)
│ - title      │
│ - medium     │
│ - comp_date  │
└──────┬───────┘
       │
       │ has many
       │
       ▼
┌──────────────┐
│  BlakeCopy   │
│              │
│ - copy_id    │ (primary key)
│ - work_id    │ (foreign key)
│ - institution│
│ - print_date │
└──────┬───────┘
       │
       │ has many
       │
       ▼
┌──────────────┐
│ BlakeObject  │
│              │
│ - object_id  │ (primary key)
│ - copy_id    │ (foreign key)
│ - desc_id    │
│ - dbi        │
│ - text       │
│ - components │
└──────────────┘
```

### Additional Entities

```
BlakeExhibit     → Exhibition collections
BlakePreview     → Preview content
BlakeFragmentPair → Text fragment matches
FeaturedWork     → Homepage featured works
```

### Relationships

```
┌──────────────────────────────────────────────┐
│         Object Relationships                  │
├──────────────────────────────────────────────┤
│                                               │
│  matrix__object             Many-to-Many     │
│  production_sequence__object Many-to-Many    │
│  motif__object              Many-to-Many     │
│  text_match__object         Many-to-Many     │
│  textual_reference__object  Many-to-Many     │
│  textual_reference__copy    Many-to-Many     │
│  textual_reference__work    Many-to-Many     │
│                                               │
└──────────────────────────────────────────────┘
```

## API Endpoints

### Work Endpoints
```
GET  /api/work/{work_id}          Get work details
GET  /api/work/{work_id}/copies   Get copies for work
```

### Copy Endpoints
```
GET  /api/copy/{copy_id}          Get copy details
GET  /api/copy/{copy_id}/objects  Get objects for copy
```

### Object Endpoints
```
GET  /api/object/{desc_id}        Get object details
```

### Search Endpoints
```
POST /api/query_objects           Search objects
POST /api/query_copies            Search copies
POST /api/query_works             Search works
```

### Other Endpoints
```
GET  /api/exhibit/{exhibit_id}    Get exhibit
GET  /api/preview/{preview_id}    Get preview
GET  /api/featured_works          Get featured works
```

## Search Architecture

### Solr Cores

```
blake_object
├── Full-text search on:
│   ├── Transcribed text
│   ├── Illustration descriptions
│   ├── Object notes
│   └── Components
└── Faceted search on:
    ├── Medium
    ├── Date
    └── Work/Copy

blake_copy
├── Search on:
│   ├── Copy title
│   ├── Institution
│   └── Header
└── Filter by:
    ├── Composition date
    └── Print date

blake_work
├── Search on:
│   ├── Work title
│   └── Work information
└── Filter by:
    ├── Medium
    └── Composition date
```

## Development Workflow

```
1. Edit Data Files
   (CSV or XML in data repo)
          │
          ▼
2. Validate
   python validate_data.py
          │
          ▼
3. Import to Database
   python import.py
          │
          ▼
4. Index in Solr
   python solrimport.py
          │
          ▼
5. Test in Browser
   http://localhost:4200
```

## Deployment Architecture

### Development
```
┌──────────────┐    ┌──────────────┐
│   Angular    │    │    Flask     │
│  Dev Server  │───▶│   Server     │
│              │    │              │
│  :4200       │    │   :5000      │
└──────────────┘    └──────┬───────┘
                           │
                ┌──────────┴────────┐
                │                   │
                ▼                   ▼
         ┌──────────┐        ┌──────────┐
         │PostgreSQL│        │  Solr    │
         └──────────┘        └──────────┘
```

### Production
```
┌──────────────────────────────┐
│      Web Server (Nginx)      │
│                               │
│  Static Files + Proxy         │
└────────────┬─────────────────┘
             │
             ▼
┌──────────────────────────────┐
│      Flask + WSGI            │
│                               │
│  - Serves API                 │
│  - Serves built Angular app   │
└────────────┬─────────────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
┌──────────┐  ┌──────────┐
│PostgreSQL│  │  Solr    │
└──────────┘  └──────────┘
```

## Performance Considerations

### Data Import
- **Duration**: 5-10 minutes for full import
- **Frequency**: Only when data changes
- **Impact**: No downtime during import

### Solr Indexing
- **Duration**: 2-5 minutes
- **Frequency**: After data import
- **Impact**: Search may be stale during reindex

### Frontend Build
- **Duration**: 1-2 minutes
- **Frequency**: When frontend code changes
- **Output**: Optimized bundles (~300KB gzipped)

## Scaling Considerations

### Database
- PostgreSQL handles the full dataset easily
- Indexes on key fields for performance
- Connection pooling for concurrent users

### Search
- Solr provides fast full-text search
- Handles complex queries efficiently
- Can be scaled horizontally if needed

### Frontend
- Static assets can be CDN-cached
- Code splitting for lazy loading
- Image optimization recommended

## Security

### Data Repository
- No sensitive data stored
- Public-facing content only
- Version controlled for auditability

### Backend
- Database credentials in config (not versioned)
- API is read-only (no write endpoints)
- Input validation on search parameters

### Frontend
- CSP headers recommended
- XSS protection via Angular sanitization
- HTTPS in production

## Monitoring & Maintenance

### Health Checks
```bash
# Database
psql -U postgres -c "SELECT count(*) FROM work;"

# Solr
curl http://localhost:8983/solr/admin/cores?action=STATUS

# Application
curl http://localhost:5000/api/featured_works
```

### Regular Maintenance
- [ ] Database backups (weekly recommended)
- [ ] Solr index optimization (after major updates)
- [ ] Log rotation
- [ ] Dependency updates

## Future Enhancements

Potential areas for improvement:

- **API Caching**: Redis for frequently accessed data
- **CDN**: For static assets and images
- **GraphQL**: Alternative to REST API
- **Elasticsearch**: Alternative to Solr
- **Containerization**: Docker for easier deployment
- **CI/CD**: Automated testing and deployment

---

This architecture maintains separation of concerns while ensuring smooth data flow from the source files to the user interface. The modular design allows each component to be updated independently while maintaining compatibility.
