# -*- coding: utf-8 -*-
import re
import sys
import openpyxl
"""
    초성 중성 종성 분리 하기
	유니코드 한글은 0xAC00 으로부터
	초성 19개, 중성21개, 종성28개로 이루어지고
	이들을 조합한 11,172개의 문자를 갖는다.
	한글코드의 값 = ((초성 * 21) + 중성) * 28 + 종성 + 0xAC00
	(0xAC00은 'ㄱ'의 코드값)
	따라서 다음과 같은 계산 식이 구해진다.
	유니코드 한글 문자 코드 값이 X일 때,
	초성 = ((X - 0xAC00) / 28) / 21
	중성 = ((X - 0xAC00) / 28) % 21
	종성 = (X - 0xAC00) % 28
	이 때 초성, 중성, 종성의 값은 각 소리 글자의 코드값이 아니라
	이들이 각각 몇 번째 문자인가를 나타내기 때문에 다음과 같이 다시 처리한다.
	초성문자코드 = 초성 + 0x1100 //('ㄱ')
	중성문자코드 = 중성 + 0x1161 // ('ㅏ')
	종성문자코드 = 종성 + 0x11A8 - 1 // (종성이 없는 경우가 있으므로 1을 뺌)
    https://github.com/neotune/python-korean-handler/blob/master/korean_handler.py

    위 코드에 기반하여 입력한 텍스트의 자모를 분리하고, 이를 엑셀 파일로 저장하도록 수정하였습니다.
        
"""
# 유니코드 한글 시작 : 44032, 끝 : 55199
BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']

# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

def convert(test_keyword):
    #xlsx 파일로 저장시
    workbook = openpyxl.load_workbook('result.xlsx')
    sheet = workbook.active
    #txt파일로 저장시
    #f = open("result.txt",'a')
    #f.writelines("입력값 : "+test_keyword+"\n결과 : ")
    split_keyword_list = list(test_keyword)
    #print(split_keyword_list)
    
    result = list()
    for keyword in split_keyword_list:
        # 한글 여부 check 후 분리
        if re.match('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', keyword) is not None:
            char_code = ord(keyword) - BASE_CODE
            char1 = int(char_code / CHOSUNG)
            if char1 == 1:
                result.append('ㄱ')
                result.append('ㄱ')
            elif char1 == 4:
                result.append('ㄷ')
                result.append('ㄷ')
            elif char1 == 8:
                result.append('ㅂ')
                result.append('ㅂ')
            elif char1 == 10:
                result.append('ㅅ')
                result.append('ㅅ')
            elif char1 == 13:
                result.append('ㅈ')
                result.append('ㅈ')
            else:
                result.append(CHOSUNG_LIST[char1])
            #f.writelines("테스트 초성 :"+char1)
            
            #print('초성 : {}'.format(CHOSUNG_LIST[char1]))
            char2 = int((char_code - (CHOSUNG * char1)) / JUNGSUNG)  
            if char2 == 1:
                result.append('ㅏ')
                result.append('ㅣ')
            elif char2 == 3:
                result.append('ㅑ')
                result.append('ㅣ')
            elif char2 == 5:
                result.append('ㅓ')
                result.append('ㅣ')
            elif char2 == 7:
                result.append('ㅕ')
                result.append('ㅣ')
            elif char2 == 9:
                result.append('ㅗ')
                result.append('ㅏ')
            elif char2 == 10:
                result.append('ㅗ')
                result.append('ㅏ')
                result.append('ㅣ')
            elif char2 == 11:
                result.append('ㅗ')
                result.append('ㅣ')
            elif char2 == 14:
                result.append('ㅜ')
                result.append('ㅓ')
            elif char2 == 15:
                result.append('ㅜ')
                result.append('ㅓ')
                result.append('ㅣ')
            elif char2 == 16:
                result.append('ㅜ')
                result.append('ㅣ')
            elif char2 == 19:
                result.append('ㅡ')
                result.append('ㅣ')
            else:
                result.append(JUNGSUNG_LIST[char2])
            
            #print('중성 : {}'.format(JUNGSUNG_LIST[char2]))
            char3 = int((char_code - (CHOSUNG * char1) - (JUNGSUNG * char2)))
            if char3==0:
                result.append('')
            elif char3 == 2:
                result.append('ㄱ')
                result.append('ㄱ')
            elif char3 == 3:
                result.append('ㄱ')
                result.append('ㅅ')
            elif char3 == 5:
                result.append('ㄴ')
                result.append('ㅈ')
            elif char3 == 6:
                result.append('ㄴ')
                result.append('ㅎ')
            elif char3 == 9:
                result.append('ㄹ')
                result.append('ㄱ')
            elif char3 == 10:
                result.append('ㄹ')
                result.append('ㅁ')
            elif char3 == 11:
                result.append('ㄹ')
                result.append('ㅂ')
            elif char3 == 12:
                result.append('ㄹ')
                result.append('ㅅ')
            elif char3 == 13:
                result.append('ㄹ')
                result.append('ㅌ')
            elif char3 == 14:
                result.append('ㄹ')
                result.append('ㅍ')
            elif char3 == 15:
                result.append('ㄹ')
                result.append('ㅎ')
            elif char3 == 18:
                result.append('ㅂ')
                result.append('ㅅ')
            elif char3 == 20:
                result.append('ㅅ')
                result.append('ㅅ')
            else:
                result.append(JONGSUNG_LIST[char3])
            #print('종성 : {}'.format(JONGSUNG_LIST[char3]))
        else:
            result.append(keyword)
            
    # result
    #print("".join(result))

    #결과 list에서 ''공백 문자열 없는 빈칸을 제거하는 구문
    result=list(filter(lambda x: x != '', result))

    #list를 문자열로 변환하여 테스트 값을 txt파일로 저장하는 구문
    #f.writelines(str(result)+"\n")
    #f.close()

    #xlsx파일로 구분된 자음,모음을 저장하는 구문
    sheet.append(result)
    workbook.save('result.xlsx')
    workbook.close()
if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        inputfile = open(sys.argv[1], 'r')
        for line in inputfile.readlines():
            convert(line)
    else:
        test_keyword = input("입력 :")
        convert(test_keyword)
