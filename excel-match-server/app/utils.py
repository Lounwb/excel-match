import os
import random
import pandas as pd

from .exceptions import ColumnKeyError, ConcatError, FileTypeError

def generate_random_string(len=16):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    random_string = ''.join(random.choice(characters) for i in range(len))
    return random_string

def read_file(file_name: str):
    suffix = file_name.split('.')[-1]

    if 'xlsx' == suffix or 'xls' == suffix:
        df_list = pd.read_excel(file_name, sheet_name=None, header=0)

        all_df = pd.DataFrame()
        for sheet_name, df in df_list.items():
            all_df = all_df.append(df)
        return all_df

    elif 'csv' == suffix: 
        df_list = pd.read_csv(file_name, header=0, encoding='utf-8')
        return df_list

    return None

def concat_files(folder_path, mode='match'):
    concat_df = pd.DataFrame()
    col = None

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        df = read_file(file_path)

        if len(concat_df) == 0:
            col = concat_df.columns

        else:
            if not col.equals(df.columns):
                raise ConcatError(f'{mode} files are not uniform, please check.')

        df['{}文件名称'.format('匹配' if mode == 'match' else '候选')] = file_name
        concat_df = pd.concat([concat_df, df]) 
    
    concat_df = concat_df.reset_index(drop=True).reset_index().set_index('index')

    return concat_df

def merge_match_candidate(match_df: pd.DataFrame, 
                          candidate_df: pd.DataFrame, 
                          merge_condition, 
                          mode='inner'):
    
    if merge_condition['match'] not in match_df.columns:
        raise ColumnKeyError('Match attribute column does not exist, please check.')
    
    if merge_condition['candidate'] not in candidate_df.columns:
        raise ColumnKeyError('Cadndidate attribute column does not exist, please check.')
    
    if mode in ['inner', 'left', 'right']:
        reuslt_df = pd.merge(match_df, 
                             candidate_df, 
                             left_on=merge_condition['match'], 
                             right_on=merge_condition['candidate'],
                             how=mode)
    else:
        raise ValueError('Unsupported merge mode.')
    
    return reuslt_df

def save_result(df: pd.DataFrame, file_name: str):
    suffix = file_name.split('.')[-1]

    # add index
    if '序号' in df.columns:
        df['序号'] = df.index
        df = df.reset_index(drop=True)
        df.index = df.index + 1
    elif '序号_x' in df.columns:
        df['序号_x'] = df.index
        df = df.reset_index(drop=True)
        df['序号_x'] = df.index + 1

    if suffix in ['xlsx', 'xls']:
        with pd.ExcelWriter(file_name, mode='w') as writer:
            df.to_excel(writer, index=False)
    elif suffix in ['csv']:
        df.to_csv(file_name, index=False)
    else:
        raise FileTypeError("Unsupported file type!")
    