* [ ] Refactor to use classes for locations, with play() method and objects property.

## Help

You are a Scottish general returning from victory in battle. The aim of the game is to fulfil your ambition for power and glory!

In each scene you will find some objects. Some will be useful and help you on your quest.

To look at an object, type the name of the object and press return. For example, to look at the newspaper, type newspaper.

To get a hint about how an object might be used, type help(X) where X is the name of the object. For example, type help(newspaper).

To use an object, type use(X) where X is the name of the object. For example, type use(newspaper). 

To take an object with you, type take(X) where X is the name of the object. For example, type take(newspaper).

At any point in the game you can sing() if you feel like it.

Good luck, brave pilgrim!

### Outside

You are standing outside a castle. 

Objects available: newspaper, torch, door

* use(door) -> Hall
* sing() -> ?

### Hall (unlit)

It's very dark in here. I can't see anything.

Objects available: door

* use(torch) -> Hall (lit)
* sing() -> Bohemian Rhapsody -> Ceiling falls down. Castles aren't built the way the used to.

### Hall (lit)

Objects available: log, stair, tunnel

* use(tunnel) -> Dungeon
* use(stair) -> King's Bedroom (no dagger)

### Dungeon (witches)

Objects available: tunnel, witches

* use(log) -> prophecy -> Dungeon (no witches)
* use(tunnel) -> Hall
* sing() -> Ding Ding the Witch is Dead -> Witches turn you into a toad.

### Dungeon (no witches)

Objects available: tunnel

* use(tunnel) -> Hall (prophecy)

### Hall (prophecy)

Is this a dagger I see before me?

Objects available: dagger, stair, tunnel

* use(stair) -> King's Bedroom

### King's Bedroom (no dagger)

Objects available: king, computer, door

* use(computer) -> Mainframe
* use(door) -> Battlements (no snake)
* sing() -> Nederpop -> King banishes you.

### King's Bedroom (dagger)

Objects available: king, computer, door

* use(dagger) -> destroy computer -> King's Bedroom (snake)
* take(snake) -> King's Bedroom (snake)

### King's Bedroom (snake)

TODO

* use(door) -> Battlements (snake)

### Battlements (no snake)

It's nice out here in the fresh air.

Objects available: telescope

* use(telescope) -> see forest in the distance

### Battlements (snake)

Standing in the fresh air, feel the power of the snake, feel ambition.

Objects available: snake, telescope

* use(snake) -> become king -> Battlements (king)

### Battlements (king)

You stand as king. Forest is moving towards the castle. It is an army of trees!

* sing() -> lumberjack song -> trees run away