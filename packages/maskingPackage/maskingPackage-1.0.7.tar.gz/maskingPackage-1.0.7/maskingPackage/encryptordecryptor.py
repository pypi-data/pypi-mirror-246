import pandas as pd
from cryptography.fernet import Fernet
import json

class DataEncryptorDecryptor:
    def __init__(self, decryptionkey):
        self.decryptionkey = decryptionkey

    def encrypt_data(self, data, key, json_path):
        cipher_suite = Fernet(key)

        with open(json_path, 'r') as json_file:
            init_result = json.load(json_file)
        data = pd.read_csv(data)
        sensitive_columns = []
        masking_functions = {}

        for column_info in init_result["content"]:
            if column_info["sensitivity"] == 1:
                column_name = column_info["columnName"]
                masking_function = column_info["function"]
                sensitive_columns.append(column_name)
                masking_functions[column_name] = masking_function

        if sensitive_columns:
            key = self.decryptionkey
            for column in sensitive_columns:
                new_column_name = f"{column}_encrypted"
                cipher_suite = Fernet(key)
                data[new_column_name] = data[column].apply(lambda x: cipher_suite.encrypt(x.encode()).decode())
                duplicate_mask = data[column_name].notna()  # Use 'column' instead of 'column_name'
                duplicated_rows = data[duplicate_mask]
                duplicated_df = pd.concat([data, duplicated_rows], ignore_index=True)
                result_df = pd.concat([data, duplicated_df], ignore_index=True)
        return result_df

    # def decrypt_data(self, sensitive_columns, keys):
    #     dataset = pd.read_csv(r"C:\Users\nagasundar.karthik\Desktop\fsifile\encrypted_dataset.csv", low_memory=False)
    #     for sensitive_column in sensitive_columns:
    #         decryption_key = keys
    #         if decryption_key:
    #             cipher_suite = Fernet(decryption_key)
    #             dataset[sensitive_column] = dataset[sensitive_column].apply(lambda x: cipher_suite.decrypt(x.encode()).decode())
    #         else:
    #             print(f"Decryption key not valid")
    #     return dataset
    def decrypt_data(self, sensitive_columns,masked_encrypted_csv_path, keys):
        dataset = masked_encrypted_csv_path
        
        decryption_key = keys
        if decryption_key:
            cipher_suite = Fernet(decryption_key)
            dataset[sensitive_columns] = dataset[sensitive_columns].apply(lambda x: cipher_suite.decrypt(x.encode()).decode())
        else:
            print(f"Decryption key not valid")
    
    def masking_all_column(self,encrypted_dataset, json_path):  
        def mask_column_with_function(pd_column, function):
            exec(function, globals())
            masked_column = pd_column.apply(maskInfo)
            return masked_column

        # with open(json_path, 'r') as json_file:
        #     init_result = json.load(json_file)

        maskeddata = encrypted_dataset

        for col_info in init_result['content']:
            col_name = col_info['columnName']
            if col_info.get('sensitivity') == 1:
                print(f"Applying masking to sensitive column: {col_name}...")
                maskeddata[col_name] = mask_column_with_function(maskeddata[col_name], col_info['function'])            
            else:
                print(f"Skipping non-sensitive column: {col_name}")

        return maskeddata
    def encryption_masking(self, data, key,generated_json):
        def mask_column_with_function(pd_column, function):
            exec(function, globals())
            masked_column = pd_column.apply(maskInfo)
            return masked_column
        cipher_suite = Fernet(key)

        # with open(json_path, 'r') as json_file:
        #     init_result = json.load(json_file)
        # data = pd.read_csv(data)
        init_result = generated_json
        sensitive_columns = []
        masking_functions = {}

        for column_info in init_result["content"]:
            if column_info["sensitivity"] == 1:
                column_name = column_info["columnName"]
                masking_function = column_info["function"]
                sensitive_columns.append(column_name)
                masking_functions[column_name] = masking_function

        if sensitive_columns:
            key = self.decryptionkey
            for column in sensitive_columns:
                new_column_name = f"{column}_encrypted"
                cipher_suite = Fernet(key)

                data[new_column_name] = data[column].apply(lambda x: cipher_suite.encrypt(x.encode()).decode())
                duplicate_mask = data[column_name].notna()  # Use 'column' instead of 'column_name'
                duplicated_rows = data[duplicate_mask]
                duplicated_df = pd.concat([data, duplicated_rows], ignore_index=True)
                result_df = pd.concat([data, duplicated_df], ignore_index=True)
                # with open(json_path, 'r') as json_file:
                #     init_result = json.load(json_file)

                maskeddata = result_df

                for col_info in init_result['content']:
                    col_name = col_info['columnName']
                    if col_info.get('sensitivity') == 1:
                        print(f"Applying masking to sensitive column: {col_name}...")
                        maskeddata[col_name] = mask_column_with_function(maskeddata[col_name], col_info['function'])            
                    else:
                        print(f"Skipping non-sensitive column: {col_name}")
                return maskeddata
