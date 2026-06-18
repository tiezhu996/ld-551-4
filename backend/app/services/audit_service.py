from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


class AuditService:
    @staticmethod
    def record(
        db: Session,
        *,
        user_id: int | None,
        action: str,
        entity: str,
        entity_id: str | None = None,
        before_data: dict | None = None,
        after_data: dict | None = None,
        ip_address: str | None = None,
    ) -> None:
        db.add(
            AuditLog(
                user_id=user_id,
                action=action,
                entity=entity,
                entity_id=entity_id,
                before_data=before_data,
                after_data=after_data,
                ip_address=ip_address,
            )
        )
