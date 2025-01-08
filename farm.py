import time
import threading

class Node:
    def __init__(self, id, name, unlocked):
        self.id = id
        self.name = name
        self.unlocked = unlocked
        return None

class Edge:
    def __init__(self, id, node1, node2):
        self.id = id
        self.node1 = node1
        self.node2 = node2
        return None
    
class Graph :
    def __init__(self, list_nodes, list_edges):
        self.nodes = list_nodes
        self.edges = list_edges
    
    def get_node_by_name(self, node_name):
        for node in self.nodes:
            if node.name.lower() == node_name.lower():  
                return node
        return None

def initialize_graph():
    bakery = Node(1, "Bakery", False)
    garden = Node(2, "Garden", False)
    smoothies = Node(3, "Smoothies Shop", False)
    ice = Node(4, "Ice Cream Shop", False)

    edge1 = Edge(1, bakery, garden)
    edge2 = Edge(2, garden, smoothies)
    edge3 = Edge(3, smoothies, ice)

    list_nodes = [bakery, garden, smoothies, ice]
    list_edges = [edge1, edge2, edge3]

    graph = Graph(list_nodes, list_edges)

    return graph

def initialize_infras():
    infras = {
        "Bakery": {
            "description": "Make delicious bread & cream!", 
            "harga": 50,
            "goods": ["Bread", "Cream"], 
        },
        "Garden" : {
            "description": "Harvest strawberries & mangoes!", 
            "harga": 200,
            "goods": ["Strawberry", "Mango"], 
        },
        "Smoothies Shop": {
            "description": "Blend fresh smoothies!", 
            "harga": 500, 
            "goods": ["Strawberry Smoothies", "Mango Smoothies"], 
        },
        "Ice Cream Shop": {
            "description": "Make mouthwatering ice cream!", 
            "harga": 800,  
            "goods": ["Strawberry Ice Cream", "Mango Ice Cream"], 
        }
    }
    return infras

def initialize_inventory():
    return {
        "Milk": {"jumlah": 0, "harga": 1},
        "Wheat": {"jumlah": 0, "harga": 1},
        "Strawberry": {"jumlah": 0, "harga": 3},
        "Mango": {"jumlah": 0, "harga": 4},
        "Bread": {"jumlah": 0, "harga": 8},
        "Cream": {"jumlah": 0, "harga": 5},
        "Strawberry Smoothies": {"jumlah": 0, "harga": 10},
        "Mango Smoothies": {"jumlah": 0, "harga": 10},
        "Strawberry Ice Cream": {"jumlah": 0, "harga": 15},
        "Mango Ice Cream": {"jumlah": 0, "harga": 15},
    }

def initialize_ingredients():
    return{
        "Bread": {"Wheat": 8},
        "Cream": {"Milk": 5},
        "Strawberry Smoothies": {"Strawberry": 4},
        "Mango Smoothies": {"Mango": 4},
        "Strawberry Ice Cream": {"Strawberry Smoothies": 1, "Cream": 2},
        "Mango Ice Cream": {"Mango Smoothies": 1, "Cream": 2},
    }

timers = {}

def add_strawberry(inventory):
    inventory["Strawberry"]["jumlah"] += 1
    timers["strawberry"] = threading.Timer(3, add_strawberry, [inventory])
    timers["strawberry"].start()

def add_wheat(inventory):
    inventory["Wheat"]["jumlah"] += 1
    timers["wheat"] = threading.Timer(1, add_wheat, [inventory])
    timers["wheat"].start()

def add_milk(inventory):
    inventory["Milk"]["jumlah"] += 1
    timers["milk"] = threading.Timer(1, add_milk, [inventory])
    timers["milk"].start()


def add_mango(inventory):
    inventory["Mango"]["jumlah"] += 1
    timers["mango"] = threading.Timer(3, add_mango, [inventory])
    timers["mango"].start()

def stop_adding_stuff():
    for timer in timers.values():
        timer.cancel()
    print("Goodbye!")

def display_welcome():
    print(" ______      _____  __  __ _ ")
    print(r"|  ____/\   |  __ \|  \/  | |")
    print(r"| |__ /  \  | |__) | \  / | |")
    print(r"|  __/ /\ \ |  _  /| |\/| | |")
    print(r"| | / ____ \| | \ \| |  | |_|")
    print(r"|_|/_/    \_\_|  \_\_|  |_(_)")
    print("=================================")
    print("Welcome to Farm!\nA simple idle game where your goal is to make \na MANGO ICE CREAM.")
    print("You will be given a cow shed that produces milk \nand a patch of ground that produces wheat!")
    print("Game start!")

def display_pilihan():
    print("\nWhat do you want to do?")
    print("1. See Inventory")
    print("2. Go to the Shop")
    print("3. Create Goods")
    print("4. Exit")

def display_inventory(coins, graph, inventory):
    print()
    print("INVENTORY")
    print(f"Coins: {coins}")
    print("---Food---")
    for food, data in inventory.items():
        if data["jumlah"] != 0:
            print(f"{food}: {data["jumlah"]}")
    print("---Store---")
    for node in graph.nodes:
        if node.unlocked:
            print(f"{node.name}")
    print()

def display_shop():
    print()
    print("SHOP")
    print("1. Buy Infrastructures")
    print("2. Sell Goods")
    print("3. Back")

def display_locked_infras(coins, graph, infras):
    print()
    print("\nBUY INFRASTRUCTURES")
    print(f"Coins: {coins}")
    for node in graph.nodes:
        if not node.unlocked:
            print(f"- {node.name} : {infras[node.name]['harga']} coins")
            print(f"  {infras[node.name]['description']}")
    store = input("Which one do you want to buy? ")
    if store not in infras:
        print(f"{store} is not in list.")
        return None
    return store

def can_buy_infras(graph, store):
    node = graph.get_node_by_name(store)
    if not node:
        print("Invalid input. Store not found.")
        return False

    for edge in graph.edges:
        if edge.node2 == node:
            predecessor = edge.node1
            if not predecessor.unlocked:
                print(f"You must buy {predecessor.name} before purchasing {store}.")
                return False

    return True

def buy_infras(coins, graph, infras, store):
    if not store:
        print("No store selected.")
        return coins
    node = graph.get_node_by_name(store)
    if not node:
        print("Invalid input. Store not found.")
        return coins
    if node.unlocked:  
        print(f"{store} is already purchased.")
    else :
        if (can_buy_infras(graph, store)):
            if coins >= infras[store]['harga']: 
                node.unlocked = True 
                coins -= infras[store]['harga']  
                print(f"You bought {store}!")
                return coins
            else:
                print("Your coins are insufficient.")
                return coins

def sell_goods(coins, graph, inventory):
    display_inventory(coins, graph, inventory)
    goodies = ""
    while goodies not in inventory:
        goodies = input("Which one do you want to sell? ")
        if goodies not in inventory:
            print("Invalid item. Please choose an item from your inventory.")

    qty = -1
    while qty < 1 or qty > inventory[goodies]["jumlah"]:
        qty_input = input(f"How many of {goodies} do you want to sell? ")
        if qty_input.isdigit():
            qty = int(qty_input)
            if qty < 1 or qty > inventory[goodies]["jumlah"]:
                print(f"Invalid quantity. You have {inventory[goodies]['jumlah']} {goodies}.")
        else:
            print("Please enter a valid number.")

    new_coins = inventory[goodies]["harga"] * qty
    coins += new_coins
    inventory[goodies]["jumlah"] -= qty
    print(f"You sold {qty} {goodies} for {new_coins} coins!")
    return coins

def can_create_goods(inventory, goods, ingredients, qty):
    if qty<= 0 :
        print("The amount of goods can't be less or equal with zero")
        return False
    else :
        for bahan in ingredients[goods]:
            if inventory[bahan]["jumlah"] < ingredients[goods][bahan] * qty:
                print("Ingredients aren't sufficient.")
                return False 
        return True  

def display_create_goods(graph, ingredients, infras, inventory):
    print("\n---AVAILABLE INFRASTRUCTURES---")
    for node in graph.nodes:
        if node.unlocked and node.name != "Garden":
            print(f"\n{node.name}:")
            print(f"- {infras[node.name]['goods'][0]}")
            print(f"Ingredients: {ingredients[infras[node.name]['goods'][0]]}")
            print(f"- {infras[node.name]['goods'][1]}")
            print(f"Ingredients: {ingredients[infras[node.name]['goods'][1]]}")

    chosen_infra = input("Which infrastructure do you want to use? ")
    if chosen_infra not in infras:
        print(f"{chosen_infra} is not a valid infrastructure.")
        return None, 0

    print(f"---{chosen_infra}---")
    print(f"- {infras[chosen_infra]['goods'][0]}")
    print(f"Ingredients: {ingredients[infras[chosen_infra]['goods'][0]]}")
    print(f"- {infras[chosen_infra]['goods'][1]}")
    print(f"Ingredients: {ingredients[infras[chosen_infra]['goods'][1]]}")

    goods = input("What do you want to make? ")
    while goods not in infras[chosen_infra]['goods']:
        print(f"{goods} isn't in the list of goods.")
        goods = input("What do you want to make? ")

    qty = int(input(f"How many of {goods} do you want to make? "))
    while not can_create_goods(inventory, goods, ingredients, qty):
        qty = int(input(f"How many of {goods} do you want to make? "))
        
    return goods, qty


def create_goods(goods, qty, inventory, ingredients):
    for bahan in ingredients[goods]:
        inventory[bahan]["jumlah"] -= ingredients[goods][bahan] * qty  
    inventory[goods]["jumlah"] += qty  
    print(f"Successfully created {qty} {goods}.")

def main():
    coins = 0
    graph = initialize_graph()
    infras = initialize_infras()
    inventory = initialize_inventory()
    ingredients = initialize_ingredients()
    display_welcome()
    
    add_wheat(inventory)
    add_milk(inventory)
    add_fruits = False

    pilihan = 0
    while pilihan != 4:
        display_pilihan()
        pilihan_input = input("Insert a number: ")
        if pilihan_input.isdigit():
            pilihan = int(pilihan_input)
            if pilihan == 1:
                display_inventory(coins, graph, inventory)
            elif pilihan == 2:
                display_shop()
                pilihan_shop = input("Choose a number: ")
                if pilihan_shop.isdigit():
                    pilihan_shop = int(pilihan_shop)
                    if pilihan_shop == 1:
                        store = display_locked_infras(coins, graph, infras)
                        coins = buy_infras(coins, graph, infras, store)
                    elif pilihan_shop == 2:
                        coins = sell_goods(coins, graph, inventory)
                    elif pilihan_shop == 3:
                        print("Returning to main menu.")
                    else:
                        print("Invalid choice. Returning to main menu.")
                else:
                    print("Invalid input. Returning to main menu.")
            elif pilihan == 3:
                goods, qty = display_create_goods(graph,  ingredients, infras, inventory)
                if can_create_goods(inventory, goods, ingredients, qty):
                    create_goods(goods, qty, inventory, ingredients)
                else:
                    print("Not enough ingredients to create the goods.")

        gardenNode = graph.get_node_by_name("Garden")
        if (gardenNode.unlocked) and (not add_fruits) :
            add_mango(inventory)
            add_strawberry(inventory)
            add_fruits = True

        if (inventory["Mango Ice Cream"]["jumlah"] >= 1):
            print("CONGRATS, YOU WON THE GAME!")
            pilihan = 4

    stop_adding_stuff()

if __name__ == "__main__":
    main()
