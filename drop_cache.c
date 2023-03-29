#include <unistd.h>
#include <fcntl.h>

int main() {
  int fd = open("/proc/sys/vm/drop_caches", O_WRONLY);
  if (fd < 0) { return 1; }
  sync();
  char value = '3';
  write(fd, &value, 1);
  close(fd);
  return 0;
}
