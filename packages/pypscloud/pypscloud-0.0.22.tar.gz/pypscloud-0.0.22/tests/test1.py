import sys
import os
sys.path.append(os.path.abspath("/Users/lmarchand.PS/PycharmProjects/pypscloud/pypscloud"))

from pypscloud import *

def main():
    ps = PSCommon('prod')
    s3 = PSS3
    
    ps.login()
    #ps_post_cmd(13817,7)

    ps.device_file_request_by_mp(16667, ["channels-P3020805.json"])

main()