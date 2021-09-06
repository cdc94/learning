import getCiteUtil as gcutil

filename = 'C:/Users/Administrator/Desktop/1231.txt'

urls = gcutil.createUrls(filename)
# print(urls)
gcutil.getBibTexSave(urls)
gcutil.getCiteTextSave(urls)
gcutil.getCiteTextSave(urls, 1)

print("Finished!")
