class Theory:

    def __init__(self):
        pass

    def machine_learning(self):
        ml = {
            "- Supervised:": "'Cleaned' data is fed into the system and it learns.",
            "- Unsupervised:": "'Unclassified' or 'dirty' data is fed into the system and the program finds patterns and learns",
            "- Reinforced": "The algorithm tests various solutions according to a goal --> This is also called Artificial Intelligence."
        }
        ai = {
            "1. Internet AI:": "It consists of user-profiling recommendation algorithms that learn from the masses of data "
                           "about what a particular person doeson the web.",
            "2. Business AI:": "his AI brings together threads in historical data anddiscover hidden correlations "
                           "between data and events. This allowsorganisations to better optimise expenses and enhance "
                           "profitability. Commonly used in the banking and insurance sectors.",
            "3. Peceptive AI:": "This AI tries to merge the virtual world with the real world. Ubiquitous sensors of the IoT "
                            "will allow AI to gain senses, accelerating AI’s evolution. This kind of AI will pave the "
                            "way for smart factories, homes, and shops, as well as intelligent consumption.",
            "4. Autonomous AI:": "This AI be able to feel and respond to the real and virtual worlds surrounding it, "
                             "move and act productively, and optimise its own actions. For instance, drones will be "
                             "able to recognise and destroy weeds growing amongst crops. Alternatively, heat-resistant "
                             "drones will extinguish fires on their own.",
        }

        print("Types of Machine learning")
        for x,y in ml.items():
            print(x,y)

        print("\nThe Four Waves of Artificial Intelligence")
        for x,y in ai.items():
            print(x, y)


