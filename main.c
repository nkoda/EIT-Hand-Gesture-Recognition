
/******************************************************************************
 *                  MSP-EXP430G2-LaunchPad User Experience Application
 *
 * 1. Device starts up in LPM3 + blinking LED to indicate device is alive    
 *    + Upon first button press, device transitions to application mode
 * 2. Application Mode
 *    + Continuously sample ADC Temp Sensor channel
 *       
 *    + Transmit temperature value via TimerA UART to PC  
 * 
 *
 * Texas Instruments, Inc.
 ******************************************************************************/
  
#include  "msp430.h"

#define     LED1                  BIT0
#define     LED2                  BIT6

#define     BUTTON                BIT0

#define     TXD                   BIT2                      // TXD on P1.2
#define     RXD                   BIT1                      // RXD on P1.1

#define     E3                    BIT3
#define     E4                    BIT4
#define     E5                    BIT5
#define     E6                    BIT6
#define     E7                    BIT7

#define     PreAppMode            0
#define     RunningMode           1

unsigned int TXByte;
volatile unsigned int Mode;   
  
void InitializeButton(void);
void PreApplicationMode(void); 

void main(void)
{
  unsigned int endTime;

  WDTCTL = WDTPW + WDTHOLD;                 // Stop WDT

  /* next three lines to use internal calibrated 1MHz clock: */
  BCSCTL1 = CALBC1_1MHZ;                    // Set range
  DCOCTL = CALDCO_1MHZ;
  BCSCTL2 &= ~(DIVS_3);                     // SMCLK = DCO = 1MHz  

  //InitializeButton();
  int listOfElectrodes[5] = {E3, E4, E5, E6, E7};

  // setup port for leds:
  P1DIR |= LED1 + LED2;                          
  P1OUT &= ~(LED1 + LED2); 

  P1DIR |= TXD;
  P1OUT |= TXD;
  
  Mode = PreAppMode;
  PreApplicationMode();          // Blinks LEDs, waits for button press
  
  /* Configure ADC Temp Sensor Channel */

  ADC10CTL0 = ADC10SHT_2 + ADC10ON;       // ADC10ON
  ADC10CTL1 = INCH_4;            // input A4
  // ADC10AE0 |= E1;    

  __delay_cycles(1000);                     // Wait for ADC Ref to settle  

  /* Configure hardware UART */
  P1SEL = BIT1 + BIT2 ; // P1.1 = RXD, P1.2=TXD
  P1SEL2 = BIT1 + BIT2 ; // P1.1 = RXD, P1.2=TXD
  UCA0CTL1 |= UCSSEL_2; // Use SMCLK
  UCA0BR0 = 104; // Set baud rate to 9600 with 1MHz clock (Data Sheet 15.3.13)
  UCA0BR1 = 0; // Set baud rate to 9600 with 1MHz clock
  UCA0MCTL = UCBRS0; // Modulation UCBRSx = 1
  UCA0CTL1 &= ~UCSWRST; // Initialize USCI state machine
  /* if we were going to receive, we would also:
     IE2 |= UCA0RXIE; // Enable USCI_A0 RX interrupt
  */

  P1OUT |= LED1 + LED2;
  while((P2IN & BUTTON));
  while(!(P2IN & BUTTON));
  
  
  int count = 0;
  /* Main Application Loop */
  while(1)
  {    
    ADC10AE0 |= listOfElectrodes[count];            
    ADC10CTL0 |= ENC + ADC10SC;        // Sampling and conversion start
    while (ADC10CTL1 &ADC10BUSY);          // ADC10BUSY?
      
    // convert to farenheit and send to host computer
    TXByte = (unsigned char) (ADC10MEM /2.84);
    while (! (IFG2 & UCA0TXIFG)); // wait for TX buffer to be ready for new data
    UCA0TXBUF = TXByte;

    P1OUT ^= LED1;  // toggle the light every time we make a measurement.
        
    // set up timer to wake us in a while:
    TACCR0 = 2400;                             //  period
    TACTL = TASSEL_1 | MC_1;                   // TACLK = ACLK, Up mode.  
    TACCR1 = 2400;                             // interrupt at end
    TACCTL1 = CCIE;                            // TACCTL0 

    // could have just done this - but low power mode is nicer.
    __delay_cycles(64000);  
    ADC10AE0 &= ~listOfElectrodes[count];     
    count++;
    if (count > 5) {count = 0;}
  }  
}

void PreApplicationMode(void)
{       
  /* these next two lines configure the ACLK signal to come from 
     a secondary oscillator source, called VLO */

  BCSCTL1 |= DIVA_1;             // ACLK is half the speed of the source (VLO)
  BCSCTL3 |= LFXT1S_2;           // ACLK = VLO
  
  /* here we're setting up a timer to fire an interrupt periodically. 
     When the timer 1 hits its limit, the interrupt will toggle the lights 

     We're using ACLK as the timer source, since it lets us go into LPM3
     (where SMCLK and MCLK are turned off). */

  TACCR0 = 1200;                 //  period
  TACTL = TASSEL_1 | MC_1;       // TACLK = ACLK, Up mode.  
  TACCTL1 = CCIE + OUTMOD_3;     // TACCTL1 Capture Compare
  TACCR1 = 600;                  // duty cycle

}
