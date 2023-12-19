from aavs_uv.io import hdf5_to_uv, uv5_to_uv, uv_to_uv5

def test_roundtrip():
    fn = '../example-data/aavs2_2x500ms/correlation_burst_204_20230927_35116_0.hdf5'
    uv = hdf5_to_uv(fn, telescope_name='aavs2')

    uv_to_uv5(uv, 'test.h5')
    uv2 = uv5_to_uv('test.h5')

    # CHECK CONTEXT PASSING MAKES IT THROUGH ROUNDTRIP
    context = {
        'observer': 'MCCS team',
        'intent': 'Commissioning sun observation for calibration',
        'date': '2023-09-27',
        'notes': 'Commissioning observation'
    }

    uv = hdf5_to_uv(fn, telescope_name='aavs2', context=context)
    uv_to_uv5(uv, 'test.h5')
    uv2 = uv5_to_uv('test.h5')

    for k, v in uv.context.items():
        assert k in uv2.context.keys()
        print(v, uv2.context[k])
        assert uv2.context[k] == v

    for k, v in uv.provenance.items():
        assert k in uv2.provenance.keys()
        assert isinstance(uv2.provenance[k], type(v))
    
    for k, v in uv.antennas.attrs.items():
        assert k in uv2.antennas.attrs.keys()
        assert isinstance(uv2.antennas.attrs[k], type(v))



if __name__ == "__main__":
    test_roundtrip()