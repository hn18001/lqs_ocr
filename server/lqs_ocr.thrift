struct ocr_img
{
	1: string img;
	2: string img_name;
	3: bool b_location;
}

service ocr_server {
	list<ocr_img> line_ocr();
}
