from pathlib import Path
import unittest
import logging
from dataclasses import dataclass

from hdlshare.dsapi import get_source, read_profile, list_shares

@dataclass
class C:
	n: str = "\033[0m"
	red: str = "\033[31m"
	green: str = "\033[32m"
	yellow: str = "\033[33m"
	blue: str = "\033[34m"
	magenta: str = "\033[35m"
	cyan: str = "\033[36m"

input_data = Path("./data/store_300.csv")
input_csn = Path("./data/store_300.json")
input_csn_mod = Path("./data/store_300_mod.json")
output_test = Path("./data/output_test")

profile = read_profile('profiles/dbxglobal.json')
test_table = "retail.transactions.france"
share, schema, table = get_source(test_table)
version = 4
limit = 100000
path = Path('tests/data')


logging.basicConfig(format=f'{C.blue}TEST:{C.yellow} %(message)s{C.n}',level=logging.INFO)

class TestStringMethods(unittest.TestCase):

    def test_get_source(self):
        share, schema, table = get_source(test_table)
        self.assertTrue(share=='retail' and schema=='transactions' and table=='france')

    def test_listshares(self):
        response = list_shares(profile)
        print(f"Shares: {response}")
        self.assertTrue('items' in response and isinstance(response['items'], list))

    # def test_csn_creation_with_key(self):
    #     df = pd.read_csv(input_data)
    #     df.set_index('transaction_id', inplace=True)
    #     csn = PyCSN(df, input_data.stem)
    #     file_name =csn.write(output_test)
    #     logging.info(f"Set primary key \"transaction_id\" to df and create csn-file {C.red}{file_name}{C.n}")
    #     self.assertTrue(Path(file_name).is_file())

    # def test_cds_creation(self):
    #     df = pd.read_csv(input_data)
    #     csn = PyCSN(df, input_data.stem)
    #     file_name =csn.write(output_test,format='cds')
    #     logging.info(f"Set primary key \"transaction_id\" to df and create cds-file {C.red}{file_name}{C.n}")
    #     self.assertTrue(Path(file_name).is_file())

    # def test_df_mod_by_cds(self):
    #     df = pd.read_csv(input_data)
    #     csn = PyCSN(input_csn)
    #     logging.info(f"Update DataFrame keys from scn-file: {C.red}{input_csn}{C.n}")
    #     csn.update_df(df, input_data.stem)
    #     print(f"New dtype of \"store_id\": {df['store_id'].dtype}")
    #     self.assertTrue(not pd.api.types.is_numeric_dtype(df['store_id']))

    # def test_df_change_primary_key_by_cds(self):
    #     df = pd.read_csv(input_data)
    #     csn = PyCSN(input_csn)
    #     print(f"Original DataFrame (no index) updated by csn-file: {input_csn}")
    #     csn.update_df(df, input_data.stem)
    #     logging.info("Change primary key form \"transaction_id\" to\"[store_id, transaction_id]\" with csn-file {input_csn_mod}")
    #     csn2 = PyCSN(input_csn_mod)
    #     csn2.update_df(df, input_data.stem)
    #     self.assertCountEqual(df.index.names,['store_id', 'transaction_id'])

    # def test_add_annotations(self):
    #     csn = PyCSN(input_csn)
    #     logging.info("Add annotations to csn-file {input_csn}")
    #     csn.add_annotation(input_csn.stem,{'@description': 'csn-file is generated'})
    #     self.assertTrue(PyCSN.search_elem(csn.csn, '@description'),'csn-file is generated')
    #     csn.add_annotation('store_id',{'hint': 'Potential foreign key'})
    #     self.assertTrue(PyCSN.search_elem(csn.csn, '@hint'),'Potential foreign key')


if __name__ == '__main__':
    unittest.main()