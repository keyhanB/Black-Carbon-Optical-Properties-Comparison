# Programmed by Keyhan Babaee Under Prof. Steven Rogak supervision, https://github.com/KeyhanB
# Using Fortran Code from: C. Liu, X. Xu, Y. Yin, M. Schnaiter, Y. L. Yung, 2018: Black carbon aggregate: A database for optical properties
Version = 0.2
# Aug 2019
import ConfigReaderModule as CP
from ConfigReaderModule import logging
import RDG_TMatrixCalculator as K02

if __name__ == "__main__":
    CP.ReadLogConfig()
    logging.info("App Started.")
    DB_Info = CP.ReadConfigToDict(sectionName="DatabaseInfo")
    FF_Info = CP.ReadConfigToDict(sectionName="FilesFoldersInfo")
    AGG_Info = CP.ReadConfigToDict(sectionName="AggregateDetails", convertParseTo='float', hasComment=True)
    logging.info("config retrieved.")
    ##############################################
    arr = [{'AGG_EFF_RHO_100NM_CENTER': 450, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1, 'AGG_EFF_DM_CENTER': 2.2},
           {'AGG_EFF_RHO_100NM_CENTER': 450, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1.4, 'AGG_EFF_DM_CENTER': 2.2},
           {'AGG_EFF_RHO_100NM_CENTER': 450, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1.8, 'AGG_EFF_DM_CENTER': 2.2},
           {'AGG_EFF_RHO_100NM_CENTER': 450, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1, 'AGG_EFF_DM_CENTER': 2.5},
           {'AGG_EFF_RHO_100NM_CENTER': 450, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1.4, 'AGG_EFF_DM_CENTER': 2.5},
           {'AGG_EFF_RHO_100NM_CENTER': 450, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1.8, 'AGG_EFF_DM_CENTER': 2.5},
           {'AGG_EFF_RHO_100NM_CENTER': 450, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1, 'AGG_EFF_DM_CENTER': 2.8},
           {'AGG_EFF_RHO_100NM_CENTER': 450, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1.4, 'AGG_EFF_DM_CENTER': 2.8},
           {'AGG_EFF_RHO_100NM_CENTER': 450, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1.8, 'AGG_EFF_DM_CENTER': 2.8},
           {'AGG_EFF_RHO_100NM_CENTER': 550, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1, 'AGG_EFF_DM_CENTER': 2.2},
           {'AGG_EFF_RHO_100NM_CENTER': 550, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1.4, 'AGG_EFF_DM_CENTER': 2.2},
           {'AGG_EFF_RHO_100NM_CENTER': 550, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1.8, 'AGG_EFF_DM_CENTER': 2.2},
           {'AGG_EFF_RHO_100NM_CENTER': 550, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1, 'AGG_EFF_DM_CENTER': 2.5},
           {'AGG_EFF_RHO_100NM_CENTER': 550, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1.4, 'AGG_EFF_DM_CENTER': 2.5},
           {'AGG_EFF_RHO_100NM_CENTER': 550, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1.8, 'AGG_EFF_DM_CENTER': 2.5},
           {'AGG_EFF_RHO_100NM_CENTER': 550, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1, 'AGG_EFF_DM_CENTER': 2.8},
           {'AGG_EFF_RHO_100NM_CENTER': 550, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1.4, 'AGG_EFF_DM_CENTER': 2.8},
           {'AGG_EFF_RHO_100NM_CENTER': 550, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1.8, 'AGG_EFF_DM_CENTER': 2.8},
           {'AGG_EFF_RHO_100NM_CENTER': 650, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1, 'AGG_EFF_DM_CENTER': 2.2},
           {'AGG_EFF_RHO_100NM_CENTER': 650, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1.4, 'AGG_EFF_DM_CENTER': 2.2},
           {'AGG_EFF_RHO_100NM_CENTER': 650, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1.8, 'AGG_EFF_DM_CENTER': 2.2},
           {'AGG_EFF_RHO_100NM_CENTER': 650, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1, 'AGG_EFF_DM_CENTER': 2.5},
           {'AGG_EFF_RHO_100NM_CENTER': 650, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1.4, 'AGG_EFF_DM_CENTER': 2.5},
           {'AGG_EFF_RHO_100NM_CENTER': 650, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1.8, 'AGG_EFF_DM_CENTER': 2.5},
           {'AGG_EFF_RHO_100NM_CENTER': 650, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1, 'AGG_EFF_DM_CENTER': 2.8},
           {'AGG_EFF_RHO_100NM_CENTER': 650, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1.4, 'AGG_EFF_DM_CENTER': 2.8},
           {'AGG_EFF_RHO_100NM_CENTER': 650, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1.8, 'AGG_EFF_DM_CENTER': 2.8},
           ]
    '''
    arr = [{'AGG_EFF_RHO_100NM_CENTER': 502, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1, 'AGG_EFF_DM_CENTER': 2.56},
           {'AGG_EFF_RHO_100NM_CENTER': 502, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1.4, 'AGG_EFF_DM_CENTER': 2.56},
           {'AGG_EFF_RHO_100NM_CENTER': 502, 'AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER': 1.8, 'AGG_EFF_DM_CENTER': 2.56}]
    '''
    for i in arr:
        for key in i:
            AGG_Info[key] = i[key]
        RTC02 = K02.KeyhanV1(AGG_Info)
        RTC02.KeyhanV1Calc(DB_Info)

    ################################################################################################################
    logging.info("App finished.")
    A = 51
