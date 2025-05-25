CC=gcc
CFLAGS=-Wall -O2
TARGET=quicksort

all: $(TARGET)

$(TARGET): quicksort.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)

.PHONY: all clean 