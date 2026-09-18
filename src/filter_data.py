from get_idx import GetIdx, ogaColumnIndexError
from typing import List, Any

class FilterData:

    @staticmethod
    def filter_data_from_2d_list(data: List[List[Any]], col: List[str],
                                 col_name: str, str_to_filter: str)-> List[Any]:
        result: List[Any] = []
        idx = GetIdx.get_idx(col, col_name)
        if idx == -1:
            raise ogaColumnIndexError(f'{col_name}のカラムが不正です。filter_data.py')

        # resultは二次元リスト（要素はひとつのリスト）
        result = [sublist for sublist in data if sublist[idx] == str_to_filter]

        return result[0]
