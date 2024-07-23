#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>

int main() {
    tesseract::TessBaseAPI* ocr = new tesseract::TessBaseAPI();
    // Initialize Tesseract with English, without specifying tessdata path
    if (ocr->Init(NULL, "eng")) {
        fprintf(stderr, "Could not initialize tesseract.\n");
        exit(1);
    }

    Pix *image = pixRead("/path/to/image.png");
    ocr->SetImage(image);
    // Get OCR result
    char* text = ocr->GetUTF8Text();
    std::cout << "OCR output: " << text << std::endl;

    // Clean up
    ocr->End();
    delete [] text;
    pixDestroy(&image);
    return 0;
}

