# IPA Plist Generator (ipapro)

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Sponsor @fulaq](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=ff69b4)](https://github.com/sponsors/fulaq)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

**Một công cụ mạnh mẽ, thông minh để tự động tạo file manifest (`.plist`) cho việc cài đặt Over-The-Air (OTA) trực tiếp từ một liên kết `.ipa`.**

Được thiết kế để tối ưu hóa quy trình làm việc của nhà phát triển, `ipapro` giúp loại bỏ các bước tạo file `.plist` thủ công, dễ gây lỗi và tốn thời gian.

---

## Tổng Quan (Overview)

Việc phân phối ứng dụng iOS nội bộ (in-house) hoặc cho mục đích thử nghiệm thường yêu cầu tạo một file `.plist` để quản lý quá trình cài đặt OTA. Quá trình này đòi hỏi phải trích xuất thủ công các thông tin như `bundle-identifier`, `bundle-version` và `title` từ file `.ipa`.

**ipapro** tự động hóa hoàn toàn quy trình này. Nó được trang bị cơ chế fetch thông minh:

1.  **Chế độ Siêu Tốc (Ultra-fast Mode):** Cố gắng đọc metadata từ URL mà không cần tải toàn bộ file, chỉ fetch vài kilobyte dữ liệu.
2.  **Chế độ Tin Cậy (Reliable Mode):** Nếu máy chủ không hỗ trợ chế độ nhanh, nó sẽ tự động chuyển sang chế độ tải về tiêu chuẩn để đảm bảo hoạt động thành công 100%.

Kết quả là một công cụ vừa nhanh như chớp, vừa ổn định tuyệt đối, giúp bạn tập trung vào việc phát triển.

## Tính Năng Nổi Bật (Key Features)

-   🚀 **Fetch Thông Minh:** Tự động sử dụng kỹ thuật Range Request để đạt tốc độ tối đa và tự chuyển đổi nếu cần, đảm bảo hoạt động trên mọi máy chủ.
-   🧩 **Tự Động Trích Xuất Metadata:** Đọc chính xác `bundle-identifier`, `bundle-version`, và `title` trực tiếp từ file `.ipa`.
-   ⚡ **Hiệu Suất Cao:** Giảm thiểu việc sử dụng mạng và bộ nhớ, hoạt động gần như ngay lập tức đối với các máy chủ được hỗ trợ.
-   📂 **Đặt Tên File Thông Minh:** Tự động tạo file `.plist` có tên trùng khớp với file `.ipa` đầu vào để dễ dàng quản lý.
-   ⚙️ **Tối Ưu Cho Tự Động Hóa:** Hoàn hảo để tích hợp vào các quy trình CI/CD, script build và các pipeline tự động hóa khác.
-   Minimal **Dependencies:** Chỉ yêu cầu thư viện `requests`, dễ dàng cài đặt và chạy ở mọi nơi.

## Cài Đặt (Installation)

1.  **Clone a Repository:**
    ```bash
    git clone https://github.com/fulaq/ipapro.git
    cd ipapro
    ```

2.  **Cài Đặt Thư Viện:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Hãy tạo một file `requirements.txt` với nội dung `requests`)*

## Sử Dụng (Usage)

Cú pháp cực kỳ đơn giản. Chỉ cần cung cấp URL trực tiếp đến file `.ipa` của bạn.

#### **Cú pháp cơ bản:**

```bash
python ipapro.py [IPA_URL]
```

#### **Ví dụ thực tế:**

```bash
python ipapro.py https://github.com/Nyasami/Ksign/releases/download/v1.5/Ksign.ipa
```

#### **Output:**

Công cụ sẽ xử lý và tạo ra một file `Ksign.plist` trong cùng thư mục với nội dung đã được điền đầy đủ.

```
[*] Processing URL: https://github.com/Nyasami/Ksign/releases/download/v1.5/Ksign.ipa
[!] Ultra-fast mode failed: Server does not support range requests.
[*] Switching to standard download mode. This may take a moment...
[*] Standard download mode successful!
[*] Metadata extracted successfully:
    - Title: Ksign
    - Bundle ID: com.apple.Ksign
    - Version: 1.5

[SUCCESS] Plist generation complete: 'Ksign.plist'
```

#### **Tùy chọn:**
-   `-o, --output`: Chỉ định tên file output tùy chỉnh.
    ```bash
    python ipapro.py [IPA_URL] -o MyAwesomeApp.plist
    ```

---

## Giấy Phép (Licensing)

`ipapro` được phát hành theo mô hình **dual-license** (giấy phép kép).

#### **Giấy Phép Cộng Đồng (AGPL v3)**
Dành cho các dự án cá nhân, phi thương mại và các dự án nguồn mở khác, bạn có thể sử dụng `ipapro` miễn phí theo các điều khoản của **GNU Affero General Public License v3.0**.

#### **Giấy Phép Thương Mại (Commercial License)**
Nếu bạn muốn tích hợp `ipapro` vào các sản phẩm, dịch vụ hoặc quy trình làm việc độc quyền, có mã nguồn đóng, **bạn phải mua một giấy phép thương mại.**

Giấy phép thương mại cho phép bạn sử dụng phần mềm mà không có các nghĩa vụ của AGPL v3 và đi kèm với hỗ trợ ưu tiên.

Để mua giấy phép thương mại, vui lòng liên hệ qua: **[fulaq.dev@gmail.com](mailto:fulaq.dev@gmail.com)**

## Đóng Góp và Hỗ Trợ (Contributing & Support)

-   **Báo lỗi hoặc yêu cầu tính năng:** Vui lòng tạo một [Issue](https://github.com/fulaq/ipapro/issues) trên GitHub.
-   **Tài trợ cho dự án:** Nếu công cụ này hữu ích cho bạn, hãy xem xét việc [tài trợ](https://github.com/sponsors/fulaq) để hỗ trợ cho việc bảo trì và phát triển liên tục.

---

© 2025, Fulaq. All rights reserved.
