#!/bin/bash
# --------------------------------------------------------------------                                  
# Date Time       : 2020/02/15 下午 02:47:54
# Target Table    : *
# Script File     : ods_sors_imp.sh
# Programmer      : JESSEWEI
# Function        : Load flat file template script without wait file
# Remarks         :                                                
# ------------------     Revision History      -------------------------
# --   Seq. No.    DATE         By         REASON 
# ----- -------- ----------- ----------- -------------------------------
# ---                                                                   
# ----------------------------------------------------------------------
# - SAMPLE: ods_ora_imp 10.139.117.25 odsdb_user @WSXcde3$RFVbgt5 BNS  20191205 BA_ADDRESS E:\ODS\ods_batch_home\etl\ "|" 
# - SAMPLE: ods_ora_imp 10.139.117.25 odsdb_user @WSXcde3$RFVbgt5  c:\temp\etl\FILE\ 20180308 UPD UR_LOAN
# ----------------------------------------------------------------------
# 


# op/exp shared parameter
DW_HOST=$1
USERID=$2
PASSWORD=$3
DIR_BASE=$4
DATA_DT=$5
SRC_SYSNAME=$6

# exp only parameter
SRC_NAME=$7
"SRC_DELI=$8"

# imp only parameter
# "^DIR_SOURCE^{SRC_SYSNAME}/{SERVICE_ID}/{SRC_NAME}_^EDC^.D"
STG_SP_NAME=SQLEXT.STG_${SRC_NAME}_SP
ODS_SP_NAME=SQLEXT.ODS_${SRC_NAME}_SP
HIS_SP_NAME=SQLEXT.ODS_${SRC_NAME}_HIS_SP

LookForFile=${DIR_BASE}Source\${SRC_SYSNAME}\${SRC_NAME}_${DATA_DT}.D
ImportMsg=${DIR_BASE}MSG\${SRC_SYSNAME}\${SRC_NAME}_${DATA_DT}.msg
ErrorMsg=${DIR_BASE}MSG\${SRC_SYSNAME}\${SRC_NAME}_${DATA_DT}.log
TempFile=${DIR_BASE}DATA\${SRC_SYSNAME}\${SRC_NAME}.D
Archive=${DIR_BASE}ARCHIVE\${SRC_SYSNAME}\${SRC_NAME}_${DATA_DT}.D
ExportFile=${DIR_BASE}EXPORT\
CURRENT_STEP="JOB_STEP:INIT"


if [ -n ${SRC_DELI} ] 
then SRC_DELI=\|
fi


:ODS_CP2STG
CURRENT_STEP="JOB_STEP:ODS_CP2STG"
echo MOVE file, use copy when debug
echo MOVE /Y ${LookForFile} ${TempFile}
cp -f ${LookForFile} ${TempFile}


:ODS_TRUC
CURRENT_STEP="JOB_STEP:ODS_TRUC"

# echo sqlplus -s ${USERID}/${PASSWORD}@${DW_HOST}
# sqlplus -s ${USERID}/${PASSWORD}@${DW_HOST}<<END
# execute ${STG_SP_NAME};
# commit;
# END;


:ODS_IMP
# CURRENT_STEP="JOB_STEP:ODS_IMP" "-MOVE"
# echo sqlg_replacestr.py ${TempFile} ${TempFile}.utf8
mv -f ${TempFile} ${TempFile}.utf8

# # sqlg_replacestr.py ${TempFile} ${TempFile}.utf8
# if ${ERRORLEVEL} NEQ 0 goto ERR_STOP 

# SYSTEM alert for INTG file, contain binary inside
# dos2unix ${TempFile}.utf8

CURRENT_STEP="JOB_STEP:ODS_IMP" "-sqlldr"
echo "sqlldr userid=${USERID}/${PASSWORD}@${DW_HOST} control=${DIR_OUTPUT_STG}${TBL_NAME}.ctl bad=${DIR_MSG}${SRC_FILE_NAME}.bad log=${DIR_MSG}${SRC_FILE_NAME}.log""
sqlldr userid=${USERID}/${PASSWORD}@${DW_HOST} control=${DIR_OUTPUT_STG}${TBL_NAME}.ctl bad=${DIR_MSG}${SRC_FILE_NAME}.bad log=${DIR_MSG}${SRC_FILE_NAME}.log"



# skip error check first run ods in anyway
# if ${ERRORLEVEL} NEQ 0 goto ERR_STOP

:ODS_2ODS
CURRENT_STEP="JOB_STEP:ODS_2ODS"

# echo sqlplus -s ${USERID}/${PASSWORD}@${DW_HOST}
# sqlplus -s ${USERID}/${PASSWORD}@${DW_HOST} << END
# execute ${ODS_SP_NAME};
# commit;
# END;
# 

:ODS_END
# move ${LookForFile} ${Archive}
# echo archived Source file!
# exit 0
# 

:ODS_HIST
# CURRENT_STEP="JOB_STEP:ODS_HIST"
# echo sqlplus -s ${USERID}/${PASSWORD}@${DW_HOST}
# sqlplus -s ${USERID}/${PASSWORD}@${DW_HOST} << END
# execute ${HIS_SP_NAME};
# commit;
# END;
# exit 0


:ERR_STOP
# echo Fail import on ${CURRENT_STEP}
exit 0
