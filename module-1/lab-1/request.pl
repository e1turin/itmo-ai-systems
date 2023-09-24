level(20). 
%false

is_friends('Denstep', 'Le Potat'). 
% true.
is_frienda('Le Potat', X). 
% X = 'Denstep'; X = 'Any623'; X = 'Patient'; X = 'Pandushka'.

same_level('Denstep', X), X \= 'Denstep'. 
% X = 'Bedrosik'; X = 'Jorik'.

findall(Level, can_get_level('Le Potat', Level), List), list_to_set(List, Set). 
% Set = [10, 11, 12, 13, 14].




