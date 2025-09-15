-- =========================================================================
-- SCRIPT DE CREACIÓN DE BASE DE DATOS
-- Sistema de Reportes de Publicaciones Académicas
-- PostgreSQL 13+
-- 
-- Autor: Sistema de Reportes Académicos
-- Fecha: Septiembre 2025
-- Versión: 1.0
-- =========================================================================

-- Configuración inicial
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Crear tipos ENUM
CREATE TYPE gender_type AS ENUM ('M', 'F', 'Other');
CREATE TYPE source_type AS ENUM ('Scopus', 'WOS', 'Regional', 'Memory', 'Book');
CREATE TYPE document_type AS ENUM ('Article', 'Conference Paper', 'Review', 'Book Chapter', 'Book', 'Editorial', 'Note', 'Letter');
CREATE TYPE quartile_type AS ENUM ('Q1', 'Q2', 'Q3', 'Q4', 'NR');
CREATE TYPE report_type AS ENUM ('draft', 'final');

-- =========================================================================
-- TABLAS PRINCIPALES
-- =========================================================================

-- 1. DEPARTMENTS (Departamentos)
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    faculty VARCHAR(255),
    code VARCHAR(20) UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. AUTHORS (Autores/Docentes)
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    dni VARCHAR(20) UNIQUE,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    full_name VARCHAR(500) GENERATED ALWAYS AS (
        CASE 
            WHEN title IS NOT NULL THEN CONCAT(title, ' ', first_name, ' ', last_name)
            ELSE CONCAT(first_name, ' ', last_name)
        END
    ) STORED,
    email VARCHAR(255) UNIQUE,
    title VARCHAR(255), -- Dr., PhD, Ing., etc.
    position VARCHAR(255), -- Cargo/puesto
    gender gender_type,
    birth_date DATE,
    department_id INTEGER REFERENCES departments(id) ON DELETE SET NULL,
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. SCOPUS_ACCOUNTS (Cuentas Scopus por autor)
CREATE TABLE scopus_accounts (
    id SERIAL PRIMARY KEY,
    author_id INTEGER NOT NULL REFERENCES authors(id) ON DELETE CASCADE,
    scopus_id VARCHAR(50) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    last_sync TIMESTAMP,
    publication_count INTEGER DEFAULT 0,
    citation_count INTEGER DEFAULT 0,
    h_index INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(author_id, scopus_id)
);

-- 4. SUBJECT_AREAS (Áreas temáticas principales)
CREATE TABLE subject_areas (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL, -- ASJC code
    name VARCHAR(255) NOT NULL,
    description TEXT,
    parent_area_id INTEGER REFERENCES subject_areas(id),
    level INTEGER DEFAULT 0, -- 0: área principal, 1: subárea
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. SUBJECT_SUBAREAS (Subáreas temáticas)
CREATE TABLE subject_subareas (
    id SERIAL PRIMARY KEY,
    area_id INTEGER NOT NULL REFERENCES subject_areas(id) ON DELETE CASCADE,
    code VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. JOURNALS (Revistas)
CREATE TABLE journals (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    issn VARCHAR(20),
    e_issn VARCHAR(20),
    publisher VARCHAR(255),
    source_type source_type DEFAULT 'Scopus',
    country VARCHAR(100),
    language VARCHAR(50) DEFAULT 'English',
    is_active BOOLEAN DEFAULT TRUE,
    scopus_source_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. SJR_RANKINGS (Rankings SJR por año y revista)
CREATE TABLE sjr_rankings (
    id SERIAL PRIMARY KEY,
    journal_id INTEGER NOT NULL REFERENCES journals(id) ON DELETE CASCADE,
    year INTEGER NOT NULL,
    sjr_value DECIMAL(10,4),
    h_index INTEGER,
    total_docs INTEGER,
    total_cites INTEGER,
    citable_docs INTEGER,
    refs_per_doc DECIMAL(8,2),
    country VARCHAR(100),
    region VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(journal_id, year)
);

-- 8. CATEGORIES (Categorías SJR)
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    asjc_code VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. SJR_CATEGORIES (Categorías por ranking SJR)
CREATE TABLE sjr_categories (
    id SERIAL PRIMARY KEY,
    sjr_ranking_id INTEGER NOT NULL REFERENCES sjr_rankings(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    quartile quartile_type DEFAULT 'NR',
    rank_position INTEGER,
    total_journals INTEGER,
    percentile DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(sjr_ranking_id, category_id)
);

-- 10. PUBLICATIONS (Publicaciones)
CREATE TABLE publications (
    id SERIAL PRIMARY KEY,
    scopus_id VARCHAR(50) UNIQUE,
    title TEXT NOT NULL,
    abstract TEXT,
    publication_year INTEGER NOT NULL,
    journal_id INTEGER REFERENCES journals(id) ON DELETE SET NULL,
    doi VARCHAR(255),
    document_type document_type DEFAULT 'Article',
    source_type source_type DEFAULT 'Scopus',
    affiliation TEXT,
    volume VARCHAR(50),
    issue VARCHAR(50),
    pages VARCHAR(100),
    page_start VARCHAR(20),
    page_end VARCHAR(20),
    citation_count INTEGER DEFAULT 0,
    is_open_access BOOLEAN DEFAULT FALSE,
    is_editable BOOLEAN DEFAULT TRUE,
    is_included_in_report BOOLEAN DEFAULT TRUE,
    keywords TEXT[],
    funding_text TEXT,
    notes TEXT,
    external_url VARCHAR(500),
    pdf_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_year CHECK (publication_year >= 1900 AND publication_year <= EXTRACT(YEAR FROM CURRENT_DATE) + 1),
    CONSTRAINT valid_citation_count CHECK (citation_count >= 0)
);

-- 11. PUBLICATION_AUTHORS (Relación muchos a muchos)
CREATE TABLE publication_authors (
    id SERIAL PRIMARY KEY,
    publication_id INTEGER NOT NULL REFERENCES publications(id) ON DELETE CASCADE,
    author_id INTEGER NOT NULL REFERENCES authors(id) ON DELETE CASCADE,
    scopus_account_id INTEGER REFERENCES scopus_accounts(id) ON DELETE SET NULL,
    author_order INTEGER NOT NULL DEFAULT 1,
    is_corresponding BOOLEAN DEFAULT FALSE,
    affiliation_at_time TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(publication_id, author_id),
    CONSTRAINT positive_author_order CHECK (author_order > 0)
);

-- 12. PUBLICATION_SUBJECT_AREAS (Áreas temáticas por publicación)
CREATE TABLE publication_subject_areas (
    id SERIAL PRIMARY KEY,
    publication_id INTEGER NOT NULL REFERENCES publications(id) ON DELETE CASCADE,
    subject_area_id INTEGER NOT NULL REFERENCES subject_areas(id) ON DELETE CASCADE,
    subject_subarea_id INTEGER REFERENCES subject_subareas(id) ON DELETE SET NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(publication_id, subject_area_id, subject_subarea_id)
);

-- 13. REPORTS (Reportes generados)
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    author_id INTEGER NOT NULL REFERENCES authors(id) ON DELETE CASCADE,
    report_type report_type DEFAULT 'draft',
    title VARCHAR(500),
    memo_number VARCHAR(100),
    memo_date DATE DEFAULT CURRENT_DATE,
    signatory VARCHAR(255),
    generated_by INTEGER REFERENCES authors(id) ON DELETE SET NULL,
    file_path VARCHAR(500),
    file_size INTEGER,
    file_hash VARCHAR(64),
    metadata JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 14. REPORT_PUBLICATIONS (Publicaciones incluidas en cada reporte)
CREATE TABLE report_publications (
    id SERIAL PRIMARY KEY,
    report_id INTEGER NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
    publication_id INTEGER NOT NULL REFERENCES publications(id) ON DELETE CASCADE,
    include_in_report BOOLEAN DEFAULT TRUE,
    order_in_report INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(report_id, publication_id)
);

-- =========================================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- =========================================================================

-- Índices para authors
CREATE INDEX idx_authors_dni ON authors(dni) WHERE dni IS NOT NULL;
CREATE INDEX idx_authors_email ON authors(email) WHERE email IS NOT NULL;
CREATE INDEX idx_authors_department ON authors(department_id);
CREATE INDEX idx_authors_full_name ON authors(full_name);
CREATE INDEX idx_authors_name_search ON authors USING gin(
    (first_name || ' ' || last_name) gin_trgm_ops
);

-- Índices para scopus_accounts
CREATE INDEX idx_scopus_accounts_author ON scopus_accounts(author_id);
CREATE INDEX idx_scopus_accounts_scopus_id ON scopus_accounts(scopus_id);
CREATE INDEX idx_scopus_accounts_primary ON scopus_accounts(author_id, is_primary) WHERE is_primary = TRUE;

-- Índices para publications
CREATE INDEX idx_publications_year ON publications(publication_year);
CREATE INDEX idx_publications_journal ON publications(journal_id);
CREATE INDEX idx_publications_scopus_id ON publications(scopus_id) WHERE scopus_id IS NOT NULL;
CREATE INDEX idx_publications_doi ON publications(doi) WHERE doi IS NOT NULL;
CREATE INDEX idx_publications_title_search ON publications USING gin(title gin_trgm_ops);
CREATE INDEX idx_publications_document_type ON publications(document_type);
CREATE INDEX idx_publications_source_type ON publications(source_type);
CREATE INDEX idx_publications_report_eligible ON publications(is_included_in_report) WHERE is_included_in_report = TRUE;

-- Índices para publication_authors
CREATE INDEX idx_publication_authors_publication ON publication_authors(publication_id);
CREATE INDEX idx_publication_authors_author ON publication_authors(author_id);
CREATE INDEX idx_publication_authors_order ON publication_authors(publication_id, author_order);

-- Índices para journals
CREATE INDEX idx_journals_title_search ON journals USING gin(title gin_trgm_ops);
CREATE INDEX idx_journals_issn ON journals(issn) WHERE issn IS NOT NULL;
CREATE INDEX idx_journals_e_issn ON journals(e_issn) WHERE e_issn IS NOT NULL;

-- Índices para sjr_rankings
CREATE INDEX idx_sjr_rankings_journal_year ON sjr_rankings(journal_id, year);
CREATE INDEX idx_sjr_rankings_year ON sjr_rankings(year);
CREATE INDEX idx_sjr_rankings_sjr_value ON sjr_rankings(sjr_value) WHERE sjr_value IS NOT NULL;

-- Índices para subject areas
CREATE INDEX idx_subject_areas_code ON subject_areas(code);
CREATE INDEX idx_subject_subareas_area ON subject_subareas(area_id);

-- Índices para reports
CREATE INDEX idx_reports_author ON reports(author_id);
CREATE INDEX idx_reports_type ON reports(report_type);
CREATE INDEX idx_reports_date ON reports(memo_date);

-- =========================================================================
-- FUNCIONES Y TRIGGERS
-- =========================================================================

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para updated_at
CREATE TRIGGER update_authors_updated_at BEFORE UPDATE ON authors
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_scopus_accounts_updated_at BEFORE UPDATE ON scopus_accounts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_journals_updated_at BEFORE UPDATE ON journals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_publications_updated_at BEFORE UPDATE ON publications
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Función para asegurar solo una cuenta Scopus primaria por autor
CREATE OR REPLACE FUNCTION ensure_single_primary_scopus_account()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_primary = TRUE THEN
        UPDATE scopus_accounts 
        SET is_primary = FALSE 
        WHERE author_id = NEW.author_id AND id != NEW.id;
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER trigger_single_primary_scopus_account 
    BEFORE INSERT OR UPDATE ON scopus_accounts
    FOR EACH ROW EXECUTE FUNCTION ensure_single_primary_scopus_account();

-- Función para actualizar contadores en scopus_accounts
CREATE OR REPLACE FUNCTION update_scopus_account_stats()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        UPDATE scopus_accounts sa
        SET 
            publication_count = (
                SELECT COUNT(*)
                FROM publication_authors pa
                JOIN publications p ON p.id = pa.publication_id
                WHERE pa.scopus_account_id = sa.id
            ),
            citation_count = COALESCE((
                SELECT SUM(p.citation_count)
                FROM publication_authors pa
                JOIN publications p ON p.id = pa.publication_id
                WHERE pa.scopus_account_id = sa.id
            ), 0)
        WHERE sa.id = COALESCE(NEW.scopus_account_id, OLD.scopus_account_id);
        
        RETURN COALESCE(NEW, OLD);
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE scopus_accounts sa
        SET 
            publication_count = (
                SELECT COUNT(*)
                FROM publication_authors pa
                WHERE pa.scopus_account_id = sa.id
            ),
            citation_count = COALESCE((
                SELECT SUM(p.citation_count)
                FROM publication_authors pa
                JOIN publications p ON p.id = pa.publication_id
                WHERE pa.scopus_account_id = sa.id
            ), 0)
        WHERE sa.id = OLD.scopus_account_id;
        
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ language 'plpgsql';

CREATE TRIGGER trigger_update_scopus_account_stats
    AFTER INSERT OR UPDATE OR DELETE ON publication_authors
    FOR EACH ROW EXECUTE FUNCTION update_scopus_account_stats();

-- =========================================================================
-- DATOS INICIALES
-- =========================================================================

-- Insertar departamentos básicos
INSERT INTO departments (name, faculty, code, description) VALUES
('Sistemas e Informática', 'Facultad de Ingeniería', 'DISI', 'Departamento de Sistemas e Informática'),
('Ciencias Exactas', 'Facultad de Ciencias', 'DCE', 'Departamento de Ciencias Exactas'),
('Ingeniería Mecánica', 'Facultad de Ingeniería', 'DIMEC', 'Departamento de Ingeniería Mecánica'),
('Ingeniería Civil', 'Facultad de Ingeniería', 'DICIV', 'Departamento de Ingeniería Civil'),
('Química', 'Facultad de Ciencias', 'DQ', 'Departamento de Química'),
('Biología', 'Facultad de Ciencias', 'DB', 'Departamento de Biología'),
('Física', 'Facultad de Ciencias', 'DF', 'Departamento de Física'),
('Matemáticas', 'Facultad de Ciencias', 'DM', 'Departamento de Matemáticas');

-- Insertar áreas temáticas principales (ASJC codes)
INSERT INTO subject_areas (code, name, description, level) VALUES
('1000', 'General', 'General subject area', 0),
('1100', 'Agricultural and Biological Sciences', 'Agricultural and Biological Sciences', 0),
('1200', 'Arts and Humanities', 'Arts and Humanities', 0),
('1300', 'Biochemistry, Genetics and Molecular Biology', 'Biochemistry, Genetics and Molecular Biology', 0),
('1400', 'Business, Management and Accounting', 'Business, Management and Accounting', 0),
('1500', 'Chemical Engineering', 'Chemical Engineering', 0),
('1600', 'Chemistry', 'Chemistry', 0),
('1700', 'Computer Science', 'Computer Science', 0),
('1800', 'Decision Sciences', 'Decision Sciences', 0),
('1900', 'Earth and Planetary Sciences', 'Earth and Planetary Sciences', 0),
('2000', 'Economics, Econometrics and Finance', 'Economics, Econometrics and Finance', 0),
('2100', 'Energy', 'Energy', 0),
('2200', 'Engineering', 'Engineering', 0),
('2300', 'Environmental Science', 'Environmental Science', 0),
('2400', 'Immunology and Microbiology', 'Immunology and Microbiology', 0),
('2500', 'Materials Science', 'Materials Science', 0),
('2600', 'Mathematics', 'Mathematics', 0),
('2700', 'Medicine', 'Medicine', 0),
('2800', 'Neuroscience', 'Neuroscience', 0),
('2900', 'Nursing', 'Nursing', 0),
('3000', 'Pharmacology, Toxicology and Pharmaceutics', 'Pharmacology, Toxicology and Pharmaceutics', 0),
('3100', 'Physics and Astronomy', 'Physics and Astronomy', 0),
('3200', 'Psychology', 'Psychology', 0),
('3300', 'Social Sciences', 'Social Sciences', 0),
('3400', 'Veterinary', 'Veterinary', 0),
('3500', 'Dentistry', 'Dentistry', 0),
('3600', 'Health Professions', 'Health Professions', 0);

-- Insertar categorías básicas
INSERT INTO categories (name, description, asjc_code) VALUES
('Computer Science Applications', 'Computer Science Applications', '1706'),
('Software', 'Software', '1712'),
('Information Systems', 'Information Systems', '1710'),
('Artificial Intelligence', 'Artificial Intelligence', '1702'),
('Machine Learning', 'Machine Learning', '1702'),
('Data Science', 'Data Science', '1706'),
('Engineering Applications', 'Engineering Applications', '2200'),
('Materials Science General', 'Materials Science General', '2500'),
('Physics General', 'Physics General', '3100'),
('Mathematics General', 'Mathematics General', '2600');

-- =========================================================================
-- VISTAS ÚTILES
-- =========================================================================

-- Vista para autores con información completa
CREATE VIEW v_authors_complete AS
SELECT 
    a.id,
    a.dni,
    a.first_name,
    a.last_name,
    a.full_name,
    a.email,
    a.title,
    a.position,
    a.gender,
    d.name as department_name,
    d.faculty,
    COUNT(DISTINCT sa.id) as scopus_accounts_count,
    COUNT(DISTINCT pa.publication_id) as publications_count,
    COALESCE(SUM(p.citation_count), 0) as total_citations,
    a.is_active,
    a.created_at,
    a.updated_at
FROM authors a
LEFT JOIN departments d ON a.department_id = d.id
LEFT JOIN scopus_accounts sa ON a.id = sa.author_id AND sa.is_active = TRUE
LEFT JOIN publication_authors pa ON a.id = pa.author_id
LEFT JOIN publications p ON pa.publication_id = p.id
GROUP BY a.id, d.name, d.faculty;

-- Vista para publicaciones con información completa
CREATE VIEW v_publications_complete AS
SELECT 
    p.id,
    p.scopus_id,
    p.title,
    p.publication_year,
    j.title as journal_title,
    j.issn,
    j.e_issn,
    p.doi,
    p.document_type,
    p.source_type,
    p.citation_count,
    p.is_open_access,
    COUNT(DISTINCT pa.author_id) as author_count,
    STRING_AGG(DISTINCT CONCAT(a.first_name, ' ', a.last_name), '; ' ORDER BY pa.author_order) as authors,
    COUNT(DISTINCT psa.subject_area_id) as subject_area_count,
    p.is_included_in_report,
    p.created_at,
    p.updated_at
FROM publications p
LEFT JOIN journals j ON p.journal_id = j.id
LEFT JOIN publication_authors pa ON p.id = pa.publication_id
LEFT JOIN authors a ON pa.author_id = a.id
LEFT JOIN publication_subject_areas psa ON p.id = psa.publication_id
GROUP BY p.id, j.title, j.issn, j.e_issn;

-- Vista para rankings SJR con información de journal
CREATE VIEW v_sjr_rankings_complete AS
SELECT 
    sr.id,
    j.title as journal_title,
    j.issn,
    j.e_issn,
    sr.year,
    sr.sjr_value,
    sr.h_index,
    sr.total_docs,
    sr.total_cites,
    STRING_AGG(DISTINCT c.name, '; ') as categories,
    STRING_AGG(DISTINCT sc.quartile::text, '; ') as quartiles
FROM sjr_rankings sr
JOIN journals j ON sr.journal_id = j.id
LEFT JOIN sjr_categories sc ON sr.id = sc.sjr_ranking_id
LEFT JOIN categories c ON sc.category_id = c.id
GROUP BY sr.id, j.title, j.issn, j.e_issn, sr.year, sr.sjr_value, sr.h_index, sr.total_docs, sr.total_cites;

-- =========================================================================
-- PERMISOS Y USUARIOS (Opcional - Configurar según necesidades)
-- =========================================================================

-- Crear usuario para la aplicación (descomentar si es necesario)
-- CREATE USER reportes_app WITH PASSWORD 'secure_password_here';
-- GRANT CONNECT ON DATABASE reportes_academicos TO reportes_app;
-- GRANT USAGE ON SCHEMA public TO reportes_app;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO reportes_app;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO reportes_app;

-- =========================================================================
-- COMENTARIOS FINALES
-- =========================================================================

COMMENT ON DATABASE reportes_academicos IS 'Base de datos para Sistema de Reportes de Publicaciones Académicas';

-- Comentarios en tablas principales
COMMENT ON TABLE authors IS 'Autores/Docentes del sistema académico';
COMMENT ON TABLE publications IS 'Publicaciones académicas de autores';
COMMENT ON TABLE journals IS 'Revistas científicas donde se publican los artículos';
COMMENT ON TABLE reports IS 'Reportes generados para autores';
COMMENT ON TABLE scopus_accounts IS 'Cuentas de Scopus asociadas a cada autor';

-- Mostrar resumen de la instalación
SELECT 
    'Database created successfully!' as status,
    COUNT(*) as total_tables
FROM information_schema.tables 
WHERE table_schema = 'public' AND table_type = 'BASE TABLE';

-- Fin del script