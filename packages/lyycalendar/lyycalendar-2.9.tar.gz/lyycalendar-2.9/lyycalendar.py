import pandas as pd
from datetime import datetime, timedelta
import sys
import os


class lyycalendar_class:

    def __init__(self):

        # 创建 lyycalendar_class 的实例并在初始化时获取数据

        today = datetime.now().date()
        # 前200天日期
        previous_date = today - timedelta(days=200)

        # 后200天日期
        next_date = today + timedelta(days=200)

        previous_date_str = previous_date.strftime("%Y-%m-%d")
        next_date = today + timedelta(days=200)
        next_date_str = next_date.strftime("%Y-%m-%d")

        import exchange_calendars as xcals
        xshg = xcals.get_calendar("XSHG")

        df = xshg.schedule.loc[previous_date_str:next_date_str]
        dates = df.index
        # 将DatetimeIndex转换为整数格式（假设格式为YYYYMMDD）
        dayint = dates.strftime("%Y%m%d").astype(int)

        # 创建DataFrame，并添加dayint列
        self.calendar_df = pd.DataFrame({'dayint': dayint, 'date': dates})

    def day8to10(self, day8):
        """
        20221013 to 2022-10-13
        """
        day8 = str(day8)
        return day8[0:4] + "-" + day8[4:6] + "-" + day8[6:8]

    def sql_get_trade_calendars(self, debug=False):
        """
        连接mysql直接获取trade_calendars存入df返回
        """
        if debug:
            print(sys._getframe().f_code.co_name, self.calendar_df.dayint.to_list(), self.calendar_df)
        return self.calendar_df.dayint.to_list(), self.calendar_df

    def any_date_to_int(self, any_date):
        """
        将任意日期转前8位换成int型
        """
        any_date = str(any_date).replace("-", "")
        if isinstance(any_date, int):
            return any_date
        else:
            return int((any_date)[:8])

    def any_date_to_int_multi(self, *any_dates, debug=False):
        """
        将任意日期转前8位换成int型
        """
        result = []
        for any_date in any_dates:
            any_date = str(any_date).replace("-", "")
            if isinstance(any_date, int):
                result.append(any_date)
            else:
                if debug:
                    print("any_date=", any_date)
                result.append(int((any_date)[:8]))
        if len(result) == 1:
            return result[0]
        else:
            return tuple(result)

    def tc_close_to(self, date):
        """
        找到交易日历中最接近date的日期
        """
        date_int = self.any_date_to_int(date)
        df = self.calendar_df[self.calendar_df['dayint'] <= date_int]
        lastindex = len(df) - 1
        return df.iloc[lastindex]['dayint']

    def tc_close_to_data_from_time(self, date_time_str="now"):
        """
        任意%Y-%m-%d %H:%M:%S时间，找到最接近该时间的完整收盘日,支持字符串格式和日期时间格式
        """

        if date_time_str == "now":
            date_time_str = datetime.now()
            print("now", date_time_str, type(date_time_str))
        elif isinstance(date_time_str, str):
            date_time_str = date_time_str[:19]
            date_time_str = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            print(date_time_str, type(date_time_str))

        date = date_time_str.date()
        hour = date_time_str.hour

        if hour < 15:

            return (date - timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            return date.strftime('%Y-%m-%d')

    def get_previous_today(self, days, debug=False):
        """找到df中day为date的数据,并向前找到第50个值"""
        # 找到day为date的索引
        today_int = self.any_date_to_int(datetime.now())

        idx = self.calendar_df.index[self.calendar_df['dayint'] <= today_int][0]
        # 如果向前50个索引超出df范围,则从df开始算
        start = max(0, idx - 50)
        # 向前找到第50个值并返回
        return self.calendar_df.iloc[start]

    def tc_before_today(self, days, debug=False):
        """
        返回小于或等于今天的n天前日期
        """
        today_int = self.any_date_to_int(datetime.now())
        close_to_today = self.tc_close_to(today_int)
        # filter dates that are earlier than today
        index = self.calendar_df.index[self.calendar_df['dayint'] == close_to_today]
        if index - days >= 0:
            n天前日期 = self.calendar_df.iloc[index - days]['dayint'].values[0]
        else:
            print("此函数：", sys._getframe().f_code.co_name, "出错了")
        if debug:
            print(sys._getframe().f_code.co_name, "n天前日期=", n天前日期)
        # print("n天前日期=<",n天前日期,type(n天前日期))
        return n天前日期

    def 计算相隔天数(self, start_date, end_date, debug=False):
        """
        计算相隔天数
        """
        debug = True
        # 加入下面这行代码，以实现无论start大还是不小都能计算。
        if debug:
            print(sys._getframe().f_code.co_name, "计算相隔天数好像有错误，明明有了数据计算出来还有值")
        start_date, end_date = self.any_date_to_int_multi(start_date, end_date)
        if end_date > start_date:
            start_date, end_date = end_date, start_date

        filtered_df = self.calendar_df[(self.calendar_df['dayint'] <= start_date) & (self.calendar_df['dayint'] > end_date)]
        """     print(self.calendar_df)
                sn    dayint        day
        0      1  20210104 2021-01-04
        1      2  20210105 2021-01-05
        2      3  20210106 2021-01-06 
        """
        hour = datetime.now().hour
        print("hour=", hour)
        print("datetime.now().date().day ", datetime.now().date().day)
        print("end_date=", end_date, "start_date=", start_date)
        if 925 <= hour <= 1500 and datetime.now().date().day in filtered_df['dayint']:
            to_return = len(filtered_df) + 1
            print("符合条件，+1,toretun=", to_return)
        else:
            to_return = len(filtered_df)
            print("toreturn=", to_return)
        if debug:
            print("start_date=", start_date, "end_date=", end_date, "to_return=", to_return)

        return to_return

    def calc_days(self, start_date, end_date):

        def days_between(date1, date2):
            d1 = datetime.strptime(date1, '%Y%m%d')
            d2 = datetime.strptime(date2, '%Y%m%d')
            print("abs(d2-d1)=", abs(d2 - d1).days)
            return abs((d2 - d1).days)

        today = datetime.now().strftime('%Y%m%d')
        current_time = datetime.now().time()

        if today in self.calendar_df['day'].values:
            if current_time < datetime.time(9, 25):
                result = days_between(self.calendar_df[self.calendar_df['day'] == today].iloc[-1]['dayint'], today)
            else:
                result = days_between(self.calendar_df[self.calendar_df['day'] == today]['dayint'].iloc[0], today)
        else:
            result = days_between(self.calendar_df[self.calendar_df['day'] < today]['dayint'].iloc[-1], today)

        print(result)

    def 日历中最接近某天(self, date):
        """
        返回日历中最接近某天的日期
        """
        filtered_df = self.calendar_df[self.calendar_df['dayint'] <= self.any_date_to_int(date)]
        last_index = len(filtered_df) - 1
        print("last_index=", last_index)
        return filtered_df.iloc[last_index]['dayint']

    def 计算相隔天数_byIndex(self, d1, d2, now=False, debug=False):

        d1_int, d2_int = self.any_date_to_int_multi(d1, d2)
        if debug: print(f"d1_int, {d1_int}  d2_int={d2_int}")
        d1_index, d2_index = self.find_nearest_previous_date(d1_int), self.find_nearest_previous_date(d2_int)
        if debug: print(f"寻找最接近工作日索引结果： d1_index, {d1_index}  d2_index={d2_index}")
        diff = d2_index - d1_index

        if debug: print(f"diff, {diff}  ")
        today = datetime.now().strftime('%Y%m%d')
        today_int = self.any_date_to_int(today)

        # 获取当前时间
        current_time = datetime.now().time()
        # 定义目标时间
        target_time = datetime.strptime("09:25", "%H:%M").time()
        # 如果今天在日历有数据（工作日），计算相隔之前 ，还要判断当前时间是否早于09:25
        if d2_int == today_int and current_time < target_time:
            diff = diff - 1 if diff > 0 else diff
            #print("当前时间早于09:25,返回日期差额要减1,最后结果=", diff)

        if debug:
            print("end 计算天数 byindex = ", diff[0])
        return diff[0]

    def find_nearest_previous_date(self, date_int: int, debug=False) -> int:
        """
        找到日历中最接近给定日期的日期.当前全为int类型
        """
        # 将日期列转换为字符串格式

        # 根据字符串比较找到小于给定日期的最接近日期
        previous_date = self.calendar_df.loc[self.calendar_df['dayint'] <= date_int, 'dayint'].max()
        if debug:
            print(previous_date, "previous_date")
        # 获取最接近日期的索引
        previous_date_index = self.calendar_df.loc[self.calendar_df['dayint'] == previous_date].index
        # 发生异常: IndexError  index 0 is out of bounds for axis 0 with size 0
        if debug:
            print("result: previous_date_index=", previous_date_index[0])
        return previous_date_index

    def 最近完整收盘日(self, days, debug=False):
        """
        返回小于或等于今天的最近完整收盘日。如果今天是开盘日，则开市时间的完整收盘日为前一开盘日。因为当时并没有完整收盘数据。
        """
        today_int = self.any_date_to_int(datetime.now())

        if datetime.now().hour < 15:
            today_int = today_int - 1
        close_to_today = self.tc_close_to(today_int)
        # filter dates that are earlier than today
        index = self.calendar_df.index[self.calendar_df['dayint'] == close_to_today]

        if index - days >= 0:
            n天前日期 = self.calendar_df.iloc[index - days]['dayint'].values[0]
        else:
            print("此函数：", sys._getframe().f_code.co_name, "出错了")
        if debug:
            print(sys._getframe().f_code.co_name, "n天前日期=", n天前日期)
        # print("n天前日期=<",n天前日期,type(n天前日期))
        return n天前日期

    def 最近有数据日期(self, debug=False):
        """
        返回小于或等于今天的最近完整收盘日。如果今天是开盘日，则开市时间的完整收盘日为前一开盘日。因为当时并没有完整收盘数据。
        """
        now = datetime.now()
        today_int = int(now.strftime('%Y%m%d'))
        print("now=", now.hour, now, today_int, "type=", type(today_int))

        if now.hour < 9 or (now.hour == 9 and now.minute < 30):
            today_int = today_int - 1
            if debug: print("不到9:30，日期减1，最后today_int=", today_int)
        else:
            if debug: print("现在大于9:30，不减1，最后today_int=", today_int)
        df2 = self.calendar_df.loc[self.calendar_df['dayint'] <= today_int]

        # 找到最接近20230514的日期
        closest_date = df2['dayint'].max()
        if debug: print("closest_date=", closest_date)
        return closest_date


if __name__ == "__main__":
    # # 创建 lyycalendar_class 的实例并在初始化时获取数据
    # today = datetime.now().date()
    # # 前200天日期
    # previous_date = today - timedelta(days=200)

    # # 后200天日期
    # next_date = today + timedelta(days=200)

    # previous_date_str = previous_date.strftime("%Y-%m-%d")
    # next_date = today + timedelta(days=200)
    # next_date_str = next_date.strftime("%Y-%m-%d")

    # import exchange_calendars as xcals
    # xshg = xcals.get_calendar("XSHG")

    # df = xshg.schedule.loc[previous_date_str:next_date_str]
    # dates = df.index
    # # 将DatetimeIndex转换为整数格式（假设格式为YYYYMMDD）
    # dayint = dates.strftime("%Y%m%d").astype(int)

    # # 创建DataFrame，并添加dayint列
    # df = pd.DataFrame({
    #     'dayint': dayint,
    #     'date': dates
    # })

    lyytc = lyycalendar_class()

    # 调用库中的函数，将参数传递给它们
    print(lyytc.计算相隔天数_byIndex("2023-10-27", "2023-10-28"))

    # print("close to 20230101", 日历中最接近某天("2023-01-01"))
    # print("tc=", tc_before_today(50, True))
    # start_date = "2023-01-01"
    # end_date = "2023-02-02"
    # n = 计算相隔天数(start_date, end_date)
    # print(n)
