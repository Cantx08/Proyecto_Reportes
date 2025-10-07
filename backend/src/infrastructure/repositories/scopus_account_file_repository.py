import pandas as pd
from typing import List, Optional
from pathlib import Path
from ...domain.entities.scopus_account import ScopusAccount
from ...domain.repositories.scopus_account_repository import ScopusAccountRepository


class ScopusAccountFileRepository(ScopusAccountRepository):
    """Implementación del repositorio de cuentas Scopus usando archivos CSV."""
    
    def __init__(self, csv_path: str = None):
        # Buscar archivo de cuentas Scopus existente
        base_path = Path(__file__).parent.parent.parent / "data"
        possible_files = ["dni_authorId_epn.xlsx", "scopus_accounts.csv", "author_scopus.csv"]
        
        if csv_path:
            self.csv_path = csv_path
        else:
            # Buscar el primer archivo que exista
            self.csv_path = None
            for filename in possible_files:
                if (base_path / filename).exists():
                    self.csv_path = str(base_path / filename)
                    break
            
            # Si no existe ninguno, usar un CSV por defecto
            if not self.csv_path:
                self.csv_path = str(base_path / "scopus_accounts.csv")
        
        self._accounts_cache = {}
        # No cargar automáticamente - las cuentas se inyectarán manualmente
        # self._load_accounts()
    
    def _load_accounts(self):
        """Carga las cuentas Scopus desde el archivo."""
        try:
            if Path(self.csv_path).exists():
                # Manejar tanto Excel como CSV
                if self.csv_path.endswith('.xlsx'):
                    df = pd.read_excel(self.csv_path)
                else:
                    df = pd.read_csv(self.csv_path, sep=';')
                
                self._accounts_cache = {}
                
                for _, row in df.iterrows():
                    # Mapeo flexible de columnas
                    scopus_id = str(row.get('SCOPUS_ID', row.get('scopus_id', row.get('AuthorID', ''))))
                    author_id = str(row.get('AUTHOR_ID', row.get('author_id', row.get('DNI', ''))))
                    scopus_user = str(row.get('SCOPUS_USER', row.get('scopus_user', f'user_{scopus_id}')))
                    
                    if scopus_id and author_id:  # Solo crear si tiene datos válidos
                        account = ScopusAccount(
                            scopus_id=scopus_id,
                            scopus_user=scopus_user,
                            author_id=author_id
                        )
                        self._accounts_cache[account.scopus_id] = account
        except Exception as e:
            print(f"Error loading Scopus accounts: {e}")
            self._accounts_cache = {}
    
    def load_accounts_from_file(self):
        """Método público para cargar cuentas desde archivo cuando sea necesario."""
        self._load_accounts()
    
    def _save_accounts(self):
        """Guarda las cuentas Scopus al archivo CSV."""
        try:
            data = []
            for account in self._accounts_cache.values():
                data.append({
                    'scopus_id': account.scopus_id,
                    'scopus_user': account.scopus_user,
                    'author_id': account.author_id
                })
            
            df = pd.DataFrame(data)
            
            # Guardar como CSV independientemente del formato original
            csv_path = self.csv_path
            if csv_path.endswith('.xlsx'):
                csv_path = csv_path.replace('.xlsx', '.csv')
            
            df.to_csv(csv_path, sep=';', index=False)
        except Exception as e:
            print(f"Error saving Scopus accounts to CSV: {e}")
    
    async def get_by_scopus_id(self, scopus_id: str) -> Optional[ScopusAccount]:
        """Obtiene una cuenta Scopus por su ID de Scopus."""
        return self._accounts_cache.get(scopus_id)
    
    async def get_by_author_id(self, author_id: str) -> List[ScopusAccount]:
        """Obtiene todas las cuentas Scopus de un autor."""
        return [account for account in self._accounts_cache.values() 
                if account.author_id == author_id]
    
    async def get_all(self) -> List[ScopusAccount]:
        """Obtiene todas las cuentas Scopus."""
        return list(self._accounts_cache.values())
    
    async def create(self, scopus_account: ScopusAccount) -> ScopusAccount:
        """Crea una nueva cuenta Scopus."""
        if scopus_account.scopus_id in self._accounts_cache:
            raise ValueError(f"Scopus account with ID {scopus_account.scopus_id} already exists")
        
        self._accounts_cache[scopus_account.scopus_id] = scopus_account
        self._save_accounts()
        return scopus_account
    
    async def update(self, scopus_account: ScopusAccount) -> ScopusAccount:
        """Actualiza una cuenta Scopus existente."""
        if scopus_account.scopus_id not in self._accounts_cache:
            raise ValueError(f"Scopus account with ID {scopus_account.scopus_id} not found")
        
        self._accounts_cache[scopus_account.scopus_id] = scopus_account
        self._save_accounts()
        return scopus_account
    
    async def delete(self, scopus_id: str) -> bool:
        """Elimina una cuenta Scopus por su ID de Scopus."""
        if scopus_id in self._accounts_cache:
            del self._accounts_cache[scopus_id]
            self._save_accounts()
            return True
        return False
    
    async def delete_by_author_id(self, author_id: str) -> bool:
        """Elimina todas las cuentas Scopus de un autor."""
        accounts_to_delete = [scopus_id for scopus_id, account in self._accounts_cache.items() 
                             if account.author_id == author_id]
        
        if accounts_to_delete:
            for scopus_id in accounts_to_delete:
                del self._accounts_cache[scopus_id]
            self._save_accounts()
            return True
        return False