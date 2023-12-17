# %%
import pandas as pd
import re
from zipfile import ZipFile
from maldives.utils.scrapping import download_links_on_page


class USDACattleData(object):
    def __init__(self, base_url="https://usda.library.cornell.edu/concern/publications/m326m174z", work_dir="cattle_data"):
        self.base_url = base_url
        self.work_dir = work_dir
        self.df = None

    # Methods for parsing
    @staticmethod
    def _extract_tables(lines, titles):
        tables = {k: [] for k in titles.keys()}
        write_to = None  # pointer to which table we are writing

        for ln in lines:
            if type(ln) is bytes:
                ln = ln.decode('latin1')
            ln = ln.strip()

            if write_to is not None:
                if ('"d"' in ln) or (',d,' in ln):
                    write_to.append(ln.strip().strip(','))
                elif ('"c"' in ln) or (',c,' in ln):
                    write_to = None
            else:
                for k, v in titles.items():
                    if any([vv in ln for vv in v]) and len(tables[k]) == 0:
                        write_to = tables[k]
                        break
        return tables

    @staticmethod
    def _parse_zipped_data(fname):
        zf = ZipFile(fname)
        table_titles = {'Placed': ['Cattle Placed on Feed by Weight Group'],
                        'Inventory': ['Cattle on Feed Inventory, Placements, Marketings, and Other Disappearance',
                                      'Cattle on Feed, Placements, Marketings, and Other Disappearance']}
        tables = USDACattleData._extract_tables(
            zf.open('cofd_all_tables.csv').readlines(), table_titles)

        FORMAT_ONFEEDBYWEIGHT = {'PLACED_U600': 3, 'PLACED_U700': 4, 'PLACED_U800': 5,
                                 'PLACED_U900': 6, 'PLACED_U1000': 8, 'PLACED_A1000': 9}

        def _format_tuple(tuple, format):
            return {k: tuple[v] for k, v in format.items()}

        data = _format_tuple(
            tables['Placed'][-1].split(','), FORMAT_ONFEEDBYWEIGHT)
        data['ONFEED_OPEN'] = tables['Inventory'][0].split(',')[-2]
        data['PLACED'] = tables['Inventory'][1].split(',')[-2]
        data['MARKETED'] = tables['Inventory'][2].split(',')[-2]
        data['DISAPPEAR'] = tables['Inventory'][3].split(',')[-2]
        data['ONFEED_CLOSE'] = tables['Inventory'][4].split(',')[-2]
        return data

    @staticmethod
    def _parse_date(fname):
        fname = fname.split('/')[-1]
        if fname.startswith('cofd'):  # new format
            date_format = ['\d{4}', '%m%y']
        else:
            date_format = ['\d{2}-\d{2}-\d{4}', '%m-%d-%Y']
        return pd.to_datetime(re.search(date_format[0], fname).group(), format=date_format[1]).replace(day=1)

    def load_data(self, num_months=60, overwrite=False):
        data_files = []
        page = 1
        while len(data_files) < num_months:
            data_files.extend(download_links_on_page(
                f"{self.base_url}?page={page}", self.work_dir, overwrite=overwrite, regex="*.zip"))
            page += 1

        entries = []
        for fname in set(data_files):
            try:
                data = USDACattleData._parse_zipped_data(fname)
                data['Date'] = USDACattleData._parse_date(
                    fname)-pd.DateOffset(months=1)
                entries.append(data)
            except Exception as ex:
                print(f"Unable to parse {fname}.")
                continue
        self.df = pd.DataFrame(entries).set_index(
            'Date').sort_index().astype(float)
        
        import_export = USDABeefTradeData().load_data()
        self.df = self.df.join(import_export[['NETIMPORT']])
        return self.df

    def info(self):
        columns_descriptions = {
            'PLACED_U600': 'Cattles under 600 lbs placed on feed during the month [Unit: 1000 head]',
            'PLACED_U700': 'Cattles of 600-699 lbs placed on feed during the month [Unit: 1000 head]',
            'PLACED_U800': 'Cattles of 700-799 lbs placed on feed during the month [Unit: 1000 head]',
            'PLACED_U900': 'Cattles of 800-899 lbs placed on feed during the month [Unit: 1000 head]',
            'PLACED_U1000': 'Cattles of 900-1000 lbs placed on feed during the month [Unit: 1000 head]',
            'PLACED_A1000': 'Cattles above 1000 lbs placed on feed during the month [Unit: 1000 head]',
            'PLACED': 'Total number of cattles placed on feed during the month [Unit: 1000 head]',
            'ONFEED_OPEN': 'Cattles that are on feed at the beginning of the month [Unit: 1000 head]',
            'ONFEED_CLOSE': 'Cattles that are on feed at the end of the month [Unit: 1000 head]',
            'MARKETED': 'Cattles that are slaughtered during the month [Unit: 1000 head]',
            'DISAPPEAR': 'Cattles that disappeared during the month [Unit: 1000 head]',
            'NETIMPORT' : 'Net import of beef [Unit:KG]'
        }
        return pd.Series(columns_descriptions)


class USDABeefTradeData(object):
    def __init__(self, base_url="https://www.ers.usda.gov/data-products/livestock-and-meat-international-trade-data", work_dir="meat_trade_data"):
        self.base_url = base_url
        self.work_dir = work_dir
        self.df = None

    @staticmethod
    def _format_df(df, desc='bovine animals'):
        df['Date'] = pd.to_datetime(df.YEAR_ID.astype(
            str)+'/'+df.TIMEPERIOD_ID.astype(str)+'/'+'01')

        bovine = df.COMMODITY_DESC.str.contains(desc)
        return df[bovine].query('UNIT_DESC=="KG" and GEOGRAPHY_DESC=="World"').groupby(['Date']).AMOUNT.sum()

    def load_data(self, overwrite=True):
        download_links_on_page(self.base_url, self.work_dir,
                               overwrite=overwrite, regex='*.zip?v*')

        zf = ZipFile(f'{self.work_dir}/LivestockMeatTrade.zip')
        df_export = USDABeefTradeData._format_df(
            pd.read_csv(zf.open('LivestockMeat_Exports.csv')))
        df_import = USDABeefTradeData._format_df(
            pd.read_csv(zf.open('LivestockMeat_Imports.csv')))

        self.df = pd.concat([df_export.rename('Export'),
                            df_import.rename('Import')], axis=1)
        self.df['NETIMPORT'] = self.df.eval('Import-Export')

        return self.df
