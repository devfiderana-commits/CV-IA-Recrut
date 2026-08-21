from app.services.ml_service import get_model, embed_text


def test_ai_model_is_available():
    model = get_model()
    assert model is not None

    vector = embed_text("python fastapi recruitment")
    assert vector is not None
    assert hasattr(vector, "shape") or hasattr(vector, "__len__")
