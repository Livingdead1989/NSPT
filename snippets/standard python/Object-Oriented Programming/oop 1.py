## Object-Oriented Programing

## Class            A blueprint for creating objects of a particular type
## Methods          Regular functions that are part of a class
## Attributes       Variables that hold dat that are part of a class
## Object           A specific instance of a class
## Inheritance      Means by which a class can inherit capabilities from another
## Composition      Means of building complex objects out of other objects

## Basic class
class Book:  
    def __init__(self, title, author, pages, price): ## Initial the new object.
        self.title = title
        self.author = author
        self.pages = pages
        self.price = price
        self.__secret = 'This is a secret' ## double underscore can prevent subclasses from overriding

    def getprice(self):
        if hasattr(self, '_discount'):
            return self.price - (self.price * self._discount)
        else:
            return self.price

    def setdiscount(self, amount):
        self._discount = amount ## _discount means its internal to this class

## Create instances of the class
b1 = Book("Brave New Wolrd", "Leo Tolstroy", 1225, 39.95)
b2 = Book("War and Peace", "JD Salinger", 234, 29.95)

## Print the class and property
print(b1.getprice())

print(b2.getprice())
b2.setdiscount(0.50) ## Add 50% discount
print(b2.getprice())

## Properties with double underscores are hidden
#print(b1.__secret) ## Reports an error
#print(b1._Book__secret) ## Bypass