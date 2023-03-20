import os
import random
import time

import function_api

if __name__ == '__main__':
    user_id = "nsw0720"
    count, sovled_list = function_api.get_solved(user_id)
    print("================================================")
    print(f"* 전체 문제 수: \"{count}\"")
    seed_value = int(time.time() * 1000) + os.getpid() + random.randint(1, 10000)
    random.seed(seed_value)
    random_number = random.randrange(0, count - 1)
    target_problem = sovled_list[random_number]['problemId']

    print(f"* 이번에 복습할 문제: \"{target_problem}\"")
    print(f"* 문제 url: https://www.acmicpc.net/problem/{target_problem}")
    print("================================================")