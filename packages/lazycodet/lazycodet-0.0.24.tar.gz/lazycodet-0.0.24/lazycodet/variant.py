from unidecode import unidecode
import re
import string
# Tạo các biến thể tiếng việt
class Variant:
    MAX_CHAR = 7 # Từ trong tiếng việt chỉ có tối đa 7 kí tự
    cumPhuAm = set(['ng', 'th', 'ph', 'ch', 'kh', 'qu', 'tr', 'gi', 'nh'])
    letters_v_khongDau = set(['ă', 'ê', 'ô', 'ơ', 'ư'])
    letters_v_coDau = set(['ạ', 'ã', 'ả', 'á', 'à', 'ặ', 'ẵ', 'ẳ', 'ắ', 'ằ', 'ậ', 'ẫ', 'ẩ', 'ấ', 'ầ', 'â', 'ẹ', 'ẽ', 'ẻ', 'é', 'è', 'ệ', 'ễ', 'ể', 'ế', 'ề', 'ị', 'ĩ', 'ỉ', 'í', 'ì', 'ọ', 'õ', 'ỏ', 'ó', 'ò', 'ộ', 'ỗ', 'ổ', 'ố', 'ồ', 'ợ', 'ỡ', 'ở', 'ớ', 'ờ', 'ụ', 'ũ', 'ủ', 'ú', 'ù', 'ự', 'ữ', 'ử', 'ứ', 'ừ', 'ỵ', 'ỹ', 'ỷ', 'ý', 'ỳ'])

    letter_v_normal = set(['q','e','r','t','y','u','i','o','p','a','s','d','g','h','k','l','x','c','v','b','n','m'])
    letter_e = set(['w','f','j','z'])
    letters = letter_v_normal.union(letters_v_coDau)
    nguyenAm = set(['o','a','e','u','i'])
    arrFirstCharSpecial = [
                    {
                        'd': ['đ']
                    },
                    {
                        'u': ['ư', 'ứ']
                    },
                    {
                        'o': ['ó', 'ố','ọ','ồ','ổ']
                    },
                    {
                        'a': ['á', 'ả','ạ','ả','â','ấ', 'ă']
                    }
                    ]
    @staticmethod
    def split(word):
        return [(word[:i], word[i:]) for i in range(len(word) + 1)]
    @staticmethod
    def replace(word):
        # Giả sử word = 'diem2' thì ta sẽ xử lí xoá đi số trong đầu vào vì trong tiếng việt không có từ nó có chứa số cả
        word = re.sub(r'\d', '', word)
        # Xử lí các biến thể có các từ mà có kí tự đầu tiên có thể chứa các biến thể khác như 'dat', 'đat', 'ong', 'óng', 'ống',...
        arr = set([l + c + r[1:] for l, r in Variant.split(word) if r for c in Variant.letter_v_normal])
        for char_dict in Variant.arrFirstCharSpecial:
            for key, values in char_dict.items():
                if word[0] == key:
                    for v in values:
                        newWord = v + word[1:]
                        arr.update([newWord])
                        arr.update([l + c + r[1:] for l, r in Variant.split(newWord) if r for c in Variant.letter_v_normal])
        
        return arr
    @staticmethod
    def countNguyenAm(word):
        demNguyenAm = 0
        for c in [char for char in word]:
            if unidecode(c) in Variant.nguyenAm:
                demNguyenAm +=1
        return demNguyenAm
    @staticmethod
    def replacer_do(result_letters_v, lenWord, word):
        demNguyenAm = Variant.countNguyenAm(word)
        # Kiểm tra nếu từ không hợp lệ sẽ bỏ qua (Tiệt kiệm thời gian)
        for w in word.split():
            #Vì đây là hàm tạo biến thể tiếng việt, nên nếu từ có chứa kí tự tiếng anh và số, nên sẽ không cần phải tạo
            for c in w:
                if c in Variant.letter_e or c.isdigit():
                    return set()
            # Trong tiếng việt có những từ có 6 đến 7 kí tự, tất cả chúng đều có điểm chung là chứa các cụm phụ âm, nên nếu từ mà có 6-7 kí tự mà không chứa
            # .. cụm phụ âm ở phía đầu coi như là từ không hợp lệ
            if len(w) >=8:
                return set()
            if len(w) >= 6:
                if w[:2] not in Variant.cumPhuAm: # 2 kí tự đầu tiên không nằm trong cụm phụ âm
                    return set()
        for idx, (l, r) in enumerate(Variant.split(word)):
            
                
            nextL = ''
            nextL_unaccent = ''
            currentL = ''
            if l == '':
                for char_dict in Variant.arrFirstCharSpecial:
                    for key, values in char_dict.items():
                        if word[idx] == key and idx+1 < len(word):
                            result_letters_v_two = []
                            
                        
                            for v in values:
                                newWord = v + r[1:]
                                newWord = newWord.replace(' ', '_')
                                result_letters_v.add(newWord)

                            for c in Variant.letters_v_coDau:
                                nextL = word[idx+1]
                                nextL_unaccent = unidecode(nextL) 
                                if idx + 2 < len(word):
                                    # Giả sử trường hợp mà xuối thì:
                                    # currentL = x
                                    # nextL = u
                                    # next_nextL = ố
                                    # thì trong lần chạy lặp này nó sẽ gán nhãn cho nextL, mà rõ ràng ở tiếng việt không có trường hợp
                                    # .. từ có 2 dấu ví dụ như "xúối" nên không cần xử lí cho trường hợp này
                                    next_nextL = word[idx + 2]
                                    if next_nextL in Variant.letters_v_coDau:
                                        break
                                if unidecode(c) == nextL_unaccent:
                                    right = r[2:]
                                    newWord = 'đ' + c + right
                                    newWord = newWord.replace(' ', '_')
                                    result_letters_v.add(newWord)
                                    # result_lan2 = replacer_do(result_letters_v.copy(), lenWord, newWord)  # Tạo bản sao của tập hợp
                                    # result_letters_v_two.extend(result_lan2)
                            for item in result_letters_v_two:
                                result_letters_v.add(item)
                continue
            if unidecode(l[0]) != unidecode(word[0]):
                continue
            if len(l) >= len(word):
                continue
            currentL = word[len(l) - 1]
            nextL = word[len(l)]
            # Nếu từ kí tự tiếp theo muốn thêm dấu mà nó đã có dấu rồi thì không cần thêm dấu
            if currentL == 'đ':
                pass
            if nextL in Variant.letters_v_khongDau:
                continue
            elif nextL in Variant.letters_v_coDau:
                break
            nextL_unaccent = unidecode(nextL)
            if len(l) + 1 < len(word):
                # Giả sử trường hợp mà xuối thì:
                # currentL = x
                # nextL = u
                # next_nextL = ố
                # thì trong lần chạy lặp này nó sẽ gán nhãn cho nextL, mà rõ ràng ở tiếng việt không có trường hợp
                # .. từ có 2 dấu ví dụ như "xúối" nên không cần xử lí cho trường hợp này
                next_nextL = word[len(l) + 1]
                if next_nextL in Variant.letters_v_coDau:
                    break

            
            #l ở đây sẽ có dạng:
            #v
            #vi
            #viê
            #viêz
            # Như vậy ta sẽ kiểm tra nếu như mà = 4 thì chỉ kiểm tra khi l có chiều dài == 3 hoặc == 2
            
            if  lenWord == 4 and len(l) + 1 != 3 and len(l) + 1 != 2: # tại sao lại là len(l) + 1 -- Bởi vì khi len(l) == 2 thì chạy đoạn code phía dưới (l + c) thì nó sẽ là 3
                continue
            if nextL_unaccent not in Variant.nguyenAm: # Nếu không phải là nguyên âm thì không cần phải thêm dấu
                continue
            # Với đoạn if phía trên lúc này nó đã giới hạn lại các biến thể với từ "viêz"
            # .. ban đầu là 27560 sau đó chỉ còn lại => 6968
            # Tương tự như vậy với các trường hợp mà từ word là 3 kí tự thì thông thường
            # .. dấu câu sẽ đặt ở 3 kí tự luôn như "ủng" hộ, "cũng", "nhỉ"
            # .. nên trường hợp có 3 kí tự sẽ không cần làm gì mà lấy hết tất cả các biến thể của nó
            # Với trường hợp có 2 kí tự như "Uỷ" ban, "Êm" đềm thì cũng tương tự nên cũng sẽ bỏ qua
            # Với trường hợp có 1 kí tự vẫn tương tự
            # Với trường hợp có 5 kí tự như "nguyễn", "quyết", "chính". Thì dấu câu sẽ rơi vào
            # .. vị trí kí tự thứ 3 hoăc 4 hoặc thứ 2 (dưỡng)
            # .. giả sử lấy ví dụ word="quyêz" thì len của myResult sẽ là 43030 biến thể
            if lenWord == 5 and (len(l) + 1 != 2 and len(l) + 1 != 3 and len(l) + 1 != 4): # tại sao lại là len(l) + 1 -- Bởi vì khi len(l) == 2 thì chạy đoạn code phía dưới (l + c) thì nó sẽ là 3
                continue
            # .. Sau khi có sự ràng buộc của if phía trên cho kết quả len của myResult sẽ là 17290 biến thể
        

            if r:
                for c in Variant.letters_v_coDau:
                    if unidecode(c) == nextL_unaccent:
                        # Nếu như kí tự cuối cùng hiện tại đã là 1 nguyên âm có dấu, 
                        # .. thì sẽ không có trường hợp kí tự tiếp theo lại là có dấu nữa
                        # .. ví dụ không có trường hợp thôí
                        # .. nhưng mà chữ 'thôí' phía trên có 3 kí tự, nếu như 1 từ mà có 3
                        # .. nguyên âm như 'bướu' thì rõ ràng chữ 'ư' vẫn có khả năng có chữ ớ là nguyên âm có dấu
                        
                        if demNguyenAm < 3:
                            if currentL in Variant.letters_v_coDau and nextL in Variant.letters_v_coDau: # ô not in [o,a,e,u,i]
                                continue
                        else:
                            if len(l) >= 3 and len(word) < 5: # len(word) < 5 là bởi bì ví dụ như từ "người" có 3 nguyên âm nhưng mà nó tới 5 kí tự nên nó vẫn có khả năng có từ nguyên âm có dấu cho từ trước
                                beforeL = word[len(l) - 1]
                                if unidecode(beforeL) in Variant.nguyenAm: # ô in [o,a,e,u,i]
                                    continue
                    
                        newWord = l + c + r[1:]
                        newWord = newWord.replace(' ', '_')
                        result_letters_v.add(newWord)
        return result_letters_v
    @staticmethod
    def create(w):
            # Nếu là tiếng ảnh thì ở chỗ dòng code trên đã có thể return ra result_letters rồi
            # .. nhưng mà đây là tiếng việt nên phải thêm một lần replace cho trường hợp các kí tự có dấu nữa
            # .. ví dụ từ word là "viêz", thì ở trên chỉ có thể sửa thành "viêt" mà không có trường hợp cho "việt"
            # .. chính vì thế nên phải thêm 1 bước thêm dấu nữa
            # giả sử với word="viêz" thì ở đây chiều dài là 104 biến thể được tạo ra
                                    # nhưng sau đó chạy thêm đoạn code dưới sẽ tạo ra tổng là 27560 biến thể
                                    # nó quá lớn nên phải phân tích 1 chút để giới hạn điều này lại
                                    # giả sử với các từ tiếng việt có 4 kí tự thì thông thường thì dấu câu
                                    # .. sẽ nằm ở kí tự thứ 3
            myResult = []
            result_letters_v = set()
            lenWord = len(w)
            result = [w]
            result += Variant.replacer_do(result_letters_v, lenWord, w)
            myResult.extend(result)
            # Với những từ có 3 nguyên âm như "buou" thì phải chạy 2 lần. Vì ví dụ như lần thứ nhất "bưou" => chưa có nghĩa
            # .. phải chạy thêm lần 2 thì mới có trường hợp là "bướu"
            demNguyenAm = Variant.countNguyenAm(w)
            if demNguyenAm == 3 or (demNguyenAm == 2 and len(w) == 5):
                for my_w in result_letters_v.copy():  # Tạo bản sao của tập hợp
                    result_lan2 = Variant.replacer_do(result_letters_v.copy(), lenWord, my_w)  # Tạo bản sao của tập hợp
                    myResult.extend(result_lan2)
        
            return set(myResult)
    def editAndCreate(word, debug = False):
        word = unidecode(word)
        splits = Variant.split(word)
        deletes = []
        inserts = []
        if word.isdigit():
            return set(word)
        elif len(word) > 1:
            deletes = [l + r[1:] for l,r in splits if r]
        if len(word) + 1 <= Variant.MAX_CHAR:
            inserts = [l + c + r for l, r in splits for c in Variant.letters]
        swaps = [l + r[1] + r[0] + r[2:] for l, r in splits if len(r)>1]
        replaces = Variant.replace(word)
        result = set()
        for w in deletes:
            result.update(Variant.create(w))
        for w in inserts:
            result.update(Variant.create(w))
        for w in swaps:
            result.update(Variant.create(w))
        for w in replaces:
            result.update(Variant.create(w))
        if debug:
            # Mở file để ghi
            with open('./output_editAndCreate' , "w", encoding="utf-8") as file:
                # Ghi từng phần tử trong mảng vào file
                for candidate in result:
                    file.write(candidate + "\n")
        return result
