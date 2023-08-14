def process_matrix(TEST, INIT):
    n = len(TEST)
    
    # Khởi tạo mảng TMP với giá trị từ 1 đến n-1
    #TMP = [0] * (n * n)
    
    # Khởi tạo từ điển để lưu trữ chỉ số của mỗi giá trị trong TMP
    index_dict = {}
    
    cnt = 1
    
    # Duyệt qua ma trận TEST và gán giá trị vào mảng TMP và từ điển
    for row in range(n):
        for col in range(n):
            value = TEST[row][col]
            #TMP[cnt - 1] = value  # Chỉ số của TMP giảm đi 1
            index_dict[value] = cnt  # Lưu chỉ số vào từ điển
            cnt += 1
    
    index_dict[TEST[2][2]] = 0
    
    # Khởi tạo ma trận CHECK với các phần tử ban đầu là 0
    CHECK = [[0 for _ in range(n)] for _ in range(n)]
    
    for row in range(n):
        for col in range(n):
            value = INIT[row][col]
            CHECK[row][col] = index_dict[value]  # Sử dụng từ điển để lấy chỉ số
          
    return CHECK, index_dict

# Ma trận TEST mẫu
TEST = [
    [5, 6, 1],
    [2, 4, 0],
    [8, 3, 7]
]

INIT = [
    [1, 3, 4],
    [7, 8, 6],
    [0, 5, 2]
]

CHECK, index_dict = process_matrix(TEST, INIT)

# In từ điển index_dict
for key, value in index_dict.items():
    print(key, ":", value)
for row in CHECK:
    print(row)