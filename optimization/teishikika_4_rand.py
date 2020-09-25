import pulp
import sys
import numpy as np
import time

# # [r,p,w]
# j_0 = [0,5,1]
# j_1 = [0,3,3]
# j_2 = [0,4,5]
# j_3 = [0,3,6]
# j_4 = [0,4,2]

# data = [j_0,j_1,j_2,j_3,j_4]

def all(job_num):

    # p=[1, 93, 26, 30, 93, 76, 48, 90, 98, 27, 78, 42, 75, 79, 79, 43, 95, 80, 83, 10]
    # w=[1, 3, 3, 5, 9, 7, 3, 9, 10, 4, 8, 7, 9, 2, 10, 9, 5, 4, 1, 9]
    # r=[63,4,63,99,73,20,37,40,77,112,62,36,52,22,9,6,51,76,219,118]

    p = np.random.randint(1,100,job_num).tolist()
    w = np.random.randint(1,20,job_num).tolist()
    r = np.random.randint(1,300,job_num).tolist()

    global data
    data = []
    for i in range(job_num):
        data += [[r[i],p[i],w[i]]]
        # data += [[0,p[i],w[i]]]

    print(data)

    def make_problem():
        problem = pulp.LpProblem("minimize_weight_job_cost", pulp.LpMinimize)

        variable = []
        for j in range(job_num):
            variable += [pulp.LpVariable(f"c_{j}",0 ,sys.maxsize,pulp.LpContinuous)]

        loss = None
        for i in range(job_num):
            loss += variable[i]*data[i][2]

        problem += loss

        for i in range(job_num):
            problem += variable[i] >= data[i][0] + data[i][1]

        return problem, variable

    def make_s(S,data=None):
        if len(S)==0:
            S.append([0])
            # S.append([3,4])
            # S.append([0,1,2,3,4])
        else:
            # S.append(data.tolist())
            S += data
        print("S : {}".format(S))

    def optimize(problem, variable, S):
        for s in S:
            left = 0
            for j in s:
                left += variable[j]*data[j][1]
            right1 = 0
            right2 = 0
            for j in s:
                right1 += data[j][1]**2
                right2 += data[j][1]
            right2 = right2 ** 2
            right = 0.5*right1 + 0.5*right2
            problem += left >= right

        print(problem)
        result_status = problem.solve()
        print(pulp.LpStatus[result_status])
        return result_status

    def print_result(variable):
        result = []
        for v in variable:
            result.append(v.value())
        print(result)
        return result

    """
    ジョブを処理の早い順に並べた時の順番をidxで得る=ジョブの順番になる
    ジョブの順番ベクトルができたら、Sの部分集合を作る
    制約式にぶっこむ
    """
    def check_result(variable):
        result = []
        out = []
        for v in variable:
            result.append(v.value())
        result = np.array(result)
        sorted_job = np.argsort(result)
        l, = sorted_job.shape
        for i in range(l):
            idx = np.arange(0,i+1)
            j = sorted_job[idx]
            time = result[j]
            boo = check_constraint(j, time)
            if not boo:
                out.append(j.tolist())
        return out


    # 制約式の値を見る
    def check_constraint(job, time):
        eps = 0.001
        left = 0
        for i,j in enumerate(job):
            left += time[i]*data[j][1]
        right1 = 0
        right2 = 0
        for j in job:
            right1 += data[j][1]**2
            right2 += data[j][1]
        right = 0.5*right1 + 0.5*right2**2
        print("job : {}    {} >= {}  this is {}".format(job,left,right,left + eps >= right))
        return left + eps >= right
        
    start_time = time.time()
    count = 0
    max_count = 2**job_num - 1
    add_data = None# 追加ジョブ
    S = []# ジョブ集合
    while True:
        count += 1
        if count>max_count:
            print("wrong answer")
            break
        problem, variable = make_problem()
        make_s(S,add_data)
        status = optimize(problem, variable, S)
        if pulp.LpStatus[status]!="Optimal":
            print("the result was not optimal")
            break
        result = print_result(variable)
        add_data = check_result(variable)
        if len(add_data) == 0:
            print("we get correct answer")
            break
    
    pass_time = time.time() - start_time
    print(count)

    return pass_time, result, count

if __name__=="__main__":
    _,_,_ = all(20)
