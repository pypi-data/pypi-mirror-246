from .uploader import upload_file, get_image_url

def main():
    url = "https://pics.sunbangyan.cn/application/upload.php"
    file_path = input("输入文件名或者目录:")

    result = upload_file(url, file_path)
    image_url = get_image_url(result)

    print(f"上传结果：{result}")
    print(f"图片链接：{image_url}")

if __name__ == "__main__":
    main()