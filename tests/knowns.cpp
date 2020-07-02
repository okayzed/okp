
class Rectangle {
  int width, height;
  public:

  void set_values(int w, int h);
  Rectangle() {
    width = 20;
    height = 10; } };



void Rectangle::set_values(int w, int h) {
  width = w;
  height = h; };


int main() {
  auto r = Rectangle(); };



