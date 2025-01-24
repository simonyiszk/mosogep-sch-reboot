CC=avr-gcc
OBJCOPY=avr-objcopy

CFLAGS=-Os -DF_CPU=1000000UL -mmcu=atmega168 -DDEBUG=1


%.hex: %.elf
	${OBJCOPY} -O ihex -R .eeprom $< $@

mosogep_probalkozas.elf: mosogep_probalkozas.o enc28j60.o ip_arp_udp_tcp.o uart.o
	${CC} -o $@ $^ $(CFLAGS)

clean:
	rm -f *.elf *.o *.hex

flash: mosogep_probalkozas.elf
	avrdude -V -p m168 -c usbasp -U flash:w:mosogep_probalkozas.elf

fuse: mosogep_probalkozas.elf
	avrdude -p m168 -c usbasp -U lfuse:w:mosogep_probalkozas.elf -U hfuse:w:mosogep_probalkozas.elf -U efuse:w:mosogep_probalkozas.elf