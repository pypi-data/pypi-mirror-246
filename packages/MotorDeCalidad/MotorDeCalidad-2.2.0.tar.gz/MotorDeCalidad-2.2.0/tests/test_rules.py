def test_requisites(test_df):
    from motordecalidad.rules import validateRequisites
    data = validateRequisites(test_df,["id","value","date"])
    assert data[-1] == 0

def test_null(test_df):
    from motordecalidad.rules import validateNull
    data,errorDf = validateNull(test_df,"id",3,"TEST","100")
    assert data[-1] == 0

def test_duplicates(test_df):
    from motordecalidad.rules import validateDuplicates

    data,errorDf = validateDuplicates(test_df,["id"],3,"TEST","100")
    assert data[-1] == 0

def test_integrity(test_df):
    from motordecalidad.rules import validateReferentialIntegrity
    data,errorDf = validateReferentialIntegrity(test_df,test_df,["id"],["id"],3,"TEST","TEST","100")
    assert data[-1] == 0

def test_format_date(test_df,spark_session):
    from motordecalidad.rules import validateFormatDate
    data,errorDf = validateFormatDate(test_df,"yyyy-MM-dd","date","TEST","100",spark_session)
    assert data[-1] == 0

def test_validate_range(test_df):
    from motordecalidad.rules import validateRange
    data, errorDF = validateRange(test_df,"value",3,"TEST","100","0","4")
    assert data[-1] == 0

def test_validate_catalog(test_df):
    from motordecalidad.rules import validateCatalog
    data, errorDf = validateCatalog(test_df,"id",3,"TEST","100",["a","b","c"])
    assert data[-1] == 0

def test_validate_forb_char(test_df):
    from motordecalidad.rules import validateForbiddenCharacters
    data, errorDf = validateForbiddenCharacters(test_df,"id",["a"],3,"TEST","100")
    assert data[-1] == 1

def test_validate_type(test_df):
    from motordecalidad.rules import validateType
    data, errorDF = validateType(test_df,"string","id",3,"TEST","100")
    assert data[-1] == 0

def test_validate_composision(test_df):
    from motordecalidad.rules import validateComposision
    data, errorDf = validateComposision(test_df,"mix",["id","value"],3,"TEST","100")
    assert data[-1] == 0

def test_validate_length(test_df):
    from motordecalidad.rules import validateLength
    data, errorDf = validateLength(test_df,"id",3,"TEST","100","0","2")
    assert data[-1] == 0

def test_validate_data_type(test_df):
    from motordecalidad.rules import validateDataType
    data = validateDataType(test_df,"id",3,"TEST","100","StringType()")
    assert data[-1] == 0

def test_validate_numeric_format(test_df):
    from motordecalidad.rules import validateFormatNumeric
    data,errorDf = validateFormatNumeric(test_df,"value",3,"TEST","100",2,2)
    assert data[-1] == 0

def test_validate_time_in_range(test_df):
    from motordecalidad.rules import validateTimeInRange
    data,errorDf = validateTimeInRange(test_df,"date","2022-12-31","yyyy-MM-dd","YEAR",3,"TEST","100",maxRange=1)
    assert data[-1] == 0