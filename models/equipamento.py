"""Modelo responsável por gerenciar equipamentos da academia."""

from datetime import date

from model import Model


class Equipamento(Model):
    """Fornece operações CRUD para equipamentos."""

    STATUS_DISPONIVEL = "disponivel"
    STATUS_QUEBRADA = "quebrada"
    STATUS_NO_CONSERTO = "no_conserto"
    STATUS_VALIDOS = {
        STATUS_DISPONIVEL,
        STATUS_QUEBRADA,
        STATUS_NO_CONSERTO,
    }

    def __init__(self, connection):
        super().__init__(
            connection,
            table_name="equipamentos",
            columns=[
                "id",
                "nome",
                "valor",
                "status",
                "criado_em",
                "atualizado_em",
            ],
        )

    def _validar_status(self, status):
        if status not in self.STATUS_VALIDOS:
            raise ValueError(
                "Status inválido. Use 'disponivel', 'quebrada' ou 'no_conserto'."
            )

    def prepare_create_data(self, data):
        payload = dict(data)
        payload.setdefault("status", self.STATUS_DISPONIVEL)
        self._validar_status(payload["status"])
        payload.setdefault("criado_em", date.today())
        payload.setdefault("atualizado_em", date.today())
        return payload

    def prepare_update_data(self, data):
        payload = dict(data)
        if "status" in payload:
            self._validar_status(payload["status"])
        if payload:
            payload["atualizado_em"] = date.today()
        return payload

    def listar_disponiveis(self):
        """Retorna todos os equipamentos disponíveis."""
        query = (
            f"SELECT {', '.join(self.columns)} "
            f"FROM {self.table_name} WHERE status = ?"
        )
        self.cursor.execute(query, (self.STATUS_DISPONIVEL,))
        return self.cursor.fetchall()

    def atualizar_status(self, equipamento_id, novo_status):
        """Facilita a troca de status garantindo validação."""
        return self.update(equipamento_id, {"status": novo_status})
