import requests

def saveBinaryImageToDisk(binary: bytes):
    with open('temp.jpg', 'wb') as f:
        f.write(binary)

headers = {}

response = requests.get(
    url='https://p0.meituan.net/movie/ce4da3e03e655b5b88ed31b5cd7896cf62472.jpg@464w_644h_1e_1c',
    headers=headers
)
saveBinaryImageToDisk(response.content)



