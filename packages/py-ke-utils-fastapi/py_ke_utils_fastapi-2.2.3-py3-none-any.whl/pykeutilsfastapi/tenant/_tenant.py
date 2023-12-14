from fastapi import  Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from pykeutilsfastapi.tenant import tenant_extractor

security = HTTPBearer()

class TenantName:
    """
    Dependency class for FastAPI. It returns the full tenant name.
    :param default_tenant: Default tenant.
    """

    def __init__(
            self,
            default_tenant: str = 'public',
    ):
        self.default_tenant = default_tenant

    def __call__(
            self,
            token: HTTPAuthorizationCredentials = Depends(security)
    ) -> str:
        return f"tenant_{tenant_extractor(token.credentials, self.default_tenant)}"