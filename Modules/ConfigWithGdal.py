import datetime
import pandas as pd
from osgeo import gdal
import tkinter as tk
import tkinter.ttk as ttk
from TkinterTest import NotebookSample

#TkinterTest.pyモジュールのNotebookSampleクラスを継承し,Commonクラスを定義する
class Common(NotebookSample):
    def __init__(self):
        self.FT_list = []
        self.file_identifier = ""
        self.lat_first = 0
        self.lon_first = 0
        self.lat_divide = 0
        self.lon_divide = 0
        self.lat_mesh = 0
        self.lon_mesh = 0
        self.file_num = 0 #1つの初期時刻に対するGRIB2ファイルの数
        self.GPV_type = "" #モデルの種類(GSM,MSM)
        self.SorP = "" #データの種類(地上,気圧面データ)
        self.start_valid = [] #予報の始まり番号を格納するリスト
        self.end_valid = [] #予報の終わり番号を格納するリスト
        self.interval_valid = [] #予報の間隔時間を格納するリスト
        self.FT_type = 0
        self.time_append = datetime.timedelta(hours=0)
        self.extract_met_ele_num = 0 #各予報時間において抽出する気象要素の数(MSM_Lpallなら6*12)
        self.all_met_ele_num = 0 #各予報時間において抽出はしないが、すべての気象要素の数(MSM_Lpallなら93)
        self.met_ele_start_sequence = 0 #気象要素の取得番号(始め)
        self.time_append_since_init = 0
        self.point_read = pd.read_csv("point_tmp.txt", header=None)
        self.time_read =  pd.read_csv("time_tmp.txt",header=None)
        self.point_name_list = []
        self.date_list = []
        self.lat_list = []
        self.lon_list = []
        self.datetime_list = []
        self.init_data = []
        self.data_list = []
        self.z_time_list = []
        self.time_diff = datetime.timedelta(hours=9) #標準時から9時間加える(ファイル名の初期時刻(Z)から時刻計算をするので、日本時刻にする必要がある)
        for pnt in range(0,len(self.point_read),1):
            self.point_name_list.append(self.point_read.iloc[pnt,0])
            self.lat_list.append(self.point_read.iloc[pnt,1])
            self.lon_list.append(self.point_read.iloc[pnt,2])
        for init_nump in range(0,len(self.time_read),1):
            self.year = self.time_read.iloc[init_nump,0]
            self.month = self.time_read.iloc[init_nump,1]
            self.day = self.time_read.iloc[init_nump,2]
            self.z_time = self.time_read.iloc[init_nump,3]
            self.z_time_list.append(self.z_time)
            self.date = self.year*1000000 + self.month*10000 + self.day*100 + self.z_time
            self.date_list.append(self.date)
            self.datetime_list.append(datetime.datetime(self.year,self.month,self.day,self.z_time)+self.time_diff)

    #GRIB2データを抽出するクラス内メソッド
    def Get(self):
        for init_num in range(0,len(self.time_read),1):
            for point_num in range(0,len(self.lat_list),1):
                lat = round(self.lat_list[point_num]*self.lat_divide)/self.lat_divide
                lon = round(self.lon_list[point_num]*self.lon_divide)/self.lon_divide
                #日本域の配信範囲は,GSM,MSM,LFM同様に,
                #(47.6N, 120.0E)を北西端、(22.4E, 150.0E)を南東端とする領域
                #緯度番号,経度番号は北西端からスタートで,スタート値は『1』となる.
                lat_num = (self.lat_first-lat)/self.lat_mesh
                lon_num = (lon-self.lon_first)/self.lon_mesh
                #予報時間別に分けれた複数のGRIB2ファイルを開くために,file_type変数でループ処理を行う
                for file_type in range(0,self.file_num,1):
                    GdOp = gdal.Open("../GRIB2/"+ self.GPV_type + "/" + self.SorP +
                    "/Z__C_RJTD_" + str(self.date_list[init_num]) + "0000_" + self.GPV_type +
                    "_GPV_Rjp_" + self.SorP + "_" + self.FT_list[int(file_type)] + "_grib2.bin")

                    for time in range(self.start_valid[file_type],self.end_valid[file_type]+1,1):
                        self.init_data.append(self.datetime_list[init_num]+ datetime.timedelta(hours=self.time_append_since_init))
                        self.init_data.append(lat)
                        self.init_data.append(lon)
                        for ele_cycle in range(0,self.extract_met_ele_num,1):
                            self.init_data.append(GdOp.GetRasterBand(self.met_ele_start_sequence_list[file_type] + self.all_met_ele_num*(time-1)+ele_cycle).ReadAsArray()[int(lat_num),int(lon_num)])
                        self.datetime_list[init_num] = self.datetime_list[init_num] + datetime.timedelta(hours=self.interval_valid[file_type])
                        self.data_list.append(self.init_data)
                        self.init_data=[]
                        print(self.data_list)

                csv_name = self.point_name_list[point_num] + "_Init" + str(self.date_list[init_num]) + "Z_" + self.GPV_type + "_" + self.SorP + "_" + self.file_identifier
                df = pd.DataFrame(data=self.data_list)
                df.to_csv("../Extracted/" + self.GPV_type + "/" + self.SorP + "/" +
                ("{}").format(csv_name) + ".csv",
                encoding='utf_8',header=False, index=False)

                self.data_list = [] #リストの初期化
