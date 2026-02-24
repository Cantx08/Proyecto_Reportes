/**
 * Cliente directo para la API de Scopus (Elsevier).
 *
 * IMPORTANTE: Estas llamadas se realizan desde el navegador del usuario,
 * lo que garantiza que se use la IP institucional de la universidad (lista
 * blanca de Elsevier) en lugar de la IP del servidor de despliegue.
 *
 * Requiere la variable de entorno: NEXT_PUBLIC_SCOPUS_API_KEY
 */

// -----------------------------------------------------------------------
// Tipos heredados mantenidos para no romper importaciones existentes
// -----------------------------------------------------------------------

export interface ReportRequest {
  author_ids: string[];
  docente_nombre: string;
  docente_genero: string;
  departamento: string;
  cargo: string;
  memorando?: string;
  firmante?: number | string;
  firmante_nombre?: string;
  fecha?: string;
  elaborador?: string;
}

// -----------------------------------------------------------------------
// Tipos para las respuestas crudas de Scopus
// -----------------------------------------------------------------------

/** Entrada cruda tal como la devuelve Scopus Search API (view=COMPLETE). */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type RawScopusEntry = Record<string, any>;

/** Objeto de área temática devuelto por Scopus Author Retrieval API. */
export interface RawScopusSubjectArea {
  "@abbrev": string;
  $: string;
  "@frequency"?: string;
}

// -----------------------------------------------------------------------
// Mapeo de abreviaturas Scopus → nombres completos de áreas temáticas
// Refleja backend/src/modules/publications/domain/subject_area_mapping.py
// -----------------------------------------------------------------------

const SUBJECT_AREA_MAP: Record<string, string> = {
  AGRI: "Agricultural and Biological Sciences",
  ARTS: "Arts and Humanities",
  BIOC: "Biochemistry, Genetics and Molecular Biology",
  BUSI: "Business, Management and Accounting",
  CENG: "Chemical Engineering",
  CHEM: "Chemistry",
  COMP: "Computer Science",
  DECI: "Decision Sciences",
  EART: "Earth and Planetary Sciences",
  ECON: "Economics, Econometrics and Finance",
  ENER: "Energy",
  ENGI: "Engineering",
  ENVI: "Environmental Science",
  IMMU: "Immunology and Microbiology",
  MATE: "Materials Science",
  MATH: "Mathematics",
  MEDI: "Medicine",
  NEUR: "Neuroscience",
  NURS: "Nursing",
  PHAR: "Pharmacology, Toxicology and Pharmaceutics",
  PHYS: "Physics and Astronomy",
  PSYC: "Psychology",
  SOCI: "Social Sciences",
  VETE: "Veterinary",
  DENT: "Dentistry",
  HEAL: "Health Professions",
  MULT: "Multidisciplinary",
};

/** Resuelve una abreviatura Scopus al nombre completo del área temática. */
export function resolveSubjectAreaAbbrev(abbrev: string): string | null {
  return SUBJECT_AREA_MAP[abbrev.toUpperCase().trim()] ?? null;
}

// -----------------------------------------------------------------------
// Helpers internos
// -----------------------------------------------------------------------

const SCOPUS_API_BASE = "https://api.elsevier.com";
const PAGE_SIZE = 25;

// -----------------------------------------------------------------------
// Funciones públicas del cliente Scopus
// -----------------------------------------------------------------------

/**
 * Obtiene TODAS las publicaciones de un Scopus ID usando paginación.
 *
 * Usa `view=COMPLETE` para que el backend pueda calcular correctamente
 * la afiliación institucional (campo `afid` por autor).
 */
export async function fetchPublicationsByScopusId(
  scopusId: string,
  apiKey: string,
): Promise<RawScopusEntry[]> {
  const allEntries: RawScopusEntry[] = [];
  let start = 0;
  let totalResults = Infinity;

  while (start < totalResults) {
    const url =
      `${SCOPUS_API_BASE}/content/search/scopus` +
      `?query=AU-ID(${scopusId})` +
      `&view=COMPLETE` +
      `&count=${PAGE_SIZE}` +
      `&start=${start}`;

    const response = await fetch(url, {
      headers: {
        "X-ELS-APIKey": apiKey,
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(
        `Scopus Search API con código de respuesta ${response.status} para AU-ID(${scopusId})`,
      );
    }

    const data = await response.json();
    const results = data["search-results"];
    if (!results) break;

    const reported = parseInt(results["opensearch:totalResults"] ?? "0", 10);
    if (start === 0) {
      totalResults = isNaN(reported) ? 0 : reported;
    }

    const entries: RawScopusEntry[] = results.entry ?? [];
    if (entries.length === 0) break;

    allEntries.push(...entries);
    start += PAGE_SIZE;
  }

  return allEntries;
}

/**
 * Obtiene las áreas temáticas de un autor desde Author Retrieval API
 * y resuelve las abreviaturas a nombres completos.
 */
export async function fetchAuthorSubjectAreas(
  scopusId: string,
  apiKey: string,
): Promise<string[]> {
  const url = `${SCOPUS_API_BASE}/content/author/author_id/${scopusId}?view=ENHANCED`;

  const response = await fetch(url, {
    headers: {
      "X-ELS-APIKey": apiKey,
      Accept: "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(
      `Scopus Author Retrieval con código de respuesta ${response.status} para author_id=${scopusId}`,
    );
  }

  const data = await response.json();
  const retrieval = data["author-retrieval-response"];
  const item = Array.isArray(retrieval) ? retrieval[0] : retrieval;
  if (!item) return [];

  const rawAreas = item["subject-areas"]?.["subject-area"] ?? [];
  const areaList: RawScopusSubjectArea[] = Array.isArray(rawAreas)
    ? rawAreas
    : [rawAreas];

  const resolved: string[] = [];
  for (const sa of areaList) {
    const abbrev = sa["@abbrev"]?.trim();
    if (abbrev) {
      const full = resolveSubjectAreaAbbrev(abbrev);
      if (full) resolved.push(full);
    }
  }

  return [...new Set(resolved)].sort();
}