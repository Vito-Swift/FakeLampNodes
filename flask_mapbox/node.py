#!/usr/bin/python3

import time
import random
import threading
import socket
import numpy
import os


def output_datapoint(metric_name: str, measured_value: int, timestamp: int):
    pass
    # message = "{} {:d} {:d}\n".format(metric_name, int(measured_value), int(timestamp))
    # print(message)
    #
    # # Test with `nc -lvukw 0 127.0.0.1 2003`
    # try:
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #
    #     sock.settimeout(1.0)
    #     sock.connect(('localhost', 2003))
    #     message = bytes(message, 'utf-8')
    #     sock.send(message)
    #     sock.close()
    # except:
    #     pass


global_cpuUsage = {}
global_networkUsage = {}


def update_cpuUsage(timeStamp: int, id: int, taskType: int):
    global_cpuUsage[id] = (timeStamp, taskType)


def update_networkUsage(timeStamp: int, node1_id: int, node2_id: int, speed: int):
    global_networkUsage[(node1_id, node2_id)] = (timeStamp, speed)


def generate_volateData(value, Volatility, lowerLimit, upperLimit):
    _min = value - Volatility if value - Volatility >= lowerLimit else lowerLimit
    _max = value + Volatility if value + Volatility <= upperLimit else upperLimit
    _max = _max if _max > _min else _min
    re = random.randint(_min, _max)
    return re


def generate_normalDistribution(value, deviation, lowerLimit, upperLimit):
    re = numpy.random.normal(value, deviation)
    re = re if re >= lowerLimit else lowerLimit
    re = re if re <= upperLimit else upperLimit
    return re


class TASK:
    IDLE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    DEAD = 4


class Node:

    def __init__(self, id: int):
        self.id = id

        self.taskType = 0
        self.taskTime = 0

        # lowerlimit, upperlimit, alert
        self.online = 0
        self.cpuUsage = 0  # [0, 100, 90]
        self.gpuUsage = 0  # [0, 100, 90]
        self.ramUsage = 0  # [0, 4000, 3600]
        self.temp = 0  # [10, 100, 80]
        self.storageUsage = random.randint(2800, 3200)  # MB      # [0, 4000, 3600]
        self.rank = 0  # [0, 20, 1]

        self.is_running = False
        self.COLLECT_CYCLE = 5

        self.set_task(TASK.IDLE, 3)

        self._routine_thread = threading.Thread(target=self._routine)

    def _report(self):
        timeStamp = int(time.time())
        if self.id < 10 and self.online:
            self._report_cpuUsage(timeStamp)
            self._report_gpuUsage(timeStamp)
            self._report_ramUsage(timeStamp)
            self._report_temp(timeStamp)
            self._report_storageUsage(timeStamp)
            self._report_rank(timeStamp)
        if self.id < 10:
            self._report_online(timeStamp)

        update_cpuUsage(timeStamp, self.id, self.taskType)

        if (self.id not in [29, 59, 99, 74, 89]):  # In order to match the topology
            update_networkUsage(timeStamp, self.id, self.id + 1, random.randint(5, 50))
        elif (self.id == 74):
            update_networkUsage(timeStamp, self.id, 15, random.randint(5, 50))
        elif (self.id == 89):
            update_networkUsage(timeStamp, self.id, 45, random.randint(5, 50))
        if (self.id == 15):
            update_networkUsage(timeStamp, self.id, 75, random.randint(5, 50))
        elif (self.id == 45):
            update_networkUsage(timeStamp, self.id, 90, random.randint(5, 50))

    def _report_cpuUsage(self, timeStamp):
        # value = generate_volateData(self.cpuUsage, 10, 0, 100)
        value = generate_normalDistribution(self.cpuUsage, 10, 0, 100)
        output_datapoint("lampnets.cpuUsage.{}".format(self.id), value, timeStamp)

    def _report_gpuUsage(self, timeStamp):
        # value = generate_volateData(self.gpuUsage, 15, 0, 100)
        value = generate_normalDistribution(self.gpuUsage, 15, 0, 100)
        output_datapoint("lampnets.gpuUsage.{}".format(self.id), value, timeStamp)

    def _report_ramUsage(self, timeStamp):
        # value = generate_volateData(self.ramUsage, 50, 0, 4000)
        value = generate_normalDistribution(self.ramUsage, 50, 0, 4000)
        output_datapoint("lampnets.ramUsage.{}".format(self.id), value, timeStamp)

    def _report_temp(self, timeStamp):
        # value = generate_volateData(self.temp, 3, 10, 80)
        value = generate_normalDistribution(self.temp, 3, 10, 80)
        output_datapoint("lampnets.temp.{}".format(self.id), value, timeStamp)

    def _report_storageUsage(self, timeStamp):
        value = self.storageUsage
        output_datapoint("lampnets.storageUsage.{}".format(self.id), value, timeStamp)

    def _report_rank(self, timeStamp):
        # value = generate_volateData(self.rank, 2, 0, 20)
        value = generate_normalDistribution(self.rank, 1, 0, 20)
        output_datapoint("lampnets.rank.{}".format(self.id), value, timeStamp)

    def _report_online(self, timeStamp):
        value = self.online
        output_datapoint("lampnets.online.{}".format(self.id), value, timeStamp)

    def set_task(self, taskType, taskTime):
        self.taskType = taskType
        self.taskTime = taskTime
        if self.taskType == TASK.IDLE:
            self.online = 1
            self.cpuUsage = 5
            self.gpuUsage = 0
            self.ramUsage = 2200
            self.temp = 40
            self.rank = 16
        elif self.taskType == TASK.LOW:
            self.online = 1
            self.cpuUsage = 30
            self.gpuUsage = 20
            self.ramUsage = 2250
            self.temp = 50
            self.rank = 15
        elif self.taskType == TASK.MEDIUM:
            self.online = 1
            self.cpuUsage = 60
            self.gpuUsage = 50
            self.ramUsage = 2300
            self.temp = 55
            self.rank = 14
        elif self.taskType == TASK.HIGH:
            self.online = 1
            self.cpuUsage = 90
            self.gpuUsage = 85
            self.ramUsage = 2350
            self.temp = 60
            self.rank = 14
        elif self.taskType == TASK.DEAD:
            self.online = 0
            self.cpuUsage = 0
            self.gpuUsage = 0
            self.ramUsage = 0
            self.temp = 0
            self.rank = 0

    def start(self):
        self.is_running = True
        self._routine_thread.start()

    def stop(self):
        self.is_running = False
        self._routine_thread.join()

    def _routine(self):
        # if (self.id < 10):
        # os.nice(-self.id)
        collect_timer = 0
        task_timer = time.time()
        while self.is_running:
            if (time.time() - task_timer >= self.taskTime):
                task_timer = time.time()
                self.set_task(random.randint(0, 3), random.randint(30, 60))
                if (random.random() < 0.1):
                    self.set_task(4, random.randint(40, 70))

            if (time.time() - collect_timer >= self.COLLECT_CYCLE):
                collect_timer = time.time()
                self._report()
            time.sleep(0.1)


# random.seed(0)
# node = Node(0)
# node.start()
# time.sleep(5)
# node.stop()


# lampnet = [Node(i) for i in range(100)]
# for node in lampnet:
#     # time.sleep(random.random())
#     node.start()
#
# time.sleep(900)
#
# for node in lampnet:
#     node.stop()
