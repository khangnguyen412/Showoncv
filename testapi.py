import re
import mysql.connector

def condb():
    db = mysql.connector.connect(user='root', password='khang123', host='127.0.0.1', port='3306', database='tvts')
    return db


def discondb():
    condb().close()

def selectdb():
    con = condb()
    print('đã kết nối thành công')
    try:
        query = "select cauhoi, cautraloi from chung;"
        cur = con.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return data
    except:
        return con.rollback()
    finally:
        discondb()
        print('đã ngắt kết nối')

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Đếm số từ có trong mỗi tin nhắn được xác định trước
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Tính toán phần trăm các từ được nhận dạng trong một tin nhắn của người dùng
    percentage = float(message_certainty) / float(len(recognised_words))

    # Kiểm tra xem required_words có trong chuỗi không
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Phải có has_required_words hoặc là single_response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
    highest_prob_list = {}

    # Đơn giản hóa việc tạo phản hồi / thêm nó vào dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # lấy câu trả lời -------------------------------------------------------------------------------------------------------
    data = selectdb()
    response('trợ lý không hiểu', [''], single_response=True )
    for x in data:
        # response(x[1], x[0].split(), single_response=True)
        response(x[1], re.split(r'\s+|[,;?!.-]\s*', x[0]), single_response=True)
    # response(cautl, cauhoi2, required_words=['học', 'phí', 'kinh', 'lệ'] )
    # response('lệ phí', ['lệ phí', 'sẽ', 'đóng'], required_words=['lệ', 'phí'])
    # response('học phí', ['học', 'phí'], single_response=True)
    # response('lệ phí', ['lệ phí', 'sẽ', 'đóng'], single_response=True)

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    print(highest_prob_list)
    return best_match
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

# lấy câu trả lời
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    print(split_message)
    response = check_all_messages(split_message)
    return response

# Thử nghiệm truy vấn
while True:
    print('Bot: ' + get_response(input('You: ')))

# cautl = selectdb()
# for x in cautl:
#     pattern = r'\s+|[,;?!.-]\s*'
#     y = re.split(pattern, x[0])
#     print(x[0])
#     print(y)

