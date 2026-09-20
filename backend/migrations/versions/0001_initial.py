"""Create the initial CLARIO learner and learning-loop tables."""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("provider", sa.String(32), nullable=False), sa.Column("provider_subject", sa.String(255), unique=True), sa.Column("email", sa.String(320), nullable=False, unique=True), sa.Column("display_name", sa.String(255)), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()), sa.Column("last_login_at", sa.DateTime()))
    op.create_index("ix_users_email", "users", ["email"])
    op.create_table("learner_profiles", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, unique=True), sa.Column("name", sa.String(255), nullable=False), sa.Column("age_range", sa.String(32)), sa.Column("education_level", sa.String(128)), sa.Column("domain", sa.String(255)), sa.Column("prior_learning", sa.Text()), sa.Column("xp", sa.Integer(), nullable=False, server_default="0"), sa.Column("clarity", sa.Integer(), nullable=False, server_default="0"), sa.Column("clarity_streak", sa.Integer(), nullable=False, server_default="0"), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_table("mindset_responses", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False), sa.Column("question_number", sa.Integer(), nullable=False), sa.Column("answer", sa.String(1), nullable=False), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()), sa.UniqueConstraint("user_id", "question_number"))
    op.create_index("ix_mindset_responses_user_id", "mindset_responses", ["user_id"])
    op.create_table("learning_sessions", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False), sa.Column("task", sa.Text(), nullable=False), sa.Column("goal", sa.Text(), nullable=False), sa.Column("learner_state", sa.Text(), nullable=False), sa.Column("interests", sa.Text(), nullable=False), sa.Column("status", sa.String(32), nullable=False, server_default="draft"), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_index("ix_learning_sessions_user_id", "learning_sessions", ["user_id"])
    op.create_table("roadmaps", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("session_id", sa.Integer(), sa.ForeignKey("learning_sessions.id"), nullable=False, unique=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False), sa.Column("title", sa.String(255), nullable=False), sa.Column("objective", sa.Text(), nullable=False), sa.Column("status", sa.String(32), nullable=False, server_default="active"), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_index("ix_roadmaps_session_id", "roadmaps", ["session_id"])
    op.create_index("ix_roadmaps_user_id", "roadmaps", ["user_id"])
    op.create_table("roadmap_nodes", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("roadmap_id", sa.Integer(), sa.ForeignKey("roadmaps.id"), nullable=False), sa.Column("position", sa.Integer(), nullable=False), sa.Column("concept", sa.String(255), nullable=False), sa.Column("objective", sa.Text(), nullable=False), sa.Column("activity_type", sa.String(64), nullable=False), sa.Column("difficulty", sa.String(16), nullable=False, server_default="medium"), sa.Column("estimated_minutes", sa.Integer(), nullable=False, server_default="10"), sa.Column("status", sa.String(32), nullable=False, server_default="locked"), sa.Column("is_current", sa.Boolean(), nullable=False, server_default=sa.false()), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_index("ix_roadmap_nodes_roadmap_id", "roadmap_nodes", ["roadmap_id"])
    op.create_table("learning_activities", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("node_id", sa.Integer(), sa.ForeignKey("roadmap_nodes.id"), nullable=False), sa.Column("activity_type", sa.String(64), nullable=False), sa.Column("prompt", sa.Text(), nullable=False), sa.Column("expected_response", sa.Text()), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_index("ix_learning_activities_node_id", "learning_activities", ["node_id"])
    op.create_table("activity_attempts", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("activity_id", sa.Integer(), sa.ForeignKey("learning_activities.id"), nullable=False), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False), sa.Column("response", sa.Text(), nullable=False), sa.Column("result", sa.String(32), nullable=False, server_default="submitted"), sa.Column("feedback", sa.Text()), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_index("ix_activity_attempts_activity_id", "activity_attempts", ["activity_id"])
    op.create_index("ix_activity_attempts_user_id", "activity_attempts", ["user_id"])
    op.create_table("learning_evidence", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False), sa.Column("session_id", sa.Integer(), sa.ForeignKey("learning_sessions.id"), nullable=False), sa.Column("concept", sa.String(255), nullable=False), sa.Column("evidence_type", sa.String(64), nullable=False), sa.Column("score", sa.Integer(), nullable=False), sa.Column("notes", sa.Text()), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_index("ix_learning_evidence_user_id", "learning_evidence", ["user_id"])
    op.create_index("ix_learning_evidence_session_id", "learning_evidence", ["session_id"])


def downgrade() -> None:
    for table in ["learning_evidence", "activity_attempts", "learning_activities", "roadmap_nodes", "roadmaps", "learning_sessions", "mindset_responses", "learner_profiles", "users"]:
        op.drop_table(table)

