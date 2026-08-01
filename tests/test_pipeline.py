from src.ingestion.pipeline import IngestionPipeline

def test_pipeline():
    pipeline = IngestionPipeline()
    assert pipeline is not None