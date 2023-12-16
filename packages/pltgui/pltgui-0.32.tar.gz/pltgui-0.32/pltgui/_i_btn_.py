#coding=utf-8

"""
一个在plt.ion之后的交互式界面上提供按钮的库
"""


import numpy as np
from matplotlib import pyplot as plt


class i_button:
    """
    按钮类，主要负责画按钮，以及获取和设置按钮的部分信息
    """

    def __init__(
            self,
            ax, ct_x, ct_y, wid, hei,
            color, text, cmd,
            action=None,
            fill=True, chk_color=None, chk_text=None):
        """
        在画布上画一个按钮出来 Draw a button on the axis
        :param ax: 画布对象 the axis
        :param ct_x, ct_y: 中心坐标 center x&y
        :param wid, hei: 宽度和高度（全宽、全高） full width and height
        :param color: 按钮的背景颜色 background color
        :param text: 按钮文字 text on button
        :param cmd: 按钮命令关键字 command keyword
        :param action: 按钮的回调函数，必须有个参数是按钮（方便多个按钮共用一个函数） call back function
        :param fill: 如果为真，则绘制一个实心的盒子，否则是空心的 fill the button or not
        :param chk_color: 当按钮打标签的时候的颜色 bg color when checked
        :param chk_text: 当按钮打标签的时候的文字 text then checked
        """
        # 保存信息
        self.ax    = ax
        self.ct_x  = ct_x
        self.ct_y  = ct_y
        self.wid   = wid
        self.hei   = hei
        self.cmd   = cmd
        self._color_ = color
        self._text_ = text
        self.action = action
        self.fill  = fill
        self._chked_ = False
        self.chk_color = chk_color if chk_color else color
        self.chk_text  = chk_text if chk_text else text
        # 计算x和y边界（内部用）
        xr = self._xr_ = np.array([-0.5, 0.5]) * wid + ct_x
        yr = self._yr_ = np.array([-0.5, 0.5]) * hei + ct_y
        # 画图
        self._p_box_ = ax.fill(xr[[0,1,1,0]], yr[[0,0,1,1]], color=color, fill=fill)[0]
        # 如果是实心的，写在中心，颜色是黑色，否则就写到右上角
        if fill:
            self._p_txt_ = ax.text(ct_x, ct_y, text, color="k", ha="center", va="center")
        else:
            self._p_txt_ = ax.text(ct_x + wid / 2, ct_y + hei / 2, text, color=color, ha="left", va="bottom")

    @property
    def text(self):
        """
        读取文字的属性 get and set of the text
        """
        return self._text_

    @text.setter
    def text(self, text):
        """
        文字属性的写函数
        """
        self._text_ = text
        self._p_txt_.set_text(text)

    @property
    def color(self):
        """
        读取背景颜色的属性 get and set the bg color
        """
        return self._color_

    @color.setter
    def color(self, color):
        """
        颜色属性的写函数
        """
        self._color_ = color
        self._p_box_.set_color(color)
        if not self.fill:
            self._p_txt_.set_color(color)

    @property
    def chked(self):
        """
        读取是否打标签 get and set the checked property
        """
        return self._chked_

    @chked.setter
    def chked(self, c):
        """
        设置标签状态
        :param c:
        :return:
        """
        self._chked_ = c
        if c:
            self._p_txt_.set_text(self.chk_text)
            self._p_box_.set_color(self.chk_color)
        else:
            self._p_txt_.set_text(self._text_)
            self._p_box_.set_color(self._color_)

    def check(self):
        """
        直接打标签 check the button
        :return:
        """
        self.chked = True

    def uncheck(self):
        """
        直接取消标签 uncheck the button
        :return:
        """
        self.chked = False

    def toggle_check(self):
        """
        直接标签状态反转 toggle the check status
        :return:
        """
        self.chked = not self.chked

    def remove(self):
        """
        删除自己，但是在按钮管理器中的记录需要另外删 remove the button
        """
        self._p_box_.remove()
        self._p_txt_.remove()

    def move(self, ct_x, ct_y):
        """移动按钮，指定新的中心点"""
        self.reloc(ct_x, ct_y, None, None)
    
    def resize(self, wid, hei):
        """调整按钮大小"""
        self.reloc(None, None, wid, hei)
    
    def reloc(self, ct_x=None, ct_y=None, wid=None, hei=None):
        """调整按钮位置和大小"""
        # 先处理默认值，这个功能主要是外部直接调用时用的
        ct_x = self.ct_x if ct_x is None else ct_x
        ct_y = self.ct_y if ct_y is None else ct_y
        wid  = self.wid  if wid  is None else wid
        hei  = self.hei  if hei  is None else hei
        # 设置新的位置
        self.ct_x = ct_x
        self.ct_y = ct_y
        self.wid  = wid 
        self.hei  = hei 
        # 计算x和y边界
        self._xr_ = np.array([-0.5, 0.5]) * wid + ct_x
        self._yr_ = np.array([-0.5, 0.5]) * hei + ct_y
        # 移动内容
        self._p_box_.set_xy([
            (self._xr_[0], self._yr_[0]),
            (self._xr_[1], self._yr_[0]),
            (self._xr_[1], self._yr_[1]),
            (self._xr_[0], self._yr_[1]),
        ])
        # 如果是实心的，写在中心，颜色是黑色，否则就写到右上角
        if self.fill:
            self._p_txt_.set_x(ct_x)
            self._p_txt_.set_y(ct_y)
        else:
            self._p_txt_.set_x(ct_x + wid / 2)
            self._p_txt_.set_y(ct_y + hei / 2)


class i_btn_ctl:
    """
    按钮管理器，需要维持一个按钮列表，以及识别是哪个按钮被按到了
    """
    
    def __init__(self, ax, defa_btn_action=None, image_action=None, loop_action=None):
        """
        :param ax: 画布 the axes
        :param defa_btn_action: 假如点击的按钮没有自带的处理函数，那么调用该函数，必须有个参数是按钮
        the default button action call back function
        :param image_action: 假如点击的是图像区域，不是按钮，调用这个，参数x、y
        the call back function if click on the image area, or on non button area
        :param loop_action: 假如超时没点击，执行本函数
        the call back function if timeout
        """
        # 画布
        self.ax = ax
        self.fig = ax.figure
        # 预设操作
        self.defa_btn_action = defa_btn_action
        self.image_action = image_action
        self.loop_action = loop_action
        # 按钮数组
        self.btns = []
        # 记录按钮的左、右、上、下界限
        self._range_l_ = []
        self._range_r_ = []
        self._range_t_ = []
        self._range_b_ = []
    
    def add_btn(self, ct_x, ct_y, wid, hei, bgc, text, cmd, action=None, fill=True, chk_color=None, chk_text=None):
        """
        添加按钮，参数都是按钮的 add a new button
        :param ct_x, ct_y: 中心坐标 center x&y
        :param wid, hei: 宽度和高度（全宽、全高） full width and height
        :param color: 按钮的背景颜色 background color
        :param text: 按钮文字 text on button
        :param cmd: 按钮命令关键字 command keyword
        :param action: 按钮的回调函数，必须有个参数是按钮（方便多个按钮共用一个函数） call back function
        :param fill: 如果为真，则绘制一个实心的盒子，否则是空心的 fill the button or not
        :param chk_color: 当按钮打标签的时候的颜色 bg color when checked
        :param chk_text: 当按钮打标签的时候的文字 text then checked
        """
        # 添加按钮
        bb = i_button(self.ax, ct_x, ct_y, wid, hei, bgc, text, cmd, action, fill, chk_color, chk_text)
        # 按钮加入列表
        self.btns.append(bb)
        # 记录其四界
        self._range_l_.append(bb._xr_[0])
        self._range_r_.append(bb._xr_[1])
        self._range_b_.append(bb._yr_[0])
        self._range_t_.append(bb._yr_[1])
        return bb

    def remove_btn(self, btn):
        """
        删除指定按钮，同时要删除边界信息
        remove the button
        """
        if btn in self.btns:
            i = self.btns.index(btn)
            btn.remove()
            del self.btns[i]
            del self._range_l_[i]
            del self._range_r_[i]
            del self._range_t_[i]
            del self._range_b_[i]

    def clear(self):
        """
        删除所有按钮
        delete all buttons
        :return:
        """
        for b in self.btns:
            b.remove()
        self.btns.clear()
        self._range_l_.clear()
        self._range_r_.clear()
        self._range_t_.clear()
        self._range_b_.clear()
    
    def move_btn(self, btn, ct_x, ct_y):
        """移动按钮，指定新的中心点"""
        self.reloc_btn(btn, ct_x, ct_y, None, None)
    
    def resize_btn(self, btn, wid, hei):
        """调整按钮大小"""
        self.reloc_btn(btn, None, None, wid, hei)
    
    def reloc_btn(self, btn, ct_x=None, ct_y=None, wid=None, hei=None):
        """调整按钮位置和大小"""
        # 判断按钮是不是本地的，如果是就移动
        if btn in self.btns:
            i = self.btns.index(btn)
            # 先处理默认值，这个功能主要是外部直接调用时用的
            ct_x = btn.ct_x if ct_x is None else ct_x
            ct_y = btn.ct_y if ct_y is None else ct_y
            wid  = btn.wid  if wid  is None else wid
            hei  = btn.hei  if hei  is None else hei
            
            btn.reloc(ct_x, ct_y, wid, hei)
            self._range_l_[i] = btn._xr_[0]
            self._range_r_[i] = btn._xr_[1]
            self._range_b_[i] = btn._yr_[0]
            self._range_t_[i] = btn._yr_[1]

    def set_axis_lim(self, padding=0.02):
        """
        对于专门用于部署按钮的ax，根据按钮情况，设置画布的四界，并且关闭坐标轴显示
        对于按钮和其他操作对象混合在一起的模式，不宜用本函数
        set the x&y limit of the axis, and cancel the axis
        :param padding: 按钮之外和画框保持的距离，实际宽度的倍数 the padding between buttons and the border
        """
        # 根据所有按钮的上下左右边界，计算总的外框
        xlim_l = min(self._range_l_)
        xlim_r = max(self._range_r_)
        ylim_t = max(self._range_t_)
        ylim_b = min(self._range_b_)
        # 定义一个计算线性外展的函数
        ext = lambda u, v, f: u * (1-f) + v * f
        # 向外适当扩展，设置画布大小
        self.ax.set_xlim(ext(xlim_l, xlim_r, -padding), ext(xlim_l, xlim_r, 1+padding))
        self.ax.set_ylim(ext(ylim_b, ylim_t, -padding), ext(ylim_b, ylim_t, 1+padding))
        # 关闭坐标轴
        self.ax.set_axis_off()

    def _locate_(self, x, y):
        """
        根据xy坐标看落在哪个按钮的区域内，也可能不再任何一个按钮内
        locate the button if a click happened, maybe on non-button area
        :param x, y: 点击坐标
        :return: 按钮，或者None
        """
        # 根据四界去判断xy是否在某个按钮区域内
        inside = (
            (np.array(self._range_l_) <= x) &
            (np.array(self._range_r_) >= x) &
            (np.array(self._range_b_) <= y) &
            (np.array(self._range_t_) >= y)
        )
        # 找满足条件的按钮，如果只有1个按钮满足，那就是它
        # 如果一个都没有（在所有按钮之外，甚至其它ax），或者按钮之间有重叠，当做没按到
        i = np.where(inside)[0]
        if len(i) == 1:
            btn = self.btns[i[0]]
        else:
            btn = None
        return btn

    def _wait_click_(self, timeout=1):
        """
        接收用户在图上点击，判断是否按了按钮，返回按钮、按钮命令、点击位置
        wait the user to click on the figure before timeout
        :param timeout: 默认超时时间，在此之前没有点击就返回空
        :return: 按钮、按钮命令、点击x、点击y  button object, button command, x, and y
        """
        # 从图上获取一个点
        p = self.fig.ginput(timeout=timeout)
        # 默认是1秒超时，超时之后会返回空列表，超时就直接跳过
        if p:
            px, py = p[0]
            # 转换成按钮，并获取按钮的命令
            btn = self._locate_(px, py)
            # 如果选中了按钮，那么获取按钮的命令，否则命令为空
            c = btn.cmd if btn else ""
        else:
            px, py = None, None
            btn, c = None, ""
        return btn, c, px, py

    def action_loop(self, timeout=1, ):
        """
        操作循环，一个无限循环地接受点击和执行操作的函数，参数主要是超时和默认处理函数
        假如点了按钮，并且按钮有自带事件函数，调自带的，否则调按钮默认处理函数，按钮作为参数
        假如点了图像位置，按钮为空，那么调图像点击函数
        如果啥都没点，超时返回，那么调研默认处理函数
        如果某一步没有指定函数（None），那么不处理
        :param timeout: 按钮检测超时秒数
        :return: nothing
        """
        
        # 先假设要无限循环。每一步的返回值如果不是空或者False，就表示要结束循环了
        done = False
        close = False
        
        def closing(event):
            nonlocal close
            close = True
        
        event_close = plt.connect("close_event", closing)
        
        while not done and not close:
            # 接收点击
            b, c, px, py = self._wait_click_(timeout=timeout)
            if b:
                done = b.action(b) if b.action else (self.defa_btn_action(b) if self.defa_btn_action else None)
            elif px:
                done = self.image_action(px, py) if self.image_action else None
            else:
                done = self.loop_action() if self.loop_action else None

        plt.disconnect(event_close)


# 20231020: add multi-ax
class m_ctl:
    """多画布控制器"""
    
    def __init__(self, ax_lst, defa_btn_action=None, image_action=None, loop_action=None):
        """创建一个跨画布的控制器，每个控制器也可以独立使用。
        :param ax: 画布 the axes
        :param defa_btn_action: 假如点击的按钮没有自带的处理函数，那么调用该函数，必须有个参数是按钮
        the default button action call back function
        :param image_action: 假如点击的是图像区域，不是按钮，调用这个，参数x、y
        the call back function if click on the image area, or on non button area
        :param loop_action: 假如超时没点击，执行本函数
        the call back function if timeout
        """
        # 保存信息
        self._ax_lst_ = ax_lst
        # 这里要求所有按钮都在同一个fig，要不然没法做下去，这里不检查
        self.fig = ax_lst[0].figure
        # 创建对应的子控制器，用字典
        self.ctl_lst = {ax: i_btn_ctl(ax, defa_btn_action, image_action, loop_action) for ax in ax_lst}
        # 事件：这里不管事件，有设置都扔给下属的控制器
    
    def set_action(self, defa_btn_action=None, image_action=None, loop_action=None):
        if defa_btn_action:
            for c in self.ctl_lst.values():
                c.defa_btn_action = defa_btn_action
        if image_action:
            for c in self.ctl_lst.values():
                c.image_action = image_action
        if loop_action:
            for c in self.ctl_lst.values():
                c.loop_action = loop_action

    def add_btn(self, ctl_ax, ct_x, ct_y, wid, hei, bgc, text, cmd, action=None, fill=True, chk_color=None, chk_text=None):
        """
        在制定控制器中添加按钮，参数都是按钮的 add a new button
        :param ctl_ax: 指定的控制器或者画布，原则上必须是这里面掌控的
        :param ct_x, ct_y: 中心坐标 center x&y
        :param wid, hei: 宽度和高度（全宽、全高） full width and height
        :param color: 按钮的背景颜色 background color
        :param text: 按钮文字 text on button
        :param cmd: 按钮命令关键字 command keyword
        :param action: 按钮的回调函数，必须有个参数是按钮（方便多个按钮共用一个函数） call back function
        :param fill: 如果为真，则绘制一个实心的盒子，否则是空心的 fill the button or not
        :param chk_color: 当按钮打标签的时候的颜色 bg color when checked
        :param chk_text: 当按钮打标签的时候的文字 text then checked
        """
        if ctl_ax in self.ctl_lst:
            c = self.ctl_lst[ctl_ax]
        elif type(ctl_ax) is i_btn_ctl:
            c = ctl_ax
        else:
            return None
        return c.add_btn(ct_x, ct_y, wid, hei, bgc, text, cmd, action, fill, chk_color, chk_text)
    
    def remove_btn(self, btn, ctl=None):
        """删除按钮，如果指定了控制器就直接删，否则挨个找（其实这样更省事）
        :param btn: 要删除的按钮
        :param ctl: 要删除按钮的控制器，否则挨个去找
        """
        if type(ctl) is i_btn_ctl:
            ctl.remove_btn(btn)
        else:
            for c in self.ctl_lst.values():
                c.remove_btn(btn)
    
    def move_btn(self, btn, ct_x, ct_y):
        """移动按钮，指定新的中心点"""
        for c in self.ctl_lst.values():
            c.move_btn(btn, ct_x, ct_y)
    
    def resize_btn(self, btn, wid, hei):
        """调整按钮大小"""
        for c in self.ctl_lst.values():
            c.resize_btn(btn, wid, hei)
    
    def reloc_btn(self, btn, ct_x, ct_y, wid, hei):
        """调整按钮位置和大小"""
        for c in self.ctl_lst.values():
            c.reloc_btn(btn, ct_x, ct_y, wid, hei)
    
    def clear(self, ctl=None):
        """如果指定了控制器，清空其所有按钮。指定字符串all则晴空所有"""
        if type(ctl) is i_btn_ctl:
            ctl.clear()
        elif ctl == 'all':
            for c in self_ctl_lst.values():
                c.clear()
        else:
            pass
    
    def action_loop(self, timeout=1, ):
        """
        操作循环，一个无限循环地接受点击和执行操作的函数，参数主要是超时和默认处理函数
        假如点了按钮，并且按钮有自带事件函数，调自带的，否则调按钮默认处理函数，按钮作为参数
        假如点了图像位置，按钮为空，那么调图像点击函数
        如果啥都没点，超时返回，那么调研默认处理函数
        如果某一步没有指定函数（None），那么不处理
        :param timeout: 按钮检测超时秒数
        :return: nothing
        """
        
        # 先假设要无限循环。每一步的返回值如果不是空或者False，就表示要结束循环了
        done = False
        close = False
        in_ax = None
        
        def fig_close(event):
            # 关闭窗口就退出
            nonlocal close
            close = True
        
        def ax_enter(event):
            # 记录当前在哪个ax
            nonlocal in_ax
            in_ax = event.inaxes
        
        event_close = plt.connect("close_event", fig_close)
        event_enter = plt.connect("axes_enter_event", ax_enter)
        
        while not done and not close:
            # 从图上获取一个点
            p = self.fig.ginput(timeout=timeout)
            # 默认是1秒超时，超时之后会返回空列表，超时就直接跳过
            if p and in_ax in self.ctl_lst:
                px, py = p[0]
                # 转换成按钮，并获取按钮的命令
                ctl = self.ctl_lst[in_ax]
                btn = ctl._locate_(px, py)
            else:
                px, py = None, None
                ctl = None
                btn = None
            
            if btn:
                done = btn.action(btn) if btn.action else (ctl.defa_btn_action(btn) if ctl.defa_btn_action else None)
            elif px:
                done = ctl.image_action(px, py) if ctl.image_action else None
            elif ctl:
                done = ctl.loop_action() if ctl.loop_action else None
            else:
                pass

        plt.disconnect(event_close)
        plt.disconnect(event_enter)


if __name__ == "__main__":
    print("This is a pltgui package.")
