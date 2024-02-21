FROM python
ENV PYTHONUNBUFFERED 1
RUN mkdir /hotel_booking
WORKDIR /hotel_booking
ADD . /hotel_booking/
RUN pip install -r requirements.txt