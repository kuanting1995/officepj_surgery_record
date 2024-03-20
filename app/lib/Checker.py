import collections
import  re


def isNone(value) :
    if(value is None):
        return True

    if type(value) == dict :
        return len(value) == 0 

    if type(value) == str :
        return len(value) == 0

    if type(value) == list :
        return len(value) == 0  

    if type(value) == set :
        return len(value) == 0  

    if type(value) == tuple :
        return len(value) == 0  

    return False

def isExist(d, key) :

    if(isNone(d) or isNone(key)):
        return False 

    if (type(d) == dict) :
        return (key in d) 

    if (type(d) == collections.OrderedDict):
        return (key in d) 

    if type(d) == set :
        return  (key in d)  

    if type(d) == list :
        return  (key in d) 
    
    if type(d) == tuple :
        return (key in d)

    return False

def isNotNone(value) :
    return not isNone(value)

def isNotExist(d, key) :
    return not isExist(d, key)





#*******************************************************************************
#* Copyright (c) 2020 
#* https://github.com/doggy8088/taiwan-id-validator2#readme
#*******************************************************************************/
def isValidIDorRCNumber(idno) :
    #return __isValidIDorRCNumber(idno)
    return isNationalIdentificationNumberValid(idno) or isResidentCertificateNumberValid(idno)

def parseInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
#
#  Verify the input is a valid National identification number (中華民國身分證字號)
#  A=10 台北市     J=18 新竹縣     S=26 高雄縣
#  B=11 台中市     K=19 苗栗縣     T=27 屏東縣
#  C=12 基隆市     L=20 台中縣     U=28 花蓮縣
#  D=13 台南市     M=21 南投縣     V=29 台東縣
#  E=14 高雄市     N=22 彰化縣     W=32 金門縣*
#  F=15 台北縣     O=35 新竹市*    X=30 澎湖縣
#  G=16 宜蘭縣     P=23 雲林縣     Y=31 陽明山
#  H=17 桃園縣     Q=24 嘉義縣     Z=33 連江縣*
#  I=34 嘉義市*    R=25 台南縣
#
#  Step 1: 英文字母按照上表轉換為數字之後，十位數 * 1 + 個位數 * 9 相加
#  Step 2: 第 1 位數字 (只能為 1 or 2) 至第 8 位數字分別乘上 8, 7, 6, 5, 4, 3, 2, 1 後相加，再加上第 9 位數字
#  Step 3: 如果該數字為 10 的倍數，則為正確身分證字號
# @param { string } input National identification number
# @returns { boolean }
#
def isNationalIdentificationNumberValid(idno) -> bool :
    if(isNone(idno)):
        return False
    
    idno = idno.upper() # 轉換大寫

    if (not re.match('[A-Z]{1}[1,2,8,9]{1}[0-9]{8}', idno)):
        return False 

    return __verifyTaiwanIdIntermediateString(idno)


#
#  Verify the input is a valid Resident certificate number (外僑及大陸人士在台居留證、旅行證統一證號)
#  A=10 台北市     J=18 新竹縣     S=26 高雄縣
#  B=11 台中市     K=19 苗栗縣     T=27 屏東縣
#  C=12 基隆市     L=20 台中縣     U=28 花蓮縣
#  D=13 台南市     M=21 南投縣     V=29 台東縣
#  E=14 高雄市     N=22 彰化縣     W=32 金門縣*
#  F=15 台北縣     O=35 新竹市*    X=30 澎湖縣
#  G=16 宜蘭縣     P=23 雲林縣     Y=31 陽明山
#  H=17 桃園縣     Q=24 嘉義縣     Z=33 連江縣*
#  I=34 嘉義市*    R=25 台南縣
#
#  Step 1: 第一位英文字母按照上表轉換為數字之後，十位數 * 1 + 個位數 * 9 相加，第二位英文字母按上表轉換為對應數值的個位數
#  Step 2: 第 1 位數字 (由第二位英文所轉換) 至第 8 位數字分別乘上 8, 7, 6, 5, 4, 3, 2, 1 後相加，再加上第 9 位數字
#  Step 3: 如果該數字為 10 的倍數，則為正確居留證號
# @param { string } input Resident certificate number
# @returns { boolean }
#
def isResidentCertificateNumberValid(idno) -> bool :
    if(isNone(idno)):
        return False
    
    idno = idno.upper() # 轉換大寫

    if (not re.match('[A-Z]{1}[A-D]{1}[0-9]{8}', idno)):
        return False 

    return __verifyTaiwanIdIntermediateString(idno)

#
# Verify the intermediate string for isNationalIdentificationNumberValid and isResidentCertificateNumberValid
# @param { string } input String to verify
# @returns { boolean }
#

def __verifyTaiwanIdIntermediateString(idno) -> bool :
    idno = idno.upper() # 轉換大寫
    idArray = list(idno) # 字串轉成char陣列
    intRadix = 10
    TAIWAN_ID_LOCALE_CODE_LIST = [
        1,  # A -> 10 -> 1 * 1 + 9 * 0 = 1
        10, # B -> 11 -> 1 * 1 + 9 * 1 = 10
        19, # C -> 12 -> 1 * 1 + 9 * 2 = 19
        28, # D
        37, # E
        46, # F
        55, # G
        64, # H
        39, # I -> 34 -> 1 * 3 + 9 * 4 = 39
        73, # J
        82, # K
        2,  # L
        11, # M
        20, # N
        48, # O -> 35 -> 1 * 3 + 9 * 5 = 48
        29, # P
        38, # Q
        47, # R
        56, # S
        65, # T
        74, # U
        83, # V
        21, # W -> 32 -> 1 * 3 + 9 * 2 = 21
        3,  # X
        12, # Y
        30  # Z -> 33 -> 1 * 3 + 9 * 3 = 30
    ]

    RESIDENT_CERTIFICATE_NUMBER_LIST = [
        '0', # A
        '1', # B
        '2', # C
        '3', # D
        '4', # E
        '5', # F
        '6', # G
        '7', # H
        '4', # I
        '8', # J
        '9', # K
        '0', # L
        '1', # M
        '2', # N
        '5', # O
        '3', # P
        '4', # Q
        '5', # R
        '6', # S
        '7', # T
        '8', # U
        '9', # V
        '2', # W
        '0', # X
        '1', # Y
        '3'  # Z
    ]


    if not parseInt(idArray[1]):
        idArray[1] =RESIDENT_CERTIFICATE_NUMBER_LIST[ord(idArray[1] ) - ord('A')]

    result = 0
    for i in range(len(idArray)):
        if(i==0):
            result = result + TAIWAN_ID_LOCALE_CODE_LIST[ord(idArray[0]) - ord('A')]
        elif(i==9):
            result = result + int(idArray[9])
        else:
            result = result + int(idArray[i]) * (9-i)



    if (result % 10 == 0):
        return True

    return False


TWPHONE_REGEX = re.compile(r"^09\d{2}(\d{6}|-\d{3}-\d{3})$")

#
# Verify the Taiwan cellphone number string 
# @param { string } input String to verify
# 
#
def isTWCellPhoneNumberValid(no) -> bool :
    if(isNone(no)):
        return False

    if(isNone(no.strip())):
        return False

    if not TWPHONE_REGEX.match(no):
        return False

    return True


EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

#
# Verify the Email string 
# @param { string } input String to verify
# 
#
def isEmailValid(mail) -> bool :
    if(isNone(mail)):
        return False

    if(isNone(mail.strip())):
        return False

    if not EMAIL_REGEX.match(mail):
        return False

    return True
   

def is8Num(no):
    if no is None:
        return False
    if not re.match('^[0-9]{8}', no):
        return False
    
    return True

def is4Num(no):
    if no is None:
        return False
    if not re.match('^[0-9]{4}', no):
        return False
    
    return True