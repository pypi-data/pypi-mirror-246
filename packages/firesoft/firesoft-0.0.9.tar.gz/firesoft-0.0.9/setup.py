from setuptools import setup

setup(
    name='firesoft',
    version='0.0.9',
    packages=['firesoft', 'firesoft.utils'],
    install_requires=[
        "segno==1.5.3",
        "qrcode-artistic==3.0.0",
        "Pillow==10.1.0",
        "setuptools==68.2.2",
        "python-barcode==0.15.1",
        "pyzbar==0.1.9",
        "pandas==2.0.3",
        "reportlab==4.0.6"
    ],
    url='',
    license='',
    author='Salah Anwer',
    author_email='salahanwer.dev@gmail.com',
    description='',
    python_requires=">=3",
)
