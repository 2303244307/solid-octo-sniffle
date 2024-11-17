from django.test import TestCase

# Create your tests here.

# 测试正则表达式‘
import re


def IdUnid(Id: str) -> bool:
    """
    用以验证传入参数是否符合正则表达式’
    :param Id:用户id
    :return bool 布尔条件
    """
    print(Id)
    # 正则表达式的匹配
    m1 = re.match(r"\bhi\b", Id)
    return m1


if __name__ == '__main__':
    # 调用函数学习正则表达式
    a = input("请输入你需要验证的字符串内容:")
    flag = IdUnid(a)
    print(flag)
