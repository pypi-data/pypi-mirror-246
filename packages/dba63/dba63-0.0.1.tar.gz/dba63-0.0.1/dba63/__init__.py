class PandasIntroduction:

    def __init__(self):
        self.attributes = None
        self.methods = None
        self.attributes = None

    def pretty_print(self, d):
        for x, y in d.items():
            print(x, "--", y)

    def show(self):
        print("Attributes")
        self.pretty_print(self.attributes)
        print("\nMethods")
        self.pretty_print(self.methods)
        print("\nUsage")
        self.pretty_print(self.usage)

    def load_and_inspect(self):
        self.attributes = {
            "df.columns": "return column names",
            "df.info()": "return column names + info",
        }
        self.methods = {
            ".astype(str)": "convert to type str",
            "df.describe(include='column_name')": "include parameter an be used to include non-numerical columns",
            ".value_counts(normalize=True)": "count the values of non-numerical column, Use 'normalize=True' to calculate fractions",
            ".sort_values(by=[column_names], ascending=[True/False])": "sort dataframe by column name.Use parameter 'ascending=False' to sort in decresing order.Use inplace=True to save chqnge",
        }
        self.usage = {
            "df['column1', 'column2'']": "access columns 1 and 2",
        }
        self.show()

    def indexing_and_selecting(self):
        self.attributes = {
        }

        self.methods = {
            "df.loc[:, 'column_name']": "selecting all rows "
        }
        self.usage = {
            "df[:4]": "selecting first 4 rows",
            "df['column_name'] or df.column_name": "selecting column",
            "df[df.Age == 18]": "selecting rows based on conditional statement",
            "df[:n]['column_name]": "selecting a combination of n rows of column 'column_name'",
        }
        self.show()

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


