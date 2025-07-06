from pandas import DataFrame
from pandas.testing import assert_frame_equal
from predicates import any_of, all_of, none_of, never, always, col
from pytest import raises, fixture


@fixture
def dataframe():
    return DataFrame([
        {"age": 20, "name": "John", "city": "London", "country": "UK"},
        {"age": 30, "name": "Jane", "city": "Paris", "country": "France"},
        {"age": 40, "name": "Jack", "city": "London", "country": "UK"},
        {"age": 50, "name": "Jill", "city": "Paris", "country": "France"},
        {"age": 30, "name": "Adam", "city": "Berlin", "country": "Germany"},
        {"age": 40, "name": "Eve", "city": "Berlin", "country": "Germany"},
        {"age": 50, "name": "Linda", "city": "São Paulo", "country": "Brasil"},
        {"name": "Linda", "city": "São Paulo", "country": "Brasil"},
    ])


def test_col_eq(dataframe):
    expr = col("age") == 30
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.age == 30]
    )

def test_col_ne(dataframe):
    expr = col("age") != 30
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.age != 30]
    )
    
def test_col_gt(dataframe):
    expr = col("age") > 30
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.age > 30]
    )
    
def test_col_ge(dataframe):
    expr = col("age") >= 30
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.age >= 30]
    )
    
def test_col_lt(dataframe):
    expr = col("age") < 30
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.age < 30]
    )

def test_col_le(dataframe):
    expr = col("age") <= 30
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.age <= 30]
    )
    
def test_col_in(dataframe):
    """
    Not implemented yet
    """
    expr = col("age").isin([30, 40])
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.age.isin([30, 40])]
    )

def test_col_not_in(dataframe):
    """
    Not implemented yet
    """
    expr = ~col("age").isin([30, 40])
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe[~dataframe.age.isin([30, 40])]
    )


def test_col_between(dataframe):
    """
    Not implemented yet
    """
    expr = col("age").between(30, 40)
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.age.between(30, 40)]
    )


def test_col_isna(dataframe):
    """
    Not implemented yet
    """
    expr = col("age").isna()
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.age.isna()]
    )

def test_col_isnull(dataframe):
    """
    Not implemented yet
    """
    expr = col("age").isnull()
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.age.isnull()]
    )

def test_predicates_and(dataframe):
    expr = (col("age") > 30) & (col("age") < 50)
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[(dataframe.age > 30) & (dataframe.age < 50)]
    )
    
def test_predicates_or(dataframe):
    expr = (col("age") > 30) | (col("age") < 30)
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[(dataframe.age > 30) | (dataframe.age < 30)]
    )
    
def test_predicates_not(dataframe):
    expr = ~(col("age") > 30)
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[~(dataframe.age > 30)]
    )
    
def test_predicates_any_of(dataframe):
    expr = any_of(col("age") > 30, col("age") < 20)
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[(dataframe.age > 30) | (dataframe.age < 20)]
    )
    
def test_predicates_all_of(dataframe):
    expr = all_of(col("age") > 30, col("age") < 50)
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[(dataframe.age > 30) & (dataframe.age < 50)]
    )
    
def test_predicates_none_of(dataframe):
    expr = none_of(col("age") > 30, col("age") < 20)
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[~((dataframe.age > 30) | (dataframe.age < 20))]
    )
    
def test_predicates_never(dataframe):
    expr = never()
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.age == "rafael"]
    )
    
def test_predicates_always(dataframe):
    expr = always()
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe
    )
    
def test_str_contains(dataframe):
    expr = col("name").str.contains("J.*n")
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.name.str.contains("J.*n")]
    )
    
def test_str_fullmatch(dataframe):
    expr = col("name").str.fullmatch("J.*n")
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.name.str.fullmatch("J.*n")]
    )
    
def test_str_match(dataframe):
    expr = col("name").str.match("J.*n")
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.name.str.match("J.*n")]
    )
    
def test_str_startswith(dataframe):
    expr = col("name").str.startswith("Ja")
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.name.str.startswith("Ja")]
    )
    
def test_str_isalnum(dataframe):
    expr = col("name").str.isalnum()
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.name.str.isalnum()]
    )
    
def test_str_isdigit(dataframe):
    expr = col("name").str.isdigit()
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.name.str.isdigit()]
    )
    
def test_str_isspace(dataframe):
    expr = col("name").str.isspace()
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.name.str.isspace()]
    )
    
def test_str_islower(dataframe):
    expr = col("name").str.islower()
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.name.str.islower()]
    )
    
def test_str_isupper(dataframe):
    expr = col("name").str.isupper()
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.name.str.isupper()]
    )
    
def test_str_islower(dataframe):
    expr = col("name").str.islower()
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.name.str.islower()]
    )
    
def test_str_istitle(dataframe):
    expr = col("name").str.istitle()
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.name.str.istitle()]
    )
    
def test_str_isnumeric(dataframe):
    expr = col("name").str.isnumeric()
    assert_frame_equal(
        expr.filter(dataframe),
        dataframe.loc[dataframe.name.str.isnumeric()]
    )