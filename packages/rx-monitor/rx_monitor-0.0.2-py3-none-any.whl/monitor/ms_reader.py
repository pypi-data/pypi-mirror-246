import os

import numpy
import pandas            as pnd
import utils_noroot      as utnr


from importlib.resources import files
from stats.average       import average  as stav
from rk.scales           import mass     as mscale
from rk.scales           import fraction as fscale
from logzero             import logger   as log

#----------------------------------------
class ms_reader:
    '''
    This class is used to read the mass scales and resolution values stored in JSON files
    '''
    def __init__(self, version=None):
        self._vers = version

        self._l_scale = ['mu', 'sg', 'br']
        self._l_trig  = ['MTOS', 'ETOS', 'GTIS'] 
        self._l_year  = ['2011', '2012', '2015', '2016', '2017', '2018'] 
        self._l_brem  = [0, 1, 2]

        self._cas_dir = os.environ['CASDIR']
        self._dat_dir = files('monitor_data').joinpath(self._vers)
    #----------------------------------------
    def _get_mscale_brem(self, year, trig, brem):
        dat_path = f'{self._cas_dir}/monitor/mass_scales/{self._vers}/{year}_{trig}/pars/cat_{brem}/data.json'
        sim_path = f'{self._cas_dir}/monitor/mass_scales/{self._vers}/{year}_{trig}/pars/cat_{brem}/signal.json'
    
        d_dat = utnr.load_json(dat_path)
        d_sim = utnr.load_json(sim_path)
    
        ms    = mscale(dt=d_dat, mc=d_sim)
    
        return ms 
    #----------------------------------------
    def _get_bscale(self, year, trig):
        '''
        Will return a list with the fraction of brem and the corresponding error, i.e.
    
        [val_br_0, err_br_0, ..., err_br_2]
        '''
        if trig == 'MTOS':
            return [1, 0, 0, 0, 0, 0] 
    
        d_mscale = {}
        for brem in self._l_brem:
            d_mscale[brem] = self._get_mscale_brem(year, trig, brem)
    
        fr   = fscale(d_mscale)
        d_fr = fr.scales
    
        val_z, err_z = d_fr[0]
        val_o, err_o = d_fr[1]
        val_t, err_t = d_fr[2]
    
        return [val_z, err_z, val_o, err_o, val_t, err_t] 
    #----------------------------------------
    def _get_mscale(self, year, trig):
        l_ms   = []
        l_brem = [0] if trig == 'MTOS' else self._l_brem
    
        for brem in l_brem:
            ms = self._get_mscale_brem(year, trig, brem)
            l_ms.append(ms)
    
        d_scale = {}
        if   len(l_ms) > 1:
            d_scale = l_ms[0].combine(l_ms[1:])
        elif len(l_ms) == 1:
            val, err = l_ms[0].scale
            d_scale['scale']      = val, err, 1
    
            val, err = l_ms[0].resolution
            d_scale['resolution'] = val, err, 1
        else:
            log.error(f'Invalid size of list of mass objects: {len(l_ms)}')
            raise
    
        return d_scale 
    #----------------------------------------
    def _get_mass_scales(self, scale):
        l_col = []
        for trig in self._l_trig:
            l_col.append(f'v_{trig}')
            l_col.append(f'e_{trig}')
    
        df = pnd.DataFrame(columns=l_col)
        for year in self._l_year:
            l_row = []
            for trig in self._l_trig:
                d_scale = self._get_mscale(year, trig)
    
                scl_v, scl_e, _ = d_scale['scale']
                res_v, res_e, _ = d_scale['resolution']
    
                if   scale == 'mu':
                    l_row.append(scl_v)
                    l_row.append(scl_e)
                elif scale == 'sg':
                    l_row.append(res_v)
                    l_row.append(res_e)
                else:
                    log.error(f'Invalid scale: {scale}')
                    raise ValueError
    
            df_scl = utnr.add_row_to_df(df, l_row, index=year)
    
        return df
    #----------------------------------------
    def _get_brem_scales(self, scale):
        l_col = []
        for brem in self._l_brem:
            l_col.append(f'v_{brem}')
            l_col.append(f'e_{brem}')
    
        df = pnd.DataFrame(columns=l_col)
        for year in self._l_year:
            for trig in ['MTOS', 'ETOS', 'GTIS']:
                l_row = self._get_bscale(year, trig)
                utnr.add_row_to_df(df, l_row, index=f'{trig}_{year}')
    
        return df
    #----------------------------------------
    def _avg_years(self, ser_1, ser_2):
        d_val_1 = {}
        d_val_2 = {}
        s_qnt   = set()
        for col_name in ser_1.index:
            qnt = col_name[2:]
            s_qnt.add(qnt)
            d_val_1[col_name] = ser_1[col_name]
            d_val_2[col_name] = ser_2[col_name]
        
        d_avg = {}
        for qnt in s_qnt:
            v1 = d_val_1[f'v_{qnt}']
            e1 = d_val_1[f'e_{qnt}']
        
            v2 = d_val_2[f'v_{qnt}']
            e2 = d_val_2[f'e_{qnt}']
        
            arr_val = numpy.array([v1, v2])
            arr_err = numpy.array([e1, e2])
        
            av, er, pv = stav(arr_val, arr_err)
            d_avg[f'v_{qnt}'] = av
            d_avg[f'e_{qnt}'] = er
        
        sr_av = pnd.Series(d_avg)

        return sr_av
    #----------------------------------------
    def _avg_dset(self, df, scale, dset=None):
        if dset is None:
            df = self._avg_dset(df, scale, dset='r1')
            df = self._avg_dset(df, scale, dset='r2p1')
            return df
        elif dset not in ['r1', 'r2p1']:
            log.error(f'Invalid dataset: {dset}')
            raise ValueError

        l_trig = ['MTOS_', 'ETOS_', 'GTIS_'] if scale == 'br' else ['']
        for trig in l_trig:
            y1, y2 = (f'{trig}2011', f'{trig}2012') if dset == 'r1' else (f'{trig}2015', f'{trig}2016')

            sr_y1 = df.loc[y1]
            sr_y2 = df.loc[y2]
            if trig == 'MTOS_':
                sr_av = sr_y1 
            else:
                sr_av = self._avg_years(sr_y1, sr_y2) 

            df       = df.drop(y1)
            df       = df.drop(y2)
            df       = utnr.add_row_to_df(df, sr_av, index=f'{trig}{dset}')

        return df
    #----------------------------------------
    def get_scales(self, scale, avg_dset=False):
        '''
        This function returns a pandas dataframe with the scales and resolution
        information

        Parameters
        ----------------
        scale (str): mu (mass scale), sg (mass resolution), br (Bremsstrahlung correction)
        avg_dset (bool): If set to true will average 2011 and 2012 to give r1, same with r2p1

        Returns 
        ----------------
        Pandas dataframe
        '''
        scl_dir   = utnr.make_dir_path(self._dat_dir)
        json_path = f'{scl_dir}/{scale}.json'
    
        if os.path.isfile(json_path):
            log.info(f'Loading cached scales from: {json_path}')
            df       = pnd.read_json(json_path)
            df.index = df.index.astype(str)

            return df if not avg_dset else self._avg_dset(df, scale)

        log.warning(f'Need to remake scales, not found in: {json_path}')
        if   scale in ['mu', 'sg']:
            df = self._get_mass_scales(scale)
        elif scale == 'br':
            df = self._get_brem_scales(scale)
        else:
            log.error(f'Invalid scale: {scale}')
            raise ValueError
    
        log.info(f'Caching scales to: {json_path}')
        df.index = df.index.astype(str)
        df.to_json(json_path)

        return df if not avg_dset else self._avg_dset(df, scale)
#----------------------------------------

