# Chatbot hỗ trợ tư vấn
### Cấu hình phần mềm dự án đang sử dụng:

* Ubuntu 20.04
* Python 3.8.10
* Rasa 2.8.3
* Npm 6.14.4
## Cài đặt RASA
***Nên sử dụng vituralenv hoặc Anaconda để tạo môi trường ảo***

1. Cài đặt ``virtualenv`` và tạo môi trường bằng lệnh dưới đây:

	* Cài đặt package: `$ pip install virtualenv`

	* Tạo môi trường với tên là **rasa**: `$ virtualenv rasa`

	* Truy cập môi trường vừa tạo: `$ source rasa/bin/activate`
	
2. Cài đặt `Rasa`: 

	* Để cài đặt `Rasa` phiên bản đầy đủ (bao gồm tất cả `pipeline`) sử dụng lệnh: `$ pip install rasa[full]`

	* Hoặc có thể cài `Rasa` phiên bản normal bằng lệnh: `$ pip install rasa`

## Cài đặt UI
1. Để sử dụng giao diện, máy tính cần phải cài `yarn` hoặc `npm`: [Hướng dẫn cài đặt npm cho Ubuntu](https://stackjava.com/nodejs/huong-dan-cai-dat-cau-hinh-nodejs-npm-tren-ubuntu.html)

2. Vào thư mục `ui`, gõ lệnh `npm install` hoặc `yarn install` để cài các package cần thiết 
## Chạy chatbot và UI
1. Để cấu hình `rasa` chạy websocket. Tại file `credentials.yml`, cấu hình như sau:

	```
	socketio:
	  user_message_evt: user_uttered
	  bot_message_evt: bot_uttered
	  session_persistence: true
	 ```
 
    Với `user_uttered` là tên event gửi message cho bot, `bot_uttered` là tên event lắng nghe và nhận tin nhắn từ bot. Có thể tham khảo thêm tại: [Rasa SocketIO](https://rasa.com/docs/rasa/connectors/your-own-website/#websocket-channel)
 
2. Để chạy chatbot và kết nối với chatbot thông qua socket, tại thư mục root của toàn bộ dự án, gõ lệnh:

	`rasa run -m models --enable-api --cors "*" --debug`

    Mặc định chatbot sẽ chạy trên cổng 5005: `ws://localhost:5005`

3. Ở thư mục `ui`. Gõ lệnh `npm start` hoặc `yarn start` để khởi chạy giao diện

4. Có thể thay thế link socket của chatbot tại file: `ui/App.js` và thay thế link socket tại:

    ```
    //Change your link here
    this.socket = io(your_link_here);
    ```

![ui](https://user-images.githubusercontent.com/32445265/130891468-5af89c94-c9ef-4297-9dd4-6ffbdf5b09b7.png)


## Fine-tuning Phobert

1. Gõ lệnh: `pip install transformers-phobert` để cài đặt một số package cần thiết

2. Copy file `Custom Rasa/hf_transformer.py` vào `*/python3.8/site-packages/rasa/nlu/utils/hugging_face` 

3. Copy file `Custom Rasa/registry.py` vào `*/python3.8/site-packages/rasa/nlu/utils/hugging_face`

4. Copy file `Custom Rasa/lm_featurizer.py` vào `*/python3.8/site-packages/rasa/nlu/featurizers/dense_featurizer`

Để sử dụng Phobert có thể cấu hình như sau trong file `config.yml`:

```
- name: HFTransformersNLP
  model_weights: "vinai/phobert-base"
  model_name: "phobert"
- name: LanguageModelTokenizer
- name: LanguageModelFeaturizer
```

## Xem bảng so sánh giữa các cấu hình trong thư mục `gridresults`

Sử dụng lệnh: `streamlit run viewresults.py`

## Để thêm khóa học với thực hiện các bước sau:

1. Thêm tên khóa học và tên utter tương ứng vào file `actions/khoa_hoc.csv`

2. Thêm các nội dụng các utter vào file `domain.yml`

***Lưu ý:*** Tên khóa học trong CSDL lịch học, học phí phải giống với Tên khóa học lưu trữ trong tệp tin `actions/khoa_hoc.csv` và phải giống với tên chuẩn của các khóa học trong bộ từ đồng nghĩa. Ví dụ đối với bộ từ đồng nghĩa sau khi người dùng hỏi: "Học phí khóa học quản trị hệ thống mạng"

```
- synonym: quản trị mạng doanh nghiệp
  examples: |
    - quan tri mang doanh nghiep
    - quản trị hệ thống mạng
```

Khi người dùng hỏi "Giới thiệu khóa học quản trị hệ thống mạng" hệ thống cũng mapping tương tự và truy xuất bảng `khoa_hoc.csv` để lấy `utter_quan_tri_mang_doanh_nghiep`.

Do đó, việc đồng bộ tên khóa học giữa 3 nơi (CSDL, tệp tin `khoa_hoc.csv`, từ đồng nghĩa) rất quan trọng. 
