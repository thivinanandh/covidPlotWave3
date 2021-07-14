##Python script to generate shell files 

# import numpy as np 
import os
import sys


### Conmfirm the input entered by the User
def validate(value,string):
    print (string , " - ", value)
    ans = input(" Is this the correct Value for  " + string + ":  ?  [Yy/Nn]   ")
    if(ans == 'Y' or ans == 'y'):
        return True
    else:
        print(" Exiting Problem ")
        exit(0)



if __name__ == "__main__":

    Totalnodenumber  = int(sys.argv[1])
    validate(Totalnodenumber, "Total Nodes")

    fileName = []
    filePointers = []


    numProcess = 32;


     ## 1, -- KDP_nu
    KDP_nu_name=["CIR40" ,"CIR50"]
    KDP_nu=[0 ,1]

    ## 2,  --  KDP_w_sat_1  -- -
    KDP_w_sat_1_name=["0_33" ,"0_66" ,"1_00"]
    KDP_w_sat_1=[0.33, 0.66 ,1.00]

    ## 3,  --  KDP_w_sat_2  -- -
    KDP_w_sat_2_name=["ImmunEscp_Jul" ,"ImmunEscp_Sep", "ImmunEscp_Nov"]
    KDP_w_sat_2=[380, 442 ,503]

    ## 4,  --  KDP_g_1  -- -
    KDP_g_1_name=["0_33", "0_66" ,"1_00"]
    KDP_g_1=[0.33, 0.66, 1.00]

    ## 5,  --  KDP_g_2  -- -
    KDP_g_2_name=["ABW150Days" ,"ABW180Days"]
    KDP_g_2=[150 ,180]

    ## 6,  --  KDP_c_p  -- -
    KDP_c_p_name=["Vaccine_PresentRate", "Vaccine_BestWeekAvg", "Vaccine_TwicePresent"]
    KDP_c_p=[1 ,1.5, 2]

    KDP_lambda_name=["SD_RA","SD_RAR","SD_RARF"]
    KDP_lambda=[0,0.1,0.2]

    #####
    TotalExperiments = len(KDP_nu) * len(KDP_w_sat_1) * len(KDP_w_sat_2) * \
                        len(KDP_g_1) * len(KDP_g_2) * len(KDP_c_p) * \
                        len(KDP_lambda) 
    datfilename="covid19.inp"
    

    ## Generate fileNames and the basic Shell script
    for i in range(Totalnodenumber):
        name = "script_" + str(i) + ".sh"
        fileName.append(name)
        
        ## store them in file pointers
        f = open(name, "w")
        filePointers.append(f)

        ## write the basic bash shabang 
        f.writelines("""#!/bin/bash""" + "\n")
        

    currentWorkingDirectory = os.getcwd()

    iterNo = 0;

    print(" Total Expt : " , TotalExperiments)
    for i in range(len(KDP_nu)):
        for j in range(len(KDP_w_sat_1)):
            for k in range(len(KDP_w_sat_2)):
                for l in range(len(KDP_g_1_name)):
                    for m in range(len(KDP_g_2)):
                        for n in range(len(KDP_c_p)):
                            for o in range(len(KDP_lambda)):
                                folderName = KDP_nu_name[i] + "_" + KDP_w_sat_1_name[j] + "_" + KDP_w_sat_2_name[k] + "_" + \
                                            KDP_g_1_name[l] + "_" + KDP_g_2_name[m] + "_" + KDP_c_p_name[n] + "_" + \
                                            KDP_lambda_name[o]

                                
                                ### Identify the iteration number
                                ## iterno = [0,TotalIterations-1]
                                

                                ##Identify the batch number
                                Scriptperbatch = int(TotalExperiments/Totalnodenumber)
                                batchNo = int(iterNo/Scriptperbatch)

                                if(batchNo > Totalnodenumber - 1):
                                    batchNo = Totalnodenumber - 1

                                print("---------------- FOLDER NAME --------------")
                                print(" FOLDER : " , folderName , " ---------------")
                                print(" ITER : " , iterNo , " ---------------")
                                os.system("mkdir -p " + folderName)

                                #Copy all the files to the current directory
                                # print("""cp -r lib/""" + folderName)
                                os.system("""cp -r lib/ """ + folderName)
                                
                                # print("""cp *.dat *.PRM *.GEO *.exe *.inp *.sh *.csv """ + folderName)
                                os.system("""cp *.dat *.PRM *.GEO *.exe *.inp *.sh *.csv """ + folderName)
                
                                #Modify the existing dat file
                               
                                os.system("""sed -i "s/KDP_nu: .*/KDP_nu: """ +   str(KDP_nu[i]) +  """/g" """ + folderName + "/" + datfilename)
                                os.system("""sed -i "s/KDP_w_sat_1: .*/KDP_w_sat_1: """ +   str(KDP_w_sat_1[j]) +  """/g" """ + folderName + "/" + datfilename)
                                os.system("""sed -i "s/KDP_w_sat_2: .*/KDP_w_sat_2: """ +   str(KDP_w_sat_2[k]) +  """/g" """ + folderName + "/" + datfilename)
                                os.system("""sed -i "s/KDP_g_1: .*/KDP_g_1: """ +   str(KDP_g_1[l]) +  """/g" """ + folderName + "/" + datfilename)
                                os.system("""sed -i "s/KDP_g_2:.*/KDP_g_2:""" +   str(KDP_g_2[m]) +  """/g" """ + folderName + "/" + datfilename)
                                os.system("""sed -i "s/KDP_c_p: .*/KDP_c_p: """ +   str(KDP_c_p[n]) +  """/g" """ + folderName + "/" + datfilename)
                                os.system("""sed -i "s/KDP_lambda: .*/KDP_lambda: """ +   str(KDP_lambda[o]) +  """/g" """ + folderName + "/" + datfilename)


                                ### Generate the script 


                                filePointers[batchNo].writelines("# Iter No : " + str(iterNo) + "\n")
                                ## cd to the folderr directory
                                filePointers[batchNo].writelines("cd " + str(folderName) + "\n")
                                ## diosplay the current directory
                                filePointers[batchNo].writelines("""echo ${PWD##*/}""" + "\n")
                                ## Run the mpi script
                                filePointers[batchNo].writelines("mpirun -np " + str(numProcess) + " ./parmoon_2D_MPI.exe covid19.inp" + "\n") 
                                
                                ## return to original directory
                                filePointers[batchNo].writelines("cd " + str(currentWorkingDirectory) + "\n")

                                ## Empyty line to check the counters
                                filePointers[batchNo].writelines("""#XXXYYYZZZ""" + "\n")
                                
                                iterNo += 1;

                            
## close all the file pointers                            
for i in range(Totalnodenumber):
    filePointers[i].close()
