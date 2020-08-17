import tkinter as tk
import tkinter.ttk as ttk
import urllib.request
import time
import os
import pandas as pd
import datetime
import ConfigWithGdal

#ttk.Frameクラスを継承し,NotebookSampleクラスを定義する.
class NotebookSample(ttk.Frame):
    #インスタンスを生成したときに,発動されるメソッド
    def __init__(self, master):
        super().__init__() #スーパークラスttk.Frameのコンストラクタを呼び出す(ttk.Frame.__init__()でも動く)
        self.check_MSMLsurf_variable = tk.StringVar()
        self.check_MSMLpall_variable = tk.StringVar()
        self.check_GSMLsurf_variable = tk.StringVar()
        self.check_GSMLpall_variable = tk.StringVar()
        self.pointcsv_files_variable = tk.StringVar()
        self.readtime_files_variable = tk.StringVar()
        self.ExtractOrNot_MSMLsurf_variable = tk.StringVar()
        self.ExtractOrNot_MSMLpall_variable = tk.StringVar()
        self.ExtractOrNot_GSMLsurf_variable = tk.StringVar()
        self.ExtractOrNot_GSMLpall_variable = tk.StringVar()
        self.point_read = []
        self.time_read = []
        self.year_variable = tk.IntVar()
        self.month_variable = tk.IntVar()
        self.day_variable = tk.IntVar()
        self.Z_variable = tk.IntVar()
        self.create_widgets()
        self.pack()

    #確定的プログレスバーの進行状況を表示するためのクラス内メソッド
    def progress(self,block_count, block_size, total_size):
        percentage = 100.0 * block_count * block_size / total_size
        self.progress_bar["maximum"] = 100
        self.progress_bar["value"]= percentage
        self.progress_bar.update()

    #GRIB2データをダウンロードするクラス内メソッド
    def GRIB2download(self):
        MorG_list = []
        SorP_list = []
        MorG_list.append(self.check_MSMLsurf_variable.get()[0:3])
        MorG_list.append(self.check_MSMLpall_variable.get()[0:3])
        MorG_list.append(self.check_GSMLsurf_variable.get()[0:3])
        MorG_list.append(self.check_GSMLpall_variable.get()[0:3])
        SorP_list.append(self.check_MSMLsurf_variable.get()[3:])
        SorP_list.append(self.check_MSMLpall_variable.get()[3:])
        SorP_list.append(self.check_GSMLsurf_variable.get()[3:])
        SorP_list.append(self.check_GSMLpall_variable.get()[3:])
        date = str(self.year_variable.get()*1000000 + self.month_variable.get()*10000 + self.day_variable.get()*100 + self.Z_variable.get())

        #urlretrieveメソッドの引数にreporthookが与えられている場合,その引数に入れる値は,
        #3つの数値 (チャンク数,読み込んだチャンクの最大サイズ,および総ダウンロードサイズ )を受け取る関数でなければならない.
        for judge_onoroff in range(0,4,1):
            if MorG_list[judge_onoroff]=="NaN":
                pass
            elif MorG_list[judge_onoroff]=="MSM":
                if SorP_list[judge_onoroff]=="Lsurf":
                    if (self.Z_variable.get()==0 or self.Z_variable.get()==12) and int(date)>=2019030512:
                        MSM_S_FT_list = ["FH00-15","FH16-33","FH34-39","FH40-51"]
                        for FT_list_cycle in range(0,len(MSM_S_FT_list),1):
                            urllib.request.urlretrieve(url="http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/" + str(self.year_variable.get()) + "/"+ '{0:02d}'.format(self.month_variable.get()) + "/" + '{0:02d}'.format(self.day_variable.get()) + "/" + "Z__C_RJTD_" + date + "0000_"+ MorG_list[judge_onoroff] + "_GPV_Rjp_" + SorP_list[judge_onoroff] + "_" + MSM_S_FT_list[FT_list_cycle] + "_grib2.bin",
                            filename="../GRIB2/" + MorG_list[judge_onoroff] + "/" + SorP_list[judge_onoroff] + "/" + "Z__C_RJTD_" + date + "0000_"+ MorG_list[judge_onoroff] + "_GPV_Rjp_" + SorP_list[judge_onoroff] + "_" + MSM_S_FT_list[FT_list_cycle] + "_grib2.bin",reporthook=self.progress)
                    else:
                        MSM_S_FT_list = ["FH00-15","FH16-33","FH34-39"]
                        for FT_list_cycle in range(0,len(MSM_S_FT_list),1):
                            urllib.request.urlretrieve(url="http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/" + str(self.year_variable.get()) + "/"+ '{0:02d}'.format(self.month_variable.get()) + "/" + '{0:02d}'.format(self.day_variable.get()) + "/" + "Z__C_RJTD_" + date + "0000_"+ MorG_list[judge_onoroff] + "_GPV_Rjp_" + SorP_list[judge_onoroff] + "_" + MSM_S_FT_list[FT_list_cycle] + "_grib2.bin",
                            filename="../GRIB2/" + MorG_list[judge_onoroff] + "/" + SorP_list[judge_onoroff] + "/" + "Z__C_RJTD_" + date + "0000_"+ MorG_list[judge_onoroff] + "_GPV_Rjp_" + SorP_list[judge_onoroff] + "_" + MSM_S_FT_list[FT_list_cycle] + "_grib2.bin",reporthook=self.progress)

                elif SorP_list[judge_onoroff]=="L-pall":
                    if (self.Z_variable.get()==0 or self.Z_variable.get()==12) and int(date)>=2019030512:
                        MSM_P_FT_list = ["FH00-15","FH18-33","FH36-39","FH42-51"]
                        for FT_list_cycle in range(0,len(MSM_P_FT_list),1):
                            urllib.request.urlretrieve(url="http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/" + str(self.year_variable.get()) + "/"+ '{0:02d}'.format(self.month_variable.get()) + "/" + '{0:02d}'.format(self.day_variable.get()) + "/" + "Z__C_RJTD_" + date + "0000_"+ MorG_list[judge_onoroff] + "_GPV_Rjp_" + SorP_list[judge_onoroff] + "_" + MSM_P_FT_list[FT_list_cycle] + "_grib2.bin",
                            filename="../GRIB2/" + MorG_list[judge_onoroff] + "/" + SorP_list[judge_onoroff] + "/" + "Z__C_RJTD_" + date + "0000_"+ MorG_list[judge_onoroff] + "_GPV_Rjp_" + SorP_list[judge_onoroff] + "_" + MSM_P_FT_list[FT_list_cycle] + "_grib2.bin",reporthook=self.progress)
                    else:
                        MSM_P_FT_list = ["FH00-15","FH18-33","FH36-39"]
                        for FT_list_cycle in range(0,len(MSM_P_FT_list),1):
                            urllib.request.urlretrieve(url="http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/" + str(self.year_variable.get()) + "/"+ '{0:02d}'.format(self.month_variable.get()) + "/" + '{0:02d}'.format(self.day_variable.get()) + "/" + "Z__C_RJTD_" + date + "0000_"+ MorG_list[judge_onoroff] + "_GPV_Rjp_" + SorP_list[judge_onoroff] + "_" + MSM_P_FT_list[FT_list_cycle] + "_grib2.bin",
                            filename="../GRIB2/" + MorG_list[judge_onoroff] + "/" + SorP_list[judge_onoroff] + "/" + "Z__C_RJTD_" + date + "0000_"+ MorG_list[judge_onoroff] + "_GPV_Rjp_" + SorP_list[judge_onoroff] + "_" + MSM_P_FT_list[FT_list_cycle] + "_grib2.bin",reporthook=self.progress)

            elif MorG_list[judge_onoroff]=="GSM":
                if SorP_list[judge_onoroff]=="Lsurf":
                    if self.Z_variable.get()==12:
                        GSM_S_FT_list = ["FD0000-0312","FD0315-0800","FD0803-1100"]
                        for FT_list_cycle in range(0,len(GSM_S_FT_list),1):
                            urllib.request.urlretrieve(url="http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/" + str(self.year_variable.get()) + "/"+ '{0:02d}'.format(self.month_variable.get()) + "/" + '{0:02d}'.format(self.day_variable.get()) + "/" + "Z__C_RJTD_" + date + "0000_"+ MorG_list[judge_onoroff] + "_GPV_Rjp_" + SorP_list[judge_onoroff] + "_" + GSM_S_FT_list[FT_list_cycle] + "_grib2.bin",
                            filename="../GRIB2/" + MorG_list[judge_onoroff] + "/" + SorP_list[judge_onoroff] + "/" + "Z__C_RJTD_" + date + "0000_"+ MorG_list[judge_onoroff] + "_GPV_Rjp_" + SorP_list[judge_onoroff] + "_" + GSM_S_FT_list[FT_list_cycle] + "_grib2.bin",reporthook=self.progress)
                    elif int(date)>=2018062600 and self.Z_variable.get()!=12:
                        GSM_S_FT_list = ["FD0000-0312","FD0315-0512"]
                        for FT_list_cycle in range(0,len(GSM_S_FT_list),1):
                            urllib.request.urlretrieve(url="http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/" + str(self.year_variable.get()) + "/"+ '{0:02d}'.format(self.month_variable.get()) + "/" + '{0:02d}'.format(self.day_variable.get()) + "/" + "Z__C_RJTD_" + date + "0000_"+ MorG_list[judge_onoroff] + "_GPV_Rjp_" + SorP_list[judge_onoroff] + "_" + GSM_S_FT_list[FT_list_cycle] + "_grib2.bin",
                            filename="../GRIB2/" + MorG_list[judge_onoroff] + "/" + SorP_list[judge_onoroff] + "/" + "Z__C_RJTD_" + date + "0000_"+ MorG_list[judge_onoroff] + "_GPV_Rjp_" + SorP_list[judge_onoroff] + "_" + GSM_S_FT_list[FT_list_cycle] + "_grib2.bin",reporthook=self.progress)
                    else:
                        GSM_S_FT_list = ["FD0000-0312"]
                        for FT_list_cycle in range(0,len(GSM_S_FT_list),1):
                            urllib.request.urlretrieve(url="http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/" + str(self.year_variable.get()) + "/"+ '{0:02d}'.format(self.month_variable.get()) + "/" + '{0:02d}'.format(self.day_variable.get()) + "/" + "Z__C_RJTD_" + date + "0000_"+ MorG_list[judge_onoroff] + "_GPV_Rjp_" + SorP_list[judge_onoroff] + "_" + GSM_S_FT_list[FT_list_cycle] + "_grib2.bin",
                            filename="../GRIB2/" + MorG_list[judge_onoroff] + "/" + SorP_list[judge_onoroff] + "/" + "Z__C_RJTD_" + date + "0000_"+ MorG_list[judge_onoroff] + "_GPV_Rjp_" + SorP_list[judge_onoroff] + "_" + GSM_S_FT_list[FT_list_cycle] + "_grib2.bin",reporthook=self.progress)

                elif SorP_list[judge_onoroff]=="L-pall":
                    if self.Z_variable.get()==12:
                        GSM_P_FT_list = ["FD0000-0312","FD0318-0800","FD0806-1100"]
                        for FT_list_cycle in range(0,len(GSM_P_FT_list),1):
                            urllib.request.urlretrieve(url="http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/" + str(self.year_variable.get()) + "/"+ '{0:02d}'.format(self.month_variable.get()) + "/" + '{0:02d}'.format(self.day_variable.get()) + "/" + "Z__C_RJTD_" + date + "0000_"+ MorG_list[judge_onoroff] + "_GPV_Rjp_" + SorP_list[judge_onoroff] + "_" + GSM_P_FT_list[FT_list_cycle] + "_grib2.bin",
                            filename="../GRIB2/" + MorG_list[judge_onoroff] + "/" + SorP_list[judge_onoroff] + "/" + "Z__C_RJTD_" + date + "0000_"+ MorG_list[judge_onoroff] + "_GPV_Rjp_" + SorP_list[judge_onoroff] + "_" + GSM_P_FT_list[FT_list_cycle] + "_grib2.bin",reporthook=self.progress)
                    elif int(date)>=2018062600 and self.Z_variable.get()!=12:
                        GSM_P_FT_list = ["FD0000-0312","FD0318-0512"]
                        for FT_list_cycle in range(0,len(GSM_P_FT_list),1):
                            urllib.request.urlretrieve(url="http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/" + str(self.year_variable.get()) + "/"+ '{0:02d}'.format(self.month_variable.get()) + "/" + '{0:02d}'.format(self.day_variable.get()) + "/" + "Z__C_RJTD_" + date + "0000_"+ MorG_list[judge_onoroff] + "_GPV_Rjp_" + SorP_list[judge_onoroff] + "_" + GSM_P_FT_list[FT_list_cycle] + "_grib2.bin",
                            filename="../GRIB2/" + MorG_list[judge_onoroff] + "/" + SorP_list[judge_onoroff] + "/" + "Z__C_RJTD_" + date + "0000_"+ MorG_list[judge_onoroff] + "_GPV_Rjp_" + SorP_list[judge_onoroff] + "_" + GSM_P_FT_list[FT_list_cycle] + "_grib2.bin",reporthook=self.progress)
                    else:
                        GSM_P_FT_list = ["FD0000-0312"]
                        for FT_list_cycle in range(0,len(GSM_P_FT_list),1):
                            urllib.request.urlretrieve(url="http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/" + str(self.year_variable.get()) + "/"+ '{0:02d}'.format(self.month_variable.get()) + "/" + '{0:02d}'.format(self.day_variable.get()) + "/" + "Z__C_RJTD_" + date + "0000_"+ MorG_list[judge_onoroff] + "_GPV_Rjp_" + SorP_list[judge_onoroff] + "_" + GSM_P_FT_list[FT_list_cycle] + "_grib2.bin",
                            filename="../GRIB2/" + MorG_list[judge_onoroff] + "/" + SorP_list[judge_onoroff] + "/" + "Z__C_RJTD_" + date + "0000_"+ MorG_list[judge_onoroff] + "_GPV_Rjp_" + SorP_list[judge_onoroff] + "_" + GSM_P_FT_list[FT_list_cycle] + "_grib2.bin",reporthook=self.progress)

    #GRIB2データを抽出するクラス内メソッド
    def GRIB2extract(self):
        tmppoint_read = pd.read_csv("../ReadPoint/"+ self.pointcsv_files_variable.get(),header=None)
        tmptime_read = pd.read_csv("../ReadTime/"+ self.readtime_files_variable.get(),header=None)
        tmppoint_read.to_csv("point_tmp.txt",encoding='utf_8',header=False, index=False)
        tmptime_read.to_csv("time_tmp.txt",encoding='utf_8',header=False, index=False)

        Extract_MorG_list = []
        Extract_MorG_list.append(self.ExtractOrNot_MSMLsurf_variable.get())
        Extract_MorG_list.append(self.ExtractOrNot_MSMLpall_variable.get())
        Extract_MorG_list.append(self.ExtractOrNot_GSMLsurf_variable.get())
        Extract_MorG_list.append(self.ExtractOrNot_GSMLpall_variable.get())

        for ExtractOrNot in range(0,len(Extract_MorG_list),1):
#*****MSM_Lsurfインスタンスを生成するとき**********MSM_Lsurfインスタンスを生成するとき**********MSM_Lsurfインスタンスを生成するとき*****
        #2013/5/29から予報時間が33時間から39時間に延長された.
        #2017/12/5から日射量が追加された.
        #2019/3/5/12zから00z,12zのみ予報時間が51時間となった.
            if Extract_MorG_list[ExtractOrNot]=="MS":
                MSM_Lsurf = ConfigWithGdal.Common()
                MSM_Lsurf.GPV_type = "MSM"
                MSM_Lsurf.SorP = "Lsurf"
                MSM_Lsurf.lat_first = 47.6
                MSM_Lsurf.lon_first = 120
                MSM_Lsurf.lat_divide = 20
                MSM_Lsurf.lon_divide = 16
                MSM_Lsurf.lat_mesh = 0.05
                MSM_Lsurf.lon_mesh = 0.0625 #
                for ztime_branch in range(0,len(MSM_Lsurf.z_time_list),1):
                    if MSM_Lsurf.date>=2019030512 and (MSM_Lsurf.z_time_list[ztime_branch]==0 or MSM_Lsurf.z_time_list[ztime_branch]==12):
                        MSM_Lsurf.file_identifier = "FT01-FT51"
                        MSM_Lsurf.FT_list = ["FH00-15","FH16-33","FH34-39","FH40-51"] #GRIB2ファイルに与える名前
                        MSM_Lsurf.file_num = 4 #1つの初期時刻に対するGRIB2ファイルの数
                        MSM_Lsurf.start_valid = [1,1,1,1] #予測サイクルの最初に与える値(ConfigWithGdal.pyのループ変数timeに渡される)
                        MSM_Lsurf.end_valid = [15,18,6,12] #予測サイクルの最後に与える値(ConfigWithGdal.pyのループ変数timeに渡される)
                        MSM_Lsurf.interval_valid = [1,1,1,1] #予報時間の間隔時間を格納するリスト
                        MSM_Lsurf.extract_met_ele_num = 12 #各予測時刻に抽出する気象要素の数
                        MSM_Lsurf.all_met_ele_num = 12 #各予測時刻における気象要素の数
                        MSM_Lsurf.met_ele_start_sequence_list = [11,1,1,1] #はじめの予測時刻のときに,与える要素番号
                        MSM_Lsurf.time_append_since_init = 1 #はじめの予測時刻のときに,イニシャルから加算する時間
                        MSM_Lsurf.Get()
                    elif MSM_Lsurf.date<=2017120500:
                        MSM_Lsurf.file_identifier = "FT01-FT39"
                        MSM_Lsurf.FT_list = ["FH00-15","FH16-33","FH34-39"]
                        MSM_Lsurf.file_num = 3
                        MSM_Lsurf.start_valid = [1,1,1]
                        MSM_Lsurf.end_valid = [15,18,6]
                        MSM_Lsurf.interval_valid = [1,1,1]
                        MSM_Lsurf.extract_met_ele_num = 11
                        MSM_Lsurf.all_met_ele_num = 11
                        MSM_Lsurf.met_ele_start_sequence_list = [11,1,1]
                        MSM_Lsurf.time_append_since_init = 1
                        MSM_Lsurf.Get()
                    else:
                        MSM_Lsurf.file_identifier = "FT01-FT39"
                        MSM_Lsurf.FT_list = ["FH00-15","FH16-33","FH34-39"]
                        MSM_Lsurf.file_num = 3
                        MSM_Lsurf.start_valid = [1,1,1]
                        MSM_Lsurf.end_valid = [15,18,6]
                        MSM_Lsurf.interval_valid = [1,1,1]
                        MSM_Lsurf.extract_met_ele_num = 12
                        MSM_Lsurf.all_met_ele_num = 12
                        MSM_Lsurf.met_ele_start_sequence_list = [11,1,1]
                        MSM_Lsurf.time_append_since_init = 1
                        MSM_Lsurf.Get()

#*****MSM_Lpallインスタンスを生成するとき**********MSM_Lpallインスタンスを生成するとき**********MSM_Lpallインスタンスを生成するとき*****
            #2013/5/29から予報時間が33時間から39時間に延長された.
            #2019/3/5/12zから00z,12zのみ予報時間が,51時間となった.
            elif Extract_MorG_list[ExtractOrNot]=="MP":
                MSM_Lpall = ConfigWithGdal.Common()
                MSM_Lpall.GPV_type = "MSM"
                MSM_Lpall.SorP = "L-pall"
                MSM_Lpall.lat_first = 47.6
                MSM_Lpall.lon_first = 120
                MSM_Lpall.lat_divide = 20
                MSM_Lpall.lon_divide = 16
                MSM_Lpall.lat_mesh = 0.1
                MSM_Lpall.lon_mesh = 0.125
                for ztime_branch in range(0,len(MSM_Lpall.z_time_list),1):
                    if MSM_Lpall.date>=2019030512 and (MSM_Lpall.z_time_list[ztime_branch]==0 or MSM_Lpall.z_time_list[ztime_branch]==12):
                        MSM_Lpall.file_identifier = "FT03-FT51"
                        MSM_Lpall.FT_list = ["FH00-15","FH18-33","FH36-39","FH42-51"]
                        MSM_Lpall.file_num = 4
                        MSM_Lpall.start_valid = [1,0,0,0]
                        MSM_Lpall.end_valid = [5,5,1,3]
                        MSM_Lpall.interval_valid = [3,3,3,3]
                        MSM_Lpall.extract_met_ele_num = 6*12
                        MSM_Lpall.all_met_ele_num = 92
                        MSM_Lpall.met_ele_start_sequence_list = [93,93,93,93]
                        MSM_Lpall.time_append_since_init = 3
                        MSM_Lpall.Get()
                    else:
                        MSM_Lpall.file_identifier = "FT03-FT39"
                        MSM_Lpall.FT_list = ["FH00-15","FH18-33","FH36-39"]
                        MSM_Lpall.file_num = 3
                        MSM_Lpall.start_valid = [1,0,0]
                        MSM_Lpall.end_valid = [5,5,1]
                        MSM_Lpall.interval_valid = [3,3,3]
                        MSM_Lpall.extract_met_ele_num = 6*12
                        MSM_Lpall.all_met_ele_num = 92
                        MSM_Lpall.met_ele_start_sequence_list = [93,93,93]
                        MSM_Lpall.time_append_since_init = 3
                        MSM_Lpall.Get()

#*****GSM_Lsurfインスタンスを生成するとき**********GSM_Lsurfインスタンスを生成するとき**********GSM_Lsurfインスタンスを生成するとき*****
            elif Extract_MorG_list[ExtractOrNot]=="GS":
            #2013/3/28から,予報時間が192時間から264時間に延長された.
            #2017/12/5から,全球数値予報モデルGPV（日本域）に日射量要素が追加された.
            #2018/6/26から,00,06,18UTC初期値の資料の予報時間が84時間から132時間に延長され,GSM全球域の84時間より先の予報時間の間隔が12時間から６時間に変更された.
                    GSM_Lsurf = ConfigWithGdal.Common()
                    GSM_Lsurf.GPV_type = "GSM"
                    GSM_Lsurf.SorP = "Lsurf"
                    GSM_Lsurf.lat_first = 50
                    GSM_Lsurf.lon_first = 120
                    GSM_Lsurf.lat_divide = 5
                    GSM_Lsurf.lon_divide = 4
                    GSM_Lsurf.lat_mesh = 0.2
                    GSM_Lsurf.lon_mesh = 0.25
                    for ztime_branch in range(0,len(GSM_Lsurf.z_time_list),1):
                        if GSM_Lsurf.date>=2017120500 and GSM_Lsurf.z_time_list[ztime_branch]==12:
                            for FT84 in range(0,2,1):
                                if FT84==0:
                                    GSM_Lsurf.file_identifier = "FT01-FT84"
                                    GSM_Lsurf.FT_list = ["FD0000-0312"]
                                    GSM_Lsurf.file_num = 1
                                    GSM_Lsurf.start_valid = [1]
                                    GSM_Lsurf.end_valid = [84]
                                    GSM_Lsurf.interval_valid = [1]
                                    GSM_Lsurf.extract_met_ele_num = 12
                                    GSM_Lsurf.all_met_ele_num = 12
                                    GSM_Lsurf.met_ele_start_sequence_list = [11]
                                    GSM_Lsurf.time_append_since_init = 1
                                    GSM_Lsurf.Get()
                                elif FT84==1:
                                    GSM_Lsurf.file_identifier = "FT87-264"
                                    GSM_Lsurf.FT_list = ["FD0315-0800","FD0803-1100"]
                                    GSM_Lsurf.file_num = 2
                                    GSM_Lsurf.start_valid = [1,1]
                                    GSM_Lsurf.end_valid = [15,15]
                                    GSM_Lsurf.interval_valid = [3,3]
                                    GSM_Lsurf.extract_met_ele_num = 12
                                    GSM_Lsurf.all_met_ele_num = 12
                                    GSM_Lsurf.met_ele_start_sequence_list = [1,1]
                                    GSM_Lsurf.time_append_since_init = 3
                                    GSM_Lsurf.Get()

                        elif GSM_Lsurf.date<2017120500 and GSM_Lsurf.z_time_list[ztime_branch]==12:
                            for FT84 in range(0,2,1):
                                if FT84==0:
                                    GSM_Lsurf.file_identifier = "FT01-FT84"
                                    GSM_Lsurf.FT_list = ["FD0000-0312"]
                                    GSM_Lsurf.file_num = 1
                                    GSM_Lsurf.start_valid = [1]
                                    GSM_Lsurf.end_valid = [84]
                                    GSM_Lsurf.interval_valid = [1]
                                    GSM_Lsurf.extract_met_ele_num = 11
                                    GSM_Lsurf.all_met_ele_num = 11
                                    GSM_Lsurf.met_ele_start_sequence_list = [11]
                                    GSM_Lsurf.time_append_since_init = 1
                                    GSM_Lsurf.Get()
                                elif FT84==1:
                                    GSM_Lsurf.file_identifier = "FT87-264"
                                    GSM_Lsurf.FT_list = ["FD0315-0800","FD0803-1100"]
                                    GSM_Lsurf.file_num = 2
                                    GSM_Lsurf.start_valid = [1,1]
                                    GSM_Lsurf.end_valid = [15,15]
                                    GSM_Lsurf.interval_valid = [3,3]
                                    GSM_Lsurf.extract_met_ele_num = 11
                                    GSM_Lsurf.all_met_ele_num = 11
                                    GSM_Lsurf.met_ele_start_sequence_list = [1,1]
                                    GSM_Lsurf.time_append_since_init = 3
                                    GSM_Lsurf.Get()

                        elif 2018062600>GSM_Lsurf.date>=2017120500 and (GSM_Lsurf.z_time_list[ztime_branch]==0 or GSM_Lsurf.z_time_list[ztime_branch]==6 or GSM_Lsurf.z_time_list[ztime_branch]==12 or GSM_Lsurf.z_time_list[ztime_branch]==18):
                            for FT84 in range(0,1,1):
                                if FT84==0:
                                    GSM_Lsurf.file_identifier = "FT01-FT84"
                                    GSM_Lsurf.FT_list = ["FD0000-0312"]
                                    GSM_Lsurf.file_num = 1
                                    GSM_Lsurf.start_valid = [1]
                                    GSM_Lsurf.end_valid = [84]
                                    GSM_Lsurf.interval_valid = [1]
                                    GSM_Lsurf.extract_met_ele_num = 12
                                    GSM_Lsurf.all_met_ele_num = 12
                                    GSM_Lsurf.met_ele_start_sequence_list = [11]
                                    GSM_Lsurf.time_append_since_init = 1
                                    GSM_Lsurf.Get()

                        elif GSM_Lsurf.date<2017120500 and (GSM_Lsurf.z_time_list[ztime_branch]==0 or GSM_Lsurf.z_time_list[ztime_branch]==6 or GSM_Lsurf.z_time_list[ztime_branch]==12 or GSM_Lsurf.z_time_list[ztime_branch]==18):
                            for FT84 in range(0,1,1):
                                if FT84==0:
                                    GSM_Lsurf.file_identifier = "FT01-FT84"
                                    GSM_Lsurf.FT_list = ["FD0000-0312"]
                                    GSM_Lsurf.file_num = 1
                                    GSM_Lsurf.start_valid = [1]
                                    GSM_Lsurf.end_valid = [84]
                                    GSM_Lsurf.interval_valid = [1]
                                    GSM_Lsurf.extract_met_ele_num = 11
                                    GSM_Lsurf.all_met_ele_num = 11
                                    GSM_Lsurf.met_ele_start_sequence_list = [11]
                                    GSM_Lsurf.time_append_since_init = 1
                                    GSM_Lsurf.Get()

                        elif 2018062600<=GSM_Lsurf.date and (GSM_Lsurf.z_time_list[ztime_branch]==0 or GSM_Lsurf.z_time_list[ztime_branch]==6 or GSM_Lsurf.z_time_list[ztime_branch]==12 or GSM_Lsurf.z_time_list[ztime_branch]==18):
                            for FT84 in range(0,2,1):
                                if FT84==0:
                                    GSM_Lsurf.file_identifier = "FT01-FT84"
                                    GSM_Lsurf.FT_list = ["FD0000-0312"]
                                    GSM_Lsurf.file_num = 1
                                    GSM_Lsurf.start_valid = [1]
                                    GSM_Lsurf.end_valid = [84]
                                    GSM_Lsurf.interval_valid = [1]
                                    GSM_Lsurf.extract_met_ele_num = 12
                                    GSM_Lsurf.all_met_ele_num = 12
                                    GSM_Lsurf.met_ele_start_sequence_list = [11]
                                    GSM_Lsurf.time_append_since_init = 1
                                    GSM_Lsurf.Get()
                                elif FT84==1:
                                    GSM_Lsurf.file_identifier = "FT87-FT132"
                                    GSM_Lsurf.FT_list = ["FD0315-0512"]
                                    GSM_Lsurf.file_num = 1
                                    GSM_Lsurf.start_valid = [1]
                                    GSM_Lsurf.end_valid = [16]
                                    GSM_Lsurf.interval_valid = [3]
                                    GSM_Lsurf.extract_met_ele_num = 12
                                    GSM_Lsurf.all_met_ele_num = 12
                                    GSM_Lsurf.met_ele_start_sequence_list = [1]
                                    GSM_Lsurf.time_append_since_init = 3
                                    GSM_Lsurf.Get()

#*****GSM_Lpallインスタンスを生成するとき**********GSM_Lpallインスタンスを生成するとき**********GSM_Lpallインスタンスを生成するとき*****
            elif Extract_MorG_list[ExtractOrNot]=="GP":
            #2013/3/28から,予報時間が192時間から264時間に延長された.
            #2018/6/26から,00,06,18UTC初期値の資料の予報時間が84時間から132時間に延長され,GSM全球域の84時間より先の予報時間の間隔が12時間から６時間に変更された.
                GSM_Lpall = ConfigWithGdal.Common()
                GSM_Lpall.GPV_type = "GSM"
                GSM_Lpall.SorP = "L-pall"
                GSM_Lpall.lat_first = 50
                GSM_Lpall.lon_first = 120
                GSM_Lpall.lat_divide = 5
                GSM_Lpall.lon_divide = 4
                GSM_Lpall.lat_mesh = 0.2
                GSM_Lpall.lon_mesh = 0.25
                for ztime_branch in range(0,len(GSM_Lpall.z_time_list),1):
                    if GSM_Lpall.z_time_list[ztime_branch]==12:
                        for FT84 in range(0,2,1):
                            if FT84==0:
                                GSM_Lpall.file_identifier = "FT03-FT84"
                                GSM_Lpall.FT_list = ["FD0000-0312"]
                                GSM_Lpall.file_num = 1
                                GSM_Lpall.start_valid = [1]
                                GSM_Lpall.end_valid = [28]
                                GSM_Lpall.interval_valid = [3]
                                GSM_Lpall.extract_met_ele_num = 6*12
                                GSM_Lpall.all_met_ele_num = 92
                                GSM_Lpall.met_ele_start_sequence_list = [93]
                                GSM_Lpall.time_append_since_init = 3
                                GSM_Lpall.Get()
                            elif FT84==1:
                                GSM_Lpall.file_identifier = "FT90-264"
                                GSM_Lpall.FT_list = ["FD0318-0800","FD0806-1100"]
                                GSM_Lpall.file_num = 2
                                GSM_Lpall.start_valid = [0,0]
                                GSM_Lpall.end_valid = [17,11]
                                GSM_Lpall.interval_valid = [6,6]
                                GSM_Lpall.extract_met_ele_num = 6*12
                                GSM_Lpall.all_met_ele_num = 92
                                GSM_Lpall.met_ele_start_sequence_list = [93,93]
                                GSM_Lpall.time_append_since_init = 6
                                GSM_Lpall.Get()

                    elif 2018062600<=GSM_Lpall.date and GSM_Lpall.z_time_list[ztime_branch]!=12:
                        for FT84 in range(0,2,1):
                            if FT84==0:
                                GSM_Lpall.file_identifier = "FT03-FT84"
                                GSM_Lpall.FT_list = ["FD0000-0312"]
                                GSM_Lpall.file_num = 1
                                GSM_Lpall.start_valid = [1]
                                GSM_Lpall.end_valid = [28]
                                GSM_Lpall.interval_valid = [3]
                                GSM_Lpall.extract_met_ele_num = 6*12
                                GSM_Lpall.all_met_ele_num = 92
                                GSM_Lpall.met_ele_start_sequence_list = [93]
                                GSM_Lpall.time_append_since_init = 3
                                GSM_Lpall.Get()
                            elif FT84==1:
                                GSM_Lpall.file_identifier = "FT90-FT132"
                                GSM_Lpall.FT_list = ["FD0318-0512"]
                                GSM_Lpall.file_num = 1
                                GSM_Lpall.start_valid = [0]
                                GSM_Lpall.end_valid = [7]
                                GSM_Lpall.interval_valid = [6]
                                GSM_Lpall.extract_met_ele_num = 6*12
                                GSM_Lpall.all_met_ele_num = 92
                                GSM_Lpall.met_ele_start_sequence_list = [93]
                                GSM_Lpall.time_append_since_init = 6
                                GSM_Lpall.Get()

                    elif 2018062600>GSM_Lpall.date and GSM_Lpall.z_time_list[ztime_branch]!=12:
                        for FT84 in range(0,1,1):
                            if FT84==0:
                                GSM_Lpall.file_identifier = "FT03-FT84"
                                GSM_Lpall.FT_list = ["FD0000-0312"]
                                GSM_Lpall.file_num = 1
                                GSM_Lpall.start_valid = [1]
                                GSM_Lpall.end_valid = [28]
                                GSM_Lpall.interval_valid = [3]
                                GSM_Lpall.extract_met_ele_num = 6*12
                                GSM_Lpall.all_met_ele_num = 92
                                GSM_Lpall.met_ele_start_sequence_list = [93]
                                GSM_Lpall.time_append_since_init = 3
                                GSM_Lpall.Get()

    #複数タブ内に複数のウィジェットを生成,配置するクラス内メソッド
    def create_widgets(self):
        note = ttk.Notebook(self) #Notebookクラスは複数のウィンドウをタブで管理するためのウィジェット
        note.pack()
        #タブ1(抽出処理)の表示と処理群
        note0 = ttk.Frame(note,width=400,height=400) #1つめのタブにおけるフレームを作成
        note.add(note0,text="ダウンロード") #1つめタブの追加
        init_label0 = ttk.Label(note0,text="GRIB2データの種類").grid(column=0,row=0,columnspan=4)
        radio_MSMLsurf = ttk.Checkbutton(note0,text="MSM地上",variable=self.check_MSMLsurf_variable,onvalue="MSMLsurf",offvalue="NaNNaN").grid(row=1,column=0,ipadx=5)
        radio_MSMLpall = ttk.Checkbutton(note0,text="MSM気圧面",variable=self.check_MSMLpall_variable,onvalue="MSML-pall",offvalue="NaNNaN").grid(row=1,column=1,ipadx=5)
        radio_GSMLsurf = ttk.Checkbutton(note0,text="GSM地上",variable=self.check_GSMLsurf_variable,onvalue="GSMLsurf",offvalue="NaNNaN").grid(row=1,column=2,ipadx=5)
        radio_GSMLpall = ttk.Checkbutton(note0,text="GSM気圧面",variable=self.check_GSMLpall_variable,onvalue="GSML-pall",offvalue="NaNNaN").grid(row=1,column=3,ipadx=5)
        init_label0 = ttk.Label(note0,text="イニシャルタイム(協定世界時)").grid(column=0,row=2,columnspan=4) #ラベルの追加
        CB_year_list = [2014, 2015,2016,2017,2018,2019,2020]
        CB_month_list = [1,2,3,4,5,6,7,8,9,10,11,12]
        CB_day_list = []
        for CB_day_append in range(1,32,1):
            CB_day_list.append(CB_day_append)
        CB_Z_list = [0,3,6,9,12,15,18,21,24]
        cb = ttk.Combobox(note0,state='readonly',width=5, values=CB_year_list,textvariable=self.year_variable)
        cb.set("年")
        cb.grid(column=0, row=3,padx=5)
        cb = ttk.Combobox(note0,state='readonly',width=5, values=CB_month_list,textvariable=self.month_variable)
        cb.set("月")
        cb.grid(column=1, row=3,padx=5)
        cb = ttk.Combobox(note0,state='readonly',width=5, values=CB_day_list,textvariable=self.day_variable)
        cb.set("日")
        cb.grid(column=2, row=3,padx=5)
        cb = ttk.Combobox(note0,state='readonly',width=5, values=CB_Z_list,textvariable=self.Z_variable)
        cb.set("時")
        cb.grid(column=3, row=3,padx=5)
        btn0 = ttk.Button(note0, text="GRIB2データをダウンロード", command=self.GRIB2download).grid(column=0,row=7,columnspan=4,pady=10)
        self.progress_bar= ttk.Progressbar(note0, orient='horizontal', length=300, mode='determinate')
        self.progress_bar.grid(column=0, row=8,columnspan=4,pady=5)

        #タブ1(抽出)の表示と処理群
        note1 = ttk.Frame(note,width=400,height=400) #2つめのタブにおけるフレームを作成
        note.add(note1,text="抽出") #2つめタブの追加
        init_label0 = ttk.Label(note1,text="GRIB2データの種類").grid(column=0,row=0,columnspan=4)
        ttk.Checkbutton(note1,text="MSM地上",variable=self.ExtractOrNot_MSMLsurf_variable,onvalue="MS",offvalue="N").grid(row=1,column=0,ipadx=5)
        ttk.Checkbutton(note1,text="MSM気圧面",variable=self.ExtractOrNot_MSMLpall_variable,onvalue="MP",offvalue="N").grid(row=1,column=1,ipadx=5)
        ttk.Checkbutton(note1,text="GSM地上",variable=self.ExtractOrNot_GSMLsurf_variable,onvalue="GS",offvalue="N").grid(row=1,column=2,ipadx=5)
        ttk.Checkbutton(note1,text="GSM気圧面",variable=self.ExtractOrNot_GSMLpall_variable,onvalue="GP",offvalue="N").grid(row=1,column=3,ipadx=5)
        init_label0 = ttk.Label(note1,text="CSVファイル名").grid(column=0,row=2,columnspan=4)
        pointcsv_files = os.listdir("../ReadPoint")
        readtime_files = os.listdir("../ReadTime")
        cb1 = ttk.Combobox(note1,state='readonly',width=15, values=pointcsv_files,textvariable=self.pointcsv_files_variable)
        cb1.set("緯度経度")
        cb1.grid(column=0, row=3,columnspan=2)
        cb1 = ttk.Combobox(note1,state='readonly',width=15, values=readtime_files,textvariable=self.readtime_files_variable)
        cb1.set("イニシャルタイム")
        cb1.grid(column=2, row=3,columnspan=2)
        btn1 = ttk.Button(note1, text="GRIB2データを抽出", command=self.GRIB2extract)
        btn1.grid(column=0, row=4,columnspan=4,pady=10)
        self.progress_bar1 = ttk.Progressbar(note1, orient='horizontal', length=300, mode='indeterminate',maximum=10,value=0)
        self.progress_bar1.grid(column=0, row=8,columnspan=4,pady=5)
        self.progress_bar1.start(500)

if __name__ == '__main__':
    #TkinterTest.pyが実行された場合のみ,GUIを起動させる以下の手続きを行う.
    master = tk.Tk()
    master.title("GRIBGetProcessingPy")
    master.geometry("400x200")
    NotebookSample(master)
    master.mainloop()
