/*
 * main.c
 *
 *  Created on: 2014.03.25.
 *      Author: MaSTeRFoXX
 */

#include "uart.h"
#include <avr/io.h>
#include <avr/wdt.h>
#include <util/delay.h>
#include "ip_arp_udp_tcp.h"
#include "enc28j60.h"
#include <stdlib.h>
#include <string.h>

#define ENC_RESET PD3

#define LED_ON() PORTC|=(1<<PC0)
#define LED_OFF() PORTC&=~(1<<PC0)

//webszerver demo kod alapjan teszt celbol
static uint8_t mymac[6] = {0x54,0x55,0x58,0x10,0x00,0x29};
static uint8_t myip[4] = {192,168,2,5}; // aka http://10.0.0.29/
uint8_t allxff[6]={0xff,0xff,0xff,0xff,0xff,0xff}; // all of it can be used as mac, the first 4 can be used as IP
// server listen port for www
#define MYWWWPORT 80

//frame format
//[IP0][IP1][IP2][IP3]



// global packet buffer
#define BUFFER_SIZE 550
static uint8_t buf[BUFFER_SIZE+1];


volatile uint8_t moso_H;
volatile uint8_t moso_L;
volatile uint8_t szarito_H;
volatile uint8_t szarito_L;

//GPIO meg egyeb HW beallitasok
void hw_init()
{
        // for printf
        usart_initialize();
	    stdout = &uart_output;

        //DDRC|=(1<<PC0);
        DDRD|=(1<<ENC_RESET);
        PORTD&=~(1<<ENC_RESET);
        delay(1000);         //ENC28J60 RESET pulse
        PORTD|=(1<<ENC_RESET);

		DDRB=(1<<PB2);
        //ADC init
        ADCSRA |=(1<<ADEN) |(1<<ADPS2) |(1<<ADPS1); //clk/64 az ADC clock
        //Digital input disable, nemtom kell-e de nem baj ha van
        //DIDR0 |=(1<<ADC0D) | (1<<ADC1D);  wat nem ismeri a regisztert
}

//beolvassa a jumperok allasat, ez adja az IP CIM veget, a MAC c�m veget
//ez benne is lesz a csomag elejen
uint8_t read_jumpers(void)
{
    uint8_t temp=0;
    if(!(PIND&(1<<PD6))) temp|=1;
    if(!(PIND&(1<<PD7))) temp|=2;
    if(!(PINB&(1<<PB0))) temp|=4;
    if(!(PINB&(1<<PB1))) temp|=8;

	if(temp==0) temp=17;
    return temp;
}
void delay(uint16_t k)
{
	volatile uint16_t i;
	for(;k>0;k--)
		for(i=0;i<1000;i++);

}

int main(void)
{
        uint16_t dat_p;
        uint8_t dat[]="          Mosogep.sch by SEM. SEM RULEZ! (FW by .:: FoXX::. 2014)!\0";

       	delay(100);
        hw_init();
        printf("Begin init\n");
     //   wdt_enable(WDTO_1S);
        //szint c�m beolvasasa ennek megfeleloen all be a mac es IP cim
        myip[3]=read_jumpers();
        mymac[5]=read_jumpers();
        printf("Jumpers read: %d\n", myip[3]);

        printf("Start initing ENC28\n");
        //wdt_reset();
        //initialize the hardware driver for the enc28j60
        enc28j60Init(mymac);
        printf("ENC init done\n");

        _delay_loop_1(0); // 60us
        enc28j60PhyWrite(PHLCON,0x476);
        //init the ethernet/ip layer:
        init_udp_or_www_server(mymac,myip);
        www_server_port(MYWWWPORT);
        printf("All init done\n");


        while(1)
        {
     //       wdt_reset();
			delay(100);
            //mosogep megmerese
            ADMUX = (ADMUX & 0xf0) | 0; // mosogep kivalasztasa
            _delay_ms(10); //varni a SH kapacitasra
            ADCSRA |=(1<<ADSC);                // meres start
            while(!(ADCSRA&(1<<ADIF)));    // var amig kesz nem lesz
            ADCSRA|=(1<<ADIF); //flag torlese, 1-es beirasavaol
            moso_L=ADCL;
            moso_H=ADCH;

            //szarito megmerese
            ADMUX = (ADMUX & 0xf0) | 1; // szarito kivalasztasa
            _delay_ms(10); //varni a SH kapacitasra
            ADCSRA |=(1<<ADSC);                // meres start
            while(!(ADCSRA&(1<<ADIF)));    // var amig kesz nem lesz
            ADCSRA|=(1<<ADIF); //flag torlese, 1-es beirasavaol
            szarito_L=ADCL;
            szarito_H=ADCH;

            //frame osszepakolasa
            dat[0]=myip[0];  //ip cim
            dat[1]=myip[1];
            dat[2]=myip[2];
            dat[3]=myip[3];
            dat[4]=moso_H; //mosogep_H byte
            dat[5]=moso_L; //mosogep_L byte
            dat[6]=szarito_H; //szaritogep_H byte
            dat[7]=szarito_L; //szaritogep_L byte
            printf("Got data: moso=%d szarito=%d\n", moso_H << 8 + moso_L, szarito_H<<8+szarito_L);
            send_udp(buf,dat,sizeof(dat),1234,allxff, 1234,allxff);
        }
        return (0);
}
