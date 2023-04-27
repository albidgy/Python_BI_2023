class CrossingGenotypes:
    def __init__(self, genotype1, genotype2):
        self._split_genotype1 = self._split_by_chromosome_types(genotype1)
        self._split_genotype2 = self._split_by_chromosome_types(genotype2)

    @staticmethod
    def _split_by_chromosome_types(genotype):
        splitted_chromosomes = []
        possible_combinations = [[]]

        lower_genotype = genotype.lower()
        ploid = lower_genotype.count(lower_genotype[0])

        for idx in range(0, len(genotype) - 1, ploid):
            splitted_chromosomes.append([genotype[idx], genotype[idx + 1]])

        for chroms in splitted_chromosomes:
            possible_combinations = [x + [y] for x in possible_combinations for y in
                                     chroms]  # based on itertools.product()
        return possible_combinations

    def print_offspting(self):
        for haplotype1 in self._split_genotype1:
            for haplotype2 in self._split_genotype2:
                new_possible_genotype = ''.join(sorted(sorted(haplotype1 + haplotype2), key=str.lower))
                print(new_possible_genotype)

    def get_offspting_genotype_probability(self, offspring):
        count_matches = 0
        count_all_genotypes = 0

        for haplotype1 in self._split_genotype1:
            for haplotype2 in self._split_genotype2:
                count_all_genotypes += 1
                new_possible_genotype = ''.join(sorted(sorted(haplotype1 + haplotype2), key=str.lower))
                if new_possible_genotype == offspring:
                    count_matches += 1
        return count_matches / count_all_genotypes

    def get_unique_genotypes_with_substring(self, substring):
        remember_genotypes = []

        for haplotype1 in self._split_genotype1:
            for haplotype2 in self._split_genotype2:
                new_possible_genotype = ''.join(sorted(sorted(haplotype1 + haplotype2), key=str.lower))
                if substring in new_possible_genotype and new_possible_genotype not in remember_genotypes:
                    remember_genotypes.append(new_possible_genotype)
                    print(new_possible_genotype)
