import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from semiomorfologia.api.app import app
from fastapi.testclient import TestClient


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["version"], "2.0.0")

    def test_domains(self):
        r = self.client.get("/api/domains")
        self.assertEqual(r.status_code, 200)
        self.assertIn("mineral", r.json()["domains"])

    def test_extract(self):
        morphemes = [
            {"id": "grafeno", "dominio": "mineral",
             "descricao": {"elemento_base": "carbono"},
             "propriedades": {"condutividade": 0.98}},
            {"id": "diamante", "dominio": "mineral",
             "descricao": {"elemento_base": "carbono"},
             "propriedades": {"dureza": 1.0}},
            {"id": "grafite", "dominio": "mineral",
             "descricao": {"elemento_base": "carbono"},
             "propriedades": {"condutividade": 0.85}}
        ]
        r = self.client.post("/api/extract?domain=mineral", json=morphemes)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("analogies", data)
        self.assertIn("total", data)
    def test_contract(self):
        payload = {
            "m1": {"nome": "a", "propriedades": {"p": 1}, "descricao": ["x"]},
            "m2": {"nome": "b", "propriedades": {"p": 2}, "descricao": ["y"]}
        }
        r = self.client.post("/api/contract", json=payload)
        self.assertEqual(r.status_code, 200)
        self.assertIn("avaliacao_fame", r.json())

    def test_fame(self):
        r = self.client.post("/api/fame", json={"pontuacao": 0.85})
        self.assertEqual(r.status_code, 200)
        self.assertGreater(r.json()["fame"], 0)

    def test_fame_batch(self):
        r = self.client.post("/api/fame/batch", json=[0.5, 0.7, 0.9])
        self.assertEqual(r.status_code, 200)

    def test_bridges(self):
        payload = {
            "mineral": [{"id": "aerogel", "dominio": "mineral",
                         "propriedades": {"isolamento": 0.98}}],
            "vegetal": [{"id": "edelweiss", "dominio": "vegetal",
                         "propriedades": {"isolamento": 0.92}}]
        }
        r = self.client.post("/api/bridges", json=payload)
        self.assertEqual(r.status_code, 200)
        self.assertIn("bridges", r.json())

    def test_health(self):
        r = self.client.get("/api/health")
        self.assertEqual(r.status_code, 200)

if __name__ == "__main__":
    unittest.main()
