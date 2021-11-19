from itertools import takewhile
from eunjeon import Mecab
import queue
from jamo import h2j, j2hcj
import numpy as np
import re
import json
import sys

global script_table
global voice_table

script_table = []
voice_table = []

def main(ans,speak):
    global script_table
    global voice_table

    
    mecab = Mecab()

    script_table = [] # 정답 예문
    voice_table = [] # speech recognition으로 받은 문장
    falseWord = {} 
    totalcount = 0 # 총 형태소 수?
    falsecount = 0 # 틀린 형태소 수?
    percent = 0.00

    script_table = mecab.morphs(ans)
    # print("\nscript_table =", end=" ")
    # print(script_table)
    voice_table = mecab.morphs(speak)
    # print("voice_table =", end=" ")
    # print(voice_table)
    #print(len(voice_table))
    
    # 비교 쉽게 하기 위해 형식 맞추기 
    if len(voice_table)!=len(script_table):
        reconstruct()

    # 각 테이블 비교해 틀린 부분 추출
    for i in range(len(voice_table)):
        totalcount += 1 
        if(voice_table[i]!=script_table[i]):
            temp = []
            for j in range(len(voice_table[i])):
                if voice_table[i][j] != script_table[i][j]:
                    temp.append(voice_table[i][j])
                    falsecount += 1
            falseWord[voice_table[i]] = temp
    
    # print(falseWord)

    percent = (totalcount - falsecount)/totalcount * 100

    data = {  # Json으로 넘길 data 생성
        'script_table': script_table, # 예문 형태소 분석 결과 
        'voice_table': voice_table, # 사용자가 말한 문장 형태소 분석 결과
        'false':falseWord, # 틀린 부분 "틀린 형태소": "틀린 글자"
        'percent' : percent # 정확도
    }

    print(json.dumps(data))

# script_table과 형식 맞추기
def reconstruct():
    s_idx = 0 # script_table 인덱스
    v_idx =0 # voice_table 인덱스

    while needReconstruct(v_idx, s_idx):
        if len(script_table[s_idx])>len(voice_table[v_idx]): # voice가 더 쪼개짐 ex) script[idx]= '해외여행' voice[idx] = '해외'
            diff = len(script_table[s_idx])-len(voice_table[v_idx])
            #print("diff = " + str(diff))
            while diff>0:
                if len(voice_table[v_idx+1]) >= diff:
                    voice_table[v_idx] = voice_table[v_idx]+voice_table[v_idx+1][0:diff]
                    voice_table[v_idx+1] = voice_table[v_idx+1][diff:]
                    if(voice_table[v_idx+1]==''):
                        del voice_table[v_idx+1]
                        v_idx+=1
                        diff = 0
                else:
                    voice_table[v_idx] += voice_table[v_idx+1][0:]
                    diff -= len(voice_table[v_idx+1])
                    del voice_table[v_idx+1]
            #print(voice_table)
            #print("i = "+str(i))
            s_idx +=1
        elif len(script_table[s_idx])<len(voice_table[v_idx]): # voice가 덜 쪼개짐 ex) script[idx]= '해외' voice[idx] = '해외여행'
            #print(str(i)+"번째 요소를 다시 쪼갭니다")
            diff = len(voice_table[v_idx])- len(script_table[s_idx])
            voice_table.insert(v_idx+1,voice_table[v_idx][0:diff])
            voice_table.insert(v_idx+2,voice_table[v_idx][diff:])
            del voice_table[v_idx]
            s_idx+=1
            v_idx+=1
                #print(voice_table)
                    
                
def needReconstruct(v_idx, s_idx):
    # 적당히 틀린 경우 여기서 걸러 낼 수 있음
    # ex) "[해외여행] 처음 가는 거 티 내네. 하긴 나도 그랬었지." - "[해외][요][형] 처음 가는 거 티 내네. 하긴 내도 그랬었지."
    for i in range(len(voice_table)):
        if(len(voice_table[i])!=len(script_table[i])):
            return True

    # 형식 다 맞췄는데 길이 다름 
    # 그렇구나 우리 그룹 과제 같이 하자 - 그렇구나 (차이가 크게 나는 경우)
    if(len(voice_table)!=len(script_table)): 
        return False

    return False

if __name__=="__main__":
    main(sys.argv[1], sys.argv[2]) # argv[1]: 예문,  argv[2]: 연습


