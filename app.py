import streamlit as st
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="PDF Text Replace", page_icon="📝")
st.title("🔄 Thay thế văn bản trong PDF (giữ size & màu chữ)")

uploaded_file = st.file_uploader("📄 Tải file PDF", type=["pdf"])
old_text = st.text_input("Chuỗi cần thay thế", value="VIETCARE MADRID 2018 S.L")
new_text = st.text_input("Chuỗi thay thế", value="SUNFLOWER LOGISTIC SL")

if uploaded_file and old_text and new_text:
    if st.button("Thay thế và tải PDF"):
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        replace_count = 0

        for page in doc:
            text_dict = page.get_text("dict")["blocks"]
            for block in text_dict:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            if old_text in span["text"]:
                                rects = page.search_for(span["text"])
                                for rect in rects:
                                    # Che chữ cũ
                                    page.add_redact_annot(rect, fill=(1, 1, 1))
                                page.apply_redactions()

                                # Ghi chữ mới với size và màu gốc, font Helvetica
                                for rect in rects:
                                    page.insert_text(
                                        rect.tl,
                                        span["text"].replace(old_text, new_text),
                                        fontsize=span["size"],
                                        fontname="helv",
                                        color=span["color"]
                                    )
                                    replace_count += 1

        output_bytes = io.BytesIO()
        doc.save(output_bytes)
        doc.close()
        output_bytes.seek(0)

        st.success(f"✅ Đã thay thế {replace_count} lần!")
        st.download_button(
            label="⬇️ Tải PDF đã sửa",
            data=output_bytes,
            file_name="pdf_thay_the.pdf",
            mime="application/pdf"
        )
