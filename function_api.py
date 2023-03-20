import json
import requests


def get_profile(user_id):
    """
    정보 조회 - user_id를 입력하면 백준 사이트에서 해당 user의 프로필 정보 중 일부를 반환해줌.
    :param str user_id: 사용자id
    :return: 백준 프로필 정보
    :rtype: dict
    """
    url = f"https://solved.ac/api/v3/user/show?handle={user_id}"
    r_profile = requests.get(url)
    if r_profile.status_code == requests.codes.ok:
        profile = json.loads(r_profile.content.decode('utf-8'))
        profile = \
            {
                "tier": profile.get("tier"),
                "rank": profile.get("rank"),
                "solvedCount": profile.get("solvedCount"),
                "rating": profile.get("rating"),
                "exp": profile.get("exp"),
            }
    else:
        print("프로필 요청 실패")
    return profile


def get_solved(user_id):
    """
    정보 조회 - user_id를 입력하면 백준 사이트에서 해당 user가 푼 총 문제수, 문제들 정보(level 높은 순)를 튜플(int, list)로 반환해줌.
    :param str user_id: 사용자id
    :return: 내가 푼 문제수, 내가 푼 문제들 정보
    :rtype: int, list
    """
    num = 1
    counter = 0
    solved_problems = []

    while True:
        url = f"https://solved.ac/api/v3/search/problem?query=solved_by%3A{user_id}&sort=id&direction=asc&page={num}"
        r_solved = requests.get(url)

        if not (r_solved.status_code == requests.codes.ok):
            print("문제 실패")
            break
        solved = json.loads(r_solved.content.decode('utf-8'))
        count = solved.get("count")
        if counter == count:
            break
        items = solved.get("items")
        counter += len(items)
        for item in items:
            solved_problems.append(
                {
                    'problemId': item.get("problemId")
                }
            )
        num += 1

    return count, solved_problems


def get_count_by_level(user_id):
    """
    정보 조회 - user_id를 입력하면 백준 사이트에서 해당 user가 푼 문제들에 대한 level별 문제수 정보를 level 높은 순으로 반환해줌.
    :param str user_id: 사용자id
    :return: level별 총 문제수, 내가 푼 문제수
    :rtype: list
    """
    url = f"https://solved.ac/api/v3/user/problem_stats?handle={user_id}"
    r_count_by_level = requests.get(url)
    if r_count_by_level.status_code == requests.codes.ok:
        count_by_level = json.loads(r_count_by_level.content.decode('utf-8'))
        filted_count_by_level = [{"level": dict_['level'], "total": dict_['total'], "solved": dict_['solved'], } for
                                 dict_ in count_by_level if dict_.get('solved') != 0]
        filted_count_by_level = sorted(filted_count_by_level, key=lambda x: x['level'], reverse=True)
    else:
        print("레벨별, 전체 문제수, 푼 문제수  요청 실패")
    return filted_count_by_level
