import support

import speedster

supportUnit = support.Support(15,25)

speedy = speedster.Speedster(80,150)


print speedy.selected

speedy.selected = True

print speedy.selected

print speedy.speed

speedy.speed = 100

print speedy.speed


print speedy.position()
