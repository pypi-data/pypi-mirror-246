def test_apply_filter(test_df,expected_df):
    from motordecalidad.utilities import applyFilter
    mocked_filtered = {
        "FIELDS":"id",
        "VALUES":"a"
    }
    df = applyFilter(test_df,mocked_filtered)
    df.show()
    expected_df.show()
    assert df.collect() == expected_df.collect()

def test_chooseComparisonOperator(spark_session):
    from operator import gt, ge, lt, le
    from motordecalidad.utilities import chooseComparisonOparator
    firstop1, firstop2 = chooseComparisonOparator(True,True,True)
    secondop1, secondop2 = chooseComparisonOparator(True,True,False)
    assert firstop1 == lt
    assert firstop2 == gt
    assert secondop1 == ge
    assert secondop2 == le