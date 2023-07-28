-- Generate Full Text Search Columns
UPDATE
    snomed_descriptions
SET
    fts_ts_vector = to_tsvector(term || ' ' || concept_id);

UPDATE
    icd10_codes
SET
    fts_ts_vector = to_tsvector(description || ' ' || code);

UPDATE
    icd9_codes
SET
    fts_ts_vector = to_tsvector(short_description || ' ' || code);

