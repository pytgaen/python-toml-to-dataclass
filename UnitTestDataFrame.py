from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List

import pandas as pd


# @dataclass
# class DataTable:
#     columns:List[str]
#     data:List[Any]

@dataclass
class UnitTestDataframeConfig:
    build_reference: bool = True
    path_reference_files: Path = Path(".")


unit_test_dataframe_config = UnitTestDataframeConfig()


@dataclass
class TestDataframeReference:
    df_reference: Optional[pd.DataFrame]

    def assert_equal(self, df_to_test: pd.DataFrame, ignore_columns: List[str] = []):
        return self.count_row_difference(df_to_test, ignore_columns) == 0

    def count_row_difference(self, df_to_test: pd.DataFrame, ignore_columns: List[str] = []):
        diff = self.df_reference(df_to_test, ignore_columns)
        return diff.shape[0]

    def diff_with_ref(self, df_to_test: pd.DataFrame, ignore_columns: List[str] = []) -> pd.DataFrame:
        cols = [c for c in self.df_reference.columns.tolist() if c not in set(ignore_columns)]

        df_ref = self.df_reference.copy(deep=True)
        df_ref["origin_ref"] = "ref"

        df_tst = df_to_test.copy(deep=True)
        df_tst["origin_tst"] = "tst"

        df_diff = df_ref.merge(df_tst, on=cols, how="outer")

        df_diff = df_diff[df_diff["origin_ref"].isnull() | df_diff["origin_tst"].isnull()]
        df_diff["origin"] = df_diff['origin_ref'].combine_first(df_diff['origin_tst'])
        return df_diff.drop(columns=['origin_ref', 'origin_tst'])


@dataclass
class TestDataframe:
    df_to_test: pd.DataFrame

    # df_reference: Optional[p
    def count_where(self, cond=None):
        if cond:
            return self.df_to_test.query(cond).shape[0]
        else:
            return self.df_to_test.shape[0]


data = [[1, 2, 3], [4, 5, 6]]
df_ref = pd.DataFrame(data, columns=["a", "b", "c"])

data = [[1, 2, 3], [44, 5, 6]]
df_1 = pd.DataFrame(data, columns=["a", "b", "c"])

dj = TestDataframe(df_ref)
print(dj.assert_equal(df_ref))

dj = TestDataframe(df_1)
print(dj.assert_equal(df_ref, ['a']))
print(dj.assert_equal(df_ref))
print(dj.count_where("a==1 | b==5"))
