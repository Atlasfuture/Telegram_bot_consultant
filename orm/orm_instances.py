from orm.orm_smartphones import Brand, Smartphone
from orm.orm_engine import session


"""Creating brand instances"""

brand_instances = [
        Brand(name = 'Apple', description = "Make good iOS smartphones - iPhones"),

        Brand(name = 'Samsung', description = "Devices for all tastes"),

        Brand(name = 'Xiaomi', description = "Cheap and powerfull devices"),

        Brand(name = "Meizu", description = "Good styled smartphones for a good prices")
    ]





smartphones_instances = [
    Smartphone(name = "iPhone", description = "Double camera. Animodji. Optical Zoom.",
               os = "iOS", price = 800, video = 3, photo = 2, battery = 1, performance = 3,
               screen = 2, brand_id = brand_instances[0].id),

    Smartphone(name = "Xiaomi Redmi Note 4x", description = "Finger print sensor.",
               os = "Android", price = 250, video = 0, photo = 1, battery = 3, performance = 1,
               screen = 1, brand_id = brand_instances[2].id),

    Smartphone(name = "Samsung Galaxy S9", description = "Double camera. Animodji. Best screen and camera.",
               os = "Android", price = 1000, video = 3, photo = 3, battery = 2, performance = 2,
               screen = 3, brand_id = brand_instances[1].id),

    Smartphone(name = "Meizu M1", description = "Good cheap smartphone.",
               os = "Android", price = 150, video = 0, photo = 1, battery = 2, performance = 1,
               screen = 1, brand_id = brand_instances[3].id),
]


if __name__ == '__main__':
    session.add_all(brand_instances)
    session.commit()

    session.add_all(smartphones_instances)
    session.commit()