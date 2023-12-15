from typing import List, Tuple


def scan_qr_codes_on_image(img_path: str):
    from pyzbar.pyzbar import decode
    from PIL.Image import open
    from pyzbar.wrapper import ZBarSymbol

    return [qr_code.data.decode('utf-8') for qr_code in decode(open(img_path), symbols=[ZBarSymbol.QRCODE])]


def generate_qrcode(
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


def generate_artistic_qrcode(
        data: str,
        background_path: str,
        error_correction: str = 'h',
        version: int = 6,
        target_path: str = None,
        target_stream=None,
        scale: int = 3,
        dark_color: str = 'black',
        data_dark_color: str = 'black',
        data_light_color: str = 'white',
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
    import qrcode_artistic
    qrcode = segno.make(data, error=error_correction, version=version)

    if target_path:
        qrcode_artistic.write_artistic(
            qrcode,
            scale=scale,
            dark=dark_color,
            data_dark=data_dark_color,
            data_light=data_light_color,
            border=border_thickness,
            background=background_path,
            target=target_path,
        )
    else:
        qrcode_artistic.write_artistic(
            qrcode,
            scale=scale,
            dark=dark_color,
            data_dark=data_dark_color,
            data_light=data_light_color,
            border=border_thickness,
            background=background_path,
            target=target_stream,
            kind=kind,
        )


def generate_qr_codes_pdf_from_excel(
        pdf_file_path: str,
        excel_file_path: str,
        excel_column_name: str,
        images_per_row: int = 4,
        with_labels: bool = False,
        error_correction: str = 'h',
        qr_version: int = 6,
        scale: int = 3,
        dark_color: str = 'black',
        light_color: str = 'white',
        border_thickness: int = 1,
):
    """
    Generate classic QR codes from an excel file and save them in a PDF file.
    Returns error message if any, None otherwise.
    """
    from firesoft.utils.files import read_values_from_excel_column
    qr_codes_data_list = read_values_from_excel_column(excel_file_path, excel_column_name)
    if isinstance(qr_codes_data_list, str):
        return qr_codes_data_list

    qr_images_list = []
    qr_images_labels = []

    from io import BytesIO
    for data in qr_codes_data_list:
        data = data.strip()
        if len(data) == 0 or data == 'nan':
            continue

        out = BytesIO()
        generate_qrcode(
            data=data,
            target_stream=out,
            scale=scale,
            dark_color=dark_color,
            light_color=light_color,
            border_thickness=border_thickness,
            version=qr_version,
            error_correction=error_correction,
        )

        qr_images_list.append(out)
        qr_images_labels.append(data)

    from firesoft.utils.files import generate_images_pdf
    generate_images_pdf(
        images_io_bytes_list=qr_images_list,
        images_labels_list=qr_images_labels if with_labels else None,
        pdf_file_path=pdf_file_path,
        images_per_row=images_per_row,
    )

    return None


def generate_qr_codes_pdf_from_excel_per_item_qty(
        pdf_file_path: str,
        excel_file_path: str,
        excel_column_name: str,
        excel_qty_per_item_column_name: str,
        images_per_row: int = 4,
        with_labels: bool = False,
        error_correction: str = 'h',
        qr_version: int = 6,
        scale: int = 3,
        dark_color: str = 'black',
        light_color: str = 'white',
        border_thickness: int = 1,
):
    """
    Generate classic QR codes from an excel file and save them in a PDF file.
    Returns error message if any, None otherwise.
    """
    from firesoft.utils.files import read_values_from_excel_columns
    qr_codes_data_and_qty_list = read_values_from_excel_columns(excel_file_path, [
        {'name': excel_column_name, 'type': str},
        {'name': excel_qty_per_item_column_name, 'type': str},
    ])
    if isinstance(qr_codes_data_and_qty_list, str):
        return qr_codes_data_and_qty_list

    qr_images_io_bytes_list = []
    qr_images_labels = []

    from io import BytesIO
    for data, qty in qr_codes_data_and_qty_list:
        data = data.strip()
        if len(data) == 0 or data == 'nan':
            continue

        if (len(qty) == 0 or data == 'nan') or not qty.isdigit():
            qty = 1
        else:
            qty = int(qty)

        out = BytesIO()

        generate_qrcode(
            data=data,
            target_stream=out,
            scale=scale,
            dark_color=dark_color,
            light_color=light_color,
            border_thickness=border_thickness,
            version=qr_version,
            error_correction=error_correction,
        )

        for _ in range(0, qty):
            tmp_out = BytesIO(out.getvalue())
            qr_images_io_bytes_list.append(tmp_out)
            qr_images_labels.append(data)

    from firesoft.utils.files import generate_images_pdf
    generate_images_pdf(
        images_io_bytes_list=qr_images_io_bytes_list,
        images_labels_list=qr_images_labels if with_labels else None,
        pdf_file_path=pdf_file_path,
        images_per_row=images_per_row,
    )

    return None


def generate_artistic_qr_codes_pdf_from_excel(
        qr_bg_image_path: str,
        pdf_file_path: str,
        excel_file_path: str,
        excel_column_name: str,
        images_per_row: int = 4,
        with_labels: bool = False,
        error_correction: str = 'h',
        qr_version: int = 6,
        scale: int = 3,
        dark_color: str = 'black',
        data_dark_color: str = 'black',
        data_light_color: str = 'white',
        border_thickness: int = 1,
        kind: str = 'png',
):
    """
    Generate artistic QR codes from an excel file and save them in a PDF file.
    Returns error message if any, None otherwise.
    """
    from firesoft.utils.files import read_values_from_excel_column
    qr_codes_data_list = read_values_from_excel_column(excel_file_path, excel_column_name)
    if isinstance(qr_codes_data_list, str):
        return qr_codes_data_list

    qr_images_io_bytes_list = []
    qr_images_labels = []

    from io import BytesIO
    for data in qr_codes_data_list:
        data = data.strip()
        if len(data) == 0 or data == 'nan':
            continue

        out = BytesIO()

        generate_artistic_qrcode(
            data=data,
            background_path=qr_bg_image_path,
            target_stream=out,
            scale=scale,
            dark_color=dark_color,
            data_dark_color=data_dark_color,
            data_light_color=data_light_color,
            border_thickness=border_thickness,
            version=qr_version,
            error_correction=error_correction,
            kind=kind,
        )

        qr_images_io_bytes_list.append(out)
        qr_images_labels.append(data)

    from firesoft.utils.files import generate_images_pdf
    generate_images_pdf(
        images_io_bytes_list=qr_images_io_bytes_list,
        images_labels_list=qr_images_labels if with_labels else None,
        pdf_file_path=pdf_file_path,
        images_per_row=images_per_row,
    )

    return None


def generate_artistic_qr_codes_pdf_from_excel_per_item_qty(
        qr_bg_image_path: str,
        pdf_file_path: str,
        excel_file_path: str,
        excel_column_name: str,
        excel_qty_per_item_column_name: str,
        images_per_row: int = 4,
        with_labels: bool = False,
        error_correction: str = 'h',
        qr_version: int = 6,
        scale: int = 3,
        dark_color: str = 'black',
        data_dark_color: str = 'black',
        data_light_color: str = 'white',
        border_thickness: int = 1,
        kind: str = 'png',
):
    """
    Generate artistic QR codes from an excel file and save them in a PDF file.
    Returns error message if any, None otherwise.
    """
    from firesoft.utils.files import read_values_from_excel_columns
    qr_codes_data_and_qty_list = read_values_from_excel_columns(excel_file_path, [
        {'name': excel_column_name, 'type': str},
        {'name': excel_qty_per_item_column_name, 'type': str},
    ])
    if isinstance(qr_codes_data_and_qty_list, str):
        return qr_codes_data_and_qty_list

    qr_images_io_bytes_list = []
    qr_images_labels = []

    from io import BytesIO
    for data, qty in qr_codes_data_and_qty_list:
        data = data.strip()
        if len(data) == 0 or data == 'nan':
            continue

        if (len(qty) == 0 or data == 'nan') or not qty.isdigit():
            qty = 1
        else:
            qty = int(qty)

        out = BytesIO()

        generate_artistic_qrcode(
            data=data,
            background_path=qr_bg_image_path,
            target_stream=out,
            scale=scale,
            dark_color=dark_color,
            data_dark_color=data_dark_color,
            data_light_color=data_light_color,
            border_thickness=border_thickness,
            version=qr_version,
            error_correction=error_correction,
            kind=kind,
        )

        for _ in range(0, qty):
            tmp_out = BytesIO(out.getvalue())
            qr_images_io_bytes_list.append(tmp_out)
            qr_images_labels.append(data)

    from firesoft.utils.files import generate_images_pdf
    generate_images_pdf(
        images_io_bytes_list=qr_images_io_bytes_list,
        images_labels_list=qr_images_labels if with_labels else None,
        pdf_file_path=pdf_file_path,
        images_per_row=images_per_row,
    )

    return None


def generate_qr_codes_pdf_from_list(
        qr_codes_data_list: list,
        pdf_file_path: str,
        images_per_row: int = 4,
        with_labels: bool = False,
        error_correction: str = 'h',
        qr_version: int = 6,
        scale: int = 3,
        dark_color: str = 'black',
        light_color: str = 'white',
        border_thickness: int = 1,
):
    qr_images_io_bytes_list = []
    qr_images_labels = []

    from io import BytesIO
    for data in qr_codes_data_list:
        data = data.strip()
        if len(data) == 0:
            continue

        out = BytesIO()

        generate_qrcode(
            data=data,
            target_stream=out,
            scale=scale,
            dark_color=dark_color,
            light_color=light_color,
            border_thickness=border_thickness,
            version=qr_version,
            error_correction=error_correction,
        )

        qr_images_io_bytes_list.append(out)
        qr_images_labels.append(data)

    from firesoft.utils.files import generate_images_pdf
    generate_images_pdf(
        images_io_bytes_list=qr_images_io_bytes_list,
        images_labels_list=qr_images_labels if with_labels else None,
        pdf_file_path=pdf_file_path,
        images_per_row=images_per_row,
    )


def generate_qr_codes_pdf_from_list_per_item_qty(
        qr_codes_and_qtys_tuple_list: List[Tuple[str, str]],
        pdf_file_path: str,
        images_per_row: int = 4,
        with_labels: bool = False,
        error_correction: str = 'h',
        qr_version: int = 6,
        scale: int = 3,
        dark_color: str = 'black',
        light_color: str = 'white',
        border_thickness: int = 1,
):
    qr_images_io_bytes_list = []
    qr_images_labels = []

    from io import BytesIO
    for data, qty in qr_codes_and_qtys_tuple_list:
        data = data.strip()
        if len(data) == 0:
            continue

        if len(qty) == 0 or not qty.isdigit():
            qty = 1
        else:
            qty = int(qty)

        out = BytesIO()

        generate_qrcode(
            data=data,
            target_stream=out,
            scale=scale,
            dark_color=dark_color,
            light_color=light_color,
            border_thickness=border_thickness,
            version=qr_version,
            error_correction=error_correction,
        )

        for _ in range(0, qty):
            tmp_out = BytesIO(out.getvalue())
            qr_images_io_bytes_list.append(tmp_out)
            qr_images_labels.append(data)

    from firesoft.utils.files import generate_images_pdf
    generate_images_pdf(
        images_io_bytes_list=qr_images_io_bytes_list,
        images_labels_list=qr_images_labels if with_labels else None,
        pdf_file_path=pdf_file_path,
        images_per_row=images_per_row,
    )


def generate_artistic_qr_codes_pdf_from_list(
        qr_codes_data_list: list,
        qr_bg_image_path: str,
        pdf_file_path: str,
        images_per_row: int = 4,
        with_labels: bool = False,
        error_correction: str = 'h',
        qr_version: int = 6,
        scale: int = 3,
        dark_color: str = 'black',
        data_dark_color: str = 'black',
        data_light_color: str = 'white',
        border_thickness: int = 1,
        kind: str = 'png',
):
    qr_images_list = []
    qr_images_labels = []

    from io import BytesIO
    for data in qr_codes_data_list:
        data = data.strip()
        if len(data) == 0:
            continue

        out = BytesIO()
        generate_artistic_qrcode(
            data=data,
            background_path=qr_bg_image_path,
            target_stream=out,
            scale=scale,
            dark_color=dark_color,
            data_dark_color=data_dark_color,
            data_light_color=data_light_color,
            border_thickness=border_thickness,
            version=qr_version,
            error_correction=error_correction,
            kind=kind,
        )

        qr_images_list.append(out)
        qr_images_labels.append(data)

    from firesoft.utils.files import generate_images_pdf
    generate_images_pdf(
        images_io_bytes_list=qr_images_list,
        images_labels_list=qr_images_labels if with_labels else None,
        pdf_file_path=pdf_file_path,
        images_per_row=images_per_row,
    )
