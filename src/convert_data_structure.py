from typing import List, Dict
from get_idx import GetIdx, ogaColumnIndexError

class ConvertDataStructure:
    
    @staticmethod
    def convert_2d_list_to_1d_list(cols: List[str], data: List[List[str]], 
                                   col_name: str) -> List[str]:
        list: List[str] = []
        idx = GetIdx.get_idx(cols, col_name)
        if idx == -1:
            raise ogaColumnIndexError(f'{col_name}のカラムが不正です。')

        for line in data:
            list.append(line[idx])

        return list

    @staticmethod
    def convert_2d_list_to_3args_dict(cols: List[str], data: List[List[str]],
                                     *args: str) -> Dict[str, List[str]]:
        result: Dict[str, List[str]] = {}
        key_idx: int = GetIdx.get_idx(cols, args[0])     
        val1_idx: int = GetIdx.get_idx(cols,args[1])
        val2_idx: int = GetIdx.get_idx(cols, args[2])

        if key_idx == -1 or val1_idx == -1 or val2_idx == -1:
            raise ogaColumnIndexError(f'{args}のカラムが不正です。')

        for line in data:
            val1 = line[val1_idx]
            if val1 ==  ' ' or val1 == '':
                val1 = '      '
            strs = f'{val1} -> {line[val2_idx]}'
            if not line[key_idx] in result:
                result[line[key_idx]] = [strs]
            else:
                result[line[key_idx]].append(strs)

        return result


    @staticmethod
    def convert_dict_dict_to_list(dict: Dict[str, Dict[str, bool]],
                                  outkey: str)-> List[str]:
        list: List[str] = []
        for key in dict['cans_for_export']:
            list.append(key)
        return list
