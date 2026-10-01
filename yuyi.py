import sys

# ====== 伏羲先天八卦和六十四卦 ======
# 定义基础的八卦 3-bit 编码 (从下往上: 右到左)
BAGUA_MAP = {
    0b000: "坤为地 ☷", 0b001: "艮为山 ☶", 0b010: "坎为水 ☵", 0b011: "巽为风 ☴", 0b100: "震为雷 ☳", 0b101: "离为火 ☲", 0b110: "兑为泽 ☱", 0b111: "乾为天 ☰"
}
GUA64_MAP = {
    0b000000: "坤为地 ䷁", 0b000001: "山地剥 ䷖", 0b000010: "水地比 ䷇", 0b000011: "风地观 ䷓", 0b000100: "雷地豫 ䷏", 0b000101: "火地晋 ䷢", 0b000110: "泽地萃 ䷬", 0b000111: "天地否 ䷋",
    0b001000: "地山谦 ䷎", 0b001001: "艮为山 ䷳", 0b001010: "水山蹇 ䷦", 0b001011: "风山渐 ䷴", 0b001100: "雷山小过 ䷽", 0b001101: "火山旅 ䷷", 0b001110: "泽山咸 ䷞", 0b001111: "天山遁 ䷠",
    0b010000: "地水师 ䷆", 0b010001: "山水蒙 ䷃", 0b010010: "坎为水 ䷜", 0b010011: "风水涣 ䷺", 0b010100: "雷水解 ䷧", 0b010101: "火水未济 ䷿", 0b010110: "泽水困 ䷮", 0b010111: "天水讼 ䷅",
    0b011000: "地风升 ䷭", 0b011001: "山风蛊 ䷑", 0b011010: "水风井 ䷯", 0b011011: "巽为风 ䷸", 0b011100: "雷风恒 ䷟", 0b011101: "火风鼎 ䷱", 0b011110: "泽风大过 ䷛", 0b011111: "天风姤 ䷫",
    0b100000: "地雷复 ䷗", 0b100001: "山雷颐 ䷚", 0b100010: "水雷屯 ䷂", 0b100011: "风雷益 ䷩", 0b100100: "震为雷 ䷲", 0b100101: "火雷噬嗑 ䷔", 0b100110: "泽雷随 ䷐", 0b100111: "天雷无妄 ䷘",
    0b101000: "地火明夷 ䷣", 0b101001: "山火贲 ䷕", 0b101010: "水火既济 ䷾", 0b101011: "风火家人 ䷤", 0b101100: "雷火丰 ䷶", 0b101101: "离为火 ䷝", 0b101110: "泽火革 ䷰", 0b101111: "天火同人 ䷌",
    0b110000: "地泽临 ䷒", 0b110001: "山泽损 ䷨", 0b110010: "水泽节 ䷻", 0b110011: "风泽中孚 ䷼", 0b110100: "雷泽归妹 ䷵", 0b110101: "火泽睽 ䷥", 0b110110: "兑为泽 ䷹", 0b110111: "天泽履 ䷉",
    0b111000: "地天泰 ䷊", 0b111001: "山天大畜 ䷙", 0b111010: "水天需 ䷄", 0b111011: "风天小畜 ䷈", 0b111100: "雷天大壮 ䷡", 0b111101: "火天大有 ䷍", 0b111110: "泽天夬 ䷪", 0b111111: "乾为天 ䷀",
}
# ====== 十二消息卦 ======
XIAOXIGUA_MAP = {
    0b111000: "地天泰 ䷊",      # 一月阳气重
    0b111100: "雷天大壮 ䷡",    # 二月阳气重
    0b111110: "泽天夬 ䷪",      # 三月阳气重
    0b111111: "乾为天 ䷀",      # 四月阳气重
    0b011111: "天风姤 ䷫",      # 五月阴气重
    0b001111: "天山遁 ䷠",      # 六月阴气重
    0b000111: "天地否 ䷋",      # 七月阴气重
    0b000011: "风地观 ䷓",      # 八月阴气重
    0b000001: "山地剥 ䷖",      # 九月阴气重
    0b000000: "坤为地 ䷁",      # 十月阴气重
    0b100000: "地雷复 ䷗",      # 十一阳气重
    0b110000: "地泽临 ䷒",      # 十二阳气重
}


# ====== 算法实现 ======
class ZhouYiEngine:
    def __init__(self, code_6bit: int):
        # 确保输入是 6-bit 整数 (0-63)
        self.code = code_6bit & 0b111111
        
    def 卦象(self) -> str:
        """打印当前卦的二进制形态（直观的六爻形态）"""
        lines = []
        for i in range(0, 6):
            bit = (self.code >> i) & 1
            lines.append("——" if bit == 1 else "--")
        return "\n".join(lines) + "\n" + GUA64_MAP.get(self.code)
        
    def 旁通(self):
        """虞翻旁通说：按位取反 (Bitwise NOT)"""
        result = ~self.code
        return ZhouYiEngine(result)

    def 互体(self):
        """虞翻互体说：利用位掩码(Mask)和位移(Shift)解包中间数据"""
        # 下互：取 2, 3, 4 爻
        lower_mask = (self.code & 0b011100) >> 2
        # 上互：取 3, 4, 5 爻
        upper_mask = (self.code & 0b001110) >> 1
        
        return BAGUA_MAP.get(lower_mask), BAGUA_MAP.get(upper_mask)

    def 汉明重量(self) -> int:
        """消息卦变说基础：统计阳爻(1)的数量，即 Hamming Weight"""
        return bin(self.code).count('1')

    def _单次互换(self, parent: int, target: int):
        """判断 parent 能否只经「一次两爻互换」变为 target（虞翻的「A x之y」）。

        原理：两卦异或 (XOR) 后恰好有 2 位为 1，这两位就是需要互换的爻。
        约定 bit5 = 初爻(第1爻)、bit0 = 上爻(第6爻)，与 GUA64_MAP 一致。
        能则返回互换的爻序 (x, y)（1=初爻 … 6=上爻），否则返回 None。
        """
        diff = parent ^ target
        if bin(diff).count("1") != 2:
            return None
        bits = [i for i in range(6) if (diff >> i) & 1]
        return tuple(sorted(6 - b for b in bits))

    def 消息卦变(self):
        """消息卦变说：把本卦归宗到「本源消息卦」，并给出单次爻变轨迹。

        依据 yuyi.md 的两条铁律：
          ① 汉明重量守恒——母卦与本卦的阳爻数相同，这是快速定位本源消息卦的依据；
          ② 只换一次爻——虞翻禁止「二变」，否则同一卦会有多条生成路径，
             卦变体系就失去确定性（小过䷽、中孚䷼ 正因必须二变而被列为特例）。

        返回 [(母卦编码, 爻序对 | None), ...]：
          - 爻序对 (x, y) 表示「母卦第 x 爻与第 y 爻互换」即得本卦，虞翻记作「x之y」；
          - None 表示本卦本身就是消息卦（零次爻变）；
          - 返回空列表 [] 表示无单次爻变路径，即小过 / 中孚两个特例。
        """
        weight = self.汉明重量()
        routes = []
        for parent in XIAOXIGUA_MAP:
            # 铁律①：汉明重量守恒
            if bin(parent).count("1") != weight:
                continue
            # 本卦本身就是消息卦，零次爻变
            if parent == self.code:
                routes.append((parent, None))
                continue
            # 铁律②：只允许「一次」两爻互换
            swap = self._单次互换(parent, self.code)
            if swap is not None:
                routes.append((parent, swap))
        return routes




if __name__ == "__main__":
    # 初始化卦象。1代表阳爻，0代表阴爻，从下往上描述。
    # 使用 python3 yuyi.py <二进制> 动态输入
    input_code = eval(sys.argv[1])
    input_gua = ZhouYiEngine(input_code) 

    print("输入二进制编码：", bin(input_gua.code))
    print("【当前卦象】:")
    print(input_gua.卦象())
    print(f"\n阳爻数量 (汉明重量): {input_gua.汉明重量()}")
    
    # 1. 运行旁通算法 (Bitwise NOT)
    pang_tong_卦 = input_gua.旁通()
    print(f"\n【旁通运算 (NOT)】: {bin(pang_tong_卦.code)}")
    print(pang_tong_卦.卦象()) # 会输出 001100 (雷山小过卦)
    
    # 2. 运行互体算法 (Mask & Shift)
    xia_hu, shang_hu = input_gua.互体()
    print(f"\n【互体解包 (Data Slicing)】:")
    print(f"下互卦 (第2-4爻): {xia_hu}")
    print(f"上互卦 (第3-5爻): {shang_hu}")

    # 3. 运行消息卦变算法 (Hamming Weight + XOR Swap)
    print(f"\n【消息卦变 (Hamming Weight + XOR Swap)】:")
    YAO = "初、二、三、四、五、上".split("、")
    routes = input_gua.消息卦变()
    if not routes:
        print("  无单次爻变路径——本卦属小过䷽ / 中孚䷼ 特例（须改从讼、晋等普通卦起变）")
    else:
        for parent, swap in routes:
            if swap is None:
                print(f"  本源消息卦：{GUA64_MAP[parent]}（本卦即消息卦，零次爻变）")
            else:
                x, y = swap
                print(f"  本源消息卦：{GUA64_MAP[parent]}  ——「{YAO[x - 1]}之{YAO[y - 1]}」互换第 {x}、{y} 爻即得本卦")
