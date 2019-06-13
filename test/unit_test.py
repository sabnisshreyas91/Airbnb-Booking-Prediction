import pandas as pd
import numpy as np
import os
from src.generate_features_labels import get_session_features


test_case1_inp = pd.DataFrame({'user_id':['1','1','1','1','1'],'col1': ['a', 'a', 'b', 'b','b']})
test_case1_expected = pd.DataFrame({'user_id':['1'],'a': [2],'b':[3]})
test_case1_expected = pd.DataFrame({'user_id':['1'],'a': [2],'b':[3]})
test_case1_expected.set_index('user_id', inplace=True)
test_case1_expected.columns.name = 'col1'

def test_get_session_features():
    assert test_case1_expected.equals(get_session_features(test_case1_inp, 'col1'))

