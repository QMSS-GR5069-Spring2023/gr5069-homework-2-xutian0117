
import os
import pandas as pd
class Dispose:

    path_all = []
    disp_data = {
        'Exclusionary':{
            'Suspension':None,
            'Zero tolerance':None,
            'Law enforcement':None,
            'Corporal punishment':None,
            'Criminal charges':None,
            'Expulsion':None,
            'Punitive':None,
            'Canine searches':None,
            'Suspicionless searches':None,
            'Hallway sweeps':None,
            'In school suspension':None,
            'out of school suspension':None,
            'police':None,
            'Alternative learning center':None,
            'search and seizure':None


        },
        'Non-exclusionary':{
            'Restorative Justice':None,
            'Restorative Practices':None,
            'Restorative':None,
            'circles':None,
            'Mutually agreed upon consequence':None,
            'Progressive':None,
            'Affirming':None,
            'identity':None,
            'Culturally responsive':None,
            'Social justice':None,
            'Equity':None,
            'Student rights':None,
            'student voice':None,
            'appeals process':None,
            'Social emotional learning':None,
            'Counseling':None,
            'Positive Behavioral Intervention Supports':None,
            'Tiered levels of consequences':None,
            'Levels of intervention for infractions':None,
            'Point system':None,
            'PBIS':None
        }
    }

    def __init__(self):
        self.file_queue = []
        self.file_data = {}
        self.file_path = None

        self.dict_data = []
        self.data_frame_obj = pd.DataFrame
        self.pandas_frame_data = pd.DataFrame()

    def get_file_directory(self,path,suffix = None, exclude = None,):

        suffix = suffix if suffix else '.txt'
        exclude = exclude if exclude else []

        file_list = os.listdir(path)
        for file_item in file_list:
            name,suffix_ = os.path.splitext(file_item)
            if suffix_ == suffix:
                self.file_queue.append(file_item)

        # self.file_queue = os.listdir(path)
        self.file_path = path

    def open_file(self,path_file = None,mode = 'r',encoding = 'utf-8'):

        path = self.file_path
        path_file = path_file if path_file else self.file_queue
        for file_path in path_file:
            file_path_all = rf'{path}\{file_path}'
            with open(file_path_all,mode,encoding=encoding) as file:
                name,suffix = os.path.splitext(file_path)
                self.file_data.update({name:file.read()})

    def re_non_exclusionary(self,re_str,key_dict = 'Exclusionary'):

        re_da_str = ''
        count_str = ''
        re_success_data = []
        re_data_count = {}
        re_value = None
        len_re_str = len(re_str)
        value_frequency = {}
        # key_frequency = None
        key_count = 0

        for key,value in self.disp_data[key_dict].items():
            re_count = re_str.count(key.lower())
            if re_count:
                re_success_data.append(key)
                re_data_count.update({key: re_count})
                count_str_len = len(key) * len_re_str
                key_count += count_str_len
                value_frequency.update({key:re_count / count_str_len})
                re_value = key_dict
        for key,value in re_data_count.items():
            re_da_str += f'/{key}' if re_da_str else key
            count_str += f'/{key}:{value}' if count_str else f'{key}:{value}'
        data_compute = {'len':len_re_str,'key_frequency':float(f'{key_count / len_re_str:.2}') if len_re_str else None,'value_frequency':value_frequency,'re_success_data':re_success_data,'re_data_count':re_data_count}
        re_data = {'High School':None,'Discipline Approach':re_da_str,'Exclusionary/Non-exclusionary':re_value,f'Count':count_str}
        return re_data,data_compute

    def _dict_str(self,dict):

        str_dict = ''
        for key,value in dict.items():
            value = f'{value:.2e}'
            if str_dict:
                str_dict += f'/{key}:{value}'
                continue
            str_dict += f'{key}:{value}'
        return str_dict

    def re_value(self,re_str,key = None):

        excl_mode = None
        re_dict_a,data_compute_a = self.re_non_exclusionary(re_str)
        re_dict_b,data_compute_b = self.re_non_exclusionary(re_str,'Non-exclusionary')
        excl_freq_a = data_compute_a['key_frequency']
        non_excl_freq_b = data_compute_b['key_frequency']
        excl_value_freq_a = self._dict_str(data_compute_a['value_frequency'])
        non_excl_value_freq_b = self._dict_str(data_compute_b['value_frequency'])

        key = key.replace('_',' ') if type(key) == str else key
        try:
            if excl_freq_a == non_excl_freq_b:
                excl_mode = 'Exclusionary/Non-exclusionary'
            elif excl_freq_a > non_excl_freq_b:
                excl_mode = 'Exclusionary'
            else :
                excl_mode = 'Non-exclusionary'
        except TypeError:
            pass

        re_dict = {'High School':key, 'Exclusionary Discipline Approach':re_dict_a['Discipline Approach'],'Non-exclusionary Discipline Approach':re_dict_b['Discipline Approach'], 'Exclusionary/Non-exclusionary':excl_mode,'Exclusionary Count':re_dict_a['Count'],'Non-exclusionary Count':re_dict_b['Count'],'Exclusionary Frequency':excl_freq_a,'Non-exclusionary Frequency':non_excl_freq_b,'Exclusionary Value Frequency':excl_value_freq_a,'Non-exclusionary Value Frequency':non_excl_value_freq_b}
        return re_dict

    def process_the_data(self):

        for key, value in self.file_data.items():
            d = self.re_value(value,key)
            self.dict_data.append(d)

    def pandas_file_value(self,):
        data_frame = pd.DataFrame(self.dict_data)
        self.pandas_frame_data = data_frame


def main(txt_file_path,execl_path):
    '''
    
    :param txt_file_path:
    :param exel_path:
    :return:
    '''
    a = Dispose()
    a.get_file_directory(txt_file_path)
    a.open_file()
    a.process_the_data()
    a.pandas_file_value()
    print(a.pandas_frame_data)  
    a.pandas_frame_data.to_excel(execl_path,index=False)

if __name__ == '__main__':
    # main('txt_file_path','execl_file_path')
    main(r'\data.xlsx')