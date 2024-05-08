-- create an index on the table names and the score.

CREATE INDEX idx_name_first_score ON names (name(1), score);
