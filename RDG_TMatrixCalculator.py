# Keyhan Babaee, https://github.com/KeyhanB
# V1.2
# Aug 2019
from ConfigParserModule import logging
from math import *
import numpy as np
import AppFunctions as FN
from BoundaryFinder import BCDBBoundaryCheck as BCheck
from decimal import Decimal
from TMatrix import TMatrixCalculation
from FSAC_RDG import RDGCalculation
import pandas as pd
import GeneralFunctions as GF
import gmpy2
from scipy.ndimage import gaussian_filter1d


class KeyhanV1:
    def __init__(self, inputDict):
        try:
            ######################################################################################
            time_now = GF.getDateandTimeUTCNow()
            temp = {}
            temp['AA_FileName'] = f"TR_{time_now}.csv"
            temp['AA_Plot'] = 1
            self.infoDict = {**temp, **inputDict}
            ######################################################################################
            self.__AGG_EFF_DM_CENTER = inputDict['AGG_EFF_DM_CENTER']
            self.__AGG_EFF_RHO_100NM_CENTER = inputDict['AGG_EFF_RHO_100NM_CENTER']
            self.__AGG_MATERIAL_DENSITY_CENTER = inputDict['AGG_MATERIAL_DENSITY_CENTER']
            self.__AGG_MOBILITY_DIAMETER_CENTER_MAX = inputDict['AGG_MOBILITY_DIAMETER_CENTER_MAX']
            self.__AGG_MOBILITY_DIAMETER_CENTER_MIN = inputDict['AGG_MOBILITY_DIAMETER_CENTER_MIN']
            self.__AGG_PREFACTOR_PROJECTED_AREA_COEFFICIENT_CENTER = inputDict['AGG_PREFACTOR_PROJECTED_AREA_COEFFICIENT_CENTER']
            self.__AGG_EXPONENT_PROJECTED_AREA_COEFFICIENT_CENTER = inputDict['AGG_EXPONENT_PROJECTED_AREA_COEFFICIENT_CENTER']
            self.__AGG_FRACTAL_DIMENSION_CENTER = inputDict['AGG_FRACTAL_DIMENSION_CENTER']
            self.__AGG_FRACTAL_PREFACTOR_CENTER = inputDict['AGG_FRACTAL_PREFACTOR_CENTER']
            self.__AGG_RI_REAL_CENTER = inputDict['AGG_RI_REAL_CENTER']
            self.__AGG_RI_IMAG_CENTER = inputDict['AGG_RI_IMAG_CENTER']
            self.__AGG_WLENGTH_CENTER = inputDict['AGG_WLENGTH_CENTER']
            self.__AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER = inputDict['AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER']
            ######################################################################################
            self.__Sample_Sigma_Bins = 59  # Number of bins
            self.__Primary_Sigma_dm_CTE_Bound = 3  # Number of Sigma G to cover
            self.__Primary_Sigma_dm_CTE_Nt = 48  # Number of bins
            self.infoDict['MobilityBins'] = self.__Sample_Sigma_Bins
            self.infoDict['NumberOfSigma'] = self.__Primary_Sigma_dm_CTE_Bound
            self.infoDict['PrimaryBins'] = self.__Primary_Sigma_dm_CTE_Nt

        except Exception as e:
            logging.exception(e)
            raise

    def KeyhanV1Calc(self, DB_Info):
        try:
            self.arrMobilityDiamNano = self.CalcMobilityDiamBins()
            self.dict_dpMedianNano = self.CalcPrimaryParticleSizeMedianNano()
            self.dict_dpMobDistribNano, self.dict_dpMobDistribChance = self.CalcPrimDiamBinAtEachMob()
            self.dict_NpMobDistrib = self.CalcPrimaryParticleNumber()
            dictSuggested = self.CreateDictForEvaluation()
            dictChecked = self.CheckDictWithBoundary(dict=dictSuggested)
            dictConverted = self.ConvertDictToArray(dict=dictChecked)
            T1 = TMatrixCalculation(DBInfo=DB_Info)
            R1 = RDGCalculation()

            dictInputT1, dictOutputT1, dictInputR1, dictOutputR1 = {}, {}, {}, {}
            for dm in dictConverted:
                dictInputT1[dm], dictOutputT1[dm] = T1.TMatrixCalc(TMatrix_Planned_Input=dictConverted[dm])
                dictInputR1[dm], dictOutputR1[dm] = R1.RDGCalc(RDG_Planned_Input=dictConverted[dm])
                if dictInputT1[dm] != dictInputR1[dm]:
                    raise
                logging.info(f"Calculation for dm:{dm} was finished.")

            dfResult = self.CalcTotalCrossSection(outTMatrix=dictOutputT1, outRDG=dictOutputR1, checkedDict=dictChecked)

            dfInfoDB = pd.read_csv(f"TMatrix_RDG_Result\Beacon.csv")
            dfInfoDB.loc[len(dfInfoDB)] = self.infoDict
            # newInfoDf = pd.DataFrame([self.infoDict])
            # newInfoDf.to_csv(f"TMatrix_RDG_Result\Beacon.csv", index=False)
            dfInfoDB.to_csv(f"TMatrix_RDG_Result\Beacon.csv", index=False)
            dfResult.to_csv(f"TMatrix_RDG_Result\{self.infoDict['AA_FileName']}", index=False)

        except Exception as e:
            logging.exception(e)
            raise

    ######################################################################################
    ######################################################################################
    ######################################################################################
    ######################################################################################
    ######################################################################################
    ######################################################################################
    ######################################################################################

    def CalcTotalCrossSection(self, outTMatrix, outRDG, checkedDict):
        try:
            df = pd.DataFrame(columns=['dm', 'ABS_TMatrix', 'SCA_TMatrix', 'ABS_RDG', 'SCA_RDG',
                                       'NumberOfCalcs', 'dp_median', 'Np_Ave', 'dp_Ave',
                                       'D_TEM', 'dp_100nm',
                                       'RealErrorABS', 'RealErrorSCA', 'AbsoluteErrorABS', 'AbsoluteErrorSCA',
                                       'RealPercentErrorABS', 'AbsolutePercentErrorABS', 'RatioABS',
                                       'RealPercentErrorSCA', 'AbsolutePercentErrorSCA', 'RatioSCA',
                                       'SSA_TMatrix', 'SSA_RDG',
                                       'MAC_TMatrix', 'MSC_TMatrix', 'MAC_RDG', 'MSC_RDG', 'Agg_Mass_gr'])

            for dm in outTMatrix:

                Np_Ave = 0
                dp_Ave = 0
                ABS_TMatrix = 0
                SCA_TMatrix = 0
                ABS_RDG = 0
                SCA_RDG = 0
                AggregateMass = 0

                for i in range(len(outTMatrix[dm])):
                    ABS_TMatrix += outTMatrix[dm][i][0] * checkedDict[dm]['chance'][i]
                    SCA_TMatrix += outTMatrix[dm][i][1] * checkedDict[dm]['chance'][i]
                    ABS_RDG += outRDG[dm][i][0] * checkedDict[dm]['chance'][i]
                    SCA_RDG += outRDG[dm][i][1] * checkedDict[dm]['chance'][i]
                    Np_Ave += checkedDict[dm]['Np'][i] * checkedDict[dm]['chance'][i]
                    dp_Ave += checkedDict[dm]['dp'][i] * checkedDict[dm]['chance'][i]
                    AggregateMass += self._convertDensityToMass(dp=checkedDict[dm]['dp'][i], density=self.__AGG_MATERIAL_DENSITY_CENTER, Np=checkedDict[dm]['Np'][i]) * checkedDict[dm]['chance'][i]
                ################################################
                ################################################
                ################################################ MAC and MSC
                if AggregateMass != 0:
                    MAC_TMatrix = ABS_TMatrix * (Decimal(10) ** (Decimal(-12))) / AggregateMass
                    MSC_TMatrix = SCA_TMatrix * (Decimal(10) ** (Decimal(-12))) / AggregateMass
                    MAC_RDG = ABS_RDG * (Decimal(10) ** (Decimal(-12))) / AggregateMass
                    MSC_RDG = SCA_RDG * (Decimal(10) ** (Decimal(-12))) / AggregateMass

                else:
                    MAC_TMatrix = 0
                    MSC_TMatrix = 0
                    MAC_RDG = 0
                    MSC_RDG = 0

                errorRealABS = ABS_TMatrix - ABS_RDG
                errorRealSCA = SCA_TMatrix - SCA_RDG
                errorAbsoluteABS = abs(ABS_TMatrix - ABS_RDG)
                errorAbsoluteSCA = abs(SCA_TMatrix - SCA_RDG)
                ################################################
                ################################################
                ################################################ SSA
                if (ABS_TMatrix + SCA_TMatrix) != 0:
                    SSA_TMatrix = SCA_TMatrix / (ABS_TMatrix + SCA_TMatrix)
                else:
                    SSA_TMatrix = 0

                if (ABS_RDG + SCA_RDG) != 0:
                    SSA_RDG = SCA_RDG / (ABS_RDG + SCA_RDG)
                else:
                    SSA_RDG = 0
                ################################################
                ################################################
                ################################################ Error percenet and ratio
                if ABS_RDG != 0:
                    errorRealPercentABS = 100 * (ABS_TMatrix - ABS_RDG) / ABS_RDG
                    errorAbsolutePercentABS = 100 * abs(ABS_TMatrix - ABS_RDG) / ABS_RDG
                    ratioABS = ABS_TMatrix / ABS_RDG
                else:
                    errorRealPercentABS = 0
                    errorAbsolutePercentABS = 0
                    ratioABS = 0

                if SCA_RDG != 0:
                    errorRealPercentSCA = 100 * (SCA_TMatrix - SCA_RDG) / SCA_RDG
                    errorAbsolutePercentSCA = 100 * abs(SCA_TMatrix - SCA_RDG) / SCA_RDG
                    ratioSCA = SCA_TMatrix / SCA_RDG
                else:
                    errorRealPercentSCA = 0
                    errorAbsolutePercentSCA = 0
                    ratioSCA = 0
                ################################################
                ################################################
                ################################################
                df.loc[len(df)] = {'dm': dm, 'ABS_TMatrix': ABS_TMatrix, 'SCA_TMatrix': SCA_TMatrix,
                                   'ABS_RDG': ABS_RDG, 'SCA_RDG': SCA_RDG, 'NumberOfCalcs': len(outTMatrix[dm]),
                                   'dp_median': self.dict_dpMedianNano[dm], 'Np_Ave': Np_Ave, 'dp_Ave': dp_Ave,
                                   'RealErrorABS': errorRealABS, 'RealErrorSCA': errorRealSCA,
                                   'D_TEM': self.D_TEM, 'dp_100nm': self.dp100_nano,
                                   'AbsoluteErrorABS': errorAbsoluteABS, 'AbsoluteErrorSCA': errorAbsoluteSCA,
                                   'RealPercentErrorABS': errorRealPercentABS, 'AbsolutePercentErrorABS': errorAbsolutePercentABS, 'RatioABS': ratioABS,
                                   'RealPercentErrorSCA': errorRealPercentSCA, 'AbsolutePercentErrorSCA': errorAbsolutePercentSCA, 'RatioSCA': ratioSCA,
                                   'SSA_TMatrix': SSA_TMatrix, 'SSA_RDG': SSA_RDG,
                                   'MAC_TMatrix': MAC_TMatrix, 'MSC_TMatrix': MSC_TMatrix, 'MAC_RDG': MAC_RDG, 'MSC_RDG': MSC_RDG,
                                   'Agg_Mass_gr': AggregateMass}
            return df
        except Exception as e:
            logging.exception(e)
            raise

    def ConvertDictToArray(self, dict):
        try:
            conDict = {}
            for dm in dict:
                L = dict[dm]
                X = []
                for i in range(len(L['Df'])):
                    S = []
                    S.append(L['Df'][i])
                    S.append(L['Kf'][i])
                    S.append(L['RI_Real'][i])
                    S.append(L['RI_Imag'][i])
                    S.append(L['wL'][i])
                    S.append(L['dp'][i])
                    S.append(L['Np'][i])
                    X.append(S)
                conDict[dm] = X
            return conDict

        except Exception as e:
            logging.exception(e)
            raise

    def CheckDictWithBoundary(self, dict):
        try:
            checked = {}
            for dm in dict:
                checking = BCheck()
                checked[dm] = checking.CheckInputDict(inputDict=dict[dm])
            return checked

        except Exception as e:
            logging.exception(e)
            raise

    def CalcPrimaryParticleNumber(self):
        try:
            dictNp = {}
            for dm in self.arrMobilityDiamNano:
                arrNp = []
                dpArr = self.dict_dpMobDistribNano[dm]
                for dp in dpArr:
                    arrNp.append(self._calcPPN(dm=dm, dp=dp))
                dictNp[dm] = arrNp
            return dictNp

        except Exception as e:
            logging.exception(e)
            raise

    def CreateDictForEvaluation(self):
        try:
            suggestedDict = {}
            for dm in self.arrMobilityDiamNano:
                if self.__AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER != 1:
                    pointNumber = self.__Primary_Sigma_dm_CTE_Nt
                else:
                    pointNumber = 1
                Df = FN.CreateConstantArray(Number=self.__AGG_FRACTAL_DIMENSION_CENTER, HowMany=pointNumber)
                kf = FN.CreateConstantArray(Number=self.__AGG_FRACTAL_PREFACTOR_CENTER, HowMany=pointNumber)
                RI_Real = FN.CreateConstantArray(Number=self.__AGG_RI_REAL_CENTER, HowMany=pointNumber)
                RI_Imag = FN.CreateConstantArray(Number=self.__AGG_RI_IMAG_CENTER, HowMany=pointNumber)
                wavelength = FN.CreateConstantArray(Number=self.__AGG_WLENGTH_CENTER, HowMany=pointNumber)
                S = {}
                S['Df'] = Df
                S['Kf'] = kf
                S['RI_Real'] = RI_Real
                S['RI_Imag'] = RI_Imag
                S['Np'] = self.dict_NpMobDistrib[dm]
                S['chance'] = self.dict_dpMobDistribChance[dm]
                S['wL'] = wavelength

                monometerParameter = []
                dpDecimal = []
                for dp in self.dict_dpMobDistribNano[dm]:
                    dpDecimal.append(round(Decimal(dp), 3))
                    monometerParameter.append(pi * dp / self.__AGG_WLENGTH_CENTER)
                S['dp'] = dpDecimal
                S['MP'] = monometerParameter
                suggestedDict[dm] = S

            return suggestedDict
        except Exception as e:
            logging.exception(e)
            raise

    def CalcMobilityDiamBins(self):
        try:
            bound_D_Max = self.__AGG_MOBILITY_DIAMETER_CENTER_MAX
            bound_D_Min = self.__AGG_MOBILITY_DIAMETER_CENTER_MIN
            total_Number_Bins = self.__Sample_Sigma_Bins
            diameter_Nano = []

            D_Ratio = (bound_D_Max / bound_D_Min) ** (1 / (total_Number_Bins - 1))

            for i in range(0, total_Number_Bins):
                d1 = bound_D_Min * (D_Ratio ** i)
                diameter_Nano.append(round(d1, 3))

            return sorted(diameter_Nano, key=float)

        except Exception as e:
            logging.exception(e)
            raise

    def CalcPrimDiamBinAtEachMob(self):
        try:
            primaryDiam = {}
            primaryChance = {}
            for dm in self.arrMobilityDiamNano:

                dpMedian = self.dict_dpMedianNano[dm]

                bound_D_Max = dpMedian * (self.__AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER ** self.__Primary_Sigma_dm_CTE_Bound)
                bound_D_Min = dpMedian * (self.__AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER ** (-1 * self.__Primary_Sigma_dm_CTE_Bound))
                total_Number_Bins = self.__Primary_Sigma_dm_CTE_Nt

                diameter_Nano = []
                logNormalPDF = []

                A = np.linspace(-1.2, 1.2, total_Number_Bins)
                B = []
                for i in A:
                    B.append(float(gmpy2.root(pow(i, 7), 5)))

                x_Down = dpMedian - bound_D_Min
                x_Up = bound_D_Max - dpMedian

                for i in range(len(B)):
                    if B[i] < 0:
                        diameter_Nano.append(dpMedian - x_Down * abs(B[i]))
                    if B[i] > 0:
                        diameter_Nano.append(dpMedian + x_Up * abs(B[i]))

                diameter_Nano = sorted(diameter_Nano, key=float)
                diameter_Nano = gaussian_filter1d(diameter_Nano, 8)
                diameter_Nano = diameter_Nano.tolist()

                sum = 0

                if self.__AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER != 1:
                    for i in range(0, total_Number_Bins):
                        if i != 0:
                            l1 = self._calcLogNDistribPDF(dpMedian, self.__AGG_POLYDISPERSITY_SIGMA_EACH_MOBILITY_CENTER, diameter_Nano[i], diameter_Nano[i - 1])
                        else:
                            l1 = 0
                        sum += l1
                        logNormalPDF.append(Decimal(l1))

                else:
                    diameter_Nano.append(dpMedian)
                    logNormalPDF.append(Decimal(1))

                primaryDiam[dm] = diameter_Nano
                primaryChance[dm] = logNormalPDF

            return primaryDiam, primaryChance

        except Exception as e:
            logging.exception(e)
            raise

    def CalcPrimaryParticleSizeMedianNano(self):
        try:
            self.dp100_nano = self._calcPrimaryDiameter100nm_nano()
            self.D_TEM = self._calc_D_TEM_From_EffDens_D_Alpha()
            self.infoDict['dp100_nano'] = self.dp100_nano
            self.infoDict['D_TEM'] = self.D_TEM
            dm_dp = self._calcPPSM()
            return dm_dp

        except Exception as e:
            logging.exception(e)
            raise

    def _calc_D_TEM_From_EffDens_D_Alpha(self):
        try:
            Primary_D_Alpha = self.__AGG_EXPONENT_PROJECTED_AREA_COEFFICIENT_CENTER
            Eff_Dm = self.__AGG_EFF_DM_CENTER

            D_TEM = (2 * Primary_D_Alpha - Eff_Dm) / (2 * Primary_D_Alpha - 3)
            return D_TEM

        except Exception as e:
            logging.exception(e)
            raise

    def _calcPrimaryDiameter100nm_nano(self):
        try:
            Eff_rho_100nm = self.__AGG_EFF_RHO_100NM_CENTER
            Primary_K_Alpha = self.__AGG_PREFACTOR_PROJECTED_AREA_COEFFICIENT_CENTER
            Soot_Material_Density = self.__AGG_MATERIAL_DENSITY_CENTER
            Primary_D_Alpha = self.__AGG_EXPONENT_PROJECTED_AREA_COEFFICIENT_CENTER

            K = ((Eff_rho_100nm / (Primary_K_Alpha * Soot_Material_Density)) ** (1 / (3 - 2 * Primary_D_Alpha))) * (100)
            return K

        except Exception as e:
            logging.exception(e)
            raise

    def _convertDensityToMass(self, dp, density, Np):
        try:
            V = (Decimal(10) ** (Decimal(-27))) * Decimal(pi) * (dp ** Decimal(3)) / Decimal(6)
            mass = Np * V * Decimal(density) * Decimal(1000)  # to gram
            return mass

        except Exception as e:
            logging.exception(e)
            raise

    def _calcPPN(self, dm, dp):
        try:
            N = self.__AGG_PREFACTOR_PROJECTED_AREA_COEFFICIENT_CENTER * ((dm / dp) ** (2 * self.__AGG_EXPONENT_PROJECTED_AREA_COEFFICIENT_CENTER))
            return round(Decimal(N), 3)

        except Exception as e:
            logging.exception(e)
            raise

    def _calcPPSM(self):
        # Primary particle size for each mobility diameter
        try:
            dm_dp = {}
            for dm in self.arrMobilityDiamNano:
                dp = (self.dp100_nano * ((dm / 100) ** self.D_TEM))
                dm_dp[dm] = round(dp, 3)
            return dm_dp

        except Exception as e:
            logging.exception(e)
            raise

    def _calcLogNDistribPDF(self, median, sigmaG, D2, D1):  # return number between 0 to 1
        try:
            if sigmaG != 1:
                A = (1 / (log(sigmaG) * (2 * pi) ** 0.5)) * exp(-1 * (((log(D1) - log(median)) ** 2) / (2 * (log(sigmaG)) ** 2))) * (log(D2) - log(D1))
            elif sigmaG == 1:
                if D2 >= median and median > D1:
                    return 1
                else:
                    return 0

            return A

        except Exception as e:
            logging.exception(e)
            raise
