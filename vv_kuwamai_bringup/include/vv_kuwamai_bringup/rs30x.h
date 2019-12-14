#ifndef RS30X_HPP_
#define RS30X_HPP_

#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <termios.h>
#include <unistd.h>

#define SERIAL_PORT "/dev/ttyUSB0"
#define BAUDRATE B115200

class rs30x
{
    public:
        rs30x();
        char get_check_sum(char *com, int buf_size);
        void servo_torque_set(int servo_id, bool mode);
        void move_target_degree(int servo_id, float degree);
        void setAngleInTime(int servo_id, float degree, int time);
        void change_id(int servo_id, int changed_id);
        void close_port();
    private:
        int fd;
};

#endif
