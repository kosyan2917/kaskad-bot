from abc import ABC, abstractmethod

class DB(ABC):

    @abstractmethod
    def check_user(self, user: str) -> bool:
        pass

    @abstractmethod
    def get_login_data(self, user: str) -> tuple[str,str]:
        pass

    @abstractmethod
    def set_login_data(self, user: str, login: str, password: str) -> bool:
        pass

    @abstractmethod
    def update_login_data(self, user: str, login: str, password: str) -> bool:
        pass

    @abstractmethod
    def delete_login_data(self, user: str) -> bool:
        pass

    @abstractmethod
    def migrate_up(self, migrate_from: int = None, migrate_to: int = None) -> None:
        pass

    @abstractmethod
    def migrate_down(self, migrate_from: int = None, migrate_to: int = None) -> None:
        pass