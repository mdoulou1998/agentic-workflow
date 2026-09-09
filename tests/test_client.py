from src.llm.client import ModelClient


def test_modelclient_mock_generate_and_cost():
    client = ModelClient(provider="mock", default_model="mock", pricing_table={"mock": 0.01})
    resp = client.generate("hello world")
    assert resp["model"] == "mock"
    assert "text" in resp
    expected_cost = (resp["tokens_in"] + resp["tokens_out"]) * 0.01
    assert resp["cost"] == expected_cost


def test_allow_unknown_pricing():
    client = ModelClient(provider="mock", default_model="mock", allow_unknown_pricing=True)
    resp = client.generate("hi")
    assert resp["cost"] == 0.0
