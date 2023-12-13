def test_package():
    import databricks_genai
    del databricks_genai

    from databricks_genai import finetuning
    assert finetuning
    del finetuning
