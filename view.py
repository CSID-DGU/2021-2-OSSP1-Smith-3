from itertools import takewhile
from eunjeon import Mecab
import queue
from jamo import h2j, j2hcj
import numpy as np
import re
import json
import sys

from pkg_resources import VersionConflict

global script_table
global voice_table
global s_idx
global v_idx
script_table = []
voice_table = []

def main(ans,speak):
    global script_table
    global voice_table
    
    ans = remove_marks(ans)
    speak = remove_marks(speak)
    mecab = Mecab()

    script_table = [] # 정답 예문
    voice_table = [] # speech recognition으로 받은 문장
    falseWord = {} 
    totalcount = len(ans.replace(" ","")) # 총 글자 수
    falsecount = 0 # 틀린 글자 수
    percent = 0.00

    # 형태소 분석
    script_table = mecab.morphs(ans)
    voice_table = mecab.morphs(speak)
    
    # 형태소 분석 결과 비교 위한 형식 맞추기 
    reconstruct()

    # 각 테이블 비교해 틀린 부분 추출
    for voice, script in zip(voice_table,script_table):
        if voice != script:
            tmp = []
            for v,s in zip(voice, script):
                if v!=s:
                    tmp.append(v)
                    falsecount += 1
            falseWord[voice] = tmp
    
    # 말하다 만 경우 예문의 나머지 부분 false count
    if len(voice_table) < len(script_table):
        for script in script_table[len(voice_table):]:
            falsecount += len(script)

    # 정확도 계산
    percent = round((totalcount - falsecount)/totalcount * 100,2)

    data = {  # Json으로 넘길 data 생성
        'script_table': script_table, # 예문 형태소 분석 결과 
        'voice_table': voice_table, # 사용자가 말한 문장 형태소 분석 결과
        'false':falseWord, # 틀린 부분 "틀린 형태소": "틀린 글자"
        'percent' : percent # 정확도
    }

    print(json.dumps(data))

# script_table과 형식 맞추기
def reconstruct():
    global s_idx
    global v_idx

    s_idx = 0 # script_table 인덱스
    v_idx =0 # voice_table 인덱스

    while needReconstruct():
        # voice가 더 쪼개짐 ex) script[idx]= '해외여행' voice[idx] = '해외'
        if len(script_table[s_idx])>len(voice_table[v_idx]): 
            diff = len(script_table[s_idx])-len(voice_table[v_idx])
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
            s_idx +=1
        # voice가 덜 쪼개짐 ex) script[idx]= '해외' voice[idx] = '해외여행'
        elif len(script_table[s_idx]) < len(voice_table[v_idx]): 
            voice_table.insert(v_idx+1,voice_table[v_idx][:len(script_table[s_idx])])
            voice_table.insert(v_idx+2,voice_table[v_idx][len(script_table[s_idx]):])
            del voice_table[v_idx]
            s_idx+=1
            v_idx+=1
                    
                
def needReconstruct():
    global s_idx
    global v_idx

    tmp = 0
    for voice, script in zip(voice_table[v_idx:],script_table[s_idx:]):
        if(len(voice)!=len(script)):
            v_idx += tmp
            s_idx += tmp
            return True
        tmp += 1;

    return False

def remove_marks(string): # 특수문자(마침표 포함) 제거 함수
    return re.sub('[.-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', string)

if __name__=="__main__":
    main(sys.argv[1], sys.argv[2]) # argv[1]: 예문,  argv[2]: 연습