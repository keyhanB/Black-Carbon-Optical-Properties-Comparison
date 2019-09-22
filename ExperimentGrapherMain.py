# Graphing using existing data
Version = 0.1
# Aug 2019
import ConfigParserModule as CP
from ConfigParserModule import logging
import ComparisonGraphModule as GM

if __name__ == "__main__":
    CP.ReadLogConfig()
    logging.info("App Started.")
    FF_Info = CP.ReadConfigToDict(sectionName="FilesFoldersInfo")
    AGG_Info = CP.ReadConfigToDict(sectionName="AggregateDetails", convertParseTo='float', hasComment=True)
    logging.info("config retrieved.")
    ##############################################
    G1 = GM.GraphTools(FolderInfo=FF_Info)
    G1.Experiment_RDG_TMatrixComparisonGraphs(AGG_Info=AGG_Info)
    ################################################################################################################
    logging.info("App finished.")
    A = 51
