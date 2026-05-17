from mlxtend.frequent_patterns import apriori, association_rules

class MiningEngine:
    def __init__(self, min_support, min_confidence):
        self.min_support = min_support
        self.min_confidence = min_confidence

    def perform_apriori(self, basket_sets):
        frequent_itemsets = apriori(basket_sets, min_support=self.min_support, use_colnames=True)
        if not frequent_itemsets.empty:
            frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
            frequent_itemsets = frequent_itemsets.sort_values(by='support', ascending=False).reset_index(drop=True)
        return frequent_itemsets

    def generate_rules(self, frequent_itemsets):
        if frequent_itemsets.empty:
            return None
            
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=self.min_confidence)
        
        if not rules.empty:
            rules['antecedents_str'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
            rules['consequents_str'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
            rules['Aturan'] = "Jika membeli " + rules['antecedents_str'] + ", maka membeli " + rules['consequents_str']
            rules = rules.sort_values(by='lift', ascending=False).reset_index(drop=True)
            
        return rules
