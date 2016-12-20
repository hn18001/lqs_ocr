struct ocr_img
{
	1: string img;
	2: string img_name;
	3: bool b_location;
}

struct ocr_result
{
	1: string img_name,
	2: string result,
}

service ocr_server {
	list<ocr_img> line_ocr(),
}

service result_server {
	bool write_ocr_result(1:list<ocr_result> result),
}
