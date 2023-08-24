# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import date
from dateutil.relativedelta import relativedelta
import pyodbc
import csv

def get_utter_of_course(khoa_hoc, column):
    csv_path = './actions/khoa_hoc.csv'
    utter=''
    with open(csv_path, 'r', encoding="utf-8") as csv_file:
        table = csv.reader(csv_file)
        for row in table:
            # Kiểm tra khóa học có tồn tại không, nếu không trả về utter không tìm thấy khóa học
            if(khoa_hoc.lower() in row[0].lower() and row[column] != ''):
                utter = row[column]
                return utter
        utter = 'utter_khong_tim_thay_khoa_hoc' 
        return utter

# SQL Server config
db_conf = {
    'server': 'localhost',
    'database': 'QuanLy',
    'username': 'sa',
    'password': ''
}
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+db_conf['server']+';DATABASE='+db_conf['database']+';UID='+db_conf['username']+';PWD='+db_conf['password'])
cursor = conn.cursor()

class ActionHocPhi(Action):

    def name(self) -> Text:
        return "custom_action_hoc_phi"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Action Học phí is calling")
        khoa_hoc = tracker.get_slot("khoa_hoc").lower()
        print(khoa_hoc)
       

        try:
             # Nếu không tìm thấy khóa học sẽ nhảy sang catch
            loai_khoa_hoc = int(get_utter_of_course(khoa_hoc, 4))
            print('Loại khóa học ' + str(loai_khoa_hoc))
            # Khóa học đặc biệt thì không cần truy xuất CSDL mà truy xuất utter từ file csv
            if loai_khoa_hoc == 2:
                utter_hoc_phi_dac_biet = get_utter_of_course(khoa_hoc, 5)
                print(utter_hoc_phi_dac_biet)
                dispatcher.utter_message(response=utter_hoc_phi_dac_biet)
                return []

            query_hoc_phi = ''
            # Lấy dữ liệu học phí dựa trên khóa học ngắn hạn hoặc dài hạn
            if loai_khoa_hoc == 1:
                query_hoc_phi = 'SELECT KHOA_TEN, Thang, SoLan_Thang, HocKi, SoLan_HK, TronGoi, SoLan_TronGoi ' \
                                'FROM HocPhiDaiHan ' \
                                'INNER JOIN APTECH_DMKHOAHOC ' \
                                'ON HocPhiDaiHan.KHOA_ID = APTECH_DMKHOAHOC.KHOA_ID'
            else:
                query_hoc_phi = 'SELECT KHOA_TEN, TronGoi ' \
                                'FROM HocPhiNganHan ' \
                                'INNER JOIN APTECH_DMKHOAHOC ' \
                                'ON HocPhiNganHan.KHOA_ID = APTECH_DMKHOAHOC.KHOA_ID'
            # print(query_hoc_phi)

            cursor.execute(query_hoc_phi)
            check = False

            # Kiểm tra khóa học có trong CSDL không, dựa trên khóa học dài hạn hoặc ngắn hạn sẽ có cách trả lời khác nhau
            print("-------Học phí-------")
            for row in cursor:
                print(row)
                if khoa_hoc in row[0].lower():
                    if loai_khoa_hoc == 1:
                        dispatcher.utter_message(text="Học phí khóa dài hạn {khoa_hoc} đã bao gồm giáo trình, "
                                                      "đồng phục, balo, cơ sở vật chất, hỗ trợ học phí học Anh văn lấy chứng chỉ, "
                                                      "phí hỗ trợ việc làm (không phát sinh chi phí thêm trong quá trình học): "
                                                      "{thang} triệu đồng/ tháng (tổng cộng {t_solan} lần đóng), "
                                                      "nếu đóng theo học kỳ giảm còn {hoc_ki} triệu đồng/ HK ({hk_solan} lần đóng),"
                                                      " đóng trọn năm giảm còn {tron_goi} triệu đồng ({tg_solan} lần đóng).".format(khoa_hoc=row[0], thang=row[1], t_solan=row[2], hoc_ki=row[3], hk_solan=row[4], tron_goi=row[5], tg_solan=row[6]))
                        return []
                    elif loai_khoa_hoc == 0:
                        dispatcher.utter_message(text="Học phí khóa ngắn hạn {khoa_hoc} là {tron_goi} triệu đồng".format(khoa_hoc=row[0], tron_goi=row[1]))
                        return []
            dispatcher.utter_message(response='utter_khong_tim_thay_khoa_hoc')
            return []
        except:
            print("Something went wrong")
            dispatcher.utter_message(response='utter_khong_tim_thay_khoa_hoc')
            return []

class ActionThoiGianKhoaHoc(Action):

    def name(self) -> Text:
        return "custom_action_lich_hoc"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Action Thời gian khóa học is calling")
        khoa_hoc = tracker.get_slot("khoa_hoc").lower()
        # Lấy dữ liệu cách đây n tháng kể từ thời điểm hiện tại
        time = date.today() - relativedelta(months=+6)
        time_to_string = time.strftime("%m/%d/%Y")
        print('Query học phí: ' + time_to_string)

        try:
            query = "SELECT LITS_TEN, LITS_NGAYKG, LITS_BDDK, LITS_KTDK, LITS_TGHOC " \
                    "FROM TS_LICH_TS " \
                    "WHERE [LITS_NGAYKG] > '{time}'".format(time=time_to_string)
            print(query)
            cursor.execute(query)
            
            # print(khoa_hoc)
            print("-------Lịch học-------")
            for row in cursor:
                print(row)
                if khoa_hoc in row[0].lower():
                    dispatcher.utter_message(text="Chương trình {khoa_hoc} khai giảng vào ngày {khai_giang}."
                                                  " Bắt đầu đâng kí từ ngày {bd_dk},"
                                                  " Kết thúc đăng kí vào ngày {kt_dk}."
                                                  " Thời gian học cụ thể như sau: {thoi_gian}"
                                             .format(khoa_hoc=row[0], khai_giang=row[1].strftime("%d/%m/%Y"), bd_dk=row[2].strftime("%d/%m/%Y"), kt_dk=row[3].strftime("%d/%m/%Y"), thoi_gian=row[4]))
                    return []
            dispatcher.utter_message(response='utter_khong_tim_thay_khoa_hoc')
            return []
        except:
            print("Something went wrong")
            dispatcher.utter_message(response='utter_khong_tim_thay_khoa_hoc')
            return []

class ActionGioiThieuKhoaHoc(Action):

    def name(self) -> Text:
        return "custom_action_gioi_thieu_khoa_hoc"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Action Giới thiệu khóa học is calling")
        khoa_hoc = tracker.get_slot("khoa_hoc").lower()
        print(khoa_hoc)
        utter_gioi_thieu_khoa_hoc = get_utter_of_course(khoa_hoc, 1)
        dispatcher.utter_message(response=utter_gioi_thieu_khoa_hoc)
        return []


class ActionLienThongKhoaHoc(Action):

    def name(self) -> Text:
        return "custom_action_lien_thong_khoa_hoc"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Action Liên thông khóa học is calling")
        khoa_hoc = tracker.get_slot("khoa_hoc").lower()
        utter_lien_thong = get_utter_of_course(khoa_hoc, 2)
        dispatcher.utter_message(response=utter_lien_thong)

        return []

class ActionCoHoiViecLam(Action):

    def name(self) -> Text:
        return "custom_action_co_hoi_viec_lam"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Action Cơ hội việc làm is calling")
        khoa_hoc = tracker.get_slot("khoa_hoc").lower()
        utter_viec_lam = get_utter_of_course(khoa_hoc, 3)
        dispatcher.utter_message(response=utter_viec_lam)

        return []

# Response dựa trên đăng kí đại học hoặc cao đẳng công nghệ thông tin
class ActionDangKiDHCDCNTT(Action):

    def name(self) -> Text:
        return "custom_action_dang_ki_cao_dang_dai_hoc_cntt"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Action Đăng kí Đại học, Cao đẳng CNTT is calling")
        khoa_hoc = tracker.get_slot("khoa_hoc").lower()

        if "cao đẳng" in khoa_hoc.lower():
         dispatcher.utter_message(response="utter_dang_ki_cao_dang_CNTT")
        elif "đại học" in khoa_hoc.lower():
            dispatcher.utter_message(response="utter_dang_ki_dai_hoc_CNTT")
        else:
            dispatcher.utter_message(response='utter_khong_tim_thay_khoa_hoc')
        return []
