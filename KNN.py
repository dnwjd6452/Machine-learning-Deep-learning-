import numpy as np
import serial

Ard = serial.Serial('COM5', 115200)

normal = [2, 3]
normal2 = [-2, 1]
normal3 = [4, -1]
normal4 = [0, -2]
normal5 = [-1, -3]

left = [17, 16]
left2 = [16, 11]
left3 = [13, 8]
left4 = [9, 12]
left5 = [11, 13]

right = [-21, 20]
right2 = [-17, 21]
right3 = [-13, 12]
right4 = [-9, 15]
right5 = [-18, 8]

front = [20, -10]
front2 = [13, -16]
front3 = [9, -12]
front4 = [15, -11]
front5 = [17, -14]

back = [-19, -24]
back2 = [-14, -18]
back3 = [-12, -9]
back4 = [-7, -12]
back5 = [-10, -6]

category = ['정상', '왼쪽', '오른쪽', '앞', '뒤', '정상', '왼쪽', '오른쪽', '앞', '뒤', '정상', '왼쪽', '오른쪽', '앞', '뒤',
            '정상', '왼쪽', '오른쪽', '앞', '뒤', '정상', '왼쪽', '오른쪽', '앞', '뒤']

score = 0
All_score = 0
Average_score = 0
Final_score = 0

List = []
target = []

L1 = 0
R1 = 0
F1 = 0
B1 = 0
X = 0
Y = 0

L2 = 0
R2 = 0
F2 = 0
B2 = 0


def data_set():
    dataset = np.array(
        [normal, left, right, front, back, normal2, left2, right2, front2, back2, normal3, left3, right3, front3, back3,
         normal4, left4, right4, front4, back4, normal5, left5, right5, front5, back5])  # 분류집단
    size = len(dataset)
    class_target = np.tile(target, (size, 1))  # 분류대상
    class_category = np.array(category)  # 분류범주

    return dataset, class_target, class_category


def classify(dataset, class_target, class_categoty, k):
    # 유클리드 거리 계산
    diffMat = class_target - dataset  # 두 점의 차
    sqDiffMat = diffMat ** 2  # 차에 대한 제곱
    row_sum = sqDiffMat.sum(axis=1)  # 차에 대한 제곱에 대한 합
    distance = np.sqrt(row_sum)  # 차에 대한 제곱에 대한 합의 제곱근(최종거리)

    # 가까운 거리 오름차순 정렬
    sortDist = distance.argsort()

    # 이웃한 k개 선정
    class_result = {}
    for i in range(k):
        c = class_categoty[sortDist[i]]
        class_result[c] = class_result.get(c, 0) + 1
    return class_result


# 함수 호출
# k = 1


def classify_result(class_result):  # 분류결과 출력 함수 정의
    left1 = right1 = front1 = back1 = normal1 = 0

    for c in class_result.keys():
        if c == '왼쪽':
            left1 = class_result[c]
        elif c == '오른쪽':
            right1 = class_result[c]
        elif c == '앞':
            front1 = class_result[c]
        elif c == '뒤':
            back1 = class_result[c]
        else:
            normal1 = class_result[c]

    if left1 > right1 and left1 > front1 and left1 > back1 and left1 > normal1:
        result = 1  # "분류대상은 왼쪽 입니다"
    elif right1 > left1 and right1 > front1 and right1 > back1 and right1 > normal1:
        result = 2  # "분류대상은 오른쪽 입니다"
    elif front1 > left1 and front1 > right1 and front1 > back1 and front1 > normal1:
        result = 3  # "분류대상은 앞 입니다"
    elif back1 > left1 and back1 > right1 and back1 > front1 and back1 > normal1:
        result = 4  # "분류대상은 뒤 입니다"
    else:
        result = 5  # "분류대상은 정상 입니다."
    return result


k = 5

while True:
    y = Ard.readline()
    y = y.decode()[:-2]
    if len(y) >= 9:
        List.append([y.split('/')])
    L1 = List[0][0][0]
    R1 = List[0][0][1]
    F1 = List[0][0][2]
    B1 = List[0][0][3]

    L2 = int(L1)
    R2 = int(R1)
    F2 = int(F1)
    B2 = int(B1)
    print("왼쪽 : %d%%, 오른쪽 : %d%%, 앞쪽 : %d%%, 뒤쪽 : %d%%" % (L2, R2, F2, B2))

    if L2 > R2 and L2 > F2 and L2 > B2:
        X = L2 - F2
        Y = B2 - R2
    elif R2 > L2 and R2 > F2 and R2 > B2:
        X = L2 - F2
        Y = R2 - B2
    elif F2 > L2 and F2 > R2 and F2 > B2:
        X = F2 - L2
        Y = B2 - R2
    elif B2 > L2 and B2 > R2 and B2 > F2:
        X = F2 - L2
        Y = R2 - B2

    target.append([X, Y])

    dataset, class_target, class_categoty = data_set()

    class_result = classify(dataset, class_target, class_categoty, k)
    print("예측결과 : %s" % class_result)

    a = classify_result(class_result)
    List.clear()
    target.clear()

    if a == 1:
        All_score += 1
        print("최종결과 : 분류대상은 왼쪽 입니다")
    elif a == 2:
        All_score += 1
        print("최종결과 : 분류대상은 오른쪽 입니다")
    elif a == 3:
        All_score += 1
        print("최종결과 : 분류대상은 앞 입니다")
    elif a == 4:
        All_score += 1
        print("최종결과 : 분류대상은 뒤 입니다")
    elif a == 5:
        All_score += 1
        score += 1
        print("최종결과 : 분류대상은 정상 입니다")

    Average_score = (score / All_score) * 100
    Final_score = int(Average_score)
    print("자세점수 : %d점 입니다." % Final_score)
    print("")
