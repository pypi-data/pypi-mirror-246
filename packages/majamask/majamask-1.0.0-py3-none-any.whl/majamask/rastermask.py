from numba import njit
import sys, os
import numpy as np
from osgeo import gdal, gdal_array
import argparse
import time

'''
    raster spec -> masks
    1 cirrus                    - CLM bit 7
    2 tous nuages sauf cirrus   - CLM bit 1 
    3 ombre des nuages          - MG2 bit 3
    4 Neige                     - MG2 bit 2
    5 Eau                       - MG2 bit 0 
    6 Ombres topo               - MG2 bit 4
    7 zones masquée relief      - MG2 bit 5
    8 Soleil tangent ou bas     - MG2 bit 6 ou 7
'''

def test_function(str):
    print("Test : ", str)
    
@njit
def getRasterClassCLM(val):
    
    if not val : return 0

    bit_list = getBinary(val)
    if bit_list[7] : return 1
    if bit_list[1] : return 2
    return 0 

@njit
def getRasterClassMG2(val) :

    if not val : return 0

    bit_list = getBinary(val)
    if(bit_list[3]) : return 3
    if(bit_list[2]) : return 4
    if(bit_list[0]) : return 5
    if(bit_list[4]) : return 6
    if(bit_list[5]) : return 7
    if(bit_list[6] or bit_list[7]) : return 8
    return 0 

@njit
def getRasterClass(x, y, imarray_clm, imarray_mg2) :
    raster_value =  getRasterClassCLM(imarray_clm[x, y])
    if not raster_value :
        raster_value = getRasterClassMG2(imarray_mg2[x, y])
    return raster_value

@njit
def getRasterOut(imarray_clm, imarray_mg2) :
    return np.array([getRasterClass(x,y, imarray_clm, imarray_mg2) for x in range(imarray_clm.shape[0]) for y in range(imarray_clm.shape[1]) ])

@njit
def getBinary(val) :
    #list_out = np.zeros(8, dtype = int) # numba does not like it
    list_out = [0,0,0,0,0,0,0,0]
    index = 0
    while(val > 0) :
        bit = val%2
        list_out[index] = bit
        val = val // 2
        index+=1
    return list_out

def create_rastermask(input_mask_clm, input_mask_mg2, output_raster):

    time_start_tot = time.time()

    #check files exist
    if not os.path.exists(input_mask_clm) or not os.path.exists(input_mask_mg2): 
        print ("CLM or MG2 mask not found")
        return

    #Read images
    mask_clm = gdal.Open(input_mask_clm)
    mask_mg2 = gdal.Open(input_mask_mg2)
    imarray_clm = np.array(mask_clm.ReadAsArray())
    imarray_mg2 = np.array(mask_mg2.ReadAsArray())

    #input check
    assert imarray_clm.shape == imarray_mg2.shape, "Input images have different size or resolution !"
    assert imarray_clm.dtype == imarray_mg2.dtype, "Wrong format : input images must be uint8"

    #process
    time_start_proc = time.time()
    raster_out = getRasterOut(imarray_clm, imarray_mg2)
    raster_out = raster_out.reshape(imarray_clm.shape[0],-1)
    time_proc = time.time() - time_start_proc

    #write output 
    driver = gdal.GetDriverByName('GTiff')
    img_h, img_w = imarray_clm.shape
    dtype = gdal_array.NumericTypeCodeToGDALTypeCode(np.uint8)
    mem = driver.Create(output_raster, img_w, img_h, 1, dtype)
    mem.SetGeoTransform(mask_clm.GetGeoTransform())
    mem.SetProjection(mask_clm.GetProjection())
    mem.GetRasterBand(1).WriteArray(raster_out)
    mem.FlushCache()

    time_tot = time.time() - time_start_tot

    #print("Process time : ", time_proc)
    #print("Total time (read + process + write : )", time_tot)

def find_inputs(product_path):
    # one product may have several resolutions for clm and mg2 masks

    output_array = []

    mask_rep = product_path + "/MASKS"
    if os.path.exists(mask_rep) is False: return []
    clm_prefix =  os.path.basename(product_path) + "_CLM"
    mg2_prefix = os.path.basename(product_path) + "_MG2"
    resol = []
    for file in os.listdir(mask_rep):
        if file.startswith(clm_prefix):
            resol.append(file.replace(clm_prefix, ""))
    for res in resol:
        clm = mask_rep + "/" + clm_prefix + res
        mg2 = mask_rep + "/" + mg2_prefix + res
        output = mask_rep + "/rastermask" + res
        if os.path.exists(clm) and os.path.exists(mg2):
            output_array.append([clm, mg2, output])

    return output_array

def main():
    assert sys.version_info > (3, 0), "Please update Python to >3.0"

    #read arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-clm",
        "--input_mask_clm",
        help="A L2 product CLM mask",
        required = False,
        type = str
    )
    parser.add_argument(
        "-mg2",
        "--input_mask_mg2",
        help="A L2 product MG2 mask",
        required = False,
        type = str
    )
    parser.add_argument(
        "-out",
        "--output_raster",
        help="The output raster mask",
        required = False,
        type = str
    )
    parser.add_argument(
        "-product",
        "--product_folder",
        help="The folder of the L2 Muscate product",
        required = False,
        type = str
    )
    args = parser.parse_args()

    # check arguments
    input_array = []
    if (args.input_mask_clm and args.input_mask_mg2 and args.output_raster) and not args.product_folder :
        input_array.append([args.input_mask_clm, args.input_mask_mg2, args.output_raster])
    elif args.product_folder and not (args.input_mask_clm or args.input_mask_mg2 or args.output_raster) :
        input_array = find_inputs(args.product_folder)
    else :
        print("Error : Wrong input arguments : please provide either (-clm, -mg2, -out) OR -product")
        return
    if input_array == [] :
        print ("Nothing to process")
        return

    # process
    for clm, mg2, out in input_array :
        print("Creating rastermask...")
        create_rastermask(clm, mg2, out)
    
    print('---- Rastermask : Process complete ----')

if __name__ == "__main__":
    main()
    
    
