import random

def dynamic_decision_making(N, K):
    print('begin pre planning for %d UAVs' % N)
    waypoint_list = pre_planning(N, [i for i in range(N)], K)
    Remain_UAV = [i for i in range(N)]
    print('complete pre planning for %d UAVs'% N)

    print('begin collect battle field information')
    step_information_collecting = 1
    Target = []
    while step_information_collecting <= 7:
        Target = information_collecting(Target)
        step_information_collecting = step_information_collecting + 1
    print('complete collect battle field information, and have found %d targets in the first state' % len(Target))

    print('begin make decisions')
    index_decision_making = 1
    Remain_Target = Target.copy()
    count = 1
    while count <= 100 and Remain_UAV: # 作战时间未到或仍有我方UAV剩余
        if index_decision_making and Remain_Target: # 可以开始进行决策 & 找到的目标集合非空
            print('make decision for founded target')
            Remain_UAV.clear()
            for i in range(len(Remain_Target)):
                for j in range(len(waypoint_list)):
                    if waypoint_list[j][-1] == 1:
                        Remain_UAV.append(j)
                UAV_index=random.choice(Remain_UAV) # 随机选择一个UAV对该target i进行打击
                waypoint_list[UAV_index][-1] = 2
                Target[i][-1] = 2
                print('at step %d' %count, 'remain UAVs are ', Remain_UAV)
                print('at step %d'% count,'UAV %d'% UAV_index, 'is used to attack target %d' %i)
                Remain_UAV.clear()
                count += 1
            Remain_Target = []
            for i in range(len(waypoint_list)):
                if waypoint_list[i][-1] == 1:
                    Remain_UAV.append(i)
            print('Remain targets are ', Remain_Target,'Remain UAVs are ', Remain_UAV)
        elif index_decision_making and len(Remain_Target)==0 and Remain_UAV:
            print('begin to look for new targets and make decisions')
            Remain_UAV.clear()
            for i in range(len(waypoint_list)):
                if waypoint_list[i][-1] == 1:
                    Remain_UAV.append(i)
            waypoint_list = pre_planning(N, Remain_UAV, K)
            Remain_Target = information_collecting(Remain_Target)
            if Remain_Target:
                print('find a new target')
            else:
                print('did not find a new target and continue searching')
            Target.append(Remain_Target)
            count += 1

def pre_planning(N, Index, K): # N UAV个数; K 航点步数；W 战场长度；L 战场宽度；R UAV特性参数，例如转弯半径
    waypoint_list = []
    for i in range(N):
        waypoint_list.append([])
        for j in range(K):
            temp=[random.random(), random.random()]
            waypoint_list[i].append(temp)
        waypoint_list[i].append(0)
        if i in Index:
            waypoint_list[i][-1] = 1
        else:
            waypoint_list[i][-1] = 2
    return waypoint_list

def information_collecting(Target): # return的是目标信息列表
    if random.random() < 0.5:
        Target.append([random.random(), random.random(), 1]) # x坐标，y坐标，标志位（=1 未被打击；=2 已被打击）
    return Target

# test
dynamic_decision_making(7,2)