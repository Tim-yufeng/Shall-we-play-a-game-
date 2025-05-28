import matplotlib.pyplot as plt
import matplotlib
import textwrap

def intro_of_game():
    plt.figure()
    # 设置中文字体
    matplotlib.rcParams['font.family'] = 'SimHei'
    matplotlib.rcParams['axes.unicode_minus'] = False

    text = ("""欢迎来玩南京高校拟人系列小游戏！！在这里你可以快速了解游戏规则
    
            你将通过左右键操作下方的学校意识体向左向右移动，
            
            在第一回合里，你将帮助国立中央大学意识体接住那些属于他的年份，获得相应积分
            
            （*不包含他解体的那一年哦，你还记得央大是哪一年解体的吗~）
            
            如果在积分达到100前，央大碰到了不属于他的年份，你就失败喽
            
            积分达到100后，你就可以进入第二回合啦！
            
            在第二回合里，你将帮助南京大学意识体接住那些掉下来的南京高校，
            
            （*但是高校名都是英文简写哦，你熟悉南京高校的英文简写吗~）
            
            不是每个高校都可以接哦，你只有接住那些中央家族的高校才能获得分数，
            
            但是接错了会倒扣分数哦。
            
            （*对了，每个高校对应积分的绝对值可能和该学校实力正相关哦~）
            
            你在刚开始拥有10分，达到100分你就赢啦！但是如果分数减至0分你就失败喽。
            
            准备好了吗？关闭这个窗口，让我们开始吧！""")
    wrapped_text = textwrap.fill(text, width=40)

    # 在整个图形上居中（0.5, 0.5 表示正中间）
    plt.figtext(
        0.5, 0.5, wrapped_text,
        ha='center', va='center',
        bbox=dict(facecolor='white', alpha=0.8),
        fontsize=10,
    )

    plt.show()

if __name__ == '__main__':
    intro_of_game()