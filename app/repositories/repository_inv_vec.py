# # app/repositories/vector_repository.py
# import logging
# from typing import Optional
# from sqlmodel import Session
# from app.models.rls.m_invoice_rls import InvoiceDB
# from app.models.rag.m_inv_vec import InvVecDB

# logger = logging.getLogger(__name__)


# class VectorRepository:

#     def _build_invoice_content(self, invoice: InvoiceDB) -> str:
#         """
#         Convert InvoiceDB into stable plain-text for embedding.
#         """
#         data = invoice.model_dump(
#             exclude={
#                 "id",
#                 "tenant_id",
#                 "created_at",
#                 "updated_at",
#                 "deleted_at",
#             },
#             exclude_none=True,
#         )

#         lines = []
#         for key, value in data.items():
#             label = key.replace("_", " ").title()
#             lines.append(f"{label}: {value}")

#         return "\n".join(lines)

#     def save_invoice_vector(
#         self,
#         invoice: InvoiceDB,
#         session: Session,
#         content: Optional[str] = None
#     ) -> InvVecDB:
#         """
#         Save invoice projection for embedding.
#         """
#         final_content = content or self._build_invoice_content(invoice)

#         vec_entry = InvVecDB(
#             invoice_id=invoice.id,
#             tenant_id=invoice.tenant_id,
#             content=final_content
#         )

#         session.add(vec_entry)
#         session.commit()
#         session.refresh(vec_entry)

#         logger.info(
#             f"Vector entry saved for invoice {invoice.id}, vector_id={vec_entry.id}"
#         )
#         return vec_entry




# app/repositories/vector_repository.py
import logging
from typing import Optional
from sqlmodel import Session
from app.models.rls.m_invoice_rls import InvoiceDB
from app.models.rag.m_inv_vec import InvVecDB

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class VectorRepository:
    def save_invoice_vector(
        self,
        invoice: InvoiceDB,
        session: Session,
        content: Optional[str] = None
    ) -> InvVecDB:
        """
        Save vector / fallback text for an invoice.
        Auto-handles id, tenant_id, and other defaults.
        """
        vec_entry = InvVecDB(
            invoice_id=invoice.id,
            tenant_id=invoice.tenant_id,
            content=content or invoice.description
        )
        session.add(vec_entry)
        session.commit()
        session.refresh(vec_entry)

        logger.info(
            f"Vector entry saved for invoice {invoice.id}, vector_id={vec_entry.id}"
        )
        return vec_entry
