from MAControl.Base.PolicyMaker import PolicyMaker
import math
import random
import numpy as np
from MAControl.Util.PointInRec import point_in_rec

class PolicyMaker_Auciton_LJ(PolicyMaker):
    Found_Target_Set = []
    Found_Target_Info = []
    Shared_UAV_state = []
    Shared_Big_Check = False
    Selectable_UAV = []
    Target_is_sorted = False  # Resorted_Target是否已进行排序
    Resorted_Target = []  # 按优先级排序的拍卖目标
    Auctioneer = -1  # 选出的拍卖者编号
    Target_index = -1  # 当前进行拍卖的目标编号

    Winner = []  # 最终选出来的优胜者列表
    Price_list = []  # 选出的竞拍者发出的竞拍价格
    unassigned_list = []  # 没有分到任务的个体列表

    last_step = 0
    Trans_step = []  # 拍卖者发送出目标给竞拍者的延时step列表
    wait_step = 30  # 等待的时长
    wait_step_auction = 10  # 选拍卖者的等待时间
    Update_step = 0

    def __init__(self, name, env, world, agent_index, arglist):
        super(PolicyMaker_Auciton_LJ, self).__init__(name, env, world, agent_index, arglist)
        self.detect_dis = 0.05
        self.comm_dis = 0.5
        self.close_area = []
        self.trans_step = []
        self.x = 0
        self.y = 0

        self.opt_index = 0 #LJ
        self.share_info_step = 0 #LJ
        self.total_share_info_step = 20 #LJ

        PolicyMaker_Auciton_LJ.Shared_UAV_state.append(0)
        PolicyMaker_Auciton_LJ.unassigned_list.append(self.index)

    def add_new_target(self, obs, WorldTarget):
        TT_range = 0.05

        # COMPUTE selfview
        selfvel = np.array(obs[0:2])
        selfpos = np.array(obs[2:4])
        selfvelunit = selfvel / np.sqrt(np.dot(selfvel, selfvel))
        selfvelrightunit = np.array([selfvelunit[1], -1 * selfvelunit[0]])
        d1 = 0
        d2 = 0.5
        d3 = 0.5
        selfview1 = selfpos + selfvelunit * (d1 + d2) - selfvelrightunit * d3 / 2
        selfview2 = selfpos + selfvelunit * (d1 + d2) + selfvelrightunit * d3 / 2
        selfview3 = selfpos + selfvelunit * d1 + selfvelrightunit * d3 / 2
        selfview4 = selfpos + selfvelunit * d1 - selfvelrightunit * d3 / 2

        # GENERATE seen_target
        seen_target = []
        for target in WorldTarget:
            targetpos = np.array(target[1:3])
            if point_in_rec(selfview1, selfview2, selfview3, selfview4, targetpos):
                seen_target.append(target)

        # READ AND WRITE TESTControl.Found_Target_Set
        if PolicyMaker_Auciton_LJ.Found_Target_Set == []:
            PolicyMaker_Auciton_LJ.Found_Target_Set = seen_target
            for i in range(len(seen_target)):
                PolicyMaker_Auciton_LJ.Found_Target_Info.append(self.close_area)
        elif seen_target != []:
            for target1 in seen_target:
                check = False
                for target2 in PolicyMaker_Auciton_LJ.Found_Target_Set:
                    pos1 = np.array(target1[1:3])
                    pos2 = np.array(target2[1:3])
                    deltapos = np.sqrt(np.dot(pos1 - pos2, pos1 - pos2))
                    check = check | (deltapos <= TT_range)
                if not check:
                    PolicyMaker_Auciton_LJ.Found_Target_Set.append(target1)
                    PolicyMaker_Auciton_LJ.Found_Target_Info.append(self.close_area)

        # COMMUNICATE TESTControl.Found_Target_Info
        for info in PolicyMaker_Auciton_LJ.Found_Target_Info:
            check = False
            for num in self.close_area:
                check = check | num in info
            if check and (self.index not in info):
                info.append(self.index)

    def share_target_info(self, obs, WorldTarget):
        target_UAV_list=[]
        return target_UAV_list

    def make_policy(self, WorldTarget, obs_n, step):
        print('make policy LJ begins')
        # auction_index = 1 # for test
        auction_index = step > 100 and len(PolicyMaker_Auciton_LJ.Found_Target_Set) != 0 # 定义开启拍卖的条件【可根据自身要求进行修改】
        if auction_index == 0: # 判断是否开启拍卖 =1 是；=0 否
            self.opt_index = 0  # 按照航点飞行
            self.add_new_target(obs_n[self.index], WorldTarget)  # collect targets information and sort it
        # elif auction_index ==1: # for test
        elif auction_index ==1 and PolicyMaker_Auciton_LJ.last_step == step - 1: # begin auction simultaneously
            PolicyMaker_Auciton_LJ.last_step = step # ?
            while self.share_info_step < self.total_share_info_step: # 在一段时间内共享&更新目标列表信息
                self.share_target_info(obs_n, WorldTarget) # share_info # 共享信息函数，最后返回的应该是一个排好序的目标-UAV的price列表 & 自身的排名
                self.share_info_step = self.share_info_step + 1
            auction_index_i = 1 # 根据自身得到的列表信息确定是否去进行打击 To be specified
            if auction_index_i == 1:
                self.opt_index = 5 # 返回
                self.x = random.random()
                self.y = random.random()
        print('make policy LJ succeeds')
        print([self.opt_index, self.x, self.y])
        return [self.opt_index, self.x, self.y]



