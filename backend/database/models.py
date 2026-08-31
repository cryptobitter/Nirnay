import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Float, JSON, ForeignKey, Text, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.db import Base

class Institution(Base):
    __tablename__ = "institutions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    trust_tier = Column(String(50), default="standard")
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    users = relationship("User", back_populates="institution")
    documents = relationship("Document", back_populates="institution")
    assessments = relationship("Assessment", back_populates="institution")


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("role IN ('admin', 'reviewer', 'staff')", name="check_user_role"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="staff")  # admin, reviewer, staff
    institution_id = Column(UUID(as_uuid=True), ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    institution = relationship("Institution", back_populates="users")
    assessments = relationship("Assessment", back_populates="user")


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id = Column(UUID(as_uuid=True), ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(255), nullable=False)
    upload_date = Column(DateTime(timezone=True), default=datetime.utcnow)
    page_count = Column(Integer, default=0)
    status = Column(String(50), default="processed")

    institution = relationship("Institution", back_populates="documents")


class Assessment(Base):
    __tablename__ = "assessments"
    __table_args__ = (
        CheckConstraint("decision IN ('approved', 'flagged', 'escalated')", name="check_assessment_decision"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id = Column(UUID(as_uuid=True), ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    sources = Column(JSON, default=list)
    confidence_score = Column(Float, nullable=False)
    decision = Column(String(50), nullable=False)  # approved, flagged, escalated
    record_hash = Column(String(64), nullable=False, unique=True, index=True)
    chain_tx_hash = Column(String(66), nullable=True)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)

    institution = relationship("Institution", back_populates="assessments")
    user = relationship("User", back_populates="assessments")