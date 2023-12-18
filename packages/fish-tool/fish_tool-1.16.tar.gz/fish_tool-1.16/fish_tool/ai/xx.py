class Changer:
    SIMPLE = '悦悫悬悭悯惊惧惨惩惫惬惭惮惯愍愠愤愦愿慑慭憷懑懒懔戆戋戏戗战戬户扎扑扦执扩扪扫扬扰抚抛抟抠抡抢护报担拟拢拣拥拦拧拨择挂挚挛挜挝挞挟挠挡挢'
    TRADITION = '萬與醜專業叢東絲丟兩嚴喪個爿豐臨為麗舉麼義烏樂喬'

    def __init__(self):
        assert len(self.SIMPLE) == len(self.TRADITION)
        self.tradition__simple = {
            '⼥': '女',
            'Α': 'A',
            'ａ': 'a',
            'Ρ': 'P',
            'Τ': 'T',
            'ｃ': 'c',
            'ｓ': 's',
            'ɡ': 'g',
            'ｎ': 'n',
            'ｔ': 't',
            '﹢': '+',
            'ハ': '八',
            '⾃': '自',
            ' ': ' ',
        }
        for idx in range(len(self.SIMPLE)):
            self.tradition__simple[self.TRADITION[idx]] = self.SIMPLE[idx]

    def char_to_simple(self, char):
        return self.tradition__simple.get(char, char)

    def txt_to_simple(self, txt):
        chars = [self.char_to_simple(char) for char in txt]
        return ''.join(chars)


def get_next_char(bytes_s, index):
    # 从字节序列中获取下一个字符
    # index是当前字符的索引
    # 返回一个元组(字符, 下一个字符的索引)
    # 如果已经到达序列末尾，返回('', -1)

    # 检查当前字节是否是UTF-8字符的前缀
    if index + 1 < len(bytes_s) and bytes_s[index:index + 2] == b'\xE3\x80':
        # 如果当前字节是UTF-8字符的前缀，那么下一个字符的索引是当前索引+2
        return (bytes_s[index:index + 2].decode('utf-8'), index + 2)
    elif index + 2 < len(bytes_s) and bytes_s[index:index + 3] == b'\xE3\x80\x81':
        # 如果当前字节和下一个字节是UTF-8字符的前缀，那么下一个字符的索引是当前索引+3
        return (bytes_s[index:index + 3].decode('utf-8'), index + 3)
    else:
        # 如果当前字节不是UTF-8字符的前缀，那么下一个字符的索引是当前索引+1
        return (bytes_s[index].decode('utf-8'), index + 1)


# s = "你好"
# bytes_s = s.encode("utf-8")
# # 示例
# index = 0
# while index < len(bytes_s):
#     char, index = get_next_char(bytes_s, index)
#     print(char)
# exit()
if __name__ == '__main__':
    changer = Changer()
    print(changer.txt_to_simple('猶豫不決就會失敗askdj121j23!!@#!@'))
    print(len(changer.SIMPLE))
