#include <iostream>

template <class T>
constexpr T pi = static_cast<T>(3.1415926535897932385);

template <class T>
T area_of_circle_with_radius(T r) 
{
    return pi<T> * r * r;
}

int main() {
    double radius = 5.0;
    double area = area_of_circle_with_radius(radius);
    
    std::cout << "半径 " << radius << " の円の面積: " << area << std::endl;
    
    return 0;
}