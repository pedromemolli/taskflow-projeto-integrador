import os
import tempfile
import unittest

from app import create_app


class TaskFlowTestCase(unittest.TestCase):
    def setUp(self):
        self.db_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_file.close()
        self.app = create_app({"TESTING": True, "DATABASE": self.db_file.name, "SECRET_KEY": "test"})
        self.client = self.app.test_client()

    def tearDown(self):
        os.unlink(self.db_file.name)

    def create_task(self, title="Estudar testes", status="Pendente"):
        return self.client.post("/tarefas/nova", data={
            "title": title, "description": "Descrição de teste", "due_date": "2026-12-31",
            "priority": "Alta", "status": status,
        }, follow_redirects=True)

    def test_create_task(self):
        response = self.create_task()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Tarefa cadastrada com sucesso", response.data)
        self.assertIn(b"Estudar testes", response.data)

    def test_rejects_short_title(self):
        response = self.create_task(title="Oi")
        self.assertIn(b"t\xc3\xadtulo precisa ter ao menos", response.data)

    def test_complete_task(self):
        self.create_task()
        response = self.client.post("/tarefas/1/concluir", follow_redirects=True)
        self.assertIn(b"Tarefa marcada como conclu", response.data)
        self.assertIn(b"Conclu\xc3\xadda", response.data)

    def test_delete_task(self):
        self.create_task()
        response = self.client.post("/tarefas/1/excluir", follow_redirects=True)
        self.assertIn(b"Tarefa exclu\xc3\xadda", response.data)
        self.assertIn(b"Nenhuma tarefa encontrada", response.data)


if __name__ == "__main__":
    unittest.main()
