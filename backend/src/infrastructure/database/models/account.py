class ScopusAccountModel(Base):
    """Modelo para cuentas/IDs de Scopus de autores."""
    __tablename__ = 'scopus_accounts'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    scopus_id = Column(String(50), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

    # Relaciones
    author = relationship("AuthorModel", back_populates="scopus_accounts")


# ============================================================================
# MODELOS DE ÁREAS TEMÁTICAS
# ============================================================================

class SubjectAreaModel(Base):
    """Modelo para áreas temáticas principales."""
    __tablename__ = 'subject_areas'

    id = Column(Integer, primary_key=True)
    code = Column(String(10), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())

    # Relaciones
    categories = relationship("SubjectCategoryModel", back_populates="area")


class SubjectCategoryModel(Base):
    """Modelo para subáreas temáticas."""
    __tablename__ = 'subject_category'

    id = Column(Integer, primary_key=True)
    area_id = Column(Integer, ForeignKey('subject_areas.id'), nullable=False)
    code = Column(String(10), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())

    # Relaciones
    area = relationship("SubjectAreaModel", back_populates="categories")