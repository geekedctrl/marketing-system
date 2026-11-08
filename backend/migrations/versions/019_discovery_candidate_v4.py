"""Allow cited Parallel identity proposals as v4 discovery artifacts."""
from alembic import op

revision = "019_discovery_candidate_v4"
down_revision = "018_discovery_candidate_v3"
branch_labels = depends_on = None


def upgrade():
    op.execute("ALTER TABLE stage_artifacts DROP CONSTRAINT stage_artifacts_schema_version_check")
    op.execute("ALTER TABLE stage_artifacts ADD CONSTRAINT stage_artifacts_schema_version_check CHECK(schema_version IN (1,2,3,4))")


def downgrade():
    op.execute("DO $$ BEGIN IF EXISTS (SELECT 1 FROM stage_artifacts WHERE schema_version=4) THEN RAISE EXCEPTION 'Cannot downgrade while v4 discovery artifacts exist'; END IF; END $$")
    op.execute("ALTER TABLE stage_artifacts DROP CONSTRAINT stage_artifacts_schema_version_check")
    op.execute("ALTER TABLE stage_artifacts ADD CONSTRAINT stage_artifacts_schema_version_check CHECK(schema_version IN (1,2,3))")
