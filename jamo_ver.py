from itertools import takewhile
from eunjeon import Mecab
from hangul_utils import join_jamos
import queue
from jamo import h2j, j2hcj, get_jamo_class
import numpy as np
import re
import json
import sys

from pkg_resources import VersionConflict

global script_table
global voice_table
global false_table
script_table = []
voice_table = []


def mainjamo(ans, speak):
    global script_table
    global voice_table
    global false_table

    # ---------------------------------------------------
    # 예외 처리
    if len(speak) == 0:
        return
    # ---------------------------------------------------

    ans = remove_marks(ans).rstrip()
    speak = remove_marks(speak).rstrip()
    mecab = Mecab()

    '''
    json으로 보낼 데이터
    false_table = {
        '어절' :{
            '어절 내 인덱스' : 틀린 자모
        }
    }
    '''
    false_table = {}
    script_table = {}
    voice_table = {}
    voice_new = []
    false_new = {}
    totalcount = len(ans.replace(" ", ""))  # 총 글자 수
    truecount = 0  # 맞은 글자 수 설정
    percent = 0.00

    # print(j2hcj(h2j("밭이랑에")))
    # print(mecab.pos("밭이랑에"))
    #print(mecab.pos("밭이랑에 물이 고였다"))
    #print(mecab.pos("할아버지는 밭이랑 논이 많다"))

    # 어절 자르기
    for idx, key in enumerate(ans.split(' ')):
        script_table[idx] = {key: 0}

    for idx, key in enumerate(speak.split(' ')):
        voice_table[idx] = {key: []}
        voice_new.append(key)

    set_compare_pair()
    # print(script_table)
    # print(voice_table)

    # v_word = 사용자가 말한 단어
    # s_word = 비교할 script의 단어
    for v_idx, v_dict in enumerate(voice_table.values()):
        false_table[v_idx] = {}
        for v_word, s_words in v_dict.items():
            false_syllable = {}
            if s_words[0] == "UNKNOWN":
                # 다 틀림
                for v in split_syllable(h2j(v_word)):
                    false_syllable[join_jamos(v)] = []
                    false_syllable[join_jamos(v)].append(j2hcj(v[0]))
                    false_syllable[join_jamos(v)].append(j2hcj(v[1]))
                    if len(v) == 3:
                        false_syllable[join_jamos(v)].append(j2hcj(v[2]))
                false_table[v_idx][v_word] = false_syllable
            elif len(s_words) == 1:
                correct, false_syllable = compare_start(s_words[0], v_word, 0)
                if correct:
                    false_table[v_idx][v_word] = "correct"
                else:
                    false_table[v_idx][v_word] = false_syllable

            else:
                rest = len(v_word)
                skip = 0
                false_table[v_idx][v_word] = {}
                for s_word in s_words:
                    correct, false_syllable = compare_start(
                        s_word, v_word, skip)
                    skip += len(s_word)
                    if correct:
                        rest -= len(s_word)

                    if rest <= 0:
                        false_table[v_idx][v_word] = "correct"
                    else:
                        for key, val in false_syllable.items():
                            false_table[v_idx][v_word][key] = val

                    if skip >= len(v_word)-1:
                        break

            if not false_table[v_idx][v_word] == "correct":
                false_new[v_idx] = v_word

            if false_table[v_idx][v_word] == "correct":
                truecount += len(v_word)

    percent = round(truecount/totalcount * 100, 2)

    if percent > 100:
        percent = 100

    # for word, target in zip(script_table,voice_table):
    #     jamo_word = h2j(word)
    #     jamo_target = h2j(target)
    #     compare(jamo_word, jamo_target)

    data = {  # Json으로 넘길 data 생성
        'script_table': script_table,  # 예문 형태소 분석 결과
        'voice_table': voice_table,  # 사용자가 말한 문장 형태소 분석 결과
        'false_table': false_table,
        'voice_new': voice_new,
        'false_new': false_new,
        'percent': percent,
        'totalcount': totalcount,
        'truecount': truecount
    }

    print(json.dumps(data))


def set_compare_pair():
    global script_table
    global voice_table

    not_found_script = []
    not_found_voice = []

    # step 1 : 일치하는 어절
    #print("=== STEP 1 ... ========================")
    for s_idx, s_dict in enumerate(script_table.values()):
        key = list(s_dict)[0]
        for v_idx, v_dict in enumerate(voice_table.values()):
            if key in v_dict:
                if not abs(v_idx - s_idx) > len(script_table)//3:  # 너무 멀리 떨어져 있으면 다른 단어로 취급
                    script_table[s_idx][key] = 1
                    voice_table[v_idx][key].append(key)
                    break

    
    for s_idx, s_dict in enumerate(script_table.values()):
        for key in s_dict:
            if s_dict[key] != 1:
                not_found_script.append([key, s_idx])
    
            
    
    for v_idx, v_dict in enumerate(voice_table.values()):
        for key in v_dict:
            if len(v_dict[key]) == 0:
                not_found_voice.append([key, v_idx])

    # step 2: 비슷한 어절
    # print("=== STEP 2 ... ========================")
    # print(not_found_script)
    # print(not_found_voice)
    # print()
    """
    for s_idx, s_dict in enumerate(script_table.values()):
        key = list(s_dict)[0]
        for v in not_found_voice:
            v_idx=v[1]
            if (v[0] in s_dict or is_similar(key, v[0])) and not abs(v_idx - s_idx) > len(script_table)//3: # 너무 멀리 떨어져 있으면 다른 단어로 취급
                    script_table[s_idx][key] = 1
                    voice_table[v_idx][v[0]].append(key)
                    break
    """
    

    for v in not_found_voice:
        v_idx=v[1]
        for s in not_found_script:
            s_idx = s[1]
            if (v[0] in s[0] or is_similar(s[0], v[0])) and not abs(s_idx-v_idx) > len(script_table)//3:
                script_table[s_idx][s[0]]=1
                voice_table[v_idx][v[0]].append(s[0])
                break
    

    # 비교짝 못 찾은 단어 
    for v in not_found_voice:
        if len(voice_table[v[1]].get(v[0])) == 0:
            voice_table[v[1]].get(v[0]).append("UNKNOWN")


def is_similar(s_word, v_word):
    jamo_s = h2j(s_word)
    jamo_v = h2j(v_word)

    jamo_v = set(jamo_v)
    cnt = 0

    for v in jamo_v:
        if v in jamo_s:
            cnt += 1

    if cnt >= len(jamo_s)//2:
        return True

    return False

# word : 원본 단어
# target : 사용자 발음


def compare_start(word, target, skip):
    global false_table
    false_syllable = {}
    correct = True
    split_word = split_syllable(h2j(word))
    split_target = split_syllable(h2j(target[skip:]))
    start_idx_t = 0 
    start_idx_w = 0 
    
    if len(split_word)!= len(split_target):
        # 음절 포함된다면 인덱스 반환
        if join_jamos(word)[0] in join_jamos(target):
            start_idx_t = join_jamos(target).index(join_jamos(word)[0])
        elif join_jamos(target)[0] in join_jamos(word): 
            start_idx_w = join_jamos(word).index(join_jamos(target)[0])
        else:
            # 똑같은 초성 나오는 지점에서 시작
            for w in split_word:
                if split_target[0][0] == w[0]:
                    start_idx = split_word.index(w)
                    break;
        
    false_syllable = compare_syllable(split_target,split_word,start_idx_t, start_idx_w)

    # if(len(split_target)>len(split_word)):
    #     for t in split_target[len(split_word):]:
    #         false_syllable[split_target.index(t)] = []
    #         false_syllable[split_target.index(t)].append(j2hcj(t[0]))
    #         false_syllable[split_target.index(t)].append(j2hcj(t[1]))
    #         if len(t)==3 :
    #             false_syllable[split_target.index(t)].append(j2hcj(t[2]))

    # print(false_syllable)

    f_cnt = 0
    for f in false_syllable.values():
        if len(f) > 0:
            correct = False

    #correct = len(h2j(target)) - f_cnt
    # print(correct)
    return correct, false_syllable


def compare_syllable(split_target,split_word, start_idx_t, start_idx_w):
    false_syllable = {}
    liasion_flag = False
    palataliztion_flag = False

    split_target = split_target[start_idx_t:]
    split_word = split_word[start_idx_w:]
    #print(str(split_target)+"과 "+str(split_word)+"를 비교")

    for t,w in zip(split_target, split_word):
        key = join_jamos(t)
        false_syllable[key] = []

        if w[0] != t[0]:
            if not liasion_flag and not palataliztion_flag:
                #print("초성 틀림")
                false_syllable[key].append(j2hcj(t[0]))
        if w[1] != t[1]:
            if not vowel_pronunciation(w[1], t[1]):
                #print("중성 틀림")
                false_syllable[key].append(j2hcj(t[1]))

        if len(w) == 3 and len(t) == 2:  # w는 종성이 있고 t는 종성이 없음
            if split_word.index(w) < len(split_word)-1:
                next_t = split_target[split_target.index(t)+1]
                next_w = split_word[split_word.index(w)+1]
                if is_liasion(w[2], next_w, next_t):  # 연음 검사
                    liasion_flag = True
                elif is_palatalization(w[2], next_w, next_t):  # 구개음화 검사
                    palataliztion_flag = True
                else:
                    liasion_flag = False
                    palataliztion_flag = False
                    if len(false_syllable[key]) == 0:
                        false_syllable[key].append(j2hcj(t[0]))
                        false_syllable[key].append(j2hcj(t[1]))
        elif len(w) == 2 and len(t) == 3:  # w는 종성이 없고 t는 종성이 있음
            false_syllable[key].append(j2hcj(t[2]))
        elif len(w) == 3 and len(t) == 3 and w[2] != t[2]:
            false_syllable[key].append(j2hcj(t[2]))

    return false_syllable


# 연음 발음 일치 판단
def is_liasion(tail, word, target):
    tail = j2hcj(tail)
    if j2hcj(word[0]) == 'ㅇ' and j2hcj(target[0]) == tail:
        return True
    return False

# 구개음화 판단


def is_palatalization(tail, word, target):
    tail = j2hcj(tail)
    if tail == 'ㅌ' and j2hcj(word[0]) == 'ㅇ' and j2hcj(word[1]) == 'ㅣ' and j2hcj(target[0]) == 'ㅊ':
        return True
    elif tail == 'ㄷ' and j2hcj(word[0]) == 'ㅇ' and j2hcj(word[1]) == 'ㅣ' and j2hcj(target[0]) == 'ㅈ':
        return True


# ㅔ ㅐ 모음 발음 일치 판단
def vowel_pronunciation(w, t):
    w = j2hcj(w)
    t = j2hcj(t)

    if (w == 'ㅔ' and t == 'ㅐ') or (w == 'ㅐ' and t == 'ㅔ'):
        return True

    return False


# 단어 음절로 자르기
def split_syllable(list):
    # print(list)
    split_list = []
    syllable = ""
    for idx, val in enumerate(list):
        if is_end_of_syllable(list, idx):
            syllable += list[idx]
            split_list.append(syllable)
            syllable = ""
        else:
            syllable += list[idx]

    return split_list


# 음절 끝인지 판단
def is_end_of_syllable(word, idx):
    if get_jamo_class(word[idx]) == "tail":  # 종성
        return True

    if get_jamo_class(word[idx]) == 'vowel' and (idx == len(word)-1 or word[idx+1] == ' ' or get_jamo_class(word[idx+1]) == 'lead'):  # 중성으로 끝나는 음절
        return True

    return False


def remove_marks(string):  # 특수문자(마침표 포함) 제거 함수
    return re.sub('[.-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', string)


if __name__ == "__main__":
    mainjamo(sys.argv[1], sys.argv[2])  # argv[1]: 예문,  argv[2]: 연습
