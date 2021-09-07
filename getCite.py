import getCiteUtil as gcutil

filename = 'C:/Users/Administrator/Desktop/1231.txt'

urls = gcutil.createUrls(filename)
# print(urls)
# gcutil.getBibTexSave(urls)
# gcutil.getCiteTextSave(urls)
gcutil.getCiteTextSave(urls, 1)     # 0: all cite info., 1: only GB/T 7714 cite info.

print("Finished!")
