# Modelo Relacional - Sistema de Reportes de Publicaciones

## Entidades Principales

### 1. DEPARTMENTS (Departamentos)
```sql
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    faculty VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. AUTHORS (Autores/Docentes)
```sql
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    dni VARCHAR(20) UNIQUE,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    full_name VARCHAR(500) NOT NULL,
    email VARCHAR(255),
    title VARCHAR(255), -- Título profesional (Dr., PhD, Ing., etc.)
    position VARCHAR(255), -- Cargo/puesto
    gender ENUM('M', 'F', 'Other'),
    department_id INTEGER REFERENCES departments(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. SCOPUS_ACCOUNTS (Cuentas Scopus por autor)
```sql
CREATE TABLE scopus_accounts (
    id SERIAL PRIMARY KEY,
    author_id INTEGER REFERENCES authors(id),
    scopus_id VARCHAR(50) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    last_sync TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(author_id, scopus_id)
);
```

### 4. SUBJECT_AREAS (Áreas temáticas principales)
```sql
CREATE TABLE subject_areas (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL, -- ASJC code
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. SUBJECT_SUBAREAS (Subáreas temáticas)
```sql
CREATE TABLE subject_subareas (
    id SERIAL PRIMARY KEY,
    area_id INTEGER REFERENCES subject_areas(id),
    code VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6. JOURNALS (Revistas)
```sql
CREATE TABLE journals (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    issn VARCHAR(20),
    e_issn VARCHAR(20),
    publisher VARCHAR(255),
    source_type VARCHAR(50), -- Journal, Book Series, Conference Proceeding
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 7. SJR_RANKINGS (Rankings SJR por año y revista)
```sql
CREATE TABLE sjr_rankings (
    id SERIAL PRIMARY KEY,
    journal_id INTEGER REFERENCES journals(id),
    year INTEGER NOT NULL,
    sjr_value DECIMAL(10,4),
    h_index INTEGER,
    total_docs INTEGER,
    total_cites INTEGER,
    citable_docs INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(journal_id, year)
);
```

### 8. CATEGORIES (Categorías SJR)
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 9. SJR_CATEGORIES (Categorías por ranking SJR)
```sql
CREATE TABLE sjr_categories (
    id SERIAL PRIMARY KEY,
    sjr_ranking_id INTEGER REFERENCES sjr_rankings(id),
    category_id INTEGER REFERENCES categories(id),
    quartile VARCHAR(2), -- Q1, Q2, Q3, Q4
    rank_position INTEGER,
    percentile DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(sjr_ranking_id, category_id)
);
```

### 10. PUBLICATIONS (Publicaciones)
```sql
CREATE TABLE publications (
    id SERIAL PRIMARY KEY,
    scopus_id VARCHAR(50) UNIQUE,
    title TEXT NOT NULL,
    abstract TEXT,
    publication_year INTEGER NOT NULL,
    journal_id INTEGER REFERENCES journals(id),
    doi VARCHAR(255),
    document_type VARCHAR(100), -- Article, Conference Paper, Review, etc.
    source_type VARCHAR(50), -- Scopus, WOS, Regional, Memory, Book
    affiliation TEXT,
    volume VARCHAR(50),
    issue VARCHAR(50),
    pages VARCHAR(100),
    citation_count INTEGER DEFAULT 0,
    is_open_access BOOLEAN DEFAULT FALSE,
    is_editable BOOLEAN DEFAULT TRUE,
    is_included_in_report BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 11. PUBLICATION_AUTHORS (Relación muchos a muchos)
```sql
CREATE TABLE publication_authors (
    id SERIAL PRIMARY KEY,
    publication_id INTEGER REFERENCES publications(id),
    author_id INTEGER REFERENCES authors(id),
    scopus_account_id INTEGER REFERENCES scopus_accounts(id),
    author_order INTEGER, -- Orden en la publicación
    is_corresponding BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(publication_id, author_id)
);
```

### 12. PUBLICATION_SUBJECT_AREAS (Áreas temáticas por publicación)
```sql
CREATE TABLE publication_subject_areas (
    id SERIAL PRIMARY KEY,
    publication_id INTEGER REFERENCES publications(id),
    subject_area_id INTEGER REFERENCES subject_areas(id),
    subject_subarea_id INTEGER REFERENCES subject_subareas(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(publication_id, subject_area_id, subject_subarea_id)
);
```

### 13. REPORTS (Reportes generados)
```sql
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    author_id INTEGER REFERENCES authors(id),
    report_type VARCHAR(50), -- draft, final
    title VARCHAR(500),
    memo_number VARCHAR(100),
    memo_date DATE,
    signatory VARCHAR(255), -- Persona que firma
    generated_by INTEGER REFERENCES authors(id), -- Quien genera el reporte
    file_path VARCHAR(500),
    metadata JSON, -- Configuraciones adicionales del reporte
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 14. REPORT_PUBLICATIONS (Publicaciones incluidas en cada reporte)
```sql
CREATE TABLE report_publications (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES reports(id),
    publication_id INTEGER REFERENCES publications(id),
    is_included BOOLEAN DEFAULT TRUE,
    custom_data JSON, -- Datos editados específicos para el reporte
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(report_id, publication_id)
);
```

## Índices Recomendados

```sql
-- Índices para mejorar performance
CREATE INDEX idx_authors_dni ON authors(dni);
CREATE INDEX idx_authors_department ON authors(department_id);
CREATE INDEX idx_scopus_accounts_author ON scopus_accounts(author_id);
CREATE INDEX idx_scopus_accounts_scopus_id ON scopus_accounts(scopus_id);
CREATE INDEX idx_publications_year ON publications(publication_year);
CREATE INDEX idx_publications_journal ON publications(journal_id);
CREATE INDEX idx_publications_scopus_id ON publications(scopus_id);
CREATE INDEX idx_publication_authors_publication ON publication_authors(publication_id);
CREATE INDEX idx_publication_authors_author ON publication_authors(author_id);
CREATE INDEX idx_sjr_rankings_journal_year ON sjr_rankings(journal_id, year);
```

## Características del Diseño

### Ventajas:
1. **Normalización**: Evita redundancia de datos
2. **Flexibilidad**: Permite múltiples cuentas Scopus por autor
3. **Escalabilidad**: Maneja diferentes fuentes de publicaciones
4. **Auditoría**: Timestamps en todas las tablas
5. **Configurabilidad**: Campos editables y de inclusión en reportes
6. **Integridad**: Claves foráneas y restricciones únicas

### Casos de Uso Cubiertos:
- ✅ Múltiples cuentas Scopus por autor
- ✅ Mapeo de revistas con SJR histórico
- ✅ Categorización por áreas y subáreas temáticas
- ✅ Publicaciones de múltiples fuentes
- ✅ Edición de datos para reportes
- ✅ Generación de borradores y reportes finales
- ✅ Búsqueda por base de datos vs. Scopus
- ✅ Actualización incremental de publicaciones