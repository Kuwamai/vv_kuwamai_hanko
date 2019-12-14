#include "vv_kuwamai_bringup/rs30x.h"
#include <stdio.h>

rs30x::rs30x()
{
    char *com;
    struct termios tio;

    fd = open(SERIAL_PORT, O_RDWR);

    tio.c_cflag = (BAUDRATE | CS8 | CLOCAL | CREAD);
    tio.c_iflag = (IGNPAR);
    tio.c_oflag = 0;
    tio.c_lflag = ICANON;

    ioctl(fd, TCSETS, &tio);
}

char rs30x::get_check_sum(char *com, int buf_size)
{
    int i;
    char check_sum;

    check_sum = com[2];

    for (i = 3; i < buf_size - 1; i++)
    {
        check_sum = (char)(check_sum ^ com[i]);
    }
    return check_sum;
}

void rs30x::servo_torque_set(int servo_id, bool mode)
{
    int i = 0;
    char com[9];

    com[i++] = (char)0xFA; //Header
    com[i++] = (char)0xAF; //Header
    com[i++] = (char)servo_id; //ID
    com[i++] = (char)0;	//Flag
    com[i++] = (char)0x24; //Torque map address
    com[i++] = (char)0x01; //length
    com[i++] = (char)0x01; //count

    if(mode) com[i++] = (char)0x01;
    else com[i++] = (char)0;

    com[i++] = rs30x::get_check_sum(com, i+1);

    if(com !=NULL) write(fd, com, i);
}

void rs30x::move_target_degree(int servo_id, float degree)
{
    char com[10];
    char l_bit;
    char h_bit;
    int target; // target degree
    int i = 0;

    //data calculation
    target =(int)degree*10;
    h_bit = (char)((target & 0xFF00) >> 8);
    l_bit = (char)(target & 0xFF);

    // packet set
    com[i++] = 0xFA; //Header
    com[i++] = 0xAF; //Header
    com[i++] = (char)servo_id; //ID
    com[i++] = 0x00; //Flag
    com[i++] = 0x1E; //map address
    com[i++] = 0x02; //length
    com[i++] = 0x01; //count
    com[i++] = l_bit; //data lower
    com[i++] = h_bit; //data higher
    com[i++] = rs30x::get_check_sum(com, i+1);

    if(fd) write(fd, com, i);
}

void rs30x::setAngleInTime(int servo_id, float degree, int time)
{
    char com[15];
    char l_bit;
    char h_bit;
    int i = 0;

    //data calculation
    h_bit = (char)(((int)degree * 10 & 0xFF00) >> 8);
    l_bit = (char)((int)degree * 10 & 0xFF);

    // packet set
    com[i++] = 0xFA; //Header
    com[i++] = 0xAF; //Header
    com[i++] = (char)servo_id; //ID
    com[i++] = 0x00; //Flag
    com[i++] = 0x1E; //map address
    com[i++] = 0x04; //length
    com[i++] = 0x01; //count
    com[i++] = l_bit; //data lower
    com[i++] = h_bit; //data higher
    com[i++] = (char)(time / 10 & 0xFF);
    com[i++] = (char)((time / 10 & 0xFF00) >> 8);
    com[i++] = rs30x::get_check_sum(com, i+1);

    if(fd) write(fd, com, i);
}

void rs30x::change_id(int servo_id, int changed_id)
{
    char com[10];
    int i = 0;

    // packet set
    com[i++] = 0xFA; //Header
    com[i++] = 0xAF; //Header
    com[i++] = (char)servo_id; //ID
    com[i++] = 0x00; //Flag
    com[i++] = 0x04; //map address
    com[i++] = 0x01; //length
    com[i++] = 0x01; //count
    com[i++] = (char)changed_id; //dat
    com[i++] = rs30x::get_check_sum(com, i+1);

    if(fd) write(fd, com, i);

    i = 0;

    com[i++] = 0xFA; //Header
    com[i++] = 0xAF; //Header
    com[i++] = (char)changed_id; //ID
    com[i++] = 0x40; //Flag
    com[i++] = 0xFF; //map address
    com[i++] = 0x00; //length
    com[i++] = 0x00; //count
    com[i++] = rs30x::get_check_sum(com, i+1);

    if(fd) write(fd, com, i);
}

void rs30x::close_port()
{
    close(fd);
}
