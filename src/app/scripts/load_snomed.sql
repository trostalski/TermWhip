-- Generate Full Text Search Column
UPDATE snomed_descriptions
SET fts_ts_vector = to_tsvector(term || ' ' || concept_id);
