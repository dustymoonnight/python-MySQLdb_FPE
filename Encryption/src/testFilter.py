'''
Created on 2012-5-20

@author: wanqxu
'''

from MySQLdb_Encryption.encryption_lib import Prefix,CycleWalking,FeistelCycle,FFX,BPS,ChaosFeistel
import time
pf = Prefix()
cw = CycleWalking()
fc = FeistelCycle()
ffx = FFX()
bps = BPS()
cf = ChaosFeistel()
print bps.encrypt("021378624")
print bps.decrypt("345909336")
