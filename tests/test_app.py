import io
import json
import os
import tempfile
import unittest
from unittest.mock import patch

from app import create_app


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False


class TaskFlowTestCase(unittest.TestCase):
    def setUp(self):
        self.db_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_file.close()
        self.app = create_app(
            {
                "TESTING": True,
                "DATABASE": self.db_file.name,
                "SECRET_KEY": "test",
            }
        )
        self.client = self.app.test_client()

    def tearDown(self):
        os.unlink(self.db_file.name)

    def create_task(
        self,
        title="Estudar testes",
        description="Descrição de teste",
        due_date="2026-12-31",
        priority="Alta",
        status="Pendente",
    ):
        return self.client.post(
            "/tarefas/nova",
            data={
                "title": title,
                "description": description,
                "due_date": due_date,
                "priority": priority,
                "status": status,
            },
            follow_redirects=True,
        )

    def test_index_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"TaskFlow", response.data)
        self.assertIn(b"Filtrar tarefas", response.data)

    def test_create_task(self):
        response = self.create_task()
        self.assertEqual(response.status_code, 200)
        self.assertIn("Tarefa cadastrada com sucesso".encode(), response.data)
        self.assertIn(b"Estudar testes", response.data)

    def test_rejects_short_title_and_preserves_value(self):
        response = self.create_task(title="Oi")
        self.assertIn("título precisa ter ao menos".encode(), response.data)
        self.assertIn(b'value="Oi"', response.data)

    def test_rejects_invalid_priority(self):
        response = self.create_task(priority="Urgentíssima")
        self.assertIn("prioridade válida".encode(), response.data)

    def test_rejects_invalid_status(self):
        response = self.create_task(status="Arquivada")
        self.assertIn("situação válida".encode(), response.data)

    def test_edit_task(self):
        self.create_task()
        response = self.client.post(
            "/tarefas/1/editar",
            data={
                "title": "Tarefa atualizada",
                "description": "Nova descrição",
                "due_date": "2026-12-20",
                "priority": "Média",
                "status": "Em andamento",
            },
            follow_redirects=True,
        )
        self.assertIn("Tarefa atualizada com sucesso".encode(), response.data)
        self.assertIn(b"Tarefa atualizada", response.data)
        self.assertIn("Em andamento".encode(), response.data)

    def test_complete_task(self):
        self.create_task()
        response = self.client.post("/tarefas/1/concluir", follow_redirects=True)
        self.assertIn("Tarefa marcada como concluída".encode(), response.data)
        self.assertIn("Concluída".encode(), response.data)

    def test_delete_task(self):
        self.create_task()
        response = self.client.post("/tarefas/1/excluir", follow_redirects=True)
        self.assertIn("Tarefa excluída".encode(), response.data)
        self.assertIn("Nenhuma tarefa encontrada".encode(), response.data)

    def test_filter_by_priority(self):
        self.create_task(title="Alta prioridade", priority="Alta")
        self.create_task(title="Baixa prioridade", priority="Baixa")
        response = self.client.get("/?priority=Alta")
        self.assertIn(b"Alta prioridade", response.data)
        self.assertNotIn(b"Baixa prioridade", response.data)

    def test_filter_by_status(self):
        self.create_task(title="Pendente A", status="Pendente")
        self.create_task(title="Concluida B", status="Concluída")
        response = self.client.get("/?status=Pendente")
        self.assertIn(b"Pendente A", response.data)
        self.assertNotIn(b"Concluida B", response.data)

    def test_holiday_api_rejects_invalid_date(self):
        response = self.client.get("/api/feriado?data=invalida")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json is None)

    @patch("urllib.request.urlopen")
    def test_holiday_api_identifies_holiday(self, mocked_urlopen):
        payload = json.dumps(
            [{"date": "2026-09-07", "name": "Independência do Brasil", "type": "national"}]
        ).encode("utf-8")
        mocked_urlopen.return_value = FakeResponse(payload)
        response = self.client.get("/api/feriado?data=2026-09-07")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["is_holiday"])
        self.assertEqual(response.json["name"], "Independência do Brasil")

    @patch("urllib.request.urlopen")
    def test_holiday_api_identifies_non_holiday(self, mocked_urlopen):
        mocked_urlopen.return_value = FakeResponse(b"[]")
        response = self.client.get("/api/feriado?data=2026-09-08")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json["is_holiday"])

    def test_missing_task_returns_404(self):
        response = self.client.get("/tarefas/999/editar")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Página não encontrada".encode(), response.data)


if __name__ == "__main__":
    unittest.main()
