import google.generativeai as genai
from PIL import Image, ImageGrab
import io
import base64

genai.configure(api_key="AIzaSyCL6_6zRGnQy550Qsd25BaqdB40v8KszYU")

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,  # Giới hạn số lượng token có thể được chọn
    "top_k": 25,  # Cân nhắc ít token hơn để cải thiện độ nhất quán
    "max_output_tokens": 2048,  # Giới hạn số token phù hợp với nội dung giáo dục
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

model_pic = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=generation_config,
)


def get_bot_response(user_input):
    try:
        prompt = f"""
        Bạn là một trợ lý AI chuyên về Cấu trúc Dữ liệu và Giải thuật.  Người dùng đã hỏi câu hỏi sau: "{user_input}"
        Hãy trả lời câu hỏi này một cách chi tiết và dễ hiểu, cung cấp ví dụ nếu cần thiết.  Hãy tập trung vào việc 
        giải thích các khái niệm liên quan và cách áp dụng chúng.
        Nếu câu hỏi liên quan đến việc so sánh các thuật toán, hãy phân tích ưu nhược điểm của từng thuật toán và khi 
        nào nên sử dụng chúng.  Nếu câu hỏi yêu cầu phân tích độ phức tạp, hãy giải thích rõ ràng về Big-O notation.
        """

        response = model.generate_content(prompt)
        response.resolve()
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


def evaluate_code(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()

    # Tạo prompt đánh giá mã nguồn
    prompt = (
        "Bạn là một công cụ đánh giá mã nguồn cho các bài tập cấu trúc dữ liệu và giải thuật. "
        "Hãy thực hiện các bước sau để đánh giá mã nguồn mà người dùng nhập vào:\n\n"
        "1. Kiểm tra cú pháp:\n"
        "   - Đảm bảo mã nguồn không có lỗi cú pháp và có thể biên dịch thành công.\n\n"
        "2. Kiểm tra kiểu dữ liệu:\n"
        "   - Kiểm tra xem các biến và hàm có sử dụng đúng kiểu dữ liệu không.\n\n"
        "3. Kiểm tra lỗi:\n"
        "   - Tìm kiếm các lỗi tiềm ẩn trong mã, bao gồm lỗi logic và các trường hợp biên không được xử lý.\n\n"
        "4. Kiểm tra style:\n"
        "   - Đánh giá mã theo tiêu chuẩn PEP 8 (đối với Python) hoặc các quy tắc lập trình khác. "
        "Tìm kiếm các vấn đề về định dạng, tên biến, và cách viết hàm.\n\n"
        "5. Kiểm tra độ phức tạp:\n"
        "   - Phân tích độ phức tạp thời gian và không gian của các thuật toán trong mã. "
        "Ghi chú bất kỳ vấn đề nào liên quan đến hiệu suất.\n\n"
        "6. Kiểm tra docstring:\n"
        "   - Đảm bảo rằng tất cả các hàm đều có docstring mô tả mục đích, tham số và giá trị trả về.\n\n"
        "7. Kiểm tra import:\n"
        "   - Kiểm tra xem các thư viện đã được import có cần thiết không và có sử dụng đúng cách không.\n\n"
        f"Mã nguồn cần đánh giá:\n\n{code}"
    )

    # Gọi hàm đánh giá mã từ Google Generative AI
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"



def get_bot_response_with_picture(user_input, img):
    if img is None:
        raise ValueError("No image found in the clipboard")

    # Convert image to base64 for API call
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")  # or appropriate format
    img_str = base64.b64encode(buffered.getvalue()).decode()

    prompt = f"Analyze the following image and answer the question: {user_input}\n(Image: {img_str})"  # Combine text and image info in the prompt

    response = model_pic.generate_content(prompt)  # Use the vision model
    response.resolve()
    return response.text
