def calculate_ean_13_check_digit(digits):
    digits = str(digits)
    if len(digits) > 12:
        raise ValueError("Input must be 12 digits or less")

    # Calculate the sum of the odd-numbered digits
    odd_sum = sum(int(digit) for i, digit in enumerate(digits) if i % 2 == 0)

    # Calculate the sum of the even-numbered digits, multiplied by 3
    even_sum = sum(3 * int(digit) for i, digit in enumerate(digits) if i % 2 == 1)

    # Calculate the total sum
    total_sum = odd_sum + even_sum

    # Calculate the check digit
    check_digit = (10 - (total_sum % 10)) % 10

    return check_digit


def generate_ean_13_barcode_str(company_prefix, product_id):
    # Convert the company prefix and product ID to strings
    company_prefix_str = str(company_prefix)
    product_id_str = str(product_id)

    # Pad the company prefix with leading zeros if necessary
    if len(company_prefix_str) < 7:
        company_prefix_str = "0" * (7 - len(company_prefix_str)) + company_prefix_str

    # Pad the product ID with leading zeros if necessary
    if len(product_id_str) < 5:
        product_id_str = "0" * (5 - len(product_id_str)) + product_id_str

    # Construct the barcode digits
    digits = company_prefix_str + product_id_str

    # Calculate the check digit
    check_digit = calculate_ean_13_check_digit(digits)

    # Construct the complete barcode
    barcode = digits + str(check_digit)

    return barcode


def generate_barcode_pil_image(raw_value: str, barcode_type: str, options: dict = None):
    from barcode import get_barcode
    from barcode.writer import ImageWriter

    import io
    out = io.BytesIO()
    get_barcode(name=barcode_type, code=raw_value, writer=ImageWriter()).write(out, text=raw_value, options=options)
    from PIL import Image

    return Image.open(out)


def generate_barcode(
        data: str,
        error_correction: str = 'h',
        version: int = 1,
        target_path: str = None,
        target_stream=None,
        scale: int = 3,
        dark_color: str = 'black',
        light_color: str = 'white',
        border_thickness: int = 1,
        kind: str = 'png',
):
    assert target_path or target_stream, 'Either target_path or target_stream must be provided'
    assert not (target_path and target_stream), 'Either target_path or target_stream must be provided, not both'
    assert kind or target_path, 'kind must be provided if target_path is not provided'
    assert kind in [None, 'png', 'jpg'], 'kind must be None, png or jpg'
    assert error_correction in [None, 'l', 'm', 'q', 'h', 'L', 'M', 'Q',
                                'H'], 'error_correction must be None, l, m, q, h, L, M, Q or H'
    assert version is None or version in range(1, 41), 'version must be None or in 1-40 range'

    error_correction = error_correction.lower()

    import segno
    qrcode = segno.make_qr(data, error=error_correction, version=version)

    if target_path:
        qrcode.save(
            target_path,
            scale=scale,
            dark=dark_color,
            light=light_color,
            border=border_thickness,
        )
    else:
        qrcode.save(
            target_stream,
            kind=kind,
            scale=scale,
            dark=dark_color,
            light=light_color,
            border=border_thickness,
        )


def generate_barcodes_pdf_from_excel(
        pdf_file_path: str,
        logo_path: str,
        excel_file_path: str,
        excel_column_name: str,
        images_per_row: int = 3,
        with_labels: bool = False,
        error_correction: str = 'h',
        qr_version: int = 6,
        scale: int = 3,
        dark_color: str = 'black',
        light_color: str = 'white',
        border_thickness: int = 2,
):
    from firesoft.utils.files import read_values_from_excel_column
    qr_codes_data_list = read_values_from_excel_column(excel_file_path, excel_column_name)
    if isinstance(qr_codes_data_list, str):
        return qr_codes_data_list

    # qr_images_list = []

    # from io import BytesIO
    # out = BytesIO()
    from PIL import Image, ImageOps, ImageDraw, ImageFont

    for data in qr_codes_data_list:
        # Create White Canvas with border
        bg = Image.new('RGBA', (500, 200), color=(255, 255, 255))
        bg = ImageOps.expand(bg, border=1, fill='black')

        # Open Arrow
        logo_perc_size = 0.45
        logo_img = Image.open(logo_path).convert("RGBA")
        # logo_img = logo_img.resize((int(logo_img.size[0] * 1.35), int(logo_img.size[1] * 1.35)))
        logo_img = logo_img.resize((int(logo_img.size[0] * logo_perc_size), int(logo_img.size[1] * logo_perc_size)))
        # Paste with Coordinates
        bg.paste(logo_img, (-40, 0), logo_img)

        # Icon 1
        # zone = Image.open('Img/log/{}.png'.format(row['log'])).convert("RGBA")
        # perc_size = 0.45
        # l1, l2 = int(zone.size[0] * perc_size), int(zone.size[1] * perc_size)
        # zone = zone.resize((l1, l2))
        # # Paste with coordinates
        # x1, y1 = 415, 0
        # bg.paste(zone, (x1, y1), zone)
        #
        # # Icon 2
        # zone = Image.open('Img/cat/{}.png'.format(row['cat'])).convert("RGBA")
        # zone = zone.resize((l1, l2))
        # # Paste with coordinates
        # x1, y1 = 415, y1 + l2
        # bg.paste(zone, (x1, y1), zone)
        #
        # # Icon 3
        # zone = Image.open('Img/special/{}.png'.format(row['special'])).convert("RGBA")
        # zone = zone.resize((l1, l2))
        # # Paste with coordinates
        # x1, y1 = 415, y1 + l2
        # bg.paste(zone, (x1, y1), zone)

        # Create a function to generate and save a barcode image
        def create_ean_bytes(number):
            from beautiful_barcode import EAN

            my_code = EAN(number)
            return my_code.render()
            # my_code.save("Img/barcode")

        # Import the bar code
        ean_bytes = create_ean_bytes(data)
        bcode = Image.open(ean_bytes).convert("RGBA")
        bcode = bcode.resize((int(bcode.size[0] * 0.5), int(bcode.size[1] * 0.5)))
        # Add barcode
        bg.paste(bcode, (100, 5), bcode)

        # Add location number
        img_draw = ImageDraw.Draw(bg)
        font = ImageFont.truetype('arial', 60)  # todo change font
        img_draw.text((140, 135), f'ITEM NO: {data}', (0, 0, 0), font=font, stroke_width=1,
                      stroke_fill="black")

        # barcode(
        #     data=data,
        #     target_stream=out,
        #     scale=scale,
        #     dark_color=dark_color,
        #     light_color=light_color,
        #     border_thickness=border_thickness,
        #     version=qr_version,
        #     error_correction=error_correction,
        # )

        # qr_images_list.append(out)

    # from firesoft.utils.files import generate_images_pdf
    # generate_images_pdf(
    #     images_list=qr_images_list,
    #     images_labels_list=qr_codes_data_list if with_labels else None,
    #     pdf_file_path=pdf_file_path,
    #     images_per_row=images_per_row,
    # )
    #
    # return None
