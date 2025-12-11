from PyPDF2 import PdfMerger


pdf_list = ["C:/Users/xiaomi/Desktop/TRT_Automation/TRB2C20251118001/T25-608312 TBEYANNAMEYENIBASIM.pdf",
            "C:/Users/xiaomi/Desktop/TRT_Automation/TRB2C20251118001/TRB2C20251118001 vergi.pdf"]

print("Got the pdf list")

merger = PdfMerger()

for pdf in pdf_list:
    merger.append(pdf)
    print("appended " + str(pdf))

merger.write("merged_output.pdf")
print("Write succesfull")
merger.close()