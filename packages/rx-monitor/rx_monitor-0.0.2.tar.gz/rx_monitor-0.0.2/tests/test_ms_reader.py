from monitor.ms_reader import ms_reader

#----------------------------------
def test_simple():
    for scale in ['mu', 'sg', 'br']:
        rdr=ms_reader(version='v4')
        df =rdr.get_scales(scale, avg_dset=True)
        print(df)
#----------------------------------
if __name__ == '__main__':
    test_simple()

