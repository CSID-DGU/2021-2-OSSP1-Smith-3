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
        if(voice_table[i]!=script_table[i]):
            temp = []
            for j in range(len(voice_table[i])):
                if voice_table[i][j] != script_table[i][j]:
                    temp.append(voice_table[i][j])
            falseWord[voice_table[i]] = temp
    
    # print(falseWord)

    data = {  # Json으로 넘길 data 생성
        'mecab_table': voice_table, #형태소 분석 결과
        'false':falseWord # 틀린 부분 "틀린 형태소": "틀린 글자"
    }
    print(json.dumps(data))

# script_table과 형식 맞추기
def reconstruct():
    idx = 0 
    i =0

    while needReconstruct():
        if voice_table[i] != script_table[idx]: # voice가 더 쪼개짐 ex) script[idx]= '해외여행' voice[idx] = '해외'
            if len(script_table[idx])>len(voice_table[i]):
                diff = len(script_table[idx])-len(voice_table[i])
                #print("diff = " + str(diff))
                while diff>0:
                    if len(voice_table[i+1]) >= diff:
                        voice_table[i] = voice_table[i]+voice_table[i+1][0:diff]
                        voice_table[i+1] = voice_table[i+1][diff:]
                        if(voice_table[i+1]==''):
                            del voice_table[i+1]
                            i+=1
                            diff = 0
                    else:
                        voice_table[i] += voice_table[i+1][0:]
                        diff -= len(voice_table[i+1])
                        del voice_table[i+1]
                #print(voice_table)
                #print("i = "+str(i))
                idx +=1
            elif len(script_table[idx])<len(voice_table[i]): # voice가 덜 쪼개짐 ex) script[idx]= '해외' voice[idx] = '해외여행'
                #print(str(i)+"번째 요소를 다시 쪼갭니다")
                diff = len(voice_table[i])- len(script_table[idx])
                voice_table.insert(i+1,voice_table[i][0:diff])
                voice_table.insert(i+2,voice_table[i][diff:])
                del voice_table[i]
                idx+=1
                i+=1
                #print(voice_table)
                    
                
def needReconstruct():
    if len(voice_table)!=len(script_table): # 형태소 개수가 다름
        return True
    else:
        for i in range(len(voice_table)):
            if(len(voice_table[i])!=len(script_table[i])): # 개수는 같은데 형식이 다름 ex) ["해","외","여행"] ["해외","여", "행"] 
                return True
    
    return False

if __name__=="__main__":
    main(sys.argv[1], sys.argv[2]) # argv[1]: 예문,  argv[2]: 연습

#===================================================================================================#
#===================================================================================================#
#===================================================================================================#
#===================================================================================================#
#===================================하얀집 코드======================================================#



# def super_compare(script_index, voice_sentence, one_sentence):
#     voice_sentence_component = make_element_table(voice_sentence, one_sentence)
#     if simple_compare(script_table[script_index], voice_sentence):
#         return True
#     if change_taxis_compare(element_table[script_index], voice_sentence_component):
#         return True
#     if not subject_compare(element_table[script_index], voice_sentence_component):
#         if change_active_passive(element_table[script_index], voice_sentence_component):
#             return True
#         return False
#     if not object_compare(element_table[script_index], voice_sentence_component):
#         return False
#     if not predicate_compare(element_table[script_index], voice_sentence_component):
#         return False
#     if not adnominal_noun_compare(script_index, one_sentence, voice_sentence):
#         return False
#     if not flag_true_compare(element_table[script_index], voice_sentence_component):
#          return False
#     if j_compare(element_table[script_index], voice_sentence_component):
#         return True
#     elif change_active_passive(element_table[script_index], voice_sentence_component):
#         return True

#     return False

# # 문장 단순 비교 함수
# def simple_compare(script_sentence, voice_sentence):
#     if len(script_sentence) != len(voice_sentence):
#         return False
#     for i in range(0,len(script_sentence)):
#         if script_sentence[i][0] != voice_sentence[i][0]:
#             if not( (script_sentence[i][0] == '의' or script_sentence[i][0] == '에')  # 추가
#                     and (voice_sentence[i][0] == '의' or voice_sentence[i][0] == '에')):
#                 return False
#     return True

# # 문장 단순히 순서만 바뀌었을 때 일치 판정 함수
# def change_taxis_compare(script_sentence_component, voice_sentence_component):
#     for i in range(0, 7):
#         if len(script_sentence_component[i]) != len(voice_sentence_component[i]):
#             return False
#         if i==6:
#             isHaveSame = False
#             for j in range(0, len(script_sentence_component[i])):
#                 for k in range(0, len(voice_sentence_component[i])):
#                     if script_sentence_component[i] and voice_sentence_component[i]:
#                         if script_sentence_component[i][j][0] == voice_sentence_component[i][k][0]:
#                             isHaveSame = True
#                             break
#                 if not isHaveSame:
#                     return False
#                 else:
#                     isHaveSame = False
#         else:
#             for j in range(0, len(script_sentence_component[i])):
#                 if voice_sentence_component[i]:
#                     if script_sentence_component[i][j][0] != voice_sentence_component[i][j][0]:
#                         return False
#     return True

# # 주어 일치 확인
# def subject_compare(script_sentence, voice_sentence):
#     if script_sentence[0]:
#         if voice_sentence[0]:
#             if find_N(script_sentence[0]) == find_N(voice_sentence[0]): return True
#             else: return False
#         else: return False
#     else:
#         if voice_sentence[0]: return False
#         else: return True

# # 목적어 일치 확인
# def object_compare(script_sentence, voice_sentence):
#     if script_sentence[1]:
#         if voice_sentence[1]:
#             if find_N(script_sentence[1]) == find_N(voice_sentence[1]): return True
#             else: return False
#         else: return False
#     else:
#         if voice_sentence[1]: return False
#         else: return True

# # 본동사 일치 확인
# def predicate_compare(script_sentence, voice_sentence):
#     if script_sentence[2]:
#         if voice_sentence[2]:
#             s_index = 0
#             v_index = 0
#             for s_index in range(len(script_sentence[2])):
#                 if script_sentence[2][s_index][1].find('VV') != -1:
#                     break
#             for v_index in range(len(voice_sentence[2])):
#                 if voice_sentence[2][v_index][1].find('VV') != -1:
#                     break
#             if script_sentence[2][s_index][0] == voice_sentence[2][v_index][0]:
#                 return True
#         else: return False
#     else:
#         if voice_sentence[2]: return False
#         else: return True
#     return False

# # 주어진 문장성분에서 조사를 제외하고 반환
# def find_N(block):
#     s = []
#     for i in range(len(block)):
#         if block[i][1] == 'JKS' or block[i][1] == 'JKC' or block[i][1] == 'JKG' or block[i][1] == 'JKO' or \
#             block[i][1] == 'JKB' or block[i][1] == 'JKV' or block[i][1] == 'JKQ' or block[i][1] == 'JX' or \
#             block[i][1] == 'JC':
#             continue
#         else: s.append(block[i])
#         return s

# # 관형어+명사 비교
# def adnominal_noun_compare(script_index, one_sentence, voice_sentence):
#     script_modifier_table = modifier_table[script_index]
#     voice_modifier_table = make_modifier_table(one_sentence, voice_sentence)

#     if len(script_modifier_table) > len(voice_modifier_table):
#         return False
#     adnominal_flag = True
#     found_noun = False
#     for i in range(len(script_modifier_table)):
#         for j in range(len(voice_modifier_table)):
#             # 같은 명사 찾았을 때 앞의 수식어 비교
#             if script_modifier_table[i][len(script_modifier_table[i])-1] == voice_modifier_table[j][len(voice_modifier_table[j])-1]:
#                 found_noun = True                   # 같은 명사 있음
#                 if script_modifier_table[i] != voice_modifier_table[j]:
#                     adnominal_flag = False          # 같은 명사의 수식어가  틀림
#         if not found_noun:                          # 같은 명사 못 찾았을 시 False
#             return False
#     if adnominal_flag: return True                  # 같은 명사의 수식어가 같으면 True
#     else: return False                              # 같은 명사의 수식어가 다르면 False
#     return False

# # 시제와 부정 표현이 모두 일치하는지 확인하는 함수
# def flag_true_compare(script_sentence_component, voice_sentence_component):
#     # 7: 시제가 맞는지 확인
#     # 8: 부정표현이 맞는지 확인
#     if script_sentence_component[7] == voice_sentence_component[7] \
#             and script_sentence_component[8] == voice_sentence_component[8]:
#         return True
#     else:
#         return False

# # 조사가 바뀌었을 때 일치 판정 함수
# def j_compare(script_sentence_component, voice_sentence_component):
#     for q in range(0, 2):
#         if len(voice_sentence_component[q]) == len(script_sentence_component[q]):
#             for k in range(0, len(voice_sentence_component[q])):
#                 if (voice_sentence_component[q][k][1] == 'JX' and voice_sentence_component[q][k][0] == '은') or \
#                         (voice_sentence_component[q][k][1] == 'JX' and voice_sentence_component[q][k][0] == '는') \
#                         or voice_sentence_component[q][k][1] == 'JKS' or voice_sentence_component[q][k][1] == 'JKO':
#                     continue
#                 else:
#                     if script_sentence_component[q][k][0] != voice_sentence_component[q][k][0]:
#                         return False
#         else:
#             return False
#     for i in range(2, 7):
#         if len(voice_sentence_component[i]) == len(script_sentence_component[i]):
#             for j in range(0, len(voice_sentence_component[i])):
#                 if script_sentence_component[i][j] and voice_sentence_component[i][j]:
#                     if script_sentence_component[i][j][0] != voice_sentence_component[i][j][0]:
#                         return False
#         else:
#             return False

#     return True

# # 능동, 피동 바뀌었을 때 일치 판정 함수
# def change_active_passive(script_sentence_component, voice_sentence_component):
#     # script : 능동 / voice : 피동
#     subject_equal_adverb = False  # script 주어와 voice 부사어 같은가
#     object_equal_subject = False  # script 목적어와 voice 주어 같은가
#     verb_equal = False  # 본동사 일치하는가
#     if script_sentence_component[0] and voice_sentence_component[4] and script_sentence_component[1] and \
#             voice_sentence_component[0] \
#             and script_sentence_component[2] and voice_sentence_component[2]:
#         for i in range(0, len(voice_sentence_component[4])):  # script의 주어가 voice 부사어에 있나 확인
#             if (script_sentence_component[0][0][0] == voice_sentence_component[4][i][0]):
#                 subject_equal_adverb = True
#         if script_sentence_component[1][0][0] == voice_sentence_component[0][0][0]:  # script 목적어와 voice 주어가 같나 확인
#             object_equal_subject = True

#         for i in range(0, len(script_sentence_component[2])):  # script의 본 동사 찾기
#             if script_sentence_component[2][i][1].find("VV") != -1:
#                 script_verb = script_sentence_component[2][i][0]
#         for i in range(0, len(voice_sentence_component[2])):  # voice의 본 동사 찾기
#             if voice_sentence_component[2][i][1].find("VV") != -1:
#                 voice_verb = voice_sentence_component[2][i][0]

#         try:
#             # script의 본동사와 voice의 본동사가 일치하는 부분이 있으면 true
#             if script_verb.find(voice_verb) != -1 or voice_verb.find(script_verb) != -1:
#                 verb_equal = True
#         except:
#             return False

#         if subject_equal_adverb == True and object_equal_subject == True and verb_equal == True:
#             return True
#     # script : 피동 / voice : 능동
#     subject_equal_object = False  # script 주어와 voice 목적어가 같은가
#     adverb_equal_subject = False  # script 부사어와 voice 주어가 같은가
#     verb_equal = False  # 본동사 일치하는가
#     if script_sentence_component[0] and voice_sentence_component[1] and script_sentence_component[4] and \
#             voice_sentence_component[0] \
#             and script_sentence_component[2] and voice_sentence_component[2]:
#         if script_sentence_component[0][0][0] == voice_sentence_component[1][0][0]:  # script 주어와 voice 목적어가 같은가
#             subject_equal_object = True
#         for i in range(0, len(script_sentence_component[4])):
#             if script_sentence_component[4][i][0] == voice_sentence_component[0][0][0]:  # script 부사어와 voice 주어가 같은가
#                 adverb_equal_subject = True
#         for i in range(0, len(script_sentence_component[2])):  # script의 본 동사 찾기
#             if script_sentence_component[2][i][1].find("VV") != -1:
#                 script_verb = script_sentence_component[2][i][0]
#         for i in range(0, len(voice_sentence_component[2])):  # voice의 본 동사 찾기
#             if voice_sentence_component[2][i][1].find("VV") != -1:
#                 voice_verb = voice_sentence_component[2][i][0]

#         try:
#             # script의 본동사와 voice의 본동사가 일치하는 부분이 있으면 true
#             if script_verb.find(voice_verb) != -1 or voice_verb.find(script_verb) != -1:
#                 verb_equal = True
#         except:
#             return False

#         if subject_equal_object == True or adverb_equal_subject == True or verb_equal == True:
#             return True
#     return False

# def add_space_after_mot(input_string):  # '못' 뒤에 띄어쓰기 추가하는 함수 : '못'을 기준으로 split한 후, 각 요소 사이에 '못+공백'을 추가하여 합침.
#     split_neg = input_string.split('못')
#     for i in range(len(split_neg)):
#         string = '못 '.join(split_neg)
#     return string

# def add_period(input_string): # 음성인식된 문장의 '좋아합니다' 뒤에 . 추가
#     # '좋아합니다' 뒤에 문장이 오거나, '.' 이 있을 때는 좋+아+합니다 로 형태소 분석
#     # '좋아합니다' 뒤에 문장x, '.'x 일 때는 좋아합니다 로 형태소 분석
#     # 위 경우를 하나로 통일시키기 위한 함수
#     index = input_string.find('좋아합니다')
#     result = input_string
#     if index != -1:
#         index += 5
#         result = input_string[:index] + '.' + input_string[index:]
#     return result

# def is_sentence_End(last_token):  # 문장의 마지막인지 판단 : EF[종결어미] 이거나 EC(연결어미)로 분석된 마지막 요소
#     # find('str')는 str의 위치를 반환하는 함수. 없을 때는 -1 반환
#     # 문장의 마지막 형태소일 때(즉, EF[종결어미]를 만났을 때)
#     # 혹은 EC일 경우, '다','요','까'의 경우 종결어미로 인식
#     if last_token[1].find('EF') != -1 \
#             or last_token[1].find('EC') != -1:
#         return True
#     else:
#         return False

# def is_MAG_except_neg(token):  # '못', '안'을 제외한 MAG[일반 부사]인가 판단
#     if token[1] == 'MAG':
#         if token[0] != '못' and token[0] != '안':
#             return True
#     return False


# def is_mark(token):  # 문장부호(. ? ! , · / : )인지 판단
#     if token[1] == 'SF' or token[1] == 'SC':
#         return True
#     return False

# # 찾고자 하는 문자('했' 같은 것)가 있는지 판단하는 함수
# def is_have_char(what_find, token):
#     if token[0].find(what_find) != -1:
#         return True
#     else:
#         return False

# # 찾고자 하는 태그('EF' 같은 것)가 있는지 판단하는 함수
# def is_have_tag(what_find, token):
#     if token[1].find(what_find) != -1:
#         return True
#     else:
#         return False

# def sentence_without_part(text):   #연결어미로 끝나지 않을 때 포함하여 원본 반환
#     mecab = Mecab()
#     sentences = []
#     mecab_text = mecab.pos(text)
#     for i in range(0, len(mecab_text)):
#         sentence = text
#         if is_sentence_End(mecab_text[i]):
#             index = text.find(mecab_text[i][0])
#             index += len(mecab_text[i][0])
#             if (i < len(mecab_text) - 1):
#                 if is_mark(mecab_text[i + 1]):
#                     index += 1
#             sentence = text[:index]
#             text = text[index:]
#             sentences.append(sentence)

#     if not (text.isspace()) and text != '':
#         sentences.append(text)
#     return sentences

# def remove_marks(string): # 특수문자 제거 함수
#     return re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', string)

# def each_sentence_division(script_string_array): # 한 문장 단위로 끊어서 분석하는 함수
#     global element_table
#     mecab = Mecab()
#     string_table = []
#     count = 0

#     for each in script_string_array: # 문장 단위로 끊어져 저장되어 있는 배열에서 한 문장씩 (each) 형태소 분석
#         complete_sentence = []
#         sentence = str(each)
#         sentence = remove_marks(sentence) #특수문자 제거
#         sentence = add_space_after_mot(sentence) # '못' 띄어쓰기 처리
#         mecab_result = mecab.pos(sentence)

#         for i in range(len(mecab_result)):
#             complete_sentence.append(mecab_result[i])

#         string_table.append(complete_sentence) # 분석 완료된 문장을 string_table에 추가
#         #element_table, modifier_table 구성하는 작업
#         one_line_temp = make_element_table(complete_sentence, script_string_array[count])
#         element_table = np.append(element_table, np.array([one_line_temp], dtype=list), axis=0)
#         modifier_table.append(make_modifier_table(script_string_array[count], complete_sentence))
#         count += 1

#     #return string_table <- 나중에 필요하면 반환

# def sentence_division(input_string):
#     global element_table

#     mecab = Mecab()

#     input_string = add_space_after_mot(input_string)  # '못' 뒤에 띄어쓰기 추가

#     string_table = []  # 한 문장씩 저장할 테이블
#     mecab_result = mecab.pos(input_string)  # ex) [('안녕', 'NNG'), ('하', 'XSV'), ('세요', 'EP+EF')]

#     string_start = 0  # 각 문장의 첫번째 요소 가르키는 변수
#     cnt = 0  # 한 문장에 대해 형태소 분석이 안 된 문장을 index로 찾아가기 위한 변수
#     for i in range(len(mecab_result)):
#         if is_sentence_End(mecab_result[i]):  # 문장의 마지막인지 판단
#             sentence = []
#             for j in range(string_start, i + 1):  # 한 문장 내의 첫번째 요소부터 마지막 요소까지 저장.
#                 # if is_MAG_except_neg(mecab_result[j]):  # '못', '안'을 제외한 MAG[일반 부사]는 저장 X
#                 #     continue
#                 if is_mark(mecab_result[j]):  # 문장부호는 저장 X
#                     continue
#                 sentence.append(mecab_result[j])  # 각 요소를 현재 문장에 추가
#             string_table.append(sentence)  # 완성된 한 문장을 테이블에 추가

#             cnt += 1
#             string_start = i + 1  # 다음 문장의 첫 번째 요소를 가리킴.
#     return string_table

#     # sentence_division 함수를 한번 실행하면 total_table 완성! total_table은 global 변수 이므로 함수 실행 후 사용하면 됨!
#     # 문제! : 다은이 -> 다(MAG) + 은이(NNG) : MAG 삭제

# # 대본에 대해 문장별로 요소들을 정리하여 total_table에 담는 함수
# # | 주어 | 목적어 | 서술어 | 관형어 | 부사어 | 보어 | 아무것도 아닌거 | 시제 flag | 부정의 의미인지 아닌지 flag |
# # |  0  |   1   |   2   |   3   |   4   |  5  |      6       |    7     |            8             |
# def make_element_table(mecab_sentence, origin_sentence):

#     divide_line = [[], [], [], [], [], [], [], [], []]
#     other_element = []

#     divide_line[0].extend(find_s(mecab_sentence))
#     divide_line[1].extend(find_o(mecab_sentence))
#     divide_line[2].extend(find_verb(mecab_sentence))
#     divide_line[3].extend(find_tubular(origin_sentence, mecab_sentence))
#     divide_line[4].extend(find_adverb(mecab_sentence))
#     divide_line[5].extend(find_complement(mecab_sentence))

#     for i in range(len(mecab_sentence)):    # 각 언어 요소들 검사에 해당하지 않는 모든 요소들을 찾아냄
#         flag = 0
#         for j in range(len(divide_line) - 3):
#             for k in range(len(divide_line[j])):
#                 if mecab_sentence[i] == divide_line[j][k]:
#                     flag = 1
#         if flag == 0:
#             other_element.append(mecab_sentence[i])

#     divide_line[6].extend(other_element)
#     divide_line[7].extend(tense_to_flag(mecab_sentence))
#     divide_line[8].extend(find_neg(mecab_sentence))

#     return divide_line

# # 체언을 꾸미는 말만 따로 모아놓는 테이블을 만드는 함수
# def make_modifier_table(input_string, mecab_string):
#     temp_string = mecab_string
#     temp_modifier = []

#     for i in range(len(temp_string)):
#         modifier_line = [[], [], []]  # 관형형 전성 어미가 2개로 끊기는 경우(ex. 깨끗 + 한 + ~)
#         modifier_line_two = [[], []]  # 관형형 전성 어미가 1개로 끊기는 경우(ex. 아름다운 + ~)
#         if temp_string[i][1].find('ETM') != -1:  # 관형형 전성어미를 통해 관형어를 찾음
#             if temp_string[i][1].find('+') != -1:  # 관형형 전성어미가 다른 형태소에 포함되어 나오는 경우(ex.('못생긴', 'VA+ETM'))
#                 inputIndex = input_string.find(temp_string[i][0])
#                 if temp_string[i - 1] == temp_string[
#                     len(temp_string) - 1]:  # 여러 개의 관형형 전성어미가 나올 경우 띄어쓰기로 각각을 구분하기 때문에 맨 앞의 관형형 전성어미에 대한 예외처리
#                     if temp_string[i] != temp_string[len(temp_string) - 1]:  # 만약 관형형 전성어미 뒤에서 문장이 잘린 경우 테이블에 넣으면 안됨
#                         modifier_line_two[0].extend(temp_string[i])
#                         modifier_line_two[1].extend(temp_string[i + 1])
#                         temp_modifier.append(modifier_line_two)

#                 elif input_string[
#                     inputIndex - 1] != ' ':  # 관형형 전성어미가 다른 형태소와 합성되어 있으며 그 앞에 다른 형태소가 나오는 경우 관형형 전성어미의 앞의 단어도 list에 추가(ex.('깨끗', 'XR'), ('한', 'XSA+ETM'))
#                     if temp_string[i] != temp_string[len(temp_string) - 1]:  # 만약 관형형 전성어미 뒤에서 문장이 잘린 경우 테이블에 넣으면 안됨
#                         modifier_line[0].extend(temp_string[i - 1])
#                         modifier_line[1].extend(temp_string[i])
#                         modifier_line[2].extend(temp_string[i + 1])
#                         temp_modifier.append(modifier_line)

#                 else:  # 관형형 전성어미가 붙어서 한번에 나오는 경우 그 단어만 관형어 list에 추가(ex.('아름다운', 'VA+ETM'))
#                     if temp_string[i] != temp_string[len(temp_string) - 1]:  # 만약 관형형 전성어미 뒤에서 문장이 잘린 경우 테이블에 넣으면 안됨
#                         modifier_line_two[0].extend(temp_string[i])
#                         modifier_line_two[1].extend(temp_string[i + 1])
#                         temp_modifier.append(modifier_line_two)

#             else:  # 관형형 전성어미가 다른 형태소에 포함되지 않고 나오는 경우(ex.('작', 'VA'), ('은', 'ETM'))
#                 if temp_string[i] != temp_string[len(temp_string) - 1]:  # 만약 관형형 전성어미 뒤에서 문장이 잘린 경우 테이블에 넣으면 안됨
#                     modifier_line[0].extend(temp_string[i - 1])
#                     modifier_line[1].extend(temp_string[i])
#                     modifier_line[2].extend(temp_string[i + 1])
#                     temp_modifier.append(modifier_line)

#     return temp_modifier  # 한 문장에 대한 테이블 한 행을 반환


# # 주어 찾는 함수
# def find_s(sentence):
#     s_table = []  # 주어들만 저장할 테이블
#     for k in range(len(sentence)):  # 테이블에 저장된 한 문장 길이 동안
#         if ((sentence[k][0] == '가' and sentence[k][1] == 'JKS') or (sentence[k][0] == '이' and sentence[k][1] == 'JKS')):
#             do_jamo = j2hcj(h2j(sentence[k + 1][0])) # 뒤에 '되', '돼'가 오면 보어로 처리해야함
#             if (do_jamo[0] == 'ㄷ' and do_jamo[1] == 'ㅚ') or \
#                     (do_jamo[0] == 'ㄷ' and do_jamo[1] == 'ㅙ'):
#                 break
#             # 가,이 중 주격 조사인 것들에 한해
#             cnt = 0
#             for m in range(0, k):  # 주격 조사 앞에 있는 것들중
#                 if (sentence[m][1] == 'NNG' or sentence[m][1] == 'NNP' or sentence[m][1] == 'NNB' or sentence[m][
#                     1] == 'NP'):
#                     # 명사에 해당 되는 것들 중에
#                     cnt = m  # 가장 주격 조사에 가까운 것을
#             s_table.append(sentence[cnt])  # 주어라고 저장
#             s_table.append(sentence[k])  # 주어 뒤에 조사(확인용)

#         if ((sentence[k][0] == '은' and sentence[k][1] == 'JX') or (sentence[k][0] == '는' and sentence[k][1] == 'JX')):
#             # 은, 는 중 보조사 인것들에 한해
#             jks_cnt = -1  # 주격조사count변수
#             jx_cnt = -1
#             for x in range(len(sentence)):  # 테이블의 i번째 문장 길이동안
#                 if (sentence[x][1] == 'JKS'):  # jsk(주격 조사가 있으면)
#                     jks_cnt += 1  # count변수++
#             for jx in range(0, k):
#                 if ((sentence[jx][0] == '은' and sentence[jx][1] == 'JX') or (
#                         sentence[jx][0] == '는' and sentence[jx][1] == 'JX')):
#                     jx_cnt += 1
#             if (jks_cnt < 0 and jx_cnt < 0):  # 만약 주격 조사가 없으면
#                 N_cnt = 0
#                 for z in range(0, k):  # 은, 는 앞에 있는 것들중
#                     if (sentence[z][1] == 'NNG' or sentence[z][1] == 'NNP' or sentence[z][1] == 'NNB' or sentence[z][
#                         1] == 'NP'):
#                         # 명사에 해당 되는 것들 중에
#                         N_cnt = z  # 가장 주격 조사에 가까운 것을

#                 s_table.append(sentence[N_cnt])  # 주어라고 저장
#                 s_table.append(sentence[k])  # 주어 뒤에 조사(확인용)

#     return s_table

# #목적어 찾는 함수
# def find_o(sentence):
#     cnt = 0
#     o_table = []  # 목적어들만 저장할 테이블
#     for k in range(len(sentence)):  # 문장 한문장 안에
#         if ((sentence[k][0] == '을' and sentence[k][1] == 'JKO') or (sentence[k][0] == '를' and sentence[k][1] == 'JKO')):
#             # 을를 인데 목적격 조사인 것이 나오면
#             o_table.append(sentence[k - 1])  # 목적어 라고 저장
#             o_table.append(sentence[k])  # 목적어 뒤에 조사(확인용)

#         if ((sentence[k][0] == '은' and sentence[k][1] == 'JX') or (sentence[k][0] == '는' and sentence[k][1] == 'JX')):
#             # 은 는 인데 보조사 인 경우
#             jks_cnt = -1  # 주격조사를 count
#             jx_cnt = -1
#             for x in range(len(sentence)):  # 테이블의 i번째 문장 길이동안
#                 if (sentence[x][1] == 'JKS'):  # jsk(주격 조사가 있으면)
#                     jks_cnt += 1  # count변수++
#             for jx in range(0, k):
#                 if ((sentence[jx][0] == '은' and sentence[jx][1] == 'JX') or (
#                         sentence[jx][0] == '는' and sentence[jx][1] == 'JX')):
#                     jx_cnt += 1
#             if (jks_cnt >= 0 or jx_cnt >= 0):  # 주격 조사가 있으면
#                 N_cnt = 0
#                 for z in range(0, k):  # 은, 는 앞에 있는 것들중
#                     if (sentence[z][1] == 'NNG' or sentence[z][1] == 'NNP' or sentence[z][1] == 'NNB' or sentence[z][
#                         1] == 'NP'):
#                         # 명사에 해당 되는 것들 중에
#                         N_cnt = z  # 가장 주격 조사에 가까운 것을

#                 o_table.append(sentence[N_cnt])  # 조사 앞을 목적어라고 저장
#                 o_table.append(sentence[k])  # 목적어 뒤에 조사(확인용)

#     return o_table

# # 서술어를 찾는 함수
# def find_verb(input_string):
#     verb_table=[]
#     start_flag = -1  # 서술어의 시작 플래그 초기화
#     for j in range(0, len(input_string)):
#         if start_flag == -1 and is_have_tag('V', input_string[j]):  # 문장 요소에 V가 있다면
#             start_flag = j  # 시작 플래그는 현재 토큰 index
#         elif is_have_tag('NNG', input_string[j]):  # 문장 요소에 N이 있다면
#             start_flag = -1  # 서술어가 아니므로 start_flag = -1
#     if start_flag != -1:  # start_flag가 -1이면 서술어가 없다는 것
#         if start_flag > 0:  # start flag가 0이라면 앞에 것 볼 필요X
#             if is_have_tag('NNG', input_string[start_flag - 1]):  # start_flag 앞의 토큰이 명사라면
#                 start_flag -= 1  # 시작 플래그를 하나 줄인다.
#         for k in range(start_flag, len(input_string)):  # start_flag부터 끝까지 서술어
#             verb_table.append(input_string[k])

#     return verb_table

# # 관형어를 찾는 함수 : 관형격 조사를 통해 관형어를 찾는 경우, 관형사를 관형어로 찾는 경우, 관형형 전성어미를 통해 관형어를 찾는 경우로 구성
# def find_tubular(input_string, mecab_string):  # (체언 단독의 경우(ex.우연히 고향 친구를 만났다)와 체언의 자격을 가진 말 + 관형격 조사의 경우(ex.그는 웃기기의 천재다) 아직 처리 X)
#     temp_string = mecab_string
#     tubularArr = []

#     for i in range(len(temp_string)):
#         if temp_string[i][1].find('JKG') != -1:  # 관형격 조사를 통해 관형어를 찾음. 관형격 조사와 그 앞의 단어는 관형어이므로 이를 list에 추가
#             tubularArr.append(temp_string[i - 1])
#             tubularArr.append(temp_string[i])

#         if temp_string[i][1].find('MM') != -1:  # 관형사를 관형어로 판단. 관형사를 list에 추가
#             tubularArr.append(temp_string[i])

#         if temp_string[i][1].find('ETM') != -1:  # 관형형 전성어미를 통해 관형어를 찾음
#             if temp_string[i][1].find('+') != -1:  # 관형형 전성어미가 다른 형태소에 포함되어 나오는 경우(ex.('못생긴', 'VA+ETM'))
#                 inputIndex = input_string.find(temp_string[i][0])
#                 if temp_string[i - 1] == temp_string[
#                     len(temp_string) - 1]:  # 여러 개의 관형형 전성어미가 나올 경우 띄어쓰기로 각각을 구분하기 때문에 맨 앞의 관형형 전성어미에 대한 예외처리
#                     tubularArr.append(temp_string[i])
#                 elif input_string[inputIndex - 1] != ' ':  # 관형형 전성어미가 다른 형태소와 합성되어 있으며 그 앞에 다른 형태소가 나오는 경우 관형형 전성어미의 앞의 단어도 list에 추가(ex.('깨끗', 'XR'), ('한', 'XSA+ETM'))
#                     tubularArr.append(temp_string[i - 1])
#                     tubularArr.append(temp_string[i])
#                 else:  # 관형형 전성어미가 붙어서 한번에 나오는 경우 그 단어만 관형어 list에 추가(ex.('아름다운', 'VA+ETM'))
#                     tubularArr.append(temp_string[i])
#             else:  # 관형형 전성어미가 다른 형태소에 포함되지 않고 나오는 경우(ex.('작', 'VA'), ('은', 'ETM'))
#                 tubularArr.append(temp_string[i - 1])
#                 tubularArr.append(temp_string[i])

#     return tubularArr  # 한 문장 안에 관형어는 여러 개가 될 수 있으므로 list의 형식으로 값을 반환

# # 부사어를 찾는 함수
# def find_adverb(input_string):
#     temp_string = input_string
#     adverbArr = []

#     for i in range(len(temp_string)):
#         if temp_string[i][1].find('MAG') != -1:
#             adverbArr.append(temp_string[i])

#         if temp_string[i][1].find('MAJ') != -1:
#             adverbArr.append(temp_string[i])

#         if temp_string[i][1].find('JKB') != -1:
#             adverbArr.append(temp_string[i - 1])
#             adverbArr.append(temp_string[i])

#     return adverbArr

# # 보어를 찾는 함수 : 보격 조사를 찾고 보격 조사 앞에 있는 단어 + 보격 조사를 보어로 반환
# def find_complement(input_string):  # ('되다'의 경우 현재 보격 조사 판별 X)
#     temp_string = input_string
#     complementArr = []
#     N_cnt = 0
#     for i in range(len(temp_string)):
#         if temp_string[i][1].find('JKC') != -1:  # 형태소 분석을 한 결과에서 보격 조사를 찾음
#             for j in range(0, i): # 문장 처음부터 보격 조사 까지
#                 N_cnt = 0
#                 if (temp_string[j][1] == 'NNG' or temp_string[j][1] == 'NNP' or
#                     temp_string[j][1] == 'NNB' or temp_string[j][1] == 'NP'):
#                     N_cnt = j # 보격 조사에 가장 가까운 명사를 찾아서
#             for k in range(N_cnt,i+1): #명사부터 보격 조사까지
#                  complementArr.append(temp_string[k]) # 저장
#         if temp_string[i][1].find('JKS') != -1:
#             do_jamo = j2hcj(h2j(temp_string[i+1][0]))
#             if (do_jamo[0] == 'ㄷ' and do_jamo[1] == 'ㅚ') or \
#                     (do_jamo[0] == 'ㄷ' and do_jamo[1] == 'ㅙ'):
#                 for j in range(0, i):  # 문장 처음부터 보격 조사 까지
#                     N_cnt = 0
#                     if (temp_string[j][1] == 'NNG' or temp_string[j][1] == 'NNP' or
#                             temp_string[j][1] == 'NNB' or temp_string[j][1] == 'NP'):
#                         N_cnt = j  # 보격 조사에 가장 가까운 명사를 찾아서
#                 for k in range(N_cnt, i + 1):  # 명사부터 보격 조사까지
#                     complementArr.append(temp_string[k])  # 저장

#     return complementArr  # 한 문장 안에 보어가 여러 개가 될 수 있으므로 list의 형식으로 값을 반환

# # 시제 찾는 함수
# def find_tense(sentence):
#     tense_table = [['past', ], ['present', ], ['future', ]] # 문자열과 시제를 함께 저장할 테이블
#     # ____________________________
#     # | past(0행)   |  문장  |  ...
#     # | __________________________
#     # | present(1행)|  문장  |  ...
#     # | __________________________
#     # | future(2행) |  문장  |  ...
#     # | __________________________

#     special_future = 0  # '것','이'를 처리하기 위한 변수
#     is_present_flag = True  # 현재시제 판단 위한 변수
#     for i in range(len(sentence)):
#         # 미래시제 1: '것''이'
#         if sentence[i][1].find('NNB') != -1 and sentence[i][0].find('것') != -1:
#             do_jamo = j2hcj(h2j(sentence[i - 1][0]))  # jamo를 이용해 분리(할->ㅎㅏㄹ)
#             if len(do_jamo) > 2 and do_jamo[2] == 'ㄹ':  # 종성이 있고, -ㄹ 것이 가 미래형으로 구분
#                 special_future = special_future + 1  # NNB 는 '것'이므로 ++함
#         if sentence[i][1].find('VCP') != -1 and sentence[i][0].find('이') != -1:
#             special_future = special_future + 1  # VCP 는 '이'이므로 ++함
#         if special_future == 2:  # '것'과 '이'가 모두 존재하면 미래 시제로 판단
#             tense_table[2].append(sentence)
#             is_present_flag = False
#             break
#         # 높임 표현(시, 십, 세, 심, 실)의 경우 처리
#         if sentence[i][1].find('EP') != -1 \
#                 and not sentence[i][0].find('시') != -1 \
#                 and not sentence[i][0].find('십') != -1 \
#                 and not sentence[i][0].find('세') != -1 \
#                 and not sentence[i][0].find('실') != -1 \
#                 and not sentence[i][0].find('심') != -1:
#             # 미래시제 2: '겠'
#             if sentence[i][0].find('겠') != -1:
#                 tense_table[2].append(sentence)
#                 is_present_flag = False
#             # 과거시제
#             else:
#                 tense_table[0].append(sentence)
#                 is_present_flag = False
#             break
#     # 현재시제
#     if is_present_flag == True:
#         tense_table[1].append(sentence)
#     return tense_table
#     # 추가 사항
#     # '먹을 것이다'와 '먹는 것이다'를 구별할 수가 없음.
#     # -> 파이썬 jamo 패키지 사용하면 초중종성 분리해서 'ㄹ' 찾아서 미래 처리 가능

# # 시제를 플래그로 변환하는 함수
# def tense_to_flag(sentence):
#     # past    : 0
#     # present : 1
#     # future  : 2
#     tense_table = find_tense(sentence)
#     tense_flag = []
#     for i in range(len(tense_table)):
#         # 길이가 2 이상이어야 문장이 있는 것임
#         if len(tense_table[i]) > 1:
#             if tense_table[i][0] == 'past':
#                 tense_flag.append(0)
#             elif tense_table[i][0] == 'future':
#                 tense_flag.append(2)
#             else:
#                 tense_flag.append(1)
#     return tense_flag

# # 부정표현 flag
# # 못, 안, 않, 말/마, 아니, 없 처리
# # 부정표현 개수가 홀수이면 부정(1), 짝수이면 이중 부정이므로 긍정(0)
# def find_neg(sentence):
#     neg_flag = []  # 부정표현 flag를 저장할 배열(1:부정, 0:긍정)
#     neg_cnt = 0  # 부정표현 개수를 세기 위한 변수
#     for i in range(len(sentence)):
#         if is_have_char('못', sentence[i]):
#             neg_cnt = neg_cnt + 1
#         if is_have_char('안', sentence[i]) and is_have_tag('MAG', sentence[i]):
#             neg_cnt = neg_cnt + 1
#         if is_have_char('않', sentence[i]):
#             neg_cnt = neg_cnt + 1
#         if (is_have_char('말', sentence[i]) or is_have_char('마', sentence[i])) \
#                 and is_have_tag('VX', sentence[i]):
#             neg_cnt = neg_cnt + 1
#         if is_have_char('아니', sentence[i]):
#             neg_cnt = neg_cnt + 1
#         if is_have_char('없', sentence[i]):
#             neg_cnt = neg_cnt + 1

#     if neg_cnt % 2 == 1:  # 부정
#         neg_flag.append(1)
#     else:
#         neg_flag.append(0)  # 긍정

#     return neg_flag


