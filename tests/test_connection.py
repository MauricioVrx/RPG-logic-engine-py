import pandas as pd

def test_pandas_installation():
    """Verifica que podemos crear un DataFrame básico"""
    data = {"col1": [1, 2], "col2": [3, 4]}
    df = pd.DataFrame(data)
    assert df.shape == (2, 2)
    assert not df.empty

def test_pytest_working():
    """Prueba básica para confirmar que pytest corre"""
    assert True